# Rà soát bản thảo giáo án CS112 trước khi làm video

- Đối tượng: bản thảo của người dùng (sha256 16 ký tự đầu `2065aea9accb6dd3`, 25 bài L00–L24), lúc rà soát nằm ở `curriculum/CS112.yaml`; bản sao nguyên văn: `audit/cs112/CS112_ban_thao_goc.yaml`. Lộ trình đã sửa để làm video: `curriculum/cs112.yaml` (người dùng đã đổi tên lộ trình mới thành tên này, thay chỗ bản thảo, 2026-10-27).
- Kiểm bằng máy: `audit/cs112/verify_cs112.py` (sympy + mô phỏng + vét cạn). Lần chạy 2026-10-27: **32 PASS · 15 FIX · 0 FAIL** (OBSERVED; 13 FIX lúc đầu, thêm 2 mục C29, C29b sau khi đọc file .tex).
- Quy ước nhãn (evidence-gated-work): OBSERVED = máy chạy/đọc thấy trong phiên này; CITED = có nguồn tra được; INFERRED = suy luận; NOT_VERIFIED = không kiểm được.

## 1. Nguồn: có gì trên máy, thiếu gì

| Khoá nguồn trong bản thảo | Có trên máy? | Hệ quả cho video |
|---|---|---|
| BTL_M — báo cáo BTL `[CS112.F31.LT.TTNT][BTL] PhamMinhDuc_25410035.pdf` (`13b808b57726a012`) | **Có** (`D:\TTNT\MonHoc\Toan\BaiTapLon\4_Report\`) | Nguồn chính cho bài nhân chuỗi ma trận và bài BTL; mọi số trong báo cáo đã kiểm lại (C25) |
| `YeuCauBaiToan.md` (`ed6c4bb863f7f5aa`), `BanChiDan.md` (`e9b98a7ce326ed6f`) | Có | Văn bản kế hoạch do AI soạn, **tự nhận** dựa trên thông báo của giảng viên nhưng không kèm thông báo đó. Có lỗi toán (C25b). Chỉ dùng làm gợi ý, không làm bằng chứng |
| SYL (đề cương), B01–B10 (video buổi học), SL_DQ, SL_TT (slide), CK25 (đề thi cuối kỳ), HW1_2 (bài tập về nhà), “Useful Formulas” | **Không có** (quét `D:\`, 2026-10-27) | NOT_VERIFIED. Các phát biểu chỉ dựa vào nguồn này (cấu trúc đề, thang điểm, quy tắc chấm) **không được khẳng định trong video** |
| TLTK1 Levitin, TLTK2 CLRS, “TLTK3” | Không có bản điện tử; “TLTK3” không được định nghĩa trong bản thảo | Kết quả chuẩn của giáo trình được **kiểm lại bằng máy** (bảng §2) thay vì trích nguồn |

## 2. Bảng sửa: Sai / Thiếu điều kiện / Thuật ngữ

| Mã | Bài bản thảo (→ bài video) | Bản thảo viết | Bằng chứng (verify_cs112.py) | Video phải nói |
|---|---|---|---|---|
| C2b | L00 (→ L00) | Tổng so sánh vòng trong = (n² + 8n + 4)/4 | Đúng với n chẵn (mô phỏng n = 2..58); n lẻ ra (n² + 8n + 3)/4 | Ghi rõ “với n chẵn”, cho thêm công thức n lẻ hoặc chỉ dạy n chẵn |
| C4b | L00 (→ L00) | “tổng điều hoà ln(n)” | H_n − ln n → 0,5772 (n = 10⁶) | H_n ≈ ln n + 0,577…; nói đúng: H_n thuộc Θ(log n), ln n < H_n ≤ ln n + 1 |
| C6b | L01 (→ L03) | “mảng động chèn cuối O(1) trung bình (amortized)” | Tổng chép < 2n (n < 5000); một lần chèn tệ nhất chép n phần tử | “Khấu hao” = chia đều trên cả dãy thao tác, tất định; KHÔNG phải trung bình xác suất |
| C8 | L03 (→ L05) | “cây nhị phân đầy đủ: h = ⌊log₂ n⌋” | Đúng cho cây **hoàn chỉnh** (complete) | Dùng đúng thuật ngữ “cây hoàn chỉnh”; cây “đầy đủ” (mọi nút 0 hoặc 2 con) có thể cao tới (n − 1)/2 |
| C10 | L06 (→ L01) | Phương pháp giới hạn: L = 0 → o, c → Θ, ∞ → ω | f(n) = n·(2 + (−1)ⁿ): Θ(n) nhưng f/n không có giới hạn | Chỉ dùng khi giới hạn tồn tại; không có giới hạn thì quay về định nghĩa (c, n₀) |
| C11b | L07 (→ L02) | “Chuỗi 15 bậc” | Bản thảo liệt kê 16 hàm; 15/15 cặp kề đúng thứ tự (giới hạn tỉ số = 0) | Gọi là “chuỗi tăng trưởng”, không gắn số 15 |
| C13 | L07 (→ L02) | “5·lg(n+100)^10 < ln² n” | Hiểu là lg((n+100)¹⁰) thì đúng; hiểu là (lg(n+100))¹⁰ thì SAI chiều | Luôn viết ngoặc rõ; dạy cách đọc đề hai nghĩa |
| C16b | L10 (→ L10) | T(n) = 2T(n/2) + 2 ⇒ 2n − 2 | Cần T(1) = 0; T(1) = 1 cho 3n − 2 | Nêu điều kiện cơ sở T(1) = 0 |
| — | L10 (→ L10) | Mã findMax, “a = 1 vì if-else” | Mã gốc không có trên máy (NOT_VERIFIED) | Video tự viết hàm minh hoạ, dạy nguyên tắc: đếm lời gọi **thực sự chạy** trên một nhánh, không đếm dòng mã |
| C18 | L12 (→ L12) | Định lý thợ TH3 “a f(n/b) ≤ c f(n)”; “b phải là hằng số chia nguyên” | — | TH3 cần **c < 1**; b > 1 là hằng số thực; nêu khe hở giữa các TH (2T(n/2) + n log n = Θ(n log² n), C18c) |
| C19b | L13 (→ L13) | “Sắp xếp trước để tìm Min/Max trong O(1)” | Sắp xếp Θ(n log n) > tìm min/max n − 1 phép so sánh | Ví dụ đúng của biến đổi để trị: kiểm phần tử trùng Θ(n²) → Θ(n log n) |
| C20 | L14 (→ L14) | Quên trả lại đánh dấu “chỉ tìm được 1 nghiệm” | Đúng cho liệt kê hoán vị (n = 1..7): n! → 1 | Nói rõ “trong bài liệt kê hoán vị”; tổng quát là **bỏ sót nghiệm** |
| C21 | L15 (→ L15) | Rút gọn hàng 21, cột 4, cận 25 nhưng **không ghi ma trận** | Ma trận 5×5 kinh điển cho đúng các số này; tối ưu vét cạn 28 (1→4→2→5→3→1) | Hiện đủ ma trận; bẫy “lấy min cột trên ma trận gốc” cho 18 ≠ 4 (C21b) |
| C23b | L17 (→ L17) | “duy nhất xếp theo f_i là đúng” | “Bắt đầu muộn nhất” (duyệt ngược) cũng tối ưu (400 bộ ngẫu nhiên) | “Kết thúc sớm nhất là tiêu chí đã chứng minh tối ưu”; bắt đầu sớm nhất và ngắn nhất có phản ví dụ |
| C24b | L19 (→ L19) | Bài “6 + 0 × 6 + 0,1” gọi là “Nhân chuỗi ma trận (MCM)”; công thức chỉ lấy max | Hai bài toán **khác nhau**; chỉ-lấy-max đúng khi số ≥ 0 và chỉ có +, × (300 bộ); có phép trừ thì sai (0 − 0 × 0 − 1) | Tách hai bài toán; nêu điều kiện của công thức max |
| — | L19 (→ L19) | “Bắt buộc chỉ số 1-based để khớp slide” trong khi ví dụ dùng DP[0][3] | Tự mâu thuẫn; slide không có trên máy | Không nêu quy định; mỗi ví dụ ghi rõ chỉ số bắt đầu từ đâu |
| C25b | L23 (→ L23) | Vét cạn MCM O(4ⁿ/n^1,5); testcase “p = [6, 0, 6, 0,1]” | Hàm đệ quy vét cạn gọi đúng 3^(n−1) lần (báo cáo BTL cũng ghi Θ(3ⁿ)); 4ⁿ/n^1,5 là số **cách** đặt ngoặc (Catalan); p có 0 và 0,1 không là kích thước ma trận | Θ(3ⁿ) lời gọi; phân biệt số cây với số lời gọi |
| C27b | L21 (→ L21) | Thiếu điều kiện không âm “làm miền nghiệm vô hạn” | Miền vô hạn thật, nhưng z vẫn ≤ 280 vì 15x₁ + 10x₂ = 5(x₁ + x₂) + 5(2x₁ + x₂) | Không nói “ra kết quả sai” cho ví dụ này; nói đúng: miền đổi, cần kiểm lại |
| — | L22 (→ L22) | Tên bài có “Fourier-Motzkin” nhưng nội dung không có | — | Bỏ khỏi tên bài (không dạy thứ không có trong bài) |

Các ví dụ số còn lại của bản thảo **đúng** (PASS): C1, C2, C3, C4, C6, C7, C7b, C9, C11, C12, C13b, C14, C15, C16, C16c, C17, C18b, C18c, C19, C20, C21, C21b, C22, C22b, C23, C24, C24c, C25, C26, C27, C28.

## 3. Lỗi cấu trúc lộ trình

1. **Ký hiệu dùng trước khi dạy** (luật “ký hiệu trước khi dùng”): bản thảo dạy O, Θ, Ω ở L06 nhưng L01–L05 (mảng, ngăn xếp, cây, băm, đồ thị) đã dùng O(1), O(log n), O(V + E). Sửa: đưa hai bài tiệm cận lên ngay sau bài toán nền (→ L01, L02), các bài cấu trúc dữ liệu lùi thành L03–L07. Các bài từ L08 giữ số.
2. **Quy tắc chấm / thang điểm không kiểm được**: “Cô Thương trừ sạch điểm”, “2,5 điểm mỗi câu”, “Mục 8 quan trọng nhất”, “40% + 10%”, “tờ A4 hai mặt”, “90 phút”. Nguồn (thông báo, đề thi) không có trên máy ⇒ NOT_VERIFIED. Video **không** khẳng định; bài BTL dạy chuẩn mực chuyên nghiệp có lý do riêng (so sánh nhiều thuật toán có đo đạc, ghi minh bạch phần AI làm và phần tự kiểm chứng), bài tổng ôn dạy theo dạng bài và bẫy toán học đã kiểm.
3. **Luật E29** (người học chỉ có video): bản thảo nhiều chỗ “slide”, “giáo trình”, “đề thi cô…” — không đưa vào lời/màn hình.

## 3b. Nguồn bổ sung: `giao-an-dsa-cs112-toan-dien.tex` (người dùng thêm 2026-10-27, sha256 `81f6c4b1691a7b5f`)

Bản LaTeX của cùng bản thảo (cùng cấu trúc L00–L24 và cùng các lỗi C2b, C11b, C13…, C18 “c < 1”), với hai điểm mới (OBSERVED):

| Mã | Dòng | Nội dung | Bằng chứng | Xử lý trong video |
|---|---|---|---|---|
| T1 | 87–380 | Phần lớn dấu `$` bị mất khi sinh file: `(1)$`, `11\text{…}11`, `(n) \in O(…)$`… — công thức không đọc/biên dịch được | đọc trực tiếp | Không dùng làm nguồn chữ; chỉ dùng nội dung đã kiểm |
| C29 | 221–227 | Mã `findMax` ba nhánh: so `a[m]` với `a[m+1]` rồi chỉ đi một nửa | Chỉ đúng với dãy **đơn đỉnh** (tăng rồi giảm); sai 385/1000 mảng ngẫu nhiên; `[5, 1, 2, 3]` → 3 (thật 5) | L10 phân tích hàm này kèm điều kiện đơn đỉnh |
| C29b | 230–232 | Tệ nhất (mọi phần tử bằng nhau) `T(n) = 2T(n/2) + 2` → `2n − 2` | Đúng khi chỉ đếm 2 phép so sánh điều kiện; đếm cả `max` thì `3n − 3`; tốt nhất (dãy tăng) `log₂ n` | L10 nói rõ đếm phép so sánh nào |
| — | 366–381 | Bảng “phân bổ 90 phút / 2,5 điểm mỗi câu” | Không có đề thi trên máy | NOT_VERIFIED — không đưa vào L24 |

## 4. Bảng đổi số (bản thảo → video)

| Bản thảo | Video | Ghi chú |
|---|---|---|
| L00 | L00 | |
| L06 | L01 | đưa lên trước (mục 3.1) |
| L07 | L02 | |
| L01 | L03 | |
| L02 | L04 | |
| L03 | L05 | |
| L04 | L06 | |
| L05 | L07 | |
| L08–L24 | L08–L24 | giữ số |

checked_at: 2026-10-27 (chạy lại: `.venv/Scripts/python audit/cs112/verify_cs112.py`).
