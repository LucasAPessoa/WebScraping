from uuid import UUID
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.product_repository import ProductRepository
from app.repositories.promotion_repository import PromotionRepository
from app.schemas.product_schema import ProductCreate, ProductUpdate, ProductRead, ProductReadList
from app.models.models import Product, Promotion
from typing import List, Optional

class ProductService:
    def __init__(self, session: Session):
        self.repo = ProductRepository(session)
        self.promotion_repo = PromotionRepository(session)
        self.session = session

    def create_product(self, product_data: ProductCreate) -> Product:
        """Cria um novo produto e associa automaticamente a uma promoção se aplicável"""
        try:
            # Cria o produto
            product = self.repo.create_product(product_data)
            
            # Calcula o percentual de desconto do produto
            discount_percentage = product.percentage_discount()
            
            # Busca todas as promoções ativas
            promotions = self.promotion_repo.get_all_promotions()
            
            # Para cada promoção, verifica se o produto deve ser associado
            for promotion in promotions:
                if promotion.min_discount_percentage <= discount_percentage <= promotion.max_discount_percentage:
                    self.repo.update_product_promotion(product.id, promotion.id)
                    break
            
            return self.repo.get_by_id(product.id)
        except Exception as e:
            self.session.rollback()
            raise e

    def update_product(self, product_id: str, data: ProductUpdate) -> ProductRead:
        """Atualiza um produto e reavalia sua associação com promoções"""
        try:
            # Atualiza o produto
            product = self.repo.update_product(product_id, data)
            if not product:
                raise HTTPException(status_code=404, detail="Produto não encontrado")

            # Remove a associação atual com promoção (se houver)
            if product.promotion_id:
                self.repo.update_product_promotion(product.id, None)

            # Busca todas as promoções
            promotions = self.promotion_repo.get_all_promotions()

            # Para cada promoção, verifica se o produto atende aos critérios de desconto
            discount_percentage = product.percentage_discount()
            for promotion in promotions:
                if promotion.min_discount_percentage <= discount_percentage <= promotion.max_discount_percentage:
                    self.repo.update_product_promotion(product.id, promotion.id)
                    break

            return self._format_product_response(self.repo.get_by_id(product.id))

        except Exception as e:
            self.session.rollback()
            raise e

    def delete_product(self, product_id: str):
        """Remove um produto e sua associação com promoções"""
        try:
            product = self.repo.get_by_id(product_id)
            if not product:
                raise HTTPException(status_code=404, detail="Produto não encontrado")

            # Remove a associação com promoção se existir
            if product.promotion_id:
                self.promotion_repo.remove_products_from_promotion(str(product.promotion_id))

            self.repo.delete_product(product_id)
        except Exception as e:
            self.session.rollback()
            raise e

    def get_product_by_id(self, product_id: str) -> ProductRead:
        product = self.repo.get_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        return self._format_product_response(product)

    def get_all_products(self) -> ProductReadList:
        products = self.repo.get_all()
        return ProductReadList(products=[self._format_product_response(p) for p in products])

    def filter_product(
        self,
        product_placeholder_id: UUID = None,
        establishment_id: UUID = None,
        promotion_id: UUID = None,
        min_discount: float = None,
        max_discount: float = None
    ) -> ProductReadList:
        products = self.repo.filter_products(
            product_placeholder_id,
            establishment_id,
            promotion_id,
            min_discount,
            max_discount
        )
        return ProductReadList(products=[self._format_product_response(p) for p in products])

    def _format_product_response(self, product: Product) -> ProductRead:
        """Formata a resposta do produto incluindo dados do placeholder"""
        return ProductRead(
            id=product.id,
            name=product.product_placeholder.name,
            description=product.product_placeholder.description,
            price=product.price,
            discount_price=product.discount_price,
            url=product.url,
            image_url=product.product_placeholder.background_image,
            product_placeholder_id=product.product_placeholder_id,
            establishment_id=product.establishment_id,
            promotion_id=product.promotion_id
        )
