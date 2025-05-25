from typing import List
from uuid import UUID, uuid4
from sqlmodel import Session, select

from app.models.models import Link
from app.schemas.link_schema import LinkCreate, LinkRead, LinkUpdate, LinkReadList

class LinkRepository:
    def __init__(self, session: Session):
        self.session = session
        
    def create_link(self, link_create: LinkCreate) -> LinkRead:
        link = Link(
            id=uuid4(),
            url=link_create.url.strip(),
        )
        self.session.add(link)
        self.session.commit()
        self.session.refresh(link)
        return link
    
    def get_link_by_id(self, link_id: UUID) -> Link | None:
        return self.session.get(Link, link_id)
    
    def get_link_by_url(self, url: str) -> Link | None:
        return self.session.exec(
            select(Link).where(Link.url.ilike(f"%{url.lower()}%"))
        ).first()
        
    def get_all_links(self) -> List[Link]:
        result = self.session.exec(select(Link))
        return result.all()
    
    def update_link(self, link_id: UUID, link_update: LinkUpdate) -> LinkRead | None:
        link = self.session.get(Link, link_id)
        
        if not link:
            return None
        
        for key, value in link_update.model_dump().items():
            setattr(link, key, value)
        
        self.session.commit()
        self.session.refresh(link)
        return link
    
    def delete_link(self, link_id: UUID) -> None:
        link = self.session.get(Link, link_id)
        if link:
            self.session.delete(link)
            self.session.commit()