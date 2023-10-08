from . import app

app.add_url_rule('/signup', endpoint='signup', methods=['POST'])
app.add_url_rule('/verify/<random_key>', endpoint='verify', methods=['GET'])