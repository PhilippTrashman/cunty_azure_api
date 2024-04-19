from backend.models import Absence, Base
from sqlalchemy.orm import Session, sessionmaker
import uuid
import datetime

class AbsenceAdapter:
    def __init__(self, session: sessionmaker[Session]):
        self.Session = session

    def create_abscence(self, request: dict) -> dict:
        session = self.Session()
        abscence = Absence(
            account_id = request['account_id'],
            date = datetime.strptime(request['date'], '%Y-%m-%d').date(),
            start_time = request['start_time'],
            end_time = request.get('end_time', None),
            reason = request['reason'],
            excused = request.get('excused', False)
        )
        session.add(abscence)
        session.commit()
        data = abscence.serialize()
        session.close()
        return data

    def get_abscences(self) -> list[dict]:
        session = self.Session()
        abscences = session.query(Absence).all()
        data = [abscence.serialize(depth=0) for abscence in abscences]
        session.close()
        return data
    
    def get_abscence(self, abscence_id: int) -> dict:
        session = self.Session()
        abscence = session.query(Absence).filter(Absence.id == abscence_id).first()
        data = abscence.serialize()
        session.close()
        return data
    
    def get_abscence_by_user(self, user_id: uuid.UUID) -> list[dict]:
        session = self.Session()
        abscences = session.query(Absence).filter(Absence.account_id == user_id).all()
        data = [abscence.serialize() for abscence in abscences]
        session.close()
        return data
    
    def get_abscence_by_user_date(self, user_id: uuid.UUID, date: datetime.date) -> list[dict]:
        session = self.Session()
        abscences = session.query(Absence).filter(Absence.account_id == user_id, Absence.date == date).all()
        data = [abscence.serialize() for abscence in abscences]
        session.close()
        return data

    def update_abscence(self, request: dict) -> dict:
        session = self.Session()
        abscence_id = request['id']
        date = datetime.strptime(request['date'], '%Y-%m-%d').date() if 'date' in request else abscence.date
        abscence = session.query(Absence).filter(Absence.id == abscence_id).first()
        abscence.account_id = request.get('account_id', abscence.account_id)
        abscence.date = date 
        abscence.start_time = request.get('start_time', abscence.start_time)
        abscence.end_time = request.get('end_time', abscence.end_time)
        abscence.reason = request.get('reason', abscence.reason)
        abscence.excused = request.get('excused', abscence.excused)
        session.commit()
        data = abscence.serialize()
        session.close()
        return data
    
    def delete_abscence(self, abscence_id: int) -> dict:
        session = self.Session()
        abscence = session.query(Absence).filter(Absence.id == abscence_id).first()
        data = abscence.serialize()
        session.delete(abscence)
        session.commit()
        session.close()
        return data
    




