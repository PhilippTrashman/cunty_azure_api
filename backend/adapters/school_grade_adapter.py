from backend.models import SchoolGrade
from sqlalchemy.orm import Session, sessionmaker

class SchoolGradeAdapter:
    def __init__(self, session: sessionmaker[Session]):
        self.Session = session

    def create_school_grade(self, request: dict) -> dict:
        session = self.Session()
        school_grade = SchoolGrade(
            year = request['year'],
        )
        session.add(school_grade)
        session.commit()
        data = school_grade.serialize()
        session.close()
        return data
    
    def get_school_grades(self) -> list[dict]:
        session = self.Session()
        school_grades = session.query(SchoolGrade).all()
        data = [school_grade.serialize(depth=0) for school_grade in school_grades]
        session.close()
        return data
    
    def get_school_grade(self, school_grade_id: int) -> dict:
        session = self.Session()
        school_grade = session.query(SchoolGrade).filter(SchoolGrade.id == school_grade_id).first()
        data = school_grade.serialize()
        session.close()
        return data
    
    def update_school_grade(self, request: dict) -> dict:
        session = self.Session()
        school_grade_id = request['id']
        school_grade = session.query(SchoolGrade).filter(SchoolGrade.id == school_grade_id).first()
        school_grade.year = request.get('year', school_grade.year)
        session.commit()
        data = school_grade.serialize()
        session.close()
        return data
    
    def delete_school_grade(self, school_grade_id: int) -> dict:
        session = self.Session()
        school_grade = session.query(SchoolGrade).filter(SchoolGrade.id == school_grade_id).first()
        data = school_grade.serialize()
        session.delete(school_grade)
        session.commit()
        session.close()
        return data
