"""Alinha as fichas do Diretório à composição de perfis vigente em src/config.py (única fonte de verdade dos cortes etários).

Motivo: a ficha lia a composição e os cortes da planilha de análises (fora do repositório), que ficou atrás de src/config.py
(Itália C50/D50 -> C30/D70; Coreia do Sul C80/D20 -> C30/D70, cortes 21/60 -> 22/61). Aqui:
  - o bloco "coortes" passa a vir de src/config.py;
  - os campos demográficos que o motor reproduz exatamente (conferido contra as fichas de Itália e de Coreia com os cortes antigos)
    são recalculados com os cortes vigentes (pop_2025_pct, razões A/E, dependência, Estruturadores e Descendentes em 2075);
  - o CFCc por coorte é recalculado com a NTA pública (data/raw/nta_perfis_C_YL_S.csv; src/nta_derivados.py), população da ONU de 2025 e os cortes vigentes;
  - os campos que dependiam dos cortes antigos e que o repositório não reproduz (parcela privada dos Descendentes, carga por Estruturador,
    A/E em 2075 com TFT constante) viram lacuna, com nota do motivo, em vez de mostrar número calculado com outros cortes.

Uso:  python scripts/diretorio/coortes_motor.py   (corrige data/diretorio/publicavel/paises.json e privado/paises.json, se existirem)
Também é chamado por exportar_diretorio.py para que uma nova exportação não desfaça o ajuste."""
from __future__ import annotations

import json
import sys
import warnings
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))
warnings.filterwarnings("ignore")

NOTA = "calculado com cortes etários anteriores; a recalcular com os cortes vigentes"
DEPENDEM_DOS_CORTES = {
    "demografia": ("asc_estr_2075_tft_constante", "carga_estr_2075_wpp", "carga_estr_2075_tft_constante", "carga_estr_2075_rapida"),
    "consumo": ("cfcc_total_pct_desc_estr_asc", "desc_privado_pesos_nta"),
}
NOTA_TFT_CONSTANTE = "cenário de TFT constante da planilha não reproduzido no repositório; a recalcular"
NOTA_CARGA = "definição de carga por Estruturador da planilha não reproduzida no repositório; a recalcular"
NOTA_PRIVADO = "exige separar consumo privado e público da NTA, o que os perfis do repositório não trazem; a recalcular"
NOTA_ESPECIFICA = {("demografia", "asc_estr_2075_tft_constante"): NOTA_TFT_CONSTANTE, ("demografia", "carga_estr_2075_wpp"): NOTA_CARGA,
                   ("demografia", "carga_estr_2075_tft_constante"): NOTA_CARGA, ("demografia", "carga_estr_2075_rapida"): NOTA_CARGA,
                   ("consumo", "desc_privado_pesos_nta"): NOTA_PRIVADO}


def rotulo(composicao: dict) -> str:
    return " ".join(f"{k}{round(v * 100)}" for k, v in sorted(composicao.items()) if v > 0)


def cortes_texto(bm: int, tm: int) -> dict:
    return {"descendentes": f"0–{bm}", "estruturadores": f"{bm + 1}–{tm - 1}", "ascendentes": f"{tm}+"}


def demografia_do_motor(iso: str, bm: int, tm: int) -> dict:
    """Mesmas definições das fichas (reproduzem Itália e Coreia com os cortes antigos): 2025 = índice 1; 2075 = índice 51."""
    from src import projecao as pj

    base = pj.projetar(iso)                                                   # Tendência da ONU (WPP medium)

    def coortes(res, k):
        p = res.pop.sum(axis=0)[:, k]
        return float(p[: bm + 1].sum()), float(p[bm + 1: tm].sum()), float(p[tm:].sum())

    d25, e25, a25 = coortes(base, 1)
    d75, e75, a75 = coortes(base, 51)
    tot = d25 + e25 + a25
    return {
        "pop_2025_pct": ([round(100 * d25 / tot), round(100 * e25 / tot), round(100 * a25 / tot)], lambda v: f"{v[0]} / {v[1]} / {v[2]}"),
        "asc_estr_2025": (round(a25 / e25, 2), lambda v: f"{v:.2f}"),
        "asc_estr_2075_wpp": (round(a75 / e75, 2), lambda v: f"{v:.2f}"),
        "dependencia_2025_2075_wpp": ([round((d25 + a25) / e25, 2), round((d75 + a75) / e75, 2)], lambda v: f"{v[0]:.2f} → {v[1]:.2f}"),
        "estruturadores_2075_rel": (round(100 * e75 / e25), lambda v: f"{v:.0f}"),
        "descendentes_2075_rel": (round(100 * d75 / d25), lambda v: f"{v:.0f}"),
    }


