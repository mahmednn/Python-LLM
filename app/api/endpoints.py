from .api_v1 import health, llm, users
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(health.router, prefix="/health", tags=["Health"])
api_router.include_router(llm.router, prefix="/llm", tags=["LLM"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
