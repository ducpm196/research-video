#!/usr/bin/env bash
set -euo pipefail
exec < <(tr -d '\r')
read -r KNAME KVAL STEP
W=$(mktemp -d)
trap 'rm -rf "$W"' EXIT
umask 077
printf "%s=%s\n" "$KNAME" "$KVAL" > "$W/.env"
chmod 600 "$W/.env"
set -a; source "$W/.env"; set +a
loaded_val="${!KNAME:-}"
ok=$(( ${#loaded_val} > 0 ? 1 : 0 ))
cph=$((60 / STEP))
echo "env_loaded=$ok"
echo "cron_per_hour=$cph"
echo "cron_per_day=$((cph * 24))"
