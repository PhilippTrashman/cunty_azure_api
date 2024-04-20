from backend.models import *
from backend.adapter_collection import AdapterCollection
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.schema import CreateTable
from sqlalchemy import create_engine, Text
from datetime import date
from faker import Faker
import os
import random

STUDENT1_ID = uuid.UUID('11111111-1111-1111-1111-111111111111')
STUDENT2_ID = uuid.UUID('22222222-2222-2222-2222-222222222222')
TEACHER1_ID = uuid.UUID('33333333-3333-3333-3333-333333333333')
TEACHER2_ID = uuid.UUID('44444444-4444-4444-4444-444444444444')
PARENT1_ID = uuid.UUID('55555555-5555-5555-5555-555555555555')
PARENT2_ID = uuid.UUID('66666666-6666-6666-6666-666666666666')
SU_ID = uuid.UUID('77777777-7777-7777-7777-777777777777')

class TestDataGenerator:
    def __init__(self, database_url: str):
        self.engine = create_engine(database_url)
        self.Session = sessionmaker(bind=self.engine)
        self.adapters = AdapterCollection(self.Session)
        self.fake = Faker('de_DE')

    def refresh_database(self):
        with self.engine.connect() as connection:
            try:
                connection.execute(Text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";'))
                try:
                    Base.medata.drop_all(bind=self.engine, checkfirst=True)
                except Exception as e:
                    print(e)

                Base.metadata.create_all(bind=self.engine)

                with open('backend/schema.sql', 'w') as f:
                    for table in Base.metadata.sorted_tables:
                        f.write(str(CreateTable(table).compile(connection)))
            except Exception as e:
                print(e)

    def generate_template_accountss(self):
        student1_ac = Account(
            id = STUDENT1_ID,
            email = 'student1@test.com',
            password = 'password1',
            name = 'Test',
            last_name = 'Student1',
            username = 'testStudent1',
            birthday = date(2000, 1, 1)
        )
        student2_ac = Account(
            id = STUDENT2_ID,
            email = 'student2@test.com',
            password = 'password2',
            name = 'Test',
            last_name = 'Student2',
            username = 'testStudent2',
            birthday = date(2000, 1, 1)
        )
        teacher1_ac = Account(
            id = TEACHER1_ID,
            email = 'teacher1@test.com',
            password = 'password3',
            name = 'Test',
            last_name = 'Teacher1',
            username = 'testTeacher1',
            birthday = date(2000, 1, 1)
        )
        teacher2_ac = Account(
            id = TEACHER2_ID,
            email = 'teacher2@test.com',
            password = 'password4',
            name = 'Test',
            last_name = 'Teacher2',
            username = 'testTeacher2',
            birthday = date(2000, 1, 1)
        )
        parent1_ac = Account(
            id = PARENT1_ID,
            email = 'parent1@test.com',
            password = 'password5',
            name = 'Test',
            last_name = 'Parent1',
            username = 'testParent1',
            birthday = date(2000, 1, 1)
        )
        parent2_ac = Account(
            id = PARENT2_ID,
            email = 'parent2@test.com',
            password = 'password6',
            name = 'Test',
            last_name = 'Parent2',
            username = 'testParent2',
            birthday = date(2000, 1, 1)
        )
        su_ac = Account(
            id = SU_ID,
            email = 'su@test.com',
            password = 'password7',
            name = 'Test',
            last_name = 'SU',
            username = 'testSU',
            birthday = date(2000, 1, 1)
        )

        session = self.Session()
        crud = CRUD(session)
        student1_ac = crud.create(student1_ac)
        student2_ac = crud.create(student2_ac)
        teacher1_ac = crud.create(teacher1_ac)
        teacher2_ac = crud.create(teacher2_ac)
        parent1_ac = crud.create(parent1_ac)
        parent2_ac = crud.create(parent2_ac)
        su_ac = crud.create(su_ac)

    def generate_school_grade(self) -> int:
        grade = self.adapters.school_grade_adapter.create_school_grade({
            'year': 2021
        })
        return grade['id']
    
    def generate_school_classes(self, grade_id: int) -> list[int]:
        class1 = self.adapters.school_class_adapter.create_school_class({
            'grade_id': grade_id,
            'name': 'A'
        })
        class2 = self.adapters.school_class_adapter.create_school_class({
            'grade_id': grade_id,
            'name': 'B'
        })
        return class1['id'], class2['id']

    def generate_generic_accounts(self, school_classes: list[int]):
        list_usernames = []
        students = []
        for school_class in school_classes:
            for i in range(10):
                first_name = self.fake.first_name()
                last_name = self.fake.last_name()
                username = f"{first_name}.{last_name}"
                if username in list_usernames:
                    continue
                list_usernames.append(username)
                account = {
                    'email': self.fake.email(),
                    'password': self.fake.password(),
                    'name': first_name,
                    'last_name': last_name,
                    'username': username,
                    'birthday': self.fake.date_of_birth()
                }
                acc = self.adapters.account_adapter.create_account(account)
                student = {
                    'account_id': acc['id'],
                    'school_class_id': school_class
                }
                student = self.adapters.student_adapter.create_student(student)
                students.append(student)
