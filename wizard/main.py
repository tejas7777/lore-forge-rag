from fastapi import FastAPI
from src.api.routes.query import router as query_router

app = FastAPI()

app.include_router(query_router, prefix="/api/v1")