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
    SECRET_KEY: str
    DJANGO_SETTINGS_MODULE: str
    DEBUG: bool
    ALLOWED_HOSTS: str
    API_ROOT: str
    MODEL_SAVE_PATH: str
    MODEL_FILE_NAME: str


default_env = Default(
    LOGS_FOLDER_PATH=os.environ.get('LOGS_FOLDER_PATH'),
    SECRET_KEY=os.environ.get('SECRET_KEY'),
    DJANGO_SETTINGS_MODULE=os.environ.get('DJANGO_SETTINGS_MODULE'),
    DEBUG=os.environ.get('DEBUG'),
    ALLOWED_HOSTS=os.environ.get('ALLOWED_HOSTS'),
    API_ROOT=os.environ.get('API_ROOT'),
    MODEL_SAVE_PATH=os.environ.get('MODEL_SAVE_PATH'),
    MODEL_FILE_NAME=os.environ.get('MODEL_FILE_NAME')
)


@dataclass
class Customized:
    """
        load default env - customized
    """
    DEPLOYMENT_PLATFORM_HOST: str
    SELF_CHECK_FUNCTION: bool
    DEPLOYMENT_PLATFORM_VERSION: str


customized_env = Customized(
    DEPLOYMENT_PLATFORM_HOST=os.environ.get('DEPLOYMENT_PLATFORM_HOST'),
    SELF_CHECK_FUNCTION=os.environ.get('SELF_CHECK_FUNCTION'),
    DEPLOYMENT_PLATFORM_VERSION=os.environ.get('DEPLOYMENT_PLATFORM_VERSION')
)
