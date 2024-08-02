from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from domains.comments.service import CommentService
from domains.comments.dto import CommentCreateDTO, CommentUpdateDTO, CommentDTO
from domains.users.services import UserService
from dependencies.database import provide_session
from domains.users.models import User

router = APIRouter()

name = "comments"
@router.post("/posts/{post_id}/comments", response_model=CommentDTO, status_code=status.HTTP_201_CREATED)
async def create_comment(
    post_id: int,
    payload: CommentCreateDTO,
    current_user: User = Depends(UserService.get_current_user),
    session: AsyncSession = Depends(provide_session)
):
    comment_service = CommentService(session)
    return await comment_service.create_comment(current_user.id, post_id, payload)

@router.get("/posts/{post_id}/comments", response_model=List[CommentDTO])
async def get_comments(
    post_id: int,
    skip: int = 0,
    limit: int = 10,
    session: AsyncSession = Depends(provide_session)
):
    comment_service = CommentService(session)
    return await comment_service.get_comments_by_post(post_id, skip, limit)

@router.put("/comments/{comment_id}", response_model=CommentDTO)
async def update_comment(
    comment_id: int,
    payload: CommentUpdateDTO,
    current_user: User = Depends(UserService.get_current_user),
    session: AsyncSession = Depends(provide_session)
):
    comment_service = CommentService(session)
    return await comment_service.update_comment(comment_id, current_user.id, payload)

@router.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    comment_id: int,
    current_user: User = Depends(UserService.get_current_user),
    session: AsyncSession = Depends(provide_session)
):
    comment_service = CommentService(session)
    await comment_service.delete_comment(comment_id, current_user.id)