# Auditoría — Memoria de Vicente Muñoz L'Huillier y borrador de artículo

**Repositorio:** `ingUANDES/EnergySegmentation` (público, rama única `master`, 38 MB)
**Memoria auditada:** `docs/DocumentoMemoria/` — *Inversión en capacidad de generación eléctrica cuando la atención del planificador es limitada*, Julio 2022, profesor guía Sebastián Cea Echenique.
**Borrador de artículo:** `Submissions/EnergyPolicy/cas-dc-template.tex` — *Inattention rises energy prices*, Cea-Echenique, Feijoo y Muñoz.
**Presentación de referencia:** `docs/Presentations/UVigo/home.Rmd` — *Cap-and-trade in Energy Capacity Investment when the planner is inattentive*.

La verificación de compilación se hizo con TeX Live 2026 (XeLaTeX para la memoria, pdfLaTeX para el artículo) más BibTeX, ejecutando el ciclo completo `latex → bibtex → latex → latex`.

---

## 1. Bloqueadores de compilación (memoria)

Tal como está versionada, `docs/DocumentoMemoria/memoria.tex` **no compila** — ni desde la raíz del repositorio ni desde su propio directorio. Cuatro causas, todas en `core/preambulo.tex`:

| # | Ubicación | Problema | Corrección |
|---|---|---|---|
| 1 | `core/preambulo.tex:41` | `\usepackage[outputdir=docs/DocumentoMemoria]{minted}` — la opción `outputdir` está fijada a la ruta de Overleaf, exige `-shell-escape` y Pygments instalado. **Ningún entorno `minted` se usa realmente**: las únicas apariciones en los capítulos están comentadas (`chapter02.tex:194-200`). | Eliminar el paquete. |
| 2 | `core/preambulo.tex:58` | `\usetikzlibrary{shadows.blur}` — esa librería no existe en las versiones actuales de PGF (sólo `shadows`); aborta la carga del preámbulo. | `\usetikzlibrary{shadows}`. |
| 3 | `core/preambulo.tex:99` | `\setmainfont{Times New Roman}` — fuente propietaria de Microsoft. Donde no esté instalada, XeLaTeX cae a `nullfont` y el documento se compone **sin ningún glifo** (24.082 mensajes `Missing character`). | `\setmainfont{TeX Gyre Termes}` (clon libre y métricamente equivalente). |
| 4 | `core/preambulo.tex:53` | `\usepackage{gensymb}` — el paquete no está en instalaciones mínimas de TeX Live y detiene la compilación antes de llegar al cuerpo. | Instalar `gensymb`, o reemplazar `\degree` por `\textdegree`. |

### 1.1 Contradicción de rutas relativas — el bloqueador de fondo

El documento mezcla **dos convenciones incompatibles** de rutas relativas, y no hay `\graphicspath` que las reconcilie:

- **Relativas a la raíz del repositorio** (convención Overleaf): las 10 figuras de capítulos y anexo, p. ej. `chapter02.tex:566` → `docs/DocumentoMemoria/core/images/Tabla amigo.png`.
- **Relativas al directorio del documento**: el logo institucional en `core/primeras_paginas.tex:26` → `logos/Logo-UANDES.png`, y la fuente del logo de Julia en `core/julialogo.sty:20` → `Path = fonts/`.

Verificado empíricamente:

- Compilando **desde la raíz**: falla el logo (`Package graphics Error: Division by 0` en `primeras_paginas.tex:50`, porque no existe `logos/` en la raíz).
- Compilando **desde `docs/DocumentoMemoria`**: fallan las 10 figuras de capítulos (`File 'docs/DocumentoMemoria/core/images/...' not found`).

**Corrección mínima verificada:** añadir `\graphicspath{{../../}{./}}` tras `\usepackage{graphicx}` y compilar desde el directorio del documento. La corrección robusta es normalizar las 10 rutas a `core/images/...` y prescindir del `graphicspath`.

### 1.2 Resultado tras las correcciones

