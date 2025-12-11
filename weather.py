import requests, os

# API key thời tiết 
API_KEY = os.environ.get('OPENWEATHER_API_KEY', "a3091c751181373eb2659248e0ad1db5")

def get_weather(lat, lon):
    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "metric",
        "lang": "vi" 
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    return {
        "temp": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"],
        "description": data["weather"][0]["description"],
        "icon": data["weather"][0]["icon"]
    }