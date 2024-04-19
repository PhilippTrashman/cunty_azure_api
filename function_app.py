import azure.functions as func
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
import json
import logging
import uuid


import sys
import os
from backend import models

engine = create_engine(os.environ["DATABASE_URL"])
Session = sessionmaker(bind=engine)
Base = models.Base

app = func.FunctionApp()
backend = None

TOKEN = os.environ["TOKEN"]
print(f"TOKEN: {TOKEN}")

@app.route('hello', methods=['GET'], auth_level=func.AuthLevel.ANONYMOUS)
def get_hello_world(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(f"Hello World")

@app.route('login', methods=['POST'], auth_level=func.AuthLevel.ANONYMOUS)
def post_login(req: func.HttpRequest) -> func.HttpResponse:
    session = Session()
    data = req.get_json()
    username = data.get('username')
    password = data.get('password')
    user = session.query(models.Account).filter(models.Account.username == username).first()
    if not user:
        user = session.query(models.Account).filter(models.Account.email == username).first()
    if user and user.password == password:
        data = user.serialize()
        session.close()
        return func.HttpResponse(json.dumps(data))
    return func.HttpResponse("Unauthorized", status_code=401)

@app.route('health', methods=['GET'], auth_level=func.AuthLevel.ANONYMOUS)
def get_health(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse("OK")

@app.route('user', methods=['GET'], auth_level=func.AuthLevel.ANONYMOUS)
def get_users(req: func.HttpRequest) -> func.HttpResponse:
    session = Session()
    users = session.query(models.Account).all()
    result = json.dumps([user.serialize() for user in users])
    session.close()
    return func.HttpResponse(result)

@app.route('user', methods=['POST'], auth_level=func.AuthLevel.ANONYMOUS)
def post_user(req: func.HttpRequest) -> func.HttpResponse:
    session = Session()
    data = req.get_json()
    birthday = data.get('birthday', None)
    if birthday:
        data['birthday'] = datetime.strptime(birthday, "%Y-%m-%d").date()
    user = models.Account(
        id = uuid.uuid4(),
        email=data.get('email'),
        password=data.get('password'),
        name=data.get('name'),
        last_name=data.get('last_name'),
        username=data.get('username'),
        birthday=birthday,
    )
    session.add(user)
    session.commit()
    user = session.query(models.Account).filter(models.Account.username == data.get('username')).first()
    result = json.dumps(user.serialize())
    session.close()
    return func.HttpResponse(result)
    
@app.route('user/{username}', methods=['GET'], auth_level=func.AuthLevel.ANONYMOUS)
def get_user(req: func.HttpRequest) -> func.HttpResponse:
    session = Session()
    username = req.route_params.get('username')
    user = session.query(models.Account).filter(models.Account.username == username).first()
    result = json.dumps(user.serialize())
    session.close()
    return func.HttpResponse(result)  

@app.route('user/{username}', methods=['PUT'], auth_level=func.AuthLevel.ANONYMOUS)
def put_user(req: func.HttpRequest) -> func.HttpResponse:
    session = Session()
    username = req.route_params.get('username')
    user = session.query(models.Account).filter(models.Account.username == username).first()
    data = req.get_json()
    # print(data)
    user.email = data.get('email') if data.get('email') else user.email
    user.password = data.get('password') if data.get('password') else user.password
    user.name = data.get('name') if data.get('name') else user.name
    user.last_name = data.get('last_name') if data.get('last_name') else user.last_name
    user.username = data.get('username') if data.get('username') else user.username
    user.birthday = datetime.strptime(data.get('birthday'), "%Y-%m-%d").date() if data.get('birthday') else user.birthday

    # for key, value in data.items():
    #     setattr(user, key, value)
    # session.commit()
    session.close()
    return func.HttpResponse(json.dumps(data))

@app.route('user/{username}', methods=['DELETE'], auth_level=func.AuthLevel.ANONYMOUS)
def delete_user(req: func.HttpRequest) -> func.HttpResponse:
    session = Session()
    username = req.route_params.get('username')
    user = session.query(models.Account).filter(models.Account.username == username).first()
    session.delete(user)
    session.commit()
    session.close()
    return func.HttpResponse("Deleted")



# Student Calls



@app.route('user/{username}/student', methods=['GET'], auth_level=func.AuthLevel.ANONYMOUS)
def get_student(req: func.HttpRequest) -> func.HttpResponse:
    session = Session()
    username = req.route_params.get('username')
    user = session.query(models.Account).filter(models.Account.username == username).first()
    student = session.query(models.Student).filter(models.Student.account_id == user.id).first()
    if not student:
        return func.HttpResponse("Not Found", status_code=404)
    result = json.dumps(student.serialize())
    session.close()
    return func.HttpResponse(result)

@app.route('user/{username}/student', methods=['POST'], auth_level=func.AuthLevel.ANONYMOUS)
def post_student(req: func.HttpRequest) -> func.HttpResponse:
    session = Session()
    username = req.route_params.get('username')
    user = session.query(models.Account).filter(models.Account.username == username).first()
    data = req.get_json()
    student = models.Student(
        account_id = user.id,
        school_class_id = data.get('school_class_id', None)
    )
    session.add(student)
    session.commit()
    student = session.query(models.Student).filter(models.Student.account_id == user.id).first()
    result = json.dumps(student.serialize())
    session.close()
    return func.HttpResponse(result)


@app.route('user/{username}/student', methods=['PUT'], auth_level=func.AuthLevel.ANONYMOUS)
def put_student(req: func.HttpRequest) -> func.HttpResponse:
    session = Session()
    username = req.route_params.get('username')
    user = session.query(models.Account).filter(models.Account.username == username).first()
    student = session.query(models.Student).filter(models.Student.account_id == user.id).first()
    if not student:
        return func.HttpResponse("Not Found", status_code=404)
    data = req.get_json()
    student.school_class_id = data.get('school_class_id', student.school_class_id)
    result = json.dumps(student.serialize())
    session.commit()
    session.close()
    return func.HttpResponse(result)

@app.route('user/{username}/student', methods=['DELETE'], auth_level=func.AuthLevel.ANONYMOUS)
def delete_student(req: func.HttpRequest) -> func.HttpResponse:
    session = Session()
    username = req.route_params.get('username')
    user = session.query(models.Account).filter(models.Account.username == username).first()
    student = session.query(models.Student).filter(models.Student.account_id == user.id).first()
    session.delete(student)
    session.commit()
    session.close()
    return func.HttpResponse(f"Student with id {student.id} deleted")



# Teacher Calls



@app.route('user/{username}/teacher', methods=['GET'], auth_level=func.AuthLevel.ANONYMOUS)
def get_teacher(req: func.HttpRequest) -> func.HttpResponse:
    session = Session()
    username = req.route_params.get('username')
    user = session.query(models.Account).filter(models.Account.username == username).first()
    teacher = session.query(models.Teacher).filter(models.Teacher.account_id == user.id).first()
    if not teacher:
        return func.HttpResponse("Not Found", status_code=404)
    result = json.dumps(teacher.serialize())
    session.close()
    return func.HttpResponse(result)

@app.route('user/{username}/teacher', methods=['POST'], auth_level=func.AuthLevel.ANONYMOUS)
def post_teacher(req: func.HttpRequest) -> func.HttpResponse:
    session = Session()
    username = req.route_params.get('username')
    user = session.query(models.Account).filter(models.Account.username == username).first()
    data = req.get_json()
    teacher = models.Teacher(
        account_id = user.id,
        abbreviation = data.get('abbreviation'),
    )
    session.add(teacher)
    session.commit()
    teacher = session.query(models.Teacher).filter(models.Teacher.account_id == user.id).first()
    result = json.dumps(teacher.serialize())
    session.close()
    return func.HttpResponse(result)

@app.route('user/{username}/teacher', methods=['PUT'], auth_level=func.AuthLevel.ANONYMOUS)
def put_teacher(req: func.HttpRequest) -> func.HttpResponse:
    session = Session()
    username = req.route_params.get('username')
    user = session.query(models.Account).filter(models.Account.username == username).first()
    teacher = session.query(models.Teacher).filter(models.Teacher.account_id == user.id).first()
    if not teacher:
        return func.HttpResponse("Not Found", status_code=404)
    data = req.get_json()
    teacher.abbreviation = data.get('abbreviation', teacher.abbreviation)
    result = json.dumps(teacher.serialize())
    session.commit()
    session.close()
    return func.HttpResponse(result)

@app.route('user/{username}/teacher', methods=['DELETE'], auth_level=func.AuthLevel.ANONYMOUS)
def delete_teacher(req: func.HttpRequest) -> func.HttpResponse:
    session = Session()
    username = req.route_params.get('username')
    user = session.query(models.Account).filter(models.Account.username == username).first()
    teacher = session.query(models.Teacher).filter(models.Teacher.account_id == user.id).first()
    session.delete(teacher)
    session.commit()
    session.close()
    return func.HttpResponse(f"Teacher with id {teacher.id} deleted")




# Super User calls




@app.route('user/{username}/su', methods=['GET'], auth_level=func.AuthLevel.ANONYMOUS)
def get_su(req: func.HttpRequest) -> func.HttpResponse:
    session = Session()
    username = req.route_params.get('username')
    user = session.query(models.Account).filter(models.Account.username == username).first()
    su = session.query(models.SuperUser).filter(models.SuperUser.account_id == user.id).first()
    if not su:
        return func.HttpResponse("Not Found", status_code=404)
    result = json.dumps(su.serialize())
    session.close()
    return func.HttpResponse(result)

@app.route('user/{username}/su', methods=['POST'], auth_level=func.AuthLevel.ANONYMOUS)
def post_su(req: func.HttpRequest) -> func.HttpResponse:
    session = Session()
    username = req.route_params.get('username')
    user = session.query(models.Account).filter(models.Account.username == username).first()
    data = req.get_json()
    su = models.SuperUser(
        account_id = user.id,
        admin_rights = data.get('admin_rights', False),
        change_subject_status = data.get('change_subject_status', False),
        manage_users = data.get('manage_users', False),
        manage_school = data.get('manage_school', False),
    )
    session.add(su)
    session.commit()
    su = session.query(models.SuperUser).filter(models.SuperUser.account_id == user.id).first()
    result = json.dumps(su.serialize())
    session.close()
    return func.HttpResponse(result)

@app.route('user/{username}/su', methods=['PUT'], auth_level=func.AuthLevel.ANONYMOUS)


