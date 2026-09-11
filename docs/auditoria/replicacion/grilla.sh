#!/bin/bash
# Corre las grillas que reportan las tablas del articulo. Un proceso por punto:
# los scripts dejan estado global y un MCP es sensible al punto de partida, asi que
# cada corrida debe partir limpia.
set -u
export JULIA_DEPOT_PATH="$PWD/.julia" PATH_LICENSE_STRING="$(cat .path_license)"
OUT=auditoria/corridas; mkdir -p $OUT; rm -f $OUT/*.csv
J=auditoria/correr_modelo.jl

# Tabla efectopenthetapia: efecto de P con CAP = 100 MtCO2e
for P in 0.798 0.8 0.85 0.9 0.95 0.99 1; do
  for C in 9.2e11 9.2e8; do
    echo "julia $J profit_oriented $OUT/po_P${P}_c${C}.csv P=$P cm=$C CAP=1e8"
  done
done
# Tabla efectocapthetapia: efecto del CAP con P = 0.8
for K in 1 2 3 4 5 6 7 8 9 10; do
  CAP=$(python3 -c "print(f'{$K*1e8:.6g}')")
  for C in 9.2e11 9.2e8; do
    echo "julia $J profit_oriented $OUT/po_CAP${K}_c${C}.csv P=0.8 cm=$C CAP=$CAP"
  done
  echo "julia $J quadratic_rate $OUT/tc_CAP${K}.csv cm=9.9e9 CAP=$CAP"
  echo "julia $J precision      $OUT/pm_CAP${K}.csv cm=4e6   CAP=$CAP"
done
