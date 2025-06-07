from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.services.establishment_services import EstablishmentService
from app.repositories.establishment_repository import EstablishmentRepository
from app.schemas.establishment_schema import (
    EstablishmentCreate,
    EstablishmentUpdate,
    EstablishmentRead,
    EstablishmentReadList,
    EstablishmentDelete
)
from typing import List

router = APIRouter()

@router.post("/", response_model=EstablishmentRead)
def create_establishment(
    establishment_data: EstablishmentCreate,
    db: Session = Depends(get_db)
):
    """Cria um novo estabelecimento"""
    try:
        repository = EstablishmentRepository(db)
        service = EstablishmentService(repository)
        establishment = service.create_establishment(establishment_data)
        return establishment
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[EstablishmentReadList])
def get_all_establishments(db: Session = Depends(get_db)):
    """Retorna todos os estabelecimentos"""
    try:
        repository = EstablishmentRepository(db)
        service = EstablishmentService(repository)
        establishments = service.get_all_establishments()
        return establishments
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{establishment_id}", response_model=EstablishmentRead)
def get_establishment(establishment_id: str, db: Session = Depends(get_db)):
    """Retorna um estabelecimento pelo ID"""
    try:
        repository = EstablishmentRepository(db)
        service = EstablishmentService(repository)
        establishment = service.get_establishment_by_id(establishment_id)
        if not establishment:
            raise HTTPException(status_code=404, detail="Estabelecimento não encontrado")
        return establishment
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{establishment_id}", response_model=EstablishmentRead)
def update_establishment(
    establishment_id: str,
    establishment_data: EstablishmentUpdate,
    db: Session = Depends(get_db)
):
    """Atualiza um estabelecimento"""
    try:
        repository = EstablishmentRepository(db)
        service = EstablishmentService(repository)
        establishment = service.update_establishment(establishment_id, establishment_data)
        if not establishment:
            raise HTTPException(status_code=404, detail="Estabelecimento não encontrado")
        return establishment
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{establishment_id}", response_model=EstablishmentDelete)
def delete_establishment(establishment_id: str, db: Session = Depends(get_db)):
    """Remove um estabelecimento"""
    try:
        repository = EstablishmentRepository(db)
        service = EstablishmentService(repository)
        if not service.delete_establishment(establishment_id):
            raise HTTPException(status_code=404, detail="Estabelecimento não encontrado")
        return {"message": "Estabelecimento removido com sucesso"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_establishment_by_name(establishment_name: str, session: Session = Depends(get_db)):
    service = EstablishmentService(session)
    return service.get_establishment_by_name(establishment_name)

def get_establishment_by_url(establishment_url: str, session: Session = Depends(get_db)):
    service = EstablishmentService(session)
    return service.get_establishment_by_url(establishment_url)