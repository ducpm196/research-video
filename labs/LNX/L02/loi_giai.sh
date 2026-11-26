#!/usr/bin/env bash
set -u
exec < <(tr -d '\r')
read -r GRACE SIG
bash -c "trap 'echo graceful=1; exit $GRACE' TERM; while :; do sleep 0.05; done" &
p1=$!
sleep 0.15
kill -TERM "$p1"
wait "$p1" 2>/dev/null
echo "term_exit=$?"
echo "kill_exit=$((128 + SIG))"
