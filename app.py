import os
from dotenv import load_dotenv
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from collections import Counter

# Load environment variables
load_dotenv()

# Configure the page
st.set_page_config(page_title="Weather Dashboard", layout="wide", initial_sidebar_state="collapsed")

# API Configuration
API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5"

# Add CSS styling
st.markdown("""
    <style>
        .metric-container {
            background-color: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            text-align: center;
            margin: 10px 0;
        }
        
        .metric-icon {
            font-size: 24px;
            margin-bottom: 10px;
            color: #0366d6;
        }
        
        .metric-value {
            font-size: 24px;
            font-weight: bold;
            margin: 10px 0;
            color: #1a1a1a;
        }
        
        .metric-label {
            font-size: 14px;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .chart-container {
            background-color: white;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .stMetric {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        div[data-testid="stMetricLabel"] {
            font-size: 14px;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        div[data-testid="stMetricValue"] {
            font-size: 24px;
            font-weight: bold;
            color: #1a1a1a;
        }
        
        /* Center align all content */
        .streamlit-expanderHeader, h1, h2, h3, p, div {
            text-align: center !important;
        }
        
        /* Custom icons */
        .weather-icon {
            font-size: 20px;
            margin-right: 5px;
        }
        .title-container {
            display: flex;
            justify-content: center;
            align-items: center;
            margin-bottom: 20px;
        }
        .title-text {
            margin-left: 10px;
        }
        
        /* Center input field */
        .stTextInput {
            max-width: 500px;
            margin: 0 auto;
        }
    </style>
""", unsafe_allow_html=True)

def kelvin_to_celsius(kelvin):
    return round(kelvin - 273.15, 1)

def fetch_current_weather(city):
    url = f"{BASE_URL}/weather?q={city}&appid={API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return {
            'temperature': kelvin_to_celsius(data['main']['temp']),
            'feels_like': kelvin_to_celsius(data['main']['feels_like']),
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'wind_speed': data['wind']['speed'],
            'description': data['weather'][0]['description'].capitalize(),
            'icon': data['weather'][0]['icon']
        }
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching current weather: {str(e)}")
        return None

def fetch_forecast(city):
    url = f"{BASE_URL}/forecast?q={city}&appid={API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        forecasts = []
        
        for item in data['list']:
            dt = datetime.fromtimestamp(item['dt'])
            forecasts.append({
                'datetime': dt,
                'temperature': kelvin_to_celsius(item['main']['temp']),
                'pressure': item['main']['pressure'],
                'description': item['weather'][0]['description'],
                'feels_like': kelvin_to_celsius(item['main']['feels_like']),
            })
        return forecasts
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching forecast: {str(e)}")
        return None

# Main app
st.markdown("""
    <div class="title-container">
        <span class="weather-icon">🌤️</span>
        <h1 class="title-text">Weather Dashboard</h1>
    </div>
""", unsafe_allow_html=True)

# Center the input field using columns
col1, col2, col3 = st.columns([1,2,1])
with col2:
    city = st.text_input("Enter City Name", "Chennai")

