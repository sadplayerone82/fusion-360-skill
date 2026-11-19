"""Client for the official Fusion MCP server (Streamable HTTP, 127.0.0.1:27182) + standard script header.

Used when working from Python (measured steps, report, judge) or when the native MCP tools are not loaded in the session
(it happens if Fusion was opened after the session started): it talks to the same server.

From Python:
    from mcp_fusion import Sessione, esegui
    s = Sessione()
    ok, ris, righe = esegui(s, 'e = F.extrudeFeatures.addSimple(prof, S("10 mm"), OP.NewBodyFeatureOperation)\\nout(v=vol(e.bodies.item(0)))')
From the command line:
    python -X utf8 mcp_fusion.py fusion_mcp_read '{"queryType": "licensing"}'
"""
import json, os, re, sys, time, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import impostazioni

URL = impostazioni.carica(avvisa=False)["mcp_url"]      # from impostazioni.json (default http://127.0.0.1:27182/mcp)
PROTOCOLLO = "2025-06-18"
RIGA_ADDIN = re.compile(r"^\[MCP\] Server listening on localhost:\d+$")   # line printed by the old unofficial add-in

# Header put in front of every script (see references/ricette.md §1): short names for the API and out() to return measurements.
TESTA = ("import adsk.core, adsk.fusion, math, json\n\ndef run(_context: str):\n"
         "    app = adsk.core.Application.get()\n"
         "    d = adsk.fusion.Design.cast(app.activeProduct)\n"
         "    r = d.rootComponent if d else None\n    F = r.features if r else None\n"
         "    P = adsk.core.Point3D.create\n    S = adsk.core.ValueInput.createByString\n    OP = adsk.fusion.FeatureOperations\n"
         "    H = adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation\n"
         "    V = adsk.fusion.DimensionOrientations.VerticalDimensionOrientation\n"
         # high-accuracy volume: b.volume (fast) is off by a few mm³ on intersecting curved surfaces (10/11)
         "    def vol(b): return round(b.getPhysicalProperties(adsk.fusion.CalculationAccuracy.VeryHighCalculationAccuracy).volume * 1000, 4)\n"
         "    def out(**k): print('RIS' + json.dumps(k))\n"
         # check in the same call: if it does not match, the error undoes the whole script (which is a transaction)
         "    def controlla(corpo=None, volume=None, ingombro=None, n_corpi=None, tol_v=0.0001, tol_l=0.01):\n"
         "        e = []\n"
         "        if n_corpi is not None:\n"
         "            n = r.bRepBodies.count + sum(o.bRepBodies.count for o in r.allOccurrences)\n"
         "            if n != n_corpi: e.append('corpi %d, attesi %d' % (n, n_corpi))\n"
         "        if corpo is not None and volume is not None:\n"
         "            v = vol(corpo)\n"
         "            if abs(v - volume) > volume * tol_v: e.append('volume %.3f, atteso %.3f' % (v, volume))\n"
         "        if corpo is not None and ingombro is not None:\n"
         "            bb = corpo.boundingBox; a, c = bb.minPoint, bb.maxPoint\n"
         "            m = [(c.x - a.x) * 10, (c.y - a.y) * 10, (c.z - a.z) * 10]\n"
         "            if any(abs(x - y) > tol_l for x, y in zip(m, ingombro)):\n"
         "                e.append('ingombro %s, atteso %s' % ([round(x, 3) for x in m], ingombro))\n"
         "        if e: raise RuntimeError('CONTROLLO FALLITO: ' + '; '.join(e))\n")

# Fusion defect (found on 05/11): every script adds a layer to sys.stdout and none removes it; after a few hundred scripts in
# a session the answer is «success: true» with an empty message, silently. This preamble removes the layers when there are too many.
# Private Autodesk attribute: if it disappears the loop does nothing, and the check in esegui() on lost output remains.
PROTEGGI_USCITA = True
PREAMBOLO_USCITA = ("import sys as _s\n"
                    "for _n in ('stdout', 'stderr'):\n"
                    "    _x = getattr(_s, _n); _k = 0\n"
                    "    while hasattr(_x, '_original'):\n"
                    "        _x = _x._original; _k += 1\n"
                    "    if _k > 100: setattr(_s, _n, _x)\n")

