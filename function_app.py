import azure.functions as func
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.errors import *
from backend.manifesto import get_manifesto
from datetime import date
import json

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

def verify_token(req: func.HttpRequest) -> bool:
    token = req.headers.get('Authorization')
    if not token:
        return False
    return token == f"Bearer {TOKEN}"

@app.route('fortnite', methods=['GET'], auth_level=func.AuthLevel.ANONYMOUS)
def get_fortnite(req: func.HttpRequest) -> func.HttpResponse:
    try:
        if not verify_token(req):
            return func.HttpResponse("Unauthorized", status_code=401)
        return func.HttpResponse(get_manifesto(), status_code=226)
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)

@app.route('hello', methods=['GET'], auth_level=func.AuthLevel.ANONYMOUS)
def get_hello_world(req: func.HttpRequest) -> func.HttpResponse:
    if not verify_token(req):
        return func.HttpResponse("Unauthorized", status_code=401)
    return func.HttpResponse(f"Hello World!")

@app.route('login', methods=['POST'], auth_level=func.AuthLevel.ANONYMOUS)
def post_login(req: func.HttpRequest) -> func.HttpResponse:
    if not verify_token(req):
        return func.HttpResponse("Unauthorized", status_code=401)
    try:
        session = Session()
        data = req.get_json()
        username = data.get('username')
        password = data.get('password')
        user = adapters.account_adapter.get_account_by_username_or_email(username)
        if user and adapters.account_adapter.check_account_password(username, password):
            session.close()
            return func.HttpResponse(json.dumps(user))
    
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
    try:
        if not verify_token(req):
            return func.HttpResponse("Unauthorized", status_code=401)
        result = adapters.account_adapter.get_accounts()
        return func.HttpResponse(json.dumps(result))  
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)

@app.route('users', methods=['POST'], auth_level=func.AuthLevel.ANONYMOUS)
def post_user(req: func.HttpRequest) -> func.HttpResponse:
    try:
        if not verify_token(req):
            return func.HttpResponse("Unauthorized", status_code=401)
        result = adapters.account_adapter.create_account(req.get_json())
        return func.HttpResponse(json.dumps(result))  
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)
    
@app.route('users/{username}', methods=['GET'], auth_level=func.AuthLevel.ANONYMOUS)
def get_user(req: func.HttpRequest) -> func.HttpResponse:
    try:
        if not verify_token(req):
            return func.HttpResponse("Unauthorized", status_code=401)
        result = adapters.account_adapter.get_account_by_username_or_email(req.route_params.get('username'))
        return func.HttpResponse(json.dumps(result))  
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)

@app.route('users/{username}', methods=['PUT'], auth_level=func.AuthLevel.ANONYMOUS)
def put_user(req: func.HttpRequest) -> func.HttpResponse:
    try:
        if not verify_token(req):
            return func.HttpResponse("Unauthorized", status_code=401)
        user = adapters.account_adapter.get_account_by_username_or_email(req.route_params.get('username'))
        if not user:
            return func.HttpResponse("Not Found", status_code=404)
        result = adapters.account_adapter.update_account(req.get_json(), user['id'])
        return func.HttpResponse(json.dumps(result))  
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)

@app.route('users/{username}', methods=['DELETE'], auth_level=func.AuthLevel.ANONYMOUS)
def delete_user(req: func.HttpRequest) -> func.HttpResponse:
    try:
        if not verify_token(req):
            return func.HttpResponse("Unauthorized", status_code=401)
        user = adapters.account_adapter.get_account_by_username_or_email(req.route_params.get('username'))
        if not user:
            return func.HttpResponse("Not Found", status_code=404)
        adapters.account_adapter.delete_account(user['id'])
        return func.HttpResponse("OK", status_code=200)  
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)
    
@app.route('users/{username}/contact', methods=['GET'], auth_level=func.AuthLevel.ANONYMOUS)
def get_user_contact(req: func.HttpRequest) -> func.HttpResponse:
    try:
        if not verify_token(req):
            return func.HttpResponse("Unauthorized", status_code=401)
        session = Session()
        username = req.route_params.get('username')
        user = session.query(models.Account).filter(models.Account.username == username).first()
        if not user:
            return func.HttpResponse("Not Found", status_code=404)
        session.close()
        result = adapters.contact_adapter.get_contact_by_user(user.id)
        return func.HttpResponse(json.dumps(result))
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)

