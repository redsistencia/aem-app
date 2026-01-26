from exceptions.base import AppException

class ActivityNotFound(AppException):
    def __init__(self):
        super().__init__("Activity not found", 404)

class ActivityErrorDateFormat(AppException):
    def __init__(self):
        super().__init__("Invalid date format. Use ISO format.", 422)

class ActivityTitleRequired(AppException):
    def __init__(self):
        super().__init__("Title is required", 422)

class ActivityTitleTooLong(AppException):
    def __init__(self):
        super().__init__("Title too long", 422)