"""Prova di controlla_mesh.py senza Fusion (revisione del 29/10, 02-tre-passate §2.1): crea 3MF di prova e controlla che il giudice
promuova e bocci quando deve. Uso: python -I prova_controlla_mesh.py → stampa l'esito di ogni caso; esce con 1 se un caso sbaglia.
Casi: scatola 60×30×45 giusta (OK); stessa scatola con Y e Z scambiati (NON OK: pezzo ruotato); scatola ruotata ma con una
trasformazione nel <build> che la rimette a 60×30×45 (OK); ruotata con --qualsiasi-orientamento (OK); triangoli girati al contrario
(NON OK: volume negativo); un triangolo tolto (NON OK: aperta).
"""
import json, os, subprocess, sys, tempfile, zipfile

QUI = os.path.dirname(os.path.abspath(__file__))
FACCE = [(0, 3, 2), (0, 1, 3), (4, 7, 5), (4, 6, 7), (0, 5, 1), (0, 4, 5), (2, 7, 6), (2, 3, 7), (0, 6, 4), (0, 2, 6), (1, 7, 3), (1, 5, 7)]

def scrivi(percorso, a, b, c, transform=None, facce=FACCE):
    v = [(x, y, z) for x in (0, a) for y in (0, b) for z in (0, c)]
    vx = "".join(f'<vertex x="{x}" y="{y}" z="{z}"/>' for x, y, z in v)
    tx = "".join(f'<triangle v1="{p}" v2="{q}" v3="{r}"/>' for p, q, r in facce)
    tr = f' transform="{transform}"' if transform else ""
    m = (f'<?xml version="1.0"?><model unit="millimeter"><resources><object id="1" type="model"><mesh><vertices>{vx}</vertices>'
         f'<triangles>{tx}</triangles></mesh></object></resources><build><item objectid="1"{tr}/></build></model>')
    with zipfile.ZipFile(percorso, "w") as z:
        z.writestr("3D/3dmodel.model", m)

def main():
    sys.stdout.reconfigure(encoding="utf-8")
    d = tempfile.mkdtemp(prefix="prova_controlla_mesh_")
    casi = [("giusto", (60, 30, 45), {}, [], "OK"),
            ("ruotato", (60, 45, 30), {}, [], "NON OK"),
            ("trasformato", (60, 45, 30), {"transform": "1 0 0 0 0 1 0 -1 0 0 0 45"}, [], "OK"),
            ("ruotato_qualsiasi", (60, 45, 30), {}, ["--qualsiasi-orientamento"], "OK"),
            ("rovesciato", (60, 30, 45), {"facce": [(p, r, q) for p, q, r in FACCE]}, [], "NON OK"),
            ("aperto", (60, 30, 45), {"facce": FACCE[:-1]}, [], "NON OK")]
    sbagliati = 0
    for nome, dim, opz, extra, atteso in casi:
        f = os.path.join(d, nome + ".3mf"); scrivi(f, *dim, **opz)
        r = subprocess.run([sys.executable, "-I", os.path.join(QUI, "controlla_mesh.py"), f, "--atteso-mm", "60", "30", "45", *extra],
                           capture_output=True, text=True, encoding="utf-8")
        esito = json.loads(r.stdout)["ESITO"] if r.stdout.strip().startswith("{") else "ERRORE: " + r.stderr[-200:]
        giusto = esito == atteso; sbagliati += not giusto
        print(f"{'ok ' if giusto else 'NO '} {nome:18} atteso {atteso:7} avuto {esito}")
    sys.exit(1 if sbagliati else 0)

if __name__ == "__main__":
    if sys.argv[1:2] in (["-h"], ["--help"]):  # aiuto senza Fusion
        sys.stdout.reconfigure(encoding="utf-8"); print(__doc__); sys.exit(0)
    main()
