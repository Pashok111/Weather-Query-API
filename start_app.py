import uvicorn

# Imports from project
from src.configurator import MainConfigurator  # noqa: I100
from src.logger import Logger

if __name__ == '__main__':
    # Config loading
    config = MainConfigurator()

    # Logger initialization
    logger = Logger(
        logger_name=config.api_name,
        save_logs=config.save_logs,
        logs_dir=config.logs_dir,
        log_filename=config.log_filename
    )

    uvicorn_config = {
        'app': 'src:app',
        'host': config.host,
        'port': config.port,
        'log_config': logger.logging_config(),
    }
    if config.dev:
        uvicorn_config['reload'] = True
        uvicorn_config['reload_includes'] = [
            'api_versions',
            'configurator',
            'logger',
            'open_weather_api',
            'main.py'
        ]
    uvicorn.run(**uvicorn_config)
