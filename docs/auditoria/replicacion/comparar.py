"""Cruza cada celda de las tablas del articulo contra la corrida que le corresponde.

Entradas
  cifras_articulo.csv        toda cifra reportada, con su ubicacion exacta
  auditoria/corridas_todas.csv  una fila por punto de la grilla resuelto con PATH

Salida
  auditoria/replicacion.csv  una fila por celda comparada, con veredicto

Tolerancia: 0,5 % relativo. El articulo imprime dos decimales en los precios y
redondea las razones a dos o tres, de modo que una diferencia por debajo de ese
umbral es redondeo y no discrepancia. Las razones theta/CAP se comparan con
tolerancia absoluta de 0,006, que es media unidad del ultimo decimal impreso.
"""
import csv, math, pathlib, collections

D_PUB = 0.798                      # rendimiento con informacion publica
TOL_REL = 0.005
TOL_ABS_RATIO = 0.006

art = list(csv.DictReader(open("cifras_articulo.csv")))
runs = list(csv.DictReader(open("auditoria/corridas_todas.csv")))

def f(x):
    try: return float(x)
    except (TypeError, ValueError): return None

# ---- indice de corridas por (modelo, P, cm, CAP) ----
idx = {}
for r in runs:
    key = (r["modelo"], r["P"], r["cm"], f(r["CAP"]))
    idx[key] = r

def buscar(modelo, P=None, cm=None, CAP=None):
    for (m, p, c, cap), r in idx.items():
        if m != modelo: continue
        if P is not None and (f(p) is None or not math.isclose(f(p), P, rel_tol=1e-9)): continue
        if cm is not None and (f(c) is None or not math.isclose(f(c), cm, rel_tol=1e-9)): continue
        if CAP is not None and (cap is None or not math.isclose(cap, CAP, rel_tol=1e-9)): continue
        return r
    return None

# ---- rendimiento implicado por cada modelo ----
def rendimiento(modelo, r, CAP):
    th, rp = f(r.get("theta")), f(r.get("r_p"))
    if modelo == "quadratic_rate" and th is not None:
        return 1 - ((th - CAP) / CAP) ** 2          # P = 1 - ((theta-CAP)/CAP)^2
    if modelo == "precision" and rp is not None:
        return D_PUB + rp / CAP                      # P = d + r_p/CAP
    return None

# ---- que columna de cada tabla es que magnitud ----
TABLAS = {
    "efectopenthetapia":     dict(modelo="profit_oriented", clave="P",
                                  cols={1: "theta", 2: "ratio", 3: "pi_a"}, CAP=1e8),
    "efectocapthetapia":     dict(modelo="profit_oriented", clave="CAP_millones",
                                  cols={1: "theta", 2: "ratio", 3: "pi_a"}, P=0.8),
    "resultadostasacuadrada": dict(modelo="quadratic_rate", clave="CAP",
                                  cols={1: "theta", 2: "rend", 3: "ratio", 4: "pi_a"}, cm=9.9e9),
    "resultadosprecision":   dict(modelo="precision", clave="CAP",
                                  cols={1: "theta", 2: "rend", 3: "ratio", 4: "pi_a"}, cm=4e6),
}

filas = []
for lab, spec in TABLAS.items():
    celdas = [a for a in art if a["etiqueta_latex"] == lab and a["tipo"] == "tabla"]
    # agrupar por fila de la tabla
    porfila = collections.defaultdict(dict)
    for c in celdas:
        porfila[c["fila"]][int(c["columna"])] = c
    for fila, cols in sorted(porfila.items(), key=lambda kv: int(kv[0].split(":")[0])):
        if 0 not in cols: continue
        primera = f(cols[0]["valor_crudo"].replace(",", ""))
        if primera is None: continue
        # la primera columna identifica la corrida
        if spec["clave"] == "P":
            cand = [buscar(spec["modelo"], P=primera, cm=cm, CAP=spec["CAP"]) for cm in (9.2e11, 9.2e8)]
        elif spec["clave"] == "CAP_millones":
            cand = [buscar(spec["modelo"], P=spec["P"], cm=cm, CAP=primera * 1e6) for cm in (9.2e11, 9.2e8)]
        else:
            cand = [buscar(spec["modelo"], cm=spec["cm"], CAP=primera)]
        for r in cand:
            if r is None: continue
            CAP = f(r["CAP"])
            for ci, magnitud in spec["cols"].items():
                if ci not in cols: continue
                pub = f(cols[ci]["valor_crudo"].replace(",", ""))
                if pub is None: continue
                if magnitud == "theta":   rep = f(r["theta"])
                elif magnitud == "pi_a":  rep = f(r["pi_a"])
                elif magnitud == "ratio": rep = (f(r["theta"]) / CAP) if (f(r["theta"]) and CAP) else None
                elif magnitud == "rend":  rep = rendimiento(spec["modelo"], r, CAP)
                else: rep = None
                if rep is None:
                    veredicto, dif = "no reproducible", None
                else:
                    if magnitud == "ratio":
                        coincide = abs(rep - pub) <= TOL_ABS_RATIO
                    elif magnitud == "rend":
                        coincide = abs(rep - pub) <= 0.006
                    else:
                        coincide = pub != 0 and abs(rep - pub) / abs(pub) <= TOL_REL
                    dif = (rep - pub) / abs(pub) if pub else None
                    veredicto = "coincide" if coincide else "difiere"
                filas.append(dict(
                    tabla=lab, fila=fila, magnitud=magnitud,
                    modelo=spec["modelo"], c=r["cm"], P=r["P"], CAP=r["CAP"],
                    publicado=pub, replicado=rep,
                    dif_relativa=(round(dif, 6) if dif is not None else ""),
                    veredicto=veredicto,
                    estado_solver=r["estado_crudo"] or r["estado"],
                    linea_tex=cols[ci]["linea"],
                ))

out = pathlib.Path("auditoria/replicacion.csv")
with out.open("w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(filas[0].keys())); w.writeheader(); w.writerows(filas)

cnt = collections.Counter((r["tabla"], r["veredicto"]) for r in filas)
print(f"celdas comparadas: {len(filas)}")
for (tab, ver), n in sorted(cnt.items()):
    print(f"  {tab:26} {ver:16} {n}")
