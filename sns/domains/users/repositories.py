from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from sqlalchemy import select
from .models import User
from .dto import UserSignUpDTO, UserProfileDTO
from datetime import datetime

class UserRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_user(self, payload: UserSignUpDTO) -> User:
        profile_picture_str = str(payload.profile_picture) if payload.profile_picture else None
        updated_at = datetime.utcnow()  # 현재 시간을 UTC로 설정

        user_entity = User(
            username=payload.username,
            email=payload.email,
            password=payload.password,
            full_name=payload.full_name,
            bio=payload.bio,
            profile_picture=profile_picture_str,
            updated_at=updated_at  # 현재 시간 설정
        )
        self._session.add(user_entity)
        try:
            await self._session.flush()
            await self._session.refresh(user_entity)
            await self._session.commit()
        except IntegrityError as e:
            await self._session.rollback()
            raise HTTPException(status_code=400, detail="Database integrity error: " + str(e))
        return user_entity

    async def get_user_by_username(self, username: str) -> User:
        query = select(User).where(User.username == username)
        result = await self._session.execute(query)
        user = result.scalar_one_or_none()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    async def get_user_by_id(self, user_id: int) -> User:
        query = select(User).where(User.id == user_id)
        result = await self._session.execute(query)
        user = result.scalar_one_or_none()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    async def update_user(self, user_id: int, payload: UserProfileDTO) -> User:
        query = select(User).where(User.id == user_id)
        result = await self._session.execute(query)
        user = result.scalar_one_or_none()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        for key, value in payload.dict(exclude_unset=True).items():
            setattr(user, key, value)
        
        try:
            await self._session.commit()
            await self._session.refresh(user)
        except IntegrityError as e:
            await self._session.rollback()
            raise HTTPException(status_code=400, detail="Database integrity error: " + str(e))
        
        return user