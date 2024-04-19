from backend.models import Homework
from sqlalchemy.orm import Session, sessionmaker
import datetime

class HomeworkAdapter:
    def __init__(self, session: sessionmaker[Session]):
        self.Session = session

    def create_homework(self, request: dict) -> dict:
        session = self.Session()
        homework = Homework(
            content = request['content'],
            due_date = datetime.strptime(request['due_date'], '%Y-%m-%d').date(),
        )
        session.add(homework)
        session.commit()
        data = homework.serialize()
        session.close()
        return data
    
    def get_homeworks(self) -> list[dict]:
        session = self.Session()
        homeworks = session.query(Homework).all()
        data = [homework.serialize(depth=0) for homework in homeworks]
        session.close()
        return data
    
    def get_homework(self, homework_id: int) -> dict:
        session = self.Session()
        homework = session.query(Homework).filter(Homework.id == homework_id).first()
        data = homework.serialize()
        session.close()
        return data
    
    def update_homework(self, request: dict) -> dict:
        session = self.Session()
        homework_id = request['id']
        homework = session.query(Homework).filter(Homework.id == homework_id).first()
        homework.content = request.get('content', homework.content)
        homework.due_date = datetime.strptime(request['due_date'], '%Y-%m-%d').date() if 'due_date' in request else homework.due_date
        session.commit()
        data = homework.serialize()
        session.close()
        return data
    
    def delete_homework(self, homework_id: int) -> dict:
        session = self.Session()
        homework = session.query(Homework).filter(Homework.id == homework_id).first()
        session.delete(homework)
        session.commit()
        data = homework.serialize()
        session.close()
        return data
    
    

    
    
    
    