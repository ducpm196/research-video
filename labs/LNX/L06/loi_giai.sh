#!/usr/bin/env bash
set -euo pipefail
W=$(mktemp -d)
trap 'rm -rf "$W"' EXIT
umask 077
printf "SECRET_KEY=demo_only_v1\n" > "$W/.env"
chmod 600 "$W/.env"
set -a; source "$W/.env"; set +a
ok=$(( ${#SECRET_KEY} > 0 ? 1 : 0 ))
echo "env_loaded=$ok"
echo "cron_per_hour=$((60 / 5))"
echo "cron_per_day=$(( (60 / 5) * 24 ))"
