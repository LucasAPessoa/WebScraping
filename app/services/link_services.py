from sqlmodel import Session
from app.schemas.link_schema import LinkCreate, LinkRead, LinkUpdate, LinkReadList
from app.repositories.link_repository import LinkRepository
from fastapi import HTTPException
from uuid import UUID
import re

class LinkService:
    
    def __init__(self, session: Session):
        self.session = session
        self.link_repository = LinkRepository(session)
    
    def create_link(self, link_create: LinkCreate) -> LinkRead:
        
        url = link_create.url.strip()
        if not url:
            raise HTTPException(status_code=400, detail="O URL é obrigatório.")
        
        if len(url) > 200:
            raise HTTPException(status_code=400, detail="O URL deve ter no máximo 200 caracteres.")
        if not re.match(r'^(http|https)://', url):
            raise HTTPException(status_code=400, detail="O URL deve começar com http:// ou https://")
        
        existing_link = self.link_repository.get_link_by_url(url)
        if existing_link:
            raise HTTPException(status_code=400, detail="Link já existe.")
        
        return self.link_repository.create_link(link_create)
    
    def update_link(self, link_id: str, link_update: LinkUpdate) -> LinkRead:
        try:
            link_uuid = UUID(link_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="ID de link inválido.")
        
        link = self.link_repository.get_link_by_id(link_uuid)
        if not link:
            raise HTTPException(status_code=404, detail="Link não encontrado.")
        
        url = link_update.url.strip()
        if not url:
            raise HTTPException(status_code=400, detail="O URL é obrigatório.")
        
        if len(url) > 200:
            raise HTTPException(status_code=400, detail="O URL deve ter no máximo 200 caracteres.")
        if not re.match(r'^(http|https)://', url):
            raise HTTPException(status_code=400, detail="O URL deve começar com http:// ou https://")
        
        existing_link = self.link_repository.get_link_by_url(url)
        if existing_link and existing_link.id != link_uuid:
            raise HTTPException(status_code=400, detail="Link já existe.")
        
        return self.link_repository.update_link(link_uuid, link_update)
    
    def delete_link(self, link_id: str) -> None:
        try:
            link_uuid = UUID(link_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="ID de link inválido.")
        
        link = self.link_repository.get_link_by_id(link_uuid)
        if not link:
            raise HTTPException(status_code=404, detail="Link não encontrado.")
        
        self.link_repository.delete_link(link_uuid)
        
    def get_link_by_id(self, link_id: str) -> LinkRead:
        try:
            link_uuid = UUID(link_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="ID de link inválido.")
        
        link = self.link_repository.get_link_by_id(link_uuid)
        if not link:
            raise HTTPException(status_code=404, detail="Link não encontrado.")
        
        return link
    
    def get_all_links(self) -> LinkReadList:
        links = self.link_repository.get_all_links()
        
        if not links:
            raise HTTPException(status_code=404, detail="Nenhum link encontrado.")
        
        link_read_list = [LinkRead.model_validate(link) for link in links]
        return LinkReadList(links=link_read_list)