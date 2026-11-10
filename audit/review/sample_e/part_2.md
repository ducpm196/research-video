# Mẫu E — phần 2: đã đọc 11/11 bài

Bài: CVI L02, DAN L00, DBS L17, DEN L08, DMS L08, DSC L02, DSY L15, DVO L04, ESY L05, EVT L01, GFX L12.
Với mỗi bài đã đọc: đặc tả YAML (show, say, checks, quiz), mục trong `curriculum/<khoá>.yaml`, `chapters.txt` cùng `_frames.txt` (để đổi số khung ra mốc thời gian), và 5 khung hình. Với DBS L17 và DSY L15 còn đối chiếu thêm `audit/<khoá>/sources_L*.md`.

## 1. Chuẩn xác

| Bài | Mức (MUST/SHOULD) | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng (phép tính/nguồn) | Đề xuất sửa | Tin cậy (CONFIRMED/PLAUSIBLE) |
|---|---|---|---|---|---|---|
| CVI L02 | — | | | không phát hiện lỗi | | |
| DAN L00 | — | | | không phát hiện lỗi | | |
| DBS L17 | SHOULD | stage5, step 2 (bảng “việc cần làm → công cụ hợp”) | “đổi kiểu, thêm chỉ mục, thao tác không có trong danh sách tức thì → bảng bóng chép bù, có điều tiết”; lời đọc: “vẫn cần bảng bóng chép bù” | Khẳng định quá tuyệt đối. Theo MySQL 8.0 Reference Manual, mục Online DDL Operations, phần Index Operations: tạo chỉ mục phụ chạy kiểu In Place, không dựng lại bảng và vẫn cho ghi đồng thời. Như vậy “thêm chỉ mục” không bắt buộc phải dùng bảng bóng. Người làm nghề vẫn hay dùng công cụ bảng bóng cho việc này, nhưng là để tránh bản sao trễ, không phải vì không có cách nào khác. | Đổi “vẫn cần” thành “thường dùng (nhất là khi có bản sao)”, hoặc bỏ “thêm chỉ mục” khỏi dòng đó | PLAUSIBLE |
| DEN L08 | SHOULD | hook ↔ pitfalls Lỗi 1 | hook: “Không ai làm sai: các sự kiện đi qua các phân vùng khác nhau”; Lỗi 1: “Gửi sự kiện không có khoá, hoặc khoá sai (mất thứ tự)” | Hai cảnh mâu thuẫn nhẹ. Tình huống mở đầu, ba sự kiện của đơn 42 rơi vào nhiều phân vùng, chính là Lỗi 1 mà bài gọi là “lỗi” (chọn sai khoá). | Ở hook nói rõ “không ai viết sai mã — chỉ là chọn khoá chưa đúng”, hoặc bỏ câu “không ai làm sai” | PLAUSIBLE |
| DMS L08 | — | | | không phát hiện lỗi | | |
| DSC L02 | — | | | không phát hiện lỗi | | |
| DSY L15 | — | | | không phát hiện lỗi; mọi số liệu sự kiện đều khớp câu trích nguyên văn trong `audit/dsy/sources_L15.md` (BT06 §8, SP12 §3/§4.2.1/§5.4, SQ17 §1/§8) | | |
| DVO L04 | — | | | không phát hiện lỗi | | |
| ESY L05 | — | | | không phát hiện lỗi | | |
| EVT L01 | — | | | không phát hiện lỗi | | |
| GFX L12 | SHOULD | intuition, SVG, khung ② (khung hình 00019) | “② Sửa mặt cắt gần: đẩy n = 0,5 m (hoặc dùng độ sâu đảo ngược 32 bit) → Tại z = 1 000 m, sz = 0,12 m!” | Con số 0,12 m bị gán chung cho hai phương án. Tính lại: độ sâu đảo ngược dạng dấu phẩy động 32 bit, với n = 0,01, f = 10 000, tại z = 1000 m, cho giá trị độ sâu d ≈ 9,0·10⁻⁶. Khoảng cách giữa hai số float32 kề nhau ở đó là 9,09·10⁻¹³; độ dốc dd/dz ≈ 1,0·10⁻⁸. Vậy bước ≈ 9,1·10⁻⁵ m, nhỏ hơn 0,12 m khoảng 1300 lần. | Bỏ “(hoặc dùng độ sâu đảo ngược 32 bit)” khỏi khung ②, hoặc ghi riêng “độ sâu đảo ngược: ≈ 0,1 mm” | CONFIRMED |
| GFX L12 | SHOULD | intuition, SVG, khung ② (khung hình 00019) | Chữ ghi “Cách nhau hơn 8 ô lượng tử → Tách biệt hoàn toàn!”, nhưng hình vẽ hai vạch ở x = 675 và x = 845, mỗi ô rộng 55 px | Nhãn hình lệch với hình: (845 − 675) / 55 ≈ 3,1 ô, trong khi số đúng là 1 / 0,1192 ≈ 8,4 ô. Lỗi hiển thị: cả dòng chữ “…Tách biệt hoàn toàn!” tràn qua viền phải của khung xanh, và dòng “Cùng rơi vào 1 ô lượng tử 5,96 m → NHẤP NHÁY!” nằm đè lên viền trên của ô cam. | Vẽ 9 ô hẹp giữa hai vạch (hoặc ghi đúng số ô đã vẽ), thu ngắn chữ hoặc nới rộng khung | CONFIRMED |

