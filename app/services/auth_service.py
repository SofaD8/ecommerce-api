from sqlalchemy.ext.asyncio import AsyncSession

from app.services.user_service import user_service, verify_password
from app.core.security import create_access_token


class AuthService:
    async def authenticate_user(
            self,
            db: AsyncSession,
            email: str,
            password: str
    ):
        user = await user_service.get_by_email(db, email=email)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user

    def create_token_for_user(self, user):
        return create_access_token(data={"sub": user.email})

auth_service = AuthService()
