# Giáo án bản 3 (34 bài) + bài mới L03 “Hệ phương trình tuyến tính” — 2026-10-24

Phạm vi (yêu cầu người dùng): “bổ sung đầy đủ các topic đang cân nhắc như t-SNE, NMF,… hoàn thiện giáo án đầy đủ, chuẩn xác. Sau đó tiếp tục làm video bài giảng tiếp theo.”
Nhãn: OBSERVED = chạy trong phiên này; CITED = nguồn ngoài có ngày truy cập; INFERRED = suy luận, chưa kiểm.
Môi trường: Python 3.13.5 (`.venv`), Windows 11, KaTeX 0.16.11, giọng vi-VN-NamMinhNeural, ASR faster-whisper small + medium.

## 1. Nút thắt hợp đồng

| ID | Chưa xác định / chưa kiểm | Việc phụ thuộc | Bằng chứng đóng | Trạng thái |
|---|---|---|---|---|
| B21 | “Các topic đang cân nhắc” gồm những gì; nguồn có chủ đề nào mà lộ trình còn thiếu | Lộ trình bản 3 | Quét ~110 từ khoá trên 13 văn bản PDF + tex (`topic_scan.py`), đọc ngữ cảnh từng chủ đề. Kết quả ở SYLLABUS_CS115.md §6.2 | CLOSED |
| B22 | Ghi nhận cũ “lagrange: 0 kết quả” | Nguồn của bài Lagrange/KKT | Đếm lại: 1 lần trong PR25 → ghi nhận cũ **FAILED**, đã đính chính ở SYLLABUS_CS115.md | CLOSED |
| B23 | Bài 4, 5, 8 (bản 3) dùng giải hệ phương trình mà chưa bài nào dạy (`grep "khử\|Gauss" lessons/` = 0) | Thứ tự học | Thêm L03, gắn `requires: [L03]` cho L04, L05, L08, L11, L16, L18 | CLOSED |
| B24 | Chèn bài làm lệch “bài N” trong 8 video đã làm | Lời đọc L00–L08 | Ánh xạ bằng script + đọc lại 106 dòng + sửa tay L00/L02/L04; lint E24 mới; build lại 9 video (verify PASS cả 9) | CLOSED |
| B20 | Cách đọc “logarit” | L12 | Chưa làm L12 | **OPEN** (ghi ở `fix` của L12) |
| B25 | t-SNE: không có trong nguồn môn học | L32 | Người dùng yêu cầu thêm; ghi rõ “ngoài nguồn” trong `source`; trích bài báo gốc (CITED) | CLOSED (quyết định của người dùng) |

## 2. Lộ trình bản 3 (OBSERVED: `lv.py curriculum` → 34 bài, 9 đã có đặc tả, 0 lỗi, 14:24:32Z)

Thêm 4 bài: **L03** hệ phương trình (LA24, BT1), **L21** đánh giá mô hình phân loại (ML24), **L31** NMF (GT24; Lee & Seung, Nature 401 (1999) 788–791, CITED 2026-10-24, no revision given), **L32** t-SNE (ngoài nguồn; van der Maaten & Hinton, JMLR 9 (2008) 2579–2605, CITED 2026-10-24). Dời cây quyết định lên L28. Bổ sung `fix` từ nguồn mới: hồi quy đa thức (L18, L19), Bernoulli/Categorical/Dirichlet (L13, L17), Lagrange trong MLE (L17, L24), hàm kích hoạt/khởi tạo/dropout/triệt tiêu gradient (L23, L19), gradient checking (L22), sequential vs batch (L09), entropy (L20). `not_included`: CNN/RNN, học tăng cường, UMAP/ICA/autoencoder/boosting — kèm lý do.
Phép kiểm `orig`/`prev` so với bản sao lưu bản 2 (`cur_v3_check.py`): lần đầu bắt được 8 trường `orig` sai → đã sửa → 0 lỗi.

## 3. L03: kết quả (OBSERVED)

