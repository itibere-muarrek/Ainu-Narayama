"""Triagem dos números dos instrumentos de política contra o texto das fontes (nível L1 e misto).

Para cada instrumento, pega os números escritos em valor, custo fiscal e beneficiários e procura cada um no texto completo das
fontes do instrumento (HTML até 3 MB; PDF inteiro via pdftotext). Um número "bate" se a sequência de algarismos significativos dele
aparece como começo de algum número do texto, em qualquer formato (1.234,5 ou 1,234.5), ou como percentual igual. Isso cobre arredondamento
e mudança de unidade (R$ 160 bi no texto, 160.xxx milhões na fonte), mas pode dar falso positivo para números curtos: por isso só números com
3 ou mais algarismos significativos, ou percentuais, entram, e o que não bate vai para leitura manual.

Resultado: privado/conferencia_numeros.json e .md. É triagem, não prova: "bate" diz que o número existe na fonte, não que é o do item citado.
Uso: python scripts/diretorio/conferir_numeros.py
"""
from __future__ import annotations

import json
import re
import subprocess
import tempfile
import urllib.request
from datetime import datetime
from pathlib import Path

from testar_links import UA

RAIZ = Path(__file__).resolve().parents[2]
PRI = RAIZ / "data" / "diretorio" / "privado"

# instrumentos sem IDs de evidência no registro, com as fontes lidas nas rodadas anteriores (endereços já usados na pesquisa)
EXTRA = {
    "FRA|Allocations familiales": ["https://www.caf.fr/sites/default/files/medias/cnaf/Professionnels/Actualites/2025/Rapport%20d'activit%C3%A9%202024/250194_Rapport%20d%E2%80%99activit%C3%A9%20de%20la%20branche%20Famille%202024_v5%20M%20planches.pdf",
                                   "https://www.caf.fr/professionnels/etudes-et-international/7-en-2024-les-depenses-de-prestations-pour-l-entretien-et-l-education-de-l-enfant-augmentent-de-34"],
    "CHN|Subsídio de criação de filhos": ["https://www.shanghai.gov.cn/nw4411/20250731/c35108cbd7ad4b3487fbd170ef07be8b.html"],
    "ITA|Assegno Unico": ["https://www.inps.it/content/dam/inps-site/pdf/dati-analisi-bilanci/osservatori-statistici/osservatorio-auu/Osservatorio_AUU_gennaio_2026.pdf"],
    "KOR|Abono infantil": ["https://www.korea.kr/news/policyNewsView.do?newsId=148960222"],
}


