from exceptions.base import AppException

class UserNotFound(AppException):
    def __init__(self):
        super().__init__("User not found", 404)

class UserExists(AppException):
    def __init__(self):
        super().__init__("User already exists", 409)

class InvalidUserCredentials(AppException):
    def __init__(self):
        super().__init__("Invalid user credentials", 401)

