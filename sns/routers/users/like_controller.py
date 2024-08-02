from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from domains.likes.service import LikeService
from domains.likes.dto import LikeDTO
from domains.users.services import UserService
from dependencies.database import provide_session
from domains.users.models import User


router = APIRouter()

name = "likes"

@router.post("/posts/{post_id}/likes", response_model=LikeDTO, status_code=status.HTTP_201_CREATED)
async def create_like(
    post_id: int,
    current_user: User = Depends(UserService.get_current_user),
    session: AsyncSession = Depends(provide_session)
):
    like_service = LikeService(session)
    return await like_service.create_like(current_user.id, post_id)

@router.delete("/posts/{post_id}/likes", status_code=status.HTTP_204_NO_CONTENT)
async def delete_like(
    post_id: int,
    current_user: User = Depends(UserService.get_current_user),
    session: AsyncSession = Depends(provide_session)
):
    like_service = LikeService(session)
    await like_service.delete_like(current_user.id, post_id)

@router.get("/posts/{post_id}/likes", response_model=List[LikeDTO])
async def get_likes(
    post_id: int,
    skip: int = 0,
    limit: int = 10,
    session: AsyncSession = Depends(provide_session)
):
    like_service = LikeService(session)
    return await like_service.get_likes_by_post(post_id, skip, limit)

@router.get("/posts/{post_id}/like-count", response_model=int)
async def get_like_count(
    post_id: int,
    session: AsyncSession = Depends(provide_session)
):
    like_service = LikeService(session)
    return await like_service.get_like_count(post_id)