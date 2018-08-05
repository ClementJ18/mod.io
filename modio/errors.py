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
        if errors is not None:
            msg = msg + "\n  -" + "\n  -".join([x + ": " + errors[x] for x in errors])
            
        super().__init__(msg)

class TooManyRequests(ModDBException):
    def __init__(self, msg, retry):
        super().__init__("{} Retry in {} seconds.".format(msg, retry))
