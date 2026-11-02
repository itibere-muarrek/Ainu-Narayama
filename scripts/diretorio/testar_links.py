"""Testa os links de data/diretorio/publicavel/fontes.json e grava data/diretorio/privado/links_status.json.

Só leitura, uma requisição por endereço (HEAD; GET sem baixar o corpo se o servidor não aceitar HEAD), no máximo
2 conexões por servidor, com identificação honesta (sem fingir ser navegador). Bloqueios (401, 403, 429), erros de
certificado e tempo esgotado NÃO são contornados: ficam como "não verificado", sem concluir que o link está quebrado.

Estados:
  ok            respondeu 2xx (ou 3xx que termina em 2xx)
  redirecionado respondeu 2xx em outro endereço (guarda o endereço final)
  bloqueado     401, 403 ou 429: o servidor recusa robôs; o link pode abrir no navegador
  nao_encontrado 404 ou 410
  erro_servidor 5xx
  sem_resposta  tempo esgotado, DNS, conexão ou certificado
  nao_testado   não é http(s)

Uso: python scripts/diretorio/testar_links.py
"""
from __future__ import annotations

import json
import time
import ssl
import threading
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
DADOS = RAIZ / "data" / "diretorio"
UA = "AINU-Directory-linkcheck/1.0 (independent research; link availability check)"
TIMEOUT = 20
POR_SERVIDOR = 2

_sem: dict[str, threading.Semaphore] = defaultdict(lambda: threading.Semaphore(POR_SERVIDOR))
_trava = threading.Lock()


def _semaforo(host: str) -> threading.Semaphore:
    with _trava:
        return _sem[host]


def _pedido(url: str, metodo: str):
    req = urllib.request.Request(url, method=metodo, headers={"User-Agent": UA, "Accept": "*/*"})
    # cookies aceitos como qualquer cliente comum (alguns servidores respondem 302 com um cookie na primeira visita)
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(), urllib.request.HTTPSHandler(context=ssl.create_default_context()))
    return opener.open(req, timeout=TIMEOUT)


def testar(url: str) -> dict:
    if not url.lower().startswith(("http://", "https://")):
        return {"estado": "nao_testado", "codigo": None}
    host = urllib.parse.urlsplit(url).netloc
    with _semaforo(host):
        for metodo in ("HEAD", "GET"):
            try:
                with _pedido(url, metodo) as r:
                    final = r.geturl()
                    if metodo == "GET":
                        r.read(1)                                   # não baixa o arquivo inteiro
                    mudou = final.rstrip("/") != url.rstrip("/")
                    return {"estado": "redirecionado" if mudou else "ok", "codigo": r.status, **({"url_final": final} if mudou else {})}
            except urllib.error.HTTPError as ex:
                if metodo == "HEAD" and ex.code in (400, 403, 405, 501):
                    continue                                        # alguns servidores só aceitam GET
                c = ex.code
                est = "bloqueado" if c in (401, 403, 429) else "nao_encontrado" if c in (404, 410) else "erro_servidor" if c >= 500 else "sem_resposta"
                return {"estado": est, "codigo": c}
            except Exception as ex:                                 # tempo esgotado, DNS, conexão, certificado
                return {"estado": "sem_resposta", "codigo": None, "erro": type(ex).__name__ + ": " + str(getattr(ex, "reason", ex))[:90]}
    return {"estado": "sem_resposta", "codigo": None}


def main():
    fontes = json.loads((DADOS / "publicavel" / "fontes.json").read_text(encoding="utf-8"))
    refs = json.loads((DADOS / "publicavel" / "referencias.json").read_text(encoding="utf-8")) if (DADOS / "publicavel" / "referencias.json").exists() else []
    urls = sorted({f["url"] for f in fontes if f.get("url")} | {r["url"] for r in refs})
    print(f"{len(urls)} endereços únicos em {sum(1 for f in fontes if f.get('url'))} fontes")
    with ThreadPoolExecutor(max_workers=12) as ex:
        res = list(ex.map(testar, urls))
    for k, r in enumerate(res):                                 # uma segunda tentativa, sequencial, para falhas que podem ser passageiras
        if r["estado"] in ("sem_resposta", "erro_servidor"):
            r2 = testar(urls[k])
            r2["tentativas"] = 2
            res[k] = r2
    for k, r in enumerate(res):                                 # 429 = limite de requisições: repete devagar, um por vez
        if r.get("codigo") == 429:
            time.sleep(5)
            r2 = testar(urls[k])
            r2["tentativas"] = 2
            res[k] = r2
    out = {"testado_em": datetime.now().isoformat(timespec="seconds"), "agente": UA, "links": dict(zip(urls, res))}
    (DADOS / "privado").mkdir(parents=True, exist_ok=True)
    (DADOS / "privado" / "links_status.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    (DADOS / "publicavel").mkdir(parents=True, exist_ok=True)
    (DADOS / "publicavel" / "links_status.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")   # o app lê a cópia publicável
    cont: dict[str, int] = defaultdict(int)
    for r in res:
        cont[r["estado"]] += 1
    print(dict(cont))


if __name__ == "__main__":
    main()
