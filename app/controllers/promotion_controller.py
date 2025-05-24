from fastapi import Depends
from sqlmodel import Session
from app.schemas.promotion_schema import PromotionCreate
from app.services.promotion_services import PromotionService
from app.database.session import get_session

def create_promotion(promotion_create: PromotionCreate, session: Session = Depends(get_session)):
    service = PromotionService(session)
    return service.create_promotion(promotion_create)