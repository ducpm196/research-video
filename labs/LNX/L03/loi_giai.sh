#!/usr/bin/env bash
set -euo pipefail
W=$(mktemp -d)
trap 'rm -rf "$W"' EXIT
cd "$W"
(echo 'OK'; echo 'ERR' >&2) > o.txt 2> e.txt
awk 'BEGIN{for(i=1;i<=100;i++){if(i<=12)print "500"; else if(i<=15)print "503"; else print "200"}}' > log.txt
c=$(grep -cE '^5[0-9]{2}$' log.txt)
[ "$(cat o.txt)" = "OK" ] && so=1 || so=0
[ "$(cat e.txt)" = "ERR" ] && se=1 || se=0
echo "stdout_ok=$so"
echo "stderr_ok=$se"
echo "err_5xx=$c"
