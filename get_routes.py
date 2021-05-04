from flask import Blueprint
from flask import request
from flask_cors import CORS, cross_origin
import simplejson as json
import boto3
from utils import KeyManager
from boto3.dynamodb.conditions import Key

get_routes_blueprint = Blueprint('get_routes', __name__)
dynamodb = boto3.resource('dynamodb', region_name='us-west-1',
                    aws_access_key_id=KeyManager.getInstance().KEY,
                    aws_secret_access_key=KeyManager.getInstance().SECRETKEY)

@get_routes_blueprint.route('/user',methods = ['POST'])
def getUser():
    email= request.json["email"]
    table = dynamodb.Table('UClickerAccounts')

    response = table.query(
            KeyConditionExpression=Key('email').eq(email)
    )

    if(response['Items'] == []):
        r={"error":"user not found"}
        return r,404
    items = response['Items']
    return json.dumps(items[0]),200

@get_routes_blueprint.route('/all_students_class',methods = ['POST'])
def get_all_students_class():
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
    
    response = table.scan()
 
    all_elements = response["Items"]
    return_elements = []
    for i in all_elements:
        if(i["admin"]=='false'):
            c = i["classes"]
            for ind in c:
                if(i['admin']=="false" and ind['class_name']==class_name):
                    return_elements.append(i)
    if(return_elements==[]):
        return {"error":"Nothing found with that class"},404
    return json.dumps(return_elements)

@get_routes_blueprint.route('/all_students',methods = ['GET'])
def get_all_students():
    
    table = dynamodb.Table('UClickerAccounts')
    response = table.scan()
    all_elements = response["Items"]
    return_elements = []
    for i in all_elements:
        if(i['admin']=="false" ):
            return_elements.append(i)
    return json.dumps(return_elements)



@get_routes_blueprint.route('/health_check',methods = ['GET'])
def health():
    return {"Health_check": "Im all good for now"},200