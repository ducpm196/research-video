# R7 INT L00–L08 (vòng 7, đọc độc lập sau lần sửa thứ hai, P1 chặt): 9/9 bài — ghi lại bởi người điều phối từ tin nhắn của reader (ad48255e0fd017cff)

## 1. Tóm tắt (P1=2 chắc+vừa: vòng 6 6/9 → vòng 7 1/9; xem nhận định nhiễu)
MUST 0 (9/9). P1=2: 1/9 chắc+vừa (L07; L06 = 0; 7 bài = 1); tính cả yếu 0/9. Tổng 53 mục: 1 chắc (L06 "lũy đẳng"), 11 vừa, 41 yếu. P8=2 9/9 (lab giấy-bút, `mong_doi.txt` khớp, đã chạy 10 lệnh "Tự kiểm bằng Python" trong 9 `de.md`: khớp; không có thí nghiệm đổi tham số rồi quan sát); P9=2 9/9; spec khớp 9/9; SRT khớp `say` 9/9 (kiểm văn bản, chưa nghe audio); `checks` 214/214; 15 khối mã khớp (Python L00–L08; Java thật JDK 21: `LuongAo` L01, `BigDecimal` L01, `TuGoi` L02 ghép 3 khung). Mất gốc ĐỦ 8/9 (L06 GẦN); cả yếu GẦN 9/9. 53 khung hình đã xem: một lỗi hiển thị (L01).
Các sửa gần đây đều có mặt và đạt: L01 "đệm tĩnh" có trên màn hình; L03 bảng cặp + `for ten, rtt in doi_tac:` trước mã; L04 định nghĩa bit + "8 cặp hai chữ số"; L05 prereq 3+2 hàng; L06 sơ đồ 4 tầng có mũi tên "yêu cầu"/"kết quả về" + tiêu đề; L08 bảng giải thích `3 * n * ceil(log2 n) + 2 * (n + n)` + `requires` [L04, L07] cộng `requires_ext` PYT L00–L03; 9 `de.md` có dòng "Tự kiểm bằng Python".
Nhận định: cùng bộ bài, vòng 6 reader xếp 4 vừa, vòng 7 reader xếp 11 vừa (nhiều mục là thuật ngữ nền: "học máy", "API", "token", "đảo giao dịch", "lũy đẳng") — đo lường nhiễu giữa reader (CB-P1-CODE); mục chắc 1 là mới. Không có cú pháp mã nào chưa giảng mà bảng cách đọc cũng không phủ.

## 2. SHOULD (3) + ghi chú
| Bài | Cảnh | Trích | Vấn đề | Đề xuất | Tin cậy |
|---|---|---|---|---|---|
| L01 | concept.0 (khung 22) | hộp METASPACE "Bộ nhớ ngoài heap, do hệ điều hành cấp" | chữ "cấp" tràn ra ngoài viền phải | thu gọn chữ/nới hộp | CONFIRMED |
| L01 | concept.0 | "Đệm tĩnh = vùng nhớ dùng chung giữ dữ liệu tra nhanh…" | định nghĩa "đệm tĩnh", "bể kết nối" chỉ có trên màn hình, `say` không đọc | thêm một câu vào `say` | CONFIRMED |
| L03 | quymo.1 | "SAGA… nên xong sau bốn mươi giây dù đối tác chậm đến đâu" | khẳng định tuyệt đối (40 giây chỉ là thời gian giữ khoá dòng nóng; bảng ghi "mô hình rút gọn") | "…khoá dòng nóng vẫn chỉ giữ 4 mili giây" | PLAUSIBLE |
Ghi chú: `asr_report.md` còn "chưa xem xét" L03 (1 câu "Trước khi chạy, ta đọc mã Python.") và L04 (7 câu), các câu đó không có trong `asr_reviewed` hiện tại → cần chạy lại ASR L03, L04; toàn bộ ASR NOT_VERIFIED bằng tai người. Chưa kiểm được nguồn (bài đã tự ghi): TT 50/2024, TT 77/2025, QĐ 2345 (ngưỡng 10/20 triệu), TT 31/2024 (nhóm nợ 10–90 ngày), TT 37/2025, lệnh HSM CA/CC/JE/JC và mã 68 NAPAS, "AZ là phân hệ tiền gửi kỳ hạn".

## 3. Mục chưa giảng (1 chắc + 11 vừa)
Chắc: L06 prereq.2 "lũy đẳng, Outbox, Kafka" (B; bài không giảng lũy đẳng).
Vừa: L00 pitfall.1 "nền xác suất, tối ưu và học máy" (A); L01 concept.2 "gây quá hạn API" (A; API chưa giảng), pitfall.0 "thông tin định danh và token cũ" (A); L02 chaythat.1 `Class<?>[] gt = { Dv.class };` (A; hàng bảng cả dòng, không tách `<?>`); L03 quymo.1 `print(ten, '-> giu', round(giu * 1000), 'ms;', toc, …)` (B; bảng không có hàng `print`, `round` không nói đối số 2); L04 prereq.1 và check "4 = đảo giao dịch" (A; không nói đảo là huỷ tác dụng giao dịch đã gửi, đáp án quiz dựa vào đó); L05 prereq.1 "Học máy (Machine Learning), Học sâu…", example.4 "suy luận mô hình học máy qua ONNX Runtime" (A); L06 prereq.2 "chỉ mục, kế hoạch truy vấn" (B), prereq.0 "bế tắc khoá hoặc quá hạn" (M; giảng ở example.0); L08 pitfall.1 "ràng buộc duy nhất theo mã khoản vay" (B).
Yếu (41): "JBoss/MS SQL", "chia dữ liệu cho nhiều cụm", `long`/MB, "bể luồng", "hàm", `+` nối chữ Java, `getName()`, "bản sao", "nhật ký kiểm toán", `tong =`/`s =`, "phiên/tiến trình", "nút cổ chai", "retry", "bit (Bloom)", `cho / 1000` và GB, "bộ điều hợp", VND, "huấn luyện", "C++", "danh sách đen", "cửa sổ trượt", "ngưỡng", "mã giả", "khoá", "độ bão hoà", "trung tâm dữ liệu", "offer", "tích luỹ", "hoà vốn", "AZ", "bản ghi", `toc`, "lô chi lương".

## 4. Người học kẹt ở đâu
L00 gần như không kẹt (pitfall.1 "học máy"); L01 concept.2 "quá hạn API", pitfall "token cũ"; L02 chaythat.1 `Class<?>`; L03 quymo.1 `print` 6 đối số; L04 prereq.1 "đảo giao dịch"; L05 prereq.1 "Học máy", example.4 "suy luận"; L06 prereq.0 "bế tắc", prereq.2 "lũy đẳng, chỉ mục"; L07 không kẹt; L08 pitfall.1 "ràng buộc duy nhất".
