from . import app

app.add_url_rule('/signup', endpoint='signup', methods=['GET'])