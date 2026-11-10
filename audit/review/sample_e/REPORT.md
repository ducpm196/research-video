# Đọc mẫu độc lập đợt E — chuẩn xác + đủ sâu cho người mất gốc (2026-11-10)

**Câu hỏi của người dùng**: video và giáo án đã đủ chuyên sâu cho người mới và người mất gốc chưa; đã đủ chuẩn xác, ít sai sót chưa.

**Cách rút mẫu**: mỗi khoá rút một bài bằng `random.Random(20261111).choice(sorted(lessons/<khoá>/L*.yaml))`, bỏ 84 bài đã có trong mẫu C và mẫu D. Kịch bản rút mẫu nằm ở scratchpad (`sample_e.py`); chạy lại kịch bản này tái tạo đúng danh sách bài của mẫu C và D đã công bố.

**Người đọc**: 4 tác tử AI mới, chỉ đọc. Tiêu chí ở `BRIEF.md`:
- Phần A chấm chuẩn xác, giữ đúng MUST/SHOULD của mẫu C/D.
- Phần B chấm độ sâu cho người mất gốc, gồm 7 mục P1–P7, mỗi mục 0/1/2 điểm.

Mỗi tác tử tự tính lại bằng Python mọi con số và chạy thử mã: Python, sqlite3, javac/java. Mỗi bài xem ít nhất 5 khung hình của video đã dựng. Chi tiết từng bài ở `part_1.md` … `part_4.md`.

## 1. Chuẩn xác

| | Mẫu C (09-11, trước đợt C) | Mẫu D (10-11, sau đợt C) | **Mẫu E (10-11, sau đợt D)** |
|---|---|---|---|
| Bài có MUST | 5/42 = 11,9% (5,2–25,0%) | 2/42 = 4,8% (1,3–15,8%) | **2/42 = 4,8% (1,3–15,8%)** |
| Số đã tính lại | — | mọi số | ≈ 680 số, **tất cả khớp** |

Ghi chú về mẫu E:
- Hai MUST là SDP L02 và GFX L12. Tác tử xếp GFX L12 vào SHOULD; người điều phối nâng lên MUST, vì màn hình gán một con số sai cho một phương án.
- Ước tính trên toàn kho: khoảng 9–104 trong 656 bài có MUST (Wilson 95%).
- Bài có ít nhất một phát hiện chuẩn xác (MUST hoặc SHOULD) là 18/42. Mẫu C là 16/42.

**MUST (CONFIRMED, người điều phối đã kiểm trên tệp thật và đã sửa):**
- **SDP L02**:
  - Lỗi: lớp `TaiKhoan` trên màn hình thiếu `nap`, trong khi bảng và quiz dùng "nạp 50", "nạp 30" (chạy nguyên văn báo `AttributeError`). `checks` gọi `alg.Account` chứ không gọi lớp đang hiện, nên cổng kiểm không bắt được.
  - Đã sửa: thêm `nap` (kiểm số tiền dương), sửa lời đọc bước 1, thêm một check `exec` chạy **nguyên văn** lớp trên màn hình (250 / 150 / 100).
- **GFX L12**:
  - Lỗi: khung ② ghi "đẩy n = 0,5 m (hoặc dùng độ sâu đảo ngược 32 bit) → sz = 0,12 m". Con số 0,12 m chỉ đúng cho n = 0,5 m với 24 bit (0,1192); độ sâu đảo ngược dấu phẩy động cho bước khoảng 9·10⁻⁵ m.
  - Đã sửa: "đẩy n = 0,5 m, vẫn 24 bit". Nhãn "hơn 8 ô" (hình chỉ vẽ khoảng 3 ô) đổi thành "1 m ÷ 0,12 m ≈ 8 ô (vẽ thu gọn)".

**Ngoài mẫu**, quét `ast.parse` toàn kho trên 72 khối mã trông giống Python (kịch bản `code_scan.py` ở scratchpad):
- 13 khối không biên dịch được, ở 12 bài. 11 bài là mã giả tiếng Việt hoặc đoạn trích chữ ký hàm, cố ý viết như vậy.
- **SDP L04** là lỗi thật: `class CaPhe:   def gia(self): return 30` viết trên một dòng, cùng kiểu lỗi SDP L05 ở mẫu D. Đã tách thành hai dòng và thêm check chạy nguyên văn.

**SHOULD: 22 mục ở 17 bài.** Đã sửa 1 mục (nhãn "8 ô" của GFX L12); 21 mục ở 16 bài còn lại **chưa sửa**. Danh sách đủ ở các tệp part:
- HCI L10: "giảm hàng chục/hàng trăm lần" sai, vì mức giảm là 1/p.
- INT L02: tiêu đề "5,000"; "50 triệu" không nguồn; mục tiêu "xử lý triệt để" bài không dạy.
- BNK L07: "TK-1001 → phân vùng 1" là kết quả của crc32 minh hoạ; murmur2 của Kafka cho phân vùng 2. Cần ghi rõ "hàm băm minh hoạ".
- SEP L01: quy tắc "c > N thì phần lớn lộ" sai khi N < c < 1,44N.
- SEC L15: "giữ mua chứng chỉ 1 năm". Theo CA/B Forum SC-081, chứng chỉ cấp từ 3/2026 chỉ hiệu lực tối đa 200 ngày (PLAUSIBLE, cần mở nguồn).
- RLN L12: ví dụ ôn nền thiếu lợi nhuận ±2.
- PLC L00: `@` không phải lỗi từ vựng trong Python.
- DBS L17: "vẫn cần bảng bóng" quá tuyệt đối.
- BCH L02: lẫn đánh số 0/1.
- CAS L06: mũi tên ngược chú giải.
- CLC L11: nhãn lệch; mục tiêu "rà sáu trụ cột" không làm.
- ACB L04: mục tiêu "máy trạng thái, ma trận mã lỗi" chỉ được nhắc; "25 ms" đo từ mốc ngoài quy trình.
- MLO L11: "chưng cất" chỉ có một câu.
- WEB L11 và RBM L17: tổng kết hoặc quiz rộng hơn điều bài chứng minh.
- DEN L08: mở đầu và Lỗi 1 mâu thuẫn nhẹ.

