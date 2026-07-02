# Ledger Bot – Telegram Expense Tracker

A Telegram bot for tracking expenses with natural language input, category management, and optional Google Sheets sync.

## Features

- **Natural Language Input**: Type `bb 150` or `150 rapido` to log expenses
- **Auto-Categorization**: Intelligent category detection based on keywords
- **Quick Reports**: View daily, weekly, or monthly expense summaries
- **Category Breakdown**: See spending by category
- **Web Dashboard**: Visual analytics and transaction history
- **Google Sheets Sync**: Optional automatic sync to a Google Sheet
- **Transaction Management**: Edit categories, delete transactions, export as CSV

## Deployment on Render

### 1. Prerequisites

- A Telegram Bot Token (from [@BotFather](https://t.me/botfather))
- A hosted Web Dashboard URL (e.g., Netlify, Vercel)
- (Optional) Google Service Account JSON for Sheets integration

### 2. Push to GitHub

```bash
git add .
git commit -m "Initial commit"
git push origin main
```

### 3. Create Render Service

1. Go to [render.com](https://render.com)
2. Click **New +** → **Web Service**
3. Connect your GitHub repository
4. Fill in the settings:
   - **Name**: `expense-bot`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python expense_bot.py`
   - **Plan**: Free (or paid for production)

### 4. Set Environment Variables

In the Render dashboard, add these environment variables:

```
TELEGRAM_BOT_TOKEN=your_token_here
WEBAPP_URL=https://your-webapp-url.netlify.app
GOOGLE_SERVICE_ACCOUNT_JSON={"type":"service_account",...}  # Optional
PORT=10000  # Render auto-assigns (leave blank to auto-set)
```

### 5. Deploy

Click **Deploy** and monitor logs. Once running, your bot will be live!

## Local Development

### Setup

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Configuration

Copy `.env.example` to `.env` and fill in your details:

```bash
cp .env.example .env
```

### Run

```bash
python expense_bot.py
```

The bot will:
- Listen for Telegram messages
- Serve the Flask API on port 5000 (or `PORT` env var)
- Sync Google Sheets in the background

## Usage

### Commands

- `/start` – Welcome message with inline buttons
- `/help` – Show all available commands
- **Plain text** (e.g., `bb 150`) – Add expense
- `/add 150 bb` – Alternative add syntax
- `/delete <id>` – Remove a transaction
- `/setcat <id> <category>` – Change category for a transaction
- `/listcats` – Show all available categories
- `/setsheet <url>` – Link a Google Sheet for sync
- `/export` – Export all transactions as CSV

### Examples

```
bb 150
150 rapido
rent 17000
ice cream 200 snacks
```

## Database

- **SQLite** (`ledger.db` on Render persistent disk)
- **Tables**: `expenses`, `user_settings`

## Google Sheets Integration

To link a Google Sheet:

1. Create a Google Cloud Service Account with Sheets/Drive permissions
2. Download the JSON key
3. Set `GOOGLE_SERVICE_ACCOUNT_JSON` environment variable with the JSON content (as a string)
4. In Telegram: `/setsheet <google_sheets_url>`

The bot will automatically sync both directions.

## Architecture

- **Telegram Handler**: Receives messages, processes commands
- **Flask API**: Serves transaction data to the web dashboard
- **Background Sync**: Periodically syncs with Google Sheets (every 60s)
- **SQLite DB**: Local persistent storage

## Troubleshooting

### Bot not responding on Render

1. Check **Logs** in Render dashboard
2. Verify `TELEGRAM_BOT_TOKEN` is set correctly
3. Ensure logs show `"Telegram bot started..."`

### Flask API not accessible

1. Check that `PORT` is set (Render auto-assigns 10000+)
2. Verify health check: `curl https://your-app.onrender.com/health`

### Google Sheets sync failing

1. Verify Service Account JSON is valid
2. Check that the Sheet URL is shareable with the service account email
3. Review logs for detailed error messages

## Future Enhancements

- Recurring expenses
- Budget alerts
- Receipt image uploads
- Multi-user group support
- Analytics dashboard improvements

---

**Developed with ❤️ for expense tracking on Telegram**
