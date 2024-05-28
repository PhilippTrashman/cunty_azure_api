from backend.models import *
from backend.adapter_collection import AdapterCollection
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.schema import CreateTable
from sqlalchemy import create_engine, Text
from datetime import date
from faker import Faker
import os
import random

class SubjectEntryObject:
    def __init__(self, id: int, name: str, handle: str):
        self.id = id
        self.name = name
        self.handle = handle
        self.teachers = []

    def __str__(self) -> str:
        return f"{self.name} ({self.handle}) - {self.teachers}"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def add_teacher(self, teacher_id: int) -> None:
        self.teachers.append(teacher_id)

STUDENT1_ID = uuid.UUID('11111111-1111-1111-1111-111111111111')
STUDENT2_ID = uuid.UUID('22222222-2222-2222-2222-222222222222')
TEACHER1_ID = uuid.UUID('33333333-3333-3333-3333-333333333333')
TEACHER2_ID = uuid.UUID('44444444-4444-4444-4444-444444444444')
PARENT1_ID = uuid.UUID('55555555-5555-5555-5555-555555555555')
PARENT2_ID = uuid.UUID('66666666-6666-6666-6666-666666666666')
SU_ID = uuid.UUID('77777777-7777-7777-7777-777777777777')
HEAD_TEACHER_ID = uuid.UUID('88888888-8888-8888-8888-888888888888')

