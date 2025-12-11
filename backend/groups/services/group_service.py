"""
Service for creating and managing groups.
"""

from backend.groups.actions import GroupActions  # Aquesta classe hauria de gestionar les accions sobre la base de dades
from backend.groups.models import Group  # El model que acabes de crear per al grup

class GroupService:
    def __init__(self, action: GroupActions) -> None:
        self.__action = action

    def create(self, group: Group) -> None:
        """
        Create a new group.

        Args:
            group (Group): The group to create.
        """
        self.__action.save(group)

    def update(self, group: Group) -> None:
        """
        Update an existing group.

        Args:
            group (Group): The group to update.
        """
        self.__action.update(group)

    def delete(self, group: Group) -> None:
        """
        Delete a group.

        Args:
            group (Group): The group to delete.
        """
        self.__action.delete(group)
