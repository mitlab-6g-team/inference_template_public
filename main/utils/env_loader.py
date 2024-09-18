"""
load env
"""
import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Default:
    """
        load default env
    """
    LOGS_FOLDER_PATH: str
    DJANGO_SETTINGS_MODULE: str
    DEBUG: bool
    ALLOWED_HOSTS: str
    API_ROOT: str
    MODEL_SAVE_PATH: str


default_env = Default(
    LOGS_FOLDER_PATH=os.environ.get('LOGS_FOLDER_PATH'),
    DJANGO_SETTINGS_MODULE=os.environ.get('DJANGO_SETTINGS_MODULE'),
    DEBUG=os.environ.get('DEBUG'),
    ALLOWED_HOSTS=os.environ.get('ALLOWED_HOSTS'),
    API_ROOT=os.environ.get('API_ROOT'),
    MODEL_SAVE_PATH=os.environ.get('MODEL_SAVE_PATH')
)


@dataclass
class Customized:
    """
        load default env - customized
    """
    DEPLOYMENT_PLATFORM_HOST: str
    DEPLOYMENT_PLATFORM_VERSION: str


customized_env = Customized(
    DEPLOYMENT_PLATFORM_HOST=os.environ.get('DEPLOYMENT_PLATFORM_HOST'),
    DEPLOYMENT_PLATFORM_VERSION=os.environ.get('DEPLOYMENT_PLATFORM_VERSION')
)
