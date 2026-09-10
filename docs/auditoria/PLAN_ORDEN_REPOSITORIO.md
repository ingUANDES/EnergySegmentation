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
| `(raíz)` | 98 | 45,3 | 96 imágenes + README + `.gitignore`. 37 las componen la memoria y la presentación de Hurtado; **59 (17,0 MB) no se componen en ningún documento** |
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
| `code` | 13 | 1,2 | GAMS, Julia, notebooks |
| `docs/Presentations/HurtadoDefensa2026` | 8 | 0,3 | presentación de Hurtado (la plantilla fue borrada) |
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
│   └── hurtado-defensa-2026/      ← hoy docs/Presentations/HurtadoDefensa2026
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

1. Añadir `.gitignore` (ya propuesto en el PR de auditoría de la memoria de Muñoz) y sacar del índice los **10 artefactos de compilación versionados** con `git rm --cached`:
   `docs/DocumentoMemoria/memoria.{bbl,blg,log,lof,lot,toc}`, `memoria.tex.bak`, `core/preambulo.tex.bak`, `core/primeras_paginas.tex.bak` y `docs/Presentations/UVigo/tikz1779c212df233.log`. (`memoria.aux` no está versionado; `code/cnt_2050_total_cap900_scenarios.gdx` sí, y se conserva a propósito: es la salida del solver para CAP=900 y no se reproduce sin licencia de GAMS.)
2. Escribir el `README.md` con el mapa de carpetas y, para cada documento, **desde dónde se compila y con qué motor** (`xelatex -shell-escape` para la memoria de Hurtado, `lualatex` para su presentación, `pdflatex` para el artículo, `xelatex` para la memoria de Muñoz). Es la información que hoy no existe en ninguna parte y la causa de que cada uno haya inventado su convención.
3. Marcar `submissions/energy-2021-published/` como congelada en el README: es la línea base del [changelog](CHANGELOG_modelo.md) y no debe editarse.

### Etapa 1 — Vaciar la raíz *(el 51% del repositorio)*

Usar [`inventario_raiz.csv`](inventario_raiz.csv), que clasifica las 96 imágenes en usadas y huérfanas:

1. **37 imágenes usadas (28,3 MB)** → mover a la carpeta del documento que las usa: 29 a `presentaciones/hurtado-defensa-2026/figures/`, y las de `chapter02.tex` y `chapter04.tex` a `memorias/hurtado-2025/figures/`. Actualizar los `\includegraphics` correspondientes (son rutas planas, el reemplazo es directo).
2. **59 imágenes sin uso (17,0 MB)** → **no borrar a ciegas**. Preguntar a los autores: hay grupos que son claramente iteraciones de una misma captura (`cccc.png`/`CCCC.png`; `embudo.png`/`A.embudo.png`/`bmbudo.png`/`mbudoo.png`; `melect.png`/`melect1..3.png`; `MODELOILUS1.png`/`MODELOILUS2.png`; `calibracion.png`/`calibracion2.png`), donde en general sólo una está referenciada. Lo demás son figuras de trabajo de exploraciones anteriores (`gabaixsubastador.png`, `funcsubastadorJ(m).png`, `thetasypia.png`, …). Propuesta: mover todo a `archivo/figuras-sueltas/` en un PR, y borrar en un segundo PR una vez que los autores confirmen.
3. **Sustituir las capturas por LaTeX donde sea barato.** Las ocho más pesadas de la presentación de Hurtado (`simbologia.png` 1,93 MB, `objetivo.png`, `limitciones.png`, `parametros2.png`, `codificacion.png`, `calibracion2.png`, `MODELOILUS1.png`, `cccc.png`) son tablas y ecuaciones **que ya existen como LaTeX en la memoria**. Reescribirlas nativas en beamer ahorra ~12 MB, hace la presentación editable y elimina la dependencia de la raíz. Es la única tarea de esta etapa que requiere trabajo real de edición.

