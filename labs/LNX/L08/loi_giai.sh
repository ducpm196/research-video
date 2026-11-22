#!/usr/bin/env bash
set -euo pipefail
map="8080:80"
hp=${map%%:*}
cp=${map##*:}
echo "host_port=$hp container_port=$cp"
echo "volume_persists=1"
echo "retained_rows=500"
