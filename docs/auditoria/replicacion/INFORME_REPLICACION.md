# Informe de replicación — *Inattention rises energy prices*

Replicación independiente de los resultados de
`Submissions/EnergyPolicy/inattention_energy_prices.tex` resolviendo los modelos con
PATH desde los scripts Julia de `ingUANDES/MCP@e40d31c`.

**Veredicto corto.** El barrido de presupuesto de carbono del modelo *profit oriented*
replica: **la figura del propio artículo coincide en los diez puntos y la tabla en ocho**.
Las dos celdas que no coinciden son exactamente las que un test de consistencia ya había
señalado, y quedan zanjadas. El resto del artículo **no replica** con el código
disponible, y hay una razón declarada en el propio texto: los resultados publicados se
obtuvieron en GAMS, y ese código no está en ninguno de los dos repositorios.

---

## 1. Método

| | |
|---|---|
| Solver | PATH 5.0.x vía `PATHSolver.jl`, licencia *courtesy* vigente (emitida 5/1/2026, sin límite de tamaño) |
| Modelos | `profit_oriented.jl`, `quadratic_rate.jl`, `precision.jl` y `amigo.jl` de `ingUANDES/MCP` |
| Puntos resueltos | 54, 3.761 s de solver |
| Tolerancia de comparación | 0,5 % relativo; 0,006 absoluto en razones y rendimientos |
| Celdas comparadas | 181 |

Los scripts **no se editaron**. `auditoria/correr_modelo.jl` lee el texto de cada uno y
sustituye únicamente la línea de licencia, los parámetros `cm`, `Performance` y `mean`, y
las opciones del solver; cada sustitución queda registrada en la salida.

**Validación de la base.** `amigo.jl` reproduce $\pi^a = 315{,}8245$ y
$\pi^d = 302{,}6147$, que son exactamente el 315,83 que el artículo declara como
referencia y los valores que `profit_oriented.jl` trae escritos como punto de partida
*"optimal results from Amigo et alii code"*. La coincidencia es de once cifras: el
entorno y la calibración son los correctos.

**Un cambio de método, declarado.** Con la tolerancia de convergencia por defecto de PATH
($10^{-6}$) el modelo base termina en $\pi^a = 276{,}88$, un 12 % por debajo. Con
$10^{-8}$ converge al valor de referencia. Todas las corridas usan $10^{-8}$. PATH reporta
`SLOW_PROGRESS` con estado interno *"A stationary point was found"*, no `LOCALLY_SOLVED`.

---

## 2. Las dos celdas disputadas: resueltas

Tres evidencias independientes coinciden.

| $CAP$ | Tabla (líneas 541 y 547) | Figura `piapormodelo` (línea 1094) | Replicado con PATH | Patrón log-log de las otras 8 filas |
|---|---|---|---|---|
| 200 MtCO₂e | \$60,57 | **\$161,56** | **161,560** | 162,10 |
| 800 MtCO₂e | \$152,50 | **\$48,76** | **48,765** | 49,26 |

La serie *Profit Oriented* de la figura replica en **los diez puntos**; la tabla, en ocho.
Quitando esas dos filas, la columna $\pi^a$ de la tabla es monótona decreciente en las
siete diferencias restantes, y un ajuste log-log sobre ellas ($R^2 = 0{,}986$) predice
justo los valores de la figura.

**Son errores de transcripción de la tabla.** Los valores correctos son los de la figura.
Hay que corregir las dos celdas y retirar las tres menciones al "salto en CAP=800" como
posible error del solver (líneas 553, 654 y 671): con la celda corregida el salto no
existe.

---

## 3. Lo que no replica

### 3.1 La columna $\theta$ del mismo barrido

Sólo replican **5 de 10** celdas: exactamente las cinco filas en la esquina
$\theta = CAP\,(1+\epsilon)$, con $\epsilon = 0{,}202$. En las otras cinco, la tabla
publicada trae:

- $CAP=400$: 454.798.037, mientras la replicación da la esquina, 480.800.000;
- $CAP = 600, 700, 900$ y $1.000$: **el mismo valor, 605.279.899, repetido cuatro veces**.

Cuatro presupuestos distintos no pueden dar los mismos permisos emitidos hasta el último
dígito. Es la firma de un valor que quedó congelado, no de cuatro equilibrios.

Esto **afecta una afirmación del artículo**. La columna $\theta/CAP$ (1,01, 0,86, 0,67,
0,61) está calculada sobre esos cuatro valores repetidos, y sobre ella descansa la frase
de la línea 553: *"the model shows a decreasing relationship $\theta/CAP$ while increasing
the parameter of carbon budget"*. Con los $\theta$ replicados la razón es constante en
1,202 y **la relación decreciente desaparece**. Es lo primero que hay que resolver antes
de enviar.

### 3.2 El efecto del rendimiento $P$ (Tabla `efectopenthetapia`)

