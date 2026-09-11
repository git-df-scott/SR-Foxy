#!/bin/bash
# Ribbon searches on the r=0 RBG knots that lie OUTSIDE the Dunfield-Gong census.
#
# GHMR list three r=0 pairs, but K_{B/G}(0,0,0,1,2,-1) and K_{B/G}(0,0,-2,0,0,1)
# are the SAME pair -- identical isometry signatures on both sides, verified
# 2026-09-11 -- and that pair simplifies to 19 crossings, prime and hyperbolic.
# It therefore lies inside Dunfield-Gong's census of all prime knots with at most
# 19 crossings, which they already searched to 4 bands with ~100 CPU-years.
# Re-searching it here would be redundant and weaker.
#
# The only genuinely unsearched r=0 knots are the 27- and 24-crossing pair below.
cd /home/user/SR-Foxy
for k in MP_KG_0_0_0_-1_2_1 MP_KB_0_0_0_-1_2_1; do
  python3 scripts/band_search_shaken.py data/knots/$k.json 15 25 2 2 8 shortest \
      results/RBG_${k}_shaken15_bands2_detached.json 7 > results/logs/RBG_$k.log 2>&1
done
echo QUEUE_DONE >> results/logs/RBG_queue.log
