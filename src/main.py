import datetime

from fastapi import FastAPI, Depends

from core.schemas import VisitedLinksSchema, GetVisitedDomainsSchema
from services.visit import VisitService
from typing import Annotated
from fastapi import Query, status

app = FastAPI()


@app.post("/visited_links", status_code=status.HTTP_200_OK)
async def visited_links(links: VisitedLinksSchema, visited_links_service: VisitService = Depends()):
    return {"status": "Ok", "saved_links_ids": visited_links_service.save_links(links)}


@app.get("/visited_domains", status_code=status.HTTP_200_OK, response_model=GetVisitedDomainsSchema)
async def visited_domains(
        from_: Annotated[int | None, Query(gt=0, le=int(datetime.datetime.now().timestamp()))] = None,
        to: Annotated[int | None, Query(gt=0, le=int(datetime.datetime.now().timestamp()))] = None,
        visited_links_service: VisitService = Depends()
):
    return visited_links_service.get_links(from_, to)
