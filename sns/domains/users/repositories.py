from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from sqlalchemy import select, delete
from .models import User, Follow
from .dto import UserSignUpDTO, UserProfileDTO, UserFollowerDTO
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
    
    async def get_followers(self, user:User):
        async with self._session as session:
            followers_query = (
                select(User)
                .join(Follow, Follow.follower_id == User.id)  # Follow.follower_id가 User.id와 조인됨
                .filter(Follow.followed_id == user.id)  # Follow.followed_id가 현재 사용자의 ID와 일치함
            )
            followers = await session.execute(followers_query)
            follower_users = followers.scalars().all()
            return follower_users
        
    async def set_follow(self, admin: User, target: User):
        async with self._session as session:
            # 새 팔로우 관계를 추가
            new_follow = Follow(follower_id=admin.id, followed_id=target.id)
            session.add(new_follow)
            await session.commit()

            # `admin` 사용자가 팔로우하는 사용자 목록 조회
            followers_query = (
                select(User)
                .join(Follow, Follow.follower_id == User.id)
                .filter(Follow.follower_id == admin.id)
            )

            # 쿼리 실행
            result = await session.execute(followers_query)
            followers = result.scalars().all()

            # `target` 사용자가 `admin`의 팔로워 목록에 포함되어 있는지 확인
            target_is_follower = target in followers

            return target_is_follower
    
    async def unfollow(self, admin: User, target: User):
        async with self._session as session:
            # `admin` 사용자가 `target`을 팔로우 목록에서 제거
            query = (
                delete(Follow)
                .where(Follow.follower_id == admin.id)
                .where(Follow.followed_id == target.id)
            )
            await session.execute(query)
            await session.commit()

            # `admin` 사용자가 팔로우하는 사용자 목록 조회
            followers_query = (
                select(User)
                .join(Follow, Follow.follower_id == User.id)
                .filter(Follow.follower_id == admin.id)
            )

            # 쿼리 실행
            result = await session.execute(followers_query)
            followers = result.scalars().all()

            # `target` 사용자가 `admin`의 팔로워 목록에 포함되지 않는지 확인
            target_is_not_follower = target not in followers

            return target_is_not_follower
        
    async def get_following(self, user:User):
        async with self._session as session:
            followers_query = (
                select(User)
                .join(Follow, Follow.followed_id == User.id)  # Follow.follower_id가 User.id와 조인됨
                .filter(Follow.follower_id == user.id)  # Follow.followed_id가 현재 사용자의 ID와 일치함
            )
            followers = await session.execute(followers_query)
            follower_users = followers.scalars().all()
            print(follower_users)
            return follower_users