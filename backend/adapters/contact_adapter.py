from backend.models import Contact, Base
from sqlalchemy.orm import Session, sessionmaker
import uuid
import datetime

class ContactAdapter:
    def __init__(self, session: sessionmaker[Session]):
        self.Session = session

    def create_contact(self, request: dict) -> dict:
        session = self.Session()
        contact = Contact(
            account_id = request['account_id'],
            contact_type = request.get('contact_type', None),
            contact = request['contact'],
        )
        session.add(contact)
        session.commit()
        data = contact.serialize()
        session.close()
        return data
    
    def get_contacts(self) -> list[dict]:
        session = self.Session()
        contacts = session.query(Contact).all()
        data = [contact.serialize(depth=0) for contact in contacts]
        session.close()
        return data
    
    def get_contact(self, contact_id: int) -> dict:
        session = self.Session()
        contact = session.query(Contact).filter(Contact.id == contact_id).first()
        data = contact.serialize()
        session.close()
        return data
    
    def get_contact_by_user(self, user_id: uuid.UUID) -> list[dict]:
        session = self.Session()
        contacts = session.query(Contact).filter(Contact.account_id == user_id).all()
        data = [contact.serialize() for contact in contacts]
        session.close()
        return data
    
    def update_contact(self, request: dict) -> dict:
        session = self.Session()
        contact_id = request['id']
        contact = session.query(Contact).filter(Contact.id == contact_id).first()
        contact.account_id = request.get('account_id', contact.account_id)
        contact.contact_type = request.get('contact_type', contact.contact_type)
        contact.contact = request.get('contact', contact.contact)
        session.commit()
        data = contact.serialize()
        session.close()
        return data
    
    def delete_contact(self, contact_id: int) -> dict:
        session = self.Session()
        contact = session.query(Contact).filter(Contact.id == contact_id).first()
        data = contact.serialize()
        session.delete(contact)
        session.commit()
        session.close()
        return data