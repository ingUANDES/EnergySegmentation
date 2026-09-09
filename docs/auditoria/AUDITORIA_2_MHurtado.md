# Auditoría 2 — Memoria de Juan Matías Hurtado y estado del repositorio tras el commit `72e13ce`

Continuación de [`AUDITORIA_memoria_VMunoz.md`](AUDITORIA_memoria_VMunoz.md). Base de comparación: `29cb916` (*pre defensa matías*), el commit sobre el que se hizo la primera auditoría. Estado auditado: `72e13ce` (*pre auditoria Claude Science*).

Verificación con TeX Live 2026 (XeLaTeX para la memoria, LuaLaTeX para la presentación) más BibTeX y Pygments, ejecutando el ciclo completo.

---

## 1. Qué trae el commit `72e13ce`

47 archivos, +1.698 / −358 líneas. El contenido en texto es menor; el peso está en imágenes.

| Cambio | Detalle |
|---|---|
| **Nueva presentación de defensa** | `docs/Presentations/HurtadoDefensa2026/JMHL_presentation.tex` (1.431 líneas, beamer/LuaLaTeX) y su `references.bib` (26 entradas). |
| **Se borró la plantilla** | `docs/Presentations/HurtadoDefensa2026/presentation.tex` fue eliminado. La carpeta se llama `HurtadoDefensa2026` pero ya no contiene una plantilla: contiene la presentación de un alumno. |
| **38 PNG nuevos en la raíz** | Y `image.png` pasó de 56 KB a 1,78 MB. La raíz del repositorio es hoy **el directorio más pesado: 45,3 MB de los 89,2 MB del árbol (51%)**. |
| **Cambios en la memoria** | Sólo dos: la clave `munoz_ethical_2022` → `munoz_lhuillier_inversion_2022` en `attachments/anexo_a.tex:178`, y la eliminación de siete líneas comentadas en la tabla de parámetros de `chapters/chapter02.tex`. |

El commit **no** modificó el texto de los capítulos de la memoria. Lo que hay que auditar como material nuevo es la memoria completa (que no se había auditado) y la presentación.

---

## 2. Bloqueadores de compilación de la memoria de Hurtado

`docs/MemoriaMHurtado/memoria.Rtex` **no compila** desde ninguna ubicación. El diagnóstico es peor que el de la memoria de Muñoz, porque aquí conviven **tres** convenciones de ruta en el mismo archivo maestro:

| Ubicación | Ruta escrita | Relativa a |
|---|---|---|
| `memoria.Rtex:2` | `\input{core/preambulo.tex}` | el documento |
| `memoria.Rtex:54-60` | `\input{chapters/chapter01.tex}` … | el documento |
| `memoria.Rtex:68` | `\bibliography{docs/MemoriaMHurtado/references}` | la raíz del repo |
| `memoria.Rtex:76` | `\input{docs/MemoriaMHurtado/attachments/anexo_a}` | la raíz del repo |
| `chapters/chapter02.tex`, `chapter04.tex` | `\includegraphics{vg1.png}`, `{mprx0.0.png}`, … (11 archivos) | la raíz del repo |

Compilando desde la raíz falla el preámbulo en la primera línea. Compilando desde el directorio del documento fallan la bibliografía, el anexo y las once figuras. No hay ubicación desde la cual el documento resuelva sus propias dependencias.

Además hereda **los mismos defectos de preámbulo que la memoria de Muñoz** —`core/preambulo.tex` es una copia con añadidos—:

| # | Ubicación | Problema | Corrección |
|---|---|---|---|
| 1 | `core/preambulo.tex:61` | `\usetikzlibrary{shadows.blur}` — no existe en PGF actual. | `shadows` |
| 2 | `core/preambulo.tex:101` | `\setmainfont{Times New Roman}` — fuente propietaria; sin ella XeLaTeX compone en `nullfont`. | `TeX Gyre Termes` |
| 3 | `core/preambulo.tex:56` | `\usepackage{gensymb}` — ausente en instalaciones mínimas. | instalarlo |
| 4 | `core/preambulo.tex:46` | `\usepackage[]{minted}` — **aquí sí se usa**: `chapters/chapter03.tex:291`, `296` y `315` contienen `\begin{minted}{julia}` con el código Julia del planificador. | **NO se puede quitar.** Requiere `-shell-escape` y Pygments instalado. |

