from .repository import PostRepository
from ..users.repositories import UserRepository
from .dto import PostCreateDTO, PostUpdateDTO, PostDTO
from ..users.dto import UserProfileDTO
from ..users.models import Post
from sqlalchemy.ext.asyncio import AsyncSession


class PostService:
    def __init__(self, session: AsyncSession):
        self._session = session
        self._repository = PostRepository(session)
        self._user_repository = UserRepository(session)

    async def create_post(self, user_id: int, payload: PostCreateDTO) -> PostDTO:
        post = await self._repository.create_post(user_id, payload)
        return await self._post_to_dto(post)

    async def get_post(self, post_id: int) -> PostDTO:
        post = await self._repository.get_post_by_id(post_id)
        return await self._post_to_dto(post)

    async def update_post(self, post_id: int, user_id: int, payload: PostUpdateDTO) -> PostDTO:
        post = await self._repository.update_post(post_id, user_id, payload)
        return await self._post_to_dto(post)

    async def delete_post(self, post_id: int, user_id: int) -> None:
        await self._repository.delete_post(post_id, user_id)

    async def get_posts(self, skip: int = 0, limit: int = 10) -> list[PostDTO]:
        posts = await self._repository.get_posts(skip, limit)
        return [await self._post_to_dto(post) for post in posts]

    async def _post_to_dto(self, post: Post) -> PostDTO:
        likes_count = await self._repository.get_post_likes_count(post.id)
        comments_count = await self._repository.get_post_comments_count(post.id)
        
        author = await self._user_repository.get_user_by_id(post.author_id)
        author_dto = UserProfileDTO(
            id=author.id,
            username=author.username,
            email=author.email,
            full_name=author.full_name,
            bio=author.bio,
            profile_picture=author.profile_picture,
            created_at=author.created_at,
            updated_at=author.updated_at
        )
        
        return PostDTO(
            id=post.id,
            content=post.content,
            image_url=post.image_url,
            created_at=post.created_at,
            updated_at=post.updated_at,
            author=author_dto,
            likes_count=likes_count,
            comments_count=comments_count
        )

