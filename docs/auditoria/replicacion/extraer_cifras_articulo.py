"""Extrae a CSV cada cifra reportada en el articulo, con su ubicacion exacta.

Tres origenes: celdas de tabla, coordenadas de pgfplots y numeros en prosa.
El CSV resultante es la referencia contra la que se compara la replicacion.
"""
import re, csv, pathlib, sys

TEX = pathlib.Path(sys.argv[1])
OUT = pathlib.Path(sys.argv[2])
src = TEX.read_text(encoding="utf-8", errors="replace")
lines = src.split("\n")
off = [0]
for l in lines:
    off.append(off[-1] + len(l) + 1)
def line_of(pos):
    lo, hi = 0, len(off) - 1
    while lo < hi - 1:
        mid = (lo + hi) // 2
        if off[mid] <= pos: lo = mid
        else: hi = mid
    return lo + 1

NUM = re.compile(r"-?\d[\d,\.]*(?:[eE][-+]?\d+)?")
def to_float(s):
    t = s.strip()
    # 120,200,000 -> 120200000 ; 1.20 -> 1.20 ; 60,57 no aparece en el articulo (usa punto decimal)
    if re.fullmatch(r"-?\d{1,3}(,\d{3})+(\.\d+)?", t): t = t.replace(",", "")
    t = t.replace(",", "")
    try: return float(t)
    except ValueError: return None

def clean(s):
    s = re.sub(r"%.*", "", s)
    for cmd in ("footnotesize","scriptsize","textbf","textit","mathbf","hline","\\\\"):
        s = s.replace("\\" + cmd, " ")
    s = re.sub(r"\\[a-zA-Z@]+\*?", " ", s)
    s = s.replace("$", "").replace("{", " ").replace("}", " ").replace("\\", " ")
    return re.sub(r"\s+", " ", s).strip()

def envs(name):
    """Devuelve (inicio, fin, cuerpo) de cada entorno name, incluida la variante estrellada."""
    out = []
    for m in re.finditer(r"\\begin\{" + name + r"\*?\}", src):
        depth, k = 0, m.start()
        for mm in re.finditer(r"\\(begin|end)\{" + name + r"\*?\}", src[m.start():]):
            depth += 1 if mm.group(1) == "begin" else -1
            if depth == 0:
                k = m.start() + mm.end(); break
        out.append((m.start(), k, src[m.start():k]))
    return out

def meta(body):
    cap = re.search(r"\\caption\s*\{(.+?)\}\s*(?:\\label|\n)", body, re.S)
    lab = re.search(r"\\label\{([^}]*)\}", body)
    return (clean(cap.group(1))[:180] if cap else ""), (lab.group(1) if lab else "")

rows = []
spans = []   # (ini, fin) de tablas y figuras, para excluirlos de la prosa

# ---------- 1. tablas ----------
for ini, fin, body in envs("table"):
    spans.append((ini, fin))
    cap, lab = meta(body)
    for tini, tfin, tab in envs("tabular"):
        if not (ini <= tini < fin): continue
        m0 = re.search(r"\\begin\{tabular\*?\}(\s*\[[^\]]*\])?\s*\{[^}]*\}", tab)
        base = tini + (m0.end() if m0 else 0)          # offset absoluto del cuerpo
        inner = tab[(m0.end() if m0 else 0):]
        inner = re.sub(r"\\end\{tabular\*?\}[\s\S]*$", "", inner)
        pos = 0
        for ri, raw_row in enumerate(inner.split(r"\\")):
            row_abs = base + pos
            pos += len(raw_row) + 2                     # +2 por el separador \\
            if not NUM.search(raw_row): continue
            cells = raw_row.split("&")
            etiqueta = clean(cells[0])[:60]
            cpos = 0
            for ci, cell in enumerate(cells):
                for m in NUM.finditer(cell):
                    v = to_float(m.group(0))
                    if v is None: continue
                    rows.append(dict(archivo=TEX.name, linea=line_of(row_abs + cpos + m.start()),
                                     tipo="tabla", etiqueta_latex=lab, titulo=cap,
                                     fila=f"{ri}:{etiqueta}", columna=ci,
                                     valor_crudo=m.group(0), valor=v))
                cpos += len(cell) + 1

# ---------- 2. figuras pgfplots ----------
for ini, fin, body in envs("figure"):
    spans.append((ini, fin))
    cap, lab = meta(body)
    leg = re.search(r"\\legend\{([^}]*)\}", body)
    series = [clean(x) for x in leg.group(1).split(",")] if leg else []
    for si, pm in enumerate(re.finditer(r"\\addplot[^;]*?coordinates\s*\{(.*?)\}", body, re.S)):
        nombre = series[si] if si < len(series) else f"serie{si}"
        coord_abs = ini + pm.start(1)                  # offset absoluto del bloque de coordenadas
        for cm in re.finditer(r"\(\s*([-\d.eE]+)\s*,\s*([-\d.eE]+)\s*\)", pm.group(1)):
            x, y = to_float(cm.group(1)), to_float(cm.group(2))
            if y is None: continue
            rows.append(dict(archivo=TEX.name, linea=line_of(coord_abs + cm.start(2)),
                             tipo="figura", etiqueta_latex=lab, titulo=cap,
                             fila=f"{nombre} @ x={cm.group(1)}", columna="y",
                             valor_crudo=cm.group(2), valor=y))

# ---------- 3. prosa ----------
def en_span(pos):
    return any(a <= pos < b for a, b in spans)
for m in NUM.finditer(src):
    if en_span(m.start()): continue
    ctx0 = src.rfind("\n\n", 0, m.start())
    pre = src[max(0, m.start()-90):m.start()]
    post = src[m.end():m.end()+50]
    if re.search(r"\\(ref|label|cite|eqref|includegraphics|usepackage|documentclass|input|section|width|height|linewidth|textwidth|cm\]|pt\])", pre[-40:]): continue
    if re.match(r"^\s*(cm|pt|in|mm|\\linewidth|\\textwidth)", post): continue
    v = to_float(m.group(0))
    if v is None: continue
    rows.append(dict(archivo=TEX.name, linea=line_of(m.start()), tipo="prosa",
                     etiqueta_latex="", titulo=clean(pre)[-70:],
                     fila="", columna="", valor_crudo=m.group(0), valor=v))

with OUT.open("w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=["archivo","linea","tipo","etiqueta_latex","titulo","fila","columna","valor_crudo","valor"])
    w.writeheader(); w.writerows(rows)
from collections import Counter
print("cifras extraidas:", len(rows), dict(Counter(r["tipo"] for r in rows)))
print("tablas con cifras:", len({r["etiqueta_latex"] for r in rows if r["tipo"]=="tabla"}))
print("figuras con series:", len({r["etiqueta_latex"] for r in rows if r["tipo"]=="figura"}))
