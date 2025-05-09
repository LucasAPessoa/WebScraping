from sqlmodel import create_engine, Session, SQLModel

DATABASE_URL = "postgresql+psycopg2://postgres:teste123@localhost:5432/webscraper"

engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session