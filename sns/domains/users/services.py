from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from .repositories import UserRepository
from .dto import UserSignUpDTO, UserLoginDTO, Token, UserProfileDTO
from .models import User
from dependencies.database import provide_session

# 이 값들은 환경 변수나 설정 파일에서 가져오는 것이 좋습니다.
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

class UserService:
    def __init__(self, session: AsyncSession):
        self._session = session
        self._repository = UserRepository(session)

    async def create_user(self, payload: UserSignUpDTO) -> User:
        hashed_password = self._hash_password(payload.password)
        payload.password = hashed_password
        return await self._repository.create_user(payload=payload)

    async def authenticate_user(self, username: str, password: str) -> Optional[User]:
        user = await self._repository.get_user_by_username(username)
        if not user:
            return None
        if not self._verify_password(password, user.password):
            return None
        return user

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    async def get_current_user(self, token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(provide_session)) -> User:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        user_service = UserService(db)  # UserService 인스턴스를 생성
        user = await user_service._repository.get_user_by_username(username)
        if user is None:
            raise credentials_exception
        return user
    

    def _hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    async def login(self, login_data: UserLoginDTO) -> Token:
        user = await self.authenticate_user(login_data.username, login_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = self.create_access_token(data={"sub": user.username})
        return Token(access_token=access_token, token_type="bearer")

    async def get_user_profile(self, user: User) -> UserProfileDTO:
        return UserProfileDTO(
            id=user.id,
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            bio=user.bio,
            profile_picture=user.profile_picture,
            created_at=user.created_at,
            updated_at=user.updated_at
        )

    async def update_user_profile(self, user_id: int, payload: UserProfileDTO) -> User:
        return await self._repository.update_user(user_id, payload)