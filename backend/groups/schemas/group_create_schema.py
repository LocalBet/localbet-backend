from uuid import UUID
from pydantic import BaseModel, Field

class GroupCreateSchema(BaseModel):
    name: str = Field(..., description="Group name")
    # Afegir més camps si cal, com la descripció del grup, etc.

    class Config:
        schema_extra = {
            "example": {
                "name": "Football Lovers",
            }
        }
