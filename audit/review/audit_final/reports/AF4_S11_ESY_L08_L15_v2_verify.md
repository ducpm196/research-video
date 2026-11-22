# Báo cáo kiểm định độc lập AF4 v2 — Stage 11 ESY (L08–L15)

**Verdict: `NO-GO`** *(chỉ đọc)*

- `tools/lv.py lint` (`L08..L15`): **8/8 PASS** (0 FAIL, 0 WARN; 9.76–13.83p, L15 20.29p).
- `audit/esy/verify_esy.py`: **72/72 PASS**; `screen_code` **PASS**; `loi_giai.py == mong_doi.txt` **8/8 PASS**; `layout_ESY.tsv` **0 dòng**; `P9 = 2` đạt **8/8**; không lộ code/output trước `pause: 30` **8/8**.
- Bản dựng MP4 (`out/esy/L08..L15`): **PENDING REBUILD**.

## Bảng tổng hợp & lỗi cần sửa (L08–L15)
| Bài | Phút | P1 | P8 | P9 | `covers:` | Lỗi chính |
|---|---:|---:|---:|---:|---|---|
| **L08** | 12.14 | 1 | 2 | 2 | Sai obj 1 (`sym`), 3 (`example`) | `SDA/SCL`, `ACK` chưa mở nghĩa; `practice#2` dư `dict(...)` |
| **L09** | 13.73 | 0 | 1 | 2 | Sai obj 2 (`rta`/`example`) | `de.md` thiếu chữ số thập phân `U` (3) & `LL_bound` (4, `0.7798`); P1 thiếu `n`, `ngắt`, `CPU`, `RTA`, `(1, 5)`, `for c, p`, `_`, dư `dict(...)` |
| **L10** | 13.83 | 0 | 1 | 2 | Đúng | `de.md` trùng số ví dụ `(2,4),(3,6)` @ `12ms`; P1 `EDF`, `ngắt`, `False/True`, `key=`, `a,b,c=`, nested tuple, `if ready:`, `>`, dư `dict(...)` |
| **L11** | 11.83 | 0 | 1 | 2 | Sai obj 3 (`pitfalls`/`quiz`/`queue`) | `de.md` thiếu chú thích `{msg!r}` (`decoded='TEMP:42\n'`); P1 C `queue#0`, `RTOS`, `MCU`, `ISR`, `b'...'`, `bytes()`, `.decode()`, `!r`, `<`, `a, b =`, `_`, dư `set()` |
| **L12** | 10.31 | 0 | 2 | 2 | Đúng | P1 `0x`, `watchdog timer`, `reset`, `[0xA5]*16`, `(50,75,110,60)`, `sum(... if ...)`, `>`, dư `set()` |
| **L13** | 9.76 | 2 | 1 | 2 | Yếu obj 3 (`example`) | `de.md` thiếu làm tròn `avg_ma` (4 chữ số) & `battery_days` (nguyên `:.0f`); dư `dict(...)` |
| **L14** | 10.99 | 0 | 2 | 2 | Sai obj 2 (`boot`), obj 3 (`example`) | P1 `CRC`, `SHA-256`, `b'...'`, `hashlib.sha256()`, `and`, `True`; thừa `.encode().hexdigest()` & `set()` |
| **L15** | 20.29 | 1 | 2 | 2 | Sai obj 3 (`quiz`) | `practice` thiếu `>`, `print(a, b)`, dư `dict(...)` |
