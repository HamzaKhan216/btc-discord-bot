import requests
import os

# ==========================================
# ⚙️ SETTINGS: Choose your AI provider here!
# Options: "gemini", "groq", "openai"
# ==========================================
ACTIVE_AI = "groq" 

def get_btc_price():
    # Using CoinDesk's Data API endpoint
    url = "https://data-api.coindesk.com/index/cc/v1/latest/tick?market=ccix&instruments=BTC-USD"
    response = requests.get(url)
    data = response.json()
    return float(data["Data"]["BTC-USD"]["VALUE"])

def get_historical_data():
    # Fetch the last 30 days of BTC prices using CoinGecko's free API
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=30&interval=daily"
    try:
        response = requests.get(url)
        data = response.json()
        prices = [round(item[1], 2) for item in data.get("prices",[])]
        return prices
    except Exception as e:
        print(f"Error fetching historical data: {e}")
        return[]

def get_ai_prediction(current_price, historical_prices, provider="groq"):
    price_history_str = ", ".join(map(str, historical_prices))
    
    prompt = (
        f"You are an expert cryptocurrency analyst. "
        f"The current price of Bitcoin is ${current_price:,.2f}. "
        f"Here are the daily closing prices for the last 30 days: {price_history_str}. "
        f"Based strictly on this previous data and the current price, predict the short-term future trend of Bitcoin. "
        f"Keep your answer to exactly 2-3 sentences. End by clearly stating if the short-term trend is BULLISH, BEARISH, or NEUTRAL."
    )

    try:
        if provider == "groq":
            from groq import Groq
            client = Groq(api_key=os.getenv("GROQ_API_KEY"))
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile", 
                messages=[
                    {"role": "system", "content": "You are a helpful crypto trading assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content.strip()

        elif provider == "gemini":
            from google import genai
            
            # Initialize the new Google GenAI client
            client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
            
            # Use the new models.generate_content syntax
            response = client.models.generate_content(
                model='gemini-3-flash-preview', 
                contents=f"System: You are a helpful crypto trading assistant.\n\nUser: {prompt}"
            )
            return response.text.strip()

        elif provider == "openai":
            from openai import OpenAI
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful crypto trading assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
            
        else:
            return "Invalid AI provider selected in settings."

    except Exception as e:
        return f"Could not generate {provider.upper()} prediction. Check your API key. Error: {e}"

def main():
    # 1. Fetch the current price
    print("Fetching current price...")
    price = get_btc_price()
    formatted_price = f"${price:,.2f}"
    
    # 2. Fetch historical data
    print("Fetching 30-day historical data...")
    historical_prices = get_historical_data()
    
    # 3. Get AI Prediction
    print(f"Analyzing trend using {ACTIVE_AI.upper()}...")
    if historical_prices:
        ai_prediction = get_ai_prediction(price, historical_prices, provider=ACTIVE_AI)
    else:
        ai_prediction = "Could not fetch historical data to make a prediction."
    
    # --- YOUR CUSTOM CONDITIONS ---
    if price > 80000:
        message_content = f"🛑 **STOP AUTO-INVEST!** BTC is soaring at {formatted_price}. Pause your Binance Auto-Invest now."
    elif price < 60000:
        message_content = f"🤑 **TIME TO INVEST MORE!** BTC has dipped to {formatted_price}. Great buying opportunity!"
    else:
        message_content = f"📊 **Market Update:** BTC is currently sitting at {formatted_price}. No action needed."

    # 4. Combine your message with the AI prediction
    final_message = f"{message_content}\n\n🤖 **{ACTIVE_AI.upper()} Trend Analysis (Last 30 Days):**\n> {ai_prediction}"

    # 5. Prepare the payload for Discord
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        print("Error: No Webhook URL found!")
        return

    payload = {
        "content": final_message
    }

    # 6. Send the message to Discord
    response = requests.post(webhook_url, json=payload)
    
    if response.status_code == 204:
        print(f"Success! Sent message to Discord.")
    else:
        print(f"Failed to send: {response.status_code} - {response.text}")

if __name__ == "__main__":
    main()