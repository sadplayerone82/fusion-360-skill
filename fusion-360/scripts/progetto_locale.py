"""Work in measured steps, with safe resumption, in a project folder on the PC (created by nuovo_progetto.py).

For each step: runs the script in Fusion → measures (total volume and per body, timeline items, items in error) → compares with
the EXPECTED volume if you give it (tolerance 0.01 %) → saves the script in passi/NN-name.py and a line in registro.json → updates the
backup copy progetto.f3d → git commit of the project (if the folder is a repository). If the script fails or the volume does not match, the
step is NOT recorded and it tells you: find the cause before going on.

Command line (from the scripts/ folder, with python -X utf8):
    progetto_locale.py <folder> passo <name> <code_file.py> [--atteso VOLUME_MM3]
    progetto_locale.py <folder> misura
    progetto_locale.py <folder> riapri        # after Fusion was closed: reopens progetto.f3d and compares with the project log
    progetto_locale.py <folder> rigioca       # replays all steps from the saved scripts, in a new document
    progetto_locale.py <folder> versione      # delivery: saves consegna/<name>-vN.f3d (never overwritten)
The step file contains only the code (without header: mcp_fusion.corpo adds it; see references/ricette.md §1).
"""
import datetime, json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_fusion import Sessione, esegui

MISURA = """
PREC = adsk.fusion.CalculationAccuracy.VeryHighCalculationAccuracy   # b.volume (fast) is off by a few mm³ on curves (10/11)
corpi = [(c.name, b.name, round(b.getPhysicalProperties(PREC).volume * 1000, 4)) for c in d.allComponents for b in c.bRepBodies]
def _piatta(t):   # a group (e.g. the one created by importing a DXF) has state 5 and hides its items: those are inspected
    for o in t:
        if o.isGroup:
            g = adsk.fusion.TimelineGroup.cast(o)
            yield from _piatta([g.item(k) for k in range(g.count)])
        else:
            yield o
ns = [o.name for o in _piatta(d.timeline) if o.healthState != adsk.fusion.FeatureHealthStates.HealthyFeatureHealthState and not o.isSuppressed]   # a suppressed feature is not an error
out(volume=round(sum(v for _, _, v in corpi), 4), corpi=len(corpi), per_corpo=corpi, timeline=d.timeline.count, non_sani=ns)
"""
TOLLERANZA = 1e-4   # 0.01 % of the model volume

class Progetto:
    def __init__(self, cartella, sessione=None):
        self.cart = os.path.abspath(cartella)
        self.s = sessione or Sessione()
        os.makedirs(os.path.join(self.cart, "passi"), exist_ok=True)
        self.reg_file = os.path.join(self.cart, "registro.json")
        self.registro = json.load(open(self.reg_file, encoding="utf-8")) if os.path.exists(self.reg_file) else []
        self.f3d = os.path.join(self.cart, "progetto.f3d")

    def script(self, codice, sola_lettura=False):
        return esegui(self.s, codice, sola_lettura)

    def misura(self):
        return self.script(MISURA, sola_lettura=True)[1]

    def salva_copia(self, file=None):
        f = file or self.f3d
        ok = self.script(f"em = d.exportManager\nout(ok=em.execute(em.createFusionArchiveExportOptions({f!r}, r)))")[1]
        return bool(ok and ok.get("ok")) and os.path.exists(f)

    def _git(self, messaggio):
        if os.path.isdir(os.path.join(self.cart, ".git")):
            subprocess.run(["git", "-C", self.cart, "add", "-A"], capture_output=True)
            subprocess.run(["git", "-C", self.cart, "commit", "-q", "-m", messaggio], capture_output=True)

    def passo(self, nome, codice, atteso=None):
        ok, ris, righe = self.script(codice)
        if not ok:
            return {"passo": nome, "ok": False, "errore": righe}
        m = self.misura()
        esito = {"passo": nome, "ok": True, "risultato_script": ris, "misure": m}
        if atteso is not None:
            esito["atteso_mm3"] = atteso
            esito["uguale_atteso"] = abs(m["volume"] - atteso) <= TOLLERANZA * max(abs(atteso), 1)
            if not esito["uguale_atteso"]:
                esito["ok"] = False
                esito["avviso"] = "volume different from the expected one: step NOT recorded. Measure the geometry and find the cause (calculation or model?)"
                return esito
        if m["non_sani"]:
            esito["ok"] = False
            esito["avviso"] = "timeline items in error: step NOT recorded"
            return esito
        n = len(self.registro) + 1
        f = os.path.join(self.cart, "passi", f"{n:02d}-{nome}.py")
        open(f, "w", encoding="utf-8").write(codice)
        esito["copia_f3d"] = self.salva_copia()
        riga = {"n": n, "passo": nome, "file": os.path.basename(f), "misure": m, "atteso_mm3": atteso,
                "data": datetime.datetime.now().isoformat(timespec="seconds")}
        self.registro.append(riga)
        json.dump(self.registro, open(self.reg_file, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        self._git(f"step {n:02d} {nome}: volume {m['volume']} mm3")
        esito["n"] = n
        return esito

    def riapri(self):
        self.script(f"im = app.importManager\nim.importToNewDocument(im.createFusionArchiveImportOptions({self.f3d!r}))\nout(ok=True)")
        m = self.misura(); atteso = self.registro[-1]["misure"] if self.registro else None
        return {"misure": m, "registro": atteso,
                "uguale": bool(atteso) and abs(m["volume"] - atteso["volume"]) <= TOLLERANZA * max(atteso["volume"], 1) and m["timeline"] == atteso["timeline"]}

    def rigioca(self):
        self.script("app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)\nout(ok=True)")
        esiti = []
        for riga in self.registro:
            ok, _, righe = self.script(open(os.path.join(self.cart, "passi", riga["file"]), encoding="utf-8").read())
            m = self.misura()
            uguale = ok and abs(m["volume"] - riga["misure"]["volume"]) <= TOLLERANZA * max(riga["misure"]["volume"], 1)
            esiti.append({"passo": riga["passo"], "ok": ok, "uguale": uguale, "errore": None if ok else righe})
            if not uguale:
                break
        return esiti

    def versione(self):
        """Delivery: consegna/<folder name>-vN.f3d with the next N; never overwrites."""
        cons = os.path.join(self.cart, "consegna"); os.makedirs(cons, exist_ok=True)
        base = os.path.basename(self.cart)
        nums = [int(m.group(1)) for f in os.listdir(cons) for m in [re.match(re.escape(base) + r"-v(\d+)\.f3d$", f)] if m]
        f = os.path.join(cons, f"{base}-v{max(nums, default=0) + 1}.f3d")
        ok = self.salva_copia(f)
        self._git(f"delivery {os.path.basename(f)}")
        return {"file": f, "ok": ok}

def main():
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(2)
    p = Progetto(sys.argv[1]); cmd = sys.argv[2]
    if cmd == "passo":
        atteso = float(sys.argv[sys.argv.index("--atteso") + 1]) if "--atteso" in sys.argv else None
        r = p.passo(sys.argv[3], open(sys.argv[4], encoding="utf-8").read(), atteso)
    elif cmd in ("misura", "riapri", "rigioca", "versione"):
        r = getattr(p, cmd)()
    else:
        print(__doc__); sys.exit(2)
    print(json.dumps(r, indent=2, ensure_ascii=False))
    sys.exit(0 if (not isinstance(r, dict) or r.get("ok", True) is not False) else 1)

if __name__ == "__main__":
    main()
