from typing import List
from uuid import UUID, uuid4
from sqlmodel import Session, select

from app.models.models import Plataform
from app.schemas.plataform_schema import PlataformCreate, PlataformRead, PlataformUpdate

class PlataformRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_plataform(self, plataform_create: PlataformCreate) -> PlataformRead:
        plataform = Plataform(
            id=uuid4(),
            name=plataform_create.name.strip(),
        )
        self.session.add(plataform)
        self.session.commit()
        self.session.refresh(plataform)
        return plataform

    def get_plataform_by_id(self, plataform_id: UUID) -> Plataform | None:
        return self.session.get(Plataform, plataform_id)

    def get_plataform_by_name(self, name: str) -> Plataform | None:
        return self.session.exec(
            select(Plataform).where(Plataform.name.ilike(f"%{name.lower()}%"))
        ).first()

    def get_all_plataforms(self) -> List[Plataform]:
        result = self.session.exec(select(Plataform))
        return result.all()

    def update_plataform(self, plataform_id: UUID, plataform_update: PlataformUpdate) -> PlataformRead | None:
        plataform = self.session.get(Plataform, plataform_id)

        if not plataform:
            return None

        for key, value in plataform_update.model_dump().items():
            setattr(plataform, key, value)

        self.session.commit()
        self.session.refresh(plataform)
        return plataform

    def delete_plataform(self, plataform_id: UUID) -> None:
        plataform = self.session.get(Plataform, plataform_id)
        if plataform:
            self.session.delete(plataform)
            self.session.commit()
