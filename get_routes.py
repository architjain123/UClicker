from flask import Blueprint

get_routes_blueprint = Blueprint('get_routes', __name__)

@get_routes_blueprint.route('/{uuid}')
def getStudent():
    
    return "This is an example app"