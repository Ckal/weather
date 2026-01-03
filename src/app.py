import gradio as gr
import requests

def get_time_and_weather(city: str, country: str) -> dict:
    """
    Returns the current time and weather for the specified city and country.
    """
    try:
        
        # 1. Get lat/lon from Open-Meteo's Geocoding API (no key required!)
        geo_res = requests.get("https://geocoding-api.open-meteo.com/v1/search", params={
            "name": city,
            "count": 1,
            "language": "en",
            "format": "json"
        })

        if geo_res.status_code != 200:
            return {"error": f"Geolocation failed. Status: {geo_res.status_code}"}

        geo_data = geo_res.json()
        results = geo_data.get("results", [])

        if not results:
            return {"error": f"Could not find location: {city}, {country}"}

        lat = results[0]["latitude"]
        lon = results[0]["longitude"]
        timezone = results[0]["timezone"]
 
        print(f"Location: {city}, {country}")
        print(f"Latitude: {lat}, Longitude: {lon}")
        print(f"Timezone: {timezone}")
        # 2. Get weather from Open-Meteo
        weather_url = "https://api.open-meteo.com/v1/forecast"
        weather_res = requests.get(weather_url, params={
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,weathercode"
        })

        if weather_res.status_code != 200:
            return {"error": f"Weather API failed. Status: {weather_res.status_code}"}

        weather_data = weather_res.json()
        current_weather = weather_data.get("current", {})
        temperature = current_weather.get("temperature_2m", "N/A")
        weather_code = current_weather.get("weathercode", "N/A")

        # 3. Get timezone from lat/lon using TimeZoneDB (no key alternative)
       # timezone_res = requests.get("http://worldtimeapi.org/api/timezone")

        #if timezone_res.status_code != 200:
        #    return {"error": f"Timezone list fetch failed. Status: {timezone_res.status_code}"}

        #all_timezones = timezone_res.json()
        #match = next((tz for tz in all_timezones if city.lower() in tz.lower()), None)

        #if not match:
        #    match = next((tz for tz in all_timezones if country.lower() in tz.lower()), None)

        #if not match:
        #    return {"error": f"No matching timezone found for {city}, {country}"}

        #time_detail_res = requests.get(f"http://worldtimeapi.org/api/timezone/{match}")
        #if time_detail_res.status_code != 200:
        #    return {"error": f"Time fetch failed for zone: {match}"}

        #time_data = time_detail_res.json()
        #datetime = time_data.get("datetime", "N/A")

        return {
            "location": f"{city}, {country}",
            "timezone": "n/a",
            "local_time": "n/a",
            "temperature (°C)": temperature,
            "weather_code": weather_code
        }

    except Exception as e:
        return {"error": f"{type(e).__name__}: {str(e)}"}

iface = gr.Interface(
    fn=get_time_and_weather,
    inputs=[gr.Textbox(label="City", value="Berlin"), gr.Textbox(label="Country", value="Germany")],
    outputs=[gr.JSON()],
    title="🌍 Weather & Time Oracle",
    description="Enter a city and country to get the local time and current weather.",
)

if __name__ == "__main__":
    iface.launch(mcp_server=True, share=True, debug=True)
