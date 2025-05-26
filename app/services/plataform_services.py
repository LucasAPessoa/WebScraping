from sqlmodel import Session
from app.schemas.plataform_schema import PlataformCreate, PlataformRead, PlataformUpdate, PlataformReadList
from app.repositories.plataform_repository import PlataformRepository
from fastapi import HTTPException
from uuid import UUID

class PlataformService:

    def __init__(self, session: Session):
        self.session = session
        self.plataform_repository = PlataformRepository(session)

    def create_plataform(self, plataform_create: PlataformCreate) -> PlataformRead:
        name = plataform_create.name.strip()

        if not name:
            raise HTTPException(status_code=400, detail="O nome é obrigatório.")
        if len(name) > 100:
            raise HTTPException(status_code=400, detail="O nome deve ter no máximo 100 caracteres.")

        existing = self.plataform_repository.get_plataform_by_name(name)
        if existing:
            raise HTTPException(status_code=400, detail="Plataforma já cadastrada.")

        return self.plataform_repository.create_plataform(plataform_create)

    def update_plataform(self, plataform_id: str, plataform_update: PlataformUpdate) -> PlataformRead:
        try:
            plataform_uuid = UUID(plataform_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="ID de plataforma inválido.")

        existing = self.plataform_repository.get_plataform_by_id(plataform_uuid)
        if not existing:
            raise HTTPException(status_code=404, detail="Plataforma não encontrada.")

        name = plataform_update.name.strip()
        if not name:
            raise HTTPException(status_code=400, detail="O nome é obrigatório.")
        if len(name) > 100:
            raise HTTPException(status_code=400, detail="O nome deve ter no máximo 100 caracteres.")

        name_exists = self.plataform_repository.get_plataform_by_name(name)
        if name_exists and name_exists.id != plataform_uuid:
            raise HTTPException(status_code=400, detail="Outra plataforma com este nome já existe.")

        return self.plataform_repository.update_plataform(plataform_uuid, plataform_update)

    def delete_plataform(self, plataform_id: str) -> None:
        try:
            plataform_uuid = UUID(plataform_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="ID de plataforma inválido.")

        plataform = self.plataform_repository.get_plataform_by_id(plataform_uuid)
        if not plataform:
            raise HTTPException(status_code=404, detail="Plataforma não encontrada.")

        self.plataform_repository.delete_plataform(plataform_uuid)

    def get_plataform_by_id(self, plataform_id: str) -> PlataformRead:
        try:
            plataform_uuid = UUID(plataform_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="ID de plataforma inválido.")

        plataform = self.plataform_repository.get_plataform_by_id(plataform_uuid)
        if not plataform:
            raise HTTPException(status_code=404, detail="Plataforma não encontrada.")

        return plataform

    def get_all_plataforms(self) -> PlataformReadList:
        plataforms = self.plataform_repository.get_all_plataforms()
        if not plataforms:
            raise HTTPException(status_code=404, detail="Nenhuma plataforma encontrada.")

        plataform_read_list = [PlataformRead.model_validate(p) for p in plataforms]
        return PlataformReadList(plataforms=plataform_read_list)