Aplicando los cuatro cambios anteriores más el `\graphicspath`, la memoria compila **limpia**: **112 páginas**, 0 errores LaTeX, 0 figuras faltantes, 0 referencias cruzadas indefinidas y **1 sola cita indefinida** (ver §3).

---

## 2. Contenido sin terminar (memoria)

Elementos de plantilla que quedaron sin llenar y se imprimen tal cual en el PDF:

| Ubicación | Contenido actual |
|---|---|
| `memoria.tex:16` | Resumen: *"Hacer resumen al terminar la tesis. Máximo 1 página"* — **la memoria no tiene abstract**. |
| `memoria.tex:20` | Agradecimientos: *"Muchas gracias a todos"* |
| `memoria.tex:23` | Dedicatoria: *"ok.."* |
| `memoria.tex:10-11` | `\nombreprofdos` = *"Nombre Profe 2"*, `\nombreproftres` = *"Nombre Profesor Invitado"* — la página de firmas de la comisión sale con nombres de plantilla. |

Además, el capítulo 5 (conclusiones) tiene 522 palabras y **no reporta ni una cifra**: cierra en términos cualitativos ("menor cantidad de permisos, menor precio") sobre un capítulo de resultados de 7.502 palabras.

---

## 3. Bibliografía y referencias cruzadas

**Memoria.** 164 etiquetas definidas, 109 referencias cruzadas, **todas resueltas y sin duplicados** — esto está sano. La única cita indefinida es:

- `d__aertrycke_risk_2017`, citada en `chapter01.tex` (metodología) y `chapter02.tex:76`. La entrada existe en `references.bib:13585` pero con la clave **`de_maere_d__aertrycke_risk_2017`** — que es además la clave que usa la bibliografía de la presentación (`referencesPres.bib:32`). Es un desajuste de nombre, no una referencia ausente.

`docs/DocumentoMemoria/references.bib` tiene **2.038 entradas** para un documento que cita 17: es el volcado completo de una biblioteca Zotero. Conviene reducirlo a las entradas efectivamente citadas.

**Borrador de artículo.** `Submissions/EnergyPolicy/references.bib` tiene 336 entradas y **2 claves citadas que no existen**: `feijoo_design_2014` y `ferris_complementarity_2000`. Además, el resumen cita "Sims (2003)" y "Amigo et alii (2021)" como texto plano; Sims (2003) no tiene entrada en la bibliografía.

---

## 4. Defectos tipográficos verificados en el PDF

| Ubicación | Problema | Cómo se imprime |
|---|---|---|
| `chapter03.tex:274-275` | Falta el separador `\\` entre las dos restricciones del `eqnarray`. | La ecuación (3.17) sale como una sola línea: `θπᵃP − c(P−d)² ≥ 0 (η)θ ≥ 0 (ϱ)`. La etiqueta `perforconrestrfact:r1` queda además compartiendo número con la segunda restricción. |
| `chapter03.tex:302` | Signo `+` sobrante antes del `\perp`. | `0 ≤ −Pπᵃ(1+η)+ ⊥ θ ≥ 0`. La misma condición aparece correcta en `chapter04.tex:104`. |

---

## 5. Consistencia numérica

Se extrajeron programáticamente todas las tablas y todas las series `pgfplots` de la memoria (capítulo 4), del borrador de artículo y de la presentación UVigo, y se cruzaron θ, θ/CAP, πᵃ y πᵈ por presupuesto de carbono y por modelo.

**Lo que está consistente:**

- La presentación UVigo reproduce **exactamente** las tres tablas de la memoria (rendimiento a CAP=100, CAP múltiple *profit-oriented*, y *welfare-oriented*): **0 discrepancias**.
- Los cocientes θ/CAP impresos coinciden con los calculados desde θ en todas las filas.
- Las series de los modelos Original, Tasa Cuadrada y Precisión coinciden con sus tablas.

**Lo que no cuadra — 2 celdas, idénticas en la memoria y en el borrador:**

| CAP | πᵃ en la tabla `efectocapthetapia` | πᵃ en la figura `piapormodelo` |
|---|---|---|
| 200 MtCO₂e | \$60,57 | \$161,56 |
| 800 MtCO₂e | \$152,50 | \$48,76 |