class TestDataGenerator:
    """
    Generates test data for the database
    Can Crash at times as it generates Hundreds of random accounts, who all should have unique usernames.
    This Leads to crashes if the same username or even email is generated twice.

    Just restart the script if it crashes and it should work fine.
    """
    def __init__(self, database_url: str):
        self.engine = create_engine(database_url)
        self.Session = sessionmaker(bind=self.engine)
        self.adapters = AdapterCollection(self.Session)
        self.fake = Faker()

        self.refresh_database()
        self.grade_ids = self.generate_school_grade()
        self.subject_types = self.generate_subject_types()
        self.teacher_accounts = self.generate_teacher_accounts()
        self.generate_template_accounts()
        self.school_classes: dict[int, list[int]] = self.generate_school_classes()

        self.generate_generic_data()
        print("Done")


    def refresh_database(self):
        print("Refreshing database")
        with self.engine.connect() as connection:
            try:
                # connection.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
                try:
                    Base.metadata.drop_all(bind=self.engine, checkfirst=True)
                except Exception as e:
                    print(e)

                Base.metadata.create_all(bind=self.engine)

                with open('backend/schema.sql', 'w') as f:
                    for table in Base.metadata.sorted_tables:
                        f.write(str(CreateTable(table).compile(connection)))
            except Exception as e:
                print(e)

    def generate_template_accounts(self):
        print("Generating template accounts")
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

        crud = CRUD(self.Session)
        student1_ac = crud.create(student1_ac)
        student2_ac = crud.create(student2_ac)
        teacher1_ac = crud.create(teacher1_ac)
        teacher2_ac = crud.create(teacher2_ac)
        parent1_ac = crud.create(parent1_ac)
        parent2_ac = crud.create(parent2_ac)
        su_ac = crud.create(su_ac)

        self.adapters.su_adapter.create_su({
            'account_id': str(SU_ID),
            'admin_rights': True,
            'change_subject_status': True,
            'manage_users': True,
            'manage_school': True
        })

        self.adapters.teacher_adapter.create_teacher({
            'account_id': str(TEACHER1_ID),
            'abbreviation': 'T1'
        })
        self.adapters.teacher_adapter.create_teacher({
            'account_id': str(TEACHER2_ID),
            'abbreviation': 'T2'
        })

    def generate_school_grade(self) -> List[int]:
        print("Generating school grade")
        grades = []
        for i in range(2012, 2024):
            grade = self.adapters.school_grade_adapter.create_school_grade({
                'year': i
            })
            grades.append(grade['id'])
        return grades
    
    def generate_school_classes(self) -> dict[int, list[int]]:
        print("Generating school classes")
        classes = {}
        crud = CRUD(self.Session)

        head_teacher_ac = Account(
            id = HEAD_TEACHER_ID,
            email = 'm.skibidi@test.com',
            password = 'password8',
            name = 'Michael',
            last_name = 'Skibidi',
            username = 'headteacher',
            birthday = date(1969, 4, 20)
        )
        head_teacher_ac = crud.create(head_teacher_ac)
        teacher_id = self.adapters.teacher_adapter.create_teacher({
            'account_id': str(HEAD_TEACHER_ID),
            'abbreviation': 'HT'
        })['id']
        
        for grade_id in self.grade_ids:
            class1 = self.adapters.school_class_adapter.create_school_class({
                'grade_id': grade_id,
                'name': 'A',
                'head_teacher_id': teacher_id
            })
            class2 = self.adapters.school_class_adapter.create_school_class({
                'grade_id': grade_id,
                'name': 'B',
                'head_teacher_id': teacher_id
            })
            classes[grade_id] = [class1['id'], class2['id']]
        return classes
    
    def generate_parent_accounts(self) -> list[int]:
        parents = []
        for i in range(2):
            first_name = self.fake.first_name()
            last_name = self.fake.last_name()
            username = f"{first_name}.{last_name}"
            account = {
                'email': self.fake.email(),
                'password': self.fake.password(),
                'name': first_name,
                'last_name': last_name,
                'username': username,
                'birthday': self.fake.date_of_birth().strftime('%Y-%m-%d')
            }
            try:
                acc = self.adapters.account_adapter.create_account(account)
            except Exception as e:
                continue
            parent = {
                'account_id': acc['id']
            }
            parent = self.adapters.parent_adapter.create_parent(parent)
            parents.append(parent)
        return parents

    def generate_subject_types(self) -> dict[str, SubjectEntryObject]:
        subjects = {'Mathematik': 'Ma', 'Deutsch': 'De', 'Englisch': 'En', 'Geschichte': 'Ge', 'Biologie': "Bio", 'Physik': 'Ph',
                    'Chemie': 'Ch', 'Sport': 'Sp', 'Kunst': 'Ku', 'Musik': 'Mu', 'Informatik': 'IT', 'Ethik': 'Eth', 'Religion': 'Re',
                    'Französisch': 'Fr', 'Spanisch': 'Spa', 'Latein': 'Lat', 'Politik': 'Po'}
        
        subject_types = {}
        for subject, handle in subjects.items():
            subject_type = self.adapters.subject_type_adapter.create_subject_type({
                'name': subject,
                'handle': handle
            })
            subject_types[subject] = SubjectEntryObject(subject_type['id'], subject, handle)
        return subject_types

    def generate_teacher_accounts(self) -> dict[int, list[int]]:
        teachers = {}
        for i in range(24):
            first_name = self.fake.first_name()
            last_name = self.fake.last_name()
            username = f"{first_name}.{last_name}"
            account = {
                'email': self.fake.email(),
                'password': self.fake.password(),
                'name': first_name,
                'last_name': last_name,
                'username': username,
                'birthday': self.fake.date_of_birth().strftime('%Y-%m-%d')
            }
            try:
                acc = self.adapters.account_adapter.create_account(account)
            except Exception as e:
                continue
            teacher = {
                'account_id': acc['id'],
                'abbreviation': f'{first_name[:2]}{last_name[:2]}'
            }
            try:
                teacher = self.adapters.teacher_adapter.create_teacher(teacher)
            except Exception as e:
                continue
            taught_subjects = random.sample(list(self.subject_types.values()), 3)
            for subject in taught_subjects:
                self.subject_types[subject.name].add_teacher(teacher['id'])

            teachers[teacher['id']] = taught_subjects
        return teachers

    def generate_timetable(self) -> List[int]:
        timetable = []
        for day in range(1, 6):
            subjects = random.sample(list(self.subject_types.values()), 5)
            timeslot = 1
            for subject in subjects:
                teacher = random.choice(subject.teachers)
                sub = self.adapters.school_subject_adapter.create_school_subject({
                    'teacher_id': teacher,
                    'subject_type_id': subject.id,
                    'week_day': day,
                    'timeslot': timeslot
                })
                timetable.append(sub['id'])
                timeslot += 1
                if random.choice([True, False]) and timeslot < 10 and timeslot % 2 == 0:
                    sub = self.adapters.school_subject_adapter.create_school_subject({
                        'teacher_id': teacher,
                        'subject_type_id': subject.id,
                        'week_day': day,
                        'timeslot': timeslot
                    })
                    timetable.append(sub['id'])
                    timeslot += 1
        return timetable

    def generate_generic_data(self) -> None:
        print("Generating generic accounts")
        list_usernames = []
        # list_emails = []
        template_added = False
        for grade, school_classes in self.school_classes.items():
            print(f"Generating Grade {grade} - {school_classes}")
            for school_class in school_classes:
                timetable = self.generate_timetable()
                students = []
                if not template_added:
                    student1 = {
                        'account_id': str(STUDENT1_ID),
                        'school_class_id': school_class
                    }
                    student2 = {
                        'account_id': str(STUDENT2_ID),
                        'school_class_id': school_class
                    }
                    student1 = self.adapters.student_adapter.create_student(student1)
                    student2 = self.adapters.student_adapter.create_student(student2)
                    students.append(student1)
                    students.append(student2)
                    parents = self.generate_parent_accounts()

                    for parent in parents:
                        self.adapters.parent_student_adapter.create_parent_student({
                            'parent_id': parent['id'],
                            'student_id': student1['id']
                        })
                        self.adapters.parent_student_adapter.create_parent_student({
                            'parent_id': parent['id'],
                            'student_id': student2['id']
                        })

                    template_added = True

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
                        'birthday': self.fake.date_of_birth().strftime('%Y-%m-%d')
                    }
                    try:
                        acc = self.adapters.account_adapter.create_account(account)
                    except Exception as e:
                        continue
                    
                    self.adapters.contact_adapter.create_contact({
                        'account_id': acc['id'],
                        'contact_type': 'email',
                        'contact': acc['email']
                    })

                    student = {
                        'account_id': acc['id'],
                        'school_class_id': school_class
                    }
                    student = self.adapters.student_adapter.create_student(student)
                    students.append(student)

                    parents = self.generate_parent_accounts()

                    for parent in parents:
                        self.adapters.parent_student_adapter.create_parent_student({
                            'parent_id': parent['id'],
                            'student_id': student['id']
                        })

                for student in students:
                    for subject in timetable:
                        self.adapters.school_subject_student_adapter.create_school_subject_student({
                            'student_id': student['id'],
                            'subject_id': subject
                        })



if __name__ == '__main__':
    database_url = "postgresql://postgres:1234@localhost:6971/cuntydb"
    TestDataGenerator(database_url)
    print("")
    database_url = "postgresql://test:test@localhost:6972/test_db"
    TestDataGenerator(database_url)
