"""
This module contains the base implementation of the OpenWeatherMap API.
"""

import os
from typing import Tuple, Union

from dotenv import load_dotenv

from pydantic import BaseModel

import requests

load_dotenv('.env.api')
OPEN_WEATHER_API_KEY = os.getenv('OPEN_WEATHER_API_KEY')

if not OPEN_WEATHER_API_KEY:
    raise ValueError('OPEN_WEATHER_API_KEY is not set')

OPEN_WEATHER_GEO_URL = 'https://api.openweathermap.org/geo/1.0/direct'
OPEN_WEATHER_DATA_URL = 'https://api.openweathermap.org/data/2.5/weather'

OPEN_WEATHER_GEO_PARAMS = {
    'appid': OPEN_WEATHER_API_KEY,
    'limit': 1
}

OPEN_WEATHER_DATA_PARAMS = {
    'appid': OPEN_WEATHER_API_KEY,
    'units': 'metric',
    'lang': 'en'
}


APIError = ValueError


class City(BaseModel):
    name: str
    country: str
    lat: float
    lon: float


class WeatherInfo(BaseModel):
    weather_name: str
    weather_description: str
    weather_icon: str
    temp: float
    pressure: float
    humidity: float
    visibility: float
    wind_speed: float
    wind_degree: int
    wind_direction: str
    wind_code: str
    cloudiness: float
    sunrise: int
    sunset: int


class OpenWeatherAPI:
    def __init__(self):
        self._geo_url = OPEN_WEATHER_GEO_URL
        self._data_url = OPEN_WEATHER_DATA_URL
        self._geo_params = OPEN_WEATHER_GEO_PARAMS
        self._data_params = OPEN_WEATHER_DATA_PARAMS

    def get_geo_data(self, city) -> City:
        params = self._geo_params.copy()
        params['q'] = city
        response = requests.get(self._geo_url, params=params)
        if not response.json():
            raise APIError('No such city')
        if (not isinstance(response.json(), list)
                and response.json()['cod'] != 200):
            raise APIError(response.json()['message'])
        _json = response.json()
        return City(
            name=city,
            country=_json[0]['country'],
            lat=_json[0]['lat'],
            lon=_json[0]['lon']
        )

    def get_weather_data(self, lat, lon):
        params = self._data_params.copy()
        params['lat'] = lat
        params['lon'] = lon
        response = requests.get(self._data_url, params=params)
        if response.json()['cod'] != 200:
            raise APIError(response.json()['message'])
        _json = response.json()
        wind_d, wind_c = self.get_direction(_json['wind']['deg'])
        return WeatherInfo(
            weather_name=_json['weather'][0]['main'],
            weather_description=_json['weather'][0]['description'],
            weather_icon=_json['weather'][0]['icon'],
            temp=_json['main']['temp'],
            pressure=_json['main']['pressure'],
            humidity=_json['main']['humidity'],
            visibility=_json['visibility'],
            wind_speed=_json['wind']['speed'],
            wind_degree=_json['wind']['deg'],
            wind_direction=wind_d,
            wind_code=wind_c,
            cloudiness=_json['clouds']['all'],
            sunrise=_json['sys']['sunrise'],
            sunset=_json['sys']['sunset']
        )

    @staticmethod
    def get_direction(degrees: Union[int, float]) -> Tuple[str, str]:
        """Convert degrees to direction and code (1-2 letters)"""
        degrees = degrees % 360

        if 22.5 <= degrees < 67.5:
            return 'Northeast', 'NE'
        elif 67.5 <= degrees < 112.5:
            return 'East', 'E'
        elif 112.5 <= degrees < 157.5:
            return 'Southeast', 'SE'
        elif 157.5 <= degrees < 202.5:
            return 'South', 'S'
        elif 202.5 <= degrees < 247.5:
            return 'Southwest', 'SW'
        elif 247.5 <= degrees < 292.5:
            return 'West', 'W'
        elif 292.5 <= degrees < 337.5:
            return 'Northwest', 'NW'
        else:
            return 'North', 'N'
