from fastapi import Depends
from sqlalchemy.orm import Session
from ..session import get_db


class BaseDatabaseRepository:

    def __init__(self, session: Session = Depends(get_db)) -> None:
        self._session = session
