from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
import json

from ..database import get_db

router = APIRouter()

PAISES_DATA_PATH = "../frontend/data/paises_narayama.json"


class PaisResponse(BaseModel):
    id: int
    pais: str
    pop_base: float
    pop_topo: float
    nasc: float
    mortes: float
    tfr_atual: float
    tfr_1999: float
    ncii: float
    L: float
    A_ext: float
    T: float
    U: float
    M: float
    I: float
    n_star: float
    status_n: str
    nih: float
    nsii: float
    ies: float
    status_ies: str

    class Config:
        from_attributes = True


def load_paises():
    try:
        with open("frontend/data/paises_narayama.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []


def calcular_n_star(pais_data):
    pop_base = pais_data.get("pop_base", 1)
    pop_topo = pais_data.get("pop_topo", 1)
    nasc = pais_data.get("nasc", 1)
    mortes = pais_data.get("mortes", 0.1)
    tfr_atual = pais_data.get("tfr_atual", 1)
    tfr_1999 = pais_data.get("tfr_1999", 1)

    NGII_Puro = (pop_base / pop_topo) * (nasc / mortes)
    Fator_Geracional = tfr_atual / tfr_1999
    n_star = NGII_Puro * Fator_Geracional

    return round(n_star, 3)


def get_status_n(n_star):
    if n_star > 1.3:
        return "PROMISSOR"
    elif 0.9 <= n_star <= 1.3:
        return "EQUILÍBRIO"
    elif 0.5 <= n_star < 0.9:
        return "CRÍTICO"
    else:
        return "COLAPSO"


def calcular_ies(pais_data):
    L = pais_data.get("L", 0.5)
    NGII = (pais_data.get("pop_base", 1) / pais_data.get("pop_topo", 1))
    NCII = pais_data.get("ncii", 1)

    T = pais_data.get("T", 0.05)
    U = pais_data.get("U", 0.07)
    M = pais_data.get("M", 0.06)
    I = pais_data.get("I", 0.01)

    NIH = max(0.35, min(0.85, 1 - (0.35*T + 0.25*U + 0.20*M + 0.20*I)))
    A_ext = pais_data.get("A_ext", 0.5)
    NSII = 0.45*A_ext + 0.55*NIH

    ies = L * (NGII * NCII * NSII) ** (1/3)

    return round(ies, 3)


def get_status_ies(ies):
    if ies > 0.8:
        return "SAUDÁVEL"
    elif 0.6 <= ies <= 0.8:
        return "ESTÁVEL"
    elif 0.4 <= ies < 0.6:
        return "FRÁGIL"
    else:
        return "CRÍTICO"


@router.get("/", response_model=List[PaisResponse])
def listar_paises(db: Session = Depends(get_db)):
    paises = load_paises()
    return paises


@router.get("/{pais_id}", response_model=PaisResponse)
def get_pais(pais_id: int, db: Session = Depends(get_db)):
    paises = load_paises()
    for pais in paises:
        if pais["id"] == pais_id:
            return pais
    raise HTTPException(status_code=404, detail="País não encontrado")


@router.get("/status/promissores", response_model=List[PaisResponse])
def paises_promissores(db: Session = Depends(get_db)):
    paises = load_paises()
    return [p for p in paises if p.get("status_n") == "PROMISSOR"]


@router.get("/status/criticos", response_model=List[PaisResponse])
def paises_criticos(db: Session = Depends(get_db)):
    paises = load_paises()
    return [p for p in paises if p.get("status_n") == "CRÍTICO"]


@router.get("/status/colapso", response_model=List[PaisResponse])
def paises_colapso(db: Session = Depends(get_db)):
    paises = load_paises()
    return [p for p in paises if p.get("status_n") == "COLAPSO"]
