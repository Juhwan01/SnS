from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional
from ..users.dto import UserProfileDTO

class PostCreateDTO(BaseModel):
    content: str
    image_url: Optional[HttpUrl] = None

class PostUpdateDTO(BaseModel):
    content: Optional[str] = None
    image_url: Optional[HttpUrl] = None

class PostDTO(BaseModel):
    id: int
    content: str
    image_url: Optional[HttpUrl] = None
    created_at: datetime
    updated_at: datetime
    author: UserProfileDTO
    likes_count: int
    comments_count: int
    
