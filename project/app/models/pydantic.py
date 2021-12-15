from pydantic import AnyHttpUrl, BaseModel
from typing import List

class LinkPayloadSchema(BaseModel):
    url: AnyHttpUrl


class LinkResponseSchema(LinkPayloadSchema):
    id: int

class LinkUpdatePayloadSchema(LinkPayloadSchema):
    sublinks: List[str]
