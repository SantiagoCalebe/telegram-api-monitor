# API Monitor Telegram

A lightweight API monitoring system built with Python, Telegram Bot API, and GitHub Actions.

Automatically monitor up to **5 APIs** and receive hourly status reports directly on Telegram.

## Features

- Monitor up to 5 APIs.
- Automatic HTTP health checks.
- ONLINE and OFFLINE status detection.
- HTTP status code monitoring.
- Response time measurement.
- Configurable request timeout.
- Customizable Telegram notifications.
- Hourly monitoring with GitHub Actions.
- Manual workflow execution.
- JSONC configuration with comments.
- Environment variables managed through `.env`.
- No VPS or dedicated server required.
- No database required.

## Architecture

The project uses GitHub Actions to execute the Python monitoring script every hour.

text

```text
GitHub Actions
      |
      v
  Python App
      |
      v
  config.jsonc
      |
      v
 API Health Checks
      |
      v
 Report Generator
      |
      v
 Telegram Bot API
      |
      v
 Telegram Chat
```

## Project Structure

text

```text
api-monitor-telegram/
├── .github/
│   └── workflows/
│       └── monitor.yml
├── config.jsonc
├── .env
├── .env.example
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Requirements

- Python 3.12 or newer.
- GitHub account.
- Telegram account.
- Telegram bot created through BotFather.

## 1\. Create a Telegram Bot

Telegram provides a free Bot API.

### Step 1: Open BotFather

Visit:

[https://t.me/BotFather](<https://t.me/BotFather>)

### Step 2: Create your bot

Send the following command:

text

```text
/newbot
```

### Step 3: Choose a bot name

Example:

text

```text
API Monitor
```

### Step 4: Choose a username

The username must end with `bot`.

Example:

text

```text
my_api_monitor_bot
```

### Step 5: Get your bot token

BotFather will generate an API token.

Example:

text

```text
123456789:AAExampleToken123456789
```

Save this token securely.

> **Important:** Never share your bot token or commit it to GitHub.

## 2\. Get Your Telegram Chat ID

The bot needs your numerical Chat ID to know where to send notifications.

### Step 1: Open your bot

Search for your bot username in Telegram.

### Step 2: Start the conversation

Click **Start** or send:

text

```text
/start
```

Then send any message, for example:

text

```text
Hello!
```

### Step 3: Retrieve your Chat ID

Open the following URL in your browser:

text

```text
https://api.telegram.org/botYOUR_BOT_TOKEN/getUpdates
```

Replace `YOUR_BOT_TOKEN` with your actual bot token.

Look for:

json

```json
{
  "message": {
    "chat": {
      "id": 123456789,
      "type": "private"
    }
  }
}
```

Your Chat ID is:

text

```text
123456789
```

> **Note:** Telegram bots use numerical Chat IDs for private conversations. A personal username or phone number cannot be used directly as the `chat_id` parameter.

## 3\. Install Python

Download Python from:

[https://www.python.org/downloads/](<https://www.python.org/downloads/>)

During installation, enable:

text

```text
Add Python to PATH
```

Verify the installation:

bash

```bash
python --version
```

## 4\. Create the Project Environment

Open a terminal inside the project directory.

### Create a virtual environment

bash

```bash
python -m venv .venv
```

### Activate it on Windows CMD

cmd

```cmd
.venv\Scripts\activate
```

### Activate it on PowerShell

powershell

```powershell
.\.venv\Scripts\Activate.ps1
```

### Install the dependencies

bash

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 5\. Configure Environment Variables

Create a `.env` file in the project root.

dotenv

```dotenv
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

Replace the example values with your actual credentials.

### Environment Variables

| Variable | Description |
| --- | --- |
| `TELEGRAM_BOT_TOKEN` | Telegram bot authentication token |
| `TELEGRAM_CHAT_ID` | Destination chat identifier |

The `.env` file is used for local development.

For GitHub Actions, credentials must be configured using GitHub Secrets.

## 6\. Configure API Monitoring

Open `config.jsonc`.

This file controls the monitored APIs and notification settings.

### Monitoring Configuration

jsonc

```jsonc
{
  "monitor": {
    // Interval between checks (minutes)
    "interval_minutes": 60,

    // Report timezone
    "timezone": "America/Sao_Paulo",

    // Maximum request timeout
    "timeout_seconds": 15,

    // Successful HTTP status codes
    "success_status_codes": [
      200,
      201,
      202,
      204
    ]
  }
}
```

### API Configuration

Add your API endpoints inside the `apis` array.

jsonc

```jsonc
{
  "apis": [
    {
      "name": "Customers API",
      "url": "https://api.example.com/health",
      "enabled": true
    },
    {
      "name": "Finance API",
      "url": "https://finance.example.com/health",
      "enabled": true
    },
    {
      "name": "Orders API",
      "url": "https://orders.example.com/health",
      "enabled": true
    },
    {
      "name": "Authentication API",
      "url": "https://auth.example.com/health",
      "enabled": true
    },
    {
      "name": "Products API",
      "url": "https://products.example.com/health",
      "enabled": true
    }
  ]
}
```

