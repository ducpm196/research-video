# fix4 BNX L34–L38 (nhóm C của tác tử sửa L24–L38, 2026-11-15)

## Tiến độ
- Xong 5/5 bài: L34, L35, L36, L37, L38. Đã sửa NGUỒN `audit/bnx/src/l34..l38.py`, chạy `gen.py` từng bài (không sửa tay YAML).
- **Cả 5 bài đổi nội dung (lời đọc, bảng, khung mã) nên đều CẦN DỰNG LẠI** (tts, asr, render, build). Khung PNG `out/BNX/L34..L38/frames` đã dựng lại bằng `lv.py render` (chỉ để xem; mp4/srt cũ).
- Không chạm L24–L33 (nhóm khác), không sửa tệp dùng chung (`symbols.BNX.yaml`, lexicon, `gen.py`, `lib*.py`, sổ `BNX.yaml`, `curriculum/bnx.yaml`).

## Số liệu cổng (đo thật 2026-11-15)
| Bài | lint | từ lời đọc (≤ 2300) | render | verify_bnx | screen_fast (khối của bài) |
|---|---|---|---|---|---|
| L34 | 0 FAIL 0 WARN | 2289 | 0 vấn đề | 28/28 PASS | PASS |
| L35 | 0/0 | 2292 | 0 | 28/28 PASS | PASS |
| L36 | 0/0 | 2299 | 0 | 29/29 PASS | PASS |
| L37 | 0/0 | 2295 | 0 | 24/24 PASS (SQL Server 2022 và Java/JDBC Oracle chạy thật, không SKIP) | PASS |
| L38 | 0/0 | 2290 | 0 | 23/23 PASS (Oracle thật) | PASS |
- `verify_bnx.py L34..L38`: 132/132 PASS. `screen_fast.py L34..L38`: 100 khối — PASS 133, FAIL 0, STALE 0, MISSING 0, ORPHAN 0 (`screen_keep.py` chạy trước từng bài, "chưa khớp 0").
- `tests/test_e52.py`: 0 FAIL. `arith_scan.py BNX`: 58 phép tính, 0 FAIL. (Các cổng toàn khoá còn lại ghi ở cuối báo cáo.)

## MUST (1/1 phần việc của nhóm C đã sửa)
- **L37 example ⑤/⑥**: thêm hai bước "Dựng lại bảng" (hiện nguyên khối `MSS_BASE`, cùng sha với khối ở cảnh prereq nên sổ dùng lại mục cũ) ngay trước ⑤ và trước ⑥; ⑥ ghi "Bảng đã dựng lại". Kiểm thật qua `dbrun.mss` (ver/l37.py, dòng mới): chạy ⑥ ngay sau ⑤ không dựng lại → **1 800 000**; dựng lại bảng rồi ⑥ → **1 300 000**. Lời đọc bước dựng lại thứ hai nói rõ vì sao (phép thử trước để lại 1 800 000).

## P1 — giảng tại chỗ (mọi mục trong danh sách P1 của báo cáo người đọc cho L34–L38)
Cách làm: bảng "viết trong mã / nghĩa / ví dụ nhỏ" (kèm 1–2 câu lời đọc) ngay trước khối mã dùng cú pháp; thuật ngữ giảng ở cột "nghĩa". Không thêm mục `term:` nào.
- **L34**: bảng cách đọc ở đầu cảnh formula (`?` giữ chỗ, `(hs,)`, `.fetchone()[0]`, `executemany`, chuỗi f); bảng ở check (`sum(1 for … if …)`, `log[1:]`, `zip(log, log[1:])`, `DUOC.get(tu, set())`); bảng ở quymo (`global dem`, `create_function`, `i // 5`, `i % 5`, `range`); `GROUP BY kq ORDER BY kq` giải thích cạnh khối mã (nay hiện đủ 11 dòng tới câu đếm); lược đồ (`ho_so`, `ls`) vào bảng ký hiệu; bước 3a hiện `BAC`/`HANG`; bảng bậc có đủ bậc 1–3 cá nhân và doanh nghiệp, "giám đốc khối", "hội đồng" giải nghĩa ở lần đầu; ví dụ DN 3000 có lý do.
- **L35**: bảng ký hiệu thêm "API, cổng API", "mã tương quan", "đối soát" (định nghĩa tại chỗ, không chờ bài 36).
- **L36**: hằng số `KHACH, GD_KHACH, DINH, BYTE, NUT` hiện bằng khối mã + bảng (bước 2a); "mã HTTP" (200/409/422), "API", "cổng API", "API v1" trong bảng ký hiệu; bảng regex (`re.search`, `\b`, `(?! NOT)`, `TU`, `t in cau.lower()`; không dùng chữ "biểu thức chính quy" để khỏi tạo assumes chéo L31); cột `idempot/retr/unique` giải thích cạnh kết quả.
- **L37**: bảng ký hiệu thứ ba (bế tắc, `Msg 547, Level 16, State 1`, `--`, `'X'' OR ''1''=''1'`); hàng `THROW 50001, '…', 1;` (ba phần) và `FOR UPDATE` của Oracle (giải nghĩa) trong bảng thứ hai; bảng quymo cho `SELECT TOP (@n) … INTO … FROM sys.all_objects a, sys.all_objects b` và vòng `WHILE`; de.md giải thích `--`. Bỏ mọi chỗ "bài 6/bài sáu": thêm bảng "cần có để chạy lại" (Oracle Docker, `BNX_PASS`, jar `ojdbc11`, bảng + thủ tục Oracle cùng ý với T-SQL).
- **L38**: bảng ký hiệu giải nghĩa AQ (Advanced Queuing = hàng đợi nâng cao) và tên `DBMS_AQADM`/`DBMS_AQ`; "thời gian lưu giữ 0" nói rõ nghĩa (không giữ lại thông điệp đã nhận; đã có nguồn `L38AQ`).
- Điểm P1 dự kiến: tự đánh giá 4–5/5 bài đạt 2; cần người đọc chấm lại. Rủi ro: cú pháp rất nền (`for`, `def`, `class`, `with`) vẫn không có bảng riêng ở L34–L36.

