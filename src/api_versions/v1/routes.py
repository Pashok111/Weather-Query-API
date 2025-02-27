"""
Main routes for API v1
"""

# Other imports
from logging import Logger
from typing import Dict, List, Union
try:
    from typing import Annotated
except ImportError:
    # for backward compatibility, Python < 3.9
    from typing_extensions import Annotated

# Main imports
from fastapi import APIRouter, Query, Request, Response, status
from fastapi.responses import RedirectResponse

# Import from this API version
from . import constants
from .database import City as DB_City, Query as DB_Query, SessionLocal
from .pydantic_models import (
    Error,
    GetWeathersQueryParams,
    WeatherResponse
)
# Imports from project
from ...open_weather_api import APIError, OpenWeatherAPI

main_router = APIRouter()
open_weather_api = OpenWeatherAPI()
error_logger = Logger('uvicorn.error')


@main_router.get('', include_in_schema=False)
async def root(response: Response, request: Request) -> Dict[str, str]:
    """Welcome text"""
    response.status_code = status.HTTP_200_OK
    return {'welcome_text':
            f'This is the {constants.API_NAME} API, '
            f'version {constants.API_VERSION}. '
            f'You can check the docs at {request.url}/docs '
            f'and {request.url}/redoc.{constants.MAIN_SITE}'}


@main_router.get('/docs', status_code=301, include_in_schema=False)
async def docs_redirect() -> RedirectResponse:
    """Redirect to docs from any API version"""
    return RedirectResponse(
        f'{constants.MAIN_API_ADDRESS}/docs', status_code=301
    )


@main_router.get('/redoc', status_code=301, include_in_schema=False)
async def redoc_redirect() -> RedirectResponse:
    """Redirect to redoc from any API version"""
    return RedirectResponse(
        f'{constants.MAIN_API_ADDRESS}/redoc', status_code=301
    )


@main_router.get('/openapi.json', status_code=301, include_in_schema=False)
async def openapi_json_redirect() -> RedirectResponse:
    """Redirect to openapi.json from any API version"""
    return RedirectResponse(
        f'{constants.MAIN_API_ADDRESS}/openapi.json', status_code=301
    )


