"""J0 — environment check before working in Fusion (Windows).

Checks: Fusion open (process Fusion360.exe, how many copies); MCP server answering (port of `mcp_url` in impostazioni.json,
default 27182); the ports in `porte_da_controllare` (e.g. 9876 of the Rhino MCP bridge: if Fusion holds it, an old add-in has
restarted, to be reported to the user); MCP tools identical to the saved ones (Fusion updates itself and could change them).

Usage: python -X utf8 ambiente.py                 → check
       python -X utf8 ambiente.py --avvia         → if Fusion is CLOSED it starts it (never a second copy) and waits for the server (max 5 min)
       python -X utf8 ambiente.py --salva-strumenti → records the current list of tools as the reference
Exits with 0 if work can go on, 1 otherwise. Never uses screen control.
"""
import glob, hashlib, json, os, socket, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import impostazioni

QUI = os.path.dirname(os.path.abspath(__file__))
RIF = os.path.join(QUI, "strumenti-mcp.json")
IMP = impostazioni.carica()
PORTA = impostazioni.porta_mcp(IMP)

# Word searched inside the warnings to decide si_puo_lavorare (see main): the sentences that block work contain one of these.
# Keep them in sync with the warning sentences below.
PAROLE_BLOCCANTI = ("add-in", "have changed")

def comando(argomenti):
    """Output of a Windows command: tasklist and netstat write in the console encoding (cp850 on Italian Windows), not in UTF-8."""
    return subprocess.run(argomenti, capture_output=True, encoding="oem", errors="replace").stdout or ""

def porta_aperta(p):
    s = socket.socket(); s.settimeout(1)
    try:
        s.connect(("127.0.0.1", p)); return True
    except OSError:
        return False
    finally:
        s.close()

def processi(nome):
    out = comando(["tasklist", "/FI", f"IMAGENAME eq {nome}", "/FO", "CSV", "/NH"])
    return [l.split('","')[1] for l in out.splitlines() if l.startswith('"' + nome)]

def proprietario_porta(p):
    out = comando(["netstat", "-ano", "-p", "TCP"])
    for l in out.splitlines():
        c = l.split()
        # listening = no remote address (0.0.0.0:0 / [::]:0). The state column is NOT used: on Windows 11 build 26300
        # netstat writes it wrong (04/11: port 445 listening shown as «FIN_WAIT_1», the Fusion server as «CLOSED»)
        if len(c) >= 5 and c[1].endswith(f":{p}") and c[2] in ("0.0.0.0:0", "[::]:0") and c[-1] != "0":
            pid = c[-1]
            t = comando(["tasklist", "/FI", f"PID eq {pid}", "/FO", "CSV", "/NH"])
            return t.split('","')[0].strip('"') if t.strip().startswith('"') else pid
    return None

def script_risponde(secondi=25):
    """Real test: a one-line script must come back. The server can answer initialize while Fusion is blocked by a dialog
    («Recovered documents» after a forced close, 04/11: it does not appear among the system windows, so it is not searched by title)."""
    from mcp_fusion import Sessione, esegui
    try:
        return bool(esegui(Sessione(timeout=secondi), "out(ok=1)", sola_lettura=True)[1])
    except OSError:                # timeout included
        return False

def strumenti():
    from mcp_fusion import Sessione
    s = Sessione()
    r, _ = s._rpc("tools/list", {})
    t = sorted((x["name"], hashlib.sha256(json.dumps(x, sort_keys=True).encode()).hexdigest()[:12]) for x in (r or {}).get("tools", []))
    return {"server": (s.info or {}).get("serverInfo"), "strumenti": t}

def avvia():
    # only COMPLETE launchers (with FusionLauncher.exe.ini next to them): a half-finished update folder has the exe but not the
    # configuration file and gives «Configuration file … is missing or incomplete» (happened on 01/11 taking the most recent one)
    lanciatori = sorted((f for f in glob.glob(os.path.join(os.environ["LOCALAPPDATA"], "Autodesk", "webdeploy", "production", "*", "FusionLauncher.exe"))
                         if os.path.exists(f + ".ini")), key=lambda f: os.path.getmtime(f + ".ini"), reverse=True)
    if not lanciatori:
        return "no complete FusionLauncher.exe (with .ini) found: ask the user to open Fusion"
    subprocess.Popen([lanciatori[0]], creationflags=0x00000008)      # DETACHED_PROCESS
    t0 = time.time()
    while time.time() - t0 < 300 and not porta_aperta(PORTA):
        time.sleep(5)
    return f"started ({lanciatori[0]}), server {'ready' if porta_aperta(PORTA) else 'NOT ready'} after {round(time.time() - t0)} s"

