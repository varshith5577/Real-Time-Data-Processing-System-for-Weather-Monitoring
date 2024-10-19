# Real-Time Weather Monitoring System

## Overview

This system retrieves real-time weather data from the OpenWeatherMap API for major cities in India and calculates daily weather summaries using rollups and aggregates. It continuously monitors temperature and weather conditions, and can trigger alerts when user-configurable thresholds are exceeded. The data is stored in an SQLite database for further analysis.

### Cities Monitored:
- Delhi
- Mumbai
- Chennai
- Bangalore
- Kolkata
- Hyderabad

### Features:
- **Real-Time Data**: Fetches weather data at configurable intervals (default: every 5 minutes).
- **Temperature Conversion**: Converts temperatures from Kelvin to Celsius.
- **Daily Aggregates**: Calculates daily averages, maximum, minimum temperatures, and identifies the dominant weather condition.
- **Alert System**: Triggers an alert if a temperature exceeds a specified threshold (default: 35°C).
- **Database Storage**: Stores daily summaries in an SQLite database for later analysis.

---

## Setup Instructions

### Prerequisites
- Python 3.11.7
- Internet connection to access the OpenWeatherMap API
- An OpenWeatherMap API key (sign up for free at [OpenWeatherMap](https://home.openweathermap.org/users/sign_up))

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/varshith5577/Real-Time-Data-Processing-System-for-Weather-Monitoring.git
   cd Real-Time-Data-Processing-System-for-Weather-Monitoring
