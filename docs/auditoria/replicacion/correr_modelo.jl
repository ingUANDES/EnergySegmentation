#!/usr/bin/env julia
# Corre un modelo del crash course (repo ingUANDES/MCP) sin editar sus scripts.
#
# Los scripts fijan sus parametros por asignacion literal y evaluan un solo punto.
# Este envoltorio lee el texto del script, sustituye solo las lineas de parametros y
# la de la licencia, y lo evalua. Toda sustitucion queda registrada en el CSV de salida,
# de modo que el informe puede declarar exactamente con que valores se corrio.
#
#   julia auditoria/correr_modelo.jl <modelo> <salida.csv> [P=..] [cm=..] [CAP=..]
#
# modelo: amigo | profit_oriented | quadratic_rate | precision

using JuMP, DataFrames, CSV, Printf

const RUTAS = Dict(
    "amigo"           => "mcp/scripts/amigo/amigo.jl",
    "profit_oriented" => "mcp/scripts/innatention/profit_oriented/profit_oriented.jl",
    "quadratic_rate"  => "mcp/scripts/innatention/social_benefit/quadratic_rate.jl",
    "precision"       => "mcp/scripts/innatention/social_benefit/precision.jl",
)

modelo = ARGS[1]
salida = ARGS[2]
ov = Dict{String,String}()
for a in ARGS[3:end]
    k, v = split(a, "=", limit=2); ov[k] = v
end

ruta = RUTAS[modelo]
src  = read(ruta, String)
dir  = dirname(ruta)
sust = String[]

# 1. licencia: fuera del codigo, se toma de PATH_LICENSE_STRING
src2 = replace(src, r"PATHSolver\.c_api_License_SetString\(\"[^\"]*\"\)" =>
                    "PATHSolver.c_api_License_SetString(ENV[\"PATH_LICENSE_STRING\"])")
src2 != src && push!(sust, "licencia<-PATH_LICENSE_STRING")
src = src2

# 2. cm (costo marginal de precision). En profit_oriented esta comentado y hay que insertarlo.
if haskey(ov, "cm")
    if occursin(r"(?m)^cm\s*=", src)
        src = replace(src, r"(?m)^cm\s*=.*$" => "cm = $(ov["cm"])")
        push!(sust, "cm=$(ov["cm"]) (reemplaza el del script)")
    else
        src = replace(src, r"(?m)^# cm = .*$" => "cm = $(ov["cm"])")
        push!(sust, "cm=$(ov["cm"]) (el script no lo define: descomentado e inyectado)")
    end
end

# 3. Performance
if haskey(ov, "P") && occursin(r"(?m)^Performance\s*=", src)
    src = replace(src, r"(?m)^Performance\s*=.*$" => "Performance = $(ov["P"])")
    push!(sust, "Performance=$(ov["P"])")
end

# 4. CAP: 'mean' se define en parameters.jl, asi que se reasigna despues del include
if haskey(ov, "CAP")
    m = match(r"(?m)^include\(\"[^\"]*parameters\.jl\"\)$", src)
    @assert m !== nothing "no encontre el include de parameters.jl en $ruta"
    src = replace(src, m.match => m.match * "\nmean = $(ov["CAP"])")
    push!(sust, "mean=$(ov["CAP"])")
end

# 5. todo include relativo del script se reescribe a una ruta resuelta desde el cwd:
#    include_string no fija @__DIR__ de forma fiable para la resolucion relativa.
src = replace(src, r"include\(\"([^\"]+)\"\)" => m -> begin
    rel = match(r"include\(\"([^\"]+)\"\)", m).captures[1]
    "include(\"" * abspath(normpath(joinpath(dir, rel))) * "\")"
end)

# 6. opciones del solver. El unico cambio de metodo respecto de los scripts: la
#    tolerancia de convergencia por defecto (1e-6) deja el modelo base en un punto
#    con pi^a = 276,88; con 1e-8 converge al 315,8245 que el articulo declara. No se
#    toca ninguna ecuacion, solo el criterio de parada.
const OPCIONES = [
    ("cumulative_iteration_limit", "10_000_000"),
    ("major_iteration_limit", "10_000"),
    ("minor_iteration_limit", "100_000"),
    ("convergence_tolerance", "1e-8"),
    ("restart_limit", "10"),
    ("output", "\"no\""),
]
let m = match(r"(?m)^model = Model\(PATHSolver\.Optimizer\)$", src)
    @assert m !== nothing "no encontre la creacion del modelo en $ruta"
    inyec = m.match * "\n" * join(["set_optimizer_attribute(model, \"$k\", $v)" for (k,v) in OPCIONES], "\n")
    global src = replace(src, m.match => inyec)
end
push!(sust, "convergence_tolerance=1e-8 y limites de iteracion ampliados")

@assert haskey(ENV, "PATH_LICENSE_STRING") "falta PATH_LICENSE_STRING en el entorno"

t0 = time()
M = Module(:Corrida)
Core.eval(M, :(using JuMP, DataFrames))
# un Module creado en tiempo de ejecucion no trae `include`: se lo damos
Core.eval(M, :(include(p) = Base.include(@__MODULE__, p)))
function evaluar(M, src, ruta)
    try
        include_string(M, src, ruta); return (true, "")
    catch e
        return (false, replace(sprint(showerror, e), "\n" => " ")[1:min(end,400)])
    end
end
ok, err = evaluar(M, src, ruta)
ok || @warn "la corrida fallo" err
seg = time() - t0

leer(nombre) = try
    v = Core.eval(M, Meta.parse("value($nombre)")); isa(v, Number) ? Float64(v) : missing
catch; missing end
leer_est() = try string(Core.eval(M, :(termination_status(model)))) catch; "sin_modelo" end

fila = DataFrame(
    modelo = modelo,
    P = get(ov, "P", ""), cm = get(ov, "cm", ""), CAP = get(ov, "CAP", ""),
    estado = ok ? leer_est() : "ERROR",
    estado_crudo = ok ? (try string(Core.eval(M, :(raw_status(model)))) catch; "" end) : "",
    theta = leer("theta"), pi_a = leer("pi_a"), eta = leer("eta"),
    r_p = leer("r_p"),
    pi_d_2018 = try Float64(Core.eval(M, :(value(pi_d[2018])))) catch; missing end,
    theta_sobre_CAP = (haskey(ov,"CAP") && leer("theta") !== missing) ? leer("theta")/parse(Float64, ov["CAP"]) : missing,
    segundos = round(seg, digits=1),
    sustituciones = join(sust, "; "),
    error = err,
)
if isfile(salida)
    CSV.write(salida, fila; append=true)
else
    CSV.write(salida, fila)
end
println(first(fila, 1))
