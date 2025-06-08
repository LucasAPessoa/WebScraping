from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.controllers import promotion_controller
from app.schemas.promotion_schema import PromotionCreate, PromotionRead, PromotionUpdate, PromotionReadList
from app.database.session import get_db


router = APIRouter(prefix="/promotions", tags=["Promotions"])

@router.post("/", response_model=PromotionRead, status_code=status.HTTP_201_CREATED)
def create_promotion(   
    promotion_create: PromotionCreate, 
    session: Session = Depends(get_db)
):
    return promotion_controller.create_promotion(promotion_create, session)

@router.put("/{promotion_id}", response_model=PromotionRead, status_code=status.HTTP_200_OK)
def update_promotion(
    promotion_id: str, 
    promotion_update: PromotionUpdate, 
    session: Session = Depends(get_db)
):
    return promotion_controller.update_promotion(promotion_id, promotion_update, session)

@router.delete("/{promotion_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_promotion(
    promotion_id: str, 
    session: Session = Depends(get_db)
):
    return promotion_controller.delete_promotion(promotion_id, session)

@router.get("/{promotion_id}", response_model=PromotionRead, status_code=status.HTTP_200_OK)
def get_promotion_by_id(
    promotion_id: str, 
    session: Session = Depends(get_db)
):
    return promotion_controller.get_promotion_by_id(promotion_id, session)

@router.get("/", response_model=PromotionReadList, status_code=status.HTTP_200_OK)
def get_all_promotions(
    session: Session = Depends(get_db)
):
    return promotion_controller.get_all_promotions(session)

