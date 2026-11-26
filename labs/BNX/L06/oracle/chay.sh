#!/usr/bin/env bash
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MSYS_NO_PATHCONV=1 docker exec -i bnx-ora sqlplus -s -L bnx/bnx_pass@//localhost/FREEPDB1 < "$DIR/thu.sql"
