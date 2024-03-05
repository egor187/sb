"""
Directory for describing models.

Import model here to enable alembic autogenerate.

"""

__all__ = (
    "BaseModel",
    "Link",
)

from db.models.base import BaseModel
from db.models.link import Link
