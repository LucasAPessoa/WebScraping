from typing import List
from uuid import UUID, uuid4
from sqlmodel import Session, select

from app.models.models import Promotion
from app.schemas.promotion_schema import PromotionCreate, PromotionRead, PromotionUpdate, PromotionReadList

class PromotionRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_promotion(self, promotion_create: PromotionCreate) -> PromotionRead:
        promotion = Promotion(
            id=uuid4(),
            name=promotion_create.name
        )
        self.session.add(promotion)
        self.session.commit()
        self.session.refresh(promotion)
        return promotion

    def get_promotion_by_id(self, promotion_id: UUID) -> Promotion | None:
        return self.session.get(Promotion, promotion_id)
    
    def get_promotion_by_name(self, promotion_name: str) -> Promotion | None:
        return self.session.exec(
            select(Promotion).where(Promotion.name.ilike(f"%{promotion_name.lower()}%"))
        ).first()
        
    def get_all_promotions(self) -> List[Promotion]:
        result = self.session.exec(select(Promotion))
        return result.all()
    
    def update_promotion(self, promotion_id: UUID, promotion_update: PromotionUpdate) -> PromotionRead | None:
        promotion = self.session.get(Promotion, promotion_id)
        
        if not promotion:
            return None
        
        for key, value in promotion_update.model_dump().items():
            setattr(promotion, key, value)
        
        self.session.commit()
        self.session.refresh(promotion)
        return promotion
    
    def delete_promotion(self, promotion_id: UUID) -> None:
        promotion = self.session.get(Promotion, promotion_id)
        if promotion:
            self.session.delete(promotion)
            self.session.commit()
            
            
    