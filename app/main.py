from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.product_placeholder_routes import router as product_placeholder_router
from app.routes.establishment_routes import router as establishment_router
from app.routes.promotion_routes import router as promotion_router
from app.routes.product_routes import router as product_router
from app.database.session import create_tables

app = FastAPI(title="Web Scraping API")

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registra as rotas
app.include_router(product_placeholder_router)
app.include_router(establishment_router)
app.include_router(promotion_router)
app.include_router(product_router)

# Cria as tabelas do banco de dados
create_tables()

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API de Web Scraping"}