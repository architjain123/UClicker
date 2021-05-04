# UClicker
Cloud based attendance system
At the moment everything is a POST method as I cant figure out why GET wont work. Will find a work around.

Signup POST request
 

    Sample json body with request
    http://localhost:5000/account/signup

    {
    "name":"evan chopra",
    "email":"e@gmail.com",
    "password":"ksdjflkjaf"
    }



Signup admin POST request

    Sample json body with request
    http://localhost:5000/account/admin_signup
    {
    "name":"Kong Li",
    "email":"k@gmail.com",
    "password":"asdasdsa"
    }

    return:
    {
    "email": "k@gmail.com", 
    "name": "Kong Li", 
    "password": "asdasdsa"
    }
    201



Login POST Request

    Sample json body with request
    http://localhost:5000/account/login
    {
    "email":"e@gmail.com",
    "password":"ksdjflkjaf"
    }

    return:
        {
        "admin": "false", 
        "email": "e@gmail.com", 
        "status": "Login sucess"
        }
    200

Deleting a class as an admin request POST
    http://localhost:8080/add/delete_class
    {
    "email":"k@gmail.com",
    "class":"CS222",
    "students":["e@gmail.com","d@gmail.com","a@gmail.com"]

    }
    NOTE: You must include the emails of students in the class as well in this request. 

    return an array of new classes after the deletion!





starting a class as an admin request POST
    http://localhost:8080/add/start_class
    {
        "email":"k@gmail.com",
        "class_name":"Biology"
    }

    Will respond with teachers classes

starting a class as an admin request POST (This response also flips isAttending to false for students)
    http://localhost:8080/add/end_class
    {
        "email":"k@gmail.com",
        "class_name":"Biology"
    }

    Will respond with teachers classes






Adding new classes as an Admin request POST request (If student emails that do not exisit are given it will still make class just it will be empty)

    http://localhost:5000/add/new_class
    {
        "email":"k@gmail.com",
        "class":"Biology",
        "start":"08:30:00",
        "end":"10:00:00" ,
        "students":["e@gmail.com"],
        "days": ["Monday","Wednesday"]
    }

    response:
    {
        "class": "Biology", 
        "email": "k@gmail.com", 
        "end": "10:00:00", 
        "start": "08:30:00", 
        "students": [
            "e@gmail.com"
        ]
    }
    201



Adding students to an exisiting class as Admin 
    http://localhost:5000/add/add_students
    {
        "email":"k@gmail.com",
        "class":"Biology",
        "start":"08:30:00",
        "end":"10:00:00" ,
        "students":["d@gmail.com"],
        "days": ["Monday","Wednesday"]
    }

    response:
    {
        "class": "Biology", 
        "email": "k@gmail.com", 
        "end": "10:00:00", 
        "start": "08:30:00", 
        "students": [
            "d@gmail.com"
        ]
    }
    200


Adding attendence to a students record (As of now will always return 200 but wont increment attendence unless class exists)
    http://localhost:5000/add/attend
     {
        "email":"d@gmail.com", 
        "class":"Biology"
    }
     
   This is what d@gmail.com in db looks like now
    {
        "admin": "false",
        "classes": [
            {
                "attend": 1,
                "class_name": "Biology",
                "end_time": "10:00:00",
                "start_time": "08:30:00"
            }
        ],
        "email": "d@gmail.com",
        "name": "diego",
        "password": "ksdfjhlksjaf",
        "uuid": "a4010f02447892cae1b18c705d59d74a"
    }


Adding total attendence to students record
    http://localhost:8080/add/add_to_total
    {
        "email":"e@gmail.com",
        "class_name":"Spanish"
    }




Gets a user POST method
    http://localhost:5000/get/user
    {
            "email": "k@gmail.com"
    }
    {"uuid": "3baf7de1e1a73ef76103cd19c9ffdd7a", "password": "asdasdsa", "email": "k@gmail.com", "admin": "true", "name": "Kong Li", "classes": [{"end_time": "10:00:00", "class_name": "Biology", "start_time": "08:30:00"}]}


Get all students in a given class POST request

    http://localhost:5000/get/all_students_class
     {
       "class": "Biology", 
        "email": "k@gmail.com", 
        "end": "10:00:00", 
        "start": "08:30:00"
    }

    returns a list of all users in that class (This return is subject to change. This method is inefficient at the moment)

    [{"uuid": "fea04fc70e529ef42a70e5d1fdcb1ecb", "password": "ksdjflkjaf", "email": "e@gmail.com", "admin": "false", "name": "evan chopra", "classes": [{"end_time": "10:00:00", "start_time": "08:30:00", "attend": 0, "class_name": "Biology"}]}]


Gets all students GET method
    http://localhost:5000/get/all_students

    no body needed

    [{"uuid": "a4010f02447892cae1b18c705d59d74a", "password": "ksdfjhlksjaf", "email": "d@gmail.com", "admin": "false", "name": "diego", "classes": [{"end_time": "10:00:00", "start_time": "08:20:00", "attend": 1, "class_name": "Biology"}]}, {"uuid": "fea04fc70e529ef42a70e5d1fdcb1ecb", "password": "ksdjflkjaf", "email": "e@gmail.com", "admin": "false", "name": "evan chopra", "classes": [{"end_time": "10:00:00", "start_time": "08:30:00", "attend": 0, "class_name": "Biology"}]}]