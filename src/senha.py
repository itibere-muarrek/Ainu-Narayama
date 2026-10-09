"""Hash e verificação de senhas (PBKDF2-SHA256 com sal individual).

Funções puras, sem Streamlit — usadas por src/auth.py (app) e por
scripts/gerar_credenciais.py (administração), para os dois nunca divergirem.
"""

import hashlib
import hmac
import os

ITERACOES = 240_000


def gerar_hash(senha: str, iteracoes: int = ITERACOES) -> str:
    sal = os.urandom(16)
    h = hashlib.pbkdf2_hmac("sha256", senha.encode("utf-8"), sal, iteracoes)
    return f"pbkdf2_sha256${iteracoes}${sal.hex()}${h.hex()}"


def verificar_hash(senha: str, armazenado: str) -> bool:
    try:
        algoritmo, it, sal_hex, h_hex = armazenado.split("$")
        if algoritmo != "pbkdf2_sha256":
            return False
        calc = hashlib.pbkdf2_hmac("sha256", senha.encode("utf-8"), bytes.fromhex(sal_hex), int(it))
        return hmac.compare_digest(calc.hex(), h_hex)
    except (ValueError, TypeError):
        return False
