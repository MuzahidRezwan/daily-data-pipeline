"""
Daily Automated Data Pipeline
Author: Muzahid Rezwan
Description: Fetches daily weather & climate metrics from Open-Meteo public API,
records data to CSV, and auto-updates README statistics.
"""

import json
import urllib.request
from datetime import datetime
import os

API_URL = "https://api.open-meteo.com/v1/forecast?latitude=23.8103&longitude=90.4125&current=temperature_2m,relative_humidity_2m,apparent_temperature,wind_speed_10m&timezone=Asia%2FDhaka"

def fetch_weather_data():
    req = urllib.request.Request(API_URL, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=10) as response:
        return json.loads(response.read().decode('utf-8'))

def update_csv(timestamp, temp, apparent_temp, humidity, wind):
    os.makedirs("data", exist_ok=True)
    csv_file = os.path.join("data", "weather_history.csv")
    file_exists = os.path.isfile(csv_file)
    
    with open(csv_file, "a", encoding="utf-8") as f:
        if not file_exists:
            f.write("Timestamp,Temperature_C,Apparent_Temp_C,Humidity_Percent,Wind_Speed_Kmh\n")
        f.write(f"{timestamp},{temp},{apparent_temp},{humidity},{wind}\n")

def get_total_records():
    csv_file = os.path.join("data", "weather_history.csv")
    if not os.path.exists(csv_file):
        return 0
    with open(csv_file, "r", encoding="utf-8") as f:
        return max(0, len(f.readlines()) - 1)

def update_readme(timestamp, temp, apparent_temp, humidity, wind, total_records):
    readme_content = f"""# 🌦️ Automated Daily Climate & Data Pipeline

![Automated Pipeline](https://img.shields.io/badge/Pipeline-Automated%20via%20GitHub%20Actions-brightgreen?style=for-the-badge&logo=github-actions)
![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Maintained By](https://img.shields.io/badge/Maintained%20By-Muzahid%20Rezwan-orange?style=for-the-badge)

An autonomous Data Engineering & Collection pipeline that runs every single day using **GitHub Actions**. It fetches live climate data, logs it into a time-series CSV dataset, and updates this repository automatically.

---

### 📍 Latest Recorded Weather (Dhaka, Bangladesh)
* **Last Updated:** `{timestamp} (Asia/Dhaka)`
* **Temperature:** `{temp} °C`
* **Feels Like:** `{apparent_temp} °C`
* **Relative Humidity:** `{humidity}%`
* **Wind Speed:** `{wind} km/h`
* **Total Days Tracked:** `{total_records} days`

---

### 📊 Time-Series Dataset
All recorded data is stored in [`data/weather_history.csv`](data/weather_history.csv) for historical analysis, machine learning forecasting, and exploratory modeling.

---
*Created & Automated by [Muzahid Rezwan](https://github.com/MuzahidRezwan)* 🚀
"""
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)

def main():
    print("Fetching live data...")
    try:
        data = fetch_weather_data()
        current = data.get("current", {})
        
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        temp = current.get("temperature_2m", "N/A")
        apparent_temp = current.get("apparent_temperature", "N/A")
        humidity = current.get("relative_humidity_2m", "N/A")
        wind = current.get("wind_speed_10m", "N/A")
        
        update_csv(now, temp, apparent_temp, humidity, wind)
        total = get_total_records()
        update_readme(now, temp, apparent_temp, humidity, wind, total)
        print("Pipeline executed successfully!")
    except Exception as e:
        print(f"Error executing pipeline: {e}")

if __name__ == "__main__":
    main()
