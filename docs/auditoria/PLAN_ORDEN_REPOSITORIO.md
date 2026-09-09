# Plan de orden y limpieza — `ingUANDES/EnergySegmentation`

Estado auditado: `72e13ce`. **447 archivos, 89,2 MB.** Inventario de la raíz en [`inventario_raiz.csv`](inventario_raiz.csv).

---

## 1. Diagnóstico: el problema es uno, no cinco

Todos los síntomas —figuras en la raíz, duplicados, memorias que no compilan, artefactos versionados— vienen de la misma causa: **el repositorio se ha usado como si fuera un único proyecto de Overleaf**, donde todo es relativo a la raíz y todo convive en un espacio de nombres plano. Cada documento nuevo (memoria, presentación, submission) se añadió a ese espacio en vez de recibir una carpeta autocontenida.

De ahí las tres consecuencias medibles:

| Síntoma | Medida |
|---|---|
| La raíz es el directorio más pesado | **97 archivos, 45,3 MB — el 51% del repositorio** |
| Nada compila desde una ubicación única | ninguna de las dos memorias compila sin corregir rutas; la presentación de Hurtado sólo compila desde la raíz; el borrador del artículo perdía sus nueve figuras |
| Duplicación por copia entre carpetas | **99 archivos redundantes, 15,5 MB** en 69 grupos |

## 2. Inventario actual

| Directorio | Archivos | MB | Qué es |
|---|---|---|---|
| `(raíz)` | 98 | 45,3 | 96 imágenes + README + `.gitignore`. 38 las usan la memoria y la presentación de Hurtado; **58 (16,9 MB) no las usa nadie** |
| `docs/Presentations/IFORS` | 79 | 10,1 | presentación Quarto 2023 (`home.qmd` + `home.html` + libs) |
| `Submissions/AppliedEnergy_V2` | 26 | 5,8 | envío a Applied Energy |
| `Submissions/Energy_8000` | 34 | 5,5 | **artículo publicado en *Energy*** (línea base) |
| `Submissions/draft_paper` | 25 | 5,2 | borrador previo |
| `docs/DocumentoMemoria` | 45 | 4,9 | memoria de Vicente Muñoz (2022) |
| `docs/MemoriaMHurtado` | 26 | 2,6 | memoria de Juan Matías Hurtado (2025) |
| `docs/Presentations/June2020.pdf` | 1 | 1,9 | PDF suelto sin fuente |
| `docs/Informe` | 10 | 1,8 | informe + `defensa.rmd`, sin relación declarada con el resto |
| `Submissions/EnergyPolicy` | 21 | 1,7 | artículo en desarrollo |
| `docs/Presentations/UVigo` | 28 | 1,1 | presentación xaringan 2022 (incluye 18 archivos de `libs/` y `home_files/`) |
| `Apuntes` + `docs/Apuntes` | 26 | 1,6 | **el mismo árbol, duplicado íntegro** |
| `code` | 12 | 1,2 | GAMS, Julia, notebooks |
| `docs/Presentations/presentation-template` | 8 | 0,3 | presentación de Hurtado (la plantilla fue borrada) |
| `docs/Memoria` | 5 | 0,04 | **plantilla muerta**: 4 archivos de `core/` y un anexo, sin documento maestro |
| `docs/Presentations/PhDEIIPUCV` | 2 | 0,01 | presentación PUCV |

## 3. Estructura propuesta

Tres reglas, y todo lo demás se deduce:

1. **Cada documento es autocontenido**: su carpeta tiene sus figuras, su bibliografía y su preámbulo, y compila desde su propio directorio.
2. **Nada en la raíz** salvo `README.md`, `.gitignore` y `LICENSE`.
3. **Un preámbulo compartido** para las memorias, en vez de tres copias divergentes.

