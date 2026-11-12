import os
import requests
from datetime import datetime

COORDINATES = {
    "mumbai": (19.0760, 72.8777),
    "pune": (18.5204, 73.8567),
    "hyderabad": (17.3850, 78.4867),
    "bengaluru": (12.9716, 77.5946),
    "ahmedabad": (23.0225, 72.5714)
}

def validate_iso_date(date_str):
    if not isinstance(date_str, str):
        return False
    import re
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", date_str):
        return False
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def get_weather(city, date):
    if not city or city.lower() not in COORDINATES:
        return {"ok": False, "error": f"unsupported city: {city}"}
        
    if not validate_iso_date(date):
        return {"ok": False, "error": f"invalid date: {date}"}
        
    city_key = city.lower()
    lat, lon = COORDINATES[city_key]
    mode = os.getenv("WEATHER_MODE", "stub").lower()
    
    if mode == "live":
        try:
            url = "https://archive-api.open-meteo.com/v1/archive"
            params = {
                "latitude": lat,
                "longitude": lon,
                "start_date": date,
                "end_date": date,
                "timezone": "Asia/Kolkata",
                "daily": "temperature_2m_mean,relative_humidity_2m_mean,wind_speed_10m_max,precipitation_sum"
            }
            response = requests.get(url, params=params, timeout=10)
            if response.status_code != 200:
                return {"ok": False, "error": f"HTTP status {response.status_code}"}
                
            data = response.json()
            daily = data.get("daily", {})
            
            temp = daily.get("temperature_2m_mean", [None])[0]
            humidity = daily.get("relative_humidity_2m_mean", [None])[0]
            wind = daily.get("wind_speed_10m_max", [None])[0]
            rain = daily.get("precipitation_sum", [None])[0]
            
            if temp is None or humidity is None or wind is None or rain is None:
                return {"ok": False, "error": "incomplete weather data received"}
                
            return {
                "ok": True,
                "city": city,
                "date": date,
                "mode": "live",
                "temperature_c": float(temp),
                "humidity_pct": float(humidity),
                "wind_kmh": float(wind),
                "rain_mm": float(rain)
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}
    else:
        # Stub mode calculation
        dt = datetime.strptime(date, "%Y-%m-%d")
        doy = dt.timetuple().tm_yday
        n = len(city)
        
        temperature_c = float(20 + (n + doy) % 15)
        humidity_pct = float(40 + (3 * n + doy) % 50)
        wind_kmh = float(5 + doy % 10)
        rain_mm = 6.5 if doy % 4 == 0 else 0.0
        
        return {
            "ok": True,
            "city": city,
            "date": date,
            "mode": "stub",
            "temperature_c": temperature_c,
            "humidity_pct": humidity_pct,
            "wind_kmh": wind_kmh,
            "rain_mm": rain_mm
        }
