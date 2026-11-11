
import os
import time
import html
import logging
import json5
import requests

from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from dotenv import load_dotenv

# ==========================================
# LOGGING
# ==========================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("api-monitor")


# ==========================================
# CONFIGURATION
# ==========================================

BASE_DIR = Path(__file__).resolve().parent

CONFIG_FILE = BASE_DIR / "config.jsonc"
ENV_FILE = BASE_DIR / ".env"

# Load environment variables
load_dotenv(ENV_FILE)


# ==========================================
# LOAD CONFIGURATION
# ==========================================

def load_config():

    if not CONFIG_FILE.exists():
        raise FileNotFoundError(
            f"Configuration file not found: {CONFIG_FILE}"
        )

    with open(CONFIG_FILE, "r", encoding="utf-8") as file:
        config = json5.load(file)

    if not config.get("apis"):
        raise ValueError("No APIs configured.")

    if not os.getenv("TELEGRAM_BOT_TOKEN"):
        raise ValueError("Telegram bot token is missing.")

    if not os.getenv("TELEGRAM_CHAT_ID"):
        raise ValueError("Telegram chat ID is missing.")

    logger.info("Configuration loaded successfully.")

    return config


# ==========================================
# API HEALTH CHECK
# ==========================================

def check_api(api, monitor_config):

    name = api["name"]
    url = api["url"]

    timeout = monitor_config["timeout_seconds"]
    success_codes = monitor_config["success_status_codes"]

    start = time.perf_counter()

    try:
        response = requests.get(
            url,
            timeout=timeout,
            allow_redirects=True
        )

        elapsed = round(
            (time.perf_counter() - start) * 1000
        )

        online = response.status_code in success_codes

        return {
            "name": name,
            "status": "ONLINE" if online else "OFFLINE",
            "http": response.status_code,
            "response_time": elapsed,
            "error": None
        }

    except requests.RequestException as error:

        logger.warning("Failed to check %s: %s", name, error)

        return {
            "name": name,
            "status": "OFFLINE",
            "http": None,
            "response_time": None,
            "error": str(error)
        }


# ==========================================
# MONITORING
# ==========================================

def monitor_apis(config):

    enabled_apis = [
        api for api in config["apis"]
        if api.get("enabled", True)
    ]

    results = []

    for api in enabled_apis:

        logger.info("Checking API: %s", api["name"])

        result = check_api(
            api,
            config["monitor"]
        )

        results.append(result)

        logger.info(
            "%s status: %s",
            result["name"],
            result["status"]
        )

    return results


# ==========================================
# REPORT GENERATION
# ==========================================

def build_report(results, config):

    settings = config["report"]

    timezone = ZoneInfo(
        config["monitor"]["timezone"]
    )

    now = datetime.now(timezone)

    lines = [
        html.escape(settings["title"])
    ]

    if settings.get("show_date", True):
        lines.extend([
            "",
            f"🕒 {now.strftime('%d/%m/%Y %H:%M:%S')}"
        ])

    lines.append("")

    for item in results:

        emoji = (
            settings["online_emoji"]
            if item["status"] == "ONLINE"
            else settings["offline_emoji"]
        )

        lines.append(
            f'{emoji} <b>{html.escape(item["name"])}</b>'
        )

        lines.append(
            f'Status: {item["status"]}'
        )

        if settings.get("show_http_status", True):
            lines.append(
                f'HTTP: {item["http"] or "N/A"}'
            )

        if settings.get("show_response_time", True):
            latency = item["response_time"]

            lines.append(
                f"Response time: {latency} ms"
                if latency is not None
                else "Response time: N/A"
            )

        if item["error"]:
            lines.append(
                f'{settings["error_emoji"]} Connection error'
            )

        lines.append("")

    if settings.get("show_summary", True):

        online = sum(
            1 for item in results
            if item["status"] == "ONLINE"
        )

        offline = len(results) - online

        lines.extend([
            "━━━━━━━━━━━━━━━━━━",
            f"🟢 Online: {online}",
            f"🔴 Offline: {offline}",
            f"📡 Total: {len(results)}"
        ])

    footer = settings.get("footer")

    if footer:
        lines.extend([
            "",
            html.escape(footer)
        ])

    return "\n".join(lines)


# ==========================================
# TELEGRAM NOTIFICATIONS
# ==========================================

def send_telegram(message):

    token = os.environ["TELEGRAM_BOT_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]

    url = (
        f"https://api.telegram.org/"
        f"bot{token}/sendMessage"
    )

    response = requests.post(
        url,
        json={
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "HTML"
        },
        timeout=20
    )

    response.raise_for_status()

    data = response.json()

    if not data.get("ok"):
        raise RuntimeError("Telegram message delivery failed.")

    logger.info("Telegram report sent successfully.")


# ==========================================
# MAIN
# ==========================================

def main():

    logger.info("Starting API Monitor...")

    config = load_config()

    results = monitor_apis(config)

    if not results:
        raise ValueError("No enabled APIs found.")

    message = build_report(results, config)

    send_telegram(message)

    logger.info("Monitoring completed successfully.")


if __name__ == "__main__":
    main()