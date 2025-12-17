from pydantic import BaseModel
from typing import List

class LoggedUsersResponseSchema(BaseModel):
    logged_users: List[str]
    count: int
