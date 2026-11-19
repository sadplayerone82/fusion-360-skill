"""Report of the active model in Fusion (read only): document type, parameters, timeline items in error, sketches not
constrained, and for each body volume, bounding box (`dimensioni_mm`), faces, material, mass. Runs `fusion_rapporto.py` inside Fusion.
ASSEMBLIES: the «corpi» (bodies) are measured in their component (not where they sit in the assembly); the assembly bounding box is in
`assieme` (`ingombro_visibili`, `ingombro_tutti`, `corpi_nascosti`).

Usage: python -X utf8 rapporto_modello.py            → prints the report
       python -X utf8 rapporto_modello.py --breve    → only the J5 gate (errors, free sketches, bodies with volume and bounding box)
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
        raise RuntimeError("report failed: " + str(j.get("error"))[-500:])
    righe = [l for l in j["message"].splitlines() if l.startswith("{")]
    return json.loads(righe[-1])

def breve(rap):
    return {"elementi_in_errore": rap["timeline"]["non_sani"], "schizzi_non_vincolati": rap["schizzi_non_vincolati"],
            "parametri_utente": len(rap["parametri_utente"]),
            "corpi": [{"nome": c["nome"], "componente": c["componente"], "solido": c["solido"], "visibile": c["visibile"],
                       "volume_mm3": c["volume_mm3"], "dimensioni_mm": c["dimensioni_mm"]} for c in rap["corpi"]],
            # in assemblies the «corpi» measurements are in their component: the true bounding box is this one (visible bodies, in position)
            "assieme": rap.get("assieme"),
            "cancello_J5": not rap["timeline"]["non_sani"] and not rap["schizzi_non_vincolati"] and all(c["solido"] for c in rap["corpi"])}

if __name__ == "__main__":
    if sys.argv[1:2] in (["-h"], ["--help"]):  # aiuto senza Fusion
        sys.stdout.reconfigure(encoding="utf-8"); print(__doc__); sys.exit(0)
    sys.stdout.reconfigure(encoding="utf-8")
    rap = rapporto()
    print(json.dumps(breve(rap) if "--breve" in sys.argv else rap, indent=2, ensure_ascii=False))
