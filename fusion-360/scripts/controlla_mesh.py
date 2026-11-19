"""Checks an exported STL (binary or ASCII) or 3MF file, before giving it to the slicer. Standard library only.

Usage: python -I controlla_mesh.py file.stl|file.3mf [--atteso-mm X Y Z] [--atteso-volume-mm3 V]
Checks: the file exists and is not empty; units (3MF); triangles; bounding box in mm; **closed** (every edge used by exactly
2 triangles, in opposite directions = consistent normals); signed volume (positive = normals pointing outwards); comparison with the
expected dimensions AXIS BY AXIS (X, Y, Z: a rotated part does not pass, unless --qualsiasi-orientamento); 3MF: <build> transforms applied (tolerance 0.01 mm / 0.1 %). Vertices are merged by EXACT value (no rounding, which invents holes or
hides them: defect of the An-Gah-V skill). Exits with code 1 if a check fails.
"""
import argparse, collections, json, re, struct, sys, zipfile

def leggi_stl(percorso):
    b = open(percorso, "rb").read()
    if len(b) >= 84:
        n = int.from_bytes(b[80:84], "little")
        if 84 + 50 * n == len(b):  # binary
            tri = []
            for i in range(n):
                o = 84 + 50 * i + 12
                tri.append(tuple(struct.unpack("<3f", b[o + 12 * k:o + 12 * k + 12]) for k in range(3)))
            return tri, "mm (STL does not declare units: Fusion exports in mm)"
    v = [tuple(map(float, m)) for m in re.findall(rb"vertex\s+(\S+)\s+(\S+)\s+(\S+)", b)]
    return [tuple(v[i:i + 3]) for i in range(0, len(v) - 2, 3)], "mm (ASCII STL, units not declared)"

def leggi_3mf(percorso):
    z = zipfile.ZipFile(percorso)
    nome = next(n for n in z.namelist() if n.lower().endswith(".model"))
    t = z.read(nome).decode("utf-8")
    unita = (re.search(r'<model[^>]*\bunit="([^"]+)"', t) or [None, "millimeter (3MF default)"])[1]
    scala = {"micron": 0.001, "millimeter": 1, "centimeter": 10, "inch": 25.4, "foot": 304.8, "meter": 1000}.get(unita.split()[0], 1)
    # objects by id; the <build> says which ones to print and with which transform (3MF core spec: row «m00 m01 m02 m10 … m32»)
    oggetti = {}
    for oid, corpo_ in re.findall(r'<object\s(?:[^>]*\s)?id="(\d+)"[^>]*>(.*?)</object>', t, flags=re.S):
        if "<components>" in corpo_:
            raise ValueError("3MF with <components>: not handled by this check")
        mesh = re.search(r"<mesh>(.*?)</mesh>", corpo_, flags=re.S)
        if mesh:
            oggetti[oid] = mesh.group(1)
    elementi = re.findall(r'<item\s([^>]*)/?>', re.search(r"<build>(.*?)</build>", t, flags=re.S).group(1)) if "<build>" in t else []
    tri = []
    for el in elementi or [f'objectid="{k}"' for k in oggetti]:
        oid = re.search(r'objectid="(\d+)"', el).group(1)
        m = re.search(r'transform="([^"]+)"', el)
        M = [float(x) for x in m.group(1).split()] if m else [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0]
        tr = lambda x, y, z: (x * M[0] + y * M[3] + z * M[6] + M[9], x * M[1] + y * M[4] + z * M[7] + M[10], x * M[2] + y * M[5] + z * M[8] + M[11])
        vs = [tuple(v * scala for v in tr(*map(float, q))) for q in re.findall(r'<vertex\s+x="([^"]+)"\s+y="([^"]+)"\s+z="([^"]+)"', oggetti[oid])]
        for a, b_, c in re.findall(r'<triangle\s+v1="(\d+)"\s+v2="(\d+)"\s+v3="(\d+)"', oggetti[oid]):
            tri.append((vs[int(a)], vs[int(b_)], vs[int(c)]))
    return tri, unita

def analizza(tri):
    spigoli = collections.Counter()
    vol = 0.0
    for a, b, c in tri:
        for p, q in ((a, b), (b, c), (c, a)):
            spigoli[(p, q)] += 1
        vol += (a[0] * (b[1] * c[2] - b[2] * c[1]) - a[1] * (b[0] * c[2] - b[2] * c[0]) + a[2] * (b[0] * c[1] - b[1] * c[0])) / 6
    aperti = sum(1 for (p, q), n in spigoli.items() if spigoli.get((q, p), 0) == 0)
    doppi = sum(1 for n in spigoli.values() if n > 1)
    pts = [p for t in tri for p in t]
    lo = [min(p[i] for p in pts) for i in range(3)]
    hi = [max(p[i] for p in pts) for i in range(3)]
    return {"triangoli": len(tri), "spigoli_aperti": aperti, "spigoli_stesso_verso_ripetuti": doppi,
            "chiuso_e_coerente": aperti == 0 and doppi == 0, "volume_mm3": round(vol, 4),
            "ingombro_min_mm": [round(x, 4) for x in lo], "dimensioni_mm": [round(hi[i] - lo[i], 4) for i in range(3)]}

def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--atteso-mm", nargs=3, type=float)
    ap.add_argument("--atteso-volume-mm3", type=float)
    ap.add_argument("--qualsiasi-orientamento", action="store_true",
                    help="compares the dimensions ignoring the axes (normally X, Y, Z must match: model Z = print Z)")
    a = ap.parse_args()
    import os
    esito = {"file": a.file, "esiste": os.path.exists(a.file), "byte": os.path.getsize(a.file) if os.path.exists(a.file) else 0}
    ok = esito["esiste"] and esito["byte"] > 0
    if ok:
        tri, unita = (leggi_3mf if a.file.lower().endswith(".3mf") else leggi_stl)(a.file)
        esito["unita"] = unita
        esito.update(analizza(tri) if tri else {"triangoli": 0})
        ok = bool(tri) and esito["chiuso_e_coerente"] and esito["volume_mm3"] > 0
        if a.atteso_mm:
            ord_ = sorted if a.qualsiasi_orientamento else list
            esito["misure_ok"] = all(abs(x - y) <= 0.01 for x, y in zip(ord_(esito["dimensioni_mm"]), ord_(a.atteso_mm)))
            ok = ok and esito["misure_ok"]
        if a.atteso_volume_mm3:
            esito["volume_ok"] = abs(esito["volume_mm3"] - a.atteso_volume_mm3) <= 0.001 * a.atteso_volume_mm3
            ok = ok and esito["volume_ok"]
    esito["ESITO"] = "OK" if ok else "NON OK"
    print(json.dumps(esito, indent=2, ensure_ascii=False))
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