Replace the example URLs with your actual API health-check endpoints.

You can add, remove, or disable APIs without modifying `app.py`.

### API Configuration Options

| Property | Description |
| --- | --- |
| `name` | API display name |
| `url` | API endpoint |
| `enabled` | Enables or disables monitoring |

### Report Customization

The `report` section allows you to customize Telegram messages.

jsonc

```jsonc
{
  "report": {
    "title": "API MONITORING REPORT",
    "show_date": true,
    "show_http_status": true,
    "show_response_time": true,
    "show_summary": true,
    "online_emoji": "🟢",
    "offline_emoji": "🔴",
    "error_emoji": "⚠️",
    "footer": "API Monitor Bot"
  }
}
```

You can enable or disable individual report sections without changing the Python code.

## 7\. Run Locally

Make sure your virtual environment is activated and your `.env` file is configured.

Execute:

bash

```bash
python app.py
```

The application will:

1. Load the environment variables.
2. Read `config.jsonc`.
3. Check all enabled APIs.
4. Measure response times.
5. Generate the monitoring report.
6. Send the report to Telegram.

## 8\. Configure GitHub Actions

GitHub Actions handles automatic execution without requiring a VPS.

### Step 1: Create a GitHub Repository

Create a repository named:

text

```text
api-monitor-telegram
```

Upload the project files.

Do not upload `.env` or `.venv`.

### Step 2: Configure GitHub Secrets

Open your repository:

text

```text
Settings
   |
   v
Secrets and variables
   |
   v
Actions
   |
   v
New repository secret
```

Create the following secrets:

| Secret Name | Value |
| --- | --- |
| `TELEGRAM_BOT_TOKEN` | Your bot token |
| `TELEGRAM_CHAT_ID` | Your numerical Chat ID |

### Step 3: Enable GitHub Actions

Open:

text

```text
Repository > Actions
```

Enable workflows if necessary.

### Step 4: Automatic Execution

The workflow is configured to execute every hour.

The default schedule is:

yaml

```yaml
on:
  schedule:
    - cron: "17 * * * *"

  workflow_dispatch:
```

The workflow runs at minute 17 of every hour, using UTC scheduling.

The report timestamp uses the timezone configured in `config.jsonc`.

> **Note:** GitHub Actions schedules are not guaranteed to execute at the exact scheduled minute.

### Step 5: Manual Execution

You can also trigger monitoring manually.

1. Open the repository.
2. Select **Actions**.
3. Open **API Monitor**.
4. Click **Run workflow**.
5. Confirm execution.

## 9\. Dependencies

The project uses the following Python packages:

| Package | Purpose |
| --- | --- |
| `requests` | HTTP requests |
| `json5` | JSONC configuration parsing |
| `python-dotenv` | Environment variable loading |
| `tzdata` | Timezone database for Windows |

Install all dependencies:

bash

```bash
pip install -r requirements.txt
```

## 10\. Notification Example

The Telegram bot sends a consolidated report.

text

```text
API MONITORING REPORT

11/11/2026 16:17:00

🟢 Customers API

Status: ONLINE
HTTP: 200
Response time: 120 ms

🔴 Finance API

Status: OFFLINE
HTTP: 503
Response time: 230 ms

🟢 Orders API

Status: ONLINE
HTTP: 200
Response time: 90 ms

━━━━━━━━━━━━━━━━━━

🟢 Online: 2
🔴 Offline: 1
📡 Total: 3

API Monitor Bot
```

## 11\. Security

Follow these security recommendations:

- Never commit `.env` to GitHub.
- Never expose your Telegram bot token.
- Use GitHub Secrets for automated execution.
- Avoid storing API credentials directly in `config.jsonc`.
- Use HTTPS for API endpoints.
- Do not log authentication headers or sensitive information.

## 12\. Troubleshooting

### Telegram Unauthorized (401)

Check whether your `TELEGRAM_BOT_TOKEN` is correct.

### Telegram Not Found (404)

Check the bot token and Telegram API URL.

### Empty getUpdates Response

Send `/start` to your bot and then send another message.

### API Connection Error

Check the endpoint URL, DNS resolution, network connectivity, and API availability.

### TimezoneNotFoundError

Install timezone data:

bash

```bash
pip install tzdata
```

### ModuleNotFoundError

Activate your virtual environment and reinstall dependencies:

bash

```bash
pip install -r requirements.txt
```

## 13\. Project Limitations

- GitHub Actions does not guarantee execution at an exact minute.
- Monitoring occurs once per scheduled execution.
- There is no persistent database or historical uptime dashboard.
- Each monitoring run sends one consolidated Telegram report.
- APIs requiring authentication need additional request configuration.
- Health-check endpoints should be used whenever available.

## 14\. Future Improvements

Potential improvements include:

- Alert only when an API changes status.
- Recovery notifications.
- Daily uptime reports.
- API availability history.
- Authentication headers.
- Configurable HTTP methods.
- Response content validation.
- Latency thresholds.
- Multiple Telegram recipients.

## License

This project is intended for personal and educational use.

Feel free to modify and extend it for your monitoring needs.