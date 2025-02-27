"""
This module contains the base implementation of a logger and special method
in ``Logger`` class for creating configuration for uvicorn.
"""
import logging
import os
from datetime import datetime
from typing import Union

__all__ = ['Logger']

DEFAULT_LOG_DIR = 'logs'
DEFAULT_LOG_NAME = datetime.now().strftime('%Y-%m-%d__%H-%M-%S%z') + '.log'
DEFAULT_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
DEFAULT_DATE_FORMAT = '%Y-%m-%d %H-%M-%S%z'


class Logger:
    def __init__(
            self,
            logger_name: str = 'logger',
            save_logs: bool = True,
            logs_dir: str = DEFAULT_LOG_DIR,
            log_filename: Union[str, None] = DEFAULT_LOG_NAME
    ):
        """
        Initializes logging for console and for file output
        if ``save_logs`` is True.
        """
        self._save_logs = save_logs
        self._logs_dir = logs_dir
        self._log_filename = log_filename

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)

        formatter = logging.Formatter(
            DEFAULT_FORMAT, datefmt=DEFAULT_DATE_FORMAT
        )
        stream_handler.setFormatter(formatter)

        self._logger = logging.getLogger(logger_name)
        self._logger.setLevel(logging.INFO)
        self._logger.addHandler(stream_handler)
        if self._save_logs:
            if not self._log_filename:
                self._log_filename = DEFAULT_LOG_NAME
            os.makedirs(self._logs_dir, exist_ok=True)
            full_log_path = os.path.join(self._logs_dir, self._log_filename)
            file_handler = logging.FileHandler(full_log_path)
            file_handler.setLevel(logging.INFO)
            file_handler.setFormatter(formatter)
            self._logger.addHandler(file_handler)

    @property
    def logger(self):
        return self._logger

    def get_logger(self):
        return self._logger

    def logging_config(self) -> dict:
        """Creating configuration for uvicorn logging."""
        cfg = {
            'version': 1,
            'disable_existing_loggers': True,
            'formatters': {
                'default': {
                    'format': DEFAULT_FORMAT,
                    'datefmt': DEFAULT_DATE_FORMAT
                }
            },
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    'level': 'INFO',
                    'formatter': 'default'
                }
            },
            'loggers': {
                'uvicorn': {
                    'handlers': ['console'],
                    'level': 'TRACE',
                    'propagate': False
                },
                'uvicorn.access': {
                    'handlers': ['console'],
                    'level': 'TRACE',
                    'propagate': False
                },
                'uvicorn.error': {
                    'handlers': ['console'],
                    'level': 'TRACE',
                    'propagate': False
                },
                'uvicorn.asgi': {
                    'handlers': ['console'],
                    'level': 'TRACE',
                    'propagate': False
                },
            }
        }
        if self._save_logs:
            cfg['handlers']['file'] = {
                'class': 'logging.FileHandler',
                'level': 'INFO',
                'formatter': 'default',
                'filename': os.path.join(
                    self._logs_dir, self._log_filename
                )
            }
            logger_names = (
                'uvicorn', 'uvicorn.access', 'uvicorn.error', 'uvicorn.asgi'
            )
            for logger_name in logger_names:
                cfg['loggers'][logger_name]['handlers'].append('file')
        return cfg
