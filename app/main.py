from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routes.category_routes import api_router
from app.database.session import create_db_and_tables

app = FastAPI()

app.include_router(api_router)

async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)