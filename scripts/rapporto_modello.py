"""Rapporto del modello attivo in Fusion (sola lettura): tipo di documento, parametri, elementi della timeline in errore, schizzi non
vincolati, e per ogni corpo volume, ingombro (`dimensioni_mm`), facce, materiale, massa. Esegue `fusion_rapporto.py` dentro Fusion.
ASSIEMI: i «corpi» sono misurati nel loro componente (non dove stanno nell'assieme); l'ingombro dell'assieme è in `assieme`
(`ingombro_visibili`, `ingombro_tutti`, `corpi_nascosti`).

Uso: python -X utf8 rapporto_modello.py            → stampa il rapporto
     python -X utf8 rapporto_modello.py --breve    → solo il cancello di J5 (errori, schizzi liberi, corpi con volume e ingombro)
     from rapporto_modello import rapporto; r = rapporto(sessione)
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_fusion import Sessione, testi

CODICE = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "fusion_rapporto.py"), encoding="utf-8").read()

def rapporto(s=None):
    s = s or Sessione()
    r, _ = s.strumento("fusion_mcp_execute", {"featureType": "script", "object": {"script": CODICE, "readOnly": True}})
    j = json.loads(testi(r)[0])
    if not j.get("success"):
        raise RuntimeError("rapporto non riuscito: " + str(j.get("error"))[-500:])
    righe = [l for l in j["message"].splitlines() if l.startswith("{")]
    return json.loads(righe[-1])

def breve(rap):
    return {"elementi_in_errore": rap["timeline"]["non_sani"], "schizzi_non_vincolati": rap["schizzi_non_vincolati"],
            "parametri_utente": len(rap["parametri_utente"]),
            "corpi": [{"nome": c["nome"], "componente": c["componente"], "solido": c["solido"], "visibile": c["visibile"],
                       "volume_mm3": c["volume_mm3"], "dimensioni_mm": c["dimensioni_mm"]} for c in rap["corpi"]],
            # negli assiemi le misure dei «corpi» sono nel loro componente: l'ingombro vero è questo (corpi visibili, in posizione)
            "assieme": rap.get("assieme"),
            "cancello_J5": not rap["timeline"]["non_sani"] and not rap["schizzi_non_vincolati"] and all(c["solido"] for c in rap["corpi"])}

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    rap = rapporto()
    print(json.dumps(breve(rap) if "--breve" in sys.argv else rap, indent=2, ensure_ascii=False))
