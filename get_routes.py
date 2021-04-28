from flask import Blueprint

get_routes_blueprint = Blueprint('get_routes', __name__)
dynamodb = boto3.resource('dynamodb',
                    aws_access_key_id=os.getenv('KEY'),
                    aws_secret_access_key=os.environ.get('SECRET_KEY'))
@get_routes_blueprint.route('/user')
def getUser():
     email= request.json["email"]
     response = table.query(
            KeyConditionExpression=Key('email').eq(email)
    )
    items = response['Items']
    return items[0],200


@get_routes_blueprint.route('/allStudentsInClass')
def getAllStudents():
    email=request.json["email"]
    table = dynamodb.Table('UClickerAccounts')
    response = table.query(
            KeyConditionExpression=Key('email').eq(email)
    )
    items = response['Items']
    if(items[0]["admin"] == ""):
        r={"Error":"Not allowed to add classes"}
        return 403
    class_name=request.json["class"]
    start_time=request.json["start"]
    end_time=request.json["end"]
    
