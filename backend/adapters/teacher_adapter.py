from backend.models import Teacher
from sqlalchemy.orm import Session, sessionmaker
import uuid

class TeacherAdapter:
    def __init__(self, session: sessionmaker[Session]):
        self.Session = session

    def create_teacher(self, request: dict) -> dict:
        session = self.Session()
        teacher = Teacher(
            account_id = uuid.UUID(request['account_id']),
            abbreviation = request['abbreviation'],
        )
        session.add(teacher)
        session.commit()
        data = teacher.serialize()
        session.close()
        return data
    
    def get_teachers(self) -> list[dict]:
        session = self.Session()
        teachers = session.query(Teacher).all()
        data = [teacher.serialize(0) for teacher in teachers]
        session.close()
        return data
    
    def get_teacher(self, teacher_id: int) -> dict:
        session = self.Session()
        teacher = session.query(Teacher).filter(Teacher.id == teacher_id).first()
        data = teacher.serialize()
        session.close()
        return data
    
    def get_teacher_by_account(self, account_id: uuid.UUID) -> dict:
        session = self.Session()
        teacher = session.query(Teacher).filter(Teacher.account_id == account_id).first()
        if teacher == None:
            raise Exception('Teacher not found')
        data = teacher.serialize()
        session.close()
        return data
    
    def update_teacher(self, request: dict) -> dict:
        session = self.Session()
        teacher_id = request['id']
        teacher = session.query(Teacher).filter(Teacher.id == teacher_id).first()
        teacher.account_id = request.get('account_id', teacher.account_id)
        teacher.abbreviation = request.get('abbreviation', teacher.abbreviation)
        session.commit()
        data = teacher.serialize()
        session.close()
        return data
    
    def delete_teacher(self, teacher_id: int) -> None:
        session = self.Session()
        teacher = session.query(Teacher).filter(Teacher.id == teacher_id).first()
        session.delete(teacher)
        session.commit()
        session.close()
        