**El punto 4 es la diferencia importante respecto de la memoria de Muñoz.** Allí `minted` se podía eliminar porque ningún entorno estaba activo; aquí eliminarlo rompe tres bloques de código. La receta de corrección no es transferible entre las dos memorias.

Paquetes adicionales que exige este preámbulo y no trae una instalación mínima: `changes`, `makecell`, `xurl`, `todonotes`, `truncate`.

### 2.1 Errores en el propio código fuente

- **`attachments/anexo_a.tex:171`** — hay una **línea en blanco dentro de `\begin{cases}`**, lo que termina el párrafo en modo matemático y produce cuatro errores en cascada (`Missing $ inserted`, `Extra }`, `Missing } inserted`). Se corrige borrando la línea en blanco.

### 2.2 Resultado tras las correcciones

Con `shadows.blur` → `shadows`, `Times New Roman` → `TeX Gyre Termes`, `\graphicspath{{../../}{./}}`, las dos rutas del maestro normalizadas a relativas al documento, la línea en blanco de `anexo_a.tex` eliminada, y compilando **con `-shell-escape`** y Pygments disponible:

**57 páginas, 0 errores LaTeX, 0 figuras faltantes, 0 referencias cruzadas indefinidas, 0 citas indefinidas.**

BibTeX emite 5 avisos `empty institution` (`international_carbon_action_partnership_eu_2024`, `..._icap_brazilian_2022`, `ministerio_de_energia_de_chile_plan_2024`, `ministerio_del_medio_ambiente_reporte_2024`, `palma_behnke_chilean_2019`): son entradas `@techreport`/`@misc` sin campo `institution`, cosmético.

### 2.3 La extensión `.Rtex` es vestigial

El único fragmento de knitr del proyecto está en `attachments/anexo_b.Rtex`, y `anexo_b` está **comentado** en el maestro (`memoria.Rtex:78`), igual que `anexo_c`. Es decir: la memoria no ejecuta código R y no necesita knitr. `memoria.Rtex` puede pasar a `memoria.tex` sin perder nada, lo que además elimina el paso de knitr del ciclo de compilación en Overleaf.

---

## 3. Bibliografía y referencias cruzadas

`docs/MemoriaMHurtado/references.bib` tiene **25 entradas para 20 citas**: está depurada, en contraste con las 2.038 entradas de la memoria de Muñoz. Es el estándar que conviene adoptar.

Dos claves aparecen citadas y no existen en la bibliografía —`munoz_ethical_2022` y `sims_implications_2003`— pero **ambas están en líneas comentadas** de `attachments/anexo_a.tex` (líneas 76, 88 y 373, dentro de la bitácora de trabajo). No rompen la compilación ni generan citas indefinidas. Vale corregirlas de todos modos si esas líneas se van a reactivar: la clave viva de la primera es `munoz_lhuillier_inversion_2022` y la segunda habría que añadirla.

Existe además `referencesOLD.bib` (sin uso desde ningún documento) que conviene borrar.

---

## 4. El modelo de Hurtado: qué aporta y qué hay que revisar

### 4.1 El aporte teórico es sustantivo

La memoria diagnostica correctamente el problema de fondo de la formulación de `\citeA{amigo_two_2021}` —y lo hace de forma más precisa que la memoria de Muñoz—: la restricción probabilística `Pr(θ ≥ CAP) ≤ ε` **se satisface con igualdad**, de modo que θ = CAP determinísticamente y el subastador no toma ninguna decisión. `chapters/chapter02.tex`, sección *Espacio de Mejora para el Planificador Social*, lo muestra con dos escenarios de `F(θ)` (costo fijo y costo convexo) y concluye que el problema del planificador **está indeterminado**, no sólo mal parametrizado.

La reformulación adopta el marco de anclaje y ajuste de `\citeA{gabaix_behavioral_2019}`:

