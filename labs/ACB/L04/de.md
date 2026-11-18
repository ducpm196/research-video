# Lab ACB L04 — Khoá lạc quan bằng sqlite, tiền lãi mất đi khi rút sớm và máy trạng thái

Số liệu (số minh hoạ, khác ví dụ trong bài):
- Bảng `so (id INT, ver INT)` có một dòng `(2, 3)`. Ba người mua A, B, C đều đã đọc `ver = 3` rồi lần lượt chạy câu cập nhật `UPDATE so SET ver = ver + 1 WHERE id = 2 AND ver = ?` với tham số `3`.
- Sổ gốc **300 000 000** đồng, lãi **6,8%** một năm, kỳ hạn 12 tháng. Rút trước hạn ở ngày thứ **200** thì chỉ hưởng lãi không kỳ hạn **0,1%** một năm.
- Cạnh được phép: `CHAO_BAN → PROCESSING`, `PROCESSING → HOLD`, `PROCESSING → DONE`, `HOLD → DONE`, `HOLD → REVERT`. Thử hai bước: `HOLD → DONE` và `DONE → HOLD`.

Viết `mau.py` (Python 3, dùng `sqlite3` có sẵn) in đúng các dòng:

1. `mua A: <số dòng tác động>`, rồi `mua B: …`, `mua C: …`.
2. `phien ban cuoi: <ver>` đọc lại từ bảng.
3. `lai du kien: <số>` — gốc × 68 chia nguyên cho 1000.
4. `lai rut truoc han: <số>` — làm tròn `gốc × 200 / 365000`.
5. `mat: <lãi dự kiến trừ lãi rút trước hạn>`.
6. Hai dòng `<từ> -> <sang>: <cho phep | tu choi>` cho hai bước thử.

Chạy: `python mau.py`. Chấm: `bash labs/cham.sh ACB L04 mau.py`.
