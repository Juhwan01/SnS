from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from domains.posts.services import PostService
from domains.posts.dto import PostCreateDTO, PostUpdateDTO, PostDTO
from domains.users.services import UserService
from dependencies.database import provide_session
from domains.users.models import User

router = APIRouter()

name = "posts"

@router.post("/posts", response_model=PostDTO, status_code=status.HTTP_201_CREATED)
async def create_post(
    payload: PostCreateDTO,
    current_user: User = Depends(UserService.get_current_user),
    session: AsyncSession = Depends(provide_session)
):
    post_service = PostService(session)
    return await post_service.create_post(current_user.id, payload)

@router.get("/posts/{post_id}", response_model=PostDTO)
async def get_post(
    post_id: int,
    session: AsyncSession = Depends(provide_session)
):
    post_service = PostService(session)
    return await post_service.get_post(post_id)

@router.put("/posts/{post_id}", response_model=PostDTO)
async def update_post(
    post_id: int,
    payload: PostUpdateDTO,
    current_user: User = Depends(UserService.get_current_user),
    session: AsyncSession = Depends(provide_session)
):
    post_service = PostService(session)
    return await post_service.update_post(post_id, current_user.id, payload)

@router.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int,
    current_user: User = Depends(UserService.get_current_user),
    session: AsyncSession = Depends(provide_session)
):
    post_service = PostService(session)
    await post_service.delete_post(post_id, current_user.id)

@router.get("/posts", response_model=List[PostDTO])
async def get_posts(
    skip: int = 0,
    limit: int = 10,
    session: AsyncSession = Depends(provide_session)
):
    post_service = PostService(session)
    return await post_service.get_posts(skip, limit)