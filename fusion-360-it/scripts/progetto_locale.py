"""Lavoro a passi misurati, con ripresa sicura, in una cartella di progetto sul PC (creata da nuovo_progetto.py).

Per ogni passo: esegue lo script in Fusion → misura (volume totale e per corpo, elementi di timeline, elementi in errore) → confronta con
il volume ATTESO se lo dai (tolleranza 0.01 %) → salva lo script in passi/NN-nome.py e una riga in registro.json → aggiorna la copia
di sicurezza progetto.f3d → commit git del progetto (se la cartella è un repository). Se lo script fallisce o il volume non torna, il
passo NON viene registrato e te lo dice: cerca la causa prima di andare avanti.

Riga di comando (dalla cartella scripts/, con python -X utf8):
    progetto_locale.py <cartella> passo <nome> <file_codice.py> [--atteso VOLUME_MM3] [--nuovo-documento]
                                                # --nuovo-documento: al PRIMO passo, apre un documento nuovo e lavora lì
    progetto_locale.py <cartella> misura
    progetto_locale.py <cartella> riapri        # dopo una chiusura di Fusion: riapre progetto.f3d (un documento) e confronta col registro
    progetto_locale.py <cartella> rigioca       # rifà tutti i passi dagli script salvati, in un documento nuovo (uno solo)
    progetto_locale.py <cartella> versione [--step]   # consegna: consegna/<nome>-vN.f3d (mai sovrascritta); --step anche
                                                # consegna/<nome>-vN.step; poi commit git di tutto ciò che c'è in consegna/
    progetto_locale.py <cartella> stato [--fase "<fase>"] [--domanda "<testo>"]... [--risolta N]...
                                                # fase e domande aperte in stato.json (senza Fusion); senza opzioni le mostra
Il file del passo contiene solo il codice (senza intestazione: la aggiunge mcp_fusion.corpo; vedi references/ricette.md §1).
Altre uscite (3MF, DXF, PDF) salvale in consegna/ PRIMA di `versione`: così entrano nello stesso commit.
"""
import datetime, json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_fusion import Sessione, esegui

MISURA = """
PREC = adsk.fusion.CalculationAccuracy.VeryHighCalculationAccuracy   # b.volume (veloce) sbaglia di qualche mm³ sulle curve (10/11)
corpi = [(c.name, b.name, round(b.getPhysicalProperties(PREC).volume * 1000, 4)) for c in d.allComponents for b in c.bRepBodies]
def _piatta(t):   # un gruppo (es. quello creato importando un DXF) ha stato 5 e nasconde i suoi elementi: si guardano quelli
    for o in t:
        if o.isGroup:
            g = adsk.fusion.TimelineGroup.cast(o)
            yield from _piatta([g.item(k) for k in range(g.count)])
        else:
            yield o
ns = [o.name for o in _piatta(d.timeline) if o.healthState != adsk.fusion.FeatureHealthStates.HealthyFeatureHealthState and not o.isSuppressed]   # una feature sospesa non è un errore
out(volume=round(sum(v for _, _, v in corpi), 4), corpi=len(corpi), per_corpo=corpi, timeline=d.timeline.count, non_sani=ns)
"""
TOLLERANZA = 1e-4   # 0.01 % sul volume del modello
NUOVO_DOC = "app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)\nout(ok=True)"

def git_commit(cart, messaggio):
    if os.path.isdir(os.path.join(cart, ".git")):
        subprocess.run(["git", "-C", cart, "add", "-A"], capture_output=True)
        subprocess.run(["git", "-C", cart, "commit", "-q", "-m", messaggio], capture_output=True)

def leggi_stato(cart):
    f = os.path.join(os.path.abspath(cart), "stato.json")
    return json.load(open(f, encoding="utf-8")) if os.path.exists(f) else {"fase": None, "domande_aperte": []}

