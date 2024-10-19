import sqlite3
from datetime import datetime

# Function to retrieve weather data from the SQLite database
def retrieve_weather_data(city=None, date=None):
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()

    # Build the query based on user input for filtering by city or date
    query = "SELECT * FROM daily_weather_summary"
    params = []
    if city or date:
        query += " WHERE"
    if city:
        query += " city = ?"
        params.append(city)
    if city and date:
        query += " AND"
    if date:
        query += " date = ?"
        params.append(date)

    cursor.execute(query, params)
    rows = cursor.fetchall()

    # Display the retrieved data
    if rows:
        for row in rows:
            print(f"Date: {row[0]}, City: {row[1]}, Avg Temp: {row[2]:.2f}°C, Max Temp: {row[3]:.2f}°C, "
                  f"Min Temp: {row[4]:.2f}°C, Dominant Condition: {row[5]}")
    else:
        print("No data found for the given criteria.")

    conn.close()

# Example usage of the retrieval function
if __name__ == "__main__":
    print("Retrieve stored weather data:")
    city_input = input("Enter city (or leave blank to retrieve data for all cities): ")
    date_input = input("Enter date (YYYY-MM-DD) (or leave blank to retrieve data for all dates): ")

    retrieve_weather_data(city=city_input if city_input else None, date=date_input if date_input else None)
