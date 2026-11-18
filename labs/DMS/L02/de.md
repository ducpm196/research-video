# Lab DMS L02 — Kiểm câu có lượng từ trên một miền hữu hạn

Viết `luongtu.py` (Python 3.11 trở lên); chạy: `python luongtu.py`.

Miền: `D = range(20)`, tức các số tự nhiên 0, 1, ..., 19. Với mỗi câu dưới đây, in đúng một dòng:

| số | câu | in ra |
|---|---|---|
| 1 | với mọi x trong D: x·x > x | `1: dung` nếu đúng; nếu sai: `1: sai, phan vi du x=<giá trị nhỏ nhất làm câu sai>` |
| 2 | tồn tại x trong D: x·x = 2x + 3 | nếu đúng: `2: dung, vi du x=<giá trị nhỏ nhất>`; nếu sai: `2: sai` |
| 3 | với mọi x trong D tồn tại y trong D: x + y = 19 | `3: dung` hoặc `3: sai` |
| 4 | tồn tại y trong D với mọi x trong D: x + y = 19 | `4: dung` hoặc `4: sai` |
| 5 | với mọi x trong D tồn tại y trong D: y > x | `5: dung` nếu đúng; nếu sai: `5: sai, phan vi du x=<giá trị nhỏ nhất của x không có y>` |

Gợi ý: `all(...)` là "với mọi", `any(...)` là "tồn tại"; câu 3 và 4 chỉ khác thứ tự lượng từ. Phản ví dụ: danh sách `[x for x in D if not (...)]`, lấy phần tử đầu.

Chấm: `bash labs/cham.sh DMS L02 luongtu.py` — in `ĐÚNG` khi đầu ra trùng `mong_doi.txt`.