@app.route('users/{username}/contact', methods=['POST'], auth_level=func.AuthLevel.ANONYMOUS)
def post_user_contact(req: func.HttpRequest) -> func.HttpResponse:
    try:
        if not verify_token(req):
            return func.HttpResponse("Unauthorized", status_code=401)
        session = Session()
        username = req.route_params.get('username')
        user = session.query(models.Account).filter(models.Account.username == username).first()
        if not user:
            return func.HttpResponse("Not Found", status_code=404)
        session.close()
        result = adapters.contact_adapter.create_contact(req.get_json())
        return func.HttpResponse(json.dumps(result))
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)

@app.route('users/{username}/student', methods=['GET'], auth_level=func.AuthLevel.ANONYMOUS)
def get_user_student(req: func.HttpRequest) -> func.HttpResponse:
    try:
        if not verify_token(req):
            return func.HttpResponse("Unauthorized", status_code=401)
        try:
            session = Session()
            username = req.route_params.get('username')
            user = adapters.account_adapter.get_account_by_username_or_email(username)
            if user is None:
                raise ValueError("User not found")
            student = adapters.student_adapter.get_student_by_account(user['id'])
            if not student:
                raise
            result = json.dumps(student)
            session.close()
            return func.HttpResponse(result)
        except Exception as e:
            return func.HttpResponse(str(e))
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)

@app.route('users/{username}/student', methods=['POST'], auth_level=func.AuthLevel.ANONYMOUS)
def post_user_student(req: func.HttpRequest) -> func.HttpResponse:
    try:
        if not verify_token(req):
            return func.HttpResponse("Unauthorized", status_code=401)
        session = Session()
        username = req.route_params.get('username')
        user = session.query(models.Account).filter(models.Account.username == username).first()
        if not user:
            return func.HttpResponse("Not Found", status_code=404)
        student = user.student
        if student:
            return func.HttpResponse("Conflict", status_code=409)
        user_id = user.id
        request = req.get_json()
        request["account_id"] = str(user_id)
        session.close()
        result = adapters.student_adapter.create_student(request)
        return func.HttpResponse(json.dumps(result))
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)

@app.route('users/{username}/student', methods=['PUT'], auth_level=func.AuthLevel.ANONYMOUS)
def put_user_student(req: func.HttpRequest) -> func.HttpResponse:
    try:
        if not verify_token(req):
            return func.HttpResponse("Unauthorized", status_code=401)
        session = Session()
        username = req.route_params.get('username')
        user = session.query(models.Account).filter(models.Account.username == username).first()
        if not user:
            return func.HttpResponse("Not Found", status_code=404)
        request = req.get_json()
        request["id"] = user.student.id
        result = adapters.student_adapter.update_student(request)
        session.close()
        return func.HttpResponse(json.dumps(result))
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)

@app.route('users/{username}/student', methods=['DELETE'], auth_level=func.AuthLevel.ANONYMOUS)
def delete_user_student(req: func.HttpRequest) -> func.HttpResponse:
    try:
        if not verify_token(req):
            return func.HttpResponse("Unauthorized", status_code=401)
        session = Session()
        username = req.route_params.get('username')
        user = session.query(models.Account).filter(models.Account.username == username).first()
        if not user:
            return func.HttpResponse("Not Found", status_code=404)
        result = adapters.student_adapter.delete_student(user.student.id)
        session.close()
        return func.HttpResponse('OK', status_code=200)
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)


@app.route('users/{username}/teacher', methods=['GET'], auth_level=func.AuthLevel.ANONYMOUS)
def get_user_teacher(req: func.HttpRequest) -> func.HttpResponse:
    if not verify_token(req):
        return func.HttpResponse("Unauthorized", status_code=401)
    try:
        session = Session()
        username = req.route_params.get('username')
        user = adapters.account_adapter.get_account_by_username_or_email(username)
        if user is None:
            raise ValueError("User not found")
        teacher = adapters.teacher_adapter.get_teacher_by_account(user['id'])
        if not teacher:
            return func.HttpResponse("Not Found", status_code=404)
        result = json.dumps(teacher)
        session.close()
        return func.HttpResponse(result)
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)

