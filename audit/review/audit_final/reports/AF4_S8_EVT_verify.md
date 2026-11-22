# Báo cáo Kiểm định Độc lập Stage 8 — Khóa `EVT` (`L00–L11`, 12 bài)

**Vai trò:** WP-AF4-3 Stage 8 EVT Verifier (read-only)  
**Kết luận tổng thể:** **`NO-GO`**

- **MUST:** **2 lỗi nội dung/toán học trên màn hình & đề lab (`L08`, `L11`)** + **thiếu khối `Hai mức quy mô` trong `recap` ở `12/12` bài** (`5/12` bài `L01, L02, L03, L06, L09` chưa có so sánh định lượng 2 quy mô ngay cả trong thân bài).
- **P1 (ngưỡng ≥ 80%):** **100.0% (`12/12`)** cho phần bài giảng lõi (`hook..recap`), nhưng **16.7% (`2/12`: `L08, L09`)** theo chuẩn chặt tính cả bảng `practice#0` và `labs/EVT/L*/de.md` do `upgrade_evt.py` đưa nhiều thuật ngữ/viết tắt tiếng Anh chưa giải thích tại chỗ (`bus`, `p2p`, `DLQ`, `Event Sourcing`, `snapshot`, `CQRS`, `Saga`, `Stream-Stream`, `DAG`, `RPC`, tên biến/hàm tiếng Anh).
- **P8 (ngưỡng = 100%):** **83.3% (`10/12`)** về khớp nội bộ `practice` ↔ `de.md` ↔ `loi_giai.py` ↔ `mong_doi.txt` (rớt `L08`, `L11`), và **0.0% (`0/12`)** nếu tính đủ cả `recap Hai mức quy mô` và khớp ngữ nghĩa `covers:` (`12/12` bài đều bị gán cứng `[(1, example/stage1), (2, check), (3, practice)]`).
- **P9 (ngưỡng ≥ 80%):** **100.0% (`12/12`)** — đã xem trực tiếp **43 PNG (`1920x1080`)**, `audit/layout_EVT.tsv` có `0` lỗi, hình SVG/bảng/code sắc nét, không tràn/chồng chữ.

---

## 1. Kết quả cổng tự động toàn khóa (`OBSERVED`)

| Cổng / Dữ liệu kiểm tra | Kết quả quan sát được |
|---|---|
| `lv.py curriculum curriculum/evt.yaml` | `12 bài, 12 đã có đặc tả, 0 lỗi` (PASS) |
| `audit/evt/verify_evt.py` | `12/12 PASS` (đối chiếu độc lập công thức `L00–L11` và `sources_L11.md`) |
| `lv.py lint lessons/evt/L*.yaml` | `12/12 PASS` (`0 FAIL, 0 WARN`; `L00–L10` PASS `E39`, `L11` PASS `E40`, `L00–L11` PASS `E51/E53`) |
| `lv.py verify lessons/evt/L*.yaml` | `12/12 PASS` (`spec_sha256` & `tts_sha256` khớp `build_report.json` `12/12`, `0` STALE, MP4 `h264`/`aac`/`1920x1080`) |
| `out/EVT/L*/L*.srt` vs `say` | `12/12` khớp 1–1 từng câu phụ đề |
| `out/EVT/L*/asr_report.md` | `12/12` có `thiếu audio: 0`, `chưa xem xét: 0` (`L00:0, L01:2, L02:2, L03:3, L04:2, L05:2, L06:1, L07:16, L08:0, L09:1, L10:3, L11:9`) |
| `screen_code.py check --course EVT` | `12 khối — PASS 12 · FAIL 0 · STALE 0 · MISSING 0 · ORPHAN 0 · WARN 0` |
| `audit/layout_EVT.tsv` | `0` lỗi bố cục/chồng chữ SVG |
| Chạy trực tiếp `labs/EVT/L*/loi_giai.py` == `mong_doi.txt` | `12/12 PASS` |
| Từ tiếng Anh / ký hiệu trong `say` | Sạch `12/12` |

---

