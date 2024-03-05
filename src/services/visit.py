from datetime import datetime
import tldextract

from fastapi import Depends
from sqlalchemy.orm import Session

from db.session import get_db
from db.repositories.visited_links import VisitRepository


class VisitService:
    def __init__(self, repo: VisitRepository = Depends(), session: Session = Depends(get_db)):
        self._repo = repo
        self._session = session

    @staticmethod
    def _links_to_domains(domains: list[str]) -> dict[str, list]:
        return {
            "domains": [
                f"{tldextract.extract(domain).domain}.{tldextract.extract(domain).suffix}" for domain in domains
            ]
        }

    def get_links(self, from_: int | None = None, to: int | None = None):
        from_ = datetime.fromtimestamp(from_) if from_ else None
        to = datetime.fromtimestamp(to) if to else None
        return self._links_to_domains(self._repo.get_visited_domains(from_, to))

    def save_links(self, payload):
        ids = self._repo.save_links(payload.urls)
        self._session.commit()
        return ids
