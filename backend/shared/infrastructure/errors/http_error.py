"""
HTTPError module.
"""

from .infrastructure_base_error import InfrastructureBaseError


class HTTPError(InfrastructureBaseError):
    """
    HTTPError class.
    """

    __status_code: int
    __title: str

    def __init__(self, *, status_code: int, title: str, message: str) -> None:
        """
        HTTPError constructor.

        Args:
            status_code (int): The error status code.
            title (str): The error title.
            message (str): The error message to be displayed.
        """
        self.__status_code = status_code
        self.__title = title

        super().__init__(message=message)

    @property
    def status_code(self) -> int:
        """
        Get the error status code.

        Returns:
            int: The error status code.
        """
        return self.__status_code

    @property
    def title(self) -> str:
        """
        Get the error title.

        Returns:
            str: The error tile.
        """
        return self.__title
