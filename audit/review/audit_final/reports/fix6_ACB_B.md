# fix6_ACB_B — L06, L07, L08 (fork B, 2026-11-16)

## Bài đã đổi (cần requeue): L06, L07, L08 (+ curriculum/acb.yaml L08 title; sổ screen_code ACB: đổi khoá "ACB L08 symbol 1 0" thành "symbol 2 0" + câu claims; không đổi sha)

## Quyết định L08 "thấu chi lương"
Không có nguồn kiểm được: `resources/job/hub-system-graph.md` chỉ liệt kê tên API ("Kiểm tra hợp đồng/trạng thái đăng ký thấu chi lương", "Gỡ hạn mức thấu chi lương"), không có bội số lương, hạn mức hay lãi; JD.md không nêu. Vì vậy BỎ lời hứa, không bịa số: sửa tiêu đề bài ("Thấu chi Sổ tiết kiệm và Cổng CIC", cả lessons và curriculum), hook (bảng + "Hôm nay ta làm chủ"), lời hook, concept (bỏ "Whitelist lương" khỏi SVG và lời; xoá bước "ba dòng sản phẩm" gồm thấu chi lương và vay trên thẻ/thẻ ảo), recap (chuỗi + bảng). Auto-Debit và câu cụt "chuyển tiền qua NAPAS khi khách lệnh" đã sửa ở recap. Mục tiêu/fix curriculum vốn không nhắc lương nên không đổi.

## Theo bài
- L06: 3 bảng "Đọc trước" trong cảnh code (for/or/`a if c else b`/print; import/`b""`/`.encode()`/hexdigest/từ điển; def/return/`+`/str/`!=`/set/in/.add), định nghĩa `hmac.compare_digest` trên màn hình và lời; chân trang cham.sh tách bước riêng (có giải thích) + đề practice "lưu mau.py, python mau.py"; quiz đáp án đúng chuyển sang D (xáo phương án, sửa show + lời); cắt lời ở hook/prereq/concept/check để vừa trần. Pháp lý giữ nhãn.
- L07: 3 bảng Đọc trước (b""/encode/HMAC/chuỗi JSON; set()/in/.add/return "200 OK"; while/len/elif/`i, j = i+1, j+1`/`a[i:]`), định nghĩa "Có quyết toán", NAPAS Clearing File, O(N)/duyệt một lượt, `LIKE '8888%'`, ràng buộc duy nhất; quymo s1 nêu rõ "giả định 24 giờ, khác khoá 120 giây ở bước một"; hình SVG hai/ba con trỏ (mũi tên có đầu thật, khớp lời) ở example bước 5; chân trang cham.sh tách bước; quiz đúng = C; compare_digest đã có từ trước.
- L08: 3 bảng Đọc trước (Go `:=`/`=`/`err != nil`/`nil`/`return`/`ctx`; def/if not/return/print; import sqlite3/`:memory:`/CREATE TABLE PRIMARY KEY/INSERT INTO; for/try-except IntegrityError/print), "đối soát" định nghĩa tại chỗ, chân trang cham.sh có giải thích, đề practice thêm "python mau.py"; cắt lời để vừa trần. Quiz giữ B.

## Từ lời đọc (lint "ước lượng")
L06 2277 · L07 2300 · L08 2296 (≤ 2300).

## Cổng thật (chạy lại cuối)
- lint L06/L07/L08: 0 FAIL, 0 WARN (29/34/30 PASS).
- `lv.py render` 3 bài: 0 vấn đề (đã sửa 1 lần tràn L07 practice bằng cách tách bước chân trang; xem khung L06 54, L07 52 hình con trỏ, L08 34 và 72).
- `verify_acb.py L06 L07 L08`: 71/71 PASS (tức không có chỉ số step cố định nào bị lệch; chạy đầy đủ cả khoá do người điều phối).
- `tests/test_e52.py` 0 FAIL; `lv.py curriculum curriculum/acb.yaml` 9 bài 0 lỗi; `arith_scan.py` 257 phép 0 FAIL; `check_legal.py` 111 lượt dẫn, không FAIL (8 văn bản CHUA_KIEM giữ nhãn).
- CHƯA chạy: `screen_code.py check --course ACB` (các mục cảnh `code` L06–L08 lệch chỉ số step tới khi người điều phối chạy `gen_sc_acb.py`), `lab_gate.py ACB` (lab không đổi), `check_curricula_graph.py`.

## Mục chưa giảng ước còn lại
L06 0 · L07 0 · L08 0 (có thể 0–1: chữ "mTLS"/"Cloud CA" chỉ giải thích bằng lời trong bài như trước).

## Còn mở
- Cần nghe/ASR lại mọi câu mới; asr_reviewed của câu đã đổi đã xoá.
- Người điều phối: chạy `gen_sc_acb.py` rồi `screen_code.py check`; L08 symbol (Go) đã đổi khoá thủ công.
- Không thêm mục vào symbols.ACB.yaml (L07 dùng `introduces: acb_byte` đã có sẵn, `acb_hmac` chuyển sang bước Đọc trước của L06).
