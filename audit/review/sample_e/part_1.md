# Mẫu E — phần 1: đã đọc 11/11 bài

Bài: ACB L04, AGT L05, AIF L06, BCH L02, BNK L07, CAS L06, CLC L11, CLD L09, CS112 L03, CS115 L12, CSA L13.
Đã đọc với mỗi bài: đặc tả `lessons/<khoá>/Lxx_*.yaml` (show, say, checks, quiz), mục giáo án trong `curriculum/<khoá>.yaml`, `chapters.txt`, `_frames.txt` (cộng dồn duration để biết khung nào ứng với cảnh nào), và ít nhất 5 khung hình. Bài CAS L06 đã đối chiếu thêm `audit/cas/sources_L06.md`.

## 1. Chuẩn xác

| Bài | Mức (MUST/SHOULD) | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng (phép tính/nguồn) | Đề xuất sửa | Tin cậy (CONFIRMED/PLAUSIBLE) |
|---|---|---|---|---|---|---|
| ACB L04 | SHOULD | title bài + concept (tiêu đề “…và Máy Trạng thái Chuyển nhượng”); objective 3 | “máy trạng thái Core Banking T24”; “xử lý ma trận mã lỗi treo lệnh” | Lời đọc ở hook định nghĩa máy trạng thái là “danh sách các trạng thái của một lệnh và những bước chuyển hợp lệ giữa chúng”, nhưng không cảnh nào liệt kê đủ trạng thái và bước chuyển (chỉ nhắc PROCESSING, HOLD; không có trạng thái ban đầu, thành công, hoàn tiền). “Ma trận mã lỗi” chỉ có một câu “04, 05, 999 → HOLD”. Như vậy giáo án hứa nhiều hơn phần bài thực sự dạy. | Thêm một bảng hoặc sơ đồ trạng thái (ví dụ OPEN→PROCESSING→DONE / HOLD→DONE hoặc REFUNDED) và một bảng mã lỗi → hành động. Nếu không thêm thì sửa tiêu đề cho khớp. | CONFIRMED |
| ACB L04 | SHOULD | example step 3 | “Toàn bộ quy trình loại trừ xung đột hoàn tất trong khoảng $25$ mili giây” | Bài nói 10:00:00.100 là “lần cập nhật trước”, tức chưa thuộc quy trình. Hai lệnh mua diễn ra lúc .120 và .125, nên quy trình loại trừ chỉ kéo dài 125 − 120 = 5 ms. Con số 25 ms là 125 − 100, tính từ một mốc nằm ngoài quy trình. | Đổi thành “khoảng 5 mili giây giữa hai lệnh”, hoặc nói rõ 25 ms được tính từ lần cập nhật trước. | PLAUSIBLE |
| BCH L02 | SHOULD | sym/intuition (lá đánh số gd1…gd8) và example step 2 (luật chẵn/lẻ) | “vị trí lẻ thì anh em đứng ngay trước, vị trí chẵn thì anh em đứng ngay sau” | Luật này chỉ đúng khi đánh số từ 0. Phần ví dụ có ghi “đánh số từ 0”, nhưng hình 8 lá và câu 2 của quiz lại đánh số từ 1. Áp luật lên số trên hình: gd6 mang số chẵn 6 sẽ bị ghép với gd7, trong khi đúng phải là h5 (hình tô cam h5). Người mới dễ áp sai. | Đánh số lá trên hình từ 0, hoặc ghi luật theo “vị trí tính từ 0” kèm một ví dụ trên hình. | PLAUSIBLE |
| BNK L07 | SHOULD | formula step 1 | “Làm thử: khoá TK-1001 hai lần đều vào phân vùng 1.” | Số này tính bằng crc32 (`checklib.bnk_key_partition`). Bộ chia mặc định của Kafka dùng murmur2: tôi tự cài murmur2 theo Kafka, kiểm với giá trị chuẩn trong test của Kafka (`murmur2("21") = −973932308`, khớp), rồi tính `toPositive(murmur2("TK-1001")) % 6 = 2`. Màn hình đặt câu này trong bối cảnh Kafka, nên người học sẽ hiểu là Kafka thật xếp khoá vào phân vùng 1. | Ghi “(băm minh hoạ, Kafka thật dùng murmur2 → phân vùng 2)”, hoặc đổi số thành 2. | CONFIRMED |
| CAS L06 | SHOULD | intuition (SVG) | “mũi tên: hộp bên phải cần hộp bên trái chạy được” + mũi tên “cần” đi từ hệ con cấp chỗ lên hệ con chỉ mục | Các mũi tên khác đi từ thành phần được cần tới thành phần cần nó. Riêng mũi tên “cần” lại đi từ cấp chỗ lên chỉ mục, tức ngược chiều với chú giải, trong khi nguồn ghi “placement … requires the index subsystem”. Hai mũi tên đỏ “gỡ nhầm máy” là quan hệ nhân quả, không phải phụ thuộc, nhưng dùng chung kiểu mũi tên. | Đảo chiều mũi tên (chỉ mục → cấp chỗ), hoặc tách chú giải cho mũi tên đỏ và mũi tên “cần”. | CONFIRMED |
| CLC L11 | SHOULD | sym + toàn bài; objective 2 | “Sáu trụ cột: vận hành xuất sắc, an toàn, tin cậy, hiệu năng, tối ưu chi phí, bền vững — mỗi quyết định được rà theo cả sáu.” | Objective “Rà thiết kế theo sáu trụ cột” không được thực hiện. Sáu trụ cột chỉ được đọc tên, không giảng nghĩa từng trụ cột. Ví dụ chính (3 thành phần) không đem ra rà theo sáu trụ cột; chỉ lỗi 3 nhắc tới 2 trụ cột. | Thêm một bảng rà thiết kế đích theo 6 trụ cột (mỗi trụ cột một dòng nghĩa + được/mất). | CONFIRMED |
| CLC L11 | SHOULD | intuition (SVG) | nhãn “co giãn theo nhóm” (y=160) chồng ngay trên “chuyển có chỉnh” (y=190) | Khung 00019.png: nhãn của hàng máy ứng dụng nằm giữa hàng 1 và hàng 2, xếp chồng với nhãn của hàng cơ sở dữ liệu, nên trông như hàng cơ sở dữ liệu có hai chiến lược. | Đặt nhãn “co giãn theo nhóm” ngang hàng y≈110. | CONFIRMED |
| AGT L05 | — | | | không phát hiện lỗi | | |
| AIF L06 | — | | | không phát hiện lỗi | | |
| CLD L09 | — | | | không phát hiện lỗi | | |
| CS112 L03 | — | | | không phát hiện lỗi | | |
| CS115 L12 | — | | | không phát hiện lỗi | | |
| CSA L13 | — | | | không phát hiện lỗi | | |

