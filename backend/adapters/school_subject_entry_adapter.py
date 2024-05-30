from backend.models import SchoolSubjectEntry
from sqlalchemy.orm import Session, sessionmaker
from datetime import datetime, date
from backend.errors import *

class SchoolSubjectEntryAdapter:
    def __init__(self, session: sessionmaker[Session]):
        self.Session = session

    def create_school_subject_entry(self, request: dict) -> dict:
        session = self.Session()
        current_date = datetime.strptime(request['date'], '%Y-%m-%d').date() if 'date' in request else None
        school_subject_entry = SchoolSubjectEntry(
            teacher_id = request.get('teacher_id', None),
            subject_id = request['subject_id'],
            date = request['date'],
            note = request.get('note', None),
        )
        check_school_subject_entry = session.query(SchoolSubjectEntry).filter(
            SchoolSubjectEntry.date == current_date, SchoolSubjectEntry.subject_id == school_subject_entry.date).first()
        if check_school_subject_entry:
            raise SubjectEntryAlreadyExists(f"School subject entry for subject {school_subject_entry.subject_id} and date {school_subject_entry.date} already exists")
        
        session.add(school_subject_entry)
        session.commit()
        data = school_subject_entry.serialize()
        session.close()
        return data

    def get_school_subject_entries(self) -> list[dict]:
        session = self.Session()
        school_subject_entries = session.query(SchoolSubjectEntry).all()
        data = [school_subject_entry.serialize(depth=0) for school_subject_entry in school_subject_entries]
        session.close()
        return data
    
    def get_school_subject_entries_for_week(self, week: int, year: int) -> list[dict]:
        session = self.Session()
        current_year = year
        week = int(week)
        results = {}
        for i in range(7):
            try:
                current_date = date.fromisocalendar(current_year, week, i+1)
            except ValueError as e:
                current_year += 1
                week = week - 52
                current_date = date.fromisocalendar(current_year, int(week), i+1)
            school_subject_entries = session.query(SchoolSubjectEntry).filter(SchoolSubjectEntry.date == current_date).all()
            data = [school_subject_entry.serialize() for school_subject_entry in school_subject_entries]
            results[str(current_date)] = data
                
        session.close()
        return results
    
    def get_school_subject_entry(self, school_subject_entry_id: int) -> dict:
        session = self.Session()
        school_subject_entry = session.query(SchoolSubjectEntry).filter(SchoolSubjectEntry.id == school_subject_entry_id).first()
        data = school_subject_entry.serialize()
        session.close()
        return data
    
    def get_school_subject_entry_for_week(self, subject_id: int, week: int, year: int) -> list[dict]:
        session = self.Session()
        current_year = year
        results = {}
        for i in range(7):
            try:
                current_date = date.fromisocalendar(current_year, week, i+1)
            except ValueError as e:
                current_year += 1
                week = week - 52
                current_date = date.fromisocalendar(current_year, week, i+1)
            
            school_subject_entry = session.query(SchoolSubjectEntry).filter(
                SchoolSubjectEntry.subject_id == subject_id, SchoolSubjectEntry.date == current_date).first()
            if school_subject_entry:
                results[current_date] = school_subject_entry.serialize()

        session.close()
        return results
    
    def update_school_subject_entry(self, request: dict) -> dict:
        session = self.Session()
        school_subject_entry_id = request['id']
        school_subject_entry = session.query(SchoolSubjectEntry).filter(SchoolSubjectEntry.id == school_subject_entry_id).first()
        school_subject_entry.teacher_id = request.get('teacher_id', school_subject_entry.teacher_id)
        school_subject_entry.subject_id = request.get('subject_id', school_subject_entry.subject_id)
        school_subject_entry.date = request.get('date', school_subject_entry.date)
        school_subject_entry.note = request.get('note', school_subject_entry.note)
        session.commit()
        data = school_subject_entry.serialize()
        session.close()
        return data
    
    def delete_school_subject_entry(self, school_subject_entry_id: int) -> dict:
        session = self.Session()
        school_subject_entry = session.query(SchoolSubjectEntry).filter(SchoolSubjectEntry.id == school_subject_entry_id).first()
        data = school_subject_entry.serialize()
        session.delete(school_subject_entry)
        session.commit()
        session.close()
        return data
    