Tổng: 0 MUST, 4 SHOULD.

## 2. Độ sâu cho người mất gốc

| Bài | Phút (từ chapters/srt) | P1 | P2 | P3 | P4 | P5 | P6 | P7 | Tổng | Mất gốc | Chỗ thiếu chính |
|---|---|---|---|---|---|---|---|---|---|---|---|
| CVI L02 | 11,7 | 2 | 1 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | P2: formula bước 2 “Phương sai của cả ảnh tách đúng thành hai phần, với mọi ngưỡng” chỉ được khẳng định rồi thử bằng số, không có lý do |
| DAN L00 | 6,4 | 2 | 2 | 2 | 2 | 1 | 1 | 1 | 11 | GẦN | P5: câu 1 chỉ là lọc dòng “mua”, gần như nhớ lại. P6: “câu hỏi quyết định” chỉ có một dòng ở Lỗi 3; nhật ký ví dụ không có giờ nên thành phần “múi giờ” không được làm thử. P7: mục tiêu “viết định nghĩa đủ chặt” không có lượt nào cho người học tự viết |
| DBS L17 | 14,3 | 0 | 2 | 2 | 2 | 2 | 2 | 2 | 12 | GẦN | P1: các từ chưa được giảng: “tổng kiểm”, “siêu dữ liệu / từ điển dữ liệu”, “cập nhật cuốn chiếu”; “bản sao” khi thì là bảng sao chép, khi thì là máy chủ bản sao (“bản sao trễ”) |
| DEN L08 | 7,3 | 1 | 2 | 2 | 2 | 2 | 2 | 1 | 12 | ĐỦ | P1: “băm” chỉ được dẫn về “bài 4”, không giải thích lại. P7: mục tiêu “chọn thời điểm ghi nhận vị trí đọc” chỉ có ở Lỗi 2, không có ví dụ số hay câu quiz |
| DMS L08 | 7,9 | 1 | 2 | 2 | 2 | 2 | 1 | 2 | 12 | ĐỦ | P1: “hoán vị” (“máy duyệt mọi hoán vị”) và ký hiệu “a R b” chưa giảng. P6: không nói vì sao luôn có phần tử tối tiểu để lấy; không có tình huống phụ thuộc thật có số liệu |
| DSC L02 | 7,4 | 1 | 2 | 2 | 2 | 2 | 2 | 1 | 12 | ĐỦ | P1: “biến”, “quan sát” chưa giảng (khung 00018). P7: mục tiêu “sắp dữ liệu về dạng gọn” chỉ có một bảng 2 dòng, không có bước chuyển hay bài tập |
| DSY L15 | 14,3 | 0 | 2 | 1 | 2 | 2 | 2 | 2 | 11 | GẦN | P1: các từ chưa giảng: “nguyên tử”, “thủ lĩnh”, “lược đồ”, “khoá–giá trị”, “phương ngữ SQL”, “máy phục vụ”. P3: hình duy nhất là trục thời gian (khung 00018); chỉ mục 3 tầng và khoảng giờ bất định chỉ có bảng, không có sơ đồ cơ chế |
| DVO L04 | 6,7 | 1 | 2 | 2 | 1 | 1 | 2 | 2 | 11 | GẦN | P4: mã băm SHA-256 và byte của tệp zip không thể làm lại bằng giấy bút. P5: câu 1 (“đổi một byte thì mã băm có đổi không?”) chỉ là nhắc lại câu đã nói nhiều lần. P1: “thăng hạng”, “bản ghi triển khai” chưa giảng |
| ESY L05 | 10,3 | 1 | 2 | 2 | 2 | 2 | 2 | 1 | 12 | ĐỦ | P1: “ADC / tín hiệu tương tự”, “vi điều khiển” chưa giảng (lời đọc chỉ nói “bộ chuyển đổi”). P7: mục tiêu “chọn tần số lấy mẫu” không có ví dụ chọn f_s bằng số, cũng không có câu quiz |
| EVT L01 | 7,7 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | P1: “triển khai”, “bảng đọc” chưa giảng |
| GFX L12 | 9,7 | 0 | 1 | 1 | 2 | 2 | 2 | 2 | 10 | GẦN | P1: các từ chưa giảng: “mặt cắt gần/xa” (bảng ký hiệu định nghĩa vòng), “bộ đệm độ sâu”, “dấu phẩy động / số mũ”, “lệnh vẽ, băng thông”. P2: formula bước 1 “lấy đạo hàm” mà không giảng đạo hàm. P3: hình ở khung 00019 không cho thấy “dồn vạch chia ở sát mắt” như tiêu đề hứa; nhãn lệch hình và chữ tràn khung (xem bảng 1) |

