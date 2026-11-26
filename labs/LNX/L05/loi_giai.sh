#!/usr/bin/env bash
set -euo pipefail
exec < <(tr -d '\r')
read -r L1 H1
read -r L2 H2
PY=python
command -v python3 >/dev/null 2>&1 && python3 --version >/dev/null 2>&1 && PY=python3
"$PY" -c "
import os, socket, sys
for k, host in ((sys.argv[1], sys.argv[2]), (sys.argv[3], sys.argv[4])):
    s = socket.socket(); s.bind((host, 0)); print(f'{k}={s.getsockname()[0]}'); s.close()
cfg = open('/etc/nsswitch.conf').read() if os.path.exists('/etc/nsswitch.conf') else ''
hl = next((l for l in cfg.splitlines() if l.startswith('hosts:')), '')
ok = ('files' in hl and ('dns' not in hl or hl.index('files') < hl.index('dns'))) if hl else ('127.0.0.1' in socket.gethostbyname_ex('localhost')[2])
print(f'hosts_before_dns={int(ok)}')
" "$L1" "$H1" "$L2" "$H2"
