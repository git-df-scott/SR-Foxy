#!/usr/bin/env bash
# Run one KnotJob invariant and record HOW it ended, not just what it printed.
#
# A long KnotJob run on a large diagram can vanish with an empty log: the JVM is
# killed before it writes anything, so "no output" and "still working" look the
# same from outside. Worse, a watcher built on `pgrep -f KnotJob.jar` matches its
# own command line and concludes the job is alive forever. This wrapper removes
# both failure modes by writing a sidecar status file with the pid, the exit
# code and the wall time, so an aborted run is recorded as an abort and can
# never be read as a computed zero.
#
# usage: run_knotjob_watched.sh <java> <jar> <input.txt> <flag> <outdir> [heap]
set -u
java=$1; jar=$2; input=$3; flag=$4; outdir=$5; heap=${6:--Xmx12g}
mkdir -p "$outdir"
base=$(basename "$input" .txt)
log="$outdir/${base}${flag}.log"
status="$outdir/${base}${flag}.status.json"

start_epoch=$(date -u +%s)
start_iso=$(date -u +%Y-%m-%dT%H:%M:%SZ)
"$java" "$heap" -Djava.awt.headless=true -jar "$jar" "$input" "$flag" -nf >"$log" 2>&1 &
pid=$!
printf '{"state":"running","pid":%d,"started":"%s","heap":"%s","flag":"%s","log":"%s"}\n' \
  "$pid" "$start_iso" "$heap" "$flag" "$log" >"$status"

# If THIS script is killed (a timeout, a reclaimed container, an operator ^C)
# the status file would otherwise stay "running" forever - the same silent-death
# blind spot the wrapper exists to remove. Record the interruption and take the
# child down with us so no orphan JVM keeps holding memory.
on_signal() {
  printf '{"state":"wrapper_interrupted","pid":%d,"started":"%s","ended":"%s","seconds":%d,"log_bytes":%d,"heap":"%s","flag":"%s","log":"%s","caution":"the wrapper was killed; NO VALUE was computed and none may be inferred"}\n' \
    "$pid" "$start_iso" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
    "$(( $(date -u +%s) - start_epoch ))" "$(wc -c <"$log")" "$heap" "$flag" "$log" >"$status"
  kill "$pid" 2>/dev/null
  exit 1
}
trap on_signal TERM INT HUP

wait "$pid"; code=$?
seconds=$(( $(date -u +%s) - start_epoch ))
bytes=$(wc -c <"$log")

# A nonzero exit or a signal death with an empty log is a RESOURCE FAILURE.
# It is never an invariant value. Signals arrive as 128+n; 137 is SIGKILL,
# which is what a kernel OOM kill looks like from here.
if [ "$code" -eq 0 ] && [ "$bytes" -gt 0 ]; then
  state=finished
elif grep -q "OutOfMemoryError" "$log" 2>/dev/null; then
  # The JVM exhausted its own heap and said so. Distinguishable from an
  # external kill, which leaves the log empty.
  state=java_heap_exhausted
elif [ "$code" -ge 128 ]; then
  state=killed_by_signal
else
  state=resource_failure
fi

printf '{"state":"%s","pid":%d,"exit_code":%d,"signal":%s,"started":"%s","ended":"%s","seconds":%d,"log_bytes":%d,"heap":"%s","flag":"%s","log":"%s","caution":"state other than finished means NO VALUE was computed; do not record it as zero"}\n' \
  "$state" "$pid" "$code" "$([ "$code" -ge 128 ] && echo $((code-128)) || echo null)" \
  "$start_iso" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$seconds" "$bytes" "$heap" "$flag" "$log" >"$status"

cat "$status"
[ "$state" = finished ] || exit 1
