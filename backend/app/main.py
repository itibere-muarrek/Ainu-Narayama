from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import logging

from .database import init_db
from .routers import auth, paises, admin

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AINU.SYSTEMS v3.1.0",
    description="Agente Inteligente Narayama de Uniformização",
    version="3.1.0"
)

# CORS
ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:8501,http://localhost:3000,https://narayama.live"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar banco de dados
init_db()

# Routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(paises.router, prefix="/api/v1/paises", tags=["Paises"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["Admin"])


@app.get("/")
async def root():
    return {
        "message": "AINU.SYSTEMS v3.1.0",
        "status": "online",
        "docs": "/docs"
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
