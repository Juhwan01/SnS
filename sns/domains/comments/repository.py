from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from ..users.models import Comment, Like
from fastapi import HTTPException
from .dto import *

class CommentRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_comment(self, user_id: int, post_id: int, payload: CommentCreateDTO) -> Comment:
        comment = Comment(
            content=payload.content,
            author_id=user_id,
            post_id=post_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        self._session.add(comment)
        await self._session.commit()
        await self._session.refresh(comment)
        return comment

    async def get_comment_by_id(self, comment_id: int) -> Comment:
        query = select(Comment).options(joinedload(Comment.author)).where(Comment.id == comment_id)
        result = await self._session.execute(query)
        comment = result.scalar_one_or_none()
        if comment is None:
            raise HTTPException(status_code=404, detail="Comment not found")
        return comment

    async def update_comment(self, comment_id: int, user_id: int, payload: CommentUpdateDTO) -> Comment:
        comment = await self.get_comment_by_id(comment_id)
        if comment.author_id != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to update this comment")
        
        comment.content = payload.content
        comment.updated_at = datetime.utcnow()
        
        await self._session.commit()
        await self._session.refresh(comment)
        return comment

    async def delete_comment(self, comment_id: int, user_id: int) -> None:
        comment = await self.get_comment_by_id(comment_id)
        if comment.author_id != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to delete this comment")
        
        await self._session.delete(comment)
        await self._session.commit()

    async def get_comments_by_post_id(self, post_id: int, skip: int = 0, limit: int = 10) -> list[Comment]:
        query = select(Comment).options(joinedload(Comment.author)).where(Comment.post_id == post_id).order_by(Comment.created_at.desc()).offset(skip).limit(limit)
        result = await self._session.execute(query)
        return result.scalars().all()