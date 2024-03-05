from sqlalchemy import select, and_, insert

from db.models.link import Link
from db.repositories.base import BaseDatabaseRepository


class VisitRepository(BaseDatabaseRepository):

    def get_visited_domains(self, from_, to):
        query = select(Link.url)
        if from_ and to:
            query = query.filter(and_(Link.created_at >= from_, Link.created_at <= to))
        if from_:
            query = query.filter(Link.created_at >= from_)
        if to:
            query = query.filter(Link.created_at <= to)
        result = self._session.scalars(query.order_by(Link.created_at)).all()
        return result

    def save_links(self, links: list[str]):
        links_ids = self._session.scalars(
            insert(Link).returning(Link.id), [
                {"url": str(link)} for link in links
            ]
        )
        self._session.flush()
        return links_ids.all()