### Etapa 2 — Deduplicar *(hecho: 31 archivos, 2,79 MB)*

El titular original de esta etapa —15,5 MB en 99 archivos— **sobrestimaba lo deduplicable**,
porque 10,2 MB corresponden a los `Figures/` triplicados de los envíos, que deben quedar
repetidos a propósito, y 6,2 MB a los `libs/` de las charlas ya expuestas, que tampoco se
tocan. Lo que quedaba y se eliminó:

| Grupo eliminado | Archivos | MB | Por qué es seguro |
|---|---|---|---|
| `Apuntes/` en la raíz | 14 | 0,95 | Copia obsoleta de `docs/Apuntes/`: 13 archivos idénticos byte a byte más `Figures/contaminación.png`, que ninguna fuente referencia. La copia viva es la de `docs/`, porque `cnt.tex` incluye una figura de `Informe/`, carpeta que sólo existe como hermana dentro de `docs/`. |
| `docs/Presentations/UVigo/home_files/` | 12 | 0,40 | **Sobrante de render, no soporte de la charla.** `home.html` referencia únicamente `libs/`; ni el HTML ni el `.Rmd` mencionan `home_files`, que además contiene la figura de ejemplo `pressure-1.png` de la plantilla de rmarkdown. El caso de IFORS es el opuesto: su `home.html` referencia `home_files/` 23 veces, y por eso se conserva. |
| `docs/Presentations/IFORS/images/Captura de pantalla 2023-07-12…png` | 1 | 1,09 | Idéntica a `frontSlide.png`, que es la que la charla usa; ninguna fuente nombra la captura. |
| `docs/DocumentoMemoria/images/` | 4 | 0,35 | Réplica de `core/images/`, que es la ruta que usan los capítulos. Dos de los cuatro archivos (`cqgl_1.png`, `crystal.pdf`) no se referencian en ninguna copia. |

Verificado tras eliminar: la memoria de Muñoz sigue en 113 páginas con 0 errores y 0
figuras faltantes, y los tres apuntes compilan desde su propia carpeta (`cnt` 7 páginas,
`cnt_v2` 11, `cnt_v3` 15; ninguno con errores ni figuras faltantes).

Los focos que **no** se deduplican, y la razón:

| Grupo | Archivos redundantes | Acción |
|---|---|---|
| `Figures/` triplicado en `AppliedEnergy_V2`, `Energy_8000/R1` y `draft_paper` | 42 | Los tres son envíos históricos y deben quedar autocontenidos para reproducibilidad. **No deduplicar**: documentar en el README que la repetición es deliberada. |
| `Apuntes/` y `docs/Apuntes/` idénticos archivo por archivo | 13 | **Eliminar uno.** Conservar `apuntes/` en la raíz de la nueva estructura. |
| `docs/DocumentoMemoria/images/` replica `core/images/` | 4 | Sólo se referencia `core/images/`. **Eliminar `images/`.** |
| `core/` de `DocumentoMemoria`, `Memoria` y `MemoriaMHurtado` | 4 + logos | **Unificar en `shared/`.** Es la etapa 3. |
| `docs/Presentations/UVigo/libs/` y `home_files/`, `IFORS/home_files/` | 88 archivos, 6,2 MB | **Corregido tras verificar: NO deben sacarse del índice.** `UVigo/home.html` e `IFORS/home.html` están versionados y no funcionan sin ellos — son el registro de charlas ya expuestas, no artefactos regenerables sin el entorno de R/Quarto original. Si se quiere un formato de archivo más liviano, exportar cada charla a PDF y retirar HTML y `libs/` juntos. |

### Etapa 3 — Preámbulo compartido y limpieza de plantillas *(hecha)*

