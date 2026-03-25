# 📈 BTC Discord Bot (Free & Serverless)

A simple Python script that checks the real-time price of Bitcoin using the Binance API and sends alerts to a Discord server via Webhooks. It runs completely for free using GitHub Actions!

## How to use this for yourself:
1. **Fork** this repository.
2. Create a Discord Webhook in your server settings.
3. Go to your forked repository's **Settings** -> **Secrets and variables** -> **Actions**.
4. Add a new secret named `DISCORD_WEBHOOK_URL` and paste your Discord webhook link.
5. Go to the **Actions** tab and enable workflows.

The bot will automatically run every hour and send you updates! 
To change the thresholds (like alerting when BTC is > $80k), just edit the `main.py` file.
