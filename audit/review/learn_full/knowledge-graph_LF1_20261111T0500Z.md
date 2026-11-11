# knowledge-graph_LF1_20261111T0500Z: đồ thị chứng cứ đợt LF1 (HOC_TAP.html trọn lộ trình + khoá BNX theo JD)

Chỉ ghi nút OBSERVED hoặc CITED; máy chạy trong phiên 2026-11-11. `checked_at` trong log là UTC; giờ máy là UTC+7 (nên `02:47` giờ máy = 19:47Z hôm trước). Phiên dài, có ngắt giữa chừng do giới hạn.
Môi trường: Windows 11; `.venv` Python 3.13.5; git 2.53; openssl 3.5.5; JDK 21/22; Docker 28.3.2 (Oracle AI Database 26ai Free 23.26.3, SQL Server 2022 CU27, Kafka 3.9.0); Edge (Playwright).

| ID | Khẳng định | Phương pháp (lệnh đã chạy) | Quan sát | validity | checked_at |
|---|---|---|---|---|---|
| LF-01 | Khoảng trống JD là thật: 0/656 đặc tả bài nói JWT, OIDC, OpenAPI/Swagger, gRPC, Elasticsearch, Couchbase, SWIFT, ví/thuế điện tử, RabbitMQ, DDD, Open Banking | `grep -rlI` từng từ khoá trong `lessons/` | 0 tệp cho mỗi từ trên; OAuth 1 (WEB L09); T-SQL 1 (DBS L17, chỉ nhắc) | VALID | 2026-11-11 |
| LF-02 | Dãy học 11 chặng phủ đủ mọi bài, mỗi bài một chỗ, mọi tiên quyết đứng trước | `pack.py list`; assert trong `pack.stages()` | 672 bài; không assert nào hỏng | VALID | 2026-11-11 |
| LF-03 | Giáo án BNX 16 bài hợp lệ, không chu trình, mọi VER PASS | `lv.py curriculum curriculum/bnx.yaml`; `check_curricula_graph.py`; `verify_plan_curricula.py` | 16 bài/16 đặc tả/0 lỗi; 0 VER hỏng, 0 ví dụ số thiếu VER; 561 PASS/0 FAIL | VALID | 2026-11-11T03:34Z |
| LF-04 | Mã trên màn hình BNX chạy nguyên văn (git, openssl+ssl, Oracle, SQL Server, Kafka, Python) | `verify_bnx.py` (280 dòng); `screen_code.py check` toàn kho | verify_bnx 280/280 PASS không SKIP; screen_code 712 khối PASS 903 FAIL 0 STALE 0 MISSING 0 ORPHAN 0 | VALID (cần `docker start bnx-ora bnx-mss`) | 2026-11-11T03:48Z |
| LF-05 | Dò phát âm từ ngoại: chỉ JSON, YAML đạt | `audit/bnx/probe_terms_gpu.py x1.yaml` (small+medium, 4 ngữ cảnh) | JSON «Giây-sơn» 8/8, YAML «Giam-mồ» 8/8; 10 từ còn lại < 7/8; 12 đối chứng âm đều 0/8 | VALID | 2026-11-11 |
| LF-06 | 5 người đọc độc lập (chỉ đọc) đọc trọn 16 bài BNX | báo cáo từng tác tử (`ĐÃ ĐỌC K/K`) | 4+4+2+3+3 = 16; 11 MUST, ≈ 116 SHOULD/BLOCK (đếm lại từ bảng báo cáo, ±3) | VALID (CITED: báo cáo tác tử) | 2026-11-11 |
| LF-07 | Mọi MUST đã sửa; mọi SHOULD/BLOCK áp trừ 3 có lý do | người điều phối kiểm từng phản hồi của tác tử soạn; giáo án + VER sửa tay (L04 `>=`, L12 fix, E29) | 11/11 MUST; ngoại lệ: L06 lỗi 1205 (chưa nguồn), TT40 loại giao dịch (chưa nguyên văn), chữ "bit" (như CSA/BNK) | VALID | 2026-11-11 |
| LF-08 | 16 bài BNX dựng, một giọng, ASR 0 câu chưa xem xét | `audit/.build_queue_run.sh` (2 hàng, 2 lượt: lần 1 trước sửa, lần 2 sau sửa); `asr_review_dms.py --course BNX`; `asr_flags.py BNX` | mọi dòng `verify … → PASS`; `BNX: 0 câu chưa xem xét`; HAND "BNX L00–L15" + 1 mục L06 (TTS gửi đủ 5 chữ số 0-0-0-6-0) | VALID | 2026-11-11 |
| LF-09 | Toàn vẹn 672 bài: tệp đủ, giải mã trọn, khớp đặc tả, bản duyệt nhanh mới | `pack.py check --decode` (656 cũ, chạy 02:47→05:45 giờ máy, 0 vấn đề, 5937,9 phút); `pack.py check --decode --course BNX`; `pack.py check` toàn kho | `# 656 … 0 vấn đề … giải mã trọn 656`; BNX `# 16 … 0 … 213.7 phút … giải mã trọn 16`; toàn kho `# 672 … 0 vấn đề … 6151.6 phút` (logs/pack_check_after_preview.out) | VALID | 2026-11-11 |
| LF-10 | 656 video cũ không đổi sau lần giải mã | `find out -newermt "2026-11-11 02:47" ( mp4, build_report.json ) ngoài BNX` (giờ máy = UTC+7, cùng múi giờ với lần giải mã) | 0 tệp | VALID | 2026-11-11 |
| LF-11 | Toàn kho sạch | `audit_all.py` | `audit_all: 672 bài, 672 đã dựng, 0 bài có vấn đề`; `status_report: 672/672, 6152 phút` | VALID | 2026-11-11 (cổng cuối kết thúc 04:33Z) |
| LF-12 | Bộ kiểm khoá cũ và nhất quán không hỏng vì thay công cụ dùng chung (`checklib.py`, `screen_code.py`, `check_xref.py`) | `final_gates.sh` → `logs/verify_final_lf1.out` | verify_jva 110/110; verify_bnk 21/21; verify_cs112 FAIL 0; verify_cs112_p2 37/0; test_lint 0 FAIL; check_meta 0; check_course_refs 0; check_xref 0; sync_tpl 0 mẫu lệch ×3; interview 92/92 trùng byte | VALID | 2026-11-11 |
| LF-13 | Trang học đúng, không liên kết chết, chạy trên Edge (máy tính + 390 px) | `pack.py page`; Playwright `ui_test.py` | 672 bài; HOC_TAP.html 4164 liên kết tệp + 1537 neo, chết 0; xem.html 6177 chết 0; HOC_TAP.md 673 chết 0; tự kiểm 672/672, khung hình 672/672; JS 0 lỗi; không tràn ngang | VALID | 2026-11-11 |
| LF-14 | Mục lục tổng sinh từ cùng nguồn với trang học; mọi liên kết sống | `master_sections.py`; quét `file:///` | 3 khối LF_* ghi; 297 liên kết, chết 0; 16/16 BNX "đặc tả khớp video: có" | VALID | 2026-11-11 |
| LF-15 | Nguồn pháp lý/chuẩn có ngày, nguồn thứ cấp ghi rõ | `audit/bnx/sources.md` (30 mục nguồn) | CBPR+ 22/11/2025 (Clearstream, trang 03/11/2026); NĐ 52/2024 Đ6 k3; TT 41/2025 (NHNN 07/11/2025); Luật QLT 2019 Đ58; RFC; tài liệu sản phẩm | CITED (một phần thứ cấp, xem OB-LF-3) | 2026-11-11 |

