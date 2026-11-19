"""Test of controlla_mesh.py without Fusion (review of 29/10, 02-tre-passate §2.1): creates test 3MF files and checks that the judge
passes and fails them when it should. Usage: python -I prova_controlla_mesh.py → prints the result of each case; exits with 1 if a case is wrong.
Cases: correct 60×30×45 box (OK); same box with Y and Z swapped (NON OK = not OK: rotated part); rotated box but with a
transform in the <build> that brings it back to 60×30×45 (OK); rotated with --qualsiasi-orientamento (OK); triangles flipped
(NON OK: negative volume); one triangle removed (NON OK: open).
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
        esito = json.loads(r.stdout)["ESITO"] if r.stdout.strip().startswith("{") else "ERROR: " + r.stderr[-200:]
        giusto = esito == atteso; sbagliati += not giusto
        print(f"{'ok ' if giusto else 'NO '} {nome:18} expected {atteso:7} got {esito}")
    sys.exit(1 if sbagliati else 0)

if __name__ == "__main__":
    if sys.argv[1:2] in (["-h"], ["--help"]):  # aiuto senza Fusion
        sys.stdout.reconfigure(encoding="utf-8"); print(__doc__); sys.exit(0)
    main()
