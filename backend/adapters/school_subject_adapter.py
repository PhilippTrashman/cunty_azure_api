from backend.models import SchoolSubject
from sqlalchemy.orm import Session, sessionmaker

class SchoolSubjectAdapter:
    def __init__(self, session: sessionmaker[Session]):
        self.Session = session

    def create_school_subject(self, request: dict) -> dict:
        session = self.Session()
        school_subject = SchoolSubject(
            teacher_id = request['teacher_id'],
            subject_type_id = request['subject_type_id'],
            week_day = request['week_day'],
            timeslot = request['timeslot'],
        )
        session.add(school_subject)
        session.commit()
        data = school_subject.serialize()
        session.close()
        return data
    
    def get_school_subjects(self) -> list[dict]:
        session = self.Session()
        school_subjects = session.query(SchoolSubject).all()
        data = [school_subject.serialize(depth=0) for school_subject in school_subjects]
        session.close()
        return data
    
    def get_school_subject(self, school_subject_id: int) -> dict:
        session = self.Session()
        school_subject = session.query(SchoolSubject).filter(SchoolSubject.id == school_subject_id).first()
        data = school_subject.serialize()
        session.close()
        return data
    
    def update_school_subject(self, request: dict) -> dict:
        session = self.Session()
        school_subject_id = request['id']
        school_subject = session.query(SchoolSubject).filter(SchoolSubject.id == school_subject_id).first()
        school_subject.teacher_id = request.get('teacher_id', school_subject.teacher_id)
        school_subject.subject_type_id = request.get('subject_type_id', school_subject.subject_type_id)
        school_subject.week_day = request.get('week_day', school_subject.week_day)
        school_subject.timeslot = request.get('timeslot', school_subject.timeslot)
        session.commit()
        data = school_subject.serialize()
        session.close()
        return data
    
    def delete_school_subject(self, school_subject_id: int) -> dict:
        session = self.Session()
        school_subject = session.query(SchoolSubject).filter(SchoolSubject.id == school_subject_id).first()
        session.delete(school_subject)
        session.commit()
        data = school_subject.serialize()
        session.close()
        return data


