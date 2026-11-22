# WP-AF4-3 Stage 7 Verification Report — Course `SDP` (`L00–L15`)

**Verifier:** `b3830b93` (`WP-AF4-3 Stage 7 SDP Verifier`, read-only)  
**Verdict: `NO-GO`** (`MUST = 1`: `SDP L13` off-topic lab; `P1 = 93.8%`, `P8 = 100%` tech sync, `P9 = 93.8%`)

---

## 1. Observed Results (`L00–L15`, 16 lessons)
- `lv.py curriculum` (`18/18 0 lỗi`), `lv.py lint` & `lv.py verify` (`16/16`), `screen_code` (`56 khối — PASS 57 / 0 FAIL`), scene `checks` (`176/176`), `SRT == say` (`16/16`), `ASR` (`16/16 0/0`), `loi_giai.py == mong_doi.txt` (`16/16`), `L05` & `L07` genuine non-hardcoded solutions, `30/30` PNGs crisp.
- **MUST-1 (`SDP L13`):** `labs/SDP/L13/*` and `lessons/sdp/L13_mui_ma_tai_cau_truc.yaml` `practice` (`upgrade_sdp.py` L189–200) teach bounded queue / backpressure (`queued_end=9`, `consumed_total=8`, `rejected_backpressure=7`) instead of **Mùi mã và tái cấu trúc an toàn** (`thue`/`phi_giao`, equivalence testing + catching refactor regression).
- **Non-blocking SHOULD:** gloss `MB` (`L09`), `Instance` (`L08/de.md`), clarify `L11/de.md` 4-state set.
