# Báo cáo Kiểm định Độc lập WP-AF4-5 Stage 8 — Khóa `EVT` (`L00–L11`, 12 bài, v2)

**Phán quyết tổng thể:** **`NO-GO`**

## 1. Tóm tắt kiểm tra tự động
- `tools/lv.py curriculum curriculum/evt.yaml`: **PASS** (`12/12`)
- `audit/evt/verify_evt.py`: **12/12 PASS**
- `tools/lv.py lint lessons/evt/L*.yaml`: **12/12 PASS** (`0 FAIL, 0 WARN`)
- `loi_giai.py` vs `mong_doi.txt`: **12/12 PASS**
- `audit/review/screen_code.py check --course EVT`: **12/12 PASS**
- `arith_scan.py EVT`: **66/66 PASS**; `check_meta.py`: **0 vấn đề**; `check_xref.py`: **0 lượt**; 13/13 SVG sạch
- `out/EVT/L*/build_report.json`: **12/12 STALE** (thuộc bản dựng `2026-11-19`)

## 2. Danh sách `MUST fix`

### M1. MP4/ASR STALE `12/12` & thời lượng `< 9.0` phút (`10/12` bài `L00, L01, L03..L10`)
- Bổ sung lời đọc (`Hai mức quy mô`, mở rộng phân tích, bảng đọc mã) để đạt `>= 9.0p` (`>= 540s` thực tế), chạy `layout_scan.py EVT` và rebuild `L00–L11`.

### M2. Lỗi toán học & mâu thuẫn đơn vị ở `L05 recap#1` (`L05_tach_ghi_doc.yaml:220`)
- Sai đơn vị `"2 lít mỗi giây"` (thân bài `prereq#0`: `mỗi phút`).
- Nhầm `"trễ 150 giây"` (`60 000 / 400` là thời gian xả khi dừng ghi mới; trễ thực tế khi đang đến `500/s` là `120s`).
- `"mất nhiều giờ"` mâu thuẫn `pitfalls#3` (`33,3 phút`).

### M3. `[P8]` Trùng bộ số bài giảng (`10/12`), lộ đáp số/công thức & thiếu làm tròn ở `de.md` / `practice#0`
- Trùng số bài giảng: `L00, L02..L06, L08..L11` (thêm `L02/loi_giai.py` không mô phỏng vòng 3 lần; `L06` lệch tên `'reserve'` vs `'reserve_stock'`).
- Lộ công thức/đáp số ở `de.md` (`L00..L06, L09, L11`) và `practice#0` (`L00, L02, L03, L05, L08..L11`).
- Thiếu quy tắc làm tròn `ceil`/`round` trong `de.md`: `L09` (`ceil(30+7.5)=38`), `L04` (`round(..., 0)`), `L11` (`round(..., 0)`).

### M4. `[P1]` Thiếu hoàn toàn bảng đọc mã Python `practice` (`12/12` bài) & thuật ngữ tiếng Anh chưa giảng
- Bổ sung bảng đọc mã bằng `ast_p1.py` cho `12/12` bài (`audit/evt/af2/upgrade_evt.py`).
- Thuật ngữ chưa giảng tại chỗ: `bus, p2p` (`L00`), `DLQ` (`L02`), `version, NTP` (`L03`), `Event Sourcing, snapshot` (`L04`), `CQRS, ev/s` (`L05`), `Saga` (`L06`), `Stream-Stream` (`L07`), `đường găng, DAG` (`L10`), `RPC, Raft, 1 TB = 1000 GB` (`L11`).

### M5. `covers:` trỏ sai cảnh dạy thực chất (`9/12` bài)
- `L01` obj3→`sym/quiz`; `L02` obj3→`pitfalls/sym`; `L03` obj2→`pitfalls/sym/quiz`, obj3→`example/check`; `L04` obj3→`pitfalls/sym/quiz`; `L05` obj1→`sym`, obj2→`example`; `L06` obj2→`example/check`, obj3→`pitfalls/sym`; `L09` obj1→`sym`, obj3→`pitfalls/quiz`; `L10` obj3→`pitfalls`; `L11` obj3→`quiz/pitfalls`.

## 3. SHOULD fix
- Bổ sung `say:` và `focus:` cho `Hai mức quy mô` (`L00–L11`, nhất là `L01, L03`) và đồng bộ số `L00/L04 recap#1` với thân bài.
- Bỏ ngoặc lồng (`L10:239`) & giảm ngoặc đơn dày đặc trong `de.md` / `show`.
- Chuẩn chính tả `"mili giây"` trên `show:` (`L00:144`, `L10:32`); làm rõ `"k > 1"` ở `L09:144-145` (`$k$ càng gần 1 từ phía trên`).
- Cập nhật `screen_code/EVT.yaml` & `audit/evt/af2/upgrade_evt.py`.
