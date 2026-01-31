"""
Permission Resource type enum.
"""

from enum import StrEnum, unique

@unique
class PermissionResourceType(StrEnum):
    """
    PermissionResourceType type enum.
    """
    USER = 'USER'
    GROUP = 'GROUP'
    BET = 'BET'
    WALLET = 'WALLET'
    PERMISSION = 'PERMISSION'
    ROLE = 'ROLE'
    COIN = 'COIN'