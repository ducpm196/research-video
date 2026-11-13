# Mốc đầu đợt AF2 (đo 2026-11-12T18:20Z → 20:15Z; commit `df811558`; bài của khoá cũ chưa bị sửa tại thời điểm đo, trừ L04 JVA ở cuối)

Nguồn: `gates_pre.out` (bản chạy sau chót; đầu tệp lẫn dòng do hai lần chạy trùng, xem "Sự cố"), `gates_cheap.out`, `pack_check.out`.

| Cổng | Kết quả (OBSERVED) |
|---|---|
| verify_jva | 110/110 PASS (18:20:19Z, lần chạy đầu); sau khi thêm lab L04: 10/10 PASS cho L04 (`verify_jva.py L04`, 18:52Z) |
| verify_bnk / verify_bnx | 21/21 · 493/493 PASS |
| verify_cs112 / _p2 | 38 PASS + 15 FIX (kế thừa), 0 FAIL · 37 PASS 0 FAIL |
| verify_plan_curricula | 570 PASS · 0 FAIL |
| check_curricula_graph | 0 chu trình, 0 VER lỗi |
| tests/test_lint | 0 FAIL |
| check_xref · check_meta · check_course_refs | 0 · 0 · 0 |
| scan_ctrl | 59 hit (mốc LF2) |
| sync_tpl (CS112, DMS, CS115) | 0 mẫu lệch |
| screen_code toàn kho | 880 khối — PASS 1089 · FAIL 0 · STALE 0 · MISSING 4 (khối của khoá FND/JV2 đang soạn) · ORPHAN 0 |
| interview_sync_video | 92/92 trùng byte |
| asr_flags BNX | 0 câu chưa xem xét |
| pack.py check (cả kho, không giải mã) | 680 bài · 0 vấn đề · 6312 phút |
| audit_all | 680 đã dựng; bài có vấn đề ngoài FND/JV2: chỉ BNX L19 "mã màn hình" (khối bash Redis cụm lệch `CROSSSLOT`) — **chập chờn**: chạy riêng 3 lần, lần 1 FAIL, lần 2–3 PASS (331 khối, PASS 360); chạy khi có tiến trình khác dùng Docker/Redis thì lệch |
| pack_page | 680 bài, 4220 liên kết tệp, chết 0 |
| arith_scan (mới) | 216 phép tính kiểm được, 1 FAIL thật: LLM L05 `12,9 + 34,4 = 47,2` |
| check_next_refs (mới) | 551 lời hẹn: 93 lệch với thuật toán xếp dãy cũ; **0 lệch** sau khi đổi thuật toán (cạnh ngầm L(k)→L(k+1)) |
| check_legal (mới) | 77 lượt dẫn, 20 văn bản; 4 FAIL đã biết (BNX L12 ×3, MASTER TT 50/2024 không ghi sửa đổi) |
| lab_gate (mới) | chạy được; chấm ĐÚNG lời giải và KHÁC với bản cố tình sai (đối chứng âm) |

## Sự cố trong lúc đo (ghi để không lặp lại)
1. `final_gates.sh` khởi chạy bằng `nohup … &` trong tool: bản đầu tưởng đã chết nhưng vẫn chạy; hai bản chạy song song, tranh `audit_all.tsv`, Docker/Redis và nhật ký → đã kill bản thứ nhất (cây tiến trình 16788). **Chỉ chạy cổng bằng `run_in_background` trực tiếp, và kiểm `Get-CimInstance Win32_Process` trước khi chạy lại.**
2. Trong khi đo, tôi sửa `audit/jva/src/l04.py` bằng heredoc Python → chuỗi `\n` biến thành xuống dòng thật → `verify_jva` lỗi cú pháp ở một lần chạy. Đã sửa bằng Edit; mốc JVA lấy từ lần chạy đầu (110/110).
3. Các tác tử FND/JV2 viết bài mới trong lúc `audit_all` chạy → `audit_all` đếm 818 bài, 134 bài "có vấn đề" (đều thuộc FND/JV2 chưa dựng). Không ảnh hưởng khoá cũ.
