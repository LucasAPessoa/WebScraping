from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.controllers import promotion_controller
from app.schemas.promotion_schema import PromotionCreate, PromotionRead, PromotionUpdate, PromotionReadList
from app.database.session import get_session

promotion_router = APIRouter(prefix="/promotions", tags=["Promotions"])

@promotion_router.post("/", response_model=PromotionRead, status_code=status.HTTP_201_CREATED)
def create_promotion(   
    promotion_create: PromotionCreate, 
    session: Session = Depends(get_session)
):
    return promotion_controller.create_promotion(promotion_create, session)