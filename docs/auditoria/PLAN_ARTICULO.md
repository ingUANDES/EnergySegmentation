# Plan del artículo — ¿seguir alineado a UVigo, y qué aporta la memoria de Hurtado?

Documento de decisión. Contexto en [`CHANGELOG_modelo.md`](CHANGELOG_modelo.md); hallazgos técnicos en [`AUDITORIA_memoria_VMunoz.md`](AUDITORIA_memoria_VMunoz.md) y [`AUDITORIA_2_MHurtado.md`](AUDITORIA_2_MHurtado.md).

---

## 1. Evaluación del borrador de `Submissions/EnergyPolicy`

### El borrador como vehículo: sí. Como contribución: no alcanza.

Lo que hay en la carpeta hoy es sólido en su parte mecánica y débil en su parte científica.

**Lo que funciona y hay que conservar.** El artículo entregado (`inattention_energy_prices.tex`, 15 páginas, 0 errores, sin citas ni referencias indefinidas) ya tiene escrita la formulación completa —productores, subastador, equilibrio, condiciones de vaciado—, las tres especificaciones del planificador, los resultados sobre diez presupuestos con sus tablas y sus nueve figuras, el anexo con las condiciones MCP de las tres variantes, y la bibliografía cerrada. Eso es infraestructura de artículo que cuesta semanas reconstruir y que **es independiente del mecanismo de inatención que se elija**: el bloque de productores y el equilibrio son los del artículo publicado en *Energy* y no cambian.

**Lo que no alcanza.** La contribución declarada —"tres especificaciones de un planificador inatento"— no resiste una revisión de revista, y la razón está en las propias conclusiones del artículo:

- En la especificación *profit oriented*, el rendimiento `P` es un **parámetro**, no una variable. Ese modelo es un análisis de sensibilidad respecto de la atención, no inatención racional.
- En la especificación de *precisión*, donde `P` es endógeno, la solución se queda en la **esquina `P = 0,798`** para los diez presupuestos: el planificador nunca compra información.
- Sólo la de *tasa cuadrada* tiene atención endógena e interior, y su estática comparativa no es monótona.
- El costo marginal `c` se calibra igualando `π^a` al del modelo original; no tiene interpretación estructural ni contraparte observable. Tres especificaciones dan tres valores de `c` que difieren en cinco órdenes de magnitud (920.000 M, 9.900 M y 4 M USD), lo que es señal de que `c` está absorbiendo el desajuste del modelo y no midiendo nada.

Un revisor preguntará qué es `c` y cómo se mide. Con el material del estado actual, la respuesta honesta es que se ajusta para reproducir un precio. **Ése es el techo del artículo tal como está planteado**, y no se sube escribiendo mejor: se sube cambiando de qué se hace cargo el artículo.

### Recomendación

**Seguir desarrollando el artículo en `Submissions/EnergyPolicy`, conservando el arco expositivo de la presentación UVigo, pero reencuadrando la contribución: de "tres especificaciones de inatención racional" a "una familia de subastadores con racionalidad limitada, anidados en un mismo marco, calibrada sobre Chile".**

Tres razones:

1. **La presentación UVigo sigue siendo la arquitectura correcta.** Su secuencia —motivación, literatura, modelo en dos etapas, subastador, equilibrio, mecanismo de inatención, resultados, comentarios finales— es la de un artículo de política energética y es la que ya está implementada. Lo que hay que cambiar es el contenido de una sección, no el orden de las secciones.
2. **El mecanismo de Gabaix resuelve el problema que UVigo dejó abierto.** Los *Final Remarks* de la presentación dicen literalmente *"Unclear relation of inattention"* y *"Multiple solutions and comparative statics"*. La memoria de Hurtado elimina las dos: solución cerrada (sin multiplicidad ni esquinas) y atención con contraparte observable.
3. **Abandonar UVigo y escribir un artículo nuevo sólo sobre Hurtado desperdiciaría el resto.** El costo de precisión de Muñoz es justamente lo que le falta al modelo de Hurtado, donde la atención está identificada pero es gratis.

---

## 2. Qué aporta la memoria de Hurtado al artículo

Los dos trabajos son **mitades complementarias del mismo problema**, y esto no es una lectura forzada: es lo que dice la conclusión de la memoria de Hurtado cuando propone como línea futura *"incorporar explícitamente el costo de aumentar la capacidad de atención del planificador"* — que es, exactamente, el `c(P−d)²` de Muñoz.

