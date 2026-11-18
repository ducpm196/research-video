# fix10 CS112 L00–L14 (sửa nhỏ sau R7_CS112_A) — 2026-11-17

Không chạy build/tts/asr/git/docker. Không đổi bài ngoài danh sách.

## Việc đã làm (7 bài đổi)
| Bài | Sửa | Từ lời đọc | Lint |
|---|---|---|---|
| L01 | limit.4 (`n log₂ n`): thêm ghi chú trên màn hình "log₂ n đọc là lôgarit cơ số 2 của n: số lần chia đôi n để còn 1" và một câu mở lời đọc tương ứng; thêm `focus` [1, 2, 2, 2] | 2151 | 0/0 |
| L02 | sort7 step 0: bỏ đại từ "nó" mơ hồ: "Vì tỉ số của lôgarit của n cộng 100 với lôgarit của n tiến về 1, hàm đầu bằng 50 lần một hàm cùng bậc lôgarit của n" (tách thành hai câu, thêm một mục focus); màn hình giữ Θ(log₂ n) | 2065 | 0/0 |
| L03 | linked.2: một dòng ánh xạ tên trên màn hình ("mã giả viết next, head; trong Python là tiep, dau") và một câu lời đọc (không đọc tên tiếng Anh: "con trỏ kế tiếp và biến đầu danh sách mang tên tiếng Anh, còn trong chương trình là ngăn tiếp và biến đầu") | 2211 | 0/0 |
| L06 | (mẫu `.tpl.yaml` + `regen_a.py gen`) bảng quy mô: số có nhóm dùng `&nbsp;` (100&nbsp;000, 99&nbsp;990, 1&nbsp;660&nbsp;964…) nên không gãy | 2297 | 0/0 |
| L08 | tiêu đề cột "viết trong mã" `white-space:nowrap` ở cả hai bảng (không gập) | 1931 | 0/0 |
| L00 | nested: công thức tổng k số lẻ `= 2 · k(k+1)/2 − k = k²` bọc `white-space:nowrap` (không gãy sau "2 ·") | 2296 | 0/0 |
| L12 | bảng 3 hàng cuối: ô "pop(0)" ghi "chỉ để gọn: bản chuẩn dùng hai chỉ số" và câu lời đọc cùng ý (đúng vì `pop(0)` dời cả danh sách, Θ(độ dài) mỗi lần) | 2298 | 0/0 |

Mọi bảng vẫn ≤ 4 hàng/step, step sau bảng có `clear: true`. Không đổi chỉ số step nên khoá `screen_code` CS112 giữ nguyên (khối mã không đổi chữ).

## Render
- `tools/lv.py render lessons/cs112/L01_*.yaml` chạy được: 117 khung, 0 vấn đề.
- Các lần chạy tiếp theo cho L00, L02, L03, L06, L08, L12 bị bộ phân loại quyền từ chối (Undermining Oversight); không đi vòng. Cần điều phối chạy render cho 6 bài này khi dựng lại (rebuild.claims CS112_L00–L29 đã tồn tại và rebuild.done có đủ L00–L14 từ 2026-11-16, nên không có luồng dựng đang giữ chúng).

## Lưu ý
- L12 (2298), L06 (2297), L00 (2296) sát trần 2300: mọi sửa tiếp phải cắt chỗ khác.
- Câu mới của L02/L03/L01 chưa qua ASR/nghe.
