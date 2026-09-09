# Figuras sueltas archivadas

Estas imágenes estaban en la raíz del repositorio y **ningún documento del proyecto las
compone**: 58 no aparecen en ninguna fuente y una aparece sólo dentro de un bloque
comentado (ver más abajo). Comprobado sobre todos los `.tex`, `.Rtex`, `.Rmd`, `.qmd`,
`.sty` y `.cls` versionados. Son 59 archivos, 17,0 MB.

Se archivan en vez de borrarse: algunas pueden ser figuras de resultados cuyo código
generador ya no existe. **Pendiente de que los autores confirmen qué se conserva y qué
se elimina** — etapa 1 de [`../docs/auditoria/PLAN_ORDEN_REPOSITORIO.md`](../docs/auditoria/PLAN_ORDEN_REPOSITORIO.md).

## Descartes de una figura que sí se usa

En estos cuatro grupos la versión vigente ya está en la carpeta del documento que la usa,
y aquí queda la anterior. Son los candidatos más claros a eliminar:

| archivada aquí | versión en uso | MB de la archivada |
|---|---|---|
| `calibracion.png` | `calibracion2.png` | 1.38 |
| `CCCC.png` | `cccc.png` | 1.06 |
| `melect.png` | `melect3.png` | 0.22 |
| `melect1.png` | `melect3.png` | 0.17 |
| `melect2.png` | `melect3.png` | 0.18 |
| `MODELOILUS2.png` | `MODELOILUS1.png` | 1.47 |

## Caso aparte: referenciada, pero en código comentado

`costo precisión gabaix.png` sí aparece en un `\includegraphics` de
`docs/MemoriaMHurtado/attachments/anexo_a.tex`, pero dentro de un bloque `figure`
íntegramente comentado (líneas 455-459), así que no se compone en el PDF. Se archiva aquí
y la línea comentada lleva una nota: si se reactiva el bloque, hay que mover el archivo a
`docs/MemoriaMHurtado/figures/`.

## Series completas sin uso

- `emisionesm0.png`, `emisionesm0.5.png`, `emisionesm1.png` — emisiones por nivel de atención;
  ninguna se referencia, aunque la memoria de Hurtado sí discute ese resultado.

## Las diez más pesadas

| archivo | MB |
|---|---|
| `impuestoscarb.png` | 1.82 |
| `sapiro1.png` | 1.79 |
| `evol.png` | 1.79 |
| `image.png` | 1.69 |
| `matrixenerg.png` | 1.60 |
| `MODELOILUS2.png` | 1.47 |
| `calibracion.png` | 1.38 |
| `CCCC.png` | 1.06 |
| `impuestoscarbono2.png` | 0.38 |
| `melect.png` | 0.22 |

## Inventario completo

[`../docs/auditoria/inventario_raiz.csv`](../docs/auditoria/inventario_raiz.csv) lista las 96 imágenes que estaban en la
raíz, con su tamaño y su destino: archivada aquí, o movida a la carpeta del documento que la usa.

