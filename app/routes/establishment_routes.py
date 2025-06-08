from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.database.session import get_db
from app.controllers.establishment_controller import (
    create_establishment,
    update_establishment,
    delete_establishment,
    get_establishment_by_id,
    get_all_establishments,
    filter_establishments
)
from app.schemas.establishment_schema import (
    EstablishmentCreate,
    EstablishmentUpdate,
    EstablishmentRead,
    EstablishmentReadList,
    EstablishmentDelete
)
from typing import List
from app.core.logger import get_logger
from app.models.models import Establishment

router = APIRouter(prefix="/establishments", tags=["establishments"])
logger = get_logger(__name__)

@router.post("/", response_model=EstablishmentRead)
def create_establishment_route(
    establishment_data: EstablishmentCreate,
    db: Session = Depends(get_db)
):
    """Cria um novo produto placeholder"""
    logger.debug(f"Creating new establishment with data: {establishment_data.dict()}")
    try:
        return create_establishment(establishment_data, db)
    except Exception as e:
        logger.debug(f"Error creating establishment: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=EstablishmentReadList)
def get_all_establishments_route(db: Session = Depends(get_db)):
    """Retorna todos os estabelecimentos"""
    logger.debug(f"Fetching establishments with skip=0 and limit=100")
    establishments = get_all_establishments(db)
    return establishments

@router.get("/{establishment_id}", response_model=EstablishmentRead)
def get_establishment_route(establishment_id: str, db: Session = Depends(get_db)):
    """Retorna um estabelecimento pelo ID"""
    logger.debug(f"Fetching establishment with id: {establishment_id}")
    establishment = get_establishment_by_id(establishment_id, db)
    if not establishment:
        logger.debug(f"Establishment with id {establishment_id} not found")
        raise HTTPException(status_code=404, detail="Estabelecimento não encontrado")
    return establishment

@router.put("/{establishment_id}", response_model=EstablishmentRead)
def update_establishment_route(
    establishment_id: str,
    establishment_data: EstablishmentUpdate,
    db: Session = Depends(get_db)
):
    """Atualiza um estabelecimento"""
    logger.debug(f"Updating establishment {establishment_id} with data: {establishment_data.dict()}")
    establishment = update_establishment(establishment_id, establishment_data, db)
    if not establishment:
        logger.debug(f"Establishment with id {establishment_id} not found for update")
        raise HTTPException(status_code=404, detail="Estabelecimento não encontrado")
    logger.debug(f"Successfully updated establishment {establishment_id}")
    return establishment

@router.delete("/{establishment_id}", response_model=EstablishmentDelete)
def delete_establishment_route(establishment_id: str, db: Session = Depends(get_db)):
    """Remove um estabelecimento"""
    logger.debug(f"Attempting to delete establishment {establishment_id}")
    delete_establishment(establishment_id, db)
    logger.debug(f"Successfully deleted establishment {establishment_id}")
    return {"message": "Estabelecimento removido com sucesso"}