| Punto | Estado |
|---|---|
| `docs/Memoria/` (plantilla muerta, 5 archivos) | **eliminada** por instrucción de los autores |
| Unificar los tres preámbulos | **hecho**: `shared/memoria/preambulo-base.tex`. Cada `core/preambulo.tex` queda en 8 y 20 líneas y sólo añade lo propio: el `\graphicspath` y, en Hurtado, `minted` más `subcaption`, `makecell`, `url` y `xurl`. `minted` **no** está en la base: sólo Hurtado lo usa y obliga a `-shell-escape` con Pygments. |
| `presentation-template/` → nombre real | **hecho**: `docs/Presentations/HurtadoDefensa2026/`, siguiendo la convención de las otras carpetas de `Presentations/`. No era una plantilla: es la defensa del 15 de mayo de 2026. |
| `docs/Informe/` | **se conserva**: es el material inicial de la investigadora postdoctoral coautora del artículo de *Energy*. Descrito así en el README. |
| `docs/Presentations/June2020.pdf` | **se conserva** por instrucción de los autores. |
| `referencesOLD.bib` | **eliminado** (sólo existía en `MemoriaMHurtado`; `DocumentoMemoria` no tenía uno). |

Dos hallazgos al unificar:

- **`changes` se cargaba sin usarse.** El preámbulo de Hurtado lo pedía, pero no hay ni un `\added`, `\deleted` ni `\replaced` en los capítulos. Sale del preámbulo y de la lista de paquetes del README. Lo mismo con `subfigure` en el de Muñoz: ninguna de las dos memorias usa comandos de subfiguras.
- **Los `.sty` de terceros, `fonts/` y `logos/` siguen duplicados a propósito.** Son 0,97 MB que sí se podrían unificar, pero `kpathsea` no busca en `shared/`: hacer que los encuentre exige fijar `TEXINPUTS`, y eso rompe el criterio de aceptación de compilar desde la propia carpeta con `xelatex` a secas. Las fuentes `TamilMN*.otf` no son peso muerto: `core/julialogo.sty` las declara con `Path=fonts/`.

Verificado tras unificar, cada documento desde su propia carpeta y con el ciclo completo
de bibliografía: memoria de Muñoz **113 páginas**, memoria de Hurtado **57**, presentación
**48**; las tres con 0 errores, 0 figuras faltantes y 0 citas ni referencias indefinidas.
Mismos conteos que antes de tocar los preámbulos.

### Etapa 4 — Rutas y compilación reproducible *(hecha)*