Tổng: 0 MUST, 7 SHOULD.

## 2. Độ sâu cho người mất gốc

| Bài | Phút (từ chapters/srt) | P1 | P2 | P3 | P4 | P5 | P6 | P7 | Tổng | Mất gốc | Chỗ thiếu chính |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ACB L04 | 6,6 | 0 | 2 | 1 | 2 | 1 | 2 | 1 | 9 | GẦN | P1: các thuật ngữ OFS, HTTP 200/409, API Gateway, cú pháp `UPDATE … SET … WHERE`, “hạch toán”, “đối soát”, “phong toả” đều không được giảng tại chỗ. P3: SVG 4 hộp (00021.png) chỉ có tác dụng minh hoạ, không có hình trạng thái. P5: các phương án nhiễu B/C/D quá vô lý (“không cần cơ sở dữ liệu”, “cộng thêm tiền lãi”) nên quiz không kiểm được hiểu. P7: máy trạng thái và ma trận mã lỗi còn mỏng. |
| AGT L05 | 9,1 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | P1: “tác tử”, “mô hình” được dùng ngay từ hook mà không giảng. |
| AIF L06 | 5,8 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | P1: lỗi 1 dùng “nhánh b”, “độ sâu d”, “b = 35” mà không nói 35 là số nước đi trung bình của cờ vua. Phụ: cây (00016.png) không ghi nhãn B/C/D, dù phần ví dụ gọi các nhánh theo tên này. |
| BCH L02 | 7,7 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | P1: “khối”, “tiêu đề khối”, “chuỗi đúng” dựa vào bài 1 mà không giảng lại. Bài cũng lẫn cách đánh số lá từ 0 và từ 1 (xem bảng 1). |
| BNK L07 | 8,0 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | P1: “lũy đẳng” là cách chữa then chốt, có trong recap, nhưng không có câu định nghĩa. `poll()`, `max.poll.interval.ms`, `max.poll.records` chỉ hiện trên màn hình. |
| CAS L06 | 10,6 | 2 | 2 | 1 | 2 | 2 | 2 | 2 | 13 | ĐỦ | P3: chiều mũi tên trong hình phụ thuộc mâu thuẫn với chú giải (00029.png). |
| CLC L11 | 7,0 | 1 | 2 | 1 | 2 | 1 | 1 | 1 | 9 | GẦN | P1: tên 6 trụ cột, “đặt trước”, “khấu hao” không được giảng. P3: hình trước/sau chỉ có tác dụng minh hoạ, nhãn lệch hàng (00019.png). P5: lời giải câu 1 chỉ một dòng. P6: chưa có đánh đổi theo trụ cột ở ví dụ chính, cũng không có số liệu tại chỗ để so với “đắt hơn tại chỗ”. P7: objective 2 không đạt. |
| CLD L09 | 7,3 | 1 | 2 | 2 | 2 | 1 | 2 | 2 | 12 | ĐỦ | P1: “Pod” chỉ được dẫn về bài 5; “hạt giống ngẫu nhiên” không giảng. P5: quiz là phép tính thuần (liệt kê vòng tròn, tính %), không kiểm hiểu về “chọn tốt hơn trong hai” hay về kết nối giữ lâu. |
| CS112 L03 | 9,1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | Phụ: quiz chỉ dừng 8 giây. Không có hình cho bước chèn đầu (chỉ có mã kèm bảng duyệt). |
| CS115 L12 | 11,7 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | Phụ: quiz chỉ dừng 8 giây. |
| CSA L13 | 7,4 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | P1: “lõi” (lõi bộ xử lý) được dùng từ tiêu đề hook mà không giảng. |

