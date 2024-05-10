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
    SECRET_KEY:str
    DJANGO_SETTINGS_MODULE:str
    DEBUG:bool
    ALLOWED_HOSTS:str
    API_ROOT:str
    API_VERSION:str
    DB_NAME:str
    DB_USER:str
    DB_PASSWORD:str
    DB_HOST:str
    DB_PORT:int
    RPC_URL:str
    

env_loader = Default(
    SECRET_KEY=os.environ.get('SECRET_KEY'),
    DJANGO_SETTINGS_MODULE=os.environ.get('DJANGO_SETTINGS_MODULE'),
    DEBUG=os.environ.get('DEBUG'),
    ALLOWED_HOSTS=os.environ.get('ALLOWED_HOSTS'),
    API_ROOT=os.environ.get('API_ROOT'),
    API_VERSION=os.environ.get('API_VERSION'),
    DB_NAME=os.environ.get('DB_NAME'),
    DB_USER=os.environ.get('DB_USER'),
    DB_PASSWORD=os.environ.get('DB_PASSWORD'),
    DB_HOST=os.environ.get('DB_HOST'),
    DB_PORT=os.environ.get('DB_PORT'),
    RPC_URL=os.environ.get('RPC_URL'),
)
