import itertools
from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, Boolean, CheckConstraint
from sqlalchemy.orm import relationship, Session, declarative_base
from sqlalchemy.dialects.postgresql import UUID


from typing import List
import uuid


Base = declarative_base()

class CRUD:

    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, instance: Base) -> Base: #type: ignore
        session = self.session()
        try:
            session.add(instance)
            session.commit()
            return instance
        except Exception as e:
            print(e)
            session.rollback()
            raise e
        finally:
            session.close()

    def read(self, model: Base, instance_id: uuid.UUID | int) -> Base: #type: ignore
        session = self.session()
        try:
            return session.query(model).filter(model.id == instance_id).first()
        except Exception as e:
            print(e)
            session.rollback()
            raise e
        finally:
            session.close()
    
    def read_all(self, model: Base) -> List[Base]: #type: ignore
        session = self.session()
        try:
            return session.query(model).all()
        except Exception as e:
            print(e)
            session.rollback()
            raise e
        finally:
            session.close()

    def update(self, model: Base, instance_id: uuid.UUID | int, **kwargs) -> Base: #type: ignore
        session = self.session()
        try:
            instance = session.query(model).filter(model.id == instance_id).first()
            for key, value in kwargs.items():
                setattr(instance, key, value)
            session.commit()
            return instance
        except Exception as e:
            print(e)
            session.rollback()
            raise e
        finally:
            session.close()

    def delete(self, model: Base, instance_id: uuid.UUID | int) -> None: #type: ignore
        session = self.session()
        try:
            instance = session.query(model).filter(Account.id == instance_id).first()
            session.delete(instance)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()


class SchoolGrade(Base):
    __tablename__ = "school_grade"

    id = Column(Integer, primary_key=True)
    year = Column(Integer, nullable=False, unique=True)

    classes = relationship("SchoolClass", back_populates="grade")

    def __repr__(self) -> str:
        return f"SchoolGrade(id={self.id}, year={self.year})"
    
    def serialize(self, depth=1) -> dict:
        data = {
            "id": self.id,
            "year": self.year
        }

        if depth > 0:
            data.update({
                "classes": {c.id: c.serialize(depth-1) for c in self.classes}
            })

        return data

# Works
class SchoolClass(Base):
    __tablename__ = "school_class"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    grade_id = Column(Integer, ForeignKey("school_grade.id"), nullable=False)
    head_teacher_id = Column(Integer, ForeignKey("teacher.id"))

    grade = relationship("SchoolGrade", back_populates="classes")
    head_teacher = relationship("Teacher", back_populates="school_class")
    students = relationship("Student", back_populates="school_class")

    def __repr__(self) -> str:
        return f"SchoolClass(id={self.id}, name={self.name}, grade_id={self.grade_id}, head_teacher_id={self.head_teacher_id})"

    def serialize(self, depth=1) -> dict:
        data = {
            "id": self.id,
            "name": self.name,
            "grade_id": self.grade_id,
            "head_teacher_id": self.head_teacher_id if self.head_teacher_id else "N/A",
            "head_teacher_name": self.head_teacher.account.name + " " + self.head_teacher.account.last_name if self.head_teacher_id else "N/A",
            "head_teacher_abbreviation": self.head_teacher.abbreviation if self.head_teacher_id else "N/A"
        }

        if depth > 0:
            data.update({
                "grade": self.grade.serialize(depth-1),
                "head_teacher": self.head_teacher.serialize(depth-1) if self.head_teacher_id else None,
                "students": {s.id: s.serialize(depth-1) for s in self.students}
            })
        
        return data

class Contact(Base):
    __tablename__ = "contact"

    id = Column(Integer, primary_key=True)
    account_id = Column(UUID(as_uuid=True), ForeignKey("account.id"), nullable=False)
    contact_type = Column(String)
    contact = Column(String, nullable=False)

    account = relationship("Account", back_populates="contacts")

    def __repr__(self) -> str:
        return f"Contact(id={self.id}, account_id={self.account_id}, contact_type={self.contact_type}, contact={self.contact})"

    def serialize(self, depth=1) -> dict:
        data = {
            "id": self.id,
            # "account_id": self.account_id,
            "contact_type": self.contact_type,
            "contact": self.contact
        }

        if depth > 0:
            data.update({
                "account": self.account.serialize(depth-1)
            })

        return data
    
