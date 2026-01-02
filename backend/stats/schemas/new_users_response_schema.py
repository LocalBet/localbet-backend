from pydantic import BaseModel
from typing import List

class NewUsersResponseSchema(BaseModel):
    new_users: List[str]
    count: int
