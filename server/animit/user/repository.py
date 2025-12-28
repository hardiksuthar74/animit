from sqlalchemy import func
from animit.kit.repository import (
    RepositoryBase,
)
from animit.models import User


class UserRepository(
    RepositoryBase[User],
):
    model = User

    async def get_by_email(
        self,
        email: str,
    ) -> User | None:
        statement = self.get_base_statement().where(
            func.lower(User.email) == email.lower()
        )

        return await self.get_one_or_none(statement)
