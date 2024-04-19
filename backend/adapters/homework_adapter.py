from backend.models import Homework, Base
from sqlalchemy.orm import Session, sessionmaker
import uuid
import datetime

class HomeworkAdapter:
    def __init__(self, session: sessionmaker[Session]):
        self.Session = session

    def create_homework(self, request: dict) -> dict:
        session = self.Session()
        homework = Homework(
            account_id = request['account_id'],
            title = request['title'],
            description = request['description'],
            due_date = datetime.strptime(request['due_date'], '%Y-%m-%d').date(),
            completed = request.get('completed', False)
        )
        session.add(homework)
        session.commit()
        data = homework.serialize()
        session.close()
        return data