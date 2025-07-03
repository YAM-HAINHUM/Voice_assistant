# === FILE: location_utils.py ===
import requests

def get_current_location():
    """
    Fetches the user's current location using IP geolocation.

    Returns:
        dict: {
            "latitude": float,
            "longitude": float,
            "city": str,
            "region": str,
            "country": str
        }
        or None if the request fails.
    """
    try:
        response = requests.get("https://ipinfo.io/json")
        if response.status_code == 200:
            data = response.json()
            loc = data.get("loc", "0,0").split(',')
            return {
                "latitude": float(loc[0]),
                "longitude": float(loc[1]),
                "city": data.get("city", "Unknown"),
                "region": data.get("region", "Unknown"),
                "country": data.get("country", "Unknown")
            }
        else:
            print(f"⚠️ Location fetch failed: HTTP {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Exception while fetching location: {e}")
        return None

