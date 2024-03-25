import requests
import APIkeys


class WeatherApi:
    def __init__(self, key):
        self.weather_key = key
        self.url = f'https://api.openweathermap.org/data/2.5/forecast'

    def get_weather(self, cords):
        parameters = {
            "lat": cords[0],
            "lon": cords[1],
            "appid": self.weather_key,
            "units": 'metric',
            "cnt": 10
        }

        response = requests.get(self.url, params=parameters)

        if response.status_code == 200:
            data = response.json()
            return data

        else:
            print(f"error: {response.status_code}")
            return

    def get_air(self, cords):
        parameters = {
            "lat": cords[0],
            "lon": cords[1],
            "appid": self.weather_key
        }

        url = f'http://api.openweathermap.org/data/2.5/air_pollution?'
        response = requests.get(url, params=parameters)

        if response.status_code == 200:
            data = response.json()
            return data

        else:
            print(f"error: {response.status_code}")
            return
