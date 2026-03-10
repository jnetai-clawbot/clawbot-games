#!/usr/bin/env python3
"""
WeatherNow - Beautiful Weather App
Displays current weather and forecast with stunning visuals
"""

import os
import json
import datetime

# For demo - in production would use requests library
def get_weather_data():
    """Get weather data (demo with sample data)"""
    return {
        "location": "London, UK",
        "temperature": 15,
        "condition": "Partly Cloudy",
        "humidity": 72,
        "wind_speed": 18,
        "feels_like": 13,
        "uv_index": 3,
        "visibility": 10,
        "pressure": 1015,
        "sunrise": "06:45",
        "sunset": "17:42",
        "hourly": [
            {"time": "09:00", "temp": 12, "condition": "Sunny", "icon": "☀️"},
            {"time": "12:00", "temp": 15, "condition": "Partly Cloudy", "icon": "⛅"},
            {"time": "15:00", "temp": 16, "condition": "Cloudy", "icon": "☁️"},
            {"time": "18:00", "temp": 14, "condition": "Clear", "icon": "🌤️"},
            {"time": "21:00", "temp": 11, "condition": "Clear", "icon": "⭐"}
        ],
        "daily": [
            {"day": "Mon", "high": 16, "low": 9, "condition": "⛅", "rain": 10},
            {"day": "Tue", "high": 14, "low": 7, "condition": "🌧️", "rain": 60},
            {"day": "Wed", "high": 12, "low": 5, "condition": "⛈️", "rain": 80},
            {"day": "Thu", "high": 13, "low": 6, "condition": "🌤️", "rain": 20},
            {"day": "Fri", "high": 15, "low": 8, "condition": "☀️", "rain": 5}
        ]
    }

def format_time():
    """Get current time formatted"""
    return datetime.datetime.now().strftime("%H:%M")

def main():
    print("=" * 50)
    print("🌤️ WeatherNow - Weather App")
    print("=" * 50)
    print()
    
    weather = get_weather_data()
    
    print(f"📍 Location: {weather['location']}")
    print(f"🌡️  Temperature: {weather['temperature']}°C")
    print(f"☁️  Condition: {weather['condition']}")
    print(f"💧 Humidity: {weather['humidity']}%")
    print(f"💨 Wind: {weather['wind_speed']} km/h")
    print(f"🌡️  Feels like: {weather['feels_like']}°C")
    print()
    print("Hourly Forecast:")
    for h in weather['hourly']:
        print(f"  {h['time']}: {h['icon']} {h['temp']}°C - {h['condition']}")
    print()
    print("5-Day Forecast:")
    for d in weather['daily']:
        print(f"  {d['day']}: {d['condition']} {d['high']}°/{d['low']}° 🌧️{d['rain']}%")
    print()

if __name__ == "__main__":
    main()
