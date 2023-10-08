from flask import Flask
from pymongo import MongoClient
import os
import json
from cryptography.fernet import Fernet

app = None
db = None

def create_app():
    global app
    global db

    with open('config.json', mode='r') as config_file:
        config_data = json.load(config_file)

    class Base_config():
        DEBUG = False
        TESTING = False
        APPLICATION_HOST = config_data['APPLICATION_HOST']
        MONGO_DATABASE_USERNAME = ''
        MONGO_DATABASE_PASSWORD = ''
        MONGO_DATABASE_URI = config_data['MONGO_DATABASE_URI'] #os.environ.get('MONGO_DATABASE_URI')
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        SECRET_KEY = config_data['APP_SECRET_KEY']
        SMTP_SSL_HOST = config_data['SMTP_SSL_HOST']
        SMTP_SSL_PORT = config_data['SMTP_SSL_PORT']
        MAIL_SENDER_ADDRESS = config_data['MAIL_SENDER_ADDRESS']
        MAIL_SENDER_PASSWORD = config_data['MAIL_SENDER_PASSWORD']
        ENCRYPTION_KEY = Fernet.generate_key()
        DEBUG = True

    app = Flask(__name__)
    app.config.from_object(Base_config)  

    client = MongoClient(app.config['MONGO_DATABASE_URI'])
    db = client.health_and_fitness_api


    from . import urls, routes

    return app                                           

create_app()