# Independent Verification Report — AF4 LNX (`L00–L09`)

**Verifier:** Read-only independent verifier (`0a20a258-9823-498c-89a9-d513b4b5acf2`)
**Scope:** `lessons/lnx/L00–L09`, `out/LNX/L00–L09/`, `labs/LNX/L00–L09/`, `curriculum/lnx.yaml`, `audit/review/screen_code/LNX.yaml`
**Verdict:** **NO-GO (REQUIRES FIX & REBUILD)** — Video/SRT/ASR technical pipeline is clean (`10/10` MP4 verified, `0` spec_sha stale, `10/10` SRT exact match, `0` unreviewed ASR flags), **but 6 MUST defects** must be fixed before sign-off.

## 1. MUST Items (6 Blocking Defects)
1. **MUST-1 (`L00`):** `labs/LNX/L00/loi_giai.sh` ran `ln -s` on Windows Git Bash (without Docker/nativestrict symlink), copying instead of symlinking, producing `sym_failed=0` in `mong_doi.txt` and `practice#1` (`00046.png`) while `de.md` expects `sym_failed=1`.
2. **MUST-2 (`L05`):** `labs/LNX/L05/loi_giai.sh` matched a `#` comment in `/etc/hosts`, printing `loopback_only=#` in `mong_doi.txt` and `practice#1` (`00039.png`) instead of `loopback_only=127.0.0.1` (and didn't bind a socket as `de.md` asks).
3. **MUST-3 (`L00, L02, L03`):** `check_xref.py --course LNX` flagged `"FND"` references in `prereq#0` (`L00, L02, L03`) and `NET=`/`$NET` (`L08`).
4. **MUST-4 (`L00, L08, L09`):** `af2_kit.svg_arrow` always drew a right-pointing arrowhead even on left (`L00 00016.png`) and downward (`L08 00010.png`) arrows; `L09` (`00010.png`) `"kiểm mỗi 2s"` overlapped box borders.
5. **MUST-5 (`L04`):** `example#2` (`00021.png`) displays `data_kb=4` (4 KB directory block) while `say` states `"bằng không ki-lô-bai"`.
6. **MUST-6 (`L05`):** Objective 2 promises `curl`/open-port inspection (`ss`), while `example#0` glosses unused `socket.bind` and neither `curl` nor `ss` is demonstrated in `example`/`check`.

## 2. SHOULD & P1/P8/P9 Summary (`L00–L09`)
- **P1=2:** `1/10` (`L04`) — gloss `MSYS_NO_PATHCONV=1`, `POSIX`, `PID`, `SSH`, `OOMKill`, `FD`, `sort`, `nsswitch`, `umask 077`, `MiB`/`MB`, `reverse proxy`, `getent`, `Redis`/`redis-cli`/`+PONG` cleanly inline!
- **P8=2:** `4/10` (3 fails `L00, L04, L05`; 3 partial `L02, L03, L06`). Align `L01` & `L09` `loi_giai.sh` with `de.md` (actual `chmod` / config inspection instead of hardcoded echo).
- **P9=2:** `10/10` (polish `L07` row-1 `125 MB` vs `1 200 / 12 000 MB`).
- **SHOULD:** Move `"Giam-mồ"` / `"S S H"` / phonetic spellings out of `show` into `lexicon_vi.LNX.yaml`; fix `L06` tight grey box & wrapped `*/5`; set `curriculum/lnx.yaml` `status: active`.
