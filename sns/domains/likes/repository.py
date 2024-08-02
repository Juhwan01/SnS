from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,func
from sqlalchemy.orm import joinedload
from ..users.models import Comment, Like
from fastapi import HTTPException
from .dto import *
from datetime import datetime
from sqlalchemy.exc import IntegrityError

class LikeRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_like(self, user_id: int, post_id: int) -> Like:
        like = Like(
            user_id=user_id,
            post_id=post_id,
            created_at=datetime.utcnow()
        )
        self._session.add(like)
        try:
            await self._session.commit()
            await self._session.refresh(like)
            return like
        except IntegrityError:
            await self._session.rollback()
            raise HTTPException(status_code=400, detail="You have already liked this post")

    async def delete_like(self, user_id: int, post_id: int) -> None:
        query = select(Like).where(Like.user_id == user_id, Like.post_id == post_id)
        result = await self._session.execute(query)
        like = result.scalar_one_or_none()
        if like is None:
            raise HTTPException(status_code=404, detail="Like not found")
        
        await self._session.delete(like)
        await self._session.commit()
        
    async def get_like_count(self, post_id: int) -> int:
        query = select(func.count(Like.id)).where(Like.post_id == post_id)
        result = await self._session.execute(query)
        return result.scalar_one()

    async def get_likes_by_post_id(self, post_id: int, skip: int = 0, limit: int = 10) -> list[Like]:
        query = select(Like).options(joinedload(Like.user)).where(Like.post_id == post_id).order_by(Like.created_at.desc()).offset(skip).limit(limit)
        result = await self._session.execute(query)
        return result.scalars().all()