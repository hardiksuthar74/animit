from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import CHAR, TIMESTAMP, String, Uuid, ForeignKey
from animit.kit.db.models.base import RecordModel

if TYPE_CHECKING:
    from animit.models import User


class LoginCode(RecordModel):
    __tablename__ = "tbl_login_codes"

    code_hash: Mapped[str] = mapped_column(
        CHAR(64), nullable=False, index=True, unique=True
    )
    expires_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, index=True
    )
    email: Mapped[str] = mapped_column(String(320), nullable=False, index=True)

    user_id: Mapped[UUID | None] = mapped_column(
        Uuid,
        ForeignKey("tbl_users.id", ondelete="cascade"),
        nullable=True,
        index=True,
    )
    user: Mapped["User | None"] = relationship("User", lazy="raise")