def _reparar(ficha: dict, iso: str) -> bool:
    """Passos idempotentes sobre lacunas deixadas pelo ajuste de cortes: notas específicas e CFCc recalculado com a NTA pública."""
    mudou = False
    for (bloco, chave), nota in NOTA_ESPECIFICA.items():
        reg = ficha[bloco].get(chave)
        if reg is not None and reg.get("lacuna") and reg.get("nota") == NOTA:
            reg["nota"] = nota
            mudou = True
    reg = ficha["consumo"].get("cfcc_total_pct_desc_estr_asc")
    if reg is not None and reg.get("lacuna") and reg.get("nota") == NOTA:
        from src.nta_derivados import cfcc_por_coorte

        cf = cfcc_por_coorte(iso)
        if cf is not None:
            pct = [round(x, 1) for x in cf["pct"]]
            ficha["consumo"]["cfcc_total_pct_desc_estr_asc"] = {
                "texto": " / ".join(f"{x:.1f}" for x in pct), "valor": pct, "natureza": "EST",
                "fonte": f"NTA {cf['ano_perfil']} (ntaccounts.org) × população da ONU de {cf['ano_pop']}; cortes de src/config.py",
                "nota": "método do repositório (src/nta_derivados.py); a ficha anterior usava pesos da NTA de 2010 e cortes anteriores (16.7 / 50.6 / 32.7)"}
            mudou = True
    return mudou


def aplicar(ficha: dict) -> bool:
    """Ajusta a ficha (in place). Devolve True se algo mudou."""
    from src.config import COMPOSICAO_PERFIL_POR_PAIS, cortes_por_composicao

    iso = ficha["iso"]
    if iso not in COMPOSICAO_PERFIL_POR_PAIS:
        return False
    comp = COMPOSICAO_PERFIL_POR_PAIS[iso]
    bm, tm = cortes_por_composicao(comp)
    novo = {"composicao_perfis": rotulo(comp), **cortes_texto(bm, tm), "ano_referencia": 2025,
            "fonte": "src/config.py (composição de perfis, decisão do autor)"}
    antigo = ficha["coortes"]
    mudou_cortes = (antigo.get("descendentes"), antigo.get("estruturadores"), antigo.get("ascendentes")) != (novo["descendentes"], novo["estruturadores"], novo["ascendentes"])
    if (antigo.get("composicao_perfis"), antigo.get("descendentes"), antigo.get("estruturadores"), antigo.get("ascendentes")) == (novo["composicao_perfis"], novo["descendentes"], novo["estruturadores"], novo["ascendentes"]):
        return _reparar(ficha, iso)
    ficha["coortes"] = novo
    if mudou_cortes:
        dem = demografia_do_motor(iso, bm, tm)
        for chave, (valor, fmt) in dem.items():
            reg = ficha["demografia"].get(chave)
            if reg is not None and not reg.get("lacuna"):
                num = [float(x) for x in valor] if isinstance(valor, list) else float(valor)
                ficha["demografia"][chave] = {"texto": fmt(valor), "valor": num, "natureza": reg.get("natureza", "DER")}
        for bloco, chaves in DEPENDEM_DOS_CORTES.items():
            for chave in chaves:
                reg = ficha[bloco].get(chave)
                if reg is not None and not reg.get("lacuna") and not reg.get("retido"):
                    ficha[bloco][chave] = {"texto": "—", "valor": None, "lacuna": True, "natureza": reg.get("natureza", "EST"), "nota": NOTA}
    _reparar(ficha, iso)
    return True


def corrigir_arquivos() -> None:
    for sub in ("publicavel", "privado"):
        p = RAIZ / "data" / "diretorio" / sub / "paises.json"
        if not p.exists():
            continue
        dados = json.loads(p.read_text(encoding="utf-8"))
        alterados = [f["iso"] for f in dados if aplicar(f)]
        with open(p, "w", encoding="utf-8", newline="") as fh:
            fh.write(json.dumps(dados, ensure_ascii=False, indent=1).replace("\n", "\r\n"))  # mesmo formato do arquivo exportado (CRLF, sem quebra final)
        print(f"{sub}/paises.json: ajustados {alterados}")


if __name__ == "__main__":
    corrigir_arquivos()
