from . import app
from health_and_fitness_api.routes import user_signup, user_verify, user_login, get_diet_plans

app.add_url_rule('/signup', methods=['POST'], view_func=user_signup)
app.add_url_rule('/verify/<random_key>', methods=['GET'], view_func=user_verify)
app.add_url_rule('/login', methods=['POST'], view_func=user_login)
app.add_url_rule('/dietplans', methods=['GET'], view_func=get_diet_plans)