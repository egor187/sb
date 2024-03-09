from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

BaseModel = declarative_base()


def current_time():
    return datetime.now()


class IDMixin:
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)


class CreatedMixin:
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now())


class UpdatedMixin:
    __abstract__ = True

    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(), onupdate=lambda: datetime.now()
    )
