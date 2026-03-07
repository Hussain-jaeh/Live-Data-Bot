import streamlit as st
import requests
import os
from dotenv import load_dotenv
import pandas as pd
import plotly.express as px
from datetime import datetime

load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
CURRENCY_API_KEY = os.getenv("CURRENCY_API_KEY")

st.set_page_config(
    page_title="LiveData Bot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Outfit', sans-serif;
    }

    /* Gradient Background for everything */
    .stApp {
        background: radial-gradient(circle at top left, #0f172a 0%, #1e293b 100%);
        color: #f8fafc;
    }

    /* Custom Chat Bubble Styles */
    .chat-bubble {
        padding: 1rem;
        border-radius: 12px;
        margin-bottom: 10px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        max-width: 80%;
    }

    .user-bubble {
        background: rgba(59, 130, 246, 0.2);
        margin-left: auto;
        border-right: 4px solid #3b82f6;
    }

    .bot-bubble {
        background: rgba(255, 255, 255, 0.05);
        margin-right: auto;
        border-left: 4px solid #6366f1;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.95);
        border-right: 1px solid rgba(255,255,255,0.05);
    }

    h1, h2, h3 {
        color: #f8fafc !important;
        font-weight: 600;
        letter-spacing: -0.02em;
    }

    .stTextInput input {
        background-color: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        color: white !important;
        border-radius: 8px;
    }

    .stButton button {
        background: linear-gradient(135deg, #6366f1 0%, #3b82f6 100%);
        border: none;
        color: white;
        font-weight: 600;
        padding: 0.5rem 2rem;
        border-radius: 8px;
        transition: all 0.3s ease;
    }

    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);
    }

    /* Hide standard streamlit elements for cleaner look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- Helper Functions ---

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
    
    # Check map first
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

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am **LiveData Bot**. I can provide real-time weather and currency conversion. How can I help you today?"}
    ]

with st.sidebar:
    st.image("https://img.icons8.com/isometric-line/100/ffffff/bot.png", width=100)
    st.title("🤖 LiveData Bot")
    st.markdown("---")
    
    st.subheader("📖 Quick Instructions")
    st.info("""
    **Weather**
    Try: `Weather in London` or `What's the weather in Tokyo?`
    
    **Currency**
    Try: `Convert 100 USD to EUR` or `What is 50 GBP in USD?`
    
    **Other**
    I can also handle simple greetings and small talk!
    """)
    
    st.markdown("---")
    st.markdown("**Powered by**")
    st.markdown("OpenWeatherMap & ExchangeRate-API")
    
    if st.button("Clear History"):
        st.session_state.messages = [{"role": "assistant", "content": "History cleared. How can I help?"}]
        st.rerun()

st.markdown("<h1 style='text-align: center; margin-bottom: 2rem;'>🚀 LiveData Intelligent Bot</h1>", unsafe_allow_html=True)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"], unsafe_allow_html=True)

if prompt := st.chat_input("Ask about weather or currency..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    response_content = ""
    prompt_lower = prompt.lower()

    weather_keywords = ["weather", "wheather", "temperature", "condition", "temp"]
    if any(k in prompt_lower for k in weather_keywords):
        import re
        city_match = re.search(r"(?:in|at|for)\s+([a-zA-Z\s]+)", prompt_lower)
        if city_match:
            city = city_match.group(1).strip()
        else:
            words = prompt_lower.split()
            city = words[-1].strip("? .!")
            if city in weather_keywords:
                 city = "London" 

        with st.spinner(f"Checking weather for {city}..."):
            data = get_weather(city)
            if isinstance(data, dict):
                response_content = f"""
                ### Weather in {data['city']} 🌡️
                - **Temperature**: {data['temp']}°C
                - **Conditions**: {data['desc'].capitalize()}
                - **Humidity**: {data['humidity']}%
                - **Wind Speed**: {data['wind']} m/s
                
                ![Icon]({data['icon']})
                """
            else:
                response_content = data
    
    elif any(char.isdigit() for char in prompt_lower) and ("to" in prompt_lower or "convert" in prompt_lower):
        import re
        parts = re.findall(r"(\d+\.?\d*)\s*([a-zA-Z]+)\s+(?:to|in)\s+([a-zA-Z]+)", prompt_lower)
        
        if parts:
            amount, from_val, to_val = parts[0]
            with st.spinner(f"Converting {amount} {from_val}..."):
                rate, f_code, t_code = get_exchange_rate(from_val, to_val)
                if isinstance(rate, (float, int)):
                    converted = float(amount) * rate
                    response_content = f"### Conversion Results 💸\n**{amount} {f_code}** = **{converted:,.2f} {t_code}**\n\n*Rate: 1 {f_code} = {rate:,.4f} {t_code}*"
                else:
                    response_content = rate
        else:
            response_content = "I couldn't quite understand that conversion request. Try: `Convert 100 Naira to Dollar` or `100 USD to EUR`."

    elif any(word in prompt_lower for word in ["hi", "hello", "hey", "intro", "help"]):
        response_content = "Hello! I'm ready to help you with weather updates or currency conversions. Just ask me something like 'Weather in New York' or 'Convert 50 USD to EUR'."
    else:
        response_content = "I'm specialized in weather and currency. Try asking me for weather in a city (e.g., 'Weather in Tokyo') or a currency conversion (e.g., '100 Naira to Dollar')!"
    st.session_state.messages.append({"role": "assistant", "content": response_content})
    with st.chat_message("assistant"):
        st.markdown(response_content, unsafe_allow_html=True)

