from flask import Blueprint
from flask import request
import boto3
from boto3.dynamodb.conditions import Key
from flask_cors import CORS, cross_origin
import hashlib
import re
from utils import KeyManager

login_routes_blueprint = Blueprint('login_routes', __name__)

dynamodb = boto3.resource('dynamodb', region_name='us-west-1',
                    aws_access_key_id=KeyManager.getInstance().KEY,
                    aws_secret_access_key=KeyManager.getInstance().SECRETKEY)


@login_routes_blueprint.route('/signup',methods = ['POST'])
def signup():
    regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'

    print(request.json)
    name = request.json["name"]
    email= request.json["email"]
    if(re.search(regex, email)):
        print("Valid Email")
    else:
        r = {"error": "invalid email id"}
        return r,400

    passwordHashed= request.json["password"]
    uuid = (email+passwordHashed)
    result_uuid = hashlib.md5(uuid.encode())
    table = dynamodb.Table('UClickerAccounts')

    try:
        response = table.query(
                KeyConditionExpression=Key('email').eq(email)
        )
    except Error as e:
        print(e)
        r = {"error":"error occured in querying table"}
        return r,500
    
    items = response['Items']
    if len(items) > 0:
        r = {"error":"account with this email id already exists"}
        return r,403
    
    try:
        table.put_item(
                Item={
        'uuid': result_uuid.hexdigest(),
        'name': name,
        'email': email,
        'password': passwordHashed,
        "admin": "false",
        "classes": []
            }
        )
    except Error as e:
        print(e)
        r = {"error": "error occurred in adding user to db"}
        return r,500
    
    return request.json,201

@login_routes_blueprint.route('/admin_signup',methods = ['POST'])
def admin_signup():
    regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'

    print(request.json)
    name = request.json["name"]
    email= request.json["email"]
    if(re.search(regex, email)):
        print("Valid Email")
    else:
        r = {"error": "invalid email id"}
        return r,400

    passwordHashed= request.json["password"]
    uuid = (email+passwordHashed)
    result_uuid = hashlib.md5(uuid.encode())
    table = dynamodb.Table('UClickerAccounts')
    
    try:
        response = table.query(
                KeyConditionExpression=Key('email').eq(email)
        )
    except Error as e:
        print(e)
        r = {"error":"error occured in querying table"}
        return r,500
    
    items = response['Items']
    if len(items) > 0:
        r = {"error":"account with this email id already exists"}
        return r,403

    try:
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
    except Error as e:
        print(e)
        r = {"error": "error occurred in adding user to db"}
        return r,500

    # table = dynamodb.Table('UClicker')
    
    # table.put_item(
    #         Item={
    # 'uuid': result_uuid.hexdigest()
    #         }
    # )
    return request.json,201
   

@login_routes_blueprint.route('/login',methods = ['POST'])
def login():
    email=request.json["email"]
    passwordHashed=request.json["password"]
    table = dynamodb.Table('UClickerAccounts')
    try:
        response = table.query(
                KeyConditionExpression=Key('email').eq(email)
        )
    except Error as e:
        print(e)
        r = {"error":"error occured in querying table"}
        return r,500
    
    items = response['Items']
    print(items)

    if len(items) > 0:
        if passwordHashed == items[0]['password']:
            email = items[0]['email']
            admin = items[0]['admin']
            name = items[0]['name']
            classes = items[0]['classes']
            r= {"status": "Login sucess","email":email,"admin":admin, "classes":[{"cname": "cs218"}, {"cname": "cs218"}], "name": name}
            return r,200
        r = {"error": "wrong credentials"}
        return r,401
    r = {"error": "user not registered"}
    return r,401
