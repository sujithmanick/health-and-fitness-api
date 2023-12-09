import re
from flask import jsonify

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

def validate_signup(mail_id, password, first_name, age, gender):
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', mail_id):
        return jsonify(message='Please enter valid email')
    
    password_check = pswd_check(password)
    if password_check != True:
        return jsonify(message=password_check)
    
    if not re.match(r'[A-za-z]{2,}', first_name):
        return jsonify(message='Your first-name doesn\'t match system requerments')
    
    if not age > 1 and age < 199:
        return jsonify(message='Your age doesn\'t match system requerments')
    
    if gender not in ['Male', 'Female']:
        return jsonify(message='Your gender doesn\'t match system requerments')
    
    return True