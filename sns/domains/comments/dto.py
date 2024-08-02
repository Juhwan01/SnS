from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from ..users.dto import UserProfileDTO

class CommentCreateDTO(BaseModel):
    content: str

class CommentUpdateDTO(BaseModel):
    content: str

class CommentDTO(BaseModel):
    id: int
    content: str
    created_at: datetime
    updated_at: datetime
    author: UserProfileDTO