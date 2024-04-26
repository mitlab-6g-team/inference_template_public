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
    LOGS_FOLDER_PATH:str
    SECRET_KEY:str
    DJANGO_SETTINGS_MODULE:str
    DEBUG:bool
    ALLOWED_HOSTS:str
    API_ROOT:str
    API_VERSION:str
    MODEL_SAVE_PATH:str
    MODEL_FILE_NAME:str
    HTTP_KAFKA_HOST:str
    HTTP_KAFKA_PORT1:str
    HTTP_KAFKA_PORT2:str
    HTTP_KAFKA_PORT3:str
    KAFKA_ENABLE:bool


default_env = Default(
    LOGS_FOLDER_PATH=os.environ.get('LOGS_FOLDER_PATH'),
    SECRET_KEY=os.environ.get('SECRET_KEY'),
    DJANGO_SETTINGS_MODULE=os.environ.get('DJANGO_SETTINGS_MODULE'),
    DEBUG=os.environ.get('DEBUG'),
    ALLOWED_HOSTS=os.environ.get('ALLOWED_HOSTS'),
    API_ROOT=os.environ.get('API_ROOT'),
    API_VERSION=os.environ.get('API_VERSION'),
    MODEL_SAVE_PATH=os.environ.get('MODEL_SAVE_PATH'),
    MODEL_FILE_NAME=os.environ.get('MODEL_FILE_NAME'),
    HTTP_KAFKA_HOST=os.environ.get('HTTP_KAFKA_HOST'),
    HTTP_KAFKA_PORT1=os.environ.get('HTTP_KAFKA_PORT1'),
    HTTP_KAFKA_PORT2=os.environ.get('HTTP_KAFKA_PORT2'),
    HTTP_KAFKA_PORT3=os.environ.get('HTTP_KAFKA_PORT3'),
    KAFKA_ENABLE=os.environ.get('KAFKA_ENABLE')
)
