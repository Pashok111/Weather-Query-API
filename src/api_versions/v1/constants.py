"""
Constants for API v1
Used in database.py and routes.py
"""

from ...configurator import MainConfigurator

__all__ = [
    'API_VERSION',
    'API_NAME',
    'MAIN_API_ADDRESS',
    'MAIN_SITE',
    'POSTGRES_HOST',
    'POSTGRES_PORT',
    'POSTGRES_USER',
    'POSTGRES_PASSWORD',
    'POSTGRES_NAME'
]

API_VERSION = 1

config = MainConfigurator()

API_NAME = config.api_name
MAIN_API_ADDRESS = config.main_api_address
MAIN_SITE = config.main_site

POSTGRES_HOST = config.postgres_host
POSTGRES_PORT = config.postgres_port
POSTGRES_USER = config.postgres_user
POSTGRES_PASSWORD = config.postgres_password
POSTGRES_NAME = config.postgres_name
