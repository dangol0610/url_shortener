from fastapi import APIRouter

from src.app.routers import router as urls_router

router = APIRouter(prefix="/api")
router.include_router(urls_router)
