class ModDBException(Exception):
    def __init__(self, message):
        super().__init__(message)

class BadRequest(ModDBException):
    def __init__(self):
        super().__init__("Server cannot process the request due to malformed syntax or invalid request message framing.")

class Unauthorized(ModDBException):
    def __init__(self):
        super().__init__("Your API key/access token is incorrect.")

class Forbidden(ModDBException):
    def __init__(self):
        super().__init__("You do not have permission to perform the requested action.")

class NotFound(ModDBException):
    def __init__(self):
        super().__init__("The resource requested could not be found.")

class MethodNotAllowed(ModDBException):
    def __init__(self):
        super().__init__("The method of your request is incorrect.")

class NotAcceptable(ModDBException):
    def __init__(self):
        super().__init__("You supplied or requested an incorrect Content-Type.")

class Gone(ModDBException):
    def __init__(self):
        super().__init__("The requested resource is no longer available.")

class UnprocessableEntity(ModDBException):
    def __init__(self):
        super().__init__(" The request was well formed but unable to be followed due to semantic errors.")

class TooManyRequests(ModDBException):
    def __init__(self):
        super().__init__("You have made too many requests, inspect headers for reset time.")
