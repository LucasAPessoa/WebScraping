from fastapi import APIRouter
from app.controllers.establishment_controller import router as establishment_router

router = APIRouter(prefix="/establishments", tags=["establishments"])

router.include_router(establishment_router)

