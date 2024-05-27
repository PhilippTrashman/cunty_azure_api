from backend.models import Account, Base
from backend.errors import *
from sqlalchemy.orm import Session, sessionmaker
import uuid
import datetime

class AccountAdapter:
    def __init__(self, session: sessionmaker[Session]):
        self.Session = session

    def create_account(self, request: dict) -> dict:
        session = self.Session()
        birthday = datetime.datetime.strptime(request['birthday'], '%Y-%m-%d').date() if 'birthday' in request else None
        account = Account(
            username = request['username'],
            password = request['password'],
            email = request['email'],
            name = request['name'],
            last_name = request['last_name'],
            birthday = birthday,
        )
        session.add(account)
        session.commit()
        data = account.serialize()
        session.close()
        return data
    
    def check_account_password(self, username: str, password: str) -> bool:
        session = self.Session()
        account = session.query(Account).filter(Account.username == username).first()
        if not account:
            account = session.query(Account).filter(Account.email == username).first()
        if not account:
            raise EntityNotFound(f"Account with username or email {username} not found")
        session.close()
        return account.password == password
    
    def get_accounts(self) -> list[dict]:
        session = self.Session()
        accounts = session.query(Account).all()
        data = [account.serialize(depth=0) for account in accounts]
        session.close()
        return data
    
    def get_account(self, account_id: uuid.UUID) -> dict:
        session = self.Session()
        account = session.query(Account).filter(Account.id == account_id).first()
        data = account.serialize()
        session.close()
        return data

    def get_account_by_username_or_email(self, username: str) -> dict:
        session = self.Session()
        account = session.query(Account).filter(Account.username == username).first()
        if not account:
            account = session.query(Account).filter(Account.email == username).first()
        if not account:
            raise EntityNotFound(f"Account with username or email {username} not found")
        data = account.serialize()
        session.close()
        return data
    
    def update_account(self, request: dict, account_id: uuid.UUID) -> dict:
        session = self.Session()
        account_id = uuid.UUID(account_id)
        birthday = datetime.strptime(request['birthday'], '%Y-%m-%d').date() if 'birthday' in request else account.birthday
        account = session.query(Account).filter(Account.id == account_id).first()
        account.username = request.get('username', account.username)
        account.password = request.get('password', account.password)
        account.email = request.get('email', account.email)
        account.name = request.get('name', account.name)
        account.last_name = request.get('last_name', account.last_name)
        account.birthday = birthday
        session.commit()
        data = account.serialize()
        session.close()
        return data
    
    def delete_account(self, account_id: uuid.UUID) -> None:
        session = self.Session()
        account = session.query(Account).filter(Account.id == account_id).first()
        session.delete(account)
        session.commit()
        session.close()

