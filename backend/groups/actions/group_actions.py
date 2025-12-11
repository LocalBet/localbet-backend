from abc import ABC, abstractmethod
from backend.groups.models import Group
from backend.shared.models import Condition, DataModel


class GroupActions(ABC):
    @abstractmethod
    def search(self, conditions: list[Condition[DataModel]]) -> list[Group]:
        """ Cerca grups basat en condicions específiques. """
        pass

    @abstractmethod
    def save(self, group: Group) -> None:
        """ Desa un grup a la base de dades. """
        pass

    @abstractmethod
    def update(self, group: Group) -> None:
        """ Actualitza un grup a la base de dades. """
        pass

    @abstractmethod
    def delete(self, group: Group) -> None:
        """ Elimina un grup de la base de dades. """
        pass
