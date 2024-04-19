from backend.models import SchoolSubjectStudent
from sqlalchemy.orm import Session, sessionmaker

class SchoolSubjectStudentAdapter:
    def __init__(self, session: sessionmaker[Session]):
        self.Session = session

    def create_school_subject_student(self, request: dict) -> dict:
        session = self.Session()
        school_subject_student = SchoolSubjectStudent(
            student_id = request['student_id'],
            subject_id = request['subject_id'],
        )
        session.add(school_subject_student)
        session.commit()
        data = school_subject_student.serialize()
        session.close()
        return data

    def get_school_subject_students(self) -> list[dict]:
        session = self.Session()
        school_subject_students = session.query(SchoolSubjectStudent).all()
        data = [school_subject_student.serialize(depth=0) for school_subject_student in school_subject_students]
        session.close()
        return data

    def get_school_subject_student(self, school_subject_student_id: int) -> dict:
        session = self.Session()
        school_subject_student = session.query(SchoolSubjectStudent).filter(SchoolSubjectStudent.id == school_subject_student_id).first()
        data = school_subject_student.serialize()
        session.close()
        return data

    def get_school_subject_student_for_student(self, student_id: int) -> list[dict]:
        session = self.Session()
        school_subject_students = session.query(SchoolSubjectStudent).filter(SchoolSubjectStudent.student_id == student_id).all()
        data = [school_subject_student.serialize(from_student=True) for school_subject_student in school_subject_students]
        session.close()
        return data
    
    def get_school_subject_student_for_subject(self, subject_id: int) -> list[dict]:
        session = self.Session()
        school_subject_students = session.query(SchoolSubjectStudent).filter(SchoolSubjectStudent.subject_id == subject_id).all()
        data = [school_subject_student.serialize(from_subject=True) for school_subject_student in school_subject_students]
        session.close()
        return data

    def update_school_subject_student(self, request: dict) -> dict:
        session = self.Session()
        school_subject_student_id = request['id']
        school_subject_student = session.query(SchoolSubjectStudent).filter(SchoolSubjectStudent.id == school_subject_student_id).first()
        school_subject_student.student_id = request.get('student_id', school_subject_student.student_id)
        school_subject_student.subject_id = request.get('subject_id', school_subject_student.subject_id)
        session.commit()
        data = school_subject_student.serialize()
        session.close()
        return data

    def delete_school_subject_student(self, school_subject_student_id: int) -> dict:
        session = self.Session()
        school_subject_student = session.query(SchoolSubjectStudent).filter(SchoolSubjectStudent.id == school_subject_student_id).first()
        session.delete(school_subject_student)
        session.commit()
        data = school_subject_student.serialize()
        session.close()
        return data

