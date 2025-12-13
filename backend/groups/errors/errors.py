class GroupNameError(ValueError):
    def __init__(self, name: str) -> None:
        super().__init__(f"Invalid group name: {name!r}. Must be at least 3 characters.")
