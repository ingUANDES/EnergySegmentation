# Relación entre `EnergySegmentation` y `MCP`

Los dos repositorios del proyecto son complementarios y la división es deliberada. Este
documento fija qué vive en cada uno, qué depende de qué, y qué hay que tocar en uno cuando
cambia el otro.

| | `ingUANDES/EnergySegmentation` | `ingUANDES/MCP` |
|---|---|---|
| Visibilidad | público | **privado** |
| Qué contiene | documentos y resultados | código y enseñanza |
| Token | `GITHUB_ENERGY` | `GITHUB_MCP` |
| Artefactos | memorias, artículos, presentaciones, auditorías | scripts de los modelos, *crash course*, notebooks de Colab |

## Qué vive en cada uno

**`EnergySegmentation`** — lo que se lee.

- `Submissions/Energy_8000/` — el artículo publicado en *Energy*. **Línea base congelada**:
  no se toca.
- `Submissions/EnergyPolicy/` — el artículo en desarrollo, `inattention_energy_prices.tex`.
- `docs/DocumentoMemoria/`, `docs/MemoriaMHurtado/` — las memorias de Muñoz y de Hurtado.
- `docs/Presentations/` — las charlas: UVigo, IFORS, PhDEIIPUCV y la defensa de Hurtado.
- `docs/auditoria/` — las auditorías, el changelog del modelo y los planes.
- `docs/auditoria/replicacion/` — **el código de auditoría del artículo**, que es el único
  lugar donde un repositorio depende del otro.

**`MCP`** — lo que se ejecuta y lo que se enseña.

- `scripts/amigo/` — el modelo original de Amigo et al. (2021), la línea base de calibración.
- `scripts/innatention/` — los tres planificadores del artículo: `profit_oriented.jl`,
  `quadratic_rate.jl`, `precision.jl`.
- `scripts/parameters/` — sets y calibración del sistema eléctrico chileno.
- `*.qmd` + `docs/` — el *crash course* de MCP, libro Quarto ya renderizado.
- `notebooks/` — el mini curso de Colab, autocontenido.

## La única dependencia, y en qué dirección

```
EnergySegmentation/docs/auditoria/replicacion/   ──lee──>   MCP/scripts/
```

El código de auditoría **corre los scripts de `MCP` sin editarlos**: lee su texto y
sustituye sólo la línea de licencia, los parámetros `cm`, `Performance` y `mean`, y las
opciones del solver. Cada sustitución queda registrada en la salida, así que una corrida
siempre declara con qué valores se hizo.

Para reproducir, los dos repositorios se clonan hermanos y `MCP` como `mcp/`:

```
proyecto/
├── EnergySegmentation/
└── mcp/                     # clon de ingUANDES/MCP
```

**No hay dependencia en la otra dirección.** `MCP` no lee nada de `EnergySegmentation`, y
los notebooks del mini curso no leen nada de `MCP` tampoco: traen el modelo en una celda,
precisamente para que se puedan compartir siendo `MCP` privado.

## Qué tocar cuando cambia lo otro

| Si cambia… | Hay que… |
|---|---|
| una ecuación en `MCP/scripts/innatention/` | volver a correr `docs/auditoria/replicacion/grilla.sh` y `comparar.py`, y revisar el informe de replicación |
| un parámetro de calibración en `MCP/scripts/parameters/` | lo mismo, y revisar si el artículo declara ese valor |
| una tabla o figura del artículo | volver a correr `extraer_cifras_articulo.py`; el CSV de cifras es la referencia de la comparación |
| el modelo docente `MCP/notebooks/modelo_docente.jl` | `python3 generar.py` para regenerar los cuatro notebooks |
| la licencia de PATH | nada en el código: va por `PATH_LICENSE_STRING`, nunca versionada |

## Dos cosas que conviene resolver

1. **El código que produjo los resultados publicados no está en ninguno de los dos.** El
   artículo dice dos veces que los modelos se resolvieron con PATH **en GAMS**; el único
   `.gms` versionado es el modelo original de Amigo con presupuesto por riesgo. Mientras eso
   siga así, la replicación no puede ser completa. Ver el informe de replicación.
2. **`MCP` es privado y contiene el material docente.** Si el mini curso se va a dictar, lo
   razonable es separar: el material de enseñanza —`notebooks/` y el *crash course*— en un
   repositorio público, y dejar en el privado sólo los scripts de investigación. Hoy los
   notebooks son autocontenidos justamente para no forzar esa decisión.