| Punto | Estado |
|---|---|
| Rutas de figuras relativas al documento, sin `\graphicspath` de rescate | **hecho**: 10 `\includegraphics` de la memoria de Muñoz pasan de `docs/DocumentoMemoria/core/images/…` a `core/images/…`, y el `\graphicspath` sale de los dos preámbulos. Ninguno de los dos documentos depende ya de compilarse desde una carpeta concreta. |
| `\input` y `\bibliography` relativos al documento | **ya lo estaban**. El plan decía que `memoria.Rtex` de Hurtado mezclaba tres convenciones; al verificarlo sobre el estado actual, sus diez `\input` y su `\bibliography` son todos relativos al documento. La mezcla que quedaba estaba en las rutas de figuras, y era la de Muñoz. |
| Renombrar `memoria.Rtex` → `memoria.tex` | **hecho**. Comprobado antes: no hay ni un fragmento de knitr vivo (`<<>>=` o ```` ```{r} ````) en el maestro ni en los capítulos; el único está en `attachments/anexo_b.Rtex`, que el maestro tiene comentado. |
| `latexmkrc` por carpeta | **hecho** en las seis carpetas de documentos LaTeX vivos. `Submissions/Energy_8000/` no lleva uno a propósito: es la línea base congelada y su cadena pasa por `knitr`. |

Con esto, **`latexmk` a secas desde la carpeta del documento basta**: ya no hay que
descubrir que la memoria de Hurtado necesita `-shell-escape`, ni que la presentación
necesita `lualatex`.

Un hallazgo al verificar en una instalación limpia de TeX Live: la presentación necesita
también `luatexbase`, que no estaba en la lista de paquetes del README. Se agrega.

**Criterio de aceptación, comprobado documento por documento con `latexmk` desde su
propia carpeta** — 0 errores, 0 figuras faltantes y 0 citas ni referencias indefinidas en
los ocho:

| Documento | Páginas |
|---|---|
| `docs/DocumentoMemoria/memoria.tex` | 113 |
| `docs/MemoriaMHurtado/memoria.tex` | 57 |
| `docs/Presentations/HurtadoDefensa2026/JMHL_presentation.tex` | 48 |
| `Submissions/EnergyPolicy/inattention_energy_prices.tex` | 15 |
| `docs/Apuntes/cnt.tex` · `cnt_v2.tex` · `cnt_v3.tex` | 7 · 11 · 15 |
| `docs/Presentations/PhDEIIPUCV/main.tex` | 4 |

### Etapa 5 — Bibliografías

`docs/DocumentoMemoria/references.bib` tiene **2.038 entradas para 17 citas**: es un volcado completo de Zotero. En contraste, `MemoriaMHurtado/references.bib` tiene 25 entradas para 20 citas. Depurar la primera con `bibtool -x memoria.aux` o `bibexport`, y adoptar la convención de Hurtado —bibliografía por documento, sólo lo citado— como estándar del repositorio.

## 5. Resultado esperado

| | Antes | Después |
|---|---|---|
| Peso del árbol | 92,9 MB | **40,5 MB** |
| Archivos en la raíz | 97 | 3 |
| Imágenes sin uso en la raíz | 59 (17,0 MB) | 0 |
| Duplicados redundantes | 99 (15,5 MB) | 42 (los `Figures/` de submissions, deliberados) |
| Artefactos de compilación versionados | 10 | 0 |
| Copias del preámbulo de memoria | 3 divergentes | 1 |
| Documentos que compilan desde su carpeta | 0 de 4 | 4 de 4 |

Desglose del ahorro, sobre los 92,9 MB de `master`:

| Concepto | MB | Estado |
|---|---|---|
| PDF de la presentación fuera del índice | −22,4 | hecho (etapa 1) |
| 59 imágenes sin uso de la raíz | −17,0 | **hecho**: eliminadas por instrucción de los autores; el inventario queda como registro |
| las 8 capturas pesadas de la presentación reescritas como LaTeX | −9,9 | **hecho**: tcolorbox y tikz nativos, con el contenido compartido de la memoria en `shared/datos-modelo.tex` |
| duplicados, excluidos los `Figures/` de los envíos | −2,8 | **hecho** (etapa 2); el −5,3 previo sobrestimaba lo deduplicable |
| 10 artefactos de compilación | −0,4 | hecho (etapa 0) |
| **total** | **−52,4 → 40,5 MB** | ejecutado; lo que reste depende de las etapas 3 a 5 |

Los 10,2 MB de los tres `Figures/` triplicados **se conservan** deliberadamente, porque cada envío histórico debe quedar autocontenido.

## 6. Riesgos y qué no hacer

- **No reescribir el historial.** Un `git filter-repo` para purgar las imágenes del historial bajaría el `.git`, pero rompe todos los clones existentes y las referencias a commits de las memorias ya defendidas. El repositorio es público y pequeño; no vale la pena.
- **No borrar las 59 archivadas sin confirmación.** Algunas pueden ser figuras de resultados cuyo código generador ya no existe.
- **No tocar `submissions/energy-2021-published/`.** Es la línea base del changelog y corresponde a un artículo publicado.
- **Mover con `git mv`**, no copiar y borrar, para preservar el seguimiento de historial de cada archivo.
- **Un PR por etapa.** Un PR que mueva 200 archivos y edite rutas al mismo tiempo es imposible de revisar y de revertir.