| | Muñoz (estado 1–3) | Hurtado (estado 4–5) |
|---|---|---|
| Costo de la atención | **sí**, `c(P−d)²` | no, la atención es gratis |
| Identificación de la atención | no, `c` se ajusta a un precio | **sí**, `m = σ²_CAP/(σ²_CAP+σ²_ε)` calibrado sobre datos |
| Comportamiento de la solución | esquinas, multiplicidad, no monotonía | **solución cerrada** |
| Anclaje empírico | grilla exógena 100–1.000 MtCO₂e | **presupuestos chilenos vigentes y SCC oficial** |
| Horizonte | 2019–2050 | 2020–2030 |

### Aportes concretos, en orden de valor

**(a) Un diagnóstico más fuerte del modelo original.** La memoria de Hurtado no dice que la parametrización del subastador sea mejorable: demuestra que **el problema está indeterminado**. La restricción probabilística `Pr(θ≥CAP)≤ε` se satisface con igualdad, luego `θ = CAP` determinísticamente y `F(θ)` es irrelevante; lo muestra resolviendo el problema con dos formas de `F(θ)` (costo fijo y costo convexo) y obteniendo la misma decisión. Esto reemplaza el párrafo de motivación del artículo por un argumento verificable, y es una motivación mucho más fuerte que "el `c` no tiene interpretación estructural".

**(b) Un mecanismo con solución cerrada que anida el de Muñoz.** El marco de Gabaix (2019) permite escribir las dos formulaciones como casos de una misma estructura: la atención `m` como peso entre el ancla `CAP_d` y la señal `CAP_s`, y el costo de atención como lo que determina `m` endógenamente. Muñoz da el costo; Hurtado da el mapeo `σ_ε → m`. Uniéndolos, `m` deja de ser un dato y pasa a ser elegido, que es la formulación que ninguno de los dos tiene.

**(c) Calibración empírica que el artículo hoy no tiene.** El artículo actual calibra contra un precio del modelo original. La memoria de Hurtado calibra contra **la matriz eléctrica chilena observada de 2024**, con parámetros de fuentes oficiales verificables: `CAP_s = 264,20` MtCO₂e del Plan de Mitigación 2024 del Ministerio de Energía, `CAP_d = 311,01` MtCO₂e del acumulado SNICHILE 2012–2022, `κ = 64,40` USD/tCO₂e del costo social del carbono oficial de Chile. Esto convierte la sección de calibración de un ejercicio interno en un ejercicio contrastable.

**(d) Un resultado de política publicable.** El modelo estima un presupuesto implícito de 311,01 MtCO₂e frente a la meta de 264,2 MtCO₂e del sector eléctrico: una brecha de ~47 MtCO₂e atribuible a que el sistema sigue anclado en la trayectoria histórica. Y el contraste con la literatura es directo: Gabaix reporta una atención promedio estimada de **0,44**, mientras la calibración chilena es compatible con niveles cercanos a **0,1**. Ese contraste —el regulador chileno atiende menos que el agente promedio de la literatura experimental— es un resultado con lector.

**(e) Actualización del horizonte y del marco institucional.** Horizonte 2020–2030 con datos ejecutados hasta 2024, en vez de 2019–2050 proyectado. Y 26 referencias institucionales chilenas actuales en `docs/Presentations/presentation-template/references.bib` (anteproyecto MMA 2025, Coordinador Eléctrico Nacional 2024, Leyes 20.780 y 21.455, ICAP) que hoy no están en ninguna bibliografía del repositorio.

**(f) Un contraejemplo útil para las conclusiones.** El hecho de que la calibración de Hurtado sea **monótona en `m`** —la distancia al mix observado crece de 0,2727 a 0,3026 al pasar de `m=0` a `m=1`— dice algo que el artículo debe reportar: en este modelo, *más atención empeora el ajuste al mix observado*. Sea porque el regulador chileno efectivamente atiende poco, sea porque el modelo no captura otros determinantes del mix, es un resultado que orienta la agenda.

### Lo que **no** hay que importar sin corregir

Tres cosas del estado 4 no pueden entrar al artículo tal como están (detalle en [`AUDITORIA_2_MHurtado.md`](AUDITORIA_2_MHurtado.md) §4.2):

