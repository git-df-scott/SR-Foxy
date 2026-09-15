#!/usr/bin/env bash
# Teichner partner sweep on D_{0,1}, one partner at a time.
#
# Sequential by design: this box has 4 cores and the band search is CPU-bound,
# so running the partners in parallel lowers total throughput and risks the
# memory pressure that already killed one job today.
#
# Partner order is ascending in crossing number of D_{0,1} # J, because the
# measured cost law is grossly superlinear (4.21 h at 31, 7.96 h at 33, >12 h
# at 35). Cheapest new coverage first.
#
# Dial choice per partner:
#   8_8   - its box is COMPLETE at paths=shortest, so 'simple' is the new volume.
#   rest  - never completed at ANY setting, so 'shortest' is the cheaper and
#           still entirely new coverage. Widening a box nobody has closed once
#           would be paying 75x for a box that has never been shut.
#
# NOT run, deliberately: 8_9, 8_20, 9_27. They are fibered. Adding a fibered
# ribbon J leaves K_0 and -K_1 unpaired among the fibered prime summands, so
# Miyazaki still gives non-ribbon for the sum and NO certificate can exist.
# Running them would burn hours on a box proved empty in advance.
set -u
SP=${TEICHNER_OUT:-/tmp/teichner}   # override with TEICHNER_OUT
export MAMBA_ROOT_PREFIX=/tmp/mamba
MM=/tmp/bin/micromamba
K=/home/user/SR-Foxy/data/knots/AbeTagami_D_0_1.json
OUT=$SP/teichner
mkdir -p "$OUT"

run_one() {
  local J=$1 PATHS=$2 BANDS=$3 LEN=$4
  local tag="D01_${J}_${PATHS}_b${BANDS}_l${LEN}"
  local started ended code
  started=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  echo "[$(date -u +%H:%M:%SZ)] START $tag" >>"$OUT/queue.log"
  TEICHNER_J="$J" TEICHNER_PATHS="$PATHS" \
    "$MM" run -n sage sage /home/user/SR-Foxy/scripts/teichner_certify.py \
      "$OUT/$tag.json" "$BANDS" "$LEN" "$K" >"$OUT/$tag.log" 2>&1
  code=$?
  ended=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  # An exit code is not a result. A finished search with no certificate is
  # coverage; anything else is an interrupted search, which supports no
  # conclusion at all. Record which, and never let the two blur.
  printf '{"tag":"%s","partner":"%s","paths":"%s","bands":%s,"max_band_len":%s,"started":"%s","ended":"%s","exit_code":%d,"state":"%s","caution":"a non-completed search is NOT coverage of its box and supports no conclusion"}\n' \
    "$tag" "$J" "$PATHS" "$BANDS" "$LEN" "$started" "$ended" "$code" \
    "$([ $code -eq 0 ] && echo completed || echo interrupted)" >>"$OUT/queue_status.jsonl"
  echo "[$(date -u +%H:%M:%SZ)] END   $tag exit=$code" >>"$OUT/queue.log"
}

run_one 8_8   simple   2 4
run_one 9_41  shortest 2 5
run_one 9_46  shortest 2 5
run_one 10_3  shortest 2 5
run_one 10_22 shortest 2 5
run_one 10_87 shortest 2 5
echo "PARTNER_QUEUE_DONE $(date -u +%Y-%m-%dT%H:%M:%SZ)" >>"$OUT/queue.log"