@app.route('users/{username}/teacher', methods=['POST'], auth_level=func.AuthLevel.ANONYMOUS)
def post_user_teacher(req: func.HttpRequest) -> func.HttpResponse:
    try:
        if not verify_token(req):
            return func.HttpResponse("Unauthorized", status_code=401)
        session = Session()
        username = req.route_params.get('username')
        user = session.query(models.Account).filter(models.Account.username == username).first()
        if not user:
            return func.HttpResponse("Not Found", status_code=404)
        try:
            teacher = adapters.teacher_adapter.get_teacher_by_account(user.id)
        except Exception as e:
            pass
        request = req.get_json()
        request["account_id"] = str(user.id)
        session.close()
        result = adapters.teacher_adapter.create_teacher(request)
        return func.HttpResponse(json.dumps(result))
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)

@app.route('users/{username}/teacher', methods=['PUT'], auth_level=func.AuthLevel.ANONYMOUS)
def put_user_teacher(req: func.HttpRequest) -> func.HttpResponse:
    try:
        if not verify_token(req):
            return func.HttpResponse("Unauthorized", status_code=401)
        session = Session()
        username = req.route_params.get('username')
        user = session.query(models.Account).filter(models.Account.username == username).first()
        if not user:
            return func.HttpResponse("Not Found", status_code=404)
        request = req.get_json()
        request["id"] = user.teacher.id
        session.close()
        result = adapters.teacher_adapter.update_teacher(request)
        return func.HttpResponse(json.dumps(result))
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)

@app.route('users/{username}/teacher', methods=['DELETE'], auth_level=func.AuthLevel.ANONYMOUS)
def delete_user_teacher(req: func.HttpRequest) -> func.HttpResponse:
    try:
        if not verify_token(req):
            return func.HttpResponse("Unauthorized", status_code=401)
        session = Session()
        username = req.route_params.get('username')
        user = session.query(models.Account).filter(models.Account.username == username).first()
        if not user:
            return func.HttpResponse("Not Found", status_code=404)
        session.close()
        teacher = adapters.teacher_adapter.get_teacher_by_account(user.id)
        if not teacher:
            return func.HttpResponse("Not Found", status_code=404)
        try:
            adapters.teacher_adapter.delete_teacher(teacher['id'])
            return func.HttpResponse("OK")
        except Exception as e:
            return func.HttpResponse(str(e), status_code=500)
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)


@app.route('users/{username}/su', methods=['GET'], auth_level=func.AuthLevel.ANONYMOUS)
def get_user_su(req: func.HttpRequest) -> func.HttpResponse:
    try:
        if not verify_token(req):
            return func.HttpResponse("Unauthorized", status_code=401)
        session = Session()
        username = req.route_params.get('username')
        user = session.query(models.Account).filter(models.Account.username == username).first()
        su = user.su
        if not su:
            return func.HttpResponse("Not Found", status_code=404)
        result = json.dumps(su.serialize())
        session.close()
        return func.HttpResponse(result)
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)

@app.route('users/{username}/su', methods=['POST'], auth_level=func.AuthLevel.ANONYMOUS)
def post_user_su(req: func.HttpRequest) -> func.HttpResponse:
    try:
        if not verify_token(req):
            return func.HttpResponse("Unauthorized", status_code=401)
        session = Session()
        username = req.route_params.get('username')
        user = session.query(models.Account).filter(models.Account.username == username).first()
        su = user.su
        if su:
            return func.HttpResponse("Conflict", status_code=409)
        request = req.get_json()
        request["account_id"] = str(user.id)
        result = adapters.su_adapter.create_su(request)
        return func.HttpResponse(json.dumps(result))
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)

@app.route('users/{username}/su', methods=['PUT'], auth_level=func.AuthLevel.ANONYMOUS)
def put_user_su(req: func.HttpRequest) -> func.HttpResponse:
    try:
        if not verify_token(req):
            return func.HttpResponse("Unauthorized", status_code=401)
        session = Session()
        username = req.route_params.get('username')
        user = session.query(models.Account).filter(models.Account.username == username).first()
        if not user:
            return func.HttpResponse("Not Found", status_code=404)
        su = user.su
        if not su:
            return func.HttpResponse("Not Found", status_code=404)
        result = adapters.su_adapter.update_su(req.get_json())
        return func.HttpResponse(json.dumps(result))
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)

