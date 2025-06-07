from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.models import Base

# Configuração do banco de dados
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:teste123@localhost:5432/webscraping"

# Cria o engine do SQLAlchemy
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Cria a sessão do SQLAlchemy
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Função para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Função para criar as tabelas do banco de dados
def create_tables():
    Base.metadata.create_all(bind=engine)

# Função para recriar as tabelas do banco de dados
def recreate_tables():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)