| Hạng mục | Kết quả | checked_at |
|---|---|---|
| lint | 0 FAIL, 0 WARN, 44 PASS; 37 phép kiểm sympy; 112 công thức KaTeX; 13 scene; ký hiệu mới: `aug` [A \| b], `rank`, `iff` | 14:24Z |
| Trích dẫn | 2 step nhắc bài sau (`forward_ref`, ở in_ai/recap); 11 câu nhắc bài trước (bài 2), đều nói lại nội dung (E23 sạch sau khi sửa 3 câu) | 14:24Z |
| build + verify | `out/L03/L03.mp4` 703,53 s (11,7 phút), 126 khung, verify PASS | 14:2xZ |
| ASR | 126 câu, độ khớp TB 0,973, **gắn cờ 0, chưa xem xét 0** (lượt đầu 2 cờ do tên chữ cái “của A”, “A x” → viết lại “ma trận A”, “A nhân x”) | 14:2xZ |
| render | 0 vấn đề (lượt đầu tràn ở scene gauss → `clear: true` + chép lại ma trận bậc thang) | 13:07Z |

Thiết kế: ví dụ khởi động dùng lại **đúng hệ của bài 2** (2x + y = 5, x + y = 3 → (2, 1), không cần nghịch đảo); ví dụ chính 3×3 nghiệm (1, 2, 3); trường hợp vô số nghiệm dùng lại **ma trận S của bài 2** (hai nghiệm (3, 0), (1, 1) chính là hai vector S biến thành (3, 6)); hạng nối với “khả nghịch ⇔ hạng đầy đủ”; ánh xạ tuyến tính nêu ngắn (S(x, y)ᵀ = (x + 2y)(1, 2)ᵀ, kiểm bằng sympy). Lời đọc không nói tên “Gauss” (từ ngoại chưa probe).
Phát biểu “tìm nghịch đảo tốn công hơn khử” (Lỗi 4): đếm phép nhân/chia bằng `flops.py` — nghịch đảo (Gauss–Jordan) tốn 3,2× / 4,4× / 5,6× với n = 3 / 10 / 50, hai cách cho cùng nghiệm (OBSERVED). Bài không nêu tỉ lệ cụ thể.

**Xem bằng mắt**: khung 23 (ký hiệu [A | b]), 40 (bước 1–2 khử), 46 (thế ngược), 55 (hình ba trường hợp — sửa: đường thẳng vượt trục), 65 (vô nghiệm/vô số nghiệm — sửa: chữ “đúng” rớt dòng), 79 (quy tắc hạng), 87 (nối bài 2 + ánh xạ tuyến tính), 104 (lỗi 3–4), 115 (đáp án quiz — sửa: dấu trừ sau vạch đứng, bảng quá chật), 125 (khung cuối). L00 khung 88 (bản đồ khoá học mới), L02 khung 210 (câu “bài sau” mới), L04 khung 4 (hook nhắc bài 3).

## 4. Kiểm toàn bộ (OBSERVED, 14:24:05–14:24:34Z)

| Bài | Thời lượng | verify | ASR chưa xem xét |
|---|---|---|---|
| L00 | 649,87 s | PASS | 0 |
| L01 | 1131,97 s | PASS | 8 |
| L02 | 1123,73 s | PASS | 8 |
| L03 (mới) | 703,53 s | PASS | 0 |
| L04 | 897,8 s | PASS | 1 |
| L05 | 895,57 s | PASS | 4 |
| L06 | 878,5 s | PASS | 0 |
| L07 | 891,63 s | PASS | 0 |
| L08 | 825,03 s | PASS | 0 |

`tests/test_lint.py` 0 FAIL (gồm 2 ca E24 mới) · lint 9 bài 0 FAIL 0 WARN · `audit/verify_cs115_tex.py` 59/59 PASS · `curriculum` 34 bài 0 lỗi · không còn tiến trình pipeline chạy sót (`Win32_Process`).
Hai câu ASR mới phát sinh khi đánh số lại (L02 khung 210, L07 khung 25 “bài” → “bay”) đã được viết lại; ASR lượt sau: L02 về đúng 8 câu cũ, L07 về 0.

## 5. Còn mở (NOT_VERIFIED)

- Người nghe thật: L01 (8), L02 (8), L04 (1), L05 (4), L07 (3 câu “Hết-sen” đã ghi `asr_reviewed`), L08 (3 câu “Hết-sen”).
- L01 (18,9 phút) và L02 (18,7 phút) dài hơn khung 10–15 phút — có từ trước.
- BT1 là bản scan: chỉ đọc được dòng đề “Giải các hệ phương trình tuyến tính”, chưa OCR các hệ cụ thể.
- B20 “logarit” trước khi làm L12. Bài tiếp theo theo lộ trình: **L09** Gradient Descent, SGD, Momentum, Adam.
- Hiệu quả sư phạm với người học thật: chưa đo.
