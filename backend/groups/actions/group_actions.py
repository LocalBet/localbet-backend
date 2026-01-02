from abc import ABC, abstractmethod
from uuid import UUID

from backend.groups.models import Group
from backend.shared.models import Condition, DataModel


class GroupActions(ABC):
    @abstractmethod
    def search(self, conditions: list[Condition[DataModel]]) -> list[Group]:
        """Cerca grups basat en condicions específiques."""
        raise NotImplementedError

    @abstractmethod
    def save(self, group: Group) -> None:
        """Desa un grup a la base de dades."""
        raise NotImplementedError

    @abstractmethod
    def update(self, group: Group) -> None:
        """Actualitza un grup a la base de dades."""
        raise NotImplementedError

    @abstractmethod
    def delete(self, group: Group) -> None:
        """Elimina un grup de la base de dades."""
        raise NotImplementedError

    # 🔽 EXTRA (molt útil amb la teva BD)
    @abstractmethod
    def get_by_id(self, group_id: str | UUID) -> Group | None:
        """Retorna un grup per id (amb members i bet_ids)."""
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> list[Group]:
        """Retorna tots els grups (amb members i bet_ids)."""
        raise NotImplementedError

    @abstractmethod
    def get_user_groups(self, user_id: str | UUID) -> list[Group]:
        """Retorna els grups on un user_id és membre."""
        raise NotImplementedError
