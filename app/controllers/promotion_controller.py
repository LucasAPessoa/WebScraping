from fastapi import Depends
from sqlmodel import Session
from app.schemas.promotion_schema import PromotionCreate, PromotionUpdate
from app.services.promotion_services import PromotionService
from app.database.session import get_session

def create_promotion(promotion_create: PromotionCreate, session: Session = Depends(get_session)):
    service = PromotionService(session)
    return service.create_promotion(promotion_create)

def get_promotion_by_id(promotion_id: str, session: Session = Depends(get_session)):
    service = PromotionService(session)
    return service.get_promotion_by_id(promotion_id)

def get_all_promotions(session: Session = Depends(get_session)):
    service = PromotionService(session)
    return service.get_all_promotions()

def get_promotion_by_name(promotion_name: str, session: Session = Depends(get_session)):
    service = PromotionService(session)
    return service.get_promotion_by_name(promotion_name)

def update_promotion(promotion_id: str, promotion_update: PromotionUpdate, session: Session = Depends(get_session)):
    service = PromotionService(session)
    return service.update_promotion(promotion_id, promotion_update)

def delete_promotion(promotion_id: str, session: Session = Depends(get_session)):
    service = PromotionService(session)
    return service.delete_promotion(promotion_id)