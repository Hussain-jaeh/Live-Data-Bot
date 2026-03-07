# 🤖 LiveData Intelligent Bot

A premium, interactive chatbot built with **Streamlit** that provides real-time information for **Weather** and **Currency Conversion** using live APIs.

---

## ✨ Features

- **🚀 Live Data Integration**: Fetches real-time weather from [OpenWeatherMap](https://openweathermap.org/) and current exchange rates from [ExchangeRate-API](https://www.exchangerate-api.com/).
- **💎 Premium UI/UX**: Custom CSS-styled interface with a glassmorphism aesthetic, dark-mode gradients, and smooth typography (Outfit Font).
- **🧠 Natural Language Parsing**: Smart intent detection for weather (handles typos like "wheather") and currency (handles full labels like "naira" or "dollar").
- **🔄 Session State History**: Remembers your conversation during the current session.
- **📱 Responsive Layout**: Works across desktop and mobile browsers.

---

## 🛠️ Technology Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **Data Fetching**: `requests` (API interaction)
- **Environment Management**: `python-dotenv`
- **Charting/Visuals**: `plotly` & `pandas` (for potential future expansions)

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd LiveData-bot
```

### 2. Create and activate a Virtual Environment
```bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure API Keys
Create a `.env` file in the root directory and add your API keys:
```env
WEATHER_API_KEY=your_openweathermap_key_here
CURRENCY_API_KEY=your_exchangerate_api_key_here
```

---

## 🚀 Usage

Start the application using the Streamlit CLI:
```bash
streamlit run app.py
```

### Example Queries
- **Weather**: `"What's the weather in London?"` or `"Weather in Tokyo"`
- **Currency**: `"Convert 100 Naira to Dollar"` or `"What is 50 USD in EUR?"`
- **General**: `"Hi"` or `"Help"`

---

## 📝 License
This project is open-source and available under the MIT License.
