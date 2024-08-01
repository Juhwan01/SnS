from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies.database import provide_session
from domains.users.services import UserService
from domains.users.dto import UserSignUpDTO, UserLoginDTO, Token, UserProfileDTO
from domains.users.models import User
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

name="users"
@router.post("/signup", response_model=UserProfileDTO)
async def signup(payload: UserSignUpDTO, db: AsyncSession = Depends(provide_session)):
    logger.debug(f"Signup attempt for user: {payload.username}")
    user_service = UserService(db)
    try:
        user = await user_service.create_user(payload=payload)
        logger.info(f"Signup successful for user: {payload.username}")
        return await user_service.get_user_profile(user)
    except HTTPException as he:
        logger.warning(f"Signup failed for user {payload.username}: {he.detail}")
        raise he
    except Exception as e:
        logger.error(f"An unexpected error occurred during signup: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during signup",
        )

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(provide_session)):
    logger.debug(f"Login attempt for user: {form_data.username}")
    user_service = UserService(db)
    try:
        login_data = UserLoginDTO(username=form_data.username, password=form_data.password)
        token = await user_service.login(login_data)
        logger.info(f"Login successful for user: {form_data.username}")
        return token
    except HTTPException as he:
        logger.warning(f"Login failed for user {form_data.username}: {he.detail}")
        raise he
    except Exception as e:
        logger.error(f"An unexpected error occurred during login: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during login",
        )

@router.get("/me", response_model=UserProfileDTO)
async def read_users_me(
    current_user: User = Depends(UserService.get_current_user),
    db: AsyncSession = Depends(provide_session)
):
    user_service = UserService(db)
    return await user_service.get_user_profile(current_user)

@router.put("/me", response_model=UserProfileDTO)
async def update_user_profile(
    payload: UserProfileDTO,
    current_user: User = Depends(UserService.get_current_user),
    db: AsyncSession = Depends(provide_session)
):
    user_service = UserService(db)
    updated_user = await user_service.update_user_profile(current_user.id, payload)
    return await user_service.get_user_profile(updated_user)