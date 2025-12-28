from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean

from animit.kit.db.models.base import RecordModel


class User(RecordModel):
    __tablename__ = "tbl_users"

    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    email: Mapped[str] = mapped_column(String(320), nullable=False, unique=True)
    email_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
