class modioException(Exception):
    """Base exception for the lib"""
    def __init__(self, msg):
        super().__init__(msg)

class BadRequest(modioException):
    """Server cannot process the request due to malformed syntax or invalid request message framing."""
    def __init__(self, msg):
        super().__init__(msg)

class Unauthorized(modioException):
    """Your API key/access token is incorrect."""
    def __init__(self, msg):
        super().__init__(msg)

class Forbidden(modioException):
    """You do not have permission to perform the requested action."""
    def __init__(self, msg):
        super().__init__(msg)

class NotFound(modioException):
    """The resource requested could not be found."""
    def __init__(self, msg):
        super().__init__(msg)

class MethodNotAllowed(modioException):
    """The method of your request is incorrect."""
    def __init__(self, msg):
        super().__init__(msg)

class NotAcceptable(modioException):
    """You supplied or requested an incorrect Content-Type."""
    def __init__(self, msg):
        super().__init__(msg)

class Gone(modioException):
    """The requested resource is no longer available."""
    def __init__(self, msg):
        super().__init__(msg)

class UnprocessableEntity(modioException):
    """The request was well formed but unable to be followed due to semantic errors.

    Attributes
    -----------
    errors : dict
        Dict of parameters that returned an error and the error they returned
    """
    def __init__(self, msg, errors):
        if errors:
            msg = msg + "\n  -" + "\n  -".join([x + ": " + errors[x] for x in errors])

        self.errors = errors
        super().__init__(msg)

class TooManyRequests(modioException):
    """You have made too many requests, inspect headers for reset time"""
    def __init__(self, msg, retry):
        super().__init__("{}. You need to sleep for {} seconds".format(msg, retry))