No replica: 2 de 14 celdas de $\pi^a$. En la replicación, con $CAP = 100$ MtCO₂e el modelo
se queda en la esquina $\theta = 120{,}2$ M y $\pi^a = 270{,}13$ **para todo $P \ge 0{,}8$**,
porque $\eta = 0$ y la restricción de costo de información no llega a morder. La tabla
publicada muestra $\theta$ y $\pi^a$ variando de forma no monótona (25,75 en $P=0{,}85$,
317,24 en $P=1$), que la replicación no produce con ningún $c$ probado.

### 3.3 Los modelos de bienestar

| Tabla | Celdas que coinciden |
|---|---|
| Tasa cuadrada (`resultadostasacuadrada`) | 4 de 39 |
| Precisión (`resultadosprecision`) | 0 de 40 |

Además, **cinco de las diez corridas del modelo de precisión violan la cota del propio
script**: la restricción `mu_const` exige $1 - r_p/CAP - d \ge 0$, y el punto que PATH
devuelve tiene $r_p/CAP$ hasta 1,21 cuando el máximo admisible es 0,202. El rendimiento
implicado llega a 2,00, imposible por definición ($P \le 1$). Esos puntos estacionarios
**no son soluciones del MCP**: el script de precisión, tal como está, no resuelve el
modelo que el artículo describe.

### 3.4 El valor de $c$ del planificador *profit oriented*

El artículo declara $c = 920.000$ millones. Ese valor no está en el repositorio: en
`profit_oriented.jl` la línea de `cm` está comentada, aunque la restricción `theta_const`
la usa, de modo que **el script no corre tal cual** (`UndefVarError: cm`). Al inyectarlo,
$c = 9{,}2\times10^{11}$ produce $\pi^a = 254.868$ USD/t en $P=1$, tres órdenes de magnitud
fuera de escala. Los de tasa cuadrada (9.900 millones) y precisión (4 millones) sí
coinciden con sus scripts. En el barrido de CAP el resultado es idéntico con
$9{,}2\times10^{8}$ y con $9{,}2\times10^{11}$ —el modelo está en la esquina y $c$ no
muerde—, así que la ambigüedad no afecta la corrección de las dos celdas.

---

## 4. Por qué no replica: el código publicado no está

El artículo dice dos veces que los modelos *"are transformed to a MCP … solved using the
PATH solver **in GAMS**"* (líneas 505 y 683). El único `.gms` de los dos repositorios,
`code/cnt_2050_total_cap_scenarios.gms`, es el modelo original de Amigo con presupuesto
por riesgo (`theta_const: -theta + PhiRisk*Std + mean ≥ 0`), no el del subastador
inatento. **El código que produjo las tablas publicadas no está versionado en ninguno de
los dos repositorios.** Los scripts Julia del *crash course* son una traducción
posterior, y salvo el barrido de CAP del modelo *profit oriented*, no reproducen los
resultados.

---

## 5. Otros hallazgos del artículo

- **Hueco en una tabla**: en `resultadostasacuadrada`, la fila $CAP = 400$ MtCO₂e no tiene
  valor numérico de $\pi^a$; la figura sí traza un punto ahí, con valor 0,00.
- **Inversión fijada en cero**: los cuatro scripts incluyen `variables_fix.jl`, que fija
  `x_first = 0` y `x_next = 0` antes de optimizar. El artículo presenta el modelo **con**
  decisiones de inversión en capacidad y no declara ese fijado. Un revisor que intente
  reproducir con el modelo tal como está escrito no va a obtener estos números.

---

## 6. Qué corregir antes de enviar

1. **Las dos celdas** de `efectocapthetapia`: 60,57 → 161,56 y 152,50 → 48,76, y retirar
   las tres menciones al salto de CAP=800.
2. **La columna $\theta$** del mismo barrido: resolver el valor repetido cuatro veces y
   revisar si la afirmación sobre $\theta/CAP$ decreciente sobrevive.
3. **Declarar el software y versionar el código** que produjo los resultados. Hoy el
   artículo dice GAMS y el código GAMS no existe en los repositorios.
4. **Declarar que la inversión está fijada en cero**, o correr con inversión libre.
5. **Corregir `profit_oriented.jl`**: descomentar `cm` con el valor que se declare, para
   que el script corra.
6. **Revisar el modelo de precisión**: en cinco de diez presupuestos su solución viola su
   propia restricción de rendimiento.
7. **Rellenar el hueco** de $\pi^a$ en $CAP = 400$ de la tabla de tasa cuadrada.

---

## 7. Cómo reproducir este informe

```bash
export PATH_LICENSE_STRING="<licencia courtesy de pages.cs.wisc.edu/~ferris/path/LICENSE>"
python3 extraer_cifras_articulo.py <articulo>.tex cifras_articulo.csv
bash auditoria/grilla.sh > auditoria/comandos.txt
xargs -P5 -I{} sh -c "{}" < auditoria/comandos.txt
python3 auditoria/comparar.py
```

Salidas: `cifras_articulo.csv` (865 cifras del artículo con su ubicación exacta),
`auditoria/corridas_todas.csv` (54 corridas), `auditoria/replicacion.csv` (181 celdas con
veredicto) y `auditoria/veredicto_celdas_disputadas.csv`.
