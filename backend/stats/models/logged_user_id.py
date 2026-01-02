from pydantic import BaseModel

class LoggedUserId(BaseModel):
    id: str
