from fastapi import FastAPI
from app.routes.category_routes import category_router
from app.routes.promotion_routes import promotion_router
from app.routes.link_routes import link_router
from app.routes.establishment_routes import establishment_router
from app.database.session import create_db_and_tables
from contextlib import asynccontextmanager

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     await create_db_and_tables()
#     yield

# app = FastAPI(lifespan=lifespan)

app = FastAPI()

app.include_router(category_router)
app.include_router(promotion_router)
app.include_router(link_router)
app.include_router(establishment_router)
