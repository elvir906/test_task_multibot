import requests
from decouple import config

from utils import cities

appid = config('APPID')


def get_weather(city_id: str):
    """
    Метод для извлечения данных о погоде с OpenWeatherMap
    """
    def get_key(d, value):
        """извлечение ключа словаря по его значению"""
        for k, v in d.items():
            if v == value:
                return k

    try:
        res = requests.get(
            "http://api.openweathermap.org/data/2.5/weather",
            params={
                'id': city_id,
                'units': 'metric',
                'lang': 'ru',
                'APPID': appid
            }
        )
        data = res.json()

        wether_info = (
            f"*Город:* {get_key(cities, int(city_id))}\n"
            + f"*атмосферные условия:* {data['weather'][0]['description']}\n"
            + f"*температура:* {data['main']['temp']} °C"
        )
        return wether_info

    except Exception as e:
        print("Exception (weather):", e)
        pass
