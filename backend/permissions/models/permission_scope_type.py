"""
Permission Scope type enum
"""

from enum import StrEnum, unique

@unique
class PermissionScopeType(StrEnum):
    """
    PermissionScopeType type enum.
    """
    GLOBAL = 'GLOBAL'
    GROUP = 'GROUP'