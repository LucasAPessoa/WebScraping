from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.controllers import plataform_controller
from app.schemas.plataform_schema import PlataformCreate, PlataformRead, PlataformReadList, PlataformUpdate
from app.database.session import get_session

plataform_router = APIRouter(prefix="/plataforms", tags=["Plataforms"])

@plataform_router.post("/", response_model=PlataformRead, status_code=status.HTTP_201_CREATED)
async def create_plataform(plataform_create: PlataformCreate, session: Session = Depends(get_session)):
    return plataform_controller.create_plataform(plataform_create, session)

@plataform_router.put("/{plataform_id}", response_model=PlataformRead, status_code=status.HTTP_200_OK)
def update_plataform(
    plataform_id: str,
    plataform_update: PlataformUpdate,
    session: Session = Depends(get_session)
):
    return plataform_controller.update_plataform(plataform_id, plataform_update, session)

@plataform_router.delete("/{plataform_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_plataform(plataform_id: str, session: Session = Depends(get_session)):
    return plataform_controller.delete_plataform(plataform_id, session)

@plataform_router.get("/{plataform_id}", response_model=PlataformRead, status_code=status.HTTP_200_OK)
def get_plataform_by_id(plataform_id: str, session: Session = Depends(get_session)):
    return plataform_controller.get_plataform_by_id(plataform_id, session)

@plataform_router.get("/", response_model=PlataformReadList, status_code=status.HTTP_200_OK)
def get_plataforms(session: Session = Depends(get_session)):
    return plataform_controller.get_all_plataforms(session)
