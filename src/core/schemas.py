from datetime import datetime

from pydantic import BaseModel, AnyUrl, Field, model_validator, ConfigDict


class BaseOrmSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class VisitedLinksSchema(BaseModel):
    urls: list[AnyUrl]


class QSDateFilterSchema(BaseModel):
    """
    Custom schema for date_filters from payload in 'post'-request
    """
    from_: int = Field(alias="from")
    to: int

    model_config = ConfigDict(populate_by_name=True)

    @model_validator(mode="after")
    def check_timestamp_fields(self):
        try:
            datetime.fromtimestamp(self.from_)
            datetime.fromtimestamp(self.to)
        except OverflowError:
            raise ValueError("Overflow error")
        now = int(datetime.now().timestamp())
        if self.from_ > self.to or self.to > now or self.from_ > now:
            raise ValueError("Invalid filter value")
        return self


class GetVisitedDomainsSchema(BaseModel):
    status: str = "ok"
    domains: list[str]
