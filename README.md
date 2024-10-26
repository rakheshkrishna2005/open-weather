# 🌤️ Weather Dashboard

An interactive Weather Dashboard built with Streamlit that lets users fetch and visualize current weather data and forecasts for any city in the world.

## 🌟 Features
- **Current Weather Info**: Displays temperature, humidity, wind speed, pressure, and conditions.
- **Temperature Forecast**: Visualizes temperature trends and "feels like" metrics.
- **Weather Conditions Pie Chart**: Shows distribution of weather conditions.
- **Temperature Range Chart**: Illustrates max and min temperatures over time.
- **User-Friendly Interface**: Easy city input with clear visualizations.

## 🌐 Web App
![app](https://github.com/rakheshkrishna2005/open-weather/blob/main/app.jpg)

## 🛠 Tech Stack
- **Python**: Backend logic
- **Streamlit**: Web app framework
- **Requests**: HTTP requests to OpenWeather API
- **Pandas**: Data manipulation
- **Plotly**: Interactive plots
- **dotenv**: Environment variable management

## 🚀 Installation and Usage
1. **Clone the repository**:
   ```bash
   git clone https://github.com/rakheshkrishna2005/weather-dashboard.git
   ```

1. **Navigate to the project directory**:
   ```bash
   cd weather-dashboard
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file with your OpenWeather API key:
   ```
   OPENWEATHER_API_KEY=your_api_key_here
   ```

4. **Run the app**:
   ```bash
   streamlit run app.py
   ```

## 📚 Additional Resources
- **[Plotly Documentation](https://plotly.com/python/)**
- **[Pandas Documentation](https://pandas.pydata.org/docs/)**
- **[Requests Documentation](https://docs.python-requests.org/en/master/)**
- **[Streamlit Documentation](https://docs.streamlit.io/)**
- **[OpenWeather API Documentation](https://openweathermap.org/api)**