@app.route('users/{username}/su', methods=['DELETE'], auth_level=func.AuthLevel.ANONYMOUS)
def delete_user_su(req: func.HttpRequest) -> func.HttpResponse:
    try:
        if not verify_token(req):
            return func.HttpResponse("Unauthorized", status_code=401)
        session = Session()
        username = req.route_params.get('username')
        user = session.query(models.Account).filter(models.Account.username == username).first()
        su = user.su
        if not su:
            return func.HttpResponse("Not Found", status_code=404)
        result = adapters.su_adapter.delete_su(su.id)
        return func.HttpResponse(json.dumps(result))
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)


@app.route('users/{username}/parent', methods=['GET'], auth_level=func.AuthLevel.ANONYMOUS)
def get_user_parent(req: func.HttpRequest) -> func.HttpResponse:
    try:
        if not verify_token(req):
            return func.HttpResponse("Unauthorized", status_code=401)
        session = Session()
        username = req.route_params.get('username')
        user = session.query(models.Account).filter(models.Account.username == username).first()
        parent = user.parent
        if not parent:
            return func.HttpResponse("Not Found", status_code=404)
        result = json.dumps(parent.serialize())
        session.close()
        return func.HttpResponse(result)
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)

@app.route('users/{username}/parent', methods=['POST'], auth_level=func.AuthLevel.ANONYMOUS)
def post_user_parent(req: func.HttpRequest) -> func.HttpResponse:
    try:
        if not verify_token(req):
            return func.HttpResponse("Unauthorized", status_code=401)
        session = Session()
        username = req.route_params.get('username')
        user = session.query(models.Account).filter(models.Account.username == username).first()
        if not user:
            return func.HttpResponse("Not Found", status_code=404)
        parent = user.parent
        if parent:
            return func.HttpResponse("Conflict", status_code=409)
        request = req.get_json(force=True)
        request["account_id"] = str(user.id)
        result = adapters.parent_adapter.create_parent(request)
        session.close()
        return func.HttpResponse(json.dumps(result))
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)

@app.route('users/{username}/parent', methods=['PUT'], auth_level=func.AuthLevel.ANONYMOUS)
def put_user_parent(req: func.HttpRequest) -> func.HttpResponse:
    try:
        if not verify_token(req):
            return func.HttpResponse("Unauthorized", status_code=401)
        session = Session()
        username = req.route_params.get('username')
        user = session.query(models.Account).filter(models.Account.username == username).first()
        parent = user.parent
        if not parent:
            return func.HttpResponse("Not Found", status_code=404)
        result = adapters.parent_adapter.update_parent(req.get_json())
        return func.HttpResponse(json.dumps(result))
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)

@app.route('users/{username}/parent', methods=['DELETE'], auth_level=func.AuthLevel.ANONYMOUS)
def delete_user_parent(req: func.HttpRequest) -> func.HttpResponse:
    try:
        if not verify_token(req):
            return func.HttpResponse("Unauthorized", status_code=401)
        session = Session()
        username = req.route_params.get('username')
        user = session.query(models.Account).filter(models.Account.username == username).first()
        parent = user.parent
        if not parent:
            return func.HttpResponse("Not Found", status_code=404)
        adapters.parent_adapter.delete_parent(parent.id)
        return func.HttpResponse(f"Deleted {username}", status_code=200)
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)


@app.route('users/{username}/abscence', methods=['GET'], auth_level=func.AuthLevel.ANONYMOUS)
def get_user_abscences(req: func.HttpRequest) -> func.HttpResponse:
    try:
        if not verify_token(req):
            return func.HttpResponse("Unauthorized", status_code=401)
        session = Session()
        username = req.route_params.get('username')
        user = session.query(models.Account).filter(models.Account.username == username).first()
        if not user:
            return func.HttpResponse("Not Found", status_code=404)
        session.close()
        result = adapters.absence_adapter.get_abscence_by_user(user.id)
        return func.HttpResponse(result)
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)

@app.route('users/{username}/abscence', methods=['POST'], auth_level=func.AuthLevel.ANONYMOUS)
def post_user_abscence(req: func.HttpRequest) -> func.HttpResponse:
    try:
        if not verify_token(req):
            return func.HttpResponse("Unauthorized", status_code=401)
        session = Session()
        username = req.route_params.get('username')
        user = session.query(models.Account).filter(models.Account.username == username).first()
        if not user:
            return func.HttpResponse("Not Found", status_code=404)
        session.close()
        result = adapters.absence_adapter.create_abscence(req.get_json())
        return func.HttpResponse(result)
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)

