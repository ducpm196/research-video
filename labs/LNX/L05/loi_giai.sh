#!/usr/bin/env bash
set -euo pipefail
PY=python
command -v python3 >/dev/null 2>&1 && python3 --version >/dev/null 2>&1 && PY=python3
"$PY" -c "
import os, socket
for k, host in (('loopback_only', '127.0.0.1'), ('all_ifaces', '0.0.0.0')):
    s = socket.socket(); s.bind((host, 0)); print(f'{k}={s.getsockname()[0]}'); s.close()
cfg = open('/etc/nsswitch.conf').read() if os.path.exists('/etc/nsswitch.conf') else ''
hl = next((l for l in cfg.splitlines() if l.startswith('hosts:')), '')
ok = ('files' in hl and ('dns' not in hl or hl.index('files') < hl.index('dns'))) if hl else ('127.0.0.1' in socket.gethostbyname_ex('localhost')[2])
print(f'hosts_before_dns={int(ok)}')
"
