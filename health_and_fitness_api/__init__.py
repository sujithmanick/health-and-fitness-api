from flask import Flask
from pymongo import MongoClient
import os
import json
from cryptography.fernet import Fernet
import logging

app = None
db = None
log = None

def create_app():
    global app
    global db
    global log
    
    with open('config.json', mode='r') as config_file:
        config_data = json.load(config_file)

    class Base_config():
        APPLICATION_PROTOCOL = config_data['APPLICATION_PROTOCOL']
        APPLICATION_HOST = config_data['APPLICATION_HOST']
        APPLICATION_PORT = config_data['APPLICATION_PORT']
        MONGO_DATABASE_URI = config_data['MONGO_DATABASE_URI'] #os.environ.get('MONGO_DATABASE_URI')
        SECRET_KEY = config_data['APP_SECRET_KEY']
        SMTP_SSL_HOST = config_data['SMTP_SSL_HOST']
        SMTP_SSL_PORT = config_data['SMTP_SSL_PORT']
        MAIL_SENDER_ADDRESS = config_data['MAIL_SENDER_ADDRESS']
        MAIL_SENDER_PASSWORD = config_data['MAIL_SENDER_PASSWORD']
        JWT_SECRET = config_data['JWT_SECRET']
        ENCRYPTION_KEY = config_data['ENCRYPTION_KEY'] #Fernet.generate_key()
        JWT_HASH_ALGORITHM = config_data['JWT_HASH_ALGORITHM']
        DEBUG = config_data['DEBUG']

    app = Flask(__name__)
    log = logging.getLogger('health_and_fitness_api')
    logging.basicConfig(filemode='haf_log.log',encoding='utf-8',level=config_data['LOGLEVEL'],format=config_data['LOGGER_FORMAT'])
    try:
        app.config.from_object(Base_config)
        log.info('App settings configured')  
    except:
        log.error('App config failed')


    try:
        client = MongoClient(app.config['MONGO_DATABASE_URI'])
        db = client.health_and_fitness_api
        if db != None: 
            log.info('DB settings configured') 
        else:
            log.error('DB connection failed')
    except:
        log.error('DB connection failed')

    try:
        from . import urls, routes
        log.info('Imported endpoints')
    except ImportError:
        log.error('Imported endpoints failed')

    return app