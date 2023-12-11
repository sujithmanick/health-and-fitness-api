from . import app, log
from flask import request, session, jsonify
from passlib.hash import sha256_crypt
import string
import random
from datetime import datetime, timedelta
import jwt
from functools import wraps

 
from health_and_fitness_api.util.validate import validate_signup
from health_and_fitness_api.util.messenger import send_verification_email
from health_and_fitness_api.util.db import users_db
from health_and_fitness_api.core.scrapper import diet_plan_scraper

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        jwt_options = {
        'verify_signature': True,
        'verify_exp': True,
        'verify_nbf': False,
        'verify_iat': True,
        'verify_aud': False
    }
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        print(token)
        if not token:
            return (jsonify({'Message': ' Token is missing'}), 401)
        try:
            data = jwt.decode(token, key=app.config['JWT_SECRET'],options=jwt_options,algorithms=['HS256', ])
            current_user = users_db.find_one({"mail_id": data['mail_id']})
            print('logged in user :'+str(current_user['mail_id']))
        except Exception as e:
            print(e)
            return (jsonify({'Message': 'Token is invalid'}), 401)
        return f(current_user, *args, **kwargs)
    return decorated

def user_signup():
    session['data'] = request.get_json()
    session['first-name'] = session['data']["first-name"]
    session['last-name'] = session['data']["last-name"]
    session['mail-id'] = session['data']["mail-id"]
    session['phone-number'] = session['data']["phone-number"]
    session['gender'] = session['data']["gender"]
    session['age'] = session['data']["age"]
    session['password'] = session['data']["password"]
    session['active'] = False
    session['rand-key'] = str(''.join(random.choices(string.ascii_lowercase + string.digits, k=20)))
    session['acc-creation-date'] = datetime.now()
    session['acc-verification-date'] = ''

    validation_results=validate_signup(session['mail-id'], session['password'],\
                        session['first-name'], session['age'], session['gender'])
    
    if validation_results == True:
        if users_db.find_one({"mail_id": session['mail-id']}):
            return jsonify(message='You already have an account, Try logging in')

        users_db.insert_one({"first_name": session['first-name'], \
                        "last_name": session['last-name'], "gender": session['gender'],\
                            "mail_id": session['mail-id'], "password" : sha256_crypt.encrypt(session['password']),\
                            "age": session['age'],"phone_number": session['phone-number'], "active" : session['active'],\
                                "rand_key" : session['rand-key'], "acc_creation_date" : session["acc-creation-date"],\
                                    "acc_verification_date" : session['acc-verification-date']})
        
        if app.config["APPLICATION_PORT"] == '':
            link = f'{app.config["APPLICATION_PROTOCOL"]}://{app.config["APPLICATION_HOST"]}/verify/{session["rand-key"]}'
        else:
            link = f'{app.config["APPLICATION_PROTOCOL"]}://{app.config["APPLICATION_HOST"]}:{app.config["APPLICATION_PORT"]}/verify/{session["rand-key"]}'

        send_verification_email(app, session['first-name'], session['mail-id'], link)
        
        return jsonify(message="Congratulations! You are one step closer to unlocking\
                        the full potential of your account. We have sent a verification\
                        email to your registered email address. Please check your inbox and follow the\
                        instructions to verify your account. Once you have verified your account, you will\
                        be able to access all the features and benefits of our platform. Thank you for choosing us!"), 200
    else:
        return validation_results, 401

def user_verify(random_key):
    user_data = users_db.find_one({"rand_key": random_key})
    if user_data:
        if user_data["active"]:
            return jsonify(message='You account has already activated')
        
        users_db.update_one({"rand_key": random_key},{ "$set" :{"acc_verification_date": datetime.now(), "active": True, "rand_key": random_key}})
        return jsonify(message='You account has been activated'), 201

    return jsonify(message = "Can\'t verify you account"), 400

def user_login():
    session["data"] = request.get_json()
    session["mail-id"] = session["data"]["mail-id"]
    session["password"] = session["data"]["password"]

    user = users_db.find_one({"mail_id": session["mail-id"]})
    if user != None:
        db_password = user['password']
        if sha256_crypt.verify(session["password"], db_password):
            token_validity = str(datetime.now() + timedelta(days=1))
            user_payload = {"mail_id":session["mail-id"], "created_at":str(datetime.now()), "valid_till":token_validity}
            new_token = jwt.encode(payload=user_payload, key=app.config['JWT_SECRET'])
            return jsonify(token=new_token, validity=token_validity), 200
        else:
            return jsonify(message='Invalid credentials'), 401
    else:
        return jsonify(message='No account found'), 404
    
@token_required
def get_diet_plans(current_user):
    session["user"] = current_user["mail_id"]
    session["calories"] = request.args.get("cals")
    session["protein"] = request.args.get("p")
    session["fat"] = request.args.get("f")
    session["carbs"] = request.args.get("c")
    session["diet"] = request.args.get("diet")
    print(session)
    diet_plans_scrab_url = f'https://www.prospre.io/meal-plans?cals={session["calories"]}&p={session["protein"]}&f={session["fat"]}&c={session["carbs"]}&diet={session["diet"]}'
    
    return jsonify(message=diet_plan_scraper(diet_plans_scrab_url)),200

@token_required
def calculate_cal(current_user):
    session['cal_data'] = request.get_json()
    session["user"] = current_user['mail_id']
    session['gender'] = session['cal_data']['gender']
    session['weight_type'] = session['cal_data']['weight_type']
    session['weight'] = session['cal_data']['weight']
    session['height'] = session['cal_data']['height']
    session['age'] = session['cal_data']['age']

    """Metric formula for men
    BMR = (10 × weight in kg) + (6.25 × height in cm) − (5 × age in years) + 5

    Imperial formula for men
    BMR = (4.536 × weight in pounds) + (15.88 × height in inches) − (5 × age) + 5

    Metric formula for women
    BMR = (10 × weight in kg) + (6.25 × height in cm) − (5 × age in years) − 161

    Imperial formula for women
    BMR = (4.536 × weight in pounds) + (15.88 × height in inches) − (5 × age) − 161;"""

    if session['gender'] == 'men':
        if session['weight_type'] == 'metric':
            session['bmr'] = (10 * session['weight']) + (6.25 * float(session['height'])) - (5 * int(session['age'])) + 5
        elif session['weight_type'] == 'imperial':
            session['bmr'] = (4.536 * session['weight']) + (15.88 * float(session['height'])) - (5 * int(session['age'])) + 5
        else:
            log.debug(f'Error, {session["user"]} has entred weight_type as {session["weight_type"]} in calculate_cal')
            return jsonify(message='The weight_type entred was invalid'),401
    elif session['gender'] == 'women':
        if session['weight_type'] == 'metric':
            session['bmr'] = (10 * session['weight']) + (6.25 * float(session['height'])) - (5 * int(session['age'])) - 161
        elif session['weight_type'] == 'imperial':
            session['bmr'] = (4.536 * session['weight']) + (15.88 * float(session['height'])) - (5 * int(session['age'])) - 161
        else:
            log.debug(f'Error, {session["user"]} has entred weight_type as {session["weight_type"]} in calculate_cal')
            return jsonify(message='The weight_type entred was invalid'),401
    else:
        log.debug(f'Error, {session["user"]} has entred gender as {session["gender"]} in calculate_cal')
        return jsonify(message='The gender entred was invalid'),401
    
    return jsonify(bmr=session['bmr'],calculated_time=datetime.now()),200
