"""
InfrastructureBaseError module.
"""


class InfrastructureBaseError(Exception):
    """
    InfrastructureBaseError class.
    """

    __message: str

    def __init__(self, *, message: str) -> None:
        """
        InfrastructureBaseError constructor.

        Args:
            message (str): The error message.
        """
        self.__message = message

        super().__init__(self.__message)

    @property
    def message(self) -> str:
        """
        Returns the error message.

        Returns:
            str: The error message.
        """
        return self.__message