```
EnergySegmentation/
├── README.md                      ← mapa del repo: qué es cada carpeta y cómo compilar
├── .gitignore
├── shared/
│   ├── preambulo-memoria.tex      ← preámbulo único de memorias (hoy: 3 copias)
│   ├── newapa.sty  setspace.sty  julialogo.sty
│   └── logos/                     ← hoy duplicados en DocumentoMemoria y MemoriaMHurtado
├── memorias/
│   ├── munoz-2022/                ← hoy docs/DocumentoMemoria
│   │   ├── memoria.tex  chapters/  attachments/  figures/  references.bib
│   └── hurtado-2025/              ← hoy docs/MemoriaMHurtado
│       ├── memoria.tex  chapters/  attachments/  figures/  references.bib
├── presentaciones/
│   ├── uvigo-2022/                ← hoy docs/Presentations/UVigo
│   ├── ifors-2023/                ← hoy docs/Presentations/IFORS
│   ├── pucv-phd/                  ← hoy docs/Presentations/PhDEIIPUCV
│   └── hurtado-defensa-2026/      ← hoy docs/Presentations/presentation-template
│       └── figures/               ← las 29 capturas que hoy están en la raíz
├── submissions/
│   ├── energy-2021-published/     ← hoy Energy_8000. Línea base, congelada
│   ├── applied-energy-v2/
│   ├── draft-paper/
│   └── energy-policy/             ← artículo en desarrollo
├── apuntes/                       ← hoy Apuntes/ y docs/Apuntes/ (elegir una)
├── code/
└── auditoria/                     ← los informes de auditoría y el changelog
```

## 4. Plan por etapas

Cada etapa es un PR independiente y verificable. **No avanzar a la siguiente sin que los documentos afectados compilen.**

### Etapa 0 — Congelar la línea base y detener el sangrado *(sin riesgo)*

1. Añadir `.gitignore` (ya propuesto en el PR de auditoría de la memoria de Muñoz) y sacar del índice los **11 artefactos versionados** con `git rm --cached`:
   `docs/DocumentoMemoria/memoria.{log,aux,bbl,blg,toc,lof,lot}`, `memoria.tex.bak`, `core/preambulo.tex.bak`, `core/primeras_paginas.tex.bak`, `docs/Presentations/UVigo/tikz1779c212df233.log`, `code/cnt_2050_total_cap900_scenarios.gdx`.
2. Escribir el `README.md` con el mapa de carpetas y, para cada documento, **desde dónde se compila y con qué motor** (`xelatex -shell-escape` para la memoria de Hurtado, `lualatex` para su presentación, `pdflatex` para el artículo, `xelatex` para la memoria de Muñoz). Es la información que hoy no existe en ninguna parte y la causa de que cada uno haya inventado su convención.
3. Marcar `submissions/energy-2021-published/` como congelada en el README: es la línea base del [changelog](CHANGELOG_modelo.md) y no debe editarse.

### Etapa 1 — Vaciar la raíz *(el 51% del repositorio)*

Usar [`inventario_raiz.csv`](inventario_raiz.csv), que clasifica las 96 imágenes en usadas y huérfanas:

1. **38 imágenes usadas (28,4 MB)** → mover a la carpeta del documento que las usa: 29 a `presentaciones/hurtado-defensa-2026/figures/`, y las de `chapter02.tex` y `chapter04.tex` a `memorias/hurtado-2025/figures/`. Actualizar los `\includegraphics` correspondientes (son rutas planas, el reemplazo es directo).
2. **58 imágenes huérfanas (16,9 MB)** → **no borrar a ciegas**. Preguntar a los autores: hay grupos que son claramente iteraciones de una misma captura (`cccc.png`/`CCCC.png`; `embudo.png`/`A.embudo.png`/`bmbudo.png`/`mbudoo.png`; `melect.png`/`melect1..3.png`; `MODELOILUS1.png`/`MODELOILUS2.png`; `calibracion.png`/`calibracion2.png`), donde en general sólo una está referenciada. Lo demás son figuras de trabajo de exploraciones anteriores (`gabaixsubastador.png`, `funcsubastadorJ(m).png`, `thetasypia.png`, …). Propuesta: mover todo a `archivo/figuras-sueltas/` en un PR, y borrar en un segundo PR una vez que los autores confirmen.
3. **Sustituir las capturas por LaTeX donde sea barato.** Las ocho más pesadas de la presentación de Hurtado (`simbologia.png` 2,03 MB, `objetivo.png`, `limitciones.png`, `parametros2.png`, `codificacion.png`, `calibracion2.png`, `MODELOILUS1.png`, `cccc.png`) son tablas y ecuaciones **que ya existen como LaTeX en la memoria**. Reescribirlas nativas en beamer ahorra ~12 MB, hace la presentación editable y elimina la dependencia de la raíz. Es la única tarea de esta etapa que requiere trabajo real de edición.