## 2. Đánh giá chi tiết từng bài (`L00–L11`)

- **`L00`**: Thiếu `Hai mức quy mô` trong `recap`; `P1` (`bus`, `p2p`); `covers`.
- **`L01`**: Thiếu `Hai mức quy mô` trong `recap` & thân bài; `P1` (`de.md` nhiều tên biến tiếng Anh); `covers`.
- **`L02`**: Thiếu `Hai mức quy mô` trong `recap` & thân bài; `P1` (`DLQ` vs `kênh thư chết`); `covers`.
- **`L03`**: Thiếu `Hai mức quy mô` trong `recap` & thân bài; `P1` (`version`, `cur_ver`, `stale_dropped`); `covers`.
- **`L04`**: Thiếu `Hai mức quy mô` trong `recap`; `P1` (`Event Sourcing`, `snapshot`); `covers`.
- **`L05`**: Thiếu `Hai mức quy mô` trong `recap`; `P1` (`CQRS`, `ev/s` trong `practice#0`); `de.md` thiếu `"nếu dừng ghi"`; `covers`.
- **`L06`**: Thiếu `Hai mức quy mô` trong `recap` & thân bài; `P1` (`Saga` và tên hàm tiếng Anh); `covers`.
- **`L07`**: Thiếu `Hai mức quy mô` trong `recap`; `P1` (`Stream-Stream`, `clicks`, `imps`); `covers`.
- **`L08`**: **MUST-1**: `lessons/evt/L08_ap_luc_nguoc.yaml:228` (`practice#0`, `00062.png`) ghi `mất 24 phút xả hết` thay vì `40 phút` (`720 000 / 300 = 2400 s = 40.0 phút`); thiếu `Hai mức quy mô` trong `recap`; `covers`.
- **`L09`**: Thiếu `Hai mức quy mô` trong `recap` & thân bài; dấu `` ` `` thừa ở `labs/EVT/L09/de.md:10`; `covers`.
- **`L10`**: Thiếu `Hai mức quy mô` trong `recap`; `P1` (`DAG`, `đường găng`); `covers`.
- **`L11`**: **MUST-2**: `lessons/evt/L11_hanh_trinh_nhat_ky_su_kien.yaml:531` (`practice#0`, `00132.png`) ghi `gom lô 50 giảm 8 lần số gói` (sai toán: giảm 50 lần số vòng gửi, 8 lần là tỉ lệ tăng thông lượng `[K11] §5`) + `labs/EVT/L11/de.md` thiếu dữ kiện `500 000 tin`; thiếu `Hai mức quy mô` trong `recap`; `P1` (`RPC`, `khung truyền`); `covers`.

---

## 3. Tổng hợp các điểm cần sửa để đạt `GO`

1. **[MUST] `L08` (`practice#0`)**: Sửa `mất 24 phút xả hết` → `mất 40 phút xả hết`.
2. **[MUST] `L11` (`practice#0` & `labs/EVT/L11/de.md`)**: Sửa `gom lô 50 giảm 8 lần số gói` → `gom lô 50 giảm 50 lần số vòng gửi (với 500 000 tin còn 10 000 lô; thông lượng tăng 8 lần)` và thêm dữ kiện `500 000 tin` vào `labs/EVT/L11/de.md`.
3. **[MUST / P8] `L00–L11` (`recap` Hai mức quy mô)**: Bổ sung `<p class="note"><b>Hai mức quy mô:</b> ...</p>` ở `recap` cho cả 12 bài (và thêm so sánh định lượng 2 quy mô cho `L01, L02, L03, L06, L09` vào `audit/evt/af2/base/*.yaml` + `upgrade_evt.py`).
4. **[SHOULD / P1] `L00–L11` (`practice#0` & `de.md`)**: Việt hóa/chú thích tại chỗ các thuật ngữ tiếng Anh.
5. **[SHOULD / P8] `L00–L11`**: Sửa `covers:`, bỏ backtick thừa ở `L09/de.md`, thêm `"nếu dừng ghi"` ở `L05/de.md`.
