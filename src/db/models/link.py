from sqlalchemy.orm import Mapped, mapped_column

from db.models.base import IDMixin, CreatedMixin, BaseModel, UpdatedMixin


class Link(IDMixin, CreatedMixin, BaseModel):
    __tablename__ = "link"

    url: Mapped[str] = mapped_column()