### Etapa 2 — Deduplicar *(15,5 MB, 99 archivos)*

Los cuatro focos, en orden de tamaño:

| Grupo | Archivos redundantes | Acción |
|---|---|---|
| `Figures/` triplicado en `AppliedEnergy_V2`, `Energy_8000/R1` y `draft_paper` | 42 | Los tres son envíos históricos y deben quedar autocontenidos para reproducibilidad. **No deduplicar**: documentar en el README que la repetición es deliberada. |
| `Apuntes/` y `docs/Apuntes/` idénticos archivo por archivo | 13 | **Eliminar uno.** Conservar `apuntes/` en la raíz de la nueva estructura. |
| `docs/DocumentoMemoria/images/` replica `core/images/` | 4 | Sólo se referencia `core/images/`. **Eliminar `images/`.** |
| `core/` de `DocumentoMemoria`, `Memoria` y `MemoriaMHurtado` | 4 + logos | **Unificar en `shared/`.** Es la etapa 3. |
| `docs/Presentations/UVigo/libs/` y `home_files/`, `IFORS/home_files/` | 88 archivos, 6,2 MB | **Corregido tras verificar: NO deben sacarse del índice.** `UVigo/home.html` e `IFORS/home.html` están versionados y no funcionan sin ellos — son el registro de charlas ya expuestas, no artefactos regenerables sin el entorno de R/Quarto original. Si se quiere un formato de archivo más liviano, exportar cada charla a PDF y retirar HTML y `libs/` juntos. |

### Etapa 3 — Preámbulo compartido y limpieza de plantillas

1. **`docs/Memoria/` es una plantilla muerta** (5 archivos, sin maestro): eliminar.
2. **Unificar los tres preámbulos** en `shared/preambulo-memoria.tex`. Los tres arrastran los mismos defectos —`shadows.blur`, `Times New Roman`, `gensymb`— porque son copias. Un preámbulo único con las correcciones ya verificadas evita que el próximo memorista herede los mismos cuatro bloqueadores. Diferencia a preservar: la memoria de Hurtado **usa** `minted` (tres bloques de código Julia) y la de Muñoz no, así que el preámbulo compartido debe cargarlo condicionalmente o dejar `minted` en el documento que lo necesita.
3. **`docs/Presentations/presentation-template/`**: renombrar a `presentaciones/hurtado-defensa-2026/`. Si se quiere conservar una plantilla de presentación, recuperar `presentation.tex` de `29cb916` y ponerla en `shared/plantilla-presentacion/`.
4. **`docs/Informe/`** (10 archivos, 1,8 MB, con `informe.tex` y `defensa.rmd`): no tiene relación declarada con el resto del proyecto. Preguntar a los autores si corresponde a un trabajo anterior; si sí, `archivo/informe-<año>/`.
5. **`docs/Presentations/June2020.pdf`** (1,9 MB): PDF suelto sin fuente. Mover a `archivo/` o eliminar.
6. **`referencesOLD.bib`** en `MemoriaMHurtado` y `docs/DocumentoMemoria`: sin uso, eliminar.

### Etapa 4 — Rutas y compilación reproducible

Ésta es la etapa que resuelve la causa raíz. Para cada documento:

