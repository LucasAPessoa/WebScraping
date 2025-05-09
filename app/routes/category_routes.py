from fastapi import APIRouter
from app.controllers import category_controller

api_router = APIRouter()
api_router.include_router(category_controller.router)