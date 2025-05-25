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
    
    def update_promotion(self, promotion_id: str, promotion_update: PromotionUpdate) -> PromotionRead:
        promotion = self.promotion_repository.get_promotion_by_id(UUID(promotion_id))
        
        if not promotion:
            raise HTTPException(status_code=404, detail="Promoção não encontrada.")
        
        name = promotion_update.name.strip().lower()
        
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
        
        return self.promotion_repository.update_promotion(promotion_id, promotion_update)
    
    def delete_promotion(self, promotion_id: str) -> None:
        promotion = self.promotion_repository.get_promotion_by_id(UUID(promotion_id))
        
        if not promotion:
            raise HTTPException(status_code=404, detail="Promoção não encontrada.")
        
        self.promotion_repository.delete_promotion(promotion_id)
        
    def get_promotion_by_id(self, promotion_id: str) -> PromotionRead:
        promotion = self.promotion_repository.get_promotion_by_id(UUID(promotion_id))
        
        if not promotion:
            raise HTTPException(status_code=404, detail="Promoção não encontrada.")
        
        return promotion
    
    def get_all_promotions(self) -> PromotionReadList:
        promotions = self.promotion_repository.get_all_promotions()
        
        if not promotions:
            raise HTTPException(status_code=404, detail="Nenhuma promoção encontrada.")
        
        promotion_read_list = [PromotionRead.model_validate(promo) for promo in promotions]
        return PromotionReadList(promotions=promotion_read_list)
    