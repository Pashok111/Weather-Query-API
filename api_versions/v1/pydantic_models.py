"""
Pydantic models for API v1
"""

# Main imports
from pydantic import BaseModel, Field


class Error(BaseModel):
    error: str


class WeatherResponse(BaseModel):
    id: int  # noqa: A003, VNE003
    city_name: str
    city_country: str
    latitude: float
    longitude: float
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
    utc_timestamp: float


class GetWeathersQueryParams(BaseModel):
    model_config = {'extra': 'forbid'}

    limit: int = Field(20, ge=1, le=100)
    offset: int = Field(0, ge=0)
    descending: bool = False
