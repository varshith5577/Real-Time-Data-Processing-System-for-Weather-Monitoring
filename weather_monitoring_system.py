import requests
import time
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt

# OpenWeatherMap API Key
API_KEY = "93b063b3a55d1d98c4ca6f4372797c7f"
CITY_LIST = ["Delhi", "Mumbai", "Chennai", "Bangalore", "Kolkata", "Hyderabad"]

# Initialize user-configurable thresholds
ALERT_THRESHOLD = float(input("Enter temperature alert threshold (°C): "))  # User-defined threshold
CONSECUTIVE_BREACHES_REQUIRED = 2  # Number of consecutive breaches required for an alert

# Function to create the SQLite database and the table for storing daily summaries
def create_db():
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS daily_weather_summary (
                        date TEXT,
                        city TEXT,
                        avg_temp REAL,
                        max_temp REAL,
                        min_temp REAL,
                        dominant_condition TEXT)''')
    conn.commit()
    conn.close()

# Function to store daily summary in the SQLite database
def store_daily_summary(city, avg_temp, max_temp, min_temp, dominant_condition):
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO daily_weather_summary (date, city, avg_temp, max_temp, min_temp, dominant_condition)
                      VALUES (?, ?, ?, ?, ?, ?)''',
                   (datetime.now().strftime("%Y-%m-%d"), city, avg_temp, max_temp, min_temp, dominant_condition))
    conn.commit()
    conn.close()

# Fetch weather data for a given city from OpenWeatherMap API
def get_weather_data(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200 and "main" in data:
        return {
            "temp": kelvin_to_celsius(data['main']['temp']),
            "feels_like": kelvin_to_celsius(data['main']['feels_like']),
            "condition": data['weather'][0]['main'],
            "timestamp": data['dt']
        }
    else:
        print(f"Failed to fetch weather data for {city}: {data.get('message', 'Unknown error')}")
        return None

# Convert temperature from Kelvin to Celsius
def kelvin_to_celsius(temp_k):
    return temp_k - 273.15

# Calculate daily summary based on collected weather data
def calculate_daily_summary(city_data):
    avg_temp = sum([data['temp'] for data in city_data]) / len(city_data)
    max_temp = max([data['temp'] for data in city_data])
    min_temp = min([data['temp'] for data in city_data])

    # Find the most frequent weather condition as the dominant condition
    conditions = [data['condition'] for data in city_data]
    dominant_condition = max(set(conditions), key=conditions.count)

    return avg_temp, max_temp, min_temp, dominant_condition

# Function to check if any alerts should be triggered based on temperature thresholds
def check_alerts(city, current_temp, breach_count):
    if current_temp >= ALERT_THRESHOLD:
        breach_count += 1
        if breach_count >= CONSECUTIVE_BREACHES_REQUIRED:
            print(f"ALERT: The temperature in {city} has exceeded {ALERT_THRESHOLD}°C (Current Temp: {current_temp}°C)")
            return 0  # Reset breach count after alert
    else:
        breach_count = 0  # Reset count if the temperature is below the threshold
    return breach_count

# Display simple temperature trends visualization
def plot_temperature_trends(city, city_data):
    timestamps = [datetime.utcfromtimestamp(entry['timestamp']).strftime('%H:%M') for entry in city_data]
    temps = [entry['temp'] for entry in city_data]

    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, temps, marker='o', label='Temperature (°C)')
    plt.title(f"Temperature Trend for {city}")
    plt.xlabel('Time')
    plt.ylabel('Temperature (°C)')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Main function to continuously retrieve weather data and process it
def main():
    create_db()

    daily_data = {}
    breach_counts = {city: 0 for city in CITY_LIST}  # Initialize breach counts for each city

    while True:
        for city in CITY_LIST:
            if city not in daily_data:
                daily_data[city] = []

            # Fetch current weather data for the city
            weather_data = get_weather_data(city)
            if weather_data:
                daily_data[city].append(weather_data)

                # Check for alerts based on the temperature
                breach_counts[city] = check_alerts(city, weather_data['temp'], breach_counts[city])

        # After collecting data for each city, calculate the daily summary and store it
        for city, city_data in daily_data.items():
            if city_data:
                avg_temp, max_temp, min_temp, dominant_condition = calculate_daily_summary(city_data)
                store_daily_summary(city, avg_temp, max_temp, min_temp, dominant_condition)
                print(f"{city} - Avg Temp: {avg_temp:.2f}°C, Max Temp: {max_temp:.2f}°C, Min Temp: {min_temp:.2f}°C, Dominant Condition: {dominant_condition}")

                # Visualize the temperature trend for this city
                plot_temperature_trends(city, city_data)

        # Wait for 5 minutes before the next retrieval
        time.sleep(300)

if __name__ == "__main__":
    main()
