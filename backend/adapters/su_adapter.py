from backend.models import Su
from sqlalchemy.orm import Session, sessionmaker
import uuid

class SuAdapter:
    def __init__(self, session: sessionmaker[Session]):
        self.Session = session

    def create_su(self, request: dict) -> dict:
        session = self.Session()
        su = Su(
            account_id = uuid.UUID(request['account_id']),
            admin_rights = request.get('admin_rights', False),
            change_subject_status = request.get('change_subject_status', False),
            manage_users = request.get('manage_users', False),
            manage_school = request.get('manage_school', False),
        )
        session.add(su)
        session.commit()
        data = su.serialize()
        session.close()
        return data
    
    def get_sus(self) -> list[dict]:
        session = self.Session()
        sus = session.query(Su).all()
        data = [su.serialize(depth=0) for su in sus]
        session.close()
        return data
    
    def get_su(self, su_id: int) -> dict:
        session = self.Session()
        su = session.query(Su).filter(Su.id == su_id).first()
        data = su.serialize()
        session.close()
        return data
    
    def get_su_by_account(self, account_id: uuid.UUID) -> dict:
        session = self.Session()
        su = session.query(Su).filter(Su.account_id == account_id).first()
        data = su.serialize()
        session.close()
        return data
    
    def update_su(self, request: dict) -> dict:
        session = self.Session()
        su_id = request['id']
        su = session.query(Su).filter(Su.id == su_id).first()
        su.account_id = request.get('account_id', su.account_id)
        su.admin_rights = request.get('admin_rights', su.admin_rights)
        su.change_subject_status = request.get('change_subject_status', su.change_subject_status)
        su.manage_users = request.get('manage_users', su.manage_users)
        su.manage_school = request.get('manage_school', su.manage_school)
        session.commit()
        data = su.serialize()
        session.close()
        return data
    
    def delete_su(self, su_id: int) -> dict:
        session = self.Session()
        su = session.query(Su).filter(Su.id == su_id).first()
        session.delete(su)
        session.commit()
        data = su.serialize()
        session.close()
        return data
    
    