```
CAP  ~ N(CAP_d, σ²_CAP)        CAP_s = CAP + ε,  ε ~ N(0, σ²_ε)
V(θ,CAP) = π^a·θ − (κ/2)(θ − CAP)²
θ*(CAP_s) = m·CAP_s + (1 − m)·CAP_d + π^a/κ
m = σ²_CAP / (σ²_CAP + σ²_ε)
```

Esto es **cualitativamente superior** a las tres especificaciones de Muñoz por tres razones:

1. **Tiene solución cerrada.** No hay MCP para el subastador, no hay soluciones de esquina, no hay multiplicidad. El problema del planificador se resuelve analíticamente y sólo el bloque de productores queda como MCP.
2. **La atención es un parámetro estructural, no una calibración prestada.** `m` sale de la razón señal/ruido `σ²_CAP/(σ²_CAP+σ²_ε)`, no de un costo `c(P−d)²` importado de un experimento de laboratorio.
3. **Los parámetros están anclados en fuentes chilenas verificables**, y son recientes:

| Parámetro | Valor | Fuente |
|---|---|---|
| `CAP_s` | 264,20 MtCO₂e | Plan de Mitigación del Ministerio de Energía 2024 (escenario de referencia 296 − mitigación 31,8) |
| `CAP_d` | 311,01 MtCO₂e | acumulado 11 años desde 2012, SNICHILE |
| `σ_CAP` | 61,86 MtCO₂e | calibrado |
| `κ` | 64,40 USD/tCO₂e | costo social del carbono oficial de Chile, 2024 |

### 4.2 Cuatro problemas que hay que resolver antes de llevarlo a un artículo

**(a) El término de precio es numéricamente inerte.** Con `κ = 64,40 USD/tCO₂e` y `π^a ≈ 185 USD/tCO₂e`, el término `π^a/κ` de la regla óptima vale **entre 2,85 y 3,09 toneladas**, sobre una decisión `θ*` del orden de 3×10⁸ toneladas: una parte en 10⁸. Verificado contra el Cuadro `tab:resultados_m` de `chapters/chapter04.tex`: los once valores de `θ*` reproducen `m·CAP_s + (1−m)·CAP_d` con un residuo de entre −19,6 y +3,1 toneladas, es decir el residuo no llega ni a distinguirse del redondeo de `CAP_d`. Consecuencia: la lectura de que el planificador "equilibra el incentivo económico con el costo social" **no opera a las unidades calibradas**; el modelo es, numéricamente, puro anclaje. Es un problema de escala, no de álgebra, y se arregla normalizando la penalización.

**(b) La penalización cuadrática está mal escalada por construcción.** `κ` es un costo marginal *lineal* en USD/tCO₂e (el costo social del carbono), pero se usa como coeficiente de un término *cuadrático* en toneladas, de modo que arrastra unidades implícitas de USD/(tCO₂e)². El resultado, para `m = 0,1`:

| Escenario | Ingreso `π^a·θ` | Penalización `(κ/2)(θ−CAP)²` | Razón |
|---|---|---|---|
| `CAP+` | 5,66×10¹⁰ USD | 6,63×10¹⁷ USD | 1,2×10⁷ |
| `CAP−` | 5,66×10¹⁰ USD | 1,67×10¹⁸ USD | 2,9×10⁷ |

La penalización del caso `CAP−` equivale a unas **15.000 veces el PIB mundial**. Los valores de la columna *Costo* del Cuadro `tab:cap_pos_neg_mm` son aritméticamente correctos dado el planteamiento, pero económicamente no interpretables. Hay dos salidas: normalizar la desviación (`(κ/2)·CAP·((θ−CAP)/CAP)²`, que deja el costo en el mismo orden que el ingreso) o usar una penalización lineal `κ·|θ−CAP|`, que es lo que la interpretación de `κ` como costo social del carbono realmente justifica. Esta decisión afecta también el punto (a): con la penalización normalizada, `π^a/κ` deja de ser despreciable.

**(c) La calibración de `σ_ε` no identifica la atención.** El Cuadro `tab:top10_distancia_mix` reporta la distancia absoluta entre el mix modelado y el observado en 2024 para los once niveles de `m`, y es **monótona creciente**: 0,2727 en `m=0` hasta 0,3026 en `m=1`. Por lo tanto el argmin está en la frontera `m=0` (`σ_ε = ∞`), y la elección de `m=0,1` es —como el propio texto reconoce— la de "un valor determinado", no una estimación identificada. Dos consecuencias:

