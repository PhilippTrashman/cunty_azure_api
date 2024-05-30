from backend.models import ParentStudent, Parent, Student
from sqlalchemy.orm import Session, sessionmaker
import datetime

class ParentStudentAdapter:
    def __init__(self, session: sessionmaker[Session]):
        self.Session = session

    def create_parent_student(self, request: dict) -> dict:
        session = self.Session()
        parent_student = ParentStudent(
            parent_id = request['parent_id'],
            student_id = request['student_id'],
        )
        session.add(parent_student)
        session.commit()
        data = parent_student.serialize()
        session.close()
        return data
    
    def get_parent_students(self) -> list[dict]:
        session = self.Session()
        parent_students = session.query(ParentStudent).all()
        data = [parent_student.serialize(depth=0) for parent_student in parent_students]
        session.close()
        return data
    
    def get_parent_student(self, parent_student_id: int) -> dict:
        session = self.Session()
        parent_student = session.query(ParentStudent).filter(ParentStudent.id == parent_student_id).first()
        data = parent_student.serialize()
        session.close()
        return data
    
    def get_parent_student_by_parent(self, parent_id: int) -> list[dict]:
        session = self.Session()
        parent_students = session.query(ParentStudent).filter(ParentStudent.parent_id == parent_id).all()
        data = [parent_student.serialize() for parent_student in parent_students]
        session.close()
        return data
    
    def get_parent_student_by_student(self, student_id: int) -> list[dict]:
        session = self.Session()
        parent_students = session.query(ParentStudent).filter(ParentStudent.student_id == student_id).all()
        data = [parent_student.serialize() for parent_student in parent_students]
        session.close()
        return data
    
    def update_parent_student(self, request: dict) -> dict:
        session = self.Session()
        parent_student_id = request['id']
        parent_student = session.query(ParentStudent).filter(ParentStudent.id == parent_student_id).first()
        parent_student.parent_id = request.get('parent_id', parent_student.parent_id)
        parent_student.student_id = request.get('student_id', parent_student.student_id)
        session.commit()
        data = parent_student.serialize()
        session.close()
        return data
    
    def delete_parent_student(self, parent_student_id: int) -> dict:
        session = self.Session()
        parent_student = session.query(ParentStudent).filter(ParentStudent.id == parent_student_id).first()
        data = parent_student.serialize()
        session.delete(parent_student)
        session.commit()
        session.close()
        return data
    
    