1. **La escala de la penalización.** `(κ/2)(θ−CAP)²` con `κ` en USD/tCO₂e da costos de 10¹⁷–10¹⁸ USD, unas 15.000 veces el PIB mundial, y hace que `π^a/κ` valga ~3 toneladas sobre una decisión de 3×10⁸: el canal de precio no opera. Hay que normalizar la desviación —`(κ/2)·CAP·((θ−CAP)/CAP)²`— o usar penalización lineal `κ·|θ−CAP|`, que es lo que la interpretación de `κ` como costo social del carbono justifica. **Sin esta corrección el artículo afirmaría un mecanismo de precios que sus propios números desmienten.**
2. **La conclusión fuerte de la calibración.** Con un criterio monótono, "Chile opera con `m=0,1`" no está identificado. La versión defendible es la débil: el mix observado es más compatible con atención baja que con atención alta, sobre un ajuste absoluto que es pobre a cualquier nivel (~27 puntos).
3. **El rol de `CAP_d` como media del presupuesto verdadero.** Que la tendencia histórica sea el centro no sesgado de `CAP` y la meta de política la señal ruidosa es una asignación de roles que determina el signo del resultado principal. Hay que argumentarla explícitamente, no heredarla.

---

## 3. Estructura propuesta del artículo

Manteniendo el arco de UVigo y el archivo `Submissions/EnergyPolicy/inattention_energy_prices.tex`:

| § | Sección | Origen | Estado |
|---|---|---|---|
| 1 | Introduction | actual + institucional de Hurtado | ampliar con marco chileno 2024–2025 |
| 2 | Literature review | actual + Gabaix (2019) como puente | **añadir** el anclaje y ajuste junto a la inatención racional |
| 3 | The capacity investment model | actual (productores, equilibrio) | **sin cambios** |
| 4 | The auctioneer's problem is indeterminate | Hurtado ch02 §*Espacio de Mejora* | **nueva**: los dos escenarios de `F(θ)` como motivación |
| 5 | A family of boundedly rational auctioneers | Muñoz (costo) + Hurtado (anclaje) | **nueva**: marco común, con 5.1 costo de precisión, 5.2 anclaje y ajuste, 5.3 la versión con `m` elegido y costoso |
| 6 | Calibration to the Chilean power system | Hurtado ch03–ch04 | **nueva**: `CAP_s`, `CAP_d`, `σ_CAP`, `κ`, mix 2024, con la penalización reescalada |
| 7 | Results | actual (grilla de presupuestos) + Hurtado (niveles de atención) | fusionar los dos ejercicios |
| 8 | Conclusions | actual + Hurtado ch05 | reescribir sobre la contribución nueva |
| A | MCP formulation | actual | **sin cambios** |
| B | Demand scenarios | actual | **sin cambios** |

La sección 5.3 —atención elegida *y* costosa, con `m` endógeno sobre el mapeo `σ_ε → m` calibrado— es la contribución original del artículo y no existe en ninguna de las dos memorias.

---

## 4. Orden de trabajo

1. Reescalar la penalización del planificador conductual y recalcular las columnas de costo y utilidad de la memoria de Hurtado. **Es prerrequisito de todo lo demás**: define si el canal de precio existe.
2. Resolver la discrepancia de `π^a` en `CAP=200` y `CAP=800` de la memoria de Muñoz (ver `AUDITORIA_memoria_VMunoz.md` §5); afecta la tabla y la figura que el artículo ya usa.
3. Escribir la sección 4 (indeterminación) desde `chapter02.tex` de Hurtado.
4. Escribir el marco común de la sección 5 y derivar 5.3.
5. Incorporar la sección 6 de calibración, con la penalización corregida y la conclusión en su versión débil.
6. Fusionar resultados: la grilla de presupuestos de Muñoz con los niveles de atención de Hurtado, decidiendo un horizonte único (2020–2030 con datos ejecutados, o 2019–2050 proyectado — no ambos).
7. Unificar bibliografías: `Submissions/EnergyPolicy/references.bib` + las 26 entradas institucionales de la presentación de Hurtado.
8. Reescribir conclusiones y highlights.

### Decisión pendiente de autoría

El artículo actual lleva a Cea-Echenique, Muñoz y Feijoo. Si se incorpora el material de los estados 4–5 —que es el que sostiene la contribución nueva— corresponde definir la autoría antes de escribir, no después.