def corpo(codice):
    """Wraps the code (without indentation) in the header: the result is a complete script for fusion_mcp_execute."""
    return TESTA + "".join("    " + l + "\n" for l in codice.strip("\n").splitlines())

class Sessione:
    def __init__(self, url=URL, timeout=300):
        self.url, self.sess, self.n, self.timeout = url, None, 0, timeout
        self.info, _ = self._rpc("initialize", {"protocolVersion": PROTOCOLLO, "capabilities": {},
                                                "clientInfo": {"name": "skill-fusion-360", "version": "1"}})
        self._invia({"jsonrpc": "2.0", "method": "notifications/initialized"})

    def _invia(self, dati):
        intest = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream",
                  "MCP-Protocol-Version": PROTOCOLLO}
        if self.sess:
            intest["Mcp-Session-Id"] = self.sess
        req = urllib.request.Request(self.url, data=json.dumps(dati).encode(), headers=intest, method="POST")
        with urllib.request.urlopen(req, timeout=self.timeout) as r:
            self.sess = r.headers.get("Mcp-Session-Id") or self.sess
            testo, tipo = r.read().decode("utf-8"), r.headers.get("Content-Type", "")
        if not testo.strip():
            return None
        if "text/event-stream" in tipo:
            righe = [l[5:].strip() for l in testo.splitlines() if l.startswith("data:")]
            return json.loads(righe[-1]) if righe else None
        return json.loads(testo)

    def _rpc(self, metodo, parametri):
        self.n += 1
        t0 = time.perf_counter()
        r = self._invia({"jsonrpc": "2.0", "id": self.n, "method": metodo, "params": parametri})
        dt = time.perf_counter() - t0
        if r and "error" in r:
            return {"errore_rpc": r["error"]}, dt
        return (r or {}).get("result"), dt

    def strumento(self, nome, argomenti):
        """Calls an MCP tool; returns (result, seconds)."""
        ogg = argomenti.get("object") or {}
        if PROTEGGI_USCITA and argomenti.get("featureType") == "script" and "script" in ogg:
            argomenti = {**argomenti, "object": {**ogg, "script": PREAMBOLO_USCITA + ogg["script"]}}
        return self._rpc("tools/call", {"name": nome, "arguments": argomenti})

def testi(risultato):
    """Texts of the content of a tool response (list of strings)."""
    return [c.get("text", "") for c in (risultato or {}).get("content", []) if c.get("type") == "text"]

def esegui(s, codice, sola_lettura=False, intero=False):
    """Runs a script in Fusion. `codice` without header (corpo() adds it), or complete with intero=True.
    Returns (succeeded, last out() result or None, last printed or error lines).
    The line «[MCP] Server listening on localhost:9876» of the old faust add-in is removed (if it appears, warn the user)."""
    script = codice if intero else corpo(codice)
    r, _ = s.strumento("fusion_mcp_execute", {"featureType": "script", "object": {"script": script, "readOnly": sola_lettura}})
    t = testi(r)
    if not t:
        return False, None, ["no answer from the server"]
    j = json.loads(t[0])
    # ONLY the exact line of the old add-in («[MCP] Server listening on localhost:9876») is removed: before, it was enough for a line
    # to contain «9876» (even a volume of 19,876 mm³) to discard it, and the result was lost silently (review of 18/11)
    righe = [l for l in (j.get("message") or j.get("error") or "").splitlines() if not RIGA_ADDIN.match(l.strip())]
    ris = [json.loads(l[3:]) for l in righe if l.startswith("RIS")]
    if j.get("success") and not ris and not righe and ("out(" in codice or "print(" in codice):
        # the script had to print and nothing arrived: it is not «succeeded», the result is lost
        return False, None, ["output lost: Fusion says «success» but the script returned nothing (too many scripts in the session? restart Fusion)"]
    return bool(j.get("success")), (ris[-1] if ris else None), righe[-6:]

def chiudi_documento(s):
    """Closes the active document WITHOUT saving (working documents: the project lives in the .f3d on the PC)."""
    return s.strumento("fusion_mcp_execute", {"featureType": "document", "object": {"operation": "close", "userConfirmedCloseWithoutSave": True}})

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    r, dt = Sessione().strumento(sys.argv[1], json.loads(sys.argv[2]))
    print(f"[{dt:.2f} s]")
    for x in testi(r):
        print(x)
