# fix12 DMS L11–L20 (sửa theo R8_DMS_B) — 2026-11-17

Không chạy build/tts/asr/render/audit_all/git/docker. `tools/lv.py render` đã bị từ chối quyền ở lần thử trước (L12): không đi vòng.
Sửa CẢ script vá `audit/dms/af2/lNN.py` / `fix6b.py` lẫn bài sinh ra (L16–L18 sinh từ mẫu: script ghép lại như cũ).

## (A) Git Bash ở practice.2 — chỉ đổi màn hình
`fix6b.patch_cham` (ghi đè bản của fix6lib, gọi nó rồi thêm ĐẦU ghi chú): "Git Bash là cửa sổ gõ lệnh trên Windows (đi kèm Git for Windows): vào thư mục bài làm, bấm chuột phải vào chỗ trống, chọn **Open Git Bash here**." rồi tới câu "Chấm bằng Git Bash: …". Cùng khối `<p class="note">` nên chỉ số focus [2, 2, 3, 3] giữ nguyên. Cả 10 bài. Không đổi `say`.

## (B) 5 mục riêng
- L12 quymo: thêm hàng `if điều_kiện:` ("nếu: chỉ khi điều kiện đúng mới chạy các dòng thụt vào") vào bảng "Đọc trước" trước khối mã (bảng thứ hai nay 6 hàng, tách 3 + 3), kèm câu đọc; sửa câu mở "mười ký hiệu" / "Sáu ký hiệu còn lại".
- L12 three.1: ghi chú trong hộp công thức "Dấu ∪ đọc là “hợp”: … là số phần tử thuộc ít nhất một trong ba tập" và câu đọc đầu "Dấu hợp cho số phần tử thuộc ít nhất một trong ba tập." (focus thêm một mục).
- L13 sym_mod.3: "quan hệ tương đương (bài 7: chia các số thành các lớp, hai số cùng lớp khi cùng số dư)" trên màn hình và trong câu đọc.
- L19 linearity.1: kể lại bối cảnh "n người gửi mũ, mũ bị trả ngẫu nhiên; hỏi trung bình bao nhiêu người nhận đúng mũ của mình" (màn hình và lời).
- L20 stage5.1: "Mô-đun mật mã (phần mềm hoặc thiết bị làm việc mã hoá) …" — chỉ màn hình (lời của bước này không nhắc "mô-đun").

## (C) SHOULD
- L12 three.1: "Có 16, 10, 6 số chia hết cho 6, 10, 15; có 3 số chia hết cho 30" (màn hình), lời "Có 16, 10 và 6 số chia hết cho 6, 10 và 15. Có 3 số chia hết cho cả ba, tức chia hết cho 30…".
- L17 example.2: lời "Nếu mỗi dây có độ dài riêng, tìm mạng ngắn nhất bằng cách thử hết từng cây là rất chậm, nên người ta dùng…".
- L18 example.1 (màn hình): "(Chứng minh dưới đây cần E ≥ 3; trường hợp E < 3 kiểm tay.)" thay cho dòng "Đường 3 đỉnh có E = 2… phải loại ra"; điều kiện bất đẳng thức ghi "liên thông, V ≥ 3". Lời giữ nguyên ("có từ 3 đỉnh và ít nhất 3 cạnh").
- L20 stage2.1 (lời): "viện yêu cầu các cơ quan liên bang thôi dùng SHA-1…" (mục `asr_reviewed` của câu này được cập nhật theo câu mới).
- L20 stage5.2: màn hình "MD5 vẫn chấp nhận được (RFC 6151); SHA-1: suy luận tương tự, chưa kiểm được nguồn"; lời "…MD5 vẫn chấp nhận được theo văn bản năm 2011, còn SHA-1 là suy luận chưa kiểm được nguồn."
- L20 stage1.3 (màn hình): "dù chưa cấp bách phải bỏ cách dùng này" thay cho "chưa bị phá".
- L20 sym.1: lời "bốn thuật ngữ"; hàng "bị phá" được bỏ khỏi bảng và nghĩa của nó (có cách tìm va chạm với số lần thử ít hơn hẳn 2^{n/2}) ghi ngay chỗ dùng đầu tiên, stage1.2 "MD5 đã bị phá (…)" (chỉ màn hình).
Không thêm số hiệu/điều khoản mới; tên nguồn giữ như `audit/dms/sources_L20.md`.

## Xác nhận băm `lv.sentences` (so lời đọc trước/sau, theo văn bản câu)
- Chỉ đổi màn hình (say không đổi câu nào): L11, L14, L15, L16, L18.
- Có đổi `say`: L12 (8 câu cũ → 10 câu mới), L13 (1 → 1), L17 (1 → 1), L19 (2 → 2), L20 (8 → 6).

## Số từ lời đọc (≤ 2300)
L11 1965 · L12 2297 · L13 2207 · L14 2292 · L15 2157 · L16 2135 · L17 2177 · L18 2290 · L19 2295 · L20 2297.
Cắt để giữ trần: L12 rút gọn 4 câu (vùng giữa Venn, "Ba vòng…", tổng xen kẽ, "Bây giờ kiểm D bốn…"); L19 bỏ "máy đã kiểm n từ 1 đến 6" (còn trên màn hình); L20 bỏ "Đây là thước đo của cả hành trình." và "Tổng kết lại hành trình." và rút gọn hai câu.

## Cổng
lint L11–L20: 0 FAIL, 0 WARN; screen_code DMS PASS 95, 0 FAIL, 0 STALE, 0 MISSING, 0 ORPHAN; verify_dms 324 PASS, 0 FAIL; test_e52 0 FAIL; curriculum dms 21 bài, 0 lỗi. Cấu trúc: không bảng nào > 4 hàng, mọi step sau bảng cách đọc có `clear: true` (kiểm bằng mã).
