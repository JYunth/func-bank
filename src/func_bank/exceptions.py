class FuncBankException(Exception):
    """Base exception for func_bank errors."""

    pass


class ValidationError(FuncBankException):
    """Raised when input validation fails."""

    pass


class DatabaseError(FuncBankException):
    """Raised when database operations fail."""

    pass


class AuthenticationError(FuncBankException):
    """Raised when authentication fails."""

    pass


class AuthorizationError(FuncBankException):
    """Raised when authorization fails."""

    pass


class ServiceError(FuncBankException):
    """Raised when external services fail."""

    pass
