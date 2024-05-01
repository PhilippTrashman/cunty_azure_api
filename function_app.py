import azure.functions as func
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.errors import *
from backend.manifesto import get_manifesto
import datetime
import json
import logging
import uuid


import sys
import os
from backend import models
from backend.adapter_collection import AdapterCollection

engine = create_engine(os.environ["DATABASE_URL"])
Session = sessionmaker(bind=engine)
adapters = AdapterCollection(Session)
Base = models.Base

app = func.FunctionApp()
backend = None

TOKEN = os.environ["TOKEN"]
print(f"TOKEN: {TOKEN}")

@app.route('fortnite', methods=['GET'], auth_level=func.AuthLevel.ANONYMOUS)
def get_fortnite(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(get_manifesto(), status_code=226)

@app.route('hello', methods=['GET'], auth_level=func.AuthLevel.ANONYMOUS)
def get_hello_world(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(f"Hello World")

@app.route('login', methods=['POST'], auth_level=func.AuthLevel.ANONYMOUS)
def post_login(req: func.HttpRequest) -> func.HttpResponse:
    try:
        session = Session()
        data = req.get_json()
        username = data.get('username')
        password = data.get('password')
        user = adapters.account_adapter.get_account_by_username_or_email(username)
        if user and user.password == password:
            data = user.serialize()
            session.close()
            return func.HttpResponse(json.dumps(data))
    
        return func.HttpResponse("Unauthorized", status_code=401)
    except UserNotFound as e:
        return func.HttpResponse(str(e), status_code=e.status_code)
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)

@app.route('health', methods=['GET'], auth_level=func.AuthLevel.ANONYMOUS)
def get_health(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse("OK")

@app.route('users', methods=['GET'], auth_level=func.AuthLevel.ANONYMOUS)
def get_users(req: func.HttpRequest) -> func.HttpResponse:
    result = adapters.account_adapter.get_accounts()
    return func.HttpResponse(json.dumps(result))  

@app.route('users', methods=['POST'], auth_level=func.AuthLevel.ANONYMOUS)
def post_user(req: func.HttpRequest) -> func.HttpResponse:
    result = adapters.account_adapter.create_account(req.get_json())
    return func.HttpResponse(json.dumps(result))  
    
@app.route('users/{username}', methods=['GET'], auth_level=func.AuthLevel.ANONYMOUS)
def get_user(req: func.HttpRequest) -> func.HttpResponse:
    result = adapters.account_adapter.get_account_by_username_or_email(req.route_params.get('username'))
    return func.HttpResponse(json.dumps(result))  

@app.route('users/{username}', methods=['PUT'], auth_level=func.AuthLevel.ANONYMOUS)
def put_user(req: func.HttpRequest) -> func.HttpResponse:
    result = adapters.account_adapter.update_account(req.get_json())
    return func.HttpResponse(json.dumps(result))  

@app.route('users/{username}', methods=['DELETE'], auth_level=func.AuthLevel.ANONYMOUS)
def delete_user(req: func.HttpRequest) -> func.HttpResponse:
    result = adapters.account_adapter.delete_account(req.route_params.get('username'))
    return func.HttpResponse(json.dumps(result))  

@app.route('users/{username}/student', methods=['GET'], auth_level=func.AuthLevel.ANONYMOUS)
def get_student(req: func.HttpRequest) -> func.HttpResponse:
    try:
        session = Session()
        username = req.route_params.get('username')
        user = session.query(models.Account).filter(models.Account.username == username).first()
        if user is None:
            raise ValueError("User not found")
        student = user.student
        if not student:
            raise
        result = json.dumps(student.serialize())
        session.close()
        return func.HttpResponse(result)
    except Exception as e:
        return func.HttpResponse(str(e))


@app.route('users/{username}/teacher', methods=['GET'], auth_level=func.AuthLevel.ANONYMOUS)
def get_teacher(req: func.HttpRequest) -> func.HttpResponse:
    session = Session()
    username = req.route_params.get('username')
    user = session.query(models.Account).filter(models.Account.username == username).first()
    teacher = user.teacher
    if not teacher:
        return func.HttpResponse("Not Found", status_code=404)
    result = json.dumps(teacher.serialize())
    session.close()
    return func.HttpResponse(result)

@app.route('users/{username}/su', methods=['GET'], auth_level=func.AuthLevel.ANONYMOUS)
def get_su(req: func.HttpRequest) -> func.HttpResponse:
    session = Session()
    username = req.route_params.get('username')
    user = session.query(models.Account).filter(models.Account.username == username).first()
    su = user.su
    if not su:
        return func.HttpResponse("Not Found", status_code=404)
    result = json.dumps(su.serialize())
    session.close()

@app.route('users/{username}/parent', methods=['GET'], auth_level=func.AuthLevel.ANONYMOUS)
def get_parent(req: func.HttpRequest) -> func.HttpResponse:
    session = Session()
    username = req.route_params.get('username')
    user = session.query(models.Account).filter(models.Account.username == username).first()
    parent = user.parent
    if not parent:
        return func.HttpResponse("Not Found", status_code=404)
    result = json.dumps(parent.serialize())
    session.close()
    return func.HttpResponse(result)

@app.route('users/{username}/abscence', methods=['GET'], auth_level=func.AuthLevel.ANONYMOUS)
def get_abscences(req: func.HttpRequest) -> func.HttpResponse:
    session = Session()
    username = req.route_params.get('username')
    user = session.query(models.Account).filter(models.Account.username == username).first()
    if not user:
        return func.HttpResponse("Not Found", status_code=404)
    session.close()
    result = adapters.absence_adapter.get_abscence_by_user(user.id)
    return func.HttpResponse(result)