- El criterio **discrimina poco**: el rango completo de atención mueve la distancia sólo un 11%.
- El desajuste **de base es grande**: ~27 puntos porcentuales de desviación absoluta agregada respecto del mix real de 2024 *a cualquier nivel de atención*. Es decir, el modelo no reproduce el mix observado bajo ninguna `m`, y la comparación entre niveles se hace sobre un ajuste que ya es pobre en términos absolutos.

La conclusión defendible con este resultado es la débil: *el mix observado es más compatible con atención baja que con atención alta*. La conclusión fuerte —*Chile opera con `m = 0,1`*— no está sostenida por el criterio.

**(d) Un valor obsoleto en el texto.** `chapters/chapter04.tex` afirma en la sección de calibración que se seleccionó `σ_ε = 186,90`, mientras el cuadro inmediatamente anterior asigna a `m=0,1` el valor `σ_ε = 185,58`. Ambos son consistentes con la fórmula `σ_ε = σ_CAP·√((1−m)/m)`, pero con distintos `σ_CAP`: 185,58 corresponde a `σ_CAP = 61,86` (el del cuadro de parámetros vigente) y 186,90 a `σ_CAP = 62,30`, que es el valor de una tabla anterior hoy comentada en el mismo archivo. El texto quedó con la calibración vieja.

### 4.3 Una decisión de modelación que conviene defender explícitamente

El modelo fija `CAP ~ N(CAP_d, σ²_CAP)`: la media del presupuesto verdadero es `CAP_d = 311,01` MtCO₂e, el acumulado histórico, mientras que `CAP_s = 264,20` MtCO₂e —la estimación más reciente y mejor informada, del Plan de Mitigación 2024— entra como **señal ruidosa**. Dentro del marco de Gabaix esto es coherente (el valor por defecto es lo que el agente infiere sin atención), pero implica que la tendencia histórica es el centro no sesgado del presupuesto verdadero y que la meta de política es lo observado con ruido. Es una asignación de roles que hay que argumentar, porque de ella depende el signo de todo el resultado: es lo que hace que "más atención" equivalga a "presupuesto más estricto".

Como referencia externa útil: la propia memoria cita que la literatura recogida por `\citeA{gabaix_behavioral_2019}` estima una atención promedio de **0,44**, frente al `m ≈ 0,1` que la calibración chilena sugiere. Ese contraste es material publicable.

---

## 5. La presentación `JMHL_presentation.tex`

- **29 de sus figuras son PNG de la raíz del repositorio**, y la mayoría son **capturas de pantalla del contenido de la memoria**: `simbologia.png` (2,03 MB), `objetivo.png`, `limitciones.png`, `parametros2.png`, `codificacion.png`, `calibracion2.png`, `MODELOILUS1.png`, `cccc.png`. Son tablas, ecuaciones y diagramas que ya existen como LaTeX en la memoria, versionados como imágenes de 1 a 2 MB cada una. Esto es el origen directo del crecimiento de la raíz.
- Las rutas son relativas a la raíz del repositorio. Verificado: compilada **desde la raíz** produce **47 páginas, 0 errores, 0 figuras faltantes**; compilada desde su propia carpeta produce las mismas 47 páginas con **25 errores de `luatex.def`** y las figuras sustituidas por cajas vacías (`using draft setting`). Las 29 son las figuras de la raíz que la presentación referencia en su fuente, no un conteo de cajas vacías tomado del log. Es decir, la presentación es consistente con la convención de Overleaf-desde-la-raíz — a diferencia de la memoria de Hurtado, que no compila desde ninguna ubicación. El costo de esa consistencia es que obliga a la raíz a funcionar como carpeta de figuras.
- Sus dependencias propias (`fontspec` con las DM Sans en `font/`, `academicons`, `fontawesome5`, `tcolorbox`, `appendixnumberbeamer`, `lualatex-math`) están correctamente incluidas en la carpeta o son instalables; exige LuaLaTeX o XeLaTeX, no pdfLaTeX.
- Su `references.bib` (26 entradas) trae **fuentes institucionales chilenas actuales** que no están en ninguna otra bibliografía del repositorio: Plan de Mitigación 2024, anteproyecto del Ministerio del Medio Ambiente 2025, Reporte del Coordinador Eléctrico Nacional 2024, Leyes 20.780 y 21.455, ICAP. Es material directamente reutilizable para la sección institucional del artículo.

