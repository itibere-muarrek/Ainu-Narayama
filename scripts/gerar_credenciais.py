"""
Gera logins e senhas dos beta testers do ainu.systems (Visitor1..Visitor6).

Saídas (nenhuma entra no git; ficam em ~/ainu_credenciais/):
  - senhas_AAAAMMDD.txt: SENHAS em texto, para o administrador entregar cada
    uma à pessoa por um canal separado.
  - AINU_USERS_AAAAMMDD.json: HASHES, para colar na variável de ambiente
    AINU_USERS do serviço "ainu-systems" no painel do Render (Environment).
    Não contém senhas, só hashes PBKDF2 com sal individual.

Rodar de novo gera senhas NOVAS para todos (as antigas deixam de valer assim
que o AINU_USERS novo for aplicado).

Uso: python scripts/gerar_credenciais.py [--usuarios 6] [--saida CAMINHO]
"""

import argparse
import json
import secrets
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.senha import gerar_hash  # noqa: E402


def senha_forte() -> str:
    # 16 caracteres, sem símbolos ambíguos (0/O, 1/l/I) — fácil de ditar e digitar
    alfabeto = "ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789"
    return "".join(secrets.choice(alfabeto) for _ in range(16))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--usuarios", type=int, default=6)
    ap.add_argument("--saida", type=Path, default=None)
    ap.add_argument("--imprimir", action="store_true", help="também imprime o JSON de hashes no terminal")
    a = ap.parse_args()

    pasta = a.saida or (Path.home() / "ainu_credenciais")
    pasta.mkdir(parents=True, exist_ok=True)
    arquivo = pasta / f"senhas_{date.today():%Y%m%d}.txt"

    senhas = {f"Visitor{i}": senha_forte() for i in range(1, a.usuarios + 1)}
    hashes = {u: gerar_hash(s) for u, s in senhas.items()}

    arquivo.write_text("\n".join(f"{u}\t{s}" for u, s in senhas.items()) + "\n", encoding="utf-8")
    arq_hashes = pasta / f"AINU_USERS_{date.today():%Y%m%d}.json"
    arq_hashes.write_text(json.dumps(hashes, separators=(",", ":")), encoding="utf-8")
    print(f"[ok] senhas em texto:    {arquivo}")
    print("     (fora do repositório; entregue cada uma por canal separado)")
    print(f"[ok] hashes p/ o Render: {arq_hashes}")
    print("     -> Render > ainu-systems > Environment > variável AINU_USERS = conteúdo desse arquivo")
    if a.imprimir:
        print(json.dumps(hashes, separators=(",", ":")))


if __name__ == "__main__":
    main()
