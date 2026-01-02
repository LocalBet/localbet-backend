"""
Service for creating and managing groups.
"""

from backend.groups.actions import GroupActions
from backend.groups.models import Group

class GroupService:
    def __init__(self, actions: GroupActions) -> None:
        """
        Initialize GroupService with actions repository.
        
        Args:
            actions (GroupActions): Repository for group database operations.
        """
        self.__actions = actions

    def create(self, group: Group) -> None:
        """
        Create a new group.

        Args:
            group (Group): The group to create.
        """
        self.__actions.save(group)

    def update(self, group: Group) -> None:
        """
        Update an existing group.

        Args:
            group (Group): The group to update.
        """
        self.__actions.update(group)

    def delete(self, group: Group) -> None:
        """
        Delete a group.

        Args:
            group (Group): The group to delete.
        """
        self.__actions.delete(group)

    def get_by_id(self, group_id: str) -> Group:
        """
        Get group by ID.
        
        Args:
            group_id (str): Group UUID.
            
        Returns:
            Group: The group with the given ID.
            
        Raises:
            NoRowAffectedError: If group not found.
        """
        group = self.__actions.get_by_id(group_id)
        
        if not group:
            from backend.shared.infrastructure.errors import NoRowAffectedError
            raise NoRowAffectedError()
        
        return group

    def get_all(self) -> list[Group]:
        """
        Get all groups.
        
        Returns:
            list[Group]: List of all groups.
        """
        return self.__actions.get_all()