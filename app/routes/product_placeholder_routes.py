from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.database.session import get_db
from app.controllers.product_placeholder_controller import (
    create_product_placeholder,
    update_product_placeholder,
    delete_product_placeholder,
    get_product_placeholder_by_id,
    get_all_product_placeholders
)
from app.schemas.product_placeholder_schema import (
    ProductPlaceholderCreate,
    ProductPlaceholderUpdate,
    ProductPlaceholderRead,
    ProductPlaceholderReadList,
    ProductPlaceholderDelete
)
from typing import List

router = APIRouter(prefix="/product-placeholders", tags=["product-placeholders"])

@router.post("/", response_model=ProductPlaceholderRead)
def create_product_placeholder_route(
    product_data: ProductPlaceholderCreate,
    db: Session = Depends(get_db)
):
    """Cria um novo produto placeholder"""
    try:
        return create_product_placeholder(product_data, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[ProductPlaceholderReadList])
def get_all_product_placeholders_route(db: Session = Depends(get_db)):
    """Retorna todos os produtos placeholder"""
    try:
        return get_all_product_placeholders(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{product_id}", response_model=ProductPlaceholderRead)
def get_product_placeholder_route(product_id: str, db: Session = Depends(get_db)):
    """Retorna um produto placeholder pelo ID"""
    try:
        product = get_product_placeholder_by_id(product_id, db)
        if not product:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        return product
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{product_id}", response_model=ProductPlaceholderRead)
def update_product_placeholder_route(
    product_id: str,
    product_data: ProductPlaceholderUpdate,
    db: Session = Depends(get_db)
):
    """Atualiza um produto placeholder"""
    try:
        product = update_product_placeholder(product_id, product_data, db)
        if not product:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        return product
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{product_id}", response_model=ProductPlaceholderDelete)
def delete_product_placeholder_route(product_id: str, db: Session = Depends(get_db)):
    """Remove um produto placeholder"""
    try:
        delete_product_placeholder(product_id, db)
        return {"message": "Produto removido com sucesso"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
