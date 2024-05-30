from backend.models import Student
from sqlalchemy.orm import Session, sessionmaker
import uuid

class StudentAdapter:
    def __init__(self, session: sessionmaker[Session]):
        self.Session = session

    def create_student(self, request: dict) -> dict:
        session = self.Session()
        student = Student(
            account_id = uuid.UUID(request['account_id']),
            school_class_id = request.get('school_class_id', None),
        )
        session.add(student)
        session.commit()
        data = student.serialize()
        session.close()
        return data
    
    def get_students(self) -> list[dict]:
        session = self.Session()
        students = session.query(Student).all()
        data = [student.serialize(depth=0) for student in students]
        session.close()
        return data
    
    def get_student(self, student_id: int) -> dict:
        session = self.Session()
        student = session.query(Student).filter(Student.id == student_id).first()
        data = student.serialize()
        session.close()
        return data
    
    def get_student_by_account(self, account_id: uuid.UUID) -> dict:
        session = self.Session()
        student = session.query(Student).filter(Student.account_id == account_id).first()
        data = student.serialize()
        session.close()
        return data
    
    def get_students_by_school_class(self, school_class_id: int) -> list[dict]:
        session = self.Session()
        students = session.query(Student).filter(Student.school_class_id == school_class_id).all()
        data = [student.serialize() for student in students]
        session.close()
        return data
    
    def update_student(self, request: dict) -> dict:
        session = self.Session()
        student_id = request['id']
        student = session.query(Student).filter(Student.id == student_id).first()
        student.school_class_id = request.get('school_class_id', student.school_class_id)
        session.commit()
        data = student.serialize()
        session.close()
        return data
    
    def delete_student(self, student_id: int) -> None:
        session = self.Session()
        student = session.query(Student).filter(Student.id == student_id).first()
        session.delete(student)
        session.commit()
        session.close()
    