if city:
    current_weather = fetch_current_weather(city)
    
    if current_weather:
        st.subheader(f"📍Current Weather in {city}")
        
        # KPI Metrics with icons
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
                <div class="metric-container">
                    <div class="metric-icon">🌡️</div>
                    <div class="metric-value">{temp}°C</div>
                    <div class="metric-label">Temperature</div>
                </div>
            """.format(temp=current_weather['temperature']), unsafe_allow_html=True)
            
        with col2:
            st.markdown("""
                <div class="metric-container">
                    <div class="metric-icon">💧</div>
                    <div class="metric-value">{humidity}%</div>
                    <div class="metric-label">Humidity</div>
                </div>
            """.format(humidity=current_weather['humidity']), unsafe_allow_html=True)
            
        with col3:
            st.markdown("""
                <div class="metric-container">
                    <div class="metric-icon">🌪️</div>
                    <div class="metric-value">{speed} m/s</div>
                    <div class="metric-label">Wind Speed</div>
                </div>
            """.format(speed=current_weather['wind_speed']), unsafe_allow_html=True)
            
        with col4:
            st.markdown("""
                <div class="metric-container">
                    <div class="metric-icon">📊</div>
                    <div class="metric-value">{pressure} hPa</div>
                    <div class="metric-label">Pressure</div>
                </div>
            """.format(pressure=current_weather['pressure']), unsafe_allow_html=True)

        # Fetch and display forecast
        forecast_data = fetch_forecast(city)
        if forecast_data:
            df = pd.DataFrame(forecast_data)
            st.markdown("""---""")
            
            # Temperature Forecast Line Chart
            st.subheader("📈 Temperature Forecast")
            
            fig_temp = go.Figure()
            fig_temp.add_trace(go.Scatter(
                x=df['datetime'],
                y=df['temperature'],
                name='Temperature',
                line=dict(color='#FF9F1C', width=3),
                mode='lines+markers'
            ))
            
            fig_temp.add_trace(go.Scatter(
                x=df['datetime'],
                y=df['feels_like'],
                name='Feels Like',
                line=dict(color='#2EC4B6', width=2, dash='dot'),
                mode='lines'
            ))
            
            fig_temp.update_layout(
                xaxis_title="Date & Time",
                yaxis_title="Temperature (°C)",
                hovermode='x unified',
                legend=dict(y=1.1, orientation='h'),
                margin=dict(l=20, r=20, t=40, b=20),
                height=400
            )
            
            st.plotly_chart(fig_temp, use_container_width=True, config={'displayModeBar': False})
            st.markdown("""---""")
            
            # Weather Types Distribution Bar Chart
            st.subheader("📊 Weather Conditions")
            
            weather_counts = Counter(df['description'])
        weather_df = pd.DataFrame({
            'Condition': list(weather_counts.keys()),
            'Count': list(weather_counts.values())
        })

        # Define color mapping based on weather conditions
        def get_condition_color(condition):
            condition = condition.lower()
            if 'clear' in condition:
                return '#FFD700'  # Golden yellow for clear sky
            elif 'cloud' in condition:
                return '#A2B5CD'  # Light slate gray for clouds
            elif 'rain' in condition or 'drizzle' in condition:
                return '#4682B4'  # Steel blue for rain
            elif 'snow' in condition:
                return '#E0FFFF'  # Light cyan for snow
            elif 'thunder' in condition or 'storm' in condition:
                return '#9370DB'  # Medium purple for storms
            elif 'mist' in condition or 'fog' in condition:
                return '#B8B8B8'  # Gray for mist/fog
            elif 'haze' in condition:
                return '#DEB887'  # Burlywood for haze
            else:
                return '#20B2AA'  # Light sea green for other conditions

        # Apply colors based on conditions
        colors = [get_condition_color(condition) for condition in weather_df['Condition']]

        fig_bar = go.Figure(data=[
            go.Bar(
                x=weather_df['Condition'],
                y=weather_df['Count'],
                marker_color=colors,
                text=weather_df['Count'],
                textposition='auto',
            )
        ])

        fig_bar.update_layout(
            xaxis_title="Weather Condition",
            yaxis_title="Frequency",
            showlegend=False,
            height=400,
            margin=dict(l=20, r=20, t=40, b=20),
            # Make the chart background transparent to work well in both modes
            plot_bgcolor='rgba(0,0,0,0)',
            # Add grid lines for better readability
            yaxis=dict(
                gridcolor='rgba(128,128,128,0.2)',
                zerolinecolor='rgba(128,128,128,0.2)'
            ),
            xaxis=dict(
                gridcolor='rgba(128,128,128,0.2)',
                zerolinecolor='rgba(128,128,128,0.2)'
            )
        )

        st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})

    else:
        st.error("City not found or API error occurred. Please try again.")

st.markdown("---")
st.caption("Developed by Rakhesh Krishna. Data provided by OpenWeather API")
