"""Custom application exceptions"""

from fastapi import HTTPException, status


class BatteryTwinException(Exception):
    """Base exception for Battery Twin application"""
    pass


class DatabaseException(BatteryTwinException):
    """Database related exceptions"""
    pass


class ModelException(BatteryTwinException):
    """ML model related exceptions"""
    pass


class ModelNotFoundError(ModelException):
    """Raised when a model file is not found"""
    pass


class ModelInferenceError(ModelException):
    """Raised when model inference fails"""
    pass


class ValidationException(BatteryTwinException):
    """Data validation exceptions"""
    pass


class InvalidBatteryDataError(ValidationException):
    """Raised when battery data is invalid"""
    pass


class AuthenticationException(BatteryTwinException):
    """Authentication related exceptions"""
    pass


class UnauthorizedError(AuthenticationException):
    """Raised when user is not authorized"""

    @staticmethod
    def http_exception():
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )


class InvalidTokenError(AuthenticationException):
    """Raised when JWT token is invalid"""

    @staticmethod
    def http_exception():
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
