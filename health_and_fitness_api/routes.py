from . import app, db
import re
from flask import request, session, jsonify
from passlib.hash import sha256_crypt
import smtplib
from email.mime.text import MIMEText
import string
import random
 
def send_verification_email(name,email,link):
    try:
        smtp_ssl_host = app.config['SMTP_SSL_HOST']
        smtp_ssl_port = app.config['SMTP_SSL_PORT']
        sender_address = app.config['MAIL_SENDER_ADDRESS']
        sender_pass = app.config['MAIL_SENDER_PASSWORD']
        sender = app.config['MAIL_SENDER_ADDRESS']
        targets = email
        msg = MIMEText(f'Hi {name}\n\n Use this link to activate your\
                       health-and-fittness-account\n {link}')
        msg['Subject'] = 'Account verification | health-and-fittness-api'
        msg['From'] = sender
        msg['To'] = email

        server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
        server.login(sender_address,sender_pass )
        server.sendmail(sender,targets,msg.as_string())
        server.quit()
    except Exception as e:
        print(e) 

def pswd_check(passwd):
     
    SpecialSym =['$', '@', '#', '%']
    if len(passwd) < 8:
        return 'length should be at least 8'
         
    if not any(char.isdigit() for char in passwd):
        return 'Password should have at least one numeral'
         
    if not any(char.isupper() for char in passwd):
        return 'Password should have at least one uppercase letter'
         
    if not any(char.islower() for char in passwd):
        return 'Password should have at least one lowercase letter'
         
    if not any(char in SpecialSym for char in passwd):
        return 'Password should have at least one of the symbols $@#'
    
    return True

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

    if users_db.find_one({"mail-id": session['mail-id']}):
        return jsonify(message='You already have an account, Try logging in')

    users_db.insert_one({"first-name": session['first-name'], \
                      "last-name": session['last-name'], "gender": session['gender'],\
                        "mail-id": session['mail-id'], "password" : sha256_crypt.encrypt(session['password']),\
                         "age": session['age'],"phone-number": session['phone-number'], "active" : session['active'],\
                            "rand-key" : session['rand-key']})
    
    #sha256_crypt.verify("password", password)
    link = '{}/verify/{}'.format(app.config['APPLICATION_HOST'],session['rand-key'])
    send_verification_email(session['first-name'], session['mail-id'],link)
    
    return jsonify(message="Congratulations! You are one step closer to unlocking\
                    the full potential of your account. We have sent a verification\
                    email to your registered email address. Please check your inbox and follow the\
                    instructions to verify your account. Once you have verified your account, you will\
                    be able to access all the features and benefits of our platform. Thank you for choosing us!")

@app.endpoint('verify')
def user_verify(random_key):
    users_db = db.users

    user_data = users_db.find_one({"rand-key": random_key})
    if user_data:
        #Need to be worked for verify users
        return jsonify(message='You already have an account, Try logging in')

    return jsonify(message = random_key)