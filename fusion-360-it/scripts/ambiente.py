"""J0 — controllo dell'ambiente prima di lavorare in Fusion (Windows).

Controlla: Fusion aperto (processo Fusion360.exe, quante copie); server MCP che risponde (porta di `mcp_url` in impostazioni.json,
predefinita 27182); le porte di `porte_da_controllare` (es. 9876 del ponte MCP di Rhino: se la tiene Fusion vuol dire che è ripartito
un vecchio add-in, da segnalare all'utente); strumenti MCP uguali a quelli salvati (Fusion si aggiorna da solo e potrebbe cambiarli).

Uso: python -X utf8 ambiente.py                 → controllo
     python -X utf8 ambiente.py --avvia         → se Fusion è CHIUSO lo avvia (mai una seconda copia) e aspetta il server (max 5 min)
     python -X utf8 ambiente.py --salva-strumenti → registra l'elenco attuale degli strumenti come riferimento
Esce con 0 se si può lavorare, 1 altrimenti. Non usa mai il controllo dello schermo.
"""
import glob, hashlib, json, os, socket, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import impostazioni

QUI = os.path.dirname(os.path.abspath(__file__))
RIF = os.path.join(QUI, "strumenti-mcp.json")
IMP = impostazioni.carica()
PORTA = impostazioni.porta_mcp(IMP)

def comando(argomenti):
    """Uscita di un comando di Windows: tasklist e netstat scrivono nella codifica della console (cp850 in italiano), non in UTF-8."""
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
        # in ascolto = nessun indirizzo remoto (0.0.0.0:0 / [::]:0). NON si usa la colonna dello stato: su Windows 11 build 26300
        # netstat la scrive sbagliata (04/11: porta 445 in ascolto mostrata «FIN_WAIT_1», il server di Fusion «CLOSED»)
        if len(c) >= 5 and c[1].endswith(f":{p}") and c[2] in ("0.0.0.0:0", "[::]:0") and c[-1] != "0":
            pid = c[-1]
            t = comando(["tasklist", "/FI", f"PID eq {pid}", "/FO", "CSV", "/NH"])
            return t.split('","')[0].strip('"') if t.strip().startswith('"') else pid
    return None

def script_risponde(secondi=25):
    """Prova dal vero: uno script di una riga deve tornare. Il server può rispondere a initialize con Fusion bloccato da una finestra
    («Documenti recuperati» dopo una chiusura forzata, 04/11: non compare fra le finestre del sistema, quindi non si cerca per titolo)."""
    from mcp_fusion import Sessione, esegui
    try:
        return bool(esegui(Sessione(timeout=secondi), "out(ok=1)", sola_lettura=True)[1])
    except OSError:                # compreso il tempo scaduto
        return False

def strumenti():
    from mcp_fusion import Sessione
    s = Sessione()
    r, _ = s._rpc("tools/list", {})
    t = sorted((x["name"], hashlib.sha256(json.dumps(x, sort_keys=True).encode()).hexdigest()[:12]) for x in (r or {}).get("tools", []))
    return {"server": (s.info or {}).get("serverInfo"), "strumenti": t}

def avvia():
    # solo avviatori COMPLETI (con FusionLauncher.exe.ini accanto): una cartella di aggiornamento a metà ha l'exe ma non il file di
    # configurazione e dà «Configuration file … is missing or incomplete» (successo il 01/11 prendendo il più recente)
    lanciatori = sorted((f for f in glob.glob(os.path.join(os.environ["LOCALAPPDATA"], "Autodesk", "webdeploy", "production", "*", "FusionLauncher.exe"))
                         if os.path.exists(f + ".ini")), key=lambda f: os.path.getmtime(f + ".ini"), reverse=True)
    if not lanciatori:
        return "nessun FusionLauncher.exe completo (con .ini) trovato: chiedi all'utente di aprire Fusion"
    subprocess.Popen([lanciatori[0]], creationflags=0x00000008)      # DETACHED_PROCESS
    t0 = time.time()
    while time.time() - t0 < 300 and not porta_aperta(PORTA):
        time.sleep(5)
    return f"avviato ({lanciatori[0]}), server {'pronto' if porta_aperta(PORTA) else 'NON pronto'} dopo {round(time.time() - t0)} s"