---

## 6. Estado del repositorio tras el commit

| Métrica | `29cb916` | `72e13ce` |
|---|---|---|
| Peso del árbol | 87 MB | **89,2 MB** |
| Imágenes en la raíz | 56 | **96** (45,3 MB) |
| — de ellas, compuestas por algún documento | — | 37 (28,3 MB) |
| — de ellas, **sin uso** | — | **59 (17,0 MB)**, incluida una referenciada sólo en un bloque comentado |
| Archivos duplicados exactos | 99 | 99 (15,5 MB) |
| `.gitignore` | no existe | no existe |

**Corrección respecto de la primera versión de este informe**: los conteos eran 94/37/57 y los correctos son **96 / 37 / 59**. Dos errores se compensaban en parte. Primero, `git ls-tree --name-only` entrega entrecomillados los nombres con acento, de modo que el filtro por extensión omitía `3añosproduccion.png` y `costo precisión gabaix.png`: la raíz tiene 96 imágenes, no 94. Segundo, `costo precisión gabaix.png` aparece en un `\includegraphics` de `attachments/anexo_a.tex` pero **dentro de un bloque `figure` íntegramente comentado**, así que no se compone en el PDF y cuenta como sin uso, no como referenciada.

Las 37 imágenes de la raíz que sí se componen pertenecen todas a **la memoria y la presentación de Hurtado** (30 referencias en la presentación, 6 en `chapter02.tex` y 5 en `chapter04.tex`, con tres archivos compartidos por los dos documentos). Ninguna otra fuente del repositorio referencia la raíz. Es decir: la raíz funciona hoy como carpeta de figuras de un solo alumno, y arrastra además 57 archivos que nadie usa.

Hay señales claras de iteración de capturas dejadas en el árbol: `cccc.png` y `CCCC.png`; `embudo.png`, `A.embudo.png`, `bmbudo.png` y `mbudoo.png`; `melect.png`, `melect1.png`, `melect2.png` y `melect3.png`; `MODELOILUS1.png` y `MODELOILUS2.png`; `calibracion.png` y `calibracion2.png`. De cada grupo, en general sólo una está referenciada.

El plan concreto de reordenamiento está en [`PLAN_ORDEN_REPOSITORIO.md`](PLAN_ORDEN_REPOSITORIO.md).

---

## 7. Orden de trabajo sugerido para la memoria de Hurtado

1. Corregir la línea en blanco dentro de `\begin{cases}` en `attachments/anexo_a.tex:171`.
2. Preámbulo: `shadows.blur` → `shadows`, `Times New Roman` → `TeX Gyre Termes`. **Conservar `minted`** y documentar en `LEEME.txt` que la compilación exige `-shell-escape` y Pygments.
3. Normalizar a relativas al documento las dos rutas de `memoria.Rtex` (`\bibliography` y `\input` del anexo) y añadir `\graphicspath` mientras las figuras sigan en la raíz.
4. Renombrar `memoria.Rtex` → `memoria.tex` (no hay código R activo).
5. Corregir `σ_ε = 186,90` → `185,58` en el texto de `chapters/chapter04.tex`, o recalibrar con `σ_CAP = 62,30` de forma consistente en todo el capítulo.
6. Reescalar la penalización de `eq:utilidadv` y recalcular las columnas de costo y utilidad de los Cuadros `tab:cap_pos_neg_mm`, `tab:resultados_m` y `tab:resultados_m_2`.
7. Reformular la conclusión de la calibración en su versión débil (compatibilidad con atención baja) y reportar el desajuste absoluto de base.
8. Rellenar resumen, agradecimientos, dedicatoria y `\nombreprofdos` en `memoria.Rtex` (siguen con el texto de plantilla, igual que en la memoria de Muñoz).
