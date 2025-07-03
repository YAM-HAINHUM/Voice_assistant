import requests

city = "Thane"
api_key = "f40317b78fd1a0ba7f1419d24fbab29b"
base_url = "http://api.openweathermap.org/data/2.5/weather?"
complete_url = f"{base_url}q={city}&appid={api_key}&units=metric"

response = requests.get(complete_url)
print(f"Status Code: {response.status_code}")
print(response.json())
