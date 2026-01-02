from uuid import UUID
from pydantic import BaseModel, Field

class GroupCreateSchema(BaseModel):
    name: str
    description: str