Phân bố: ĐỦ 6 (CVI, DEN, DMS, DSC, ESY, EVT), GẦN 5 (DAN, DBS, DSY, DVO, GFX), CHƯA 0.

## 3. Khung hình đã xem
- CVI L02: 00002, 00020, 00056, 00078, 00089
- DAN L00: 00015, 00021, 00053, 00061, 00065
- DBS L17: 00003, 00020, 00024, 00050, 00112
- DEN L08: 00002, 00017, 00028, 00046, 00059
- DMS L08: 00002, 00022, 00034, 00054, 00068
- DSC L02: 00002, 00018, 00022, 00049, 00060
- DSY L15: 00002, 00018, 00027, 00062, 00100
- DVO L04: 00022, 00037, 00051, 00062, 00068
- ESY L05: 00016, 00040, 00043, 00061, 00077
- EVT L01: 00001, 00019, 00033, 00054, 00065
- GFX L12: 00003, 00019, 00035, 00059, 00068

Lệch so với BRIEF: khung tổng kết chỉ được xem ở CVI, DAN và DVO. Với 8 bài còn lại, tôi ưu tiên xem khung hình cơ chế và khung quiz, còn phần tổng kết thì đọc từ YAML.
Hiển thị: chỉ GFX 00019 có lỗi (chữ tràn khung, chữ đè viền). 54 khung còn lại không thấy chữ tràn, đè hay bị cắt; cỡ chữ đều đọc được.

