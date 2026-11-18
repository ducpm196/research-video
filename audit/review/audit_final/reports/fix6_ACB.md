# fix6_ACB — sửa khoá ACB theo R4_ACB (2026-11-16)

Chi tiết từng nhóm: `fix6_ACB_A.md` (L03–L05), `fix6_ACB_B.md` (L06–L08). Phần dưới là L00–L02 và cổng tổng hợp.

## Bài đã đổi (requeue): L00 L01 L02 L03 L04 L05 L06 L07 L08 (cả 9) + curriculum/acb.yaml (title L08) + verify_acb.py + sổ screen_code (khoá thủ công L03 symbol, L08 symbol)

## L00–L02 (tôi làm)
- L00: thêm cảnh `chaytep` (bảng 4 bước: lưu `mau.py`, mở Git Bash, `python mau.py`, `bash labs/cham.sh ACB L00 mau.py`, giải thích bash / cham.sh / khoá-bài-tên tệp); bảng "Đọc trước" (gán, `*`, print, if/thụt dòng) trước khối mã; practice nhắc lưu/chạy tệp và giải thích chân trang chấm; "đối soát" định nghĩa tại symbol; "khối PIN", "chứng chỉ số", "SQL Server" giải nghĩa; concept ghi "bốn tầng phần mềm, chưa phải thứ tự thời gian; luồng chuyển đi lõi giữ tiền trước"; Redis: "một nút Redis ... số minh hoạ, cần đo"; quiz pause 40 giây. Cắt lời từ 2525 về 2297.
- L01: 2 bảng "Đọc trước" (def/+/return+join/split; từ điển/danh sách cặp/for a, b in/pop+len), chân trang cham.sh giải thích + nhắc python mau.py, "đối soát" giải nghĩa ở bảng check, quiz đúng = C.
- L02: 3 bảng "Đọc trước" (bản đồ bit; khoá có hạn; giải mã), "nguyên tử", "dịch mã PIN", "đối soát" giải nghĩa tại chỗ; bỏ "nhị phân"/"cụm Gateway"; concept ghi luồng chuyển đi theo thứ tự thời gian (SVG đổi tiêu đề); hình SVG bản đồ bit tám ô (có chú thích 0111=7, 0010=2, viết gọn 72); Redis 800 000 "số minh hoạ, cần đo"; chân trang cham.sh; quiz đúng = B. Lời đọc 2290.

## Cổng (số thật, chạy lại sau khi cả hai fork xong)
| cổng | kết quả |
|---|---|
| lint 9 bài | 0 FAIL, 0 WARN cả 9 (31/28/35/28/29/34/29/34/30 PASS) |
| lời đọc (từ) | L00 2297 · L01 2140 · L02 2290 · L03 2297 · L04 2233 · L05 2296 · L06 2277 · L07 2300 · L08 2296 |
| render | 9/9 bài 0 vấn đề (L00–L02 do tôi; L03–L08 do fork, đã xem khung bảng/hình mới) |
| `verify_acb.py` (đủ cả khoá) | 301/301 PASS (có hàm mới `fixes6_l00_l02`: 13 kiểm) |
| `tests/test_e52.py` | 0 FAIL |
| `lv.py curriculum curriculum/acb.yaml` | 9 bài, 0 lỗi |
| `check_legal.py` | 111 lượt dẫn, 0 FAIL (8 văn bản CHUA_KIEM giữ nhãn) |
| `lab_gate.py ACB` | 9 PASS · 0 FAIL (196 lab) |
| `arith_scan.py` | 0 FAIL (fork chạy 257 phép) |
| `check_curricula_graph.py` | VER dẫn tới mã không PASS: 0 |
| `screen_code.py check --course ACB` | **CHƯA SẠCH**: PASS 41 · FAIL 0 · STALE 14 · MISSING 28 · ORPHAN 28 |

## screen_code: việc còn lại cho người điều phối
Mọi dòng lỗi là mục cảnh `code` và `practice 1 0` (khoá "ACB Lxx code <step> <khối>") do `audit/acb/gen_sc_acb.py` sinh; chèn bảng "Đọc trước" làm lệch chỉ số step. Khoá thủ công (L01, L03, L04, L05, L06, L07, L08 symbol/example) đã sửa bằng Edit và PASS. Tôi chạy `gen_sc_acb.py` thì bị cơ chế phân quyền từ chối (ghi đè sổ, brief cấm script sửa sổ), nên KHÔNG chạy và không đi vòng. Cần: `.venv/Scripts/python -B audit/acb/gen_sc_acb.py` rồi `screen_code.py check --course ACB` (kỳ vọng 0 FAIL/STALE/MISSING/ORPHAN; nếu còn STALE ở mục tay thì đối chiếu sha qua `screen_code.py inventory`).

## Quyết định chính
- L08 "thấu chi lương": không có nguồn kiểm được (hub-system-graph.md chỉ có tên API; JD.md không nêu số) nên BỎ lời hứa khỏi hook, tiêu đề, concept, recap, curriculum; Auto-Debit và câu cụt đã sửa. Không bịa số.
- Quiz đáp án đúng: L01 C, L02 B, L03 D, L04 C, L05 B, L06 D, L07 C, L08 B.
- P3: hình bản đồ bit (L02), vòng chờ khoá (L05), con trỏ đối soát (L07); P2: FORALL L05 có phép tính 10 000 × 4,5 ms = 45 s, × 0,1 ms = 1 s (giả định ghi rõ "phải đo").
- Pháp lý giữ nhãn "chưa đọc nguyên văn"; không thêm số hiệu. Không thêm mục vào `symbols.ACB.yaml` / lexicon (định nghĩa mới đặt tại chỗ, không đăng ký E52).

## Mục chưa giảng ước còn lại
L00 0 · L01 0 · L02 0 · L03 0 · L04 0 · L05 0 · L06 0 · L07 0 · L08 0 (có thể 0–1 ở chữ mTLS/Cloud CA L08).

## Còn mở
- Chưa dựng/ASR/nghe lại: nhiều câu `say` mới; `asr_reviewed` của câu đã đổi đã xoá.
- `labs/ACB/*` không đổi (de.md dạy `python mau.py` như cũ).
- Công cụ phụ tôi dùng nằm ở scratchpad (chỉ đổi danh sách `focus`/`say`/xoá `asr_reviewed` mồ côi trong YAML bài; không đụng sổ).
