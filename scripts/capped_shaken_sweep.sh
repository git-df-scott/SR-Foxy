#!/bin/bash
# Per-diagram wall-clock cap for band_search_shaken.py.
# The plain script has no per-diagram cap, so a single hard diagram stalls the
# whole sweep and the run yields nothing at all.  One diagram per invocation
# under `timeout` keeps every diagram bounded and independently recorded.
KNOT="$1"; OUTDIR="$2"; NDIAG="$3"; CAP="$4"; BANDS="$5"; LEN="$6"; SEED0="$7"
P=/home/user/knot-venv/bin/python
mkdir -p "$OUTDIR"
for i in $(seq 0 $((NDIAG-1))); do
  out="$OUTDIR/diagram_$i.json"
  [ -f "$out" ] && continue
  timeout "$CAP" $P scripts/band_search_shaken.py "$KNOT" 2 25 "$BANDS" 2 "$LEN" shortest "$out" $((SEED0+i)) \
    > /dev/null 2>&1
  if [ -f "$out" ]; then
    if grep -q '"unknot_found": true' "$out"; then echo "*** RIBBON CERTIFICATE *** $KNOT diagram $i"; fi
    echo "diagram $i: completed"
  else
    echo "diagram $i: CAPPED_UNKNOWN (${CAP}s)"
  fi
done
echo "SWEEP DONE $KNOT"