# ######################## GET WEATHER FROM CITY ######################## #
@main_router.get(
    '/weather/{city_name}',
    responses={
        200: {'model': WeatherResponse},
        500: {'model': Error}
    }
)
async def get_weather(
        response: Response,
        city_name: str,
) -> Union[WeatherResponse, Error]:  # noqa
    db = SessionLocal()
    try:
        db_city = db.query(DB_City).filter(DB_City.name == city_name).first()

        if not db_city:
            try:
                city_data = open_weather_api.get_geo_data(city_name)
            except APIError as e:
                error_logger.error(e)
                response.status_code = status.HTTP_400_BAD_REQUEST
                return Error(error=str(e))
            db_city = DB_City(
                name=city_name,
                country=city_data.country,
                lat=city_data.lat,
                lon=city_data.lon
            )
            db.add(db_city)
            db.commit()

        try:
            weather_data = open_weather_api.get_weather_data(
                db_city.lat,
                db_city.lon
            )
        except APIError as e:
            error_logger.error(e)
            response.status_code = status.HTTP_400_BAD_REQUEST
            return Error(error=str(e))
        db_query = DB_Query(
            city_id=db_city.id,
            weather_name=weather_data.weather_name,
            weather_description=weather_data.weather_description,
            weather_icon=weather_data.weather_icon,
            temp=weather_data.temp,
            pressure=weather_data.pressure,
            humidity=weather_data.humidity,
            visibility=weather_data.visibility,
            wind_speed=weather_data.wind_speed,
            wind_deg=weather_data.wind_degree,
            wind_direction=weather_data.wind_direction,
            wind_code=weather_data.wind_code,
            cloudiness=weather_data.cloudiness,
            sunrise=weather_data.sunrise,
            sunset=weather_data.sunset
        )
        db.add(db_query)
        db.commit()

        updated_query = db.get(DB_Query, db_query.id)
        updated_city = db.get(DB_City, updated_query.city_id)
    except Exception as e:  # noqa: B902
        error_logger.error(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return Error(error=str(e))
    finally:
        db.close()

    response.status_code = status.HTTP_200_OK
    return WeatherResponse(
        id=updated_query.id,
        city_name=updated_city.name,
        city_country=updated_city.country,
        latitude=updated_city.lat,
        longitude=updated_city.lon,
        weather_name=updated_query.weather_name,
        weather_description=updated_query.weather_description,
        weather_icon='https://openweathermap.org/img/wn/'
                     f'{updated_query.weather_icon}@2x.png',
        temp=updated_query.temp,
        pressure=updated_query.pressure,
        humidity=updated_query.humidity,
        visibility=updated_query.visibility,
        wind_speed=updated_query.wind_speed,
        wind_degree=updated_query.wind_deg,
        wind_direction=updated_query.wind_direction,
        wind_code=updated_query.wind_code,
        cloudiness=updated_query.cloudiness,
        sunrise=updated_query.sunrise,
        sunset=updated_query.sunset,
        utc_timestamp=updated_query.utc_timestamp
    )


# ######################## GET WEATHER BY QUERY ID ######################## #
@main_router.get(
    '/queries/{query_id}',
    responses={
        200: {'model': WeatherResponse},
        400: {'model': Error},
        500: {'model': Error}
    }
)
async def get_query(
        response: Response,
        query_id: int
) -> Union[WeatherResponse, Error]:  # noqa
    db = SessionLocal()
    try:
        db_query = db.get(DB_Query, query_id)
        if not db_query:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return Error(error='No weather query with this ID')
        db_city = db_query.city
    except Exception as e:  # noqa: B902
        error_logger.error(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return Error(error=str(e))
    finally:
        db.close()

    response.status_code = status.HTTP_200_OK
    return WeatherResponse(
        id=db_query.id,
        city_name=db_city.name,
        city_country=db_city.country,
        latitude=db_city.lat,
        longitude=db_city.lon,
        weather_name=db_query.weather_name,
        weather_description=db_query.weather_description,
        weather_icon='https://openweathermap.org/img/wn/'
                     f'{db_query.weather_icon}@2x.png',
        temp=db_query.temp,
        pressure=db_query.pressure,
        humidity=db_query.humidity,
        visibility=db_query.visibility,
        wind_speed=db_query.wind_speed,
        wind_degree=db_query.wind_deg,
        wind_direction=db_query.wind_direction,
        wind_code=db_query.wind_code,
        cloudiness=db_query.cloudiness,
        sunrise=db_query.sunrise,
        sunset=db_query.sunset,
        utc_timestamp=db_query.utc_timestamp
    )


# ######################## GET ALL WEATHER QUERIES ######################## #
@main_router.get(
    '/queries',
    responses={
        200: {'model': List[WeatherResponse]},
        400: {'model': Error},
        500: {'model': Error}
    }
)
async def get_queries(
        response: Response,
        filter_query: Annotated[GetWeathersQueryParams, Query()]
) -> Union[List[WeatherResponse], Error]:  # noqa
    limit = filter_query.limit
    offset = filter_query.offset
    descending = filter_query.descending

    db = SessionLocal()
    try:
        db_queries = db.query(
            DB_Query
        ).order_by(
            DB_Query.id.desc() if descending else DB_Query.id.asc()
        ).limit(limit).offset(limit * offset).all()
        if len(db_queries) == 0:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return Error(error='End of weather queries')
        db_queries = [
            WeatherResponse(
                id=db_query.id,
                city_name=db_query.city.name,
                city_country=db_query.city.country,
                latitude=db_query.city.lat,
                longitude=db_query.city.lon,
                weather_name=db_query.weather_name,
                weather_description=db_query.weather_description,
                weather_icon='https://openweathermap.org/img/wn/'
                             f'{db_query.weather_icon}@2x.png',
                temp=db_query.temp,
                pressure=db_query.pressure,
                humidity=db_query.humidity,
                visibility=db_query.visibility,
                wind_speed=db_query.wind_speed,
                wind_degree=db_query.wind_deg,
                wind_direction=db_query.wind_direction,
                wind_code=db_query.wind_code,
                cloudiness=db_query.cloudiness,
                sunrise=db_query.sunrise,
                sunset=db_query.sunset,
                utc_timestamp=db_query.utc_timestamp
            )
            for db_query in db_queries
        ]
    except Exception as e:  # noqa: B902
        error_logger.error(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return Error(error=str(e))
    finally:
        db.close()

    response.status_code = status.HTTP_200_OK
    return db_queries
