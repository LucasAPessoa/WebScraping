from typing import List, Optional
from uuid import UUID, uuid4
from sqlmodel import select
from sqlalchemy.orm import Session
from datetime import datetime

from app.models.models import Promotion, Product
from app.schemas.promotion_schema import PromotionCreate, PromotionRead, PromotionUpdate, PromotionReadList

class PromotionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_promotion(self, promotion_data: PromotionCreate) -> Promotion:
        """Cria uma nova promoção"""
        try:
            promotion = Promotion(
                id=str(uuid4()),
                **promotion_data.model_dump()
            )
            self.db.add(promotion)
            self.db.commit()
            self.db.refresh(promotion)
            return promotion
        except Exception as e:
            self.db.rollback()
            raise e

    def get_promotion(self, promotion_id: str) -> Optional[Promotion]:
        """Busca uma promoção pelo ID"""
        return self.db.query(Promotion).filter(Promotion.id == promotion_id).first()

    def get_promotion_by_name(self, promotion_name: str) -> Optional[Promotion]:
        """Busca uma promoção pelo nome"""
        return self.db.query(Promotion).filter(
            Promotion.name.ilike(f"%{promotion_name.lower()}%")
        ).first()

    def get_all_promotions(self) -> List[Promotion]:
        """Retorna todas as promoções"""
        return self.db.query(Promotion).all()

    def update_promotion(self, promotion_id: str, promotion_data: PromotionUpdate) -> Optional[Promotion]:
        """Atualiza uma promoção"""
        try:
            promotion = self.get_promotion(promotion_id)
            if promotion:
                for key, value in promotion_data.model_dump(exclude_unset=True).items():
                    setattr(promotion, key, value)
                self.db.commit()
                self.db.refresh(promotion)
            return promotion
        except Exception as e:
            self.db.rollback()
            raise e

    def delete_promotion(self, promotion_id: str) -> bool:
        """Remove uma promoção"""
        try:
            promotion = self.get_promotion(promotion_id)
            if promotion:
                self.db.delete(promotion)
                self.db.commit()
                return True
            return False
        except Exception as e:
            self.db.rollback()
            raise e

    def associate_products_to_promotion(self, promotion: Promotion) -> None:
        """Associa produtos à promoção baseado no percentual de desconto"""
        try:
            # Busca produtos do mesmo placeholder que não estão em promoção
            products = self.db.query(Product).filter(
                Product.product_placeholder_id == promotion.product_placeholder_id,
                Product.promotion_id.is_(None)
            ).all()

            for product in products:
                discount_percentage = product.percentage_discount()
                if (promotion.min_discount_percentage <= discount_percentage <= promotion.max_discount_percentage):
                    product.promotion_id = promotion.id

            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e

    def remove_products_from_promotion(self, promotion_id: str) -> None:
        """Remove a associação de produtos de uma promoção"""
        try:
            self.db.query(Product).filter(Product.promotion_id == promotion_id).update(
                {Product.promotion_id: None}
            )
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e
            
            
    