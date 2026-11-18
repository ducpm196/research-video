# fix9_INT — sửa vòng 9 theo R6_INT (2026-11-17)

Bài đổi (requeue): L00 L01 L02 L03 L04 L05 L06 L07 L08 (cả 9). ASR L04 phải chạy lại khi dựng (lời đọc đổi).
Cổng: lint 9/9 0 FAIL 0 WARN; lời đọc L00–L08 = 2298/2298/2291/2294/2300/2287/2277/1876/2299 từ (≤ 2300); `lv.py curriculum` 0 lỗi; `check_curricula_graph` 0; `test_e52` 0 FAIL; `lab_gate INT` 9 PASS; screen_code INT + verify_int xem cuối tin nhắn. Render vẫn bị chặn quyền ("Undermining Oversight"), không đi vòng.

## 1. Bốn mục vừa (bắt buộc)
- L01 concept.0 "Đệm tĩnh": thêm định nghĩa (vùng nhớ dùng chung giữ dữ liệu tra nhanh, tồn tại suốt đời chương trình) và "bể kết nối" ngay trên sơ đồ.
- L03 quymo: bảng "Đọc trước" (danh sách cặp, `for ten, rtt in doi_tac:` lấy cặp ra hai biến, `toc, xong = a, b` gán cùng lúc, `#`) đứng TRƯỚC khối mã (step 0), mã ở step 1.
- L04 prereq: thêm hàng định nghĩa bit ("một chữ số nhị phân 0 hoặc 1; bit thứ k = vị trí k đếm từ trái; 4 bit = một chữ số hệ mười sáu") trước "bit thứ k"/"0011 0000 = 30", và câu đọc tương ứng.
## 2. SHOULD
- L04: "16 cặp" → "8 cặp hai chữ số" (màn hình + lời đọc); không có `checks` dính; thêm giải nghĩa "chữ số kiểm tra" và "khoá khử trùng".
- L08: bảng "Đọc tiếp: công thức của cột sắp xếp" giải thích `3 * n * ceil(log2 n) + 2 * (n + n)` (3 lần sắp xếp ba danh sách, 2 lượt hai con trỏ qua n + n) trước mã; `labs/INT/L08/de.md` nhắc lại; `O(N<sup>2</sup>)` mũ thật; NAPAS được giải nghĩa tại lần đầu.
- L01 quiz: "khoảng gấp đôi" (màn hình + lời đọc); chú thích tính như đúng gấp đôi.
- L02: không thể có một khung chứa trọn `TuGoi.java` (19 dòng mã, cao hơn khung 724 px; ba khung hiện tại 8 + 8 + 6 dòng): thêm ghi chú trên khung cuối "Ghép ba khung mã theo thứ tự thành một tệp TuGoi.java để gõ lại và chạy". Đề xuất nếu cần khung đủ: rút chương trình xuống ≤ 15 dòng (đổi cả sổ screen_code).
- L03: cột "40 giây" không gãy dòng (`white-space:nowrap`).
- L05/L07/L08: cột "viết trong mã" của bảng Đọc trước dùng `white-space:nowrap` (chỉ ô mã ngắn).
- L06: sơ đồ 4 tầng có mũi tên "yêu cầu" đi xuống và "kết quả về" đi ngược lên (SVG), lời đọc thêm một câu khớp hình; sửa thiếu `</td>` ở hook.1.
## 3. Mục yếu cùng họ (định nghĩa tại chỗ)
AOP, Servlet, Aspect (L02 quiz); "bản chạy (instance)" (L02); "bộ nhớ ngoài heap, do hệ điều hành cấp" thay "native" và JDK (L01); RAM (L00); "độ tương đồng cosine" nêu một vế ở prereq và "hiệu chỉnh" (L05); "gọi lại bất đồng bộ" (L06); InnoDB đọc ra một vế (L00); uptime và "vị trí dòng bị khoá" (L03).
## 4. Curriculum
L08 `requires: [L04, L07]` (kiểm `lv.py curriculum` 0 lỗi, `check_curricula_graph` 0).
## 5. Lab
Cả 9 `de.md` có một dòng "Tự kiểm bằng Python (không bắt buộc)" với lệnh `python -c "..."`; đã chạy thử từng lệnh, kết quả khớp mong_doi.txt (L04 gồm khối PIN 045802BA9876FEDC).
## Sổ screen_code / verify
Chèn/tách step làm lệch chỉ số: đổi khoá bằng Edit (L03 quymo 1; L08 quymo 2) và cập nhật `audit/int/verify_int.py` (L03 quymo 1, L08 quymo 2).
## Chưa làm
Khung TuGoi.java đủ (xem trên); render (bị chặn).

## Kết quả cổng cuối
screen_code INT: 60 khối — PASS 83 · FAIL 0 · STALE 0 · MISSING 0 · ORPHAN 0. verify_int: 208 PASS, 0 FAIL (đã sửa kiểm "L08 requires L04 và L07" cho khớp giáo án mới).

## Vòng r9 cuối (từ R7_INT.md): chỉ thêm giải nghĩa ngắn + 3 SHOULD
- Giải nghĩa thêm: L06 (lũy đẳng, chỉ mục, kế hoạch truy vấn, bế tắc, quá hạn), L00 (học máy), L01 (API, quá hạn, token), L02 (`Class<?>`/`<?>` = kiểu bất kỳ), L03 (`print(a, b, ...)`, `round(x)`/`round(x, 2)`), L04 (đảo giao dịch), L05 (học máy/mô hình, suy luận vs huấn luyện), L08 (ràng buộc duy nhất). Không thêm số hiệu pháp lý.
- SHOULD: L01 hộp METASPACE rút chữ "Bộ nhớ ngoài heap" (hết tràn); L01 concept.0 thêm 2 câu `say` về đệm tĩnh/bể kết nối (focus 4 mục); L03 SAGA: "chỉ giữ khoá dòng nóng bốn mili giây ... dù đối tác chậm đến đâu, nên xong sau bốn mươi giây". Để giữ ≤ 2300 từ, L01 prereq.3 và L06 ghi chú "Hỗ trợ mức 3" được rút gọn.
- Cổng: lint 9 bài 0 FAIL/0 WARN; từ 2277-2300 (L07 2277... L08 2299); curriculum 0 lỗi; test_e52 0 FAIL; verify_int 208 PASS; lab_gate 9 PASS; arith_scan 0 FAIL; check_curricula_graph sạch; screen_code INT 60 khối 0 FAIL/STALE/MISSING/ORPHAN.
- Render L00–L06, L08: 0 vấn đề (L07 không đổi). Đã xoá 1 mục asr_reviewed cũ của L03 (E30). ASR L03/L04 để điều phối chạy lại sau dựng.
