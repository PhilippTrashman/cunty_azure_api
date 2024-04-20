from backend.models import AccessToken, Account
from backend.errors import *
from sqlalchemy.orm import Session, sessionmaker
import uuid
from datetime import timedelta, datetime
import hmac
import hashlib

class AccessTokenAdapter:
    def __init__(self, session: sessionmaker[Session]):
        self.Session = session

    def create_access_token(self, request: dict) -> dict:
        session = self.Session()
        try:
            access_token = AccessToken(
                account_id = uuid.UUID(request['account_id']),
                token = self.generate_token(),
                expiration_date = self.get_expiration_date(),
            )
        except KeyError as e:
            raise PayloadError(f"Missing key: {e}")
        session.add(access_token)
        session.commit()
        data = access_token.serialize()
        session.close()
        return data
    
    def get_access_tokens(self) -> list[dict]:
        session = self.Session()
        access_tokens = session.query(AccessToken).all()
        data = [access_token.serialize(depth=0) for access_token in access_tokens]
        session.close()
        return data
    
    def get_access_token(self, access_token_id: int) -> dict:
        session = self.Session()
        access_token = session.query(AccessToken).filter(AccessToken.id == access_token_id).first()
        if not access_token:
            raise EntityNotFound(f"Access token with id {access_token_id} not found")
        data = access_token.serialize()
        session.close()
        return data
    
    def get_access_token_by_token(self, token: str) -> dict:
        session = self.Session()
        access_token = session.query(AccessToken).filter(AccessToken.token == token).first()
        if not access_token:
            raise EntityNotFound(f"Access token with token {token} not found")
        data = access_token.serialize()
        session.close()
        return data
    
    def get_access_token_by_account(self, account_id: uuid.UUID) -> dict:
        session = self.Session()
        access_token = session.query(AccessToken).filter(AccessToken.account_id == account_id).first()
        if not access_token:
            raise EntityNotFound(f"Access token for account {account_id} not found")
        data = access_token.serialize()
        session.close()
        return data
    
    def delete_access_token(self, access_token_id: int) -> dict:
        session = self.Session()
        access_token = session.query(AccessToken).filter(AccessToken.id == access_token_id).first()
        if not access_token:
            raise EntityNotFound(f"Access token with id {access_token_id} not found")
        session.delete(access_token)
        session.commit()
        data = access_token.serialize()
        session.close()
        return data
    
    def generate_token(self, account_id: uuid.UUID, stay_logged_in: bool) -> str:
        session = self.Session()
        account = session.query(Account).filter(Account.id == account_id).first()
        secret = account.secret
        expiration_date = self.get_expiration_date(stay_logged_in)
        data = f'{account_id}{expiration_date}'
        token = hmac.new(secret, data.encode(), hashlib.sha256).hexdigest()
        session.close()
        return token
    
    def get_expiration_date(self, stay_logged_in: bool) -> datetime:
        if stay_logged_in:
            return datetime.now() + timedelta(days=30)
        return datetime.now() + timedelta(days=1)
    
    def validate_token(self, token: str, account_id: uuid.UUID) -> None:
        session = self.Session()
        account = session.query(Account).filter(Account.id == account_id).first()
        secret = account.secret
        expiration_date = self.get_expiration_date()
        data = f'{account_id}{expiration_date}'
        expected_token = hmac.new(secret, data.encode(), hashlib.sha256).hexdigest()
        session.close()
        if not token == expected_token:
            raise TokenNotVerified("Token not verified")
    

