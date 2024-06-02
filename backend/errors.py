
class UserNotFound(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.status_code = 404

class UserNotStudent(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.status_code = 404

class UserNotTeacher(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.status_code = 404

class UserNotSU(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.status_code = 404

class UserNotParent(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.status_code = 404

class ParentNotFound(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.status_code = 404

class StudentCantBeSu(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.status_code = 400

class StudentCantBeTeacher(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.status_code = 400
    
class StudentCantBeParent(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.status_code = 400

class TokenNotVerified(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.status_code = 401

class UserCantAccess(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.status_code = 403

class PayloadError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.status_code = 400

class EntityNotFound(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.status_code = 404

class SubjectEntryAlreadyExists(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.status_code = 409

