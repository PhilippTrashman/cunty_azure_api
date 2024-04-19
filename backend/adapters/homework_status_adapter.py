from backend.models import HomeworkStatus
from sqlalchemy.orm import Session, sessionmaker
import datetime

class HomeworkStatusAdapter:
    def __init__(self, session: sessionmaker[Session]):
        self.Session = session

    def create_homework_status(self, request: dict) -> dict:
        session = self.Session()
        homework_status = HomeworkStatus(
            student_id = request['student_id'],
            homework_id = request['homework_id'],
            status = request['status'],
        )
        session.add(homework_status)
        session.commit()
        data = homework_status.serialize()
        session.close()
        return data
    
    def get_homework_statuses(self) -> list[dict]:
        session = self.Session()
        homework_statuses = session.query(HomeworkStatus).all()
        data = [homework_status.serialize(depth=0) for homework_status in homework_statuses]
        session.close()
        return data
    
    def get_homework_status(self, homework_status_id: int) -> dict:
        session = self.Session()
        homework_status = session.query(HomeworkStatus).filter(HomeworkStatus.id == homework_status_id).first()
        data = homework_status.serialize()
        session.close()
        return data
    
    def get_homework_status_by_student(self, student_id: int) -> list[dict]:
        session = self.Session()
        homework_statuses = session.query(HomeworkStatus).filter(HomeworkStatus.student_id == student_id).all()
        data = [homework_status.serialize() for homework_status in homework_statuses]
        session.close()
        return data
    
    def get_homework_status_by_homework(self, homework_id: int) -> list[dict]:
        session = self.Session()
        homework_statuses = session.query(HomeworkStatus).filter(HomeworkStatus.homework_id == homework_id).all()
        data = [homework_status.serialize() for homework_status in homework_statuses]
        session.close()
        return data
    
    def update_homework_status(self, request: dict) -> dict:
        session = self.Session()
        homework_status_id = request['id']
        homework_status = session.query(HomeworkStatus).filter(HomeworkStatus.id == homework_status_id).first()
        homework_status.student_id = request.get('student_id', homework_status.student_id)
        homework_status.homework_id = request.get('homework_id', homework_status.homework_id)
        homework_status.status = request.get('status', homework_status.status)
        session.commit()
        data = homework_status.serialize()
        session.close()
        return data
    
    def delete_homework_status(self, homework_status_id: int) -> dict:
        session = self.Session()
        homework_status = session.query(HomeworkStatus).filter(HomeworkStatus.id == homework_status_id).first()
        session.delete(homework_status)
        session.commit()
        data = homework_status.serialize()
        session.close()
        return data
    
    def delete_homework_status_by_student(self, student_id: int) -> list[dict]:
        session = self.Session()
        homework_statuses = session.query(HomeworkStatus).filter(HomeworkStatus.student_id == student_id).all()
        data = [homework_status.serialize() for homework_status in homework_statuses]
        for homework_status in homework_statuses:
            session.delete(homework_status)
        session.commit()
        session.close()
        return data
    
