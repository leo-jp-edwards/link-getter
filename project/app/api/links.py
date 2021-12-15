from typing import List

from fastapi import APIRouter, BackgroundTasks, HTTPException, Path

from app.api import crud
from app.models.tortoise import SubLinkListSchema
from app.link_getter import generate_link_list

from app.models.pydantic import (  # isort:skip
    LinkPayloadSchema,
    LinkResponseSchema,
    LinkUpdatePayloadSchema,
)


router = APIRouter()


@router.post("/", response_model=LinkResponseSchema, status_code=201)
async def create_links(
    payload: LinkPayloadSchema, background_tasks: BackgroundTasks
) -> LinkResponseSchema:
    list_id = await crud.post(payload)

    background_tasks.add_task(generate_link_list, list_id, payload.url)

    response_object = {"id": list_id, "url": payload.url}
    return response_object


@router.get("/{id}/", response_model=SubLinkListSchema)
async def read_links(id: int = Path(..., gt=0)) -> SubLinkListSchema:
    sub_link_list = await crud.get(id)
    if not sub_link_list:
        raise HTTPException(status_code=404, detail="SubLinkList not found")

    return sub_link_list


@router.get("/", response_model=List[SubLinkListSchema])
async def read_all_links() -> List[SubLinkListSchema]:
    return await crud.get_all()


@router.delete("/{id}/", response_model=LinkResponseSchema)
async def delete_links(id: int = Path(..., gt=0)) -> LinkResponseSchema:
    sub_link_list = await crud.get(id)
    if not sub_link_list:
        raise HTTPException(status_code=404, detail="SubLinkList not found")

    await crud.delete(id)

    return sub_link_list


@router.put("/{id}/", response_model=SubLinkListSchema)
async def update_summary(
    payload: LinkUpdatePayloadSchema, id: int = Path(..., gt=0)
) -> SubLinkListSchema:
    sub_link_list = await crud.put(id, payload)
    if not sub_link_list:
        raise HTTPException(status_code=404, detail="SubLinkList not found")

    return sub_link_list
