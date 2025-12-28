import datetime
import secrets
import string

from sqlalchemy import select
from sqlalchemy.orm import joinedload
from animit.config import settings
from animit.exceptions import AnimitError
from animit.kit.crypto import get_token_hash
from animit.kit.db.postgres import AsyncSession
from animit.kit.utils import utc_now
from animit.models.login_code import LoginCode
from animit.user.repository import UserRepository
from animit.user.service import user as user_service


class LoginCodeError(AnimitError): ...


class LoginCodeInvalidOrExpired(LoginCodeError):
    def __init__(self) -> None:
        super().__init__("This login code is invalid or has expired.", status_code=401)


class LoginCodeService:
    async def request(
        self,
        session: AsyncSession,
        email: str,
    ):
        user_repository = UserRepository.from_session(session)
        user = await user_repository.get_by_email(email)

        code, code_hash = self._generate_code_hash()

        login_code = LoginCode(
            code_hash=code_hash,
            email=email,
            user_id=user.id if user is not None else None,
            expires_at=utc_now()
            + datetime.timedelta(seconds=settings.LOGIN_CODE_TTL_SECONDS),
        )
        session.add(login_code)
        await session.flush()

        return login_code, code

    def _generate_code_hash(self) -> tuple[str, str]:
        code = "".join(
            secrets.choice(string.ascii_uppercase + string.digits)
            for _ in range(settings.LOGIN_CODE_LENGTH)
        )
        code_hash = get_token_hash(code, secret=settings.SECRET)
        return code, code_hash

    async def send(
        self,
        login_code: LoginCode,
        code: str,
    ):
        # delta = login_code.expires_at - utc_now()
        # code_lifetime_minutes = int(ceil(delta.seconds / 60))

        email = login_code.email
        # subject = "Sign in to Animit"

        print(f"code for email {email} is {code}")

    async def authenticate(
        self,
        session: AsyncSession,
        code: str,
        email: str,
    ):
        code_hash = get_token_hash(code, secret=settings.SECRET)

        statement = (
            select(LoginCode)
            .where(
                LoginCode.code_hash == code_hash,
                LoginCode.email == email,
                LoginCode.expires_at > utc_now(),
            )
            .options(joinedload(LoginCode.user))
        )
        result = await session.execute(statement)
        login_code = result.unique().scalar_one_or_none()

        if login_code is None:
            raise LoginCodeInvalidOrExpired()

        is_signup = False
        user = login_code.user
        if user is None:
            user, is_signup = await user_service.get_by_email_or_create(
                session,
                login_code.email,
            )

        # Mark email as verified
        if not user.email_verified:
            is_signup = True
            user.email_verified = True
            session.add(user)

        await session.delete(login_code)

        return user, is_signup


login_code = LoginCodeService()