Phân bố: ĐỦ 9, GẦN 2 (ACB L04, CLC L11), CHƯA 0.

## 3. Khung hình đã xem

- ACB L04: 00006, 00015, 00021, 00041, 00059, 00064
- AGT L05: 00002, 00028, 00064, 00073, 00082
- AIF L06: 00002, 00016, 00031, 00048, 00052
- BCH L02: 00016, 00020, 00026, 00055, 00063
- BNK L07: 00003, 00025, 00029, 00035, 00076, 00089
- CAS L06: 00003, 00029, 00048, 00075, 00087
- CLC L11: 00003, 00015, 00019, 00028, 00053, 00060
- CLD L09: 00001, 00020, 00025, 00053, 00061
- CS112 L03: 00004, 00022, 00034, 00062, 00074, 00079
- CS115 L12: 00002, 00041, 00046, 00074, 00100, 00110
- CSA L13: 00002, 00016, 00025, 00059, 00064

Tổng 60 khung. Không thấy chữ tràn, chữ bị cắt hay đè chữ. Lỗi hiển thị duy nhất là nhãn lệch hàng ở CLC 00019. Phụ đề khớp lời đọc trong `say` ở mọi khung đã xem.

## 4. Mã đã chạy / số đã tính lại

Script: `scratchpad/sample_e/p1/recompute.py` và `bnk.py`. Kết quả: **162 phép kiểm, 162 khớp** với số ghi trên màn hình hoặc trong lời đọc, đúng tới số chữ số được ghi.

