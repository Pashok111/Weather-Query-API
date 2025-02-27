"""
This module contains the implementation of a database using
SQLAlchemy (PostgreSQL).
Used to store cities and queries.
"""

# Other imports
from datetime import datetime, timezone

# Main imports
from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

# Imports from project
from . import constants

url = URL.create(
    drivername='postgresql+psycopg2',
    host=constants.POSTGRES_HOST,
    port=constants.POSTGRES_PORT,
    username=constants.POSTGRES_USER,
    password=constants.POSTGRES_PASSWORD,
    database=constants.POSTGRES_NAME
)

engine = create_engine(url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class City(Base):
    __tablename__ = 'cities'

    id = Column(Integer, primary_key=True, index=True)  # noqa: A003, VNE003
    name = Column(String, index=True)
    country = Column(String, index=True)
    lat = Column(Float, index=True)
    lon = Column(Float, index=True)
    utc_timestamp = Column(
        Float, default=lambda: datetime.now(timezone.utc).timestamp()
    )

    queries = relationship(
        'Query',
        back_populates='city',
        cascade='all, delete-orphan'
    )

    def __str__(self):
        return (
            f'ID: {self.id}\n'
            f'Name: {self.name}\n'
            f'Country: {self.country}\n'
            f'Latitude: {self.lat}\n'
            f'Longitude: {self.lon}\n'
            f'Timestamp (UTC): {self.utc_timestamp}\n'
        )

    def __repr__(self):
        return (
            f'City(id={self.id}, '
            f'name={self.name}, '
            f'country={self.country}, '
            f'lat={self.lat}, '
            f'lon={self.lon}, '
            f'utc_timestamp={self.utc_timestamp})'
        )


class Query(Base):
    __tablename__ = 'queries'

    id = Column(Integer, primary_key=True, index=True)  # noqa: A003, VNE003
    city_id = Column(Integer, ForeignKey('cities.id'))
    weather_name = Column(String, index=True)
    weather_description = Column(String, index=True)
    weather_icon = Column(String, index=True)
    temp = Column(Float, index=True)
    pressure = Column(Float, index=True)
    humidity = Column(Float, index=True)
    visibility = Column(Float, index=True)
    wind_speed = Column(Float, index=True)
    wind_deg = Column(Integer, index=True)
    wind_direction = Column(String, index=True)
    wind_code = Column(String, index=True)
    cloudiness = Column(Float, index=True)
    sunrise = Column(Integer, index=True)
    sunset = Column(Integer, index=True)
    utc_timestamp = Column(
        Float, default=lambda: datetime.now(timezone.utc).timestamp()
    )

    city = relationship('City', back_populates='queries')

    def __str__(self):
        return (
            f'ID: {self.id}\n'
            f'City ID: {self.city_id}\n'
            f'Weather name: {self.weather_name}\n'
            f'Weather description: {self.weather_description}\n'
            f'Weather icon: '
            f'https://openweathermap.org/img/wn/{self.weather_icon}@2x.png\n'
            f'Temperature: {self.temp}°C\n'
            f'Pressure: {self.pressure} hPa\n'
            f'Humidity: {self.humidity}%\n'
            f'Visibility: {self.visibility}\n'
            f'Wind speed: {self.wind_speed} m/s\n'
            f'Wind degree: {self.wind_deg}°\n'
            f'Wind direction: {self.wind_direction}\n'
            f'Wind code: {self.wind_code}\n'
            f'Cloudiness: {self.cloudiness}%\n'
            f'Sunrise: {self.sunrise}\n'
            f'Sunset: {self.sunset}\n'
            f'Timestamp (UTC): {self.utc_timestamp}\n'
        )

    def __repr__(self):
        return (
            f'Query(id={self.id}, '
            f'city_id={self.city_id}, '
            f'weather_name={self.weather_name}, '
            f'weather_description={self.weather_description}, '
            f'weather_icon={self.weather_icon}, '
            f'temp={self.temp}, '
            f'pressure={self.pressure}, '
            f'humidity={self.humidity}, '
            f'visibility={self.visibility}, '
            f'wind_speed={self.wind_speed}, '
            f'wind_deg={self.wind_deg}, '
            f'wind_direction={self.wind_direction}, '
            f'wind_code={self.wind_code}, '
            f'cloudiness={self.cloudiness}, '
            f'sunrise={self.sunrise}, '
            f'sunset={self.sunset}, '
            f'utc_timestamp={self.utc_timestamp})'
        )


Base.metadata.create_all(bind=engine)