@app.route('users/{username}/abscence/{date}', methods=['GET'], auth_level=func.AuthLevel.ANONYMOUS)
def get_abscence(req: func.HttpRequest) -> func.HttpResponse:
    try:
        if not verify_token(req):
            return func.HttpResponse("Unauthorized", status_code=401)
        session = Session()
        username = req.route_params.get('username')
        date = req.route_params.get('date')
        user = session.query(models.Account).filter(models.Account.username == username).first()
        if not user:
            return func.HttpResponse("Not Found", status_code=404)
        session.close()
        result = adapters.absence_adapter.get_abscence_by_user_date(user.id, date)
        return func.HttpResponse(result)
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)

@app.route('users/{username}/abscence/{date}', methods=['PUT'], auth_level=func.AuthLevel.ANONYMOUS)
def put_abscence(req: func.HttpRequest) -> func.HttpResponse:
    try:
        if not verify_token(req):
            return func.HttpResponse("Unauthorized", status_code=401)
        session = Session()
        username = req.route_params.get('username')
        date = req.route_params.get('date')
        user = session.query(models.Account).filter(models.Account.username == username).first()
        if not user:
            return func.HttpResponse("Not Found", status_code=404)
        session.close()
        result = adapters.absence_adapter.update_abscence(req.get_json())
        return func.HttpResponse(result)
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)



@app.route('students', methods=['GET'], auth_level=func.AuthLevel.ANONYMOUS)
def get_students(req: func.HttpRequest) -> func.HttpResponse:
    try:
        if not verify_token(req):
            return func.HttpResponse("Unauthorized", status_code=401)
        result = adapters.student_adapter.get_students()
        return func.HttpResponse(json.dumps(result))
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)

@app.route('students/{student_id}', methods=['GET'], auth_level=func.AuthLevel.ANONYMOUS)
def get_student(req: func.HttpRequest) -> func.HttpResponse:
    try:
        if not verify_token(req):
            return func.HttpResponse("Unauthorized", status_code=401)
        result = adapters.student_adapter.get_student(req.route_params.get('student_id'))
        return func.HttpResponse(json.dumps(result))
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)



@app.route('parents', methods=['GET'], auth_level=func.AuthLevel.ANONYMOUS)
def get_parents(req: func.HttpRequest) -> func.HttpResponse:
    try:
        if not verify_token(req):
            return func.HttpResponse("Unauthorized", status_code=401)
        result = adapters.parent_adapter.get_parents()
        return func.HttpResponse(json.dumps(result))
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)

@app.route('parents/{parent_id}', methods=['GET'], auth_level=func.AuthLevel.ANONYMOUS)
def get_parent(req: func.HttpRequest) -> func.HttpResponse:
    try:
        if not verify_token(req):
            return func.HttpResponse("Unauthorized", status_code=401)
        result = adapters.parent_adapter.get_parent(req.route_params.get('parent_id'))
        return func.HttpResponse(json.dumps(result))
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)




@app.route('teachers', methods=['GET'], auth_level=func.AuthLevel.ANONYMOUS)
def get_teachers(req: func.HttpRequest) -> func.HttpResponse:
    try:
        if not verify_token(req):
            return func.HttpResponse("Unauthorized", status_code=401)
        result = adapters.teacher_adapter.get_teachers()
        return func.HttpResponse(json.dumps(result))
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)

@app.route('teachers/{teacher_id}', methods=['GET'], auth_level=func.AuthLevel.ANONYMOUS)
def get_teacher(req: func.HttpRequest) -> func.HttpResponse:
    try:
        if not verify_token(req):
            return func.HttpResponse("Unauthorized", status_code=401)
        result = adapters.teacher_adapter.get_teacher(req.route_params.get('teacher_id'))
        return func.HttpResponse(json.dumps(result))
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)




@app.route('su', methods=['GET'], auth_level=func.AuthLevel.ANONYMOUS)
def get_sus(req: func.HttpRequest) -> func.HttpResponse:
    try:
        if not verify_token(req):
            return func.HttpResponse("Unauthorized", status_code=401)
        result = adapters.su_adapter.get_sus()
        return func.HttpResponse(json.dumps(result))
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)

