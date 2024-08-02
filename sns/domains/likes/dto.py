
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from ..users.dto import UserProfileDTO

class LikeDTO(BaseModel):
    id: int
    user: UserProfileDTO
    created_at: datetime