def main():
    sys.stdout.reconfigure(encoding="utf-8")
    es = {"fusion_copie": len(processi("Fusion360.exe"))}
    if "--avvia" in sys.argv and es["fusion_copie"] == 0:
        es["avvio"] = avvia(); es["fusion_copie"] = len(processi("Fusion360.exe"))
    es["server_mcp"] = porta_aperta(PORTA); es["porta_mcp"] = PORTA
    avvisi = []
    if es["fusion_copie"] > 1:
        avvisi.append("ci sono PIÙ copie di Fusion aperte: chiedi all'utente di chiuderne una")
    for porta, chi in (IMP.get("porte_da_controllare") or {}).items():
        prop = proprietario_porta(int(porta)); es[f"porta_{porta}"] = prop
        if prop and "fusion" in prop.lower():
            avvisi.append(f"la porta {porta} è tenuta da Fusion, ma serve a: {chi} — è ripartito un vecchio add-in (va spento)")
    es["script_risponde"] = es["server_mcp"] and script_risponde()
    if es["server_mcp"] and not es["script_risponde"]:
        import registri
        c = registri.comando_in_corso(); es["comando_tavole_in_corso"] = c
        avvisi.append("Fusion aspetta un clic in una tavola: dì all'utente «premi Esc in Fusion, poi dimmi fatto»" if c else
                      "il server risponde ma gli script non partono: Fusion ha una finestra aperta (spesso «Documenti recuperati»): dì "
                      "all'utente «Fusion ha una finestra aperta che blocca i comandi: chiudila, poi dimmi fatto»")
    elif es["server_mcp"]:
        try:
            att = strumenti(); es["server"] = att["server"]
            if "--salva-strumenti" in sys.argv:
                json.dump(att, open(RIF, "w", encoding="utf-8"), indent=1); es["strumenti"] = "salvati come riferimento"
            elif os.path.exists(RIF):
                ref = json.load(open(RIF, encoding="utf-8"))
                es["strumenti_invariati"] = [list(x) for x in att["strumenti"]] == [list(x) for x in ref["strumenti"]]
                if not es["strumenti_invariati"]:
                    avvisi.append("gli strumenti MCP sono cambiati (Fusion aggiornato?): ricette e trappole potrebbero non valere più, avvisa l'utente")
            else:
                # installazione nuova (17/11: la prova in una cartella pulita lo saltava in silenzio): senza riferimento il controllo
                # dopo gli aggiornamenti di Fusion non si può fare. Non blocca il lavoro.
                es["strumenti_invariati"] = None
                # attenzione al testo: la parola che blocca il lavoro (vedi si_puo_lavorare qui sotto) non deve comparire qui
                avvisi.append("manca scripts/strumenti-mcp.json (installazione nuova): lancia una volta `ambiente.py --salva-strumenti`, "
                              "così dopo un aggiornamento di Fusion il controllo degli strumenti funziona; per ora si può lavorare")
        except Exception as ex:
            avvisi.append(f"il server non risponde bene: {str(ex)[:120]}")
    elif es["fusion_copie"] and not es["server_mcp"]:
        avvisi.append("Fusion è aperto ma il server MCP non risponde: in Fusion Preferenze → Generale → API → «Server MCP di Fusion»; o Fusion è bloccato da una finestra")
    elif not es["fusion_copie"]:
        avvisi.append("Fusion è chiuso: avvialo con --avvia (o lo apre l'utente)")
    es["avvisi"] = avvisi
    es["si_puo_lavorare"] = es["script_risponde"] and es["fusion_copie"] == 1 and not any("add-in" in a or "cambiati" in a for a in avvisi)
    print(json.dumps(es, indent=2, ensure_ascii=False))
    sys.exit(0 if es["si_puo_lavorare"] else 1)

if __name__ == "__main__":
    main()
