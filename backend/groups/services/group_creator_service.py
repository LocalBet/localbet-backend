"""
Service for creating groups.
"""

from backend.groups.actions import GroupActions
from backend.groups.models import Group


class GroupCreatorService:
    def __init__(self, action: GroupActions) -> None:
        self.__action = action

    def create(self, group: Group) -> None:
        """
        Create a new group.

        Args:
            group (Group): The group to create.
        """
        self.__action.save(group)
