"""Errors generate by mod.io and the library."""


class modioException(Exception):
    """Base exception for the lib

    Attributes
    -----------
    code : Optional[int]
        The status code if this error was raised from a request
    ref : Optiona[int]
        The ref error code provided by mod.io
    text : str
        The unformatted text of the error
    errors : Optional[dict]
        The validation errors if any exist
    """

    def __init__(self, text, code=None, ref=None, errors=None):
        self.code = code
        self.text = text
        self.ref = ref
        self.errors = errors

        if errors:
            errors_text = "\n".join([f"{key} - {value}" for key, value in errors.items()])
            text = f"{text} \n{errors_text}"

        super().__init__(f"{code} ({ref}) - {text}")
