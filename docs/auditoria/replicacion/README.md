# Replicación de los resultados del artículo

Código y salidas de la replicación independiente de
`Submissions/EnergyPolicy/inattention_energy_prices.tex`. El informe es
[`INFORME_REPLICACION.md`](INFORME_REPLICACION.md).

Los modelos **no viven aquí**: son los scripts Julia de `ingUANDES/MCP`
(`scripts/innatention/`), que este código corre sin editarlos. Ver la sección de relación
entre repositorios en el README de la raíz.

| Archivo | Qué es |
|---|---|
| `extraer_cifras_articulo.py` | Vuelca a CSV toda cifra del artículo con su ubicación exacta |
| `cifras_articulo.csv` | 865 cifras: 259 de 7 tablas, 320 de 9 figuras, 286 en prosa |
| `correr_modelo.jl` | Corre un modelo del repo MCP sustituyendo sólo licencia, parámetros y opciones del solver |
| `grilla.sh` | Genera los 54 puntos de las grillas que reportan las tablas |
| `corridas_todas.csv` | Resultado crudo de las 54 corridas, con las sustituciones aplicadas |
| `comparar.py` | Cruza cada celda publicada contra su corrida |
| `replicacion.csv` | 181 celdas con veredicto |
| `veredicto_celdas_disputadas.csv` | Las dos celdas de $\pi^a$ resueltas |
| `replicacion_profit_oriented.png` | Publicado contra replicado en el barrido de CAP |

## Requisitos

- Julia con `JuMP`, `PATHSolver`, `DataFrames`, `CSV`, `XLSX`.
- El repositorio `ingUANDES/MCP` clonado como `mcp/` junto a este.
- Una licencia *courtesy* vigente de PATH en `PATH_LICENSE_STRING`, de
  <https://pages.cs.wisc.edu/~ferris/path/LICENSE>. **No se versiona.** La que traen
  embebida los scripts del repo MCP venció el 31/12/2025.

```bash
export PATH_LICENSE_STRING="..."
python3 extraer_cifras_articulo.py ../../../Submissions/EnergyPolicy/inattention_energy_prices.tex cifras_articulo.csv
bash grilla.sh > comandos.txt && xargs -P5 -I{} sh -c "{}" < comandos.txt
python3 comparar.py
```
