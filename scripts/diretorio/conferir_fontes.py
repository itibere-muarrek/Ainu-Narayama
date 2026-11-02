"""Conferência de conteúdo das fontes do Diretório (complementa testar_links.py).

Para cada endereço único de fontes.json: baixa só o começo (HTML até 400 KB; PDF até 20 MB, lendo as 3 primeiras páginas com
pdftotext) e procura nas páginas as palavras da descrição da fonte (siglas, nomes próprios, anos, códigos de séries).
Resultado: privado/conferencia_fontes.json e privado/conferencia_fontes.md, com três estados:

  confere        a página contém a maior parte dos termos da descrição
  revisar        poucos termos encontrados: abrir à mão
  nao_verificavel página sem texto lido (JavaScript, PDF digitalizado, bloqueio, tempo esgotado)

É uma triagem automática: "confere" diz que a página trata do assunto, não que o número citado está nela.
Leitura somente, mesma identificação e limites do testar_links.py. Bloqueios não são contornados.

Uso: python scripts/diretorio/conferir_fontes.py
"""
from __future__ import annotations

import json
import re
import subprocess
import tempfile
import unicodedata
import urllib.request
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path

from testar_links import UA, _semaforo

import urllib.parse

RAIZ = Path(__file__).resolve().parents[2]
DADOS = RAIZ / "data" / "diretorio"
LIMITE_HTML = 400_000
LIMITE_PDF = 20_000_000
PARADA = {"dados", "para", "pela", "pelo", "como", "mais", "sobre", "entre", "desta", "nesta", "series", "serie", "total", "pesquisa", "tabelas", "tabela",
          "base", "anos", "ano", "fonte", "fontes", "microdados", "arquivo", "local", "lido", "oficial", "documento", "caso", "sem", "com", "dos", "das",
          "nos", "nas", "aba", "abas", "citantes", "descrita", "disponivel", "pais", "paises", "uso", "ainu", "L1", "L2"}


def sem_acento(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c)).lower()


def termos(textos: list[str]) -> list[str]:
    """Siglas, nomes próprios, anos e códigos de série dos textos de descrição (sem IDs AINU-...)."""
    bruto = " ".join(textos)
    bruto = re.sub(r"AINU-[A-Z0-9]+-[A-Z0-9]+-\d{4}-\d{6}", " ", bruto)
    bruto = re.sub(r"\((?:[^()]*L[12][^()]*)\)", " ", bruto)
    achados = set()
    for m in re.finditer(r"[A-Z][A-Za-zÀ-ÿ0-9_.]{2,}|[A-Z]{2,}[A-Z0-9_.]*|\b(?:19|20)\d{2}\b", bruto):
        t = sem_acento(m.group(0).strip("."))
        if t and t not in PARADA and len(t) >= 3:
            achados.add(t)
    return sorted(achados)


def baixar(url: str) -> tuple[str, str | None]:
    """(texto, erro). PDF: 3 primeiras páginas via pdftotext; HTML: texto do começo."""
    host = urllib.parse.urlsplit(url).netloc
    with _semaforo(host):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
            with urllib.request.urlopen(req, timeout=30) as r:
                tipo = (r.headers.get("Content-Type") or "").lower()
                if "pdf" in tipo or url.lower().split("?")[0].endswith(".pdf"):
                    corpo = r.read(LIMITE_PDF)
                    with tempfile.TemporaryDirectory() as d:
                        arq = Path(d) / "x.pdf"
                        arq.write_bytes(corpo)
                        out = subprocess.run(["pdftotext", "-l", "3", "-enc", "UTF-8", str(arq), "-"], capture_output=True, timeout=60)
                        return out.stdout.decode("utf-8", "ignore"), None
                if any(x in tipo for x in ("csv", "excel", "spreadsheet", "octet-stream", "zip")):
                    return r.read(4000).decode("utf-8", "ignore"), None
                corpo = r.read(LIMITE_HTML).decode("utf-8", "ignore")
                corpo = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", corpo, flags=re.S | re.I)
                return re.sub(r"<[^>]+>", " ", corpo), None
        except Exception as ex:
            return "", type(ex).__name__ + ": " + str(getattr(ex, "reason", ex))[:80]


def avaliar(item):
    url, desc = item
    texto, erro = baixar(url)
    tx = sem_acento(re.sub(r"\s+", " ", texto))
    ts = termos(desc)
    if erro or len(tx) < 300 or not ts:
        return url, {"estado": "nao_verificavel", "motivo": erro or ("pouco texto lido" if len(tx) < 300 else "sem termos na descrição"), "termos": ts}
    ach = [t for t in ts if t in tx]
    frac = len(ach) / len(ts)
    return url, {"estado": "confere" if frac >= 0.34 or len(ach) >= 3 else "revisar", "fracao": round(frac, 2), "achados": ach[:12], "faltam": [t for t in ts if t not in tx][:12]}


def main():
    fontes = json.loads((DADOS / "privado" / "fontes.json").read_text(encoding="utf-8"))
    ev = {x["id"]: x for x in json.loads((DADOS / "privado" / "evidencias.json").read_text(encoding="utf-8"))}
    desc: dict[str, list[str]] = defaultdict(list)
    ids: dict[str, list[str]] = defaultdict(list)
    for f in fontes:
        if not f.get("url"):
            continue
        e = ev.get(f["id"])
        desc[f["url"]].append(f["descricao"])
        if e:
            desc[f["url"]] += [e["fonte"] or "", e["serie"] or "", e["variavel"] or ""]
        ids[f["url"]].append(f["id"])
    itens = [(u, d) for u, d in desc.items() if "rplumber.ilo.org" not in u]            # a API da OIT devolve CSV: conferida ao baixar os dados
    with ThreadPoolExecutor(max_workers=8) as ex:
        res = dict(ex.map(avaliar, itens))
    out = {"conferido_em": datetime.now().isoformat(timespec="seconds"), "agente": UA, "urls": {u: {**r, "ids": ids[u][:6], "n_ids": len(ids[u])} for u, r in res.items()}}
    (DADOS / "privado" / "conferencia_fontes.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    cont = defaultdict(int)
    for r in res.values():
        cont[r["estado"]] += 1
    linhas = [f"# Conferência de conteúdo das fontes ({out['conferido_em'][:10]})", "", f"{len(res)} endereços: " + ", ".join(f"{k} {v}" for k, v in sorted(cont.items())), ""]
    for est in ("revisar", "nao_verificavel"):
        linhas += ["", f"## {est}", ""]
        for u, r in res.items():
            if r["estado"] == est:
                linhas.append(f"- {u}  ({len(ids[u])} fontes; {r.get('motivo') or 'faltam: ' + ', '.join(r.get('faltam', []))})")
    (DADOS / "privado" / "conferencia_fontes.md").write_text("\n".join(linhas), encoding="utf-8")
    print(dict(cont))


if __name__ == "__main__":
    main()
