from animit.kit.db.postgres import AsyncSession
from animit.models.user import User
from animit.user.repository import UserRepository


class UserService:
    async def get_by_email_or_create(
        self,
        session: AsyncSession,
        email: str,
    ):
        repository = UserRepository.from_session(session)
        user = await repository.get_by_email(email)
        created = False
        if user is None:
            user = await self.create_by_email(
                session,
                email,
            )
            created = True

        return (user, created)

    async def create_by_email(
        self,
        session: AsyncSession,
        email: str,
    ):
        repository = UserRepository.from_session(session)
        user = await repository.create(
            User(
                email=email,
            ),
            flush=True,
        )
        return user


user = UserService()
