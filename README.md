# Energy Markets and Segmentation

Continuación de [Amigo, Cea-Echenique y Feijoo (2021)](https://doi.org/10.1016/j.energy.2021.120129), *Energy* 226:120129 — modelos de inversión en capacidad de generación eléctrica con *cap-and-trade* en dos etapas, y sus extensiones con planificador de racionalidad limitada.

## Mapa del repositorio

| Carpeta | Qué es |
|---|---|
| `Submissions/Energy_8000/` | **Artículo publicado en *Energy* (2021). Línea base — congelada, no editar.** `R1/Clean_R1.Rtex` es la versión aceptada. |
| `Submissions/EnergyPolicy/` | Artículo en desarrollo: *Inattention raises energy prices*. |
| `Submissions/AppliedEnergy_V2/`, `Submissions/draft_paper/` | Envíos y borradores anteriores. Cada uno autocontenido. |
| `docs/DocumentoMemoria/` | Memoria de **Vicente Muñoz L'Huillier** (2022) — costo de precisión del subastador. |
| `docs/MemoriaMHurtado/` | Memoria de **Juan Matías Hurtado** (2025) — anclaje y ajuste del subastador. |
| `docs/Presentations/` | Presentaciones: `UVigo/` (2022), `IFORS/` (2023), `PhDEIIPUCV/`, `HurtadoDefensa2026/` (defensa de Hurtado, 15 de mayo de 2026). Las de UVigo e IFORS conservan su HTML renderizado y los `libs/`/`home_files/` que ese HTML necesita. |
| `docs/auditoria/` | Auditorías, changelog del modelo y planes de trabajo. **Empezar por aquí.** |
| `docs/Apuntes/` | Apuntes sobre *cap-and-trade*: `cnt.tex`, `cnt_v2.tex` y `cnt_v3.tex`, tres versiones sucesivas. |
| `docs/Informe/` | Material inicial de la investigadora postdoctoral coautora del artículo de *Energy*, de cuando se incorporó al proyecto: `informe.tex` más `defensa.rmd`. Compila con `pdflatex`. |
| `shared/` | Lo que más de un documento usa: `datos-modelo.tex` (nomenclatura, ecuaciones y valores de parámetros, leído por la memoria de Hurtado y su presentación) y `memoria/preambulo-base.tex` (preámbulo común de las dos memorias). |
| `code/` | Modelos en GAMS y Julia, y notebooks. |

### Documentos de la auditoría

- [`docs/auditoria/AUDITORIA_memoria_VMunoz.md`](docs/auditoria/AUDITORIA_memoria_VMunoz.md) — memoria de Muñoz y borrador del artículo.
- [`docs/auditoria/AUDITORIA_2_MHurtado.md`](docs/auditoria/AUDITORIA_2_MHurtado.md) — memoria y presentación de Hurtado, y estado del repositorio.
- [`docs/auditoria/CHANGELOG_modelo.md`](docs/auditoria/CHANGELOG_modelo.md) — cómo evolucionó el modelo desde el artículo publicado.
- [`docs/auditoria/PLAN_ARTICULO.md`](docs/auditoria/PLAN_ARTICULO.md) — plan del próximo artículo.
- [`docs/auditoria/PLAN_ORDEN_REPOSITORIO.md`](docs/auditoria/PLAN_ORDEN_REPOSITORIO.md) — plan de orden y limpieza, por etapas.

## Cómo compilar

**En las seis carpetas con un `latexmkrc`, basta `latexmk` desde la carpeta del documento**: el motor y las banderas ya están ahí. La tabla siguiente dice cuáles son, para quien compile a mano o quiera saber qué hace `latexmk`. Cada combinación está verificada.

| Documento | Motor | Compilar desde | Notas |
|---|---|---|---|
| `Submissions/EnergyPolicy/inattention_energy_prices.tex` | `pdflatex` | su propia carpeta | clase Elsevier `cas-dc`, incluida en la carpeta. 15 páginas. |
| `docs/DocumentoMemoria/memoria.tex` | `xelatex` | su propia carpeta | lee `shared/memoria/preambulo-base.tex`. 113 páginas. |
| `docs/MemoriaMHurtado/memoria.tex` | `xelatex -shell-escape` + `bibtex` | su propia carpeta | **requiere Pygments** (`pip install Pygments`): `chapter03.tex` usa `minted`. Lee `shared/memoria/preambulo-base.tex` y `shared/datos-modelo.tex`. 57 páginas. |
| `docs/Presentations/HurtadoDefensa2026/JMHL_presentation.tex` | `lualatex` + `bibtex` | su propia carpeta | figuras en `figures/`, fuentes DM Sans en `font/`, bibliografía en su `references.bib`. 48 páginas. |
| `docs/Apuntes/cnt.tex`, `cnt_v2.tex`, `cnt_v3.tex` | `pdflatex` | su propia carpeta | 7, 11 y 15 páginas. `cnt_v3` necesita `tablefootnote`; `cnt` toma una figura de `../Informe/`. |
| `docs/Presentations/UVigo/home.Rmd` | R + `xaringan` | su propia carpeta | `rmarkdown::render("home.Rmd")`. El HTML renderizado y su `libs/` están versionados. |
| `docs/Presentations/IFORS/home.qmd` | `quarto render` | su propia carpeta | el HTML renderizado y su `home_files/` están versionados. |
| `Submissions/Energy_8000/R1/Clean_R1.Rtex` | R + `knitr` → `pdflatex` | su propia carpeta | `knitr::knit()` y luego `pdflatex` + `bibtex`. |
| `docs/Presentations/PhDEIIPUCV/main.tex` | `pdflatex` | su propia carpeta | beamer. 4 páginas. |

Las carpetas con `latexmkrc` son las de las dos memorias, la presentación de Hurtado, la de PhDEIIPUCV, el artículo en desarrollo y los apuntes. `Submissions/Energy_8000/` **no lleva uno a propósito**: es la línea base congelada y su cadena pasa por `knitr`.

Compilando a mano, los documentos con bibliografía necesitan el ciclo completo:

```bash
<motor> documento && bibtex documento && <motor> documento && <motor> documento
```

**Criterio de aceptación de un documento**: compila con 0 errores, 0 figuras faltantes y 0 citas ni referencias indefinidas.

### Paquetes LaTeX

Además de una instalación estándar: `physics`, `yhmath`, `extarrows`, `cancel`, `mathdots`, `gensymb`, `pgfplots`, `siunitx`, `eurosym`, `bbm`, `babel-spanish`, `makecell`, `luatexbase`, `xurl`, `todonotes`, `truncate`, `tablefootnote` (apuntes), `minted` (con `fvextra`, `catchfile`, `xstring`, `framed`, `upquote`), y para la presentación de Hurtado `academicons`, `fontawesome5`, `tcolorbox`, `appendixnumberbeamer`, `lualatex-math`.

## Convenciones

- **Los artefactos de compilación no se versionan** (ver `.gitignore`). Sí se versionan los PDF finales de memorias y artículos, y el HTML renderizado de las presentaciones ya expuestas.
- **`Submissions/Energy_8000/` está congelada**: es la línea base del changelog y corresponde a un artículo publicado. Los `Figures/` repetidos entre carpetas de `Submissions/` son deliberados, para que cada envío histórico quede autocontenido.
- **`code/cnt_2050_total_cap900_scenarios.gdx`** se conserva a propósito: es la salida del solver para el escenario CAP=900 y no es reproducible sin licencia de GAMS.
- **Sin duplicados, salvo los deliberados.** Los `Figures/` repetidos entre las carpetas de `Submissions/` **son a propósito**: cada envío histórico debe quedar autocontenido para poder reproducirlo. Cualquier otra copia idéntica de un archivo es un error; ver la etapa 2 del plan de orden.
- **Un preámbulo, no tres.** Las dos memorias comparten `shared/memoria/preambulo-base.tex`; cada `core/preambulo.tex` sólo añade lo suyo (el `\graphicspath`, y en el caso de Hurtado `minted` y cuatro paquetes más). Existían tres copias divergentes del mismo preámbulo y las tres arrastraban los mismos cuatro bloqueadores de compilación. Los `.sty` de terceros y las carpetas `fonts/` y `logos/` **siguen duplicados a propósito**: `kpathsea` no busca en `shared/`, y hacer que lo haga exigiría fijar `TEXINPUTS`, lo que rompe el criterio de compilar desde la propia carpeta con `xelatex` a secas.
- **Una bibliografía por documento, con lo citado y nada más.** `docs/DocumentoMemoria/references.bib` era un volcado completo de Zotero —2.038 entradas para 17 citas, 2,0 MB— y quedó en las 17. La biblioteca completa vive en Zotero, no en el repositorio; para añadir una cita, exporte esa entrada y péguela. La excepción declarada es `Submissions/EnergyPolicy/references.bib`: 339 entradas para 16 citas, que se conserva mientras el artículo esté en desarrollo porque hace de biblioteca de trabajo.
- **Un dato, un lugar.** Los valores de parámetros, las ecuaciones del planificador y las descripciones de los símbolos viven en `shared/datos-modelo.tex`, que la memoria y la presentación leen con `\input`. Antes estaban escritos por separado en cada documento, y de ahí venían las discrepancias entre ambos. Al agregar un valor, agréguelo ahí.
- **Rutas relativas al documento, sin `\graphicspath` de rescate.** Ningún documento depende ya de compilarse desde una carpeta concreta del repositorio: todas las rutas de figuras, `\input` y `\bibliography` son relativas a la carpeta del propio documento. Las únicas excepciones son deliberadas y explícitas: `shared/` se alcanza con `../../`, y `docs/Apuntes/cnt.tex` toma una figura de `../Informe/`.
- **Cada documento es autocontenido**: sus figuras viven en su propia carpeta y sus rutas son relativas a ella. El patrón heredado de Overleaf —todo relativo a la raíz del repositorio— se está retirando; ver el plan de orden. La memoria de Muñoz es la que aún lo usa.
