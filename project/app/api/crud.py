from typing import List, Union

from app.models.pydantic import LinkPayloadSchema
from app.models.tortoise import SubLinkList


async def post(payload: LinkPayloadSchema) -> int:
    sub_link_list = SubLinkList(url=payload.url, sublinks=[])
    await sub_link_list.save()
    return sub_link_list.id


async def get(id: int) -> Union[dict, None]:
    sub_link_list = await SubLinkList.filter(id=id).first().values()
    if sub_link_list:
        return sub_link_list
    return None


async def get_all() -> List:
    sub_link_list = await SubLinkList.all().values()
    return sub_link_list


async def delete(id: int) -> int:
    sub_link_list = await SubLinkList.filter(id=id).first().delete()
    return sub_link_list


async def put(id: int, payload: LinkPayloadSchema) -> Union[dict, None]:
    sub_link_list = await SubLinkList.filter(id=id).update(
        url=payload.url, sublinks=payload.sublinks
    )
    if sub_link_list:
        updated_link_list = await SubLinkList.filter(id=id).first().values()
        return updated_link_list
    return None
