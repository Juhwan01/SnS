from .repository import LikeRepository
from ..comments.repository import CommentRepository
from ..users.repositories import UserRepository
from .dto import *
from ..comments.dto import *
from ..users.dto import UserProfileDTO
from ..users.models import Post, Comment, Like
from sqlalchemy.ext.asyncio import AsyncSession

class LikeService:
    def __init__(self, session: AsyncSession):
        self._session = session
        self._repository = LikeRepository(session)
        self._user_repository = UserRepository(session)

    async def create_like(self, user_id: int, post_id: int) -> LikeDTO:
        like = await self._repository.create_like(user_id, post_id)
        return await self._like_to_dto(like)

    async def delete_like(self, user_id: int, post_id: int) -> None:
        await self._repository.delete_like(user_id, post_id)

    async def get_likes_by_post(self, post_id: int, skip: int = 0, limit: int = 10) -> list[LikeDTO]:
        likes = await self._repository.get_likes_by_post_id(post_id, skip, limit)
        return [await self._like_to_dto(like) for like in likes]
    
    async def get_like_count(self, post_id: int) -> int:
        return await self._repository.get_like_count(post_id)

    async def _like_to_dto(self, like: Like) -> LikeDTO:
        user = await self._user_repository.get_user_by_id(like.user_id)
        user_dto = UserProfileDTO(
            id=user.id,
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            bio=user.bio,
            profile_picture=user.profile_picture,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
        
        return LikeDTO(
            id=like.id,
            user=user_dto,
            created_at=like.created_at
        )