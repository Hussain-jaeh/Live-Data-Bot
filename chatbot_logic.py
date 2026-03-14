import re
import os
import requests
from dotenv import load_dotenv

load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
CURRENCY_API_KEY = os.getenv("CURRENCY_API_KEY")

# Mapping common currency names to ISO codes
CURRENCY_MAP = {
    "naira": "NGN",
    "dollar": "USD",
    "dollars": "USD",
    "euro": "EUR",
    "euros": "EUR",
    "pound": "GBP",
    "pounds": "GBP",
    "yen": "JPY",
    "won": "KRW",
    "yuan": "CNY",
    "rupee": "INR",
    "shilling": "KES",
    "rand": "ZAR",
    "dirham": "AED",
    "real": "BRL",
}

def get_weather(city):
    if not WEATHER_API_KEY:
        return "Weather API Key is missing. Please set it in .env"
    
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            temp = data['main']['temp']
            desc = data['weather'][0]['description']
            icon = data['weather'][0]['icon']
            humidity = data['main']['humidity']
            wind = data['wind']['speed']
            
            return {
                "temp": temp,
                "desc": desc,
                "icon": f"http://openweathermap.org/img/wn/{icon}@2x.png",
                "humidity": humidity,
                "wind": wind,
                "city": data['name']
            }
        else:
            return f"I couldn't find the weather for '{city}'. Please check the city name."
    except Exception as e:
        return f"Error connecting to weather service: {str(e)}"

def get_exchange_rate(from_curr, to_curr):
    if not CURRENCY_API_KEY:
        return "Currency API Key is missing. Please set it in .env"
    
    from_code = CURRENCY_MAP.get(from_curr.lower(), from_curr.upper())
    to_code = CURRENCY_MAP.get(to_curr.lower(), to_curr.upper())

    url = f"https://v6.exchangerate-api.com/v6/{CURRENCY_API_KEY}/latest/{from_code}"
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            rate = data['conversion_rates'].get(to_code)
            if rate:
                return rate, from_code, to_code
            else:
                return f"Currency code '{to_code}' not found.", None, None
        else:
            return f"Error: {data.get('error-type', 'Failed to fetch currency data.')}", None, None
    except Exception as e:
        return f"Error connecting to currency service: {str(e)}", None, None

def process_prompt(prompt):
    """
    Processes the raw prompt and returns the intent, parameters, and response content.
    This mimics the logic inside app.py.
    """
    prompt_lower = prompt.lower()
    weather_keywords = ["weather", "wheather", "temperature", "condition", "temp"]
    
    # 1. Weather Intent
    if any(k in prompt_lower for k in weather_keywords):
        # Use word boundaries to avoid matching "at" in "what"
        city_match = re.search(r"\b(?:in|at|for)\b\s+([a-zA-Z\s]+)", prompt_lower)
        if city_match:
            city = city_match.group(1).strip("? .!")
        else:
            words = prompt_lower.split()
            city = words[-1].strip("? .!")
            if city in weather_keywords:
                 city = "London" 
        
        return "weather", {"city": city.lower()}, f"Checking weather for {city}..."

    # 2. Currency Intent
    # Look for patterns like "100 USD to EUR" or "convert 100 USD in EUR" or "100 USD in EUR"
    currency_pattern = r"(\d+\.?\d*)\s*([a-zA-Z]+)\s+(?:to|in)\s+([a-zA-Z]+)"
    parts = re.findall(currency_pattern, prompt_lower)
    
    if parts:
        amount, from_val, to_val = parts[0]
        return "currency", {"amount": amount, "from": from_val.lower(), "to": to_val.lower()}, f"Converting {amount} {from_val}..."
    
    elif any(char.isdigit() for char in prompt_lower) and ("to" in prompt_lower or "convert" in prompt_lower):
        return "currency_partial", {}, "I couldn't quite understand that conversion request."

    # 3. Greeting Intent
    elif any(word in prompt_lower for word in ["hi", "hello", "hey", "intro", "help"]):
        return "greeting", {}, "Hello! I'm ready to help you..."

    # 4. Fallback Intent
    else:
        return "fallback", {}, "I'm specialized in weather and currency..."
