from ..comments.repository import CommentRepository
from ..users.repositories import UserRepository
from .dto import *
from ..comments.dto import *
from ..users.dto import UserProfileDTO
from ..users.models import Post, Comment, Like
from sqlalchemy.ext.asyncio import AsyncSession

class CommentService:
    def __init__(self, session: AsyncSession):
        self._session = session
        self._repository = CommentRepository(session)
        self._user_repository = UserRepository(session)

    async def create_comment(self, user_id: int, post_id: int, payload: CommentCreateDTO) -> CommentDTO:
        comment = await self._repository.create_comment(user_id, post_id, payload)
        return await self._comment_to_dto(comment)

    async def get_comment(self, comment_id: int) -> CommentDTO:
        comment = await self._repository.get_comment_by_id(comment_id)
        return await self._comment_to_dto(comment)

    async def update_comment(self, comment_id: int, user_id: int, payload: CommentUpdateDTO) -> CommentDTO:
        comment = await self._repository.update_comment(comment_id, user_id, payload)
        return await self._comment_to_dto(comment)

    async def delete_comment(self, comment_id: int, user_id: int) -> None:
        await self._repository.delete_comment(comment_id, user_id)

    async def get_comments_by_post(self, post_id: int, skip: int = 0, limit: int = 10) -> list[CommentDTO]:
        comments = await self._repository.get_comments_by_post_id(post_id, skip, limit)
        return [await self._comment_to_dto(comment) for comment in comments]

    async def _comment_to_dto(self, comment: Comment) -> CommentDTO:
        author = await self._user_repository.get_user_by_id(comment.author_id)
        author_dto = UserProfileDTO(
            id=author.id,
            username=author.username,
            email=author.email,
            full_name=author.full_name,
            bio=author.bio,
            profile_picture=author.profile_picture,
            created_at=author.created_at,
            updated_at=author.updated_at
        )
        
        return CommentDTO(
            id=comment.id,
            content=comment.content,
            created_at=comment.created_at,
            updated_at=comment.updated_at,
            author=author_dto
        )
