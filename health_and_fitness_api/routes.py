from . import app, db
import re
from flask import request, session, jsonify
from passlib.hash import sha256_crypt
import string
import random
from datetime import datetime
 
from health_and_fitness_api.util.validate import pswd_check
from health_and_fitness_api.util.messenger import send_verification_email



@app.endpoint('signup')
def user_signup():
    users_db = db.users

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
    session['acc-creation-date'] = str(datetime.now())
    session['acc-verification-date'] = ''

    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', session['mail-id']):
        return jsonify(message='Please enter valid email')
    
    password_check = pswd_check(session['password'])
    if password_check != True:
        return jsonify(message=password_check)
    
    if not re.match(r'[A-za-z]{2,}', session['first-name']):
        return jsonify(message='Your first-name doesn\'t match system requerments')
    
    if not session['age'] > 1 and session['age'] < 199:
        return jsonify(message='Your age doesn\'t match system requerments')
    
    if session['gender'] not in ['Male', 'Female']:
        return jsonify(message='Your gender doesn\'t match system requerments')

    if users_db.find_one({"mail-id": session['mail-id'], "rand-key" : session['rand-key']}):
        return jsonify(message='You already have an account, Try logging in')

    users_db.insert_one({"first_name": session['first-name'], \
                      "last_name": session['last-name'], "gender": session['gender'],\
                        "mail_id": session['mail-id'], "password" : sha256_crypt.encrypt(session['password']),\
                         "age": session['age'],"phone_number": session['phone-number'], "active" : session['active'],\
                            "rand_key" : session['rand-key'], "acc_creation_date" : session["acc-creation-date"],\
                                "acc_verification_date" : session['acc-verification-date']})
    
    #sha256_crypt.verify("password", password)
    link = '{}/verify/{}'.format(app.config['APPLICATION_HOST'],session['rand-key'])
    send_verification_email(app, session['first-name'], session['mail-id'],link)
    
    return jsonify(message="Congratulations! You are one step closer to unlocking\
                    the full potential of your account. We have sent a verification\
                    email to your registered email address. Please check your inbox and follow the\
                    instructions to verify your account. Once you have verified your account, you will\
                    be able to access all the features and benefits of our platform. Thank you for choosing us!")

@app.endpoint('verify')
def user_verify(random_key):
    users_db = db.users

    user_data = users_db.find_one({"rand_key": random_key})
    if user_data:
        pass
        #Need to be worked for verify users

        return jsonify(message='You account has been activated')

    return jsonify(message = random_key)