Los otros ocho presupuestos coinciden. **La serie de la figura es la internamente consistente.** Al normalizar el precio *profit-oriented* por el del modelo original en cada presupuesto, la figura entrega una razón suave —entre 0,771 y 0,880, con desviación estándar 0,032— mientras que las dos celdas de la tabla rompen por completo ese patrón (0,330 en CAP=200 y 2,564 en CAP=800, sobre una razón media de 0,838). Todo indica que las dos celdas de la tabla son errores de transcripción respecto de la salida del solver que sí está graficada.

Nota importante: la memoria **construye un argumento sobre el valor de CAP=800** (`chapter04.tex`, tras el Cuadro `efectocapthetapia`): *"existen saltos extraños como en el CAP=800MtCO₂, donde se emiten muchos permisos y los precios aumentan"*. Ese salto sólo existe con el \$152,50 de la tabla; con el \$48,76 de la figura la serie es monótona decreciente y la anomalía desaparece. Es decir: ese párrafo de interpretación se apoya en lo que el test de consistencia señala como un error de transcripción, y debe eliminarse junto con la corrección de las dos celdas. El artículo entregado no reproduce ese argumento; en su lugar explica la caída de \(\theta/CAP\) por el traspaso del costo de precisión a los compradores de permisos, que es lo que la serie monótona sí sostiene. **No se modificó ninguna cifra**: las dos celdas quedan tal cual en ambos documentos, a la espera de que los autores confirmen la salida del solver.

**Calibración.** Los valores de `c` que fija la memoria son:

| Modelo | `c` calibrado (memoria) | `c` declarado (presentación) |
|---|---|---|
| Profit Oriented | \$920.000.000.000 (`chapter04.tex`, Cuadro `calibracionPO2`) | `c=920M` → **error de 3 órdenes de magnitud** |
| Welfare Oriented — Tasa Cuadrada | \$9.900.000.000 (Cuadro `calibracioncuadrado`) | `c=9920M` → coincide salvo redondeo |
| Welfare Oriented — Precisión | \$4.000.000 (Cuadro `calibracionprecision`) | no aparece en la presentación |

---

## 6. Estado del borrador de artículo

Compila a **13 páginas**, pero:

- **Las 9 figuras salen como cajas vacías.** Todas las rutas `\includegraphics` son relativas a la raíz del repositorio (`Submissions/EnergyPolicy/Images/...`), no al directorio del artículo. Una de ellas (`cas-dc-template.tex:457`) apunta además al árbol de la memoria: `docs/DocumentoMemoria/core/images/distribucion segunda etapa.png`. Ese archivo es **byte a byte idéntico** a `Images/distribucion segunda etapa PO.png`, que ya está en la carpeta del artículo, así que basta apuntar a la copia local.
- **Falta por completo la formulación del modelo.** La presentación UVigo desarrolla demanda, decisiones del productor en primera y segunda etapa, objetivo, restricciones, problema del subastador y definición de equilibrio con sus condiciones de vaciado de mercado. En el borrador, la sección de modelo pasa de un esbozo en prosa de Amigo et al. directamente a los resultados. Es el hueco estructural más grande respecto de la presentación.
- **No hay sección de resultados.** Las tres subsecciones de resultados están anidadas bajo `\section{Model description}`.
- **Marcadores y huecos de redacción:** `x\%` y `according to XX` en la introducción; `RESUMIR INFO RELEVANTE DE \cite{...}` y una frase cortada (*"The literature on behavioral preferences of the planner is...."*) en la revisión de literatura; `WHY IS THIS HAPPENING?? ANALISIS` en el análisis; `% ESTA PARTE LA ELIMINAMOS ENTONCES??` sobre un bloque del modelo; los highlights siguen siendo *"primero / segundo / tercero"*; `\section{Conclusion}` está **vacía**; el anexo cierra con *"Each scenario is defined as ..."*.
- **Un párrafo duplicado literalmente** (el que empieza *"On the contrary, these prices may be the product of more permits issued..."*).
- **Referencia cruzada equivocada:** la sección del modelo de tasa cuadrada remite a `\ref{rendcap}`, que es la figura del modelo *profit-oriented*; debería ser `rendcapTC`.
- El archivo **conserva el nombre de la plantilla de Elsevier** (`cas-dc-template.tex`).
- Dos figuras de `Images/` no se usan: `distribucion segunda etapa PO.png` y `ratio per cap.png`.

