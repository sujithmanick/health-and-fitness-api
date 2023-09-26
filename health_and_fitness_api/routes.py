from . import app
from flask import request

@app.endpoint('signup')
def user_signup():
    data = request.get_json()
    data['status'] = 'acceppted'
    return data