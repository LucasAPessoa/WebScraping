from sqlmodel import Session, select
from app.models.models import Promotion
from app.schemas.promotion_schema import PromotionCreate, PromotionRead, PromotionUpdate, PromotionReadList
from app.repositories.promotion_repository import PromotionRepository
from fastapi import HTTPException
from uuid import UUID
import re


class PromotionService:
    def __init__(self, session: Session):
        self.session = session
        self.promotion_repository = PromotionRepository(session)
    def create_promotion(self, promotion_create: PromotionCreate) -> PromotionRead:
        name = promotion_create.name.strip().lower()

        existing_promotion = self.promotion_repository.get_promotion_by_name(name)
        if existing_promotion:
            raise HTTPException(status_code=400, detail="Promoção já existe.")

        if not name:
            raise HTTPException(status_code=400, detail="O nome da promoção é obrigatório.")
        if len(name) < 3:
            raise HTTPException(status_code=400, detail="O nome da promoção deve ter pelo menos 3 caracteres.")
        if len(name) > 50:
            raise HTTPException(status_code=400, detail="O nome da promoção deve ter no máximo 50 caracteres.")
        if not re.match(r'^[a-zA-Z0-9 ]+$', name):
            raise HTTPException(status_code=400, detail="O nome da promoção deve conter apenas letras e números.")

        return self.promotion_repository.create_promotion(promotion_create)