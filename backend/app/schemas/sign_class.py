from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class SignClassBase(BaseModel):
    label: str
    display_name: str
    description: Optional[str] = None
    category: str = "interview"
    example_url: Optional[str] = None
    is_active: bool = True


class SignClassCreate(SignClassBase):
    pass


class SignClassResponse(SignClassBase):
    id: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

