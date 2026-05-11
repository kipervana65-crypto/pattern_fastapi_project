from fastapi import HTTPException

from app.core.security import get_password_hash, verify_password
from app.db.models.user import User
from app.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def register_user(self, *, email: str, password: str) -> User:
        existing_user = await self.repository.get_by_email(email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        hashed_password = get_password_hash(password)
        return await self.repository.create(email=email, hashed_password=hashed_password)

    async def authenticate_user(self, *, email: str, password: str) -> User | None:
        user = await self.repository.get_by_email(email)
        if not user:
            return None

        if not verify_password(password, user.hashed_password):
            return None

        return user

    async def get_user_by_id(self, user_id: int) -> User | None:
        return await self.repository.get_by_id(user_id)

    async def get_active_user_by_email(self, email: str) -> User | None:
        return await self.repository.get_active_by_email(email)

    async def get_all_users(self) -> list[User]:
        return await self.repository.get_all()

    async def create_user(self, *, email: str, password: str) -> User:
        return await self.register_user(email=email, password=password)

    async def update_user(self, user: User, *, email: str, password: str) -> User:
        hashed_password = get_password_hash(password)
        return await self.repository.update(
            user,
            email=email,
            hashed_password=hashed_password,
        )

    async def delete_user(self, user: User) -> None:
        await self.repository.delete(user)