Một số điểm đáng chú ý:
- **ACB:** câu UPDATE khoá lạc quan chạy bằng sqlite3: người mua 1 được 1 dòng, người mua 2 được 0 dòng, khớp với bài.
- **AIF:** tự viết alpha–beta; cả ba cây cho số lá đã xét là 7 / 5 / 4 / 5, khớp với bài.
- **BCH:** dựng cây SHA-256 1024 lá, tính các vị trí anh em của lá 357, kiểm bằng chứng → True. Đếm 2047 lần băm, khớp.
- **BNK:** mô phỏng commit được [1,1,2,1,1] và [1,1,0,1,1], khớp. Riêng murmur2 thật của Kafka cho phân vùng 2 chứ không phải 1 (xem bảng 1).
- **CLD:** tự mô phỏng với 10 hạt giống: chọn 1 máy cho tải lớn nhất 228–249, chọn tốt hơn trong 2 luôn ra 202; hạt giống 1 cho đúng 243/202. Khớp.
- **CS112:** mô phỏng mảng động cho 15/31/1023 lần chép, khớp. Chèn đầu danh sách ra 4,7,3,9; làm sai thứ tự gán thì nút tự trỏ vào chính nó. Cả hai khớp.
- **CS115:** dưới tràn (0,1^400 = 0; số dương nhỏ nhất có 323 chữ số 0 sau dấu phẩy), các giá trị e, ln, đạo hàm bằng bước nhỏ, bảng đồng xu. Tất cả khớp.
- **CSA, CAS, CLC, AGT:** toàn bộ phép tính khớp.
- Mã Go Fiber ở ACB không chạy được, chỉ đọc. `res.RowsAffected() == 0` hợp lệ nếu dùng pgx (`CommandTag.RowsAffected() int64`); với `database/sql` dòng này không biên dịch được. Bài không nói dùng driver nào, nên tôi không báo.

## 5. Nhận xét chung

- Điểm mạnh: không phát hiện MUST nào. Tôi tự tính lại 162 con số và chạy lại toàn bộ đoạn mã chạy được, tất cả khớp. Gần như mọi bài có “kiểm bằng đường khác” (đếm trên 1000 câu, tính bằng giây, dựng gốc kiểu khác).
- Điểm mạnh: phần lỗi thường gặp có cả lỗi của người đã đi làm, kèm số liệu (BNK max.poll, CLD trọng số 2:2:1, AGT tăng số lần sinh, CS112 xin thêm 1 ô). P6 đạt ở 10/11 bài.
- Điểm mạnh: bài sự cố CAS L06 khớp từng mốc giờ với `sources_L06.md` [S17]. Số minh hoạ được ghi rõ là minh hoạ.
- Yếu lặp lại 1 (P1, 9/11 bài): thuật ngữ then chốt bị dùng trước khi giảng, hoặc chỉ dẫn về bài trước (lũy đẳng, Pod, lõi, tác tử, khối, OFS/HTTP 409). Người chỉ xem một video sẽ bị kẹt.
- Yếu lặp lại 2: hai bài tổng hợp/phỏng vấn (ACB L04, CLC L11) hứa trong tiêu đề hoặc objective nhiều hơn phần thực dạy (máy trạng thái, rà theo sáu trụ cột). Quiz của hai bài này dễ hoặc có lời giải chỉ một dòng.
- Yếu lặp lại 3: hình cơ chế có lỗi ngữ nghĩa nhỏ: chiều mũi tên (CAS), nhãn lệch hàng (CLC), nhãn không khớp tên dùng trong lời đọc (AIF thiếu nhãn B/C/D, BCH lẫn đánh số 0/1).
- Yếu nhỏ: số minh hoạ phụ thuộc cách cài đặt ẩn mà không ghi rõ (BNK dùng crc32 trong khi Kafka dùng murmur2). Quiz của CS112, CS115, CSA chỉ dừng 8 giây.
