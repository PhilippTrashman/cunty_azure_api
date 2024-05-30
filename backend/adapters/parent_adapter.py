from backend.models import Parent
from sqlalchemy.orm import Session, sessionmaker
import uuid

class ParentAdapter:
    def __init__(self, session: sessionmaker[Session]):
        self.Session = session

    def create_parent(self, request: dict) -> dict:
        session = self.Session()
        parent = Parent(
            account_id = uuid.UUID(request['account_id']),
        )
        session.add(parent)
        session.commit()
        data = parent.serialize()
        session.close()
        return data
    
    def get_parents(self) -> list[dict]:
        session = self.Session()
        parents = session.query(Parent).all()
        data = [parent.serialize(depth=0) for parent in parents]
        session.close()
        return data
    
    def get_parent(self, parent_id: int) -> dict:
        session = self.Session()
        parent = session.query(Parent).filter(Parent.id == parent_id).first()
        data = parent.serialize()
        session.close()
        return data
    
    def get_parent_by_account(self, account_id: uuid.UUID) -> dict:
        session = self.Session()
        parent = session.query(Parent).filter(Parent.account_id == account_id).first()
        data = parent.serialize()
        session.close()
        return data
    
    def update_parent(self, request: dict) -> dict:
        session = self.Session()
        parent_id = request['id']
        parent = session.query(Parent).filter(Parent.id == parent_id).first()
        parent.account_id = request.get('account_id', parent.account_id)
        session.commit()
        data = parent.serialize()
        session.close()
        return data
    
    def delete_parent(self, parent_id: int) -> None:
        session = self.Session()
        parent = session.query(Parent).filter(Parent.id == parent_id).first()
        session.delete(parent)
        session.commit()
        session.close()