## 2. Độ sâu cho người mất gốc (P1–P7, 42 bài)

| Mục | TB /2 | 2 | 1 | 0 |
|---|---|---:|---:|---:|
| **P1 Nền: mọi thuật ngữ được giảng tại chỗ** | **1,02** | 9 | 25 | 8 |
| P2 Từng bước có lý do + thử số | 1,88 | 37 | 5 | 0 |
| P3 Hình cơ chế, khớp lời, đọc được | 1,74 | 32 | 9 | 1 |
| P4 Ví dụ làm tay được | 1,95 | 40 | 2 | 0 |
| P5 Quiz kiểm hiểu, lời giải từng bước | 1,86 | 36 | 6 | 0 |
| P6 Chuyên sâu: vì sao, giới hạn, cách làm nghề | 1,88 | 37 | 5 | 0 |
| P7 Giáo án khớp, mục tiêu được dạy thật | 1,71 | 30 | 12 | 0 |

**Kết luận theo bài**: **ĐỦ 29/42 (69%, 54–81%) · GẦN 12 · CHƯA 1** (INT L02, 6 điểm: dày thuật ngữ Spring, chữ SVG nhỏ, quiz nhớ chữ).
- GẦN: ACB L04, CLC L11, DAN L00, DBS L17, DSY L15, DVO L04, GFX L12, RBM L17, RLN L12, SDP L02, SWF L06, TOC L08.
- Video thật: thời lượng trung vị 8,0 phút (5,8–18,5). Khoảng 230 khung hình đã xem; lỗi hiển thị chỉ thấy ở HCI L10 (chữ vàng/trắng trên nền kem, khung 00023), INT L02 (chữ SVG quá nhỏ, 00020), CLC L11 và GFX L12 (nhãn lệch, tràn).

**Điểm yếu lặp lại** (theo thứ tự, gộp từ 4 phần):
1. **P1: thuật ngữ phụ chưa giảng tại chỗ.** Chỉ 9/42 bài sạch. Thường gặp ở phần lỗi hay gặp, quiz, và bài tình huống/hành trình. Ví dụ: "phần dư", "trị riêng" (RBM), "văn phạm phi ngữ cảnh", "không đơn định" (TOC), "luồng", "khoá", "trường" (SDP), "phương sai" (RLN, có trong cả tựa bài), "lũy đẳng", "Pod", "OFS", "HTTP 409". Đây là cùng phát hiện của mẫu D (36/55 dòng SHOULD), nên vẫn là việc hàng đầu (BN-0039).
2. **P7: tiêu đề hoặc mục tiêu hứa nhiều hơn phần dạy kỹ.** Mục tiêu phụ chỉ có một câu, không có ví dụ số hay câu quiz: MLO, INT, ACB, CLC, ROB, WEB, SWF, DAN, DEN, DSC, ESY.
3. **P3: 75% bài toàn kho (495/656) chỉ có đúng một hình cơ chế.** Mẫu thấy hình yếu đúng chỗ cần nhất: SEC không có hình cho Heartbleed đọc quá biên, SWF và DSY chỉ có hộp hoặc trục thời gian. Có vài lỗi nhãn và chiều mũi tên.
4. **Mã trên màn hình không được chạy nguyên văn.** `checks` gọi hàm trong `checklib`, không gọi đoạn mã người học thấy. Đây là lỗi hệ thống sinh ra SDP L02, L04, L05.

## 3. Điều cổng máy không đo được
`pedagogy_scan.py` hôm nay cho 656/656 bài **ĐỦ** theo E39; ngày 31-10 chỉ có 6 bài. Thời lượng ước tính trung vị 10,3 phút. Nhưng mẫu E cho thấy E39 chỉ đo **cấu trúc**: có ôn nền, có hình, có ≥ 4 bước số, có quiz. E39 không đo được thuật ngữ đã được giảng chưa (P1), và cũng không đo được mục tiêu có được dạy thật không (P7).

## 4. Đề xuất (theo thứ tự lợi ích / công)
1. **Cổng mới "mã trên màn hình chạy được"**: trích khối `class="code"` có khai `lang: python` và chạy nguyên văn. Đây là việc nhỏ, chặn được cả một loại lỗi MUST.
2. **Đợt "định nghĩa tại chỗ" (BN-0039)** trên 572 bài ngoài ba mẫu. Kèm theo đợt này: mục tiêu nào chỉ được nói thì thêm một ví dụ số hoặc một câu quiz (P7). Sửa luôn 21 SHOULD còn lại của mẫu E.
3. Thêm hình cơ chế thứ hai cho bài chỉ có một hình, ưu tiên bài tình huống và hành trình.
4. Rút mẫu F sau bước 2 để đo lại P1 và MUST.

## 5. Đã làm trong phiên này
- Sửa SDP L02, SDP L04, GFX L12: lint 0 FAIL/0 WARN; render 0 vấn đề; `verify_sdp` 36 PASS/0 FAIL; `verify_gfx` 19/19.
- Dựng lại 3 bài (log `audit/review/sample_e/rebuild_e.out`).
