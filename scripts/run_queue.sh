#!/bin/bash
# Sequential queue of shaken band searches on the r=0 RBG knots (both sides of each pair).
cd /home/user/SR-Foxy
for k in MP_KB_0_0_0_1_2_-1 MP_KG_0_0_0_1_2_-1 MP_KB_0_0_-2_0_0_1 MP_KG_0_0_-2_0_0_1 MP_KB_0_0_0_-1_2_1 MP_KG_0_0_0_-1_2_1; do
  python3 scripts/band_search_shaken.py data/knots/$k.json 12 25 2 2 8 shortest results/RBG_${k}_shaken12_bands2_detached.json 5 > results/logs/RBG_$k.log 2>&1
done
echo QUEUE_DONE >> results/logs/RBG_queue.log