def main():
    sys.stdout.reconfigure(encoding="utf-8")
    es = {"fusion_copie": len(processi("Fusion360.exe"))}
    if "--avvia" in sys.argv and es["fusion_copie"] == 0:
        es["avvio"] = avvia(); es["fusion_copie"] = len(processi("Fusion360.exe"))
    es["server_mcp"] = porta_aperta(PORTA); es["porta_mcp"] = PORTA
    avvisi = []
    if es["fusion_copie"] > 1:
        avvisi.append("there are SEVERAL copies of Fusion open: ask the user to close one")
    for porta, chi in (IMP.get("porte_da_controllare") or {}).items():
        prop = proprietario_porta(int(porta)); es[f"porta_{porta}"] = prop
        if prop and "fusion" in prop.lower():
            # contains the blocking word «add-in» (PAROLE_BLOCCANTI)
            avvisi.append(f"port {porta} is held by Fusion, but it is meant for: {chi} — an old add-in has restarted (it must be turned off)")
    es["script_risponde"] = es["server_mcp"] and script_risponde()
    if es["server_mcp"] and not es["script_risponde"]:
        import registri
        c = registri.comando_in_corso(); es["comando_tavole_in_corso"] = c
        avvisi.append("Fusion is waiting for a click in a drawing: tell the user «press Esc in Fusion, then tell me done»" if c else
                      "the server answers but scripts do not run: Fusion has a dialog open (often «Recovered documents»): tell "
                      "the user «Fusion has a dialog open that blocks the commands: close it, then tell me done»")
    elif es["server_mcp"]:
        try:
            att = strumenti(); es["server"] = att["server"]
            if "--salva-strumenti" in sys.argv:
                json.dump(att, open(RIF, "w", encoding="utf-8"), indent=1); es["strumenti"] = "saved as the reference"
            elif os.path.exists(RIF):
                ref = json.load(open(RIF, encoding="utf-8"))
                es["strumenti_invariati"] = [list(x) for x in att["strumenti"]] == [list(x) for x in ref["strumenti"]]
                if not es["strumenti_invariati"]:
                    # contains the blocking words «have changed» (PAROLE_BLOCCANTI)
                    avvisi.append("the MCP tools have changed (Fusion updated?): recipes and traps may no longer apply, warn the user")
            else:
                # new installation (17/11: the test in a clean folder skipped it silently): without the reference the check
                # after Fusion updates cannot be done. It does not block work.
                es["strumenti_invariati"] = None
                # careful with the text: the words that block work (PAROLE_BLOCCANTI, see si_puo_lavorare below) must not appear here
                avvisi.append("scripts/strumenti-mcp.json is missing (new installation): run `ambiente.py --salva-strumenti` once, "
                              "so that after a Fusion update the tool check works; for now work can go on")
        except Exception as ex:
            avvisi.append(f"the server does not answer properly: {str(ex)[:120]}")
    elif es["fusion_copie"] and not es["server_mcp"]:
        avvisi.append("Fusion is open but the MCP server does not answer: in Fusion Preferences → General → API → «Fusion MCP Server»; or Fusion is blocked by a dialog")
    elif not es["fusion_copie"]:
        avvisi.append("Fusion is closed: start it with --avvia (or the user opens it)")
    es["avvisi"] = avvisi
    es["si_puo_lavorare"] = es["script_risponde"] and es["fusion_copie"] == 1 and not any(p in a for a in avvisi for p in PAROLE_BLOCCANTI)
    print(json.dumps(es, indent=2, ensure_ascii=False))
    sys.exit(0 if es["si_puo_lavorare"] else 1)

if __name__ == "__main__":
    main()
