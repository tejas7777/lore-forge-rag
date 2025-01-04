from fastapi import APIRouter, Depends
from src.api.controllers.query import QueryController

router = APIRouter()

@router.post("/query")
async def process_query(
    query: dict,
    query_controller: QueryController = Depends(QueryController)
):
    return await query_controller.process_query(query)

@router.get("/health")
async def health_check(
    query_controller: QueryController = Depends(QueryController)
):
    return await query_controller.health()