from flask import Blueprint
from flask import request
import boto3
from boto3.dynamodb.conditions import Key

post_routes_blueprint = Blueprint('post_routes', __name__)

dynamodb = boto3.resource('dynamodb',
                    aws_access_key_id="AKIA2G4DBYZWKGR4RZVC",
                    aws_secret_access_key="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")


@post_routes_blueprint.route('/newClass',methods = ['POST'])
def newClassProf():
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
    attend=0
    students=request.json["students"]
    print(students)
    response = table.query(
        KeyConditionExpression=Key('email').eq(email)
    )


    items = response['Items']
    print(items[0])
    Classes=items[0]["classes"]
    j={
        "class_name":class_name,
        "start_time":start_time,
        "end_time":end_time
    }
    Classes.append(j)
    
    response = table.update_item(
        Key={
            'email':email
        },
        UpdateExpression="set classes=:a",
        ExpressionAttributeValues={
            ':a': Classes
        },
        ReturnValues="UPDATED_NEW"
    
    )
    for i in students:
        response = table.query(
            KeyConditionExpression=Key('email').eq(i)
        )


        items = response['Items']
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
                'email':i
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
    print(request.json["uuid"])
    return request.json,200
