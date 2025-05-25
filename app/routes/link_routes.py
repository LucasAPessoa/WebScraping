from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.controllers import link_controller
from app.schemas.link_schema import LinkCreate, LinkRead, LinkUpdate, LinkReadList
from app.database.session import get_session

link_router = APIRouter(prefix="/links", tags=["Links"])

@link_router.post("/", response_model=LinkRead, status_code=status.HTTP_201_CREATED)
async def create_link(link_create: LinkCreate, session: Session = Depends(get_session)):
    return link_controller.create_link(link_create, session)

@link_router.put("/{link_id}", response_model=LinkRead, status_code=status.HTTP_200_OK)
def update_link(
    link_id: str, 
    link_update: LinkUpdate, 
    session: Session = Depends(get_session)
):
    return link_controller.update_link(link_id, link_update, session)

@link_router.delete("/{link_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_link(link_id: str, session: Session = Depends(get_session)):
    return link_controller.delete_link(link_id, session)

@link_router.get("/{link_id}", response_model=LinkRead, status_code=status.HTTP_200_OK)
def get_link_by_id(link_id: str, session: Session = Depends(get_session)):
    return link_controller.get_link_by_id(link_id, session)

@link_router.get("/", response_model=LinkReadList, status_code=status.HTTP_200_OK)
def get_links(session: Session = Depends(get_session)):
    return link_controller.get_all_links(session)