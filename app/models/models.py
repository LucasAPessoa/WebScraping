from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, JSON, Boolean, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Promotion(Base):
    __tablename__ = "promotion"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)
    discount_percentage = Column(Float, nullable=False)
    product_placeholder_id = Column(String, ForeignKey("product_placeholder.id"), nullable=False)

    # Relacionamentos
    product_placeholder = relationship("Product_Placeholder", back_populates="promotions")
    products = relationship("Product", back_populates="promotion")

class Establishment(Base):
    __tablename__ = "establishment"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    url = Column(String, nullable=False)
    logo_url = Column(String, nullable=True)

    # Relacionamentos
    products = relationship("Product", back_populates="establishment")

class Product_Placeholder(Base):
    __tablename__ = "product_placeholder"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    metacritic_score = Column(Integer, nullable=True)
    rating = Column(Float, nullable=True)
    released = Column(String, nullable=True)
    background_image = Column(String, nullable=True)
    background_image_additional = Column(String, nullable=True)
    website = Column(String, nullable=True)
    rawg_id = Column(Integer, nullable=True)
    genres = Column(String, nullable=True)
    platforms = Column(String, nullable=True)
    developers = Column(String, nullable=True)
    publishers = Column(String, nullable=True)
    screenshots = Column(Text, nullable=True)
    esrb_rating = Column(String, nullable=True)
    playtime = Column(Integer, nullable=True)
    achievements_count = Column(Integer, nullable=True)
    parent_platforms = Column(String, nullable=True)

    # Relacionamentos
    products = relationship("Product", back_populates="product_placeholder")
    promotions = relationship("Promotion", back_populates="product_placeholder")

class Product(Base):
    __tablename__ = "product"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    discount_price = Column(Float, nullable=True)
    url = Column(String, nullable=False)
    image_url = Column(String, nullable=True)
    product_placeholder_id = Column(String, ForeignKey("product_placeholder.id"), nullable=False)
    establishment_id = Column(String, ForeignKey("establishment.id"), nullable=False)
    promotion_id = Column(String, ForeignKey("promotion.id"), nullable=True)

    # Relacionamentos
    product_placeholder = relationship("Product_Placeholder", back_populates="products")
    establishment = relationship("Establishment", back_populates="products")
    promotion = relationship("Promotion", back_populates="products")

    def percentage_discount(self) -> float:
        """Calcula o percentual de desconto do produto"""
        if not self.price or not self.discount_price:
            return 0.0
        return ((self.price - self.discount_price) / self.price) * 100