1. Rutas de figuras **relativas a su propia carpeta** (`figures/...`), sin `\graphicspath` de rescate.
2. `\input` y `\bibliography` **relativos al documento**. Hoy `memoria.Rtex` de Hurtado mezcla tres convenciones en el mismo archivo (ver [`AUDITORIA_2_MHurtado.md`](AUDITORIA_2_MHurtado.md) §2).
3. Renombrar `memoria.Rtex` → `memoria.tex`: el único fragmento de knitr está en `anexo_b`, que está comentado en el maestro, así que no se ejecuta código R.
4. Añadir a cada carpeta un `Makefile` o `latexmkrc` de tres líneas con el motor y las banderas correctas. Es lo que evita que la próxima persona tenga que descubrir que hace falta `-shell-escape`.
5. **Criterio de aceptación por documento**: compila desde su propia carpeta, 0 errores, 0 figuras faltantes, 0 citas ni referencias indefinidas. Los cuatro documentos vivos ya alcanzan ese criterio con las correcciones verificadas en las auditorías (artículo 15 páginas, memoria de Muñoz 113, memoria de Hurtado 57, presentación de Hurtado 47).

### Etapa 5 — Bibliografías

`docs/DocumentoMemoria/references.bib` tiene **2.038 entradas para 17 citas**: es un volcado completo de Zotero. En contraste, `MemoriaMHurtado/references.bib` tiene 25 entradas para 20 citas. Depurar la primera con `bibtool -x memoria.aux` o `bibexport`, y adoptar la convención de Hurtado —bibliografía por documento, sólo lo citado— como estándar del repositorio.

## 5. Resultado esperado

| | Antes | Después |
|---|---|---|
| Peso del árbol | 92,9 MB | **38,0 MB** |
| Archivos en la raíz | 97 | 3 |
| Imágenes huérfanas | 58 (16,9 MB) | 0 |
| Duplicados redundantes | 99 (15,5 MB) | 42 (los `Figures/` de submissions, deliberados) |
| Artefactos versionados | 11 + 18 de xaringan | 0 |
| Copias del preámbulo de memoria | 3 divergentes | 1 |
| Documentos que compilan desde su carpeta | 0 de 4 | 4 de 4 |

Desglose del ahorro, sobre los 92,9 MB de `master`:

| Concepto | MB | Estado |
|---|---|---|
| PDF de la presentación fuera del índice | −22,4 | hecho (etapa 1) |
| 58 imágenes huérfanas de la raíz | −16,9 | archivadas en `archivo/`; **la baja de peso requiere que los autores confirmen el borrado** |
| las 8 capturas pesadas de la presentación reescritas como LaTeX | −9,9 | pendiente (etapa 1, punto 3) |
| duplicados, excluidos los `Figures/` de submissions | −5,3 | pendiente (etapa 2) |
| 10 artefactos de compilación | −0,4 | hecho (etapa 0) |
| **total** | **−54,9 → 38,0 MB** | |

Los 10,2 MB de los tres `Figures/` triplicados **se conservan** deliberadamente, porque cada envío histórico debe quedar autocontenido. La etapa 1 por sí sola es **neutra en peso del árbol de trabajo**: mueve y archiva, no borra. El árbol queda en 93,0 MB hasta que los autores decidan sobre las 58 huérfanas.

## 6. Riesgos y qué no hacer

- **No reescribir el historial.** Un `git filter-repo` para purgar las imágenes del historial bajaría el `.git`, pero rompe todos los clones existentes y las referencias a commits de las memorias ya defendidas. El repositorio es público y pequeño; no vale la pena.
- **No borrar las 58 huérfanas sin confirmación.** Algunas pueden ser figuras de resultados cuyo código generador ya no existe.
- **No tocar `submissions/energy-2021-published/`.** Es la línea base del changelog y corresponde a un artículo publicado.
- **Mover con `git mv`**, no copiar y borrar, para preservar el seguimiento de historial de cada archivo.
- **Un PR por etapa.** Un PR que mueva 200 archivos y edite rutas al mismo tiempo es imposible de revisar y de revertir.
