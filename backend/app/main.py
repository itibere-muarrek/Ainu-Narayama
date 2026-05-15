from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.database import init_db
from app.api.v1 import auth, paises, calculo, simulacoes, admin
from app.config import get_settings
from agente.scheduler import iniciar_scheduler, parar_scheduler

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup e shutdown da aplicação"""
    # Startup
    init_db()
    print("✓ Banco de dados inicializado")

    # Inicia agente coletor automático
    iniciar_scheduler()
    print("✓ Agente coletor semanal iniciado")

    yield

    # Shutdown
    parar_scheduler()
    print("✓ Agente coletor parado")
    print("✓ Aplicação encerrada")


app = FastAPI(
    title="AINU-Narayama API",
    description="Backend para Sistema de Medição Socioeconômica",
    version="3.1.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção: ["https://narayama.live", "https://frontend.example.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rotas
app.include_router(auth.router, prefix="/api/v1")
app.include_router(paises.router, prefix="/api/v1")
app.include_router(calculo.router, prefix="/api/v1")
app.include_router(simulacoes.router, prefix="/api/v1")
app.include_router(admin.router, prefix="/api/v1")


@app.get("/", tags=["root"])
async def root():
    """Root endpoint"""
    return {
        "name": "AINU-Narayama API",
        "version": "3.1.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "environment": settings.environment
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.environment == "development"
    )