## Lỗi do chính đợt này gây ra và cổng đã bắt được (ghi để không lặp lại)
| ID | Lỗi | Bắt bởi | Xử lý |
|---|---|---|---|
| LE-1 | Giáo án BNX tôi viết có chữ "tài liệu" (L08, L09) → lint E29 FAIL | lint | đổi "bản ghi" trong giáo án + nguồn |
| LE-2 | `fix` L12 và VER BNX:L04 do tôi viết dạy sai pháp lý / ngược RFC 7519 (`>`) | người đọc độc lập | sửa giáo án + VER, tác tử sửa bài |
| LE-3 | **77 lượt `check_xref`**: 11 vi phạm thật ("ở khoá trước…" trong 9 bài BNX; cổng bỏ sót thêm 1 cụm "khoá học về hệ thống ngân hàng trước") + 66 dương tính giả ("CAS" Compare-And-Swap, "INT" kiểu số nguyên) | `check_xref.py` — tôi suýt bỏ qua vì mã thoát 2 của lệnh gộp bị nhầm là do `ls` | sửa 11 chỗ trong nguồn, dựng lại 9 bài; vá cổng **hẹp** (AMBIG = {CAS, INT} cần "khoá/bài" trước hoặc "Lxx" sau; thêm tên tắt "hệ thống ngân hàng"); ca đối chứng 11/11 đúng |
| LE-4 | 9 `preview.html` cũ sau khi dựng lại (build không sinh preview) | `pack.py check` | `pack.py preview`; check 672/0 |
| LE-5 | `TaskStop` không dừng cây tiến trình: hàng dựng cũ chạy song song với hàng mới | `Get-CimInstance` | `taskkill /T`; ghi bộ nhớ `windows-taskstop-orphans` |
| LE-6 | `scan_ctrl` từ 8 → 59 | `scan_ctrl.py` | phân loại: 51 TAB nguyên văn đầu ra công cụ trong khối mã (kiểm bằng máy: 0 trong công thức/lời đọc/trước `ext{ imes heta`), ca đối chứng dương 4/4 |

## Điểm nghẽn hợp đồng (từ plan_LF1)
- LB-1 CLOSED (LF-01).
- LB-2 CLOSED (LF-02).
- LB-3 CLOSED (LF-03, LF-04, LF-05).
- LB-4 CLOSED (LF-06, LF-07).
- LB-5 CLOSED (LF-08, LF-09, LF-10, LF-11, LF-12).
- LB-6 CLOSED (LF-13, LF-14).

## Còn mở, không chặn DONE của phạm vi đã cam kết (ghi rõ thay vì gọi là đã kiểm)
- **OB-LF-1** tai người nghe phát âm: NOT_VERIFIED (chưa ai nghe 16 bài BNX).
- **OB-LF-2** sản phẩm không chạy thật: Elasticsearch, Couchbase, RabbitMQ, Schema Registry, cụm Kubernetes, GitLab runner, Oracle In-Memory/Sharding, máy chủ OAuth, JDBC trong cổng.
- **OB-LF-3** pháp lý chỉ nguồn thứ cấp: nguyên văn TT 40/2024 Điều 26, TT 41/2025, TT 64/2024 Phụ lục 01, TT 19/2021 Điều 20.
- **OB-LF-4** hiệu quả ghi nhớ của trang trên chính người học: NOT_VERIFIED.
- **OB-LF-5** 537 bài ngoài hai lộ trình LS1 vẫn chưa được đọc lại độc lập (kế thừa OB-5 của LS1); mẫu E đo ≈ 5% bài có MUST.
