"""
Main starting point for the API
"""

# Main imports
from fastapi import FastAPI, Request
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html
)
from fastapi.staticfiles import StaticFiles

# Imports from project
from .api_versions import API_LATEST, API_VERSIONS  # noqa: I100
from .configurator import MainConfigurator

# Config loading
config = MainConfigurator()

DESCRIPTION = (f'This is the {config.api_name} API.\n\n'
               f'You can check the docs at {config.main_api_address}/docs '
               f'and {config.main_api_address}/redoc.{config.main_site}')

app = FastAPI(
    title=f'{config.api_name} API',
    description=DESCRIPTION,
    version='1.0.0',
    openapi_url=f'{config.main_api_address}/openapi.json',
    docs_url=None,
    redoc_url=None,
    swagger_ui_oauth2_redirect_url=f'{config.main_api_address}'
                                   f'/docs/oauth2-redirect'
)
app.mount(
    path=f'{config.main_api_address}/{config.static_dir}',
    app=StaticFiles(directory=config.static_dir),
    name='static'
)


@app.get('/', include_in_schema=False)
async def root(request: Request):
    return {'welcome_text':
            f'This is the {config.api_name} API. '
            f'Check {request.url}{config.main_api_address[1:]} for more info.'}


@app.get(f'{config.main_api_address}/docs', include_in_schema=False)
async def custom_docs():
    """Redefined docs endpoint"""
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,  # noqa
        title=app.title + ' - Swagger Docs',  # noqa
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,  # noqa
        swagger_js_url=config.swagger_js,
        swagger_css_url=config.swagger_css,
        swagger_favicon_url=config.favicon
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)  # noqa
async def custom_oauth2():
    """Redefined oauth2 redirect endpoint"""
    return get_swagger_ui_oauth2_redirect_html()


@app.get(f'{config.main_api_address}/redoc', include_in_schema=False)
async def custom_redoc():
    """Redefined redoc endpoint"""
    return get_redoc_html(
        openapi_url=app.openapi_url,  # noqa
        title=app.title + ' - ReDoc',  # noqa
        redoc_js_url=config.redoc_js,
        redoc_favicon_url=config.favicon
    )

app.include_router(
    API_LATEST.main_router,
    prefix=config.main_api_address,
    tags=['default'],
    include_in_schema=False
)
app.include_router(
    API_LATEST.main_router,
    prefix=config.main_api_address + '/latest',
    tags=['latest'],
    include_in_schema=False
)

for version in API_VERSIONS:
    app.include_router(
        version.main_router,
        prefix=config.main_api_address + f'/v{version.API_VERSION}',
        tags=[f'v{version.API_VERSION}']
    )
