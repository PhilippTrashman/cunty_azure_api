from backend.models import SchoolClass
from sqlalchemy.orm import Session, sessionmaker

class SchoolClassAdapter:
    def __init__(self, session: sessionmaker[Session]):
        self.Session = session

    def create_school_class(self, request: dict) -> dict:
        session = self.Session()
        school_class = SchoolClass(
            name = request['name'],
            grade_id = request['grade_id'],
            head_teacher_id = request.get('head_teacher_id', None),
        )
        session.add(school_class)
        session.commit()
        data = school_class.serialize()
        session.close()
        return data
    
    def get_school_classes(self) -> list[dict]:
        session = self.Session()
        school_classes = session.query(SchoolClass).all()
        data = [school_class.serialize(depth=0) for school_class in school_classes]
        session.close()
        return data
    
    def get_school_class(self, school_class_id: int) -> dict:
        session = self.Session()
        school_class = session.query(SchoolClass).filter(SchoolClass.id == school_class_id).first()
        data = school_class.serialize()
        session.close()
        return data
    
    def update_school_class(self, request: dict) -> dict:
        session = self.Session()
        school_class_id = request['id']
        school_class = session.query(SchoolClass).filter(SchoolClass.id == school_class_id).first()
        school_class.name = request.get('name', school_class.name)
        school_class.grade_id = request.get('grade_id', school_class.grade_id)
        school_class.head_teacher_id = request.get('head_teacher_id', school_class.head_teacher_id)
        session.commit()
        data = school_class.serialize()
        session.close()
        return data
    
    def delete_school_class(self, school_class_id: int) -> dict:
        session = self.Session()
        school_class = session.query(SchoolClass).filter(SchoolClass.id == school_class_id).first()
        data = school_class.serialize()
        session.delete(school_class)
        session.commit()
        session.close()
        return data
    
    
