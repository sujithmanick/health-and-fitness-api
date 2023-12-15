from waitress import serve

from health_and_fitness_api import create_app
#from health_and_fitness_api import routes, urls

if __name__ == '__main__':
    #create_app().run()
    serve(create_app(), host='127.0.0.1', port=8080)

#Command to run
#FLASK_APP=health_and_fitness_api flask run