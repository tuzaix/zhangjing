from fastapi import APIRouter
from app.api.endpoints import card, analysis, admin

api_router = APIRouter()
api_router.include_router(card.router, prefix="/card", tags=["card"])
api_router.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
