from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import joinedload
from ..users.models import Post, User, Like, Comment
from fastapi import HTTPException
from .dto import *
from datetime import datetime


class PostRepository:
    def __init__(self, session: AsyncSession):
        self._session = session


    async def create_post(self, user_id: int, payload: PostCreateDTO) -> Post:
        # Convert image_url to string if it's a Url object
        image_url = str(payload.image_url) if payload.image_url else None
        
        post = Post(
            content=payload.content,
            image_url=image_url,
            author_id=user_id,
            created_at=datetime.utcnow(),  # Set created_at to current time
            updated_at=datetime.utcnow()   # Set updated_at to current time
        )
        self._session.add(post)
        await self._session.commit()
        await self._session.refresh(post)
        return post


    async def get_post_by_id(self, post_id: int) -> Post:
        query = select(Post).options(joinedload(Post.author)).where(Post.id == post_id)
        result = await self._session.execute(query)
        post = result.scalar_one_or_none()
        if post is None:
            raise HTTPException(status_code=404, detail="Post not found")
        return post

    async def update_post(self, post_id: int, user_id: int, payload: PostUpdateDTO) -> Post:
        post = await self.get_post_by_id(post_id)
        if post.author_id != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to update this post")
        
        for key, value in payload.dict(exclude_unset=True).items():
            setattr(post, key, value)
        
        await self._session.commit()
        await self._session.refresh(post)
        return post

    async def delete_post(self, post_id: int, user_id: int) -> None:
        post = await self.get_post_by_id(post_id)
        if post.author_id != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to delete this post")
        
        await self._session.delete(post)
        await self._session.commit()

    async def get_posts(self, skip: int = 0, limit: int = 10) -> list[Post]:
        query = select(Post).options(joinedload(Post.author)).order_by(Post.created_at.desc()).offset(skip).limit(limit)
        result = await self._session.execute(query)
        return result.scalars().all()

    async def get_post_likes_count(self, post_id: int) -> int:
        query = select(func.count(Like.id)).where(Like.post_id == post_id)
        result = await self._session.execute(query)
        return result.scalar_one()

    async def get_post_comments_count(self, post_id: int) -> int:
        query = select(func.count(Comment.id)).where(Comment.post_id == post_id)
        result = await self._session.execute(query)
        return result.scalar_one()