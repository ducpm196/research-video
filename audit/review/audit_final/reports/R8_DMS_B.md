# R8 DMS L11–L20 (lần đọc độc lập đầu tiên, P1 chặt): 10/10 bài — ghi lại bởi người điều phối từ tin nhắn của reader (a5568edeeb5310dfd)

## 1. Tóm tắt
MUST 0 (10/10). P1=2: 0/10 chắc+vừa khi tính mục 'Git Bash' lặp ở cảnh practice của cả 10 bài (loại B, vừa); nếu bỏ mục lặp này: 6/10 (L11, L14, L15, L16, L17, L18); tính cả yếu 0/10. Không có mục chắc. Mục vừa: 15 (10 Git Bash lặp + 5 riêng); yếu theo bài 3–6. P8=2 10/10; P9=2 10/10; spec khớp 10/10; SRT khớp `say` 10/10 (từng từ, 1965–2316 từ/bài); lab `cham.sh` ĐÚNG 10/10, 'Kết quả mong đợi' trên màn hình trùng `mong_doi.txt` 10/10; 9/9 chương trình 'Chạy thật' khớp từng dòng; 59 nhóm biểu thức (≈ 200 số) tính lại độc lập, 59/59 khớp (D₂₀ = 895 014 631 192 902 121, RSA, Euclid/Fibonacci, 585 năm, 2^16,9…); 55 khung hình: không tràn/đè/cắt, hình khớp lời đọc (Venn L12 27/14/7/13/7/3/3, Königsberg L16, K₄ và vương miện L18…). Chỉ một giọng `vi-VN-NamMinhNeural`. Mất gốc ĐỦ 9/10 (L12 GẦN, lên ĐỦ nếu bỏ Git Bash). SHOULD 7. Nguồn L20: mọi ngày/số trích khớp `audit/dms/sources_L20.md`; không có mạng nên 'chưa kiểm được nguồn gốc ngoài tệp đó'.

## 2. SHOULD (7)
| Bài | Cảnh | Trích | Vấn đề | Đề xuất | Tin cậy |
|---|---|---|---|---|---|
| L12 | three.1 | "16, 10, 6 là số chia hết cho 6, 10, 15; số 3 là số chia hết cho 30" (lời: "Số 3 là số chia hết cho cả ba, tức chia hết cho 30") | nghĩa đen sai (16 không chia hết cho 6): ý đúng là CÓ 16, 10, 6 số chia hết cho 6, 10, 15 và CÓ 3 số chia hết cho 30 | thêm 'có … số' / 'số lượng' | CONFIRMED |
| L17 | example.2 (lời) | "tìm mạng rẻ nhất bằng cách thử hết từng cây là rất chậm" | hook chỉ nói 'ít dây nhất'; mọi cây 10 đỉnh đều 9 đoạn; 'rẻ nhất' cần chi phí từng dây, chưa nêu | 'khi mỗi dây có độ dài riêng, tìm mạng ngắn nhất…' hoặc bỏ câu | PLAUSIBLE |
| L18 | example.1 | "(Đường 3 đỉnh có E = 2, chỉ một mặt giáp 2 cạnh, nên phải loại ra.)" | E ≤ 3V − 6 vẫn đúng ở V=3, E=2; điều kiện E ≥ 3 chỉ cần cho chứng minh | 'chứng minh dưới đây cần E ≥ 3; E < 3 kiểm tay' | CONFIRMED |
| L20 | stage2.1 (lời) | "ngày 15 tháng 3 năm 2006, viện yêu cầu thôi dùng SHA-1 cho chữ ký số…" | nguồn: 'Federal agencies should stop…'; lời bỏ chủ ngữ | thêm 'cơ quan liên bang' | PLAUSIBLE |
| L20 | stage5.2 | "chống lỗi ngẫu nhiên khi truyền… MD5 hay SHA-1 vẫn chấp nhận được" | nguồn (RF11 §1) chỉ nói MD5; SHA-1 là suy rộng, chưa kiểm được nguồn | tách MD5 (RF11) / SHA-1 ghi là suy luận | PLAUSIBLE |
| L20 | stage1.3 (màn hình) | "dù cách dùng này chưa bị phá" (HMAC-MD5) | nguồn: 'not urgent to stop using MD5 in other ways, such as HMAC-MD5'; 'chưa bị phá' là diễn giải | 'chưa cấp bách phải bỏ' | PLAUSIBLE |
| L20 | sym.1 (lời) | "Bài dùng năm thuật ngữ" | chỉ đọc bốn; 'bị phá' chỉ trên màn hình | sửa 'bốn' hoặc đọc thêm | CONFIRMED |

## 3. Mục chắc+vừa (15)
- Git Bash (B, vừa) ở practice.2 của L11–L20 (10 bài): màn hình giải nghĩa bash, cham.sh, ba tham số, 'ĐÚNG' nhưng không nói Git Bash là gì / mở thế nào. (CS112 đã sửa cùng kiểu bằng hàng 'Git Bash là cửa sổ gõ lệnh… Open Git Bash here'.)
- L12 quymo.4 `if all(p[i] != i for i in range(n)):` — `if` (B từ L01–L02), bảng không có hàng `if`.
- L12 three.1 `|A ∪ B ∪ C|` — ký hiệu ∪ không đọc ra (B từ L05).
- L13 sym_mod.3 'quan hệ tương đương/lớp (bài 7)' không giảng lại một dòng (B).
- L19 linearity.1 'Trả mũ (bài 12)… P(người i đúng) = 1/n' bối cảnh không kể lại (B).
- L20 stage5.1/.2 'Mô-đun mật mã dùng cho cơ quan liên bang phải được xét lại 5 năm một lần…' chỉ trên màn hình, lời không nhắc 'mô-đun' (A).
Yếu (3–6/bài): ∈ ℕ, ⟹, ≥, '4,9 × 10^21' (L11); |A|, ⟹, ≥ (L12); 'chuyển vế', 'số bị chia', 'Euclid' (L13); 'cơ số/số mũ', 'giản ước', 'chu kỳ', 'tràn số' (L14); 'bội của p − 1' (L15); |V|, |E|, 'bổ đề', 'bất biến' (L16); 'bổ đề', 'giả thiết quy nạp', 'hàng xóm', n!, deg(v) (L17); 'kề', 'hàng xóm', 'bậc' (L18); ≈, ≠ (L19); TLS, CWI, 'hệ quản lý phiên bản/Git/kho mã', 'khoá bí mật/công khai' (L20).
Cú pháp mã lần đầu của khoá ở L12–L19 (`sum(… for …)`, `from math import comb, factorial`, `min`, gán nhiều giá trị, `pow(3, e, m)`, `def … return`, `a if x == b else x`, `not in`, tập sinh, từ điển, `round(x, 2)`) đều đã có hàng trong bảng cách đọc của bài; chỗ không phủ duy nhất là `if` ở L12.

## 4. Người học kẹt ở đâu
L12 three.1 'số chia hết' dễ hiểu nhầm; L14 fermat.1 'ý chính của chứng minh' (ba lập luận liền, nhẹ); L17 example.2 'mạng rẻ nhất'; L18 example.2 đếm cặp (mặt, cạnh) hai cách; L20 stage4.1 'hệ quản lý phiên bản' rồi stage5.1 'mô-đun mật mã'; còn lại không kẹt. Phần Tự làm: chi tiết cú pháp lab (itertools, comb, sum(1 for …)) ở `de.md`, người chỉ có video phải có kho `labs/` để chấm.
