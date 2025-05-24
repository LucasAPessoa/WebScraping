from fastapi import FastAPI
from app.routes.category_routes import category_router
from app.routes.promotion_routes import promotion_router
from app.database.session import create_db_and_tables
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(category_router)
app.include_router(promotion_router)