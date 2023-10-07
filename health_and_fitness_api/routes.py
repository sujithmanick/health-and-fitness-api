from . import app, db
import re
from flask import request, session, jsonify
import string
import random
 

@app.endpoint('signup')
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

    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', session['mail-id']):
        return jsonify(message='Please enter valid email')
    
    """if not re.match(r'^[A-Za-z\d!@#$%^&*]{8,}$', session['password']):
        return jsonify(message='Your password doesn\'t match system requerments')"""
    
    if not re.match(r'[A-za-z]{2,}', session['first-name']):
        return jsonify(message='Your first-name doesn\'t match system requerments')
    
    if not session['age'] > 1 and session['age'] < 199:
        return jsonify(message='Your age doesn\'t match system requerments')
    
    if session['gender'] not in ['Male', 'Female']:
        return jsonify(message='Your gender doesn\'t match system requerments')


    users = db.users
    users.insert_one({"first-name": session['first-name'], "last-name": session['last-name'], "gender": session['gender'],"mail-id": session['mail-id'], "password" :session['password'], "age": session['age'],"phone-number": session['phone-number'], "active" : session['active'], "rand-key" : session['rand-key']})

    return jsonify(message="Congratulations! You are one step closer to unlocking\
                    the full potential of your account. We have sent a verification\
                    email to your registered email address. Please check your inbox and follow the\
                    instructions to verify your account. Once you have verified your account, you will\
                    be able to access all the features and benefits of our platform. Thank you for choosing us!")

