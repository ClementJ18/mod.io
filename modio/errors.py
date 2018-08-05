class modioException(Exception):
    def __init__(self, message):
        super().__init__(message)

class BadRequest(modioException):
    def __init__(self, msg):
        super().__init__(msg)

class Unauthorized(modioException):
    def __init__(self, msg):
        super().__init__(msg)

class Forbidden(modioException):
    def __init__(self, msg):
        super().__init__(msg)

class NotFound(modioException):
    def __init__(self, msg):
        super().__init__(msg)

class MethodNotAllowed(modioException):
    def __init__(self, msg):
        super().__init__(msg)

class NotAcceptable(modioException):
    def __init__(self, msg):
        super().__init__(msg)

class Gone(modioException):
    def __init__(self, msg):
        super().__init__(msg)

class UnprocessableEntity(modioException):
    def __init__(self, msg, errors):
        if errors is not None:
            msg = msg + "\n  -" + "\n  -".join([x + ": " + errors[x] for x in errors])
            
        super().__init__(msg)

class TooManyRequests(modioException):
    def __init__(self, msg, retry):
        super().__init__("{} Retry in {} seconds.".format(msg, retry))
