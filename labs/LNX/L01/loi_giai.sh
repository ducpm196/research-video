#!/usr/bin/env bash
set -euo pipefail
exec < <(tr -d '\r')
awk '{
  for(k=1;k<=NF;k++){ s=$k; o="";
    for(g=0;g<3;g++){ v=0;
      if(substr(s,g*3+1,1)=="r") v+=4;
      if(substr(s,g*3+2,1)=="w") v+=2;
      if(substr(s,g*3+3,1)=="x") v+=1; o=o v; }
    printf "%s=%s\n", s, o; }
}'
