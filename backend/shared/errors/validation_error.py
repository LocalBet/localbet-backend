"""
ValidationError module.
"""

from .domain_base_error import DomainBaseError


class ValidationError(DomainBaseError):
    """
    ValidationError class.
    This class must be used as a base class for all the exceptions that are raised when a validation error occurs.
    """
