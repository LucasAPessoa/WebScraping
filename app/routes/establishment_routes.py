from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.controllers import establishment_controller
from app.schemas.establishment_schema import EstablishmentCreate, EstablishmentRead, EstablishmentUpdate, EstablishmentReadList
from app.database.session import get_session


establishment_router = APIRouter(prefix="/establishments", tags=["Establishments"])

@establishment_router.post("/", response_model=EstablishmentRead, status_code=status.HTTP_201_CREATED)
async def create_establishment(
    establishment_create: EstablishmentCreate, 
    session: Session = Depends(get_session)
):
    return establishment_controller.create_establishment(establishment_create, session)

@establishment_router.put("/{establishment_id}", response_model=EstablishmentRead, status_code=status.HTTP_200_OK)
def update_establishment(
    establishment_id: str, 
    establishment_update: EstablishmentUpdate, 
    session: Session = Depends(get_session)
):
    return establishment_controller.update_establishment(establishment_id, establishment_update, session)

@establishment_router.delete("/{establishment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_establishment(
    establishment_id: str, 
    session: Session = Depends(get_session)
):
    return establishment_controller.delete_establishment(establishment_id, session)

@establishment_router.get("/{establishment_id}", response_model=EstablishmentRead, status_code=status.HTTP_200_OK)
def get_establishment_by_id(
    establishment_id: str, 
    session: Session = Depends(get_session)
):
    return establishment_controller.get_establishment_by_id(establishment_id, session)

@establishment_router.get("/", response_model=EstablishmentReadList, status_code=status.HTTP_200_OK)
def get_establishments(
    session: Session = Depends(get_session)
):
    return establishment_controller.get_all_establishments(session)