@app.route('su/{su_id}', methods=['GET'], auth_level=func.AuthLevel.ANONYMOUS)
def get_su(req: func.HttpRequest) -> func.HttpResponse:
    try:
        if not verify_token(req):
            return func.HttpResponse("Unauthorized", status_code=401)
        result = adapters.su_adapter.get_su(req.route_params.get('su_id'))
        return func.HttpResponse(json.dumps(result))
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)



@app.route('school_classes', methods=['GET'], auth_level=func.AuthLevel.ANONYMOUS)
def get_school_classes(req: func.HttpRequest) -> func.HttpResponse:
    try:
        if not verify_token(req):
            return func.HttpResponse("Unauthorized", status_code=401)
        result = adapters.school_class_adapter.get_school_classes()
        return func.HttpResponse(json.dumps(result))
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)

@app.route('school_classes', methods=['POST'], auth_level=func.AuthLevel.ANONYMOUS)
def post_school_class(req: func.HttpRequest) -> func.HttpResponse:
    try:
        if not verify_token(req):
            return func.HttpResponse("Unauthorized", status_code=401)
        result = adapters.school_class_adapter.create_school_class(req.get_json())
        return func.HttpResponse(json.dumps(result))
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)

@app.route('school_classes/{school_class_id}', methods=['GET'], auth_level=func.AuthLevel.ANONYMOUS)
def get_school_class(req: func.HttpRequest) -> func.HttpResponse:
    try:
        if not verify_token(req):
            return func.HttpResponse("Unauthorized", status_code=401)
        result = adapters.school_class_adapter.get_school_class(req.route_params.get('school_class_id'))
        return func.HttpResponse(json.dumps(result))
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)

@app.route('school_classes/{school_class_id}', methods=['PUT'], auth_level=func.AuthLevel.ANONYMOUS)
def put_school_class(req: func.HttpRequest) -> func.HttpResponse:
    try:
        if not verify_token(req):
            return func.HttpResponse("Unauthorized", status_code=401)
        result = adapters.school_class_adapter.update_school_class(req.get_json())
        return func.HttpResponse(json.dumps(result))
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)

@app.route('school_classes/{school_class_id}', methods=['DELETE'], auth_level=func.AuthLevel.ANONYMOUS)
def delete_school_class(req: func.HttpRequest) -> func.HttpResponse:
    try:
        if not verify_token(req):
            return func.HttpResponse("Unauthorized", status_code=401)
        result = adapters.school_class_adapter.delete_school_class(req.route_params.get('school_class_id'))
        return func.HttpResponse(json.dumps(result))
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)



@app.route('school_subject_students', methods=['GET'], auth_level=func.AuthLevel.ANONYMOUS)
def get_school_subject_students(req: func.HttpRequest) -> func.HttpResponse:
    try:
        if not verify_token(req):
            return func.HttpResponse("Unauthorized", status_code=401)
        result = adapters.school_subject_student_adapter.get_school_subject_students()
        return func.HttpResponse(json.dumps(result))
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)

@app.route('school_subject_students', methods=['POST'], auth_level=func.AuthLevel.ANONYMOUS)
def post_school_subject_student(req: func.HttpRequest) -> func.HttpResponse:
    try:
        if not verify_token(req):
            return func.HttpResponse("Unauthorized", status_code=401)
        result = adapters.school_subject_student_adapter.create_school_subject_student(req.get_json())
        return func.HttpResponse(json.dumps(result))
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)



@app.route('school_grade', methods=['GET'], auth_level=func.AuthLevel.ANONYMOUS)
def get_school_grades(req: func.HttpRequest) -> func.HttpResponse:
    try:
        if not verify_token(req):
            return func.HttpResponse("Unauthorized", status_code=401)
        result = adapters.school_grade_adapter.get_school_grades()
        return func.HttpResponse(json.dumps(result))
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)

@app.route('school_grade/{school_grade_id}', methods=['GET'], auth_level=func.AuthLevel.ANONYMOUS)
def get_school_grade(req: func.HttpRequest) -> func.HttpResponse:
    try:
        if not verify_token(req):
            return func.HttpResponse("Unauthorized", status_code=401)
        result = adapters.school_grade_adapter.get_school_grade(req.route_params.get('school_grade_id'))
        return func.HttpResponse(json.dumps(result))
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)

