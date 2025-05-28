from fastapi import FastAPI
from app.routes.category_routes import category_router
from app.routes.promotion_routes import promotion_router
from app.routes.link_routes import link_router
from app.routes.establishment_routes import establishment_router
from app.routes.plataform_routes import plataform_router
from app.routes.product_placeholder_routes import product_placeholder_router
from app.routes.photo_routes import photo_router
from app.routes.product_routes import product_router
from app.routes.product_plataform_routes import product_plataform_router
from app.database.session import create_db_and_tables
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     await create_db_and_tables()
#     yield

# app = FastAPI(lifespan=lifespan)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ou especifique domínios ex: ["https://meusite.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
    )

app.include_router(category_router)
app.include_router(promotion_router)
app.include_router(link_router)
app.include_router(establishment_router)
app.include_router(plataform_router)
app.include_router(product_placeholder_router)
app.include_router(photo_router)
app.include_router(product_router)
app.include_router(product_plataform_router)