from flask import Blueprint
from flask import request
import simplejson as json
import boto3
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr
import os

get_routes_blueprint = Blueprint('get_routes', __name__)
dynamodb = boto3.resource('dynamodb',
                    aws_access_key_id=os.getenv('KEY'),
                    aws_secret_access_key=os.environ.get('SECRET_KEY'))
@get_routes_blueprint.route('/user',methods = ['POST'])
def getUser():
    email= request.json["email"]
    table = dynamodb.Table('UClickerAccounts')

    response = table.query(
            KeyConditionExpression=Key('email').eq(email)
    )

    if(response['Items'] == []):
        r={"error":"not found"}
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
    start_time=request.json["start"]
    end_time=request.json["end"]

    response = table.scan()
 
    all_elements = response["Items"]
    return_elements = []
    for i in all_elements:
        c = i["classes"][0]
        if(i['admin']=="false" and c['start_time']==start_time and c['end_time']==end_time and c['class_name']==class_name):
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
    if(return_elements==[]):
        return {"error":"Nothing found with that class"},404
    return json.dumps(return_elements)

    


    
