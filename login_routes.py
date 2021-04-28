from flask import Blueprint
from flask import request
import boto3
from boto3.dynamodb.conditions import Key
import hashlib
login_routes_blueprint = Blueprint('login_routes', __name__)

dynamodb = boto3.resource('dynamodb',
                    aws_access_key_id="AKIA2G4DBYZWKGR4RZVC",
                    aws_secret_access_key="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")


@login_routes_blueprint.route('/signup',methods = ['POST'])
def signup():
    print(request.json)
    name = request.json["name"]
    email= request.json["email"]
    passwordHashed= request.json["password"]
    uuid = (email+passwordHashed)
    result_uuid = hashlib.md5(uuid.encode())
    table = dynamodb.Table('UClickerAccounts')
    
    table.put_item(
            Item={
    'uuid': result_uuid.hexdigest(),
    'name': name,
    'email': email,
    'password': passwordHashed,
    'classes' : []
        }
    )

    table = dynamodb.Table('UClicker')
    
    table.put_item(
            Item={
    'uuid': result_uuid.hexdigest()
            }
    )
    return request.json,200

@login_routes_blueprint.route('/admin_signup',methods = ['POST'])
def admin_signup():
    print(request.json)
    name = request.json["name"]
    email= request.json["email"]
    passwordHashed= request.json["password"]
    uuid = (email+passwordHashed)
    result_uuid = hashlib.md5(uuid.encode())
    table = dynamodb.Table('UClickerAccounts')
    
    table.put_item(
            Item={
    'uuid': result_uuid.hexdigest(),
    'name': name,
    'email': email,
    'password': passwordHashed,
    "admin": "true" ,
    "classes": []
        }
    )

    # table = dynamodb.Table('UClicker')
    
    # table.put_item(
    #         Item={
    # 'uuid': result_uuid.hexdigest()
    #         }
    # )
    return request.json,200
   
    




@login_routes_blueprint.route('/login',methods = ['POST'])
def login():
    email=request.json["email"]
    passwordHashed=request.json["password"]
    table = dynamodb.Table('UClickerAccounts')
    response = table.query(
            KeyConditionExpression=Key('email').eq(email)
    )
    items = response['Items']
    print(items)

    
    if passwordHashed == items[0]['password']:
        email = items[0]['email']
        admin =items[0]['admin']
        r= {"status": "Login sucess","email":email,"admin":admin}
        return r,200
    r = {"status": "wrong credentials"}
    return r,403
