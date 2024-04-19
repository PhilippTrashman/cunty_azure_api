from backend.models import SubjectType
from sqlalchemy.orm import Session, sessionmaker

class SubjectTypeAdapter:
    def __init__(self, session: sessionmaker[Session]):
        self.Session = session

    def create_subject_type(self, request: dict) -> dict:
        session = self.Session()
        subject_type = SubjectType(
            name = request['name'],
            handle = request['handle'],
        )
        session.add(subject_type)
        session.commit()
        data = subject_type.serialize()
        session.close()
        return data
    
    def get_subject_types(self) -> list[dict]:
        session = self.Session()
        subject_types = session.query(SubjectType).all()
        data = [subject_type.serialize(depth=0) for subject_type in subject_types]
        session.close()
        return data
    
    def get_subject_type(self, subject_type_id: int) -> dict:
        session = self.Session()
        subject_type = session.query(SubjectType).filter(SubjectType.id == subject_type_id).first()
        data = subject_type.serialize()
        session.close()
        return data
    
    def update_subject_type(self, request: dict) -> dict:
        session = self.Session()
        subject_type_id = request['id']
        subject_type = session.query(SubjectType).filter(SubjectType.id == subject_type_id).first()
        subject_type.name = request.get('name', subject_type.name)
        subject_type.handle = request.get('handle', subject_type.handle)
        session.commit()
        data = subject_type.serialize()
        session.close()
        return data
    
    def delete_subject_type(self, subject_type_id: int) -> dict:
        session = self.Session()
        subject_type = session.query(SubjectType).filter(SubjectType.id == subject_type_id).first()
        session.delete(subject_type)
        session.commit()
        data = subject_type.serialize()
        session.close()
        return data
    
    