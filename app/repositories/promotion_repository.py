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