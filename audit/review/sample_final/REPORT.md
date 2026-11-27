# Báo cáo kiểm mẫu đối chứng cuối `WP-7` (hạt giống `20261127`)

- **Thời điểm:** `2026-11-27`
- **Phương pháp (`plan_AF5` mục 6, `WP-7`):** Lấy mẫu phân tầng theo 11 chặng học (`S01..S11` từ `audit/review/learn_start/pack.py`), mỗi chặng 6 bài (`seed=20261127`), tổng **`66` bài** (`66 >= 60`).
- **Kết quả tổng hợp:** **`66 / 66` bài đạt `0 MUST`** (`0` bài rớt chuẩn).
  - Khớp `sha16` YAML hiện hành ↔ `audit/review/read_af5/<C>/<Lxx>.md`: **`66 / 66`**
  - `tools/lv.py lint`: **`66 / 66` đạt `0 FAIL`**
  - `audit/review/boiler_deny.txt`: **`66 / 66` có `0` chuỗi trùng**
  - Khung hình (`out/<C>/<Lxx>/frames/`): đã xem `≥ 2` khung hình/bài (`≥ 132` PNG) — bố cục, SVG, KaTeX, mã hiển thị sạch, khớp phụ đề.
  - Lab thực hành: tất cả lab nhẹ (`63` bài chạy trực tiếp/SQL/giấy bút `--giay`) chạy trong thư mục tạm khớp 100% `mong_doi.txt` và toàn bộ `ca_an/` (chống in cứng); 3 dự án Maven `SPB` đã kiểm đối chiếu mã & test (`SPB` đạt `14/14 PASS` khi chạy `verify_spb.py` độc lập).
  - Hạn chế mở theo quy ước (`BN-08`): chất lượng phát âm ở bài `S01..S11` mới kiểm bằng máy (ASR + tốc độ đọc), **tai người chưa nghe (`NOT_VERIFIED`)**.

## Tổng hợp theo từng phần báo cáo

| Phần | Chặng | Số bài | `sha16` khớp `read_af5` | `lv.py lint` `0 FAIL` | `MUST` | Tệp chi tiết |
|---|---|---|---|---|---|---|
| 1 | `S01..S04` (`FND, JV2, PRJ, PYT, BNK, BEP, BNX, SPB, ACB, INT`) | 24 | 24 / 24 | 24 / 24 | **0** | [part_s01_s04.md](part_s01_s04.md) |
| 2 | `S05..S08` (`CS112, CS115, DMS, CPR, LNX, OSY, PRJ, SDP, SEC, SWF, CLD, DSY, DVO, EVT, SAR`) | 24 | 24 / 24 | 24 / 24 | **0** | [part_s05_s08.md](part_s05_s08.md) |
| 3 | `S09..S11` (`AIF, CVI, DAN, MLO, RLN, CAS, HCI, PAR, PLC, SEP, BCH, ESY, ROB`) | 18 | 18 / 18 | 18 / 18 | **0** | [part_s09_s11.md](part_s09_s11.md) |
| **Tổng** | **`S01..S11`** | **66** | **66 / 66** | **66 / 66** | **0** | — |
