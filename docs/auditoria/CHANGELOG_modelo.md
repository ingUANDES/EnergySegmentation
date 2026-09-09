# Changelog del modelo — desde el artículo publicado en *Energy* hasta hoy

Línea base: **`Submissions/Energy_8000/R1/Clean_R1.Rtex`**, la versión R1 limpia de Amigo, Cea-Echenique y Feijoo, *"A two-stage stochastic capacity investment model with cap-and-trade"*, publicada en *Energy* ([10.1016/j.energy.2021.120129](https://doi.org/10.1016/j.energy.2021.120129)). Todo lo que sigue se describe como diferencia respecto de ese documento.

Los cinco estados del modelo, en orden cronológico:

| # | Estado | Ubicación | Fecha |
|---|---|---|---|
| **0** | Artículo publicado en *Energy* | `Submissions/Energy_8000/R1/Clean_R1.Rtex` | 2021 |
| **1** | Memoria de Vicente Muñoz L'Huillier | `docs/DocumentoMemoria/` | jul 2022 |
| **2** | Presentación UVigo | `docs/Presentations/UVigo/home.Rmd` | jul 2022 |
| **3** | Artículo *Inattention raises energy prices* | `Submissions/EnergyPolicy/inattention_energy_prices.tex` | sep 2026 |
| **4** | Memoria de Juan Matías Hurtado | `docs/MemoriaMHurtado/` | ago 2025 |
| **5** | Presentación de defensa de Hurtado | `docs/Presentations/HurtadoDefensa2026/JMHL_presentation.tex` | 2026 |

Los estados 4 y 5 son posteriores al 1–2 pero **no** derivan del 3: se desarrollaron en paralelo, a partir de la memoria de Muñoz directamente.

---

## Estado 0 — línea base publicada (2021)

**Estructura.** Introduction · Model Description (Producer's problem · Auctioneer's problem · Equilibrium and solution technique) · Model calibration to the Chilean Electric Sector and carbon budget estimates (The Chilean electric market · Determination of the carbon budget) · Results and discussion (Role of the cap-and-trade system in a deterministic context · Impact of demand uncertainty on the Chilean pledges) · Conclusions · Apéndices (MCP Formulation · Chilean pledges).

**Subastador.** El presupuesto de carbono es aleatorio, `CAP ~ N(μ, σ²)`, y el subastador opera bajo restricción probabilística:

```
Pr(θ ≥ CAP) ≤ ε        →        φ⁻¹(ε)·σ + μ − θ ≥ 0
min_θ  −θ·π^a + F(θ)
```

`F(θ)` se interpreta como el costo social del carbono (Feijoo y Das, 2014), sin forma funcional explícita.

**Calibración.** Sector eléctrico chileno, horizonte **2019–2050**. Presupuesto del sector eléctrico construido desde los NDC (131 MtCO₂e economía-completa a 2030) e interpolando hacia carbono-neutralidad 2050: **398,15 MtCO₂e para 2019–2030 más 532,95 MtCO₂e para 2030–2050, ≈ 930 MtCO₂e**, la *pledge cap*. Cinco escenarios de demanda. Fuente de emisiones: Climate Action Tracker, factores IPCC 2014.

**Solución.** Equilibrio reescrito como MCP vía condiciones KKT, implementado en GAMS y resuelto con PATH.

---

## Estado 1 — memoria de Muñoz (jul 2022)

*Inversión en capacidad de generación eléctrica cuando la atención del planificador es limitada.*

### Cambios respecto del estado 0

| Componente | Estado 0 | Estado 1 |
|---|---|---|
| **Problema del subastador** | restricción probabilística `Pr(θ≥CAP)≤ε` | **eliminada**. En su lugar, costo de precisión `C(P) = c(P−d)²` para `P > d`, tomado de Dewan y Neligh (2020) |
| **Objeto de decisión** | `θ` | `θ` y —según la especificación— el rendimiento `P` |
| **Nº de especificaciones** | 1 | **3**: *profit oriented*, *welfare oriented tasa cuadrada*, *welfare oriented precisión* |
| **Calibración** | *pledge cap* ≈ 930 MtCO₂e | grilla de **10 presupuestos, 100 a 1.000 MtCO₂e**; `π^a = 315,83` en `CAP = 100`; `d = 0,798` desde el error `ε = 0,202` de Andrés et al. (2014) |
| **Costo marginal de precisión `c`** | — | calibrado por especificación: 920.000 M USD (profit), 9.900 M (tasa cuadrada), 4 M (precisión) |
| **Horizonte** | 2019–2050 | 2019–2050 (sin cambio) |
| **Implementación** | GAMS + PATH | GAMS + PATH, **más una traducción a Julia/JuMP** (`code/ModeloAmigoSeparado-*.jl`) |
| **Productores y equilibrio** | — | **sin cambios**; se reutiliza íntegro |

### Qué queda abierto en el estado 1

- En la especificación *profit oriented*, `P` es **parámetro exógeno**: se recorre una grilla de valores y se resuelve el MCP para cada uno. No hay elección endógena de información.
- En la especificación de *precisión*, donde `P` sí es endógeno, la solución se queda en la esquina `P = 0,798` para los diez presupuestos: el planificador nunca adquiere información por encima de la pública.
- Sólo la especificación de *tasa cuadrada* tiene precisión endógena e interior, y su estática comparativa no es monótona.
- El `c` calibrado no tiene interpretación estructural: sale de igualar `π^a` al del estado 0.

---

## Estado 2 — presentación UVigo (jul 2022)

*Cap-and-trade in Energy Capacity Investment when the planner is inattentive*, Cea-Echenique, Feijoo y Muñoz.

No introduce cambios de modelo respecto del estado 1: es su presentación pública. Aporta la **arquitectura expositiva** que después usa el artículo (motivación · literatura · modelo con demanda/productores/subastador/equilibrio · inatención racional · resultados profit y welfare · comentarios finales) y reproduce **exactamente** las tres tablas de resultados de la memoria.

Discrepancia detectada: declara `c = 920M` para el modelo *profit oriented* cuando la memoria calibra 920.000 M USD — error de tres órdenes de magnitud. El `c` del modelo de tasa cuadrada sí coincide.

Sus *Final Remarks* ya anticipan las tres limitaciones del estado 1: respeto de la ley de demanda agregada, relación poco clara con la inatención, y multiplicidad de soluciones con estática comparativa.

---

## Estado 3 — artículo *Inattention raises energy prices* (sep 2026)

`Submissions/EnergyPolicy/inattention_energy_prices.tex`, 15 páginas, clase Elsevier `cas-dc`.

### Cambios respecto del estado 2

| Componente | Estado 2 | Estado 3 |
|---|---|---|
| **Formulación del modelo** | en diapositivas | **escrita formalmente**: horizonte y demanda en dos etapas, conjunto de elección del productor, objetivo y cinco restricciones con variables duales, problema del subastador, definición de equilibrio con las cuatro condiciones de vaciado |
| **Estructura** | — | modelo · inatención racional (las tres especificaciones) · resultados · conclusiones |
| **Notación** | dispersa | `Z := ℝ₊ × ℝ₊^{T×Ω}` como abreviatura; `ξ_i` para el vector de parámetros del productor |
| **Cifras de resultados** | tablas de la memoria | **idénticas, sin modificación** |
| **Limitaciones** | en *Final Remarks* | **declaradas en las conclusiones**: `P` paramétrico en profit oriented, esquina `P=0,798` en precisión, y la función de costo `c(P−d)²` señalada como primitiva inadecuada para un regulador |
| **Bibliografía** | `referencesPres.bib` | `references.bib` + `dirkse_path_1995`, `feijoo_design_2014`, `ferris_complementarity_2000` |

Nada del modelo cambia en este estado: es la formalización del estado 1–2 en formato de artículo. Ver [`AUDITORIA_memoria_VMunoz.md`](AUDITORIA_memoria_VMunoz.md) §6 para el estado del borrador previo (`cas-dc-template.tex`) del que partió.

---

## Estado 4 — memoria de Hurtado (ago 2025)

*Anclaje y ajuste del subastador en un modelo de permisos transables.*

**Es el primer estado que cambia el mecanismo de decisión del planificador, no sólo su parametrización.**

### Cambios respecto del estado 1

| Componente | Estado 1 (Muñoz) | Estado 4 (Hurtado) |
|---|---|---|
| **Marco teórico de la inatención** | costo de precisión de Dewan y Neligh (2020), `c(P−d)²` | **anclaje y ajuste de Gabaix (2019)** |
| **Parámetro de atención** | `P ∈ [d,1]`, rendimiento comprado | `m = σ²_CAP/(σ²_CAP + σ²_ε)`, **razón señal-ruido**; `m=1` información perfecta, `m=0` sin atención |
| **Estructura informacional** | `CAP` conocido, precisión elegida | `CAP ~ N(CAP_d, σ²_CAP)` no observado; señal `CAP_s = CAP + ε`, `ε ~ N(0, σ²_ε)` |
| **Función objetivo del planificador** | `−θπ^a P + c(P−d)²` (y dos variantes welfare) | `V(θ,CAP) = π^a θ − (κ/2)(θ − CAP)²` |
| **Solución del planificador** | tres MCP, con esquinas y multiplicidad | **solución cerrada**: `θ*(CAP_s) = m·CAP_s + (1−m)·CAP_d + π^a/κ` |
| **Nº de ecuaciones MCP** | productores + subastador | **sólo productores**; el subastador se resuelve analíticamente |
| **Horizonte** | 2019–2050 | **2020–2030** (11 años) |
| **Presupuesto** | grilla exógena 100–1.000 MtCO₂e | **valores chilenos vigentes**: `CAP_s = 264,20` MtCO₂e (Plan de Mitigación del Ministerio de Energía, 2024), `CAP_d = 311,01` MtCO₂e (acumulado histórico 11 años desde 2012, SNICHILE), `σ_CAP = 61,86` MtCO₂e |
| **Costo social** | `c` calibrado contra `π^a` | `κ = 64,40 USD/tCO₂e`, **costo social del carbono oficial de Chile 2024** |
| **Estrategia de calibración** | igualar `π^a` al estado 0 en `CAP=100` | **ajustar el mix eléctrico observado de 2024** en once niveles de `m`, escenario `ω=5`, minimizando la distancia absoluta |
| **Resultado empírico** | `π^a` entre el 77% y el 88% del estado 0 | el mix observado es más compatible con **atención baja**; el modelo estima 311,01 MtCO₂e frente a la meta de 264,2 MtCO₂e |
| **Diagnóstico del estado 0** | "el `c` no tiene interpretación estructural" | **la restricción probabilística se satisface con igualdad, `θ = CAP`, y el problema del planificador está indeterminado** — demostrado con dos escenarios de `F(θ)` |

### Qué queda abierto en el estado 4

Detallado en [`AUDITORIA_2_MHurtado.md`](AUDITORIA_2_MHurtado.md) §4.2. En resumen:

- `π^a/κ` vale 2,85–3,09 toneladas sobre una decisión de 3×10⁸: el canal de precio es **numéricamente inerte** y el modelo es, a las unidades calibradas, puro anclaje.
- La penalización `(κ/2)(θ−CAP)²` usa un costo marginal lineal como coeficiente cuadrático: resulta 10⁷ veces mayor que el ingreso.
- La distancia de calibración es **monótona en `m`** (0,2727 en `m=0` a 0,3026 en `m=1`), así que no identifica la atención; y el desajuste de base (~27 puntos) es grande a cualquier `m`.
- La atención no tiene costo: `m` está dado por `σ_ε`, no elegido. Es la simetría inversa del estado 1, que tiene costo de atención pero no identificación.

---

## Estado 5 — presentación de defensa de Hurtado (2026)

`docs/Presentations/HurtadoDefensa2026/JMHL_presentation.tex`, 47 páginas, beamer + LuaLaTeX.

No cambia el modelo. Aporta:

- La **secuencia narrativa** del estado 4: contaminación y contexto histórico · política climática en Chile · el sistema de Amigo et al. · el CAP como presupuesto ambiental · limitaciones · objetivo · simbología · planificador con inatención conductual · parámetros para Chile · calibración de la atención · incertidumbre por nivel de atención · costo social del carbono · matriz 2030 · conclusión, con anexos que reconstruyen la genealogía completa (planificador de Amigo, escenarios de `F(θ)`, los modelos profit y welfare de Muñoz, el modelo conductual).
- Una **bibliografía institucional chilena actual** de 26 entradas (Plan de Mitigación 2024, anteproyecto MMA 2025, Reporte del Coordinador Eléctrico Nacional 2024, Leyes 20.780 y 21.455, ICAP) que no existe en ninguna otra bibliografía del repositorio.

---

## Resumen de la trayectoria

El planificador ha pasado por tres formas en cinco años:

1. **Estado 0 (2021)** — restricción probabilística. El planificador emite exactamente el presupuesto; su problema es formalmente correcto pero vacío.
2. **Estados 1–3 (2022–2026)** — costo de precisión. El planificador *paga* por atención, pero el costo es una primitiva prestada y la atención no está identificada: en dos de las tres especificaciones ni siquiera es una variable interior.
3. **Estados 4–5 (2025–2026)** — anclaje y ajuste. La atención *está* identificada, con parámetros chilenos verificables y solución cerrada, pero es un dato del entorno y no una decisión: el planificador no paga por ella.

Los dos últimos estados son mitades complementarias del mismo problema. La combinación —atención con costo *y* con identificación empírica— es exactamente lo que la propia conclusión del estado 4 propone como línea futura, y es el contenido natural del próximo artículo. El plan está en [`PLAN_ARTICULO.md`](PLAN_ARTICULO.md).
