from pydantic import BaseModel, EmailStr, HttpUrl, AnyUrl
from datetime import datetime
from typing import Optional, List

class UserSignUpDTO(BaseModel):
    username: str
    email: EmailStr
    password: str
    full_name: str
    bio: Optional[str] = None
    profile_picture: Optional[HttpUrl] = None

class UserLoginDTO(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserProfileDTO(BaseModel):
    id: int
    username: str
    email: EmailStr
    full_name: str
    bio: Optional[str] = None
    profile_picture: Optional[HttpUrl] = None
    created_at: datetime
    updated_at: datetime

class PostCreateDTO(BaseModel):
    content: str
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

class CommentCreateDTO(BaseModel):
    content: str
    post_id: int

class CommentDTO(BaseModel):
    id: int
    content: str
    created_at: datetime
    updated_at: datetime
    author: UserProfileDTO
    post_id: int

class LikeDTO(BaseModel):
    id: int
    user_id: int
    post_id: int
    created_at: datetime

class FollowDTO(BaseModel):
    id: int
    follower_id: int
    followed_id: int
    created_at: datetime