@app.route('school_grade/{school_grade_id}', methods=['PUT'], auth_level=func.AuthLevel.ANONYMOUS)
def put_school_grade(req: func.HttpRequest) -> func.HttpResponse:
    try:
        if not verify_token(req):
            return func.HttpResponse("Unauthorized", status_code=401)
        result = adapters.school_grade_adapter.update_school_grade(req.get_json())
        return func.HttpResponse(json.dumps(result))
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)

@app.route('school_grade/{school_grade_id}', methods=['DELETE'], auth_level=func.AuthLevel.ANONYMOUS)
def delete_school_grade(req: func.HttpRequest) -> func.HttpResponse:
    try:
        if not verify_token(req):
            return func.HttpResponse("Unauthorized", status_code=401)
        result = adapters.school_grade_adapter.delete_school_grade(req.route_params.get('school_grade_id'))
        return func.HttpResponse(json.dumps(result))
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)


@app.route('school_subjects', methods=['GET'], auth_level=func.AuthLevel.ANONYMOUS)
def get_school_subjects(req: func.HttpRequest) -> func.HttpResponse:
    try:
        if not verify_token(req):
            return func.HttpResponse("Unauthorized", status_code=401)
        result = adapters.school_subject_adapter.get_school_subjects()
        return func.HttpResponse(json.dumps(result))
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)

@app.route('school_subjects', methods=['POST'], auth_level=func.AuthLevel.ANONYMOUS)
def post_school_subject(req: func.HttpRequest) -> func.HttpResponse:
    try:
        if not verify_token(req):
            return func.HttpResponse("Unauthorized", status_code=401)
        result = adapters.school_subject_adapter.create_school_subject(req.get_json())
        return func.HttpResponse(json.dumps(result))
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)

@app.route('school_subjects/{school_subject_id}', methods=['GET'], auth_level=func.AuthLevel.ANONYMOUS)
def get_school_subject(req: func.HttpRequest) -> func.HttpResponse:
    try:
        if not verify_token(req):
            return func.HttpResponse("Unauthorized", status_code=401)
        result = adapters.school_subject_adapter.get_school_subject(req.route_params.get('school_subject_id'))
        return func.HttpResponse(json.dumps(result))
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)

@app.route('school_subjects/{school_subject_id}', methods=['PUT'], auth_level=func.AuthLevel.ANONYMOUS)
def put_school_subject(req: func.HttpRequest) -> func.HttpResponse:
    try:
        if not verify_token(req):
            return func.HttpResponse("Unauthorized", status_code=401)
        result = adapters.school_subject_adapter.update_school_subject(req.get_json())
        return func.HttpResponse(json.dumps(result))
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)

@app.route('school_subjects/{school_subject_id}', methods=['DELETE'], auth_level=func.AuthLevel.ANONYMOUS)
def delete_school_subject(req: func.HttpRequest) -> func.HttpResponse:
    try:
        if not verify_token(req):
            return func.HttpResponse("Unauthorized", status_code=401)
        result = adapters.school_subject_adapter.delete_school_subject(req.route_params.get('school_subject_id'))
        return func.HttpResponse(json.dumps(result))
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)

@app.route('school_subject_entries', methods=['GET'], auth_level=func.AuthLevel.ANONYMOUS)
def get_school_subject_entries(req: func.HttpRequest) -> func.HttpResponse:
    try:
        if not verify_token(req):
            return func.HttpResponse("Unauthorized", status_code=401)
        week = req.params.get('week')
        year = req.params.get('year')
        if not week:
            return func.HttpResponse("Bad Request", status_code=400)
        else:
            week = int(week)
        if week < 1 or week > 53:
            return func.HttpResponse("Bad Request: a year only has at most 53 weeks", status_code=400) 
        if not year:
            year = date.today().year
        else:
            year = int(year)
        result = adapters.school_subject_entry_adapter.get_school_subject_entries_for_week(week, year)
        if not result:
            return func.HttpResponse("Not Found", status_code=404)
        return func.HttpResponse(json.dumps(result))
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)

@app.route('school_subject_entries/{school_subject_entry_id}', methods=['GET'], auth_level=func.AuthLevel.ANONYMOUS)
def get_school_subject_entry(req: func.HttpRequest) -> func.HttpResponse:
    try:
        if not verify_token(req):
            return func.HttpResponse("Unauthorized", status_code=401)
        result = adapters.school_subject_entry_adapter.get_school_subject_entry(req.route_params.get('school_subject_entry_id'))
        return func.HttpResponse(json.dumps(result))
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)





