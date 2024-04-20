from backend.adapters.abscence_adapter import AbsenceAdapter
from backend.adapters.access_token_adapter import AccessTokenAdapter
from backend.adapters.account_adapter import AccountAdapter
from backend.adapters.contact_adapter import ContactAdapter
from backend.adapters.homework_adapter import HomeworkAdapter
from backend.adapters.homework_status_adapter import HomeworkStatusAdapter
from backend.adapters.parent_adapter import ParentAdapter
from backend.adapters.parent_student_adapter import ParentStudentAdapter
from backend.adapters.school_class_adapter import SchoolClassAdapter
from backend.adapters.school_grade_adapter import SchoolGradeAdapter
from backend.adapters.school_subject_adapter import SchoolSubjectAdapter
from backend.adapters.school_subject_entry_adapter import SchoolSubjectEntryAdapter
from backend.adapters.school_subject_student_adapter import SchoolSubjectStudentAdapter
from backend.adapters.student_adapter import StudentAdapter
from backend.adapters.su_adapter import SuAdapter
from backend.adapters.subject_type_adapter import SubjectTypeAdapter
from backend.adapters.teacher_adapter import TeacherAdapter

from sqlalchemy.orm import Session, sessionmaker

class AdapterCollection:
    def __init__(self, session: sessionmaker[Session]):
        self.Session = session
        self.absence_adapter = AbsenceAdapter(session)
        self.access_token_adapter = AccessTokenAdapter(session)
        self.account_adapter = AccountAdapter(session)
        self.contact_adapter = ContactAdapter(session)
        self.homework_adapter = HomeworkAdapter(session)
        self.homework_status_adapter = HomeworkStatusAdapter(session)
        self.parent_adapter = ParentAdapter(session)
        self.parent_student_adapter = ParentStudentAdapter(session)
        self.school_class_adapter = SchoolClassAdapter(session)
        self.school_grade_adapter = SchoolGradeAdapter(session)
        self.school_subject_adapter = SchoolSubjectAdapter(session)
        self.school_subject_entry_adapter = SchoolSubjectEntryAdapter(session)
        self.school_subject_student_adapter = SchoolSubjectStudentAdapter(session)
        self.student_adapter = StudentAdapter(session)
        self.su_adapter = SuAdapter(session)
        self.subject_type_adapter = SubjectTypeAdapter(session)
        self.teacher_adapter = TeacherAdapter(session)