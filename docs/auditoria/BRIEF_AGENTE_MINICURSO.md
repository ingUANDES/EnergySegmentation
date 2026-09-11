# Brief para el agente del mini curso

Traspaso del estado del material docente y de lo que falta para la charla. El objetivo es
un mini curso que enseñe a computar los modelos de atención limitada en Google Colab con
Julia, sobre el *crash course* que dejó Vicente Muñoz en `ingUANDES/MCP` (privado, PAT
`GITHUB_MCP`).

## Lo que ya existe y corre

**`notebooks/` (rama `curso/colab-julia`)** — cuatro notebooks de Colab con runtime de
Julia, verificados de principio a fin, 0 errores:

| Notebook | Contenido | Estado |
|---|---|---|
| `00_mcp_en_colab` | KKT → complementariedad, el operador `⟂`, un equilibrio de mercado sin función objetivo | listo |
| `01_profit` | planificador *profit oriented*, atención como parámetro | listo |
| `02_tasa_cuadrada` | planificador de *tasa cuadrada*, atención endógena | listo |
| `03_precision` | planificador de *precisión*, atención comprada | listo |

`modelo_docente.jl` es la versión reducida (un periodo, tres tecnologías, demanda fija) con
las **ecuaciones del subastador idénticas** a `scripts/innatention/`. `generar.py`
reconstruye los cuatro notebooks desde ese archivo: el modelo se escribe una sola vez.

## El *crash course*, capítulo por capítulo

Libro Quarto en la raíz de `MCP`, ya renderizado en `docs/`. Trece capítulos:

| Capítulo | Palabras | Sirve para el curso |
|---|---|---|
| `teoriaDeJuego.qmd` | 1.833 | sí, base conceptual |
| `KKT.qmd` | 1.638 | sí, ya destilado en el notebook 00 |
| `MCP.qmd` | 660 | sí, ídem |
| `codingSetUp.qmd` | 810 | **obsoleto para Colab**: instala Julia local y Quarto |
| `juliaAndJump.qmd` | 1.226 | sí, 18 bloques de código ejecutables |
| `practicalExercises.qmd` | 984 | sí, ejercicios reutilizables |
| `amigoEtAlii.qmd` | 4.728 | referencia del modelo base, demasiado largo para la charla |
| `costosDeInformacion.qmd` | 600 | sí, es el corazón conceptual |
| `racionalidadPlanificador.qmd` | 308 | sí, corto y al punto |
| `planificadorProfitOriented.qmd` | 665 | sí |
| `planificadorWelfareOriented.qmd` | 3.044 | sí, cubre tasa cuadrada y precisión |
| `troubleshooting.qmd` | 561 | revisar: apunta a problemas de instalación local |

## Trampas del entorno, ya pagadas

1. **Colab soporta Julia como runtime nativo**: `Entorno de ejecución` → `Cambiar tipo de
   entorno` → Julia. No hace falta instalar kernels a mano. La versión que trae hoy es
   Julia 1.12.6.
2. **La licencia de PATH embebida en los scripts venció el 31/12/2025.** La vigente,
   *courtesy* académica y gratuita, está en
   <https://pages.cs.wisc.edu/~ferris/path/LICENSE> y corre hasta 2035. **Nunca la dejes
   escrita en un notebook**: los notebooks la piden por pantalla.
3. **PATH es libre hasta 300 variables.** El modelo docente cabe; el completo del artículo
   (unas 5.700 variables) no. Por eso el curso usa el reducido: el alumno no necesita
   licencia.
4. **`convergence_tolerance` importa.** Con la de por defecto ($10^{-6}$) el modelo base de
   Amigo termina en $\pi^a = 276{,}88$; con $10^{-8}$ converge al 315,82 correcto. Los
   notebooks ya la fijan.
5. **PATH reporta `SLOW_PROGRESS` con estado interno *"A stationary point was found"***, no
   `LOCALLY_SOLVED`, en el modelo grande. Un punto estacionario **no** es necesariamente
   solución del MCP: hay que comprobar la factibilidad a mano. En cinco de diez
   presupuestos el script de precisión devuelve un punto que viola su propia cota de
   rendimiento.
6. **`profit_oriented.jl` no corre tal cual**: usa `cm` en `theta_const` pero la línea que
   lo define está comentada y `parameters.jl` no lo declara.
7. **El repositorio es privado**, así que ningún notebook que se comparta puede clonarlo.

## Criterio de aceptación de cada notebook

- Corre de principio a fin en un Colab limpio, con runtime de Julia, **sin editar nada**.
- No clona `MCP` ni ningún repositorio privado.
- No trae licencia de PATH embebida.
- Cada modelo se resuelve y PATH reporta *"The problem was solved"*, no un punto
  estacionario.
- Cierra con al menos dos ejercicios que el alumno pueda resolver modificando una línea.

## Lo que falta para la charla

1. **Guion y duración.** Los cuatro notebooks son el material; falta el recorrido y el
   reparto de tiempo.
2. **Decidir si el curso se dicta desde el repositorio privado.** Recomendación: mover
   `notebooks/` y el *crash course* a un repositorio público y dejar los scripts de
   investigación en el privado. Los notebooks son autocontenidos para no forzar esa
   decisión ahora.
3. **Actualizar `codingSetUp.qmd` y `troubleshooting.qmd`**, que suponen instalación local
   de Julia y Quarto y no mencionan Colab.
4. **El puente hacia el artículo nuevo.** El ejercicio 3.2 del notebook de precisión deja
   planteado exactamente el hueco que el próximo artículo quiere llenar: un planificador
   que elija el nivel de atención **y** pague por él. Es un buen cierre de la charla y la
   conexión natural con la investigación en curso.

## Dónde está todo

- Notebooks: `ingUANDES/MCP`, rama `curso/colab-julia`, carpeta `notebooks/`.
- Modelos de investigación: `ingUANDES/MCP`, `scripts/`.
- Artículo y auditorías: `ingUANDES/EnergySegmentation`.
- Informe de replicación, con lo que replica y lo que no:
  `EnergySegmentation/docs/auditoria/replicacion/INFORME_REPLICACION.md`.
- Relación entre los dos repositorios: `RELACION_REPOSITORIOS.md`.