## SHOULD (CONFIRMED) đã sửa
- L34: bảng ngưỡng có bậc 3 và vai trò DN; hiện bản "ghi có điều kiện" của Lỗi 2 (`sql += " AND tt = 'CHO_DUYET'"` + `rowcount`) và đầu ra; lược đồ/BAC/HANG hiện.
- L35: giả định P3 nêu rõ (hook, box ở example ③, lời đọc): bỏ sự cố 5 phút thì 42 < 43,2 chưa vượt; "10 lần chi phí" bỏ (không có nguồn), giữ "chia ngân sách cho 10" (phép tính); dòng `print` của quymo tách hai dòng (khung nay hiện đủ 4 dòng, hết tràn); ô bảng thêm "thường".
- L36: hằng 10/2000/500 hiện; hook "trung bình 231/23 148"; `KhoaLuyDang.py` tách hai khung (9 + 7 dòng) tới `return "da chuyen"` có cộng B; quiz 2 ghi "10,4167 × 6 ≈ 62,5; nhân từ 10,4 ra 62,4".
- L37: `Goi.java` hiện `public class Goi {` (dòng 1–3 + 17–26); nêu cần `BNX_PASS`, ojdbc; "ghép chuỗi chuỗi" sửa; Java nay chạy thật trong verify (trước: NOT_VERIFIED).
- Không sửa (lý do): L38 không có SHOULD. L35 "ô bảng bỏ chữ thường" đã sửa; L36 "nhân 100: 231 là trung bình" đã sửa.

## Việc cần điều phối xử lý
- **Sổ chung**: `audit/bnx/screen/l34..l38.yaml` đã sinh lại bằng `screen_keep.py` (khối đổi khớp theo sha/chương trình); khi gộp vào `audit/review/screen_code/BNX.yaml` dùng `screen_try.py --merge`. Không có mục viết tay mới.
- **`curriculum/bnx.yaml`**: mục tiêu/`covers` của L34–L38 KHÔNG đổi, không cần sửa.
- **Cần dựng lại (tts, asr, render, build)**: L34, L35, L36, L37, L38 (cả năm). Câu `say` mới/đổi là câu TTS mới; dò ASR: "byte" (L36, đã có luật `bai`), "hàng đợi nâng cao", "bế tắc", "đối soát", "nháy đơn".
- Thư viện/DB: `audit/bnx/ver/l37.py` tạo database `bnx_l37` trên bnx-mss và bảng/thủ tục `bnx_l06_*` trên Oracle (cùng cơ chế vòng trước); không tạo đối tượng mới ngoài tên đó.

## Cổng toàn khoá (chạy cuối phiên)
- `check_course_refs.py BNX`: 0 vấn đề. `check_next_refs.py`: 550 lời hẹn, 0 lệch dãy học.
- `lab_gate.py BNX`: 39 PASS · 0 FAIL (196 lab được bài tham chiếu).
- `lv.py curriculum curriculum/bnx.yaml`: 39 bài, 39 có đặc tả, 0 lỗi.
