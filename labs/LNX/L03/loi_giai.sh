#!/usr/bin/env bash
set -euo pipefail
exec < <(tr -d '\r')
read -r TOT C500 C503 MOUT MERR
W=$(mktemp -d)
trap 'rm -rf "$W"' EXIT
cd "$W"
(echo "$MOUT"; echo "$MERR" >&2) > o.txt 2> e.txt
awk -v tot="$TOT" -v c500="$C500" -v c503="$C503" 'BEGIN{
  for(i=1;i<=tot;i++){
    if(i<=c500) print "500";
    else if(i<=c500+c503) print "503";
    else print "200";
  }
}' > log.txt
c=$(grep -cE '^5[0-9]{2}$' log.txt || true)
[ "$(cat o.txt)" = "$MOUT" ] && so=1 || so=0
[ "$(cat e.txt)" = "$MERR" ] && se=1 || se=0
echo "stdout_ok=$so"
echo "stderr_ok=$se"
echo "err_5xx=$c"
