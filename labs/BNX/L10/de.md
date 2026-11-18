# Lab BNX L10 — Nén nhật ký có bia mộ và khớp mẫu sàn chủ đề (mô phỏng bằng Python, không cần Kafka hay RabbitMQ)

Nhật ký 8 bản ghi (khoá, giá trị), offset từ 0: `("M", 10), ("N", 20), ("M", 15), ("P", 5), ("N", None), ("M", 12), ("Q", 7), ("P", 9)`.
`None` là bia mộ (xoá khoá N). Viết `mau.py` (Python 3, chỉ thư viện chuẩn), in đúng năm dòng như `mong_doi.txt`:

1. Nén giữ bản cuối của mỗi khoá, còn bia mộ. In `con bia mo:` rồi các mục `offset:khoá:giá trị` theo thứ tự offset, cách nhau một dấu cách; bia mộ in `-` thay cho giá trị.
2. Hết thời gian giữ bia mộ: in `het han bia mo:` và danh sách đã bỏ bia mộ, cùng dạng.
3. Với khoá `payment.eu.sepa.eur` và mỗi mẫu `payment.*.sepa`, `payment.#.eur`, `*.eu.#` (`*` thay đúng một từ, `#` thay không hoặc nhiều từ; từ cách nhau dấu chấm), in `payment.eu.sepa.eur voi <mẫu>: co` hoặc `: khong`.

Gợi ý cú pháp Python: `for off, (k, v) in enumerate(log):` duyệt kèm số thứ tự và tách luôn cặp (khoá, giá trị); `d[k] = (off, v)` ghi đè bản trước của khoá `k` trong từ điển `d`; `None` là giá trị rỗng (bia mộ). Số liệu là số minh hoạ, khác ví dụ trong bài. Chạy: `python mau.py`. Chấm: `bash labs/cham.sh BNX L10 mau.py`.
