#!/usr/bin/env bash
set -euo pipefail
W=$(mktemp -d)
trap 'rm -rf "$W"' EXIT
touch "$W/sec.key" "$W/app.sh"
chmod 755 "$W/app.sh" && chmod 600 "$W/sec.key"
awk 'BEGIN{
  split("rwxr-xr-x rw-r----- rw-------", a, " ");
  for(k=1;k<=3;k++){ s=a[k]; o="";
    for(g=0;g<3;g++){ v=0;
      if(substr(s,g*3+1,1)=="r") v+=4;
      if(substr(s,g*3+2,1)=="w") v+=2;
      if(substr(s,g*3+3,1)=="x") v+=1; o=o v; }
    printf "%s=%s\n", s, o; }
}'
