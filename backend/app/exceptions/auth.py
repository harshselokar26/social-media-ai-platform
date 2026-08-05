class EmailAlreadyExistsException(Exception):
    """Raised when trying to register with an email that already exists."""


class InvalidCredentialsException(Exception):
    """Raised when login credentials are invalid."""
