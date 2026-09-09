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
| `docs/Presentations/` | Presentaciones: `UVigo/` (2022), `IFORS/` (2023), `PhDEIIPUCV/`, `presentation-template/` (defensa de Hurtado). |
| `docs/auditoria/` | Auditorías, changelog del modelo y planes de trabajo. **Empezar por aquí.** |
| `docs/Apuntes/`, `Apuntes/` | Apuntes sobre *cap-and-trade*. Los dos árboles son idénticos; ver plan de orden. |
| `archivo/` | Material sin uso, a la espera de decisión de los autores. Ver `archivo/README.md`. |
| `docs/Informe/` | Documento propio (`informe.tex`, más `defensa.rmd`) cuya relación con el resto del proyecto no está declarada. Compila con `pdflatex`. |
| `docs/Memoria/` | Plantilla muerta: cuatro archivos de `core/` y un anexo, sin documento maestro. |
| `code/` | Modelos en GAMS y Julia, y notebooks. |

### Documentos de la auditoría

- [`docs/auditoria/AUDITORIA_memoria_VMunoz.md`](docs/auditoria/AUDITORIA_memoria_VMunoz.md) — memoria de Muñoz y borrador del artículo.
- [`docs/auditoria/AUDITORIA_2_MHurtado.md`](docs/auditoria/AUDITORIA_2_MHurtado.md) — memoria y presentación de Hurtado, y estado del repositorio.
- [`docs/auditoria/CHANGELOG_modelo.md`](docs/auditoria/CHANGELOG_modelo.md) — cómo evolucionó el modelo desde el artículo publicado.
- [`docs/auditoria/PLAN_ARTICULO.md`](docs/auditoria/PLAN_ARTICULO.md) — plan del próximo artículo.
- [`docs/auditoria/PLAN_ORDEN_REPOSITORIO.md`](docs/auditoria/PLAN_ORDEN_REPOSITORIO.md) — plan de orden y limpieza, por etapas.

## Cómo compilar

**El motor y el directorio de compilación no son intercambiables entre documentos.** Esta tabla es la referencia; cada combinación está verificada.

| Documento | Motor | Compilar desde | Notas |
|---|---|---|---|
| `Submissions/EnergyPolicy/inattention_energy_prices.tex` | `pdflatex` | su propia carpeta | clase Elsevier `cas-dc`, incluida en la carpeta. 15 páginas. |
| `docs/DocumentoMemoria/memoria.tex` | `xelatex` | su propia carpeta | 113 páginas. |
| `docs/MemoriaMHurtado/memoria.Rtex` | `xelatex -shell-escape` | su propia carpeta | **requiere Pygments** (`pip install Pygments`): `chapter03.tex` usa `minted`. 57 páginas. |
| `docs/Presentations/presentation-template/JMHL_presentation.tex` | `lualatex` | su propia carpeta | figuras en `figures/`, fuentes DM Sans en `font/`. 47 páginas. |
| `docs/Presentations/UVigo/home.Rmd` | R + `xaringan` | su propia carpeta | `rmarkdown::render("home.Rmd")`. El HTML renderizado y su `libs/` están versionados. |
| `docs/Presentations/IFORS/home.qmd` | `quarto render` | su propia carpeta | el HTML renderizado y su `home_files/` están versionados. |
| `Submissions/Energy_8000/R1/Clean_R1.Rtex` | R + `knitr` → `pdflatex` | su propia carpeta | `knitr::knit()` y luego `pdflatex` + `bibtex`. |
| `docs/Presentations/PhDEIIPUCV/main.tex` | `pdflatex` | su propia carpeta | beamer. |

Todos los documentos con bibliografía necesitan el ciclo completo:

```bash
<motor> documento && bibtex documento && <motor> documento && <motor> documento
```

**Criterio de aceptación de un documento**: compila con 0 errores, 0 figuras faltantes y 0 citas ni referencias indefinidas.

### Paquetes LaTeX

Además de una instalación estándar: `physics`, `yhmath`, `extarrows`, `cancel`, `mathdots`, `gensymb`, `pgfplots`, `siunitx`, `eurosym`, `bbm`, `subfigure`, `babel-spanish`, `changes`, `makecell`, `xurl`, `todonotes`, `truncate`, `minted` (con `fvextra`, `catchfile`, `xstring`, `framed`, `upquote`), y para la presentación de Hurtado `academicons`, `fontawesome5`, `tcolorbox`, `appendixnumberbeamer`, `lualatex-math`.

## Convenciones

- **Los artefactos de compilación no se versionan** (ver `.gitignore`). Sí se versionan los PDF finales de memorias y artículos, y el HTML renderizado de las presentaciones ya expuestas.
- **`Submissions/Energy_8000/` está congelada**: es la línea base del changelog y corresponde a un artículo publicado. Los `Figures/` repetidos entre carpetas de `Submissions/` son deliberados, para que cada envío histórico quede autocontenido.
- **`code/cnt_2050_total_cap900_scenarios.gdx`** se conserva a propósito: es la salida del solver para el escenario CAP=900 y no es reproducible sin licencia de GAMS.
- **Cada documento es autocontenido**: sus figuras viven en su propia carpeta y sus rutas son relativas a ella. El patrón heredado de Overleaf —todo relativo a la raíz del repositorio— se está retirando; ver el plan de orden. La memoria de Muñoz es la que aún lo usa.
