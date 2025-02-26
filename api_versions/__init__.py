"""
This module contains all API versions and the latest version variable for
convenience.
API versions are added to the `API_VERSIONS` list in descending order.
"""

from . import v1

__all__ = [
    'API_LATEST',
    'API_VERSIONS',
    'v1'
]

API_VERSIONS = [v1]
API_LATEST = API_VERSIONS[0]
