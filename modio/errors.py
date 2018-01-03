class ModDBException(Exception):
    def __init__(self, message):
        super().__init__(message)

class BadRequest(ModDBException):
    def __init__(self, msg):
        super().__init__(msg)

class Unauthorized(ModDBException):
    def __init__(self, msg):
        super().__init__(msg)

class Forbidden(ModDBException):
    def __init__(self, msg):
        super().__init__(msg)

class NotFound(ModDBException):
    def __init__(self, msg):
        super().__init__(msg)

class MethodNotAllowed(ModDBException):
    def __init__(self, msg):
        super().__init__(msg)

class NotAcceptable(ModDBException):
    def __init__(self, msg):
        super().__init__(msg)

class Gone(ModDBException):
    def __init__(self, msg):
        super().__init__(msg)

class UnprocessableEntity(ModDBException):
    def __init__(self, msg, errors):
        msg = msg + "\n  -" + "\n  -".join([x + ": " + errors[x] for x in errors])
        super().__init__(msg)

class TooManyRequests(ModDBException):
    def __init__(self, msg):
        super().__init__(msg)
