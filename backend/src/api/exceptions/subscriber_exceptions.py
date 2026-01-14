from exceptions.base import AppException

class SubscriberNotFound(AppException):
    def __init__(self):
        super().__init__("Subscriber not found", 404)

class SubscriberExists(AppException):
    def __init__(self):
        super().__init__("Subscriber already exists", 409)

class SubscriberErrorDateFormat(AppException):
    def __init__(self):
        super().__init__("Invalid date format. Use ISO format.", 422)

class SubscriberEmailInvalid(AppException):
    def __init__(self):
        super().__init__("Invalid email format.", 422)