---

## 7. Higiene del repositorio

- **No existe `.gitignore`.** De ahí que estén versionados 11 artefactos de compilación y respaldos de editor: `memoria.log`, `.aux`, `.bbl`, `.blg`, `.toc`, `.lof`, `.lot`, `memoria.tex.bak`, `core/preambulo.tex.bak`, `core/primeras_paginas.tex.bak`, `docs/Presentations/UVigo/tikz1779c212df233.log`, y el binario `code/cnt_2050_total_cap900_scenarios.gdx`.
- **58 PNG sueltos en la raíz** del repositorio (3,8 MB), sin carpeta ni referencia desde ningún documento.
- **99 archivos son duplicados exactos** (mismo hash). Los focos: tres árboles `Figures/` prácticamente idénticos de 5,2 MB cada uno en `Submissions/AppliedEnergy_V2`, `Submissions/draft_paper` y `Submissions/Energy_8000/R1`; el árbol `Apuntes/` duplicado en la raíz y en `docs/Apuntes/`; y `docs/DocumentoMemoria/images/` que replica archivos de `core/images/` (sólo se referencia `core/images/`).
- **`attachments/metodologia.tex` está huérfano** — no lo incluye ningún archivo. El `memoria.log` versionado muestra que la última compilación registrada murió justamente buscándolo, lo que sugiere que se quitó del `\input` sin borrarlo.
- **`docs/Memoria/` es una plantilla muerta** — 5 archivos de `core/` y un `anexo_a.tex`, sin documento maestro.

---

## 8. Observación de fondo sobre el modelo

En el modelo *Profit Oriented*, el rendimiento `P` (la precisión con que el subastador estima el presupuesto de carbono) es un **parámetro exógeno**, no una variable de decisión: se recorre una grilla de valores de `P` y se resuelve el MCP para cada uno. Por lo tanto ese modelo no incorpora todavía atención racional en sentido estricto — no hay elección endógena de cuánta información adquirir. En el modelo de Precisión, donde `P` sí es endógeno, la solución se queda pegada en `P = 0,798` para todos los presupuestos, es decir en una solución de esquina sin adquisición de información.

Esto es coherente con lo que la propia presentación reconoce en sus comentarios finales (*"Unclear relation of inattention"*, *"Multiple solutions and comparative statics"*) y con la recomendación del capítulo 5 de la memoria. Es la limitación que el artículo debe declarar explícitamente en lugar de presentar los tres modelos como implementaciones equivalentes de atención racional.

---

## 9. Orden de trabajo sugerido

1. Los cuatro cambios de `core/preambulo.tex` más el `\graphicspath` — la memoria pasa a compilar (112 páginas).
2. Corregir la clave `d__aertrycke_risk_2017` → `de_maere_d__aertrycke_risk_2017`.
3. Decidir cuál valor de πᵃ es correcto en CAP=200 y CAP=800, y ajustar el párrafo de interpretación del "salto" en CAP=800.
4. Corregir `c=920M` → `c=920.000M` en la presentación UVigo.
5. Los dos defectos tipográficos de `chapter03.tex` (líneas 274-275 y 302).
6. Rellenar resumen, agradecimientos, dedicatoria y nombres de la comisión.
7. Añadir `.gitignore`, sacar los artefactos de compilación del control de versiones y ordenar los 58 PNG de la raíz.
8. Para el artículo: normalizar rutas de figuras, escribir la sección de modelo que falta, separar la sección de resultados, completar conclusiones y highlights, y agregar las dos entradas bib ausentes.
