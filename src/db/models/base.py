from datetime import datetime

from sqlalchemy import DateTime, func, TIMESTAMP
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

BaseModel = declarative_base()


class IDMixin:
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)


class CreatedMixin:
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())


class UpdatedMixin:
    __abstract__ = True

    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()
    )
