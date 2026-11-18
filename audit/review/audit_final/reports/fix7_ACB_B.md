# fix7_ACB_B — L06, L07, L08 (fork B vòng 7, theo R6_ACB)

## Bài đã đổi (requeue): L06, L07, L08; curriculum/acb.yaml (chỉ objective 5 của L07)

## Theo bài
- L08: bỏ "và Thấu chi Lương" khỏi tiêu đề SVG concept; `grep -i 'thấu chi lương'` toàn lessons/acb + curriculum/acb.yaml = 0. Giải nghĩa tại chỗ "giải ngân = ngân hàng chuyển tiền cho khách vay" (lời hook + chữ hook) và "dư nợ = số tiền còn nợ ngân hàng" (lời bước phong tỏa + câu hỏi tình huống). Cắt một câu hook (và `focus` 5 → 4) để vừa trần. Lời đọc 2293.
- L07: CIF giải nghĩa ("mã khách hàng duy nhất trong ngân hàng", lời + nhãn SVG đổi thành "Ánh xạ sang CIF (mã khách)"); "Số VA (số tài khoản ảo)"; bảng HMAC thêm `import hashlib, hmac` (giải nghĩa dấu phẩy nạp hai thư viện) cùng câu lời; bảng hai con trỏ thêm `else:`; bước "Nếu kẹt" của practice có bảng 4 hàng cho lời giải lab (`set(danh_sách)`, `|` hợp hai tập, `sorted`, `in`, `not`), kèm 3 câu lời, `clear: true`. Mục tiêu 5 sửa cho đúng nội dung ("đọc cách phân loại mã lệch khi mở rộng ra ba nguồn"; cảnh concept có bảng phân loại, lab Tự làm chạy thật) ở cả lessons và curriculum. Cắt ba câu lặp (định nghĩa log2 ở quiz, câu hook, câu recap) để vừa trần. Lời đọc 2290.
- L06: OTP = "mã dùng một lần gửi qua điện thoại" (chữ + lời, prereq.0); concept.0 "đối soát dữ liệu" → "so khớp dữ liệu"; Backend ("máy chủ phía sau ứng dụng") và chip CCCD ("chip trên thẻ căn cước công dân chứa dữ liệu của chủ thẻ") giải nghĩa trên màn hình, lời nói "máy chủ phía sau ứng dụng" (tránh chữ Latin). Lời đọc 2292.

## Cổng
- lint L06/L07/L08: 0 FAIL, 0 WARN. render 3 bài: 0 vấn đề; đã xem khung bảng Nếu kẹt L07 (130) và SVG L08 (22).
- `tests/test_e52.py` 0 FAIL; `lv.py curriculum curriculum/acb.yaml` 0 lỗi; `check_legal` 0 FAIL.
- `verify_acb.py` đủ khoá: 298/301; 3 FAIL nằm NGOÀI phạm vi, do bài khác đang sửa dở lúc chạy: L05 lời đọc 2355 (>2300), hai kiểm fixes6_l00_l02 của L02 ("bảng: 1 << 3 ..." và "nguyên tử, dịch mã PIN") — chữ L02 đã đổi, cần cập nhật kiểm hoặc chữ. Không có FAIL ở L06–L08.
- Không đổi khoá screen_code (không chèn step trước khối mã hiện có); không chạy gen_sc_acb.py.

## Mục chưa giảng ước còn lại: L06 0, L07 0, L08 0.
## Còn mở: lời đọc mới cần ASR; yếu "mTLS/Cloud CA" L08 chỉ giải nghĩa bằng lời như trước.
