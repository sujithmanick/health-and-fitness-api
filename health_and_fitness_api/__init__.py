from flask import Flask
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os


class Base_config():
    DEBUG = False
    TESTING = False
    MONGO_DATABASE_USERNAME = ''
    MONGO_DATABASE_PASSWORD = ''
    MONGO_DATABASE_URI = ''
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = ''

app = Flask(__name__)
app.config.from_object(Base_config)  

from . import urls, routes                                           
