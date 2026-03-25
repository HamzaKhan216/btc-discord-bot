import requests
import os

def get_btc_price():
    # Using CoinDesk's NEW Data API endpoint
    url = "https://data-api.coindesk.com/index/cc/v1/latest/tick?market=ccix&instruments=BTC-USD"
    response = requests.get(url)
    data = response.json()
    
    # Extract the decimal price from CoinDesk's new JSON structure
    return float(data["Data"]["BTC-USD"]["VALUE"])

def main():
    # Fetch the price
    price = get_btc_price()
    
    # Format the price nicely with commas (e.g., $65,432.10)
    formatted_price = f"${price:,.2f}"
    
    # --- YOUR CUSTOM CONDITIONS ---
    if price > 80000:
        message_content = f"🛑 **STOP AUTO-INVEST!** BTC is soaring at {formatted_price}. Pause your Binance Auto-Invest now."
    elif price < 60000:
        message_content = f"🤑 **TIME TO INVEST MORE!** BTC has dipped to {formatted_price}. Great buying opportunity!"
    else:
        message_content = f"📊 **Market Update:** BTC is currently sitting at {formatted_price}. No action needed."

    # Prepare the payload for Discord
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        print("Error: No Webhook URL found!")
        return

    payload = {
        "content": message_content
    }

    # Send the message to Discord
    response = requests.post(webhook_url, json=payload)
    
    if response.status_code == 204:
        print(f"Success! Sent message for price: {formatted_price}")
    else:
        print(f"Failed to send: {response.status_code}")

if __name__ == "__main__":
    main()