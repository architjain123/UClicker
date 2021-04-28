from flask import Blueprint
from flask import request
import boto3
from boto3.dynamodb.conditions import Key
import os

post_routes_blueprint = Blueprint('post_routes', __name__)

dynamodb = boto3.resource('dynamodb',
                    aws_access_key_id=os.getenv('KEY'),
                    aws_secret_access_key=os.getenv('SECRET_KEY'))


@post_routes_blueprint.route('/new_class',methods = ['POST'])
def newClassProf():
    email=request.json["email"]
    table = dynamodb.Table('UClickerAccounts')
    class_name=request.json["class"]
    start_time=request.json["start"]
    end_time=request.json["end"]
    attend=0
    students=request.json["students"]
    print(students)
    response = table.query(
        KeyConditionExpression=Key('email').eq(email)&Key('admin').eq("true")
    )


    items = response['Items']
    if(items==[]):
            return {"error": "No person found"},404
    Classes=items[0]["classes"]
    j={
        "class_name":class_name,
        "start_time":start_time,
        "end_time":end_time
    }
    Classes.append(j)
    
    response = table.update_item(
        Key={
            'email':email,
            'admin':"true"
        },
        UpdateExpression="set classes=:a",
        ExpressionAttributeValues={
            ':a': Classes
        },
        ReturnValues="UPDATED_NEW"
    
    )
    for i in students:
        response = table.query(
            KeyConditionExpression=Key('email').eq(i)&Key('admin').eq("false")
        )


        items = response['Items']
        if(items==[]):
            return {"error": "No matching students found"},404
        print(items)
        Classes=items[0]["classes"]
        j={
        "class_name":class_name,
        "start_time":start_time,
        "end_time":end_time,
        "attend":attend
        }
        Classes.append(j)
        
        response = table.update_item(
            Key={
                'email':i,
                'admin':"false"
            },
            UpdateExpression="set classes=:a",
            ExpressionAttributeValues={
                ':a': Classes
            },
            ReturnValues="UPDATED_NEW"
        
        )
    return request.json,201


@post_routes_blueprint.route('/add_students',methods = ['POST'])
def add_students():
    email=request.json["email"]
    table = dynamodb.Table('UClickerAccounts')
    students=request.json["students"]
    start_time=request.json["start"]
    end_time=request.json["end"]
    class_name=request.json["class"]
    attend=0
    for i in students:
        response = table.query(
            KeyConditionExpression=Key('email').eq(i)&Key('admin').eq("false")

        )


        items = response['Items']
        if(items==[]):
            return {"error": "No person found"},404
        print(items[0])
        Classes=items[0]["classes"]
        j={
        "class_name":class_name,
        "start_time":start_time,
        "end_time":end_time,
        "attend":attend
        }
        Classes.append(j)
        
        response = table.update_item(
            Key={
                'email':i,
                'admin':"false"
            },
            UpdateExpression="set classes=:a",
            ExpressionAttributeValues={
                ':a': Classes
            },
            ReturnValues="UPDATED_NEW"
        
        )
    return request.json,200

@post_routes_blueprint.route('/attend',methods = ['POST'])
def attendClass():
    email=request.json["email"]
    class_name = request.json["class"]
    table = dynamodb.Table('UClickerAccounts')
    response = table.query(
            KeyConditionExpression=Key('email').eq(email)&Key('admin').eq('false')
    )
    items = response['Items']
    if(items==[]):
        return {"error": "No person found"},404
    classes=items[0]["classes"]
    for i in classes:
        if(i["class_name"]==class_name):
            i["attend"] = i["attend"]+1

    

    response = table.update_item(
            Key={
                'email':email,
                'admin':"false"
            },
            UpdateExpression="set classes=:a",
            ExpressionAttributeValues={
                ':a': classes
            },
            ReturnValues="UPDATED_NEW"
        
        )
    return request.json,200