# Works
class ParentStudent(Base):
    __tablename__ = "parent_student"
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey("parent.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("student.id"), nullable=False)

    parent = relationship("Parent", back_populates="children")
    student = relationship("Student", back_populates="parents")

    def __repr__(self) -> str:
        return f"ParentStudent(id={self.id}, parent_id={self.parent_id}, student_id={self.student_id})"
    
    def serialize(self, depth=1, from_student=False, from_parent=False) -> dict:
        data = {
            "id": self.id,
        }

        if depth > 0 and not from_student and not from_parent:
            data.update({
                "parent": self.parent.serialize(depth-1),
                "student": self.student.serialize(depth-1)
            })
        
        if from_student:
            data.update({
                "parent": self.parent.serialize(depth-1)
            })
        
        if from_parent:
            data.update({
                "student": self.student.serialize(depth-1)
            })

        return data
    
# Works
class Parent(Base):
    __tablename__ = "parent"
    id = Column(Integer, primary_key=True)
    account_id = Column(UUID(as_uuid=True), ForeignKey("account.id"), unique=True, nullable=False)
    children = relationship("ParentStudent", back_populates="parent", cascade="all, delete-orphan, delete")
    account = relationship("Account", back_populates="parent")

    def __repr__(self) -> str:
        return f"Parent(id={self.id}, account_id={self.account_id})"
    
    def serialize(self, depth=1, from_account = False) -> dict:
        data = {
            "id": self.id,
        }

        if depth > 0 or from_account:
            data.update({
                "children": {c.id: c.serialize(depth-1, False, True) for c in self.children}
            })
        
        if not from_account:
            data.update({
                "account": self.account.serialize(depth-1)
            })

        return data

# Works
class Student(Base):
    __tablename__ = "student"
    id = Column(Integer, primary_key=True)
    account_id = Column(UUID(as_uuid=True), ForeignKey("account.id"), nullable=False, unique=True)
    school_class_id = Column(Integer, ForeignKey("school_class.id"))

    parents = relationship("ParentStudent", back_populates="student", cascade="all, delete-orphan, delete")
    account = relationship("Account", back_populates="student")
    school_class = relationship("SchoolClass", back_populates="students")
    school_subjects = relationship("SchoolSubjectStudent", back_populates="student", cascade="all, delete-orphan, delete")
    homework_status = relationship("HomeworkStatus", back_populates="student", cascade="all, delete-orphan, delete")

    def __repr__(self) -> str:
        return f"Student(id={self.id}, account_id={self.account_id}, school_class_id={self.school_class_id})"
    
    def serialize(self, depth=1, from_account = False) -> dict:
        data = {
            "id": self.id,
            "school_class_id": self.school_class_id,
        }

        if depth > 0 or from_account:
            data.update({
                "parents": {p.id: p.serialize(depth-1, True) for p in self.parents},
                "school_subjects": {
                    day: {
                        timeslot: [s.serialize(depth-1, True) for s in subjects]
                        for timeslot, subjects in itertools.groupby(
                            sorted(day_subjects, key=lambda s: s.subject.timeslot), 
                            key=lambda s: s.subject.timeslot
                        )
                    } 
                    for day, day_subjects in itertools.groupby(
                        sorted(self.school_subjects, key=lambda s: s.subject.week_day), 
                        key=lambda s: s.subject.week_day
                    )
                } if self.school_subjects else None,
                "homework_status": {h.id: h.serialize(depth-1, True) for h in self.homework_status}
            })
        if from_account == False:
            data.update({
                "account": self.account.serialize(depth-1)
            })

        return data
    
# Works
class Teacher(Base):
    __tablename__ = "teacher"
    id = Column(Integer, primary_key=True)
    account_id = Column(UUID(as_uuid=True), ForeignKey("account.id"), nullable=False, unique=True)
    abbreviation = Column(String, nullable=False, unique=True)

    school_class = relationship("SchoolClass", back_populates="head_teacher")
    school_subjects = relationship("SchoolSubject", back_populates="teacher")
    school_subject_entries = relationship("SchoolSubjectEntry", back_populates="teacher")

    account = relationship("Account", back_populates="teacher")

    def __repr__(self) -> str:
        return f"Teacher(id={self.id}, account_id={self.account_id})"
    
    def serialize(self, depth=1, from_account = False) -> dict:
        data = {
            "id": self.id,
        }

        if depth > 0 or from_account:
            data.update({
                "school_class": {c.id: c.serialize(depth-1) for c in self.school_class} if self.school_class else None,
                "school_subjects": {
                    day: {
                        timeslot: [s.serialize(depth-1) for s in subjects]
                        for timeslot, subjects in itertools.groupby(
                            sorted(day_subjects, key=lambda s: s.timeslot), 
                            key=lambda s: s.timeslot
                        )
                    } 
                    for day, day_subjects in itertools.groupby(
                        sorted(self.school_subjects, key=lambda s: s.week_day), 
                        key=lambda s: s.week_day
                    )
                } if self.school_subjects else None,
            })
        
        if not from_account:
            data.update({
                "account": self.account.serialize(depth-1)
            })

        return data
    
# Works
class Su(Base):
    __tablename__ = "su"
    id = Column(Integer, primary_key=True)
    account_id = Column(UUID(as_uuid=True), ForeignKey("account.id"), nullable=False, unique=True)
    admin_rights = Column(Boolean, nullable=False, default=False)
    change_subject_status = Column(Boolean, nullable=False, default=False)
    manage_users = Column(Boolean, nullable=False, default=False)
    manage_school = Column(Boolean, nullable=False, default=False)

    account = relationship("Account", back_populates="su")

    def __repr__(self) -> str:
        return f"Su(id={self.id}, account_id={self.account_id}, admin_rights={self.admin_rights}, change_subject_status={self.change_subject_status}, manage_users={self.manage_users}, manage_school={self.manage_school})"

    def serialize(self, depth=1, from_account = False) -> dict:
        data = {
            "id": self.id,
            "admin_rights": self.admin_rights,
            "change_subject_status": self.change_subject_status,
            "manage_users": self.manage_users,
            "manage_school": self.manage_school
        }

        if depth > 0 or not from_account:
            data.update({
                "account": self.account.serialize(depth-1)
            })

        return data

# Works
class Account(Base):
    __tablename__ = "account"

    id = Column(UUID(as_uuid=True), 
                primary_key=True, 
                unique=True, 
                default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False)
    birthday = Column(Date)
    secret = Column(UUID(as_uuid=True), default=uuid.uuid4, nullable=False)

    contacts = relationship("Contact", back_populates="account", cascade="all, delete-orphan, delete")
    student = relationship("Student", back_populates="account", uselist=False, cascade="all, delete-orphan, delete")
    parent = relationship("Parent", back_populates="account", uselist=False, cascade="all, delete-orphan, delete")
    teacher = relationship("Teacher", back_populates="account", uselist=False, cascade="all, delete-orphan, delete")
    su = relationship("Su", back_populates="account", uselist=False, cascade="all, delete-orphan, delete")

    absences = relationship("Absence", back_populates="account", cascade="all, delete-orphan, delete")
    access_tokens = relationship("AccessToken", back_populates="account", cascade="all, delete-orphan, delete")

    def __repr__(self) -> str:
        return f"Account(id={self.id}, email={self.email}, password={self.password}, name={self.name}, last_name={self.last_name}, username={self.username}, birthday={self.birthday})"
    
    def serialize(self, depth=1) -> dict:
        data = {
            "id": str(self.id),
            "name": self.name,
            "last_name": self.last_name,
            "birthday": str(self.birthday),
            "username": self.username,
        }

        if depth > 0:
            data.update({
                "username": self.username,
                "email": self.email,
                "contacts": {c.id: c.serialize(depth-1) for c in self.contacts},
                "student": self.student.serialize(depth-1, True) if self.student else None,
                "parent": self.parent.serialize(depth-1, True) if self.parent else None,
                "teacher": self.teacher.serialize(depth-1, True) if self.teacher else None,
                "su": self.su.serialize(depth-1, True) if self.su else None,
                "absences": {a.id: a.serialize(depth-1) for a in self.absences},
            })

        return data

class Absence(Base):
    __tablename__ = "absence"

    id = Column(Integer, primary_key=True)
    account_id = Column(UUID(as_uuid=True), ForeignKey("account.id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime)
    date = Column(Date, nullable=False)
    reason = Column(String)
    excused = Column(Boolean, nullable=False, default=False)

    account = relationship("Account", back_populates="absences")

    def __repr__(self) -> str:
        return f"Absence(id={self.id}, account_id={self.account_id}, start_time={self.start_time}, end_time={self.end_time}, date={self.date}, reason={self.reason}, excused={self.excused})"

    def serialize(self, depth=1) -> dict:
        data = {
            "id": self.id,
            "start_time": str(self.start_time),
            "end_time": str(self.end_time) if self.end_time else None,
            "date": str(self.date),
            "reason": self.reason,
            "excused": self.excused
        }

        if depth > 0:
            data.update({
                "account": self.account.serialize(depth-1)
            })

        return data

class SubjectType(Base):
    __tablename__ = "subject_type"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    handle = Column(String, nullable=False, unique=True)

    subjects = relationship("SchoolSubject", back_populates="subject_type")

    def __repr__(self) -> str:
        return f"SubjectType(id={self.id}, name={self.name})"
    
    def serialize(self, depth=1) -> dict:
        data = {
            "id": self.id,
            "name": self.name,
            "handle": self.handle
        }

        if depth > 0:
            data.update({
                "subjects": {s.id: s.serialize(depth-1) for s in self.subjects}
            })

        return data

class SchoolSubject(Base):
    __tablename__ = "school_subject"

    id = Column(Integer, primary_key=True)
    teacher_id = Column(Integer, ForeignKey("teacher.id"))
    subject_type_id = Column(Integer, ForeignKey("subject_type.id"), nullable=False)
    week_day = Column(Integer, nullable=False)
    timeslot = Column(Integer, nullable=False)

    __table_args__ = (
        CheckConstraint('week_day >= 1 AND week_day <= 6', name='check_week_day'),
        CheckConstraint('timeslot >= 1', name='check_timeslot'),
    )

    teacher = relationship("Teacher", back_populates="school_subjects", lazy="joined")
    students = relationship("SchoolSubjectStudent", back_populates="subject", lazy="joined")
    subject_type = relationship("SubjectType", back_populates="subjects", lazy="joined")
    subject_entries = relationship("SchoolSubjectEntry", back_populates="subject", lazy="joined")

    def __repr__(self) -> str:
        return f"SchoolSubject(id={self.id}, teacher_id={self.teacher_id}, subject_type_id={self.subject_type_id}, weekday={self.weekday}, timeslot={self.timeslot})"

    def serialize(self, depth=1) -> dict:
        data = {
            "id": self.id,
            "week_day": self.week_day,
            "timeslot": self.timeslot,
            "subject": self.subject_type.name,
            "teacher_id": self.teacher_id,
            "teacher": self.teacher.account.name + " " + self.teacher.account.last_name,
            "teacher_abbreviation": self.teacher.abbreviation if self.teacher.abbreviation else "N/A"
        }

        if depth > 0:
            data.update({
                "teacher": self.teacher.serialize(depth-1),
                "students": {s.id: s.serialize(depth-1, False, False) for s in self.students},
                "subject_type": self.subject_type.serialize(depth-1),
                # "subject_entries": {s.id: s.serialize(depth-1) for s in self.subject_entries}
            })

        return data
    
class SchoolSubjectStudent(Base):
    __tablename__ = "school_subject_student"

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("student.id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("school_subject.id"), nullable=False)

    student = relationship("Student", back_populates="school_subjects", lazy="joined")
    subject = relationship("SchoolSubject", back_populates="students", lazy="joined")

    def __repr__(self) -> str:
        return f"SchoolSubjectStudent(id={self.id}, student_id={self.student_id}, subject_id={self.subject_id})"

    def serialize(self, depth=1, from_student = False, from_subject = False) -> dict:
        if not from_student and not from_subject:
            data = {
                "id": self.id,
                "subject": self.subject.serialize(depth-1),
                "student": self.student.serialize(depth-1)
            }

        elif from_student and not from_subject:
            data = {
                "subject": self.subject.serialize(depth-1)
            }

        elif from_subject and not from_student:
            data = {
                "student": self.student.serialize(depth-1)
            }
        else:
            raise ValueError("Cannot serialize from both student and subject")

        return data

class SchoolSubjectEntry(Base):
    __tablename__ = "school_subject_entry"

    id = Column(Integer, primary_key=True)
    teacher_id = Column(Integer, ForeignKey("teacher.id"))
    subject_id = Column(Integer, ForeignKey("school_subject.id"), nullable=False)
    date = Column(Date, nullable=False)
    note = Column(String)


    teacher = relationship("Teacher", back_populates="school_subject_entries", lazy="joined")
    subject = relationship("SchoolSubject", back_populates="subject_entries", lazy="joined")
    homework = relationship("Homework", back_populates="subject_entries", lazy="joined")

    def __repr__(self) -> str:
        return f"SchoolSubjectEntry(id={self.id}, teacher_id={self.teacher_id}, subject_id={self.subject_id}, date={self.date}, note={self.note})"

    def serialize(self, depth=1) -> dict:
        data = {
            "id": self.id,
            "date": str(self.date),
            "note": self.note
        }

        # if depth > 0:
        #     data.update({
        #         "teacher": self.teacher.serialize(depth-1),
        #         "subject": self.subject.serialize(depth-1),
        #         "homework": {h.id: h.serialize(depth-1) for h in self.homework}
        #     })

        return data

class Homework(Base):
    __tablename__ = "homework"

    id = Column(Integer, primary_key=True)
    subject_entry = Column(Integer, ForeignKey("school_subject_entry.id"), nullable=False)
    content = Column(String, nullable=False)
    due_date = Column(Date, nullable=False)

    subject_entries = relationship("SchoolSubjectEntry", back_populates="homework")
    status = relationship("HomeworkStatus", back_populates="homework")

    def __repr__(self) -> str:
        return f"Homework(id={self.id}, subject_entry={self.subject_entry}, content={self.content}, due_date={self.due_date})"

    def serialize(self, depth=1) -> dict:
        data = {
            "id": self.id,
            "content": self.content,
            "due_date": self.due_date
        }

        # if depth > 0:
        #     data.update({
        #         "subject_entries": {s.id: s.serialize(depth-1) for s in self.subject_entries},
        #         "status": {s.id: s.serialize(depth-1) for s in self.status}
        #     })

        return data
    
class HomeworkStatus(Base):
    __tablename__ = "homework_status"

    id = Column(Integer, primary_key=True)
    homework_id = Column(Integer, ForeignKey("homework.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("student.id"), nullable=False)
    status = Column(Boolean, nullable=False, default=False)

    homework = relationship("Homework", back_populates="status")
    student = relationship("Student", back_populates="homework_status")

    def __repr__(self) -> str:
        return f"HomeworkStatus(id={self.id}, homework_id={self.homework_id}, student_id={self.student_id}, status={self.status})"

    def serialize(self, depth=1, from_student=False) -> dict:
        data = {
            "id": self.id,         
            "status": self.status
        }

        if depth > 0:
            data.update({
                "homework": self.homework.serialize(depth-1),
                "student": self.student.serialize(depth-1)
            })
        
        if from_student:
            data.update({
                "homework": self.homework.serialize(depth-1)
            })

        return data

# TODO: Implement User Authentication, Secret should be stored in database
class AccessToken(Base):
    __tablename__ = "access_token"

    id = Column(UUID(as_uuid=True), primary_key=True)
    account_id = Column(UUID(as_uuid=True), ForeignKey("account.id"), nullable=False)
    expiration_date = Column(DateTime, nullable=False)
    creation_date = Column(DateTime, nullable=False)
    token = Column(String, nullable=False)

    account = relationship("Account", back_populates="access_tokens")

    def __repr__(self) -> str:
        return f"AccessToken(id={self.id}, account_id={self.account_id}, expiration_date={self.expiration_date}, creation_date={self.creation_date})"

    def serialize(self, depth=1) -> dict:
        data = {
            "id": self.id,
            "account_id": self.account_id,
            "expiration_date": self.expiration_date,
            "creation_date": self.creation_date
        }

        if depth > 0:
            data.update({
                "account": self.account.serialize(depth-1)
            })

        return data
    