def baixar_texto(url: str) -> str:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
        with urllib.request.urlopen(req, timeout=60) as r:
            tipo = (r.headers.get("Content-Type") or "").lower()
            corpo = r.read(60_000_000)
        if "pdf" in tipo or url.lower().split("?")[0].endswith(".pdf"):
            with tempfile.TemporaryDirectory() as d:
                a = Path(d) / "x.pdf"
                a.write_bytes(corpo)
                return subprocess.run(["pdftotext", "-enc", "UTF-8", str(a), "-"], capture_output=True, timeout=180).stdout.decode("utf-8", "ignore")
        if any(x in tipo for x in ("spreadsheet", "excel", "zip", "octet")):
            return ""
        t = corpo[:3_000_000].decode("utf-8", "ignore")
        return re.sub(r"<[^>]+>", " ", re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", t, flags=re.S | re.I))
    except Exception:
        return ""


def sig(tok: str) -> str:
    """Algarismos significativos: sem separadores, sem zeros à esquerda e à direita."""
    d = re.sub(r"\D", "", tok).strip("0")
    return d


def numeros_do_texto(t: str) -> set[str]:
    out = set()
    for m in re.finditer(r"\d[\d.,  ]*\d|\d", t):
        s = sig(m.group(0))
        if s:
            out.add(s)
    return out


def tokens_do_instrumento(texto: str) -> list[str]:
    texto = re.sub(r"AINU-[A-Z0-9]+-[A-Z0-9]+-\d{4}-\d{6}", " ", texto or "")
    texto = re.sub(r"\b(?:19|20)\d{2}\b(?:[/-]\d{2,4})?", " ", texto)               # anos, fora
    texto = re.sub(r"\bL[12]\b|\bFY\d{4}\b|\bGY\d{4}\b|\bart\. ?\d+\w*|\bLei \d[\d./]*|\bn[ºo°] ?\d+|\bR\d{5,}\b", " ", texto)
    toks = []
    for m in re.finditer(r"\d[\d.,]*\d|\d", texto):
        tok = m.group(0)
        if len(sig(tok)) >= 3 or re.match(r"^\s*%", texto[m.end():m.end() + 2]):
            toks.append(tok)
    return list(dict.fromkeys(toks))


def main():
    ins = json.loads((PRI / "instrumentos.json").read_text(encoding="utf-8"))["instrumentos"]
    fontes = {f["id"]: f for f in json.loads((PRI / "fontes.json").read_text(encoding="utf-8"))}
    cache: dict[str, set[str]] = {}
    resultados = []
    for it in ins:
        if it["nivel"] not in ("L1", "misto"):
            continue
        urls = [fontes[i]["url"] for i in (it.get("evidencias") or []) if i in fontes and fontes[i].get("url")]
        for k, v in EXTRA.items():
            iso, pref = k.split("|")
            if it["iso"] == iso and it["instrumento"].startswith(pref):
                urls += v
        urls = list(dict.fromkeys(urls))
        toks = tokens_do_instrumento(" ".join(x or "" for x in (it["valor"], it["custo_fiscal"], it["beneficiario"])))
        if not urls or not toks:
            resultados.append({"iso": it["iso"], "instrumento": it["instrumento"], "estado": "sem_fonte_ou_numeros", "urls": urls, "n": len(toks)})
            continue
        base: set[str] = set()
        lidas = []
        for u in urls:
            if u not in cache:
                cache[u] = numeros_do_texto(baixar_texto(u))
            if cache[u]:
                lidas.append(u)
            base |= cache[u]
        if not lidas:
            resultados.append({"iso": it["iso"], "instrumento": it["instrumento"], "estado": "fonte_nao_lida", "urls": urls, "n": len(toks), "numeros": toks})
            continue
        ach, falt = [], []
        for t in toks:
            s = sig(t)
            ok = s in base or any(b.startswith(s) for b in base if len(b) >= len(s)) if len(s) >= 3 else s in base
            (ach if ok else falt).append(t)
        resultados.append({"iso": it["iso"], "instrumento": it["instrumento"], "estado": "ok" if not falt else "revisar", "urls": lidas, "n": len(toks), "batem": ach, "nao_batem": falt})
    out = {"conferido_em": datetime.now().isoformat(timespec="seconds"), "itens": resultados}
    (PRI / "conferencia_numeros.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    cont: dict[str, int] = {}
    for r in resultados:
        cont[r["estado"]] = cont.get(r["estado"], 0) + 1
    linhas = [f"# Conferência de números dos instrumentos ({out['conferido_em'][:10]})", "", str(cont), ""]
    for r in resultados:
        if r["estado"] == "ok":
            linhas.append(f"- OK  {r['iso']} | {r['instrumento'][:60]} | {len(r['batem'])}/{r['n']} números batem")
    for est in ("revisar", "fonte_nao_lida", "sem_fonte_ou_numeros"):
        linhas += ["", f"## {est}", ""]
        for r in resultados:
            if r["estado"] == est:
                linhas.append(f"- {r['iso']} | {r['instrumento'][:70]} | não batem: {', '.join(r.get('nao_batem', r.get('numeros', [])))} | batem: {len(r.get('batem', []))}")
    (PRI / "conferencia_numeros.md").write_text("\n".join(linhas), encoding="utf-8")
    print(cont)


if __name__ == "__main__":
    main()
