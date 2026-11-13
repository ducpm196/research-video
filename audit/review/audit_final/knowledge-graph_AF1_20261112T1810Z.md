# knowledge-graph_AF1_20261112T1810Z — đồ thị chứng cứ đợt rà AF1 (chỉ rà, không sửa)

Môi trường: Windows 11; `.venv` Python 3.13.5; JDK trên PATH **21.0.13** (Temurin); `gcc 16.2.0` (`/c/tools/w64devkit/bin`); Docker `bnx-ora`, `bnx-mss` Up; commit `df8115588d3a7717b2c93c80a6e3b1d98ec9fb7e`, cây sạch trước khi ghi tệp AF1. Giờ lấy từ `date -u` của máy.
OBSERVED = chạy/đọc trong phiên này. CITED = lấy từ bàn giao LF2 hoặc từ tin nhắn trả về của tác tử đọc (người điều phối không tự chạy lại).

| ID | Khẳng định | Phương pháp | Quan sát | basis | validity | checked_at |
|---|---|---|---|---|---|---|
| AF1-01 | Tham chiếu chéo, siêu dữ liệu, "bài N" sạch | `check_xref.py`, `check_meta.py`, `check_course_refs.py` | 0 · 0 · 0 vấn đề (`logs/gates_cheap.out`) | OBSERVED | VALID | 2026-11-12T18:08Z |
| AF1-02 | Đồ thị lộ trình và VER sạch | `audit/check_curricula_graph.py`; `audit/verify_plan_curricula.py` | 43 lộ trình, 680 bài, 1406 cạnh, 0 chu trình, 0 tham chiếu hỏng; `570 PASS · 0 FAIL` | OBSERVED | VALID | 2026-11-12T18:08Z |
| AF1-03 | Lint tự kiểm và ký tự điều khiển ở mốc đã biết | `tests/test_lint.py`; `scan_ctrl.py` | `tests: 0 FAIL`; `hits: 59` (mốc LF2) | OBSERVED | VALID | 2026-11-12T18:07Z |
| AF1-04 | 680 bài có video khớp đặc tả hiện tại | `pack.py check` (không `--decode`) | `680 bài có video · có vấn đề 0 · 6312.0 phút` (`logs/pack_check.out`) | OBSERVED | VALID | 2026-11-12T18:11Z |
| AF1-05 | `audit_all` 680/680, `screen_code` FAIL 0, `verify_<khoá>`, ASR 0 chưa xem xét, giải mã trọn | không chạy lại | theo `learn_final/logs/gates_post.out` | CITED (LF2, 2026-11-12T16:18Z) | NOT_VERIFIED phiên này (CB-AF1-7) | — |
| AF1-06 | Mẫu F: 3/38 bài có MUST; 28/38 có phát hiện; 37 SHOULD | 3 tác tử chỉ đọc, 38 bài, sha16 trùng 38/38; Wilson tính bằng Python | 7,9% (2,7–20,8%); `sample_f/REPORT.md` | CITED (tác tử) + 7 mục người điều phối mở tệp kiểm (OBSERVED: DVO L03, SWF L03, IRS L11 ×2, LLM L05 ×2, SEP L08) | VALID cho 7 mục đã kiểm; còn lại theo người đọc | 2026-11-12T18:06Z |
| AF1-07 | Mẫu F độ sâu: ĐỦ 30, GẦN 8, CHƯA 0; P1 = 2 ở 7/38; P8 = 2 ở 2/38; P9 = 2 ở 18/38 | cộng từ ba bảng độ sâu | như trên | CITED (tác tử); phép cộng OBSERVED | VALID | 2026-11-12T18:09Z |
| AF1-08 | Người mất gốc hụt nền từ BNK L02, kẹt khi thực hành ở BNX L00; sau JVA L00 không bài nào trong 20 bài giao việc tự gõ | tác tử đọc trọn 21 bài, grep từ khoá trên `lessons/jva, bnk, bnx`, chạy 8 chương trình Java | bảng khoảng hở ở `sample_f/REPORT.md` mục 4 | CITED (tác tử) | VALID (đối chiếu AF1-09: BNK 0/15 bài có khối mã) | 2026-11-12T18:02Z |
| AF1-09 | 148/680 bài có khối mã; 16 khoá 0 khối mã; Python ở 79 bài, không khoá nào dạy từ đầu; PyTorch 4 bài, pandas 0 | `logs/stats.py` → `logs/stats.out` | như khẳng định | OBSERVED | VALID (đếm theo `class="code"`/`<pre`; từ khoá, không phải đọc hiểu) | 2026-11-12T18:05Z |
| AF1-10 | Ba MUST của mẫu F thuộc hai lớp lỗi không cổng nào bắt: mục tiêu không được dạy (AGT L04, DVO L03), pháp lý hết hiệu lực (BNX L12) | đối chiếu danh sách cổng trong `final_gates.sh` với loại lỗi | không cổng nào so mục tiêu ↔ cảnh; không có sổ hiệu lực văn bản | INFERRED từ danh sách cổng + OBSERVED DVO L03 | VALID cho DVO; BNX L12 xem AF1-11 | 2026-11-12 |
| AF1-11 | Luật Quản lý thuế 38/2019 đã bị Luật 108/2025/QH15 thay từ 01/7/2026 | tác tử tìm kiếm web, hai trang thứ cấp; chưa mở văn bản gốc | BNX L12 dẫn Luật 38/2019 Điều 58 | CITED (thứ cấp, 2026-11-12, no revision given) | NOT_VERIFIED (CB-AF1-2) | 2026-11-12 |
| AF1-12 | Môi trường trôi so với bàn giao LF2: JDK 21.0.13 (không phải 22.0.2); có gcc | `java -version`, `javac -version`, `gcc --version` | như khẳng định | OBSERVED | VALID → làm AF1-05 phần verify_jva và "không có trình biên dịch C" thành STALE | 2026-11-12T18:07Z |
| AF1-13 | Phần mờ trên màn hình dùng `opacity: .38` | `grep opacity tools/templates/player.css` | `.blk .dim { opacity: .38; }`, `.blk.past { opacity: .62; }` | OBSERVED | VALID (mức "khó đọc" là nhận xét của tác tử trên 5 khung) | 2026-11-12T18:07Z |
| AF1-14 | `.srt` trùng `say` từng từ 38/38; 224 khung hình không tràn/đè/cắt | tác tử so chuỗi, mở khung | 4 lỗi hiển thị nhỏ | CITED (tác tử) | VALID cho phụ đề và bố cục; KHÔNG là bằng chứng về âm thanh | 2026-11-12 |
| AF1-15 | Báo cáo nguyên văn của tác tử không lưu được | `save_f.py` trên nhật ký tác vụ | tệp `.output` rỗng (0 dòng) | OBSERVED | VALID (CB-AF1-6) | 2026-11-12T18:08Z |
| AF1-16 | Phiên AF1 không đổi bài, giáo án, video | `git status --short` sau khi chạy cổng | chỉ có `audit/review/audit_final/`, `audit/review/sample_f/REPORT.md`, `HANDOVER.md` (mục đầu) là mới/đổi | OBSERVED | VALID | 2026-11-12T18:12Z |

## Phụ thuộc
AF1-06, 07, 08 → `claim:AF1-04` (bài đọc là bài đã dựng, sha16 trùng) → kết luận mục 1 của plan.
AF1-10 → `claim:AF1-06`; AF1-11 → chờ CB-AF1-2. AF1-05 STALE một phần do `claim:AF1-12`.
Kết luận "chưa đạt bản final" đứng trên AF1-06, 07, 08, 09 (CITED có kiểm chọn lọc + OBSERVED), không đứng trên nút INFERRED nào.

## Contract bottleneck
CB-AF1-1…8: bảng đủ 7 trường ở `plan_AF1_20261112T1810Z.md` mục 4. Tất cả OPEN. Kế thừa từ LF2 còn mở: CB-LF2-3 (tai người) = CB-AF1-5; CB-LF2-4 = CB-AF1-8; CB-LF2-5 nhập vào CB-AF1-2.
