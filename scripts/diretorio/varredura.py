"""Varredura do Diretório: procura inconsistências nos dados publicáveis, nas páginas geradas e na conferência das fontes.

Não altera nada; imprime o que encontrou e sai com código 1 se houver problema grave (marcado ERRO).
Uso: python scripts/diretorio/varredura.py   (depois de exportar_diretorio.py, testar_links.py, conferir_fontes.py e gerar_fichas.py)
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gerar_fichas as G  # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]
PUB = RAIZ / "data" / "diretorio" / "publicavel"
PREV = RAIZ / "data" / "diretorio" / "preview"
ler = lambda p: json.loads(p.read_text(encoding="utf-8"))
erros: list[str] = []
avisos: list[str] = []


def erro(m):
    erros.append(m)


def aviso(m):
    avisos.append(m)


# 1. links e conferência de conteúdo
fontes, refs = ler(PUB / "fontes.json"), ler(PUB / "referencias.json")
links = ler(PUB / "links_status.json")["links"]
auto = ler(PUB / "conferencia_fontes_estado.json")
man = {k for k in ler(PUB / "conferencia_manual.json") if not k.startswith("_")}
urls = {f["url"] for f in fontes if f.get("url")} | {r["url"] for r in refs}
sem_teste = [u for u in urls if u not in links]
if sem_teste:
    erro(f"{len(sem_teste)} endereços sem teste de link, p. ex. {sem_teste[0]}")
ruins = {u: links[u]["estado"] for u in urls if u in links and links[u]["estado"] not in ("ok", "redirecionado")}
for u, e in ruins.items():
    (aviso if u in man else erro)(f"link {e}: {u[:100]}" + ("" if u in man else "  (sem nota manual)"))
pend_conteudo = [u for u in urls if "rplumber.ilo.org" not in u and u not in man and auto.get(u, {}).get("estado") != "confere"]
for u in pend_conteudo:
    erro(f"conteúdo não conferido e sem nota manual: {u[:110]}")
sem_link = [f["id"] for f in fontes if f["url_status"] == "a_registrar"]
if sem_link:
    aviso(f"{len(sem_link)} fontes sem link: {', '.join(sem_link)}")

# 2. dados publicáveis: nada que não deva sair
for arq in sorted(PUB.glob("*.json")):
    t = arq.read_text(encoding="utf-8")
    if re.search(r"C:\\\\|LENOVO|i'M thinker|Documents\\\\", t):
        erro(f"{arq.name}: caminho local")
    if re.search(r"[\w.+-]+@[\w-]+\.[\w.]+", t):
        erro(f"{arq.name}: e-mail")
paises = ler(PUB / "paises.json")
for p in paises:
    if "n_star" in p:
        erro(f"{p['iso']}: campo n_star (N* antigo) na ficha publicável")
    for bloco in ("cobertura", "demografia", "consumo", "multiplicadores", "valorizacao"):
        for k, reg in p[bloco].items():
            if reg.get("nivel") == "L2" and not reg.get("retido"):
                erro(f"{p['iso']}.{bloco}.{k}: valor de nível L2 sem retenção")
for i in ler(PUB / "instrumentos.json")["instrumentos"]:
    if i["nivel"] not in ("L1", "misto"):
        erro(f"instrumento fora do filtro: {i['iso']} {i['instrumento'][:50]} ({i['nivel']})")

# 3. coerência entre simulacoes.json e as fichas
sim = ler(PUB / "simulacoes.json")["paises"]
for p in paises:
    v = p["valorizacao"]["dividendo_10pct_pib"].get("valor")
    s = sim[p["iso"]]["dividendo_10pct_pib"]
    if (v is None) != (s is None) or (v is not None and abs(v - s) > 1e-9):
        erro(f"{p['iso']}: Dividendo 10% difere entre a ficha ({v}) e simulacoes.json ({s})")

# 4. páginas: o modo "dados" não pode ter marcas de suposição, e o modo "suposicoes" não pode ter dados observados
G.EMBED = True
d = G.carregar()
chip = lambda h, n: len(re.findall(rf'class="chip c-{n}"', h))
for lang in ("pt", "en", "es", "fr", "it", "ko", "ja", "zh", "fi"):
    for p in paises:
        h = G.html_ficha(p["iso"], lang, "dados")
        for n in ("EST", "PROJ", "SIM"):
            if chip(h, n):
                erro(f"{p['iso']}/{lang}: ficha de dados com marca {n}")
        if "ASSUMPTIONS FOR RESEARCHERS" in h or "SUPOSIÇÕES PARA PESQUISADORES" in h:
            erro(f"{p['iso']}/{lang}: ficha de dados com o aviso de suposições")
        hs = G.html_ficha(p["iso"], lang, "suposicoes")
        for n in ("OBS", "DER"):
            if chip(hs, n):
                erro(f"{p['iso']}/{lang}: ficha de suposições com marca {n}")
    hi = G.html_indice(lang, "dados")
    if chip(hi, "SIM") or chip(hi, "PROJ") or chip(hi, "EST"):
        erro(f"índice de dados/{lang} com marca de suposição")
    hd = G.html_dados(lang)
    if "Dividendo de 10%" in hd or "10% Dividend" in hd.replace("<b", " "):
        aviso(f"dados verificáveis/{lang} cita o Dividendo (conferir se é só de fonte)")

# 5. IDs citados nas páginas existem no registro
ids_reg = {f["id"] for f in fontes} | {e["id"] for e in ler(PUB / "evidencias.json")}
citados = set()
for lang in ("pt", "en", "es", "fr", "it", "ko", "ja", "zh", "fi"):
    for p in paises:
        citados |= set(re.findall(r"AINU-[A-Z0-9]+-[A-Z0-9]+-\d{4}-\d{6}", G.html_ficha(p["iso"], lang, "dados")))
faltam = sorted(citados - ids_reg)
if faltam:
    aviso(f"{len(faltam)} IDs citados nas fichas sem registro em fontes/evidências (p. ex. {', '.join(faltam[:3])})")

# 6. prévia estática: links relativos apontam para arquivos que existem
for html_ in PREV.glob("*/*.html"):
    t = html_.read_text(encoding="utf-8")
    for alvo in set(re.findall(r"href='([A-Za-z_]+\.html)", t) + re.findall(r'href="([A-Za-z_]+\.html)', t)):
        if not (html_.parent / alvo).exists():
            erro(f"{html_.relative_to(PREV)}: link para {alvo}, que não existe")

print(f"ERROS: {len(erros)} | AVISOS: {len(avisos)}")
for m in erros:
    print("  ERRO  ", m)
for m in avisos:
    print("  aviso ", m)
sys.exit(1 if erros else 0)