def stato(cart, fase=None, domande=(), risolte=()):
    """Fase del lavoro e domande aperte (J10), in stato.json accanto a registro.json; non serve Fusion."""
    cart = os.path.abspath(cart); s = leggi_stato(cart)
    if not (fase or domande or risolte):
        return s
    if fase:
        s["fase"] = fase
    for k in sorted(set(risolte), reverse=True):      # numeri da 1, come nell'elenco mostrato
        if 1 <= k <= len(s["domande_aperte"]):
            del s["domande_aperte"][k - 1]
    s["domande_aperte"] += [q for q in domande if q not in s["domande_aperte"]]
    s["aggiornato"] = datetime.datetime.now().isoformat(timespec="seconds")
    json.dump(s, open(os.path.join(cart, "stato.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    git_commit(cart, f"stato: fase {s['fase']}, domande aperte {len(s['domande_aperte'])}")
    return s

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
        git_commit(self.cart, messaggio)

    def passo(self, nome, codice, atteso=None, nuovo_documento=False):
        if nuovo_documento:      # J3: si lavora in un documento nuovo, non in quello che era aperto
            self.script(NUOVO_DOC)
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
                esito["avviso"] = "volume diverso dall'atteso: passo NON registrato. Misura la geometria e trova la causa (calcolo o modello?)"
                return esito
        if m["non_sani"]:
            esito["ok"] = False
            esito["avviso"] = "elementi della timeline in errore: passo NON registrato"
            return esito
        n = len(self.registro) + 1
        f = os.path.join(self.cart, "passi", f"{n:02d}-{nome}.py")
        open(f, "w", encoding="utf-8").write(codice)
        esito["copia_f3d"] = self.salva_copia()
        riga = {"n": n, "passo": nome, "file": os.path.basename(f), "misure": m, "atteso_mm3": atteso,
                "data": datetime.datetime.now().isoformat(timespec="seconds")}
        self.registro.append(riga)
        json.dump(self.registro, open(self.reg_file, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        self._git(f"passo {n:02d} {nome}: volume {m['volume']} mm3")
        esito["n"] = n
        return esito

    def riapri(self):
        self.script(f"im = app.importManager\nim.importToNewDocument(im.createFusionArchiveImportOptions({self.f3d!r}))\nout(ok=True)")
        m = self.misura(); atteso = self.registro[-1]["misure"] if self.registro else None
        return {"misure": m, "registro": atteso, "stato": leggi_stato(self.cart),
                "uguale": bool(atteso) and abs(m["volume"] - atteso["volume"]) <= TOLLERANZA * max(atteso["volume"], 1) and m["timeline"] == atteso["timeline"]}

    def rigioca(self):
        self.script(NUOVO_DOC)
        esiti = []
        for riga in self.registro:
            ok, _, righe = self.script(open(os.path.join(self.cart, "passi", riga["file"]), encoding="utf-8").read())
            m = self.misura()
            uguale = ok and abs(m["volume"] - riga["misure"]["volume"]) <= TOLLERANZA * max(riga["misure"]["volume"], 1)
            esiti.append({"passo": riga["passo"], "ok": ok, "uguale": uguale, "errore": None if ok else righe})
            if not uguale:
                break
        return esiti

    def versione(self, step=False):
        """Consegna: consegna/<nome cartella>-vN.f3d (e .step con step=True) con N successivo; non sovrascrive mai.
        Il commit viene DOPO le esportazioni: entra tutto ciò che è in consegna/."""
        cons = os.path.join(self.cart, "consegna"); os.makedirs(cons, exist_ok=True)
        base = os.path.basename(self.cart)
        nums = [int(m.group(1)) for f in os.listdir(cons) for m in [re.match(re.escape(base) + r"-v(\d+)\.(?:f3d|step)$", f)] if m]
        f = os.path.join(cons, f"{base}-v{max(nums, default=0) + 1}.f3d")
        esito = {"file": f, "ok": self.salva_copia(f)}
        if step:
            fs = f[:-4] + ".step"
            r = self.script(f"em = d.exportManager\nout(ok=em.execute(em.createSTEPExportOptions({fs!r}, r)))")[1]
            esito["step"] = fs
            esito["ok"] = esito["ok"] and bool(r and r.get("ok")) and os.path.exists(fs)
        self._git(f"consegna {os.path.basename(f)}" + (" + STEP" if step else ""))
        return esito

def _valori(a, opzione):
    return [a[i + 1] for i, x in enumerate(a[:-1]) if x == opzione]

def main():
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(2)
    cmd = sys.argv[2]
    if cmd == "stato":           # senza Fusion
        a = sys.argv[3:]
        fase = (_valori(a, "--fase") or [None])[-1]
        r = stato(sys.argv[1], fase, _valori(a, "--domanda"), [int(x) for x in _valori(a, "--risolta")])
        print(json.dumps(r, indent=2, ensure_ascii=False)); sys.exit(0)
    p = Progetto(sys.argv[1])
    if cmd == "passo":
        atteso = float(sys.argv[sys.argv.index("--atteso") + 1]) if "--atteso" in sys.argv else None
        r = p.passo(sys.argv[3], open(sys.argv[4], encoding="utf-8").read(), atteso, "--nuovo-documento" in sys.argv)
    elif cmd == "versione":
        r = p.versione("--step" in sys.argv)
    elif cmd in ("misura", "riapri", "rigioca"):
        r = getattr(p, cmd)()
    else:
        print(__doc__); sys.exit(2)
    print(json.dumps(r, indent=2, ensure_ascii=False))
    sys.exit(0 if (not isinstance(r, dict) or r.get("ok", True) is not False) else 1)

if __name__ == "__main__":
    if sys.argv[1:2] in (["-h"], ["--help"]):  # aiuto senza Fusion
        sys.stdout.reconfigure(encoding="utf-8"); print(__doc__); sys.exit(0)
    main()