## 4. Mã đã chạy / số đã tính lại
- Số trên màn hình và trong lời đọc: tính lại khoảng 195 số bằng Python (scratchpad `sample_e/p2/cvi.py`, `misc.py`, `gfx.py`). Khớp cả khoảng 195 số, đúng tới số chữ số được ghi. Gồm:
  - CVI: bảng Otsu 4 ngưỡng, phương sai trong lớp, phép cân bằng biểu đồ, tỉ số 0,771 và 0,994.
  - DBS: 2500 s, 3,17 năm, 27,8 h, 0,41 GB, 1157,4 ngày, 16 phút 40 giây.
  - DEN: tồn đọng 1 200 000 → 480 s và 2400 s.
  - DSY: 2^34, 149, 2,03 và 14,08 phút, tỉ số 6,94, 80%, 1012,5.
  - ESY: 1 − 0,8^k, 25,8125, 0,354.
  - GFX: 5,9605, 0,1192, tỉ số 50,0, 0,1676 mức, 8,38 mức, 1,4901, 0,0745.
  - Các bài khác: các số còn lại.
- Mã đã chạy:
  - DSC: 4 truy vấn nối bằng sqlite3: (6, 900); nối trong 2 dòng; nối trái (3, 1); quiz 7 dòng; tổng theo khoá (900, 300). Tất cả khớp bài.
  - DVO: SHA-256 của `xin chao` và `xin chao!` → f9b197ffdaa4 và 67fac6d42ab9. Đóng gói zip ZIP_STORED ba lần → dac8a9bd655a, 9f8086ff674d, e31d85ce8d71; gói dài 128 byte, khác nhau 6 byte ở vị trí 10–12 và 66–68. Khớp bài.
  - DMS: liệt kê hoán vị → 5 thứ tự tô pô, 7 cạnh phủ, 12 cặp ước–bội. Khớp.
  - EVT: thử `schema_compat` trên 729 cặp lược đồ, khớp quy tắc đếm; chuỗi 3 phiên bản ở Lỗi 4 khớp.
  - GFX: mô phỏng float32 cho độ sâu đảo ngược → bước 9,1·10⁻⁵ m (là bằng chứng cho phát hiện SHOULD ở bảng 1).

## 5. Nhận xét chung
- Điểm mạnh: số liệu rất sạch. Khoảng 195 số được tính lại đều khớp, và các số trong hai bài hành trình (DBS, DSY) đều có câu trích nguồn đi kèm. Mỗi bài có một ví dụ làm tay trọn vẹn, có cảnh kiểm “bằng đường khác”, và có một lỗi của người đã đi làm kèm số cụ thể (tồn đọng 40 phút, tỉ trọng lệch 75/25, dọn kho xoá mất bản đang chạy…).
- Quiz nhìn chung kiểm hiểu: có dừng 15–20 giây, lời giải có bảng được/mất. Ngoại lệ: DMS chỉ dừng 8 giây cho câu vẽ biểu đồ; DAN và DVO có câu gần như nhớ lại.
- Yếu lặp lại nhiều nhất là P1, thuật ngữ chưa giảng. Ba bài được điểm 0 đều là bài “hành trình” hay “chuyên gia” (DBS, DSY, GFX): bài dài nhưng giả định người học đã quen từ của nghề.
- Yếu thứ hai là P7: một mục tiêu chỉ được nói ra, không có ví dụ số hay câu quiz đi kèm (DAN “viết định nghĩa”, DEN “thời điểm ghi nhận”, DSC “dạng gọn”, ESY “chọn tần số lấy mẫu”).
- Yếu thứ ba là P2 và P3 ở các chỗ cần suy luận toán: có bước được khẳng định mà không có lý do (CVI phân tích phương sai, GFX đạo hàm). Hình cơ chế đôi khi chỉ là trục thời gian hoặc nhãn lệch hình (DSY, GFX).
- Các bài tình huống chuyên gia dài 14 phút (DBS, DSY) đều đạt P4–P7 nhưng mất điểm vì quá nhiều từ chuyên môn chưa giải thích. Thêm một bảng từ vựng thứ hai, hoặc giảng tại chỗ, sẽ đưa cả hai bài lên ĐỦ.
