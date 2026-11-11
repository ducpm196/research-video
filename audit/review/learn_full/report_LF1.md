# Báo cáo đợt LF1 — HOC_TAP.html trọn lộ trình 0 → senior + khoá BNX lấp khoảng trống JD

Ngày: 2026-11-11. Kế hoạch: [`plan_LF1.md`](plan_LF1.md). Nhãn: OBSERVED (chạy/đọc trong phiên) · CITED (nguồn có ngày) · INFERRED · NOT_VERIFIED.
**Kết luận: DONE** cho phạm vi đã nhận (trang học + 16 bài mới đủ cổng máy). Những điều máy không kiểm được ghi ở §5, không gọi là đã kiểm.

## 1. Trang học `HOC_TAP.html` (sinh bằng `audit/review/learn_start/pack.py page`)
- **Một dãy 11 chặng** theo cấp độ của `interview/MASTER_CURRICULUM_INDEX.md` và tầng của `curriculum/ROADMAP.md`:
  1. Java từ 0 (JVA) → 2. backend ngân hàng (BNK) → 3. kỹ năng theo JD (BNX, mới) → 4. phỏng vấn + tích hợp (INT, ACB)
     — chặng 1–4 = "đường học tối thiểu" của MASTER_INDEX;
  5. toán rời rạc, thuật toán, toán cho học máy → 6. máy tính, HĐH, mạng → 7. kỹ nghệ phần mềm, CSDL, DevOps, bảo mật →
  8. hệ phân tán, dữ liệu, đám mây, kiến trúc → 9. AI/ML (AIF, DAN, DSC, MLO, IRS, LLM, AGT, RLN, CVI) → 10. chuyên gia (TOC, PLC, PAR, HCI, SEP, CAS) →
  11. chuyên ngành mở rộng (RBM, ESY, ROB, GFX, BCH).
- Mỗi chặng = bao đóng tiên quyết (requires + requires_ext) của mục tiêu, bỏ bài đã xếp, sắp tô pô. Máy assert: mỗi bài đúng một chỗ, mọi bài của kho có chỗ,
  **mọi cạnh tiên quyết trỏ về trước** (OBSERVED: không assert nào hỏng).
- Phủ **672/672 bài có video, 102,5 giờ** (OBSERVED, ffprobe).
- Ghi nhớ lâu (localStorage, có xuất/nhập tệp sao lưu; thử thật trên Edge bằng Playwright, 0 lỗi JS, không tràn ngang ở 390 px):
  - tự kiểm sau mỗi bài: câu hỏi + đáp án lấy nguyên lời đọc cảnh `quiz` của đặc tả **và đúng khung hình** câu hỏi/đáp án trong video (672/672);
  - lịch ôn ngắt quãng Leitner 1, 3, 7, 14, 30, 60, 120 ngày; nút "Ôn hôm nay" trộn các khoá; chấm "quên / lơ mơ / nhớ chắc";
  - thẻ chuỗi logic (cảnh `recap`) và lỗi hay gặp (cảnh `pitfall`); ô "giải thích lại bằng lời của bạn" (Feynman);
  - cảnh báo khi tick bài mà bài cần học trước chưa tick; "bài nên học tiếp"; ước lượng ngày xong theo số phút/ngày;
  - nhận tự động dấu tick cũ của trang LS1 (`hoc_tap_done_v1`).
- Bảng **đối chiếu JD → bài** (22 dòng, mọi mã bài máy kiểm có thật).
- `out/<KHOÁ>/<id>/xem.html` cho 672 bài: mục lục bấm được, tốc độ, bài trước/sau theo dãy toàn cục, tự kiểm + khung hình.
- Cổng (OBSERVED 2026-11-11): HOC_TAP.html 4164 liên kết tệp + 1537 neo, **chết 0**; xem.html 6177 liên kết, chết 0; HOC_TAP.md 673 liên kết, chết 0; 3,86 MB.
- Sinh lại **537 `preview.html`** cũ/thiếu (đúng 537 bài ngoài hai lộ trình LS1 — 26 bài cuối khoá trước đó không có preview).

## 2. `interview/MASTER_CURRICULUM_INDEX.md`
- Thêm Mục 0 (bảng 11 chặng, sinh bằng `audit/review/learn_full/master_sections.py` từ cùng `pack.stages()` → hai nơi không lệch được),
  Mục 2A (khoá BNX, bảng video sinh tự động), Mục 3A (cấp 5 AI, cấp 6 chuyên gia, chuyên ngành mở rộng — trước đây chỉ mục dừng ở cấp 2),
  sơ đồ mermaid có BNX/AI/chuyên gia, đường học tối thiểu có BNX; Mục 8 viết lại theo số đo mới (bảng cũ ghi "chưa có bài" cho PKCE/thiết kế API là sai:
  WEB L09, WEB L06, SDP L14 đã có).

## 3. Khoá mới BNX · Backend ngân hàng mở rộng theo JD — 16 bài, 213,7 phút (OBSERVED, ffprobe sau lần dựng cuối)
Khoảng trống đo bằng quét chữ 656 đặc tả (OBSERVED): 0 bài về JWT, OIDC, OpenAPI/Swagger, gRPC, Elasticsearch, Couchbase, SWIFT, ví/thuế điện tử,
RabbitMQ, Oracle AQ, DDD, Open Banking, Git cơ bản. Bài (phút thật): L00 Git 12,2 · L01 OpenAPI 13,9 · L02 gRPC/Protobuf 15,2 · L03 JWT 12,9 ·
L04 OAuth/OIDC 11,5 · L05 mTLS 11,5 · L06 thủ tục lưu trữ Oracle + SQL Server 15,8 · L07 Oracle phân vùng/JSON/AQ 15,0 · L08 Elasticsearch 12,3 ·
L09 Couchbase 13,4 · L10 Kafka nâng cao/RabbitMQ 13,0 · L11 SWIFT/ISO 20022/ngoại tệ 13,7 · L12 ví + thuế điện tử 13,0 · L13 Docker/GitLab CI/K8s 12,9 ·
L14 DDD/cổng API/Open API 14,6 · L15 tình huống chuyên gia: dự án mẫu theo JD 12,9.
- **Chạy thật** (OBSERVED): git 2.53 (mã commit tái lập); openssl 3.5 + Python `ssl` (mTLS 4 ca, 30/30 lần cùng kết quả); **Oracle AI Database 26ai Free 23.26.3**
  và **SQL Server 2022 CU27** trong Docker (`audit/bnx/dbrun.py`) — cả bế tắc ORA-00060 thật hai phiên, XACT_ABORT OFF làm lệch tiền 1 800 000;
  Kafka 3.9.0 Docker (nén nhật ký); `docker build --check`; google.protobuf 7.36.2.
- Cổng `audit/review/screen_code.py` thêm `lang: oracle|mssql` (chạy nguyên văn qua Docker; thiếu container → FAIL "NOT_VERIFIED", không PASS lặng lẽ),
  và `SC_REGDIR` để thử sổ nháp (`audit/bnx/screen_try.py`).
- Dò phát âm (`audit/bnx/probes/x1.md`, GPU, small+medium, 4 ngữ cảnh, ngưỡng 7/8, đối chứng âm 12/12 = 0/8): chỉ **JSON** («Giây-sơn» 8/8),
  **YAML** («Giam-mồ» 8/8) đạt → luật trong `lexicon_vi.BNX.yaml`. Git, GitLab, JWT, OAuth, gRPC, Elasticsearch, Couchbase, RabbitMQ, SWIFT, TLS không đạt →
  lời nói tiếng Việt, tên gốc chỉ trên màn hình.
- Nguồn: `audit/bnx/sources.md` (CBPR+/Clearstream 03/11/2026; NĐ 52/2024 Đ6 k3 "không thấp hơn"; TT 40/2024, TT 41/2025 (NHNN 07/11/2025), TT 64/2024,
  TT 19/2021, Luật Quản lý thuế 2019 Đ58; RFC 7515/7519/7636/6749/6750/8252/8446/8725/9068; OIDC Core; protobuf.dev; OAS 3.0.3; tài liệu Elastic, Couchbase 8.0
  + mã nguồn SDK, Kafka 4.4, Confluent 8.4, RabbitMQ, GitLab, Kubernetes + `rolling.go`, Docker, Oracle 23, Microsoft Learn; draft-ietf-httpapi-idempotency-key-header-08).

### Kiểm độc lập trước khi dựng (5 người đọc chỉ đọc, tiêu chí `learn_start/BRIEF_LS1.md` + `audit/bnx/BRIEF_READ.md`)
| Phát hiện | Số | Đã xử lý |
|---|---|---|
| MUST | 11 (L00 khối mật khẩu chỉ đúng ở một trạng thái kho; L01 regex `$` cho lọt `\n` + null lọt; L04 giây biên ngược RFC 7519; L09 128 vBucket mặc định bản 8.0 + công thức SDK thật; L10 ngược chiều tương thích lược đồ ×2; L12 thời điểm "đã nộp thuế" sai Luật QLT Đ58; L13 mô hình cuốn chiếu sai bộ điều khiển thật + thiếu `docker login`) | 11/11 |
| SHOULD / BLOCK-TERM / BLOCK-STEP / BLOCK-QUIZ | ≈ 116 (đếm lại từng dòng bảng của 5 báo cáo, theo nhóm bài: 29 + 18 + 28 + 15 + 26; sai số ±3 vì có dòng gộp nhiều ý) | áp tất cả trừ 3 có lý do: L06 lỗi 1205 SQL Server (chưa nguồn, chưa chạy); TT40 loại giao dịch tính hạn mức (chưa đọc nguyên văn — thêm ghi chú); chữ "bit" giữ như CSA/BNK |
Ba lỗi trong giáo án/VER do chính người điều phối viết cũng được sửa: chữ "tài liệu" (E29), dòng `fix` L12, quy tắc `>` của VER BNX:L04 → `>=` (RFC 7519 §4.1.4).

### Cổng cuối của BNX (OBSERVED 2026-11-11)
- lint 16/16: 0 FAIL, 0 WARN; render 0 vấn đề; `lv.py curriculum` 16 bài 0 lỗi; `check_curricula_graph` 0 chu trình, 0 VER hỏng, 0 ví dụ số thiếu VER;
  `verify_plan_curricula` 561 PASS / 0 FAIL; `verify_bnx` 280/280 PASS (không SKIP; chạy lại trong cổng cuối với container Oracle/SQL Server đang chạy).
- screen_code BNX: 167 khối + 7 nguồn → **174 PASS**, 0 FAIL/STALE/MISSING/ORPHAN (17 khối Oracle, 6 khối SQL Server chạy thật); 23 `unverified_claims` NOT_VERIFIED. Toàn kho: 712 khối, **903 PASS**, 0 FAIL/STALE/MISSING/ORPHAN.
- build 16/16 verify PASS (dựng **hai lượt**: lượt hai chỉ cho 9 bài đổi lời sau khi cổng `check_xref` bắt tham chiếu chéo, xem §6), một giọng NamMinh; ASR 174 câu gắn cờ đều đã xem xét (khối HAND "BNX L00–L15 NamMinh (2026-11-11, đợt LF1)" trong
  `audit/dms/asr_review_dms.py`) → **0 câu chưa xem xét**; `pack.py check --decode --course BNX`: 16 bài 0 vấn đề, giải mã trọn 16.

## 4. Cổng toàn kho (OBSERVED 2026-11-11)
- `audit_all`: **672 bài, 672 đã dựng, 0 bài có vấn đề** (lint, STALE theo dấu băm, giọng, ASR chưa xem xét, screen_code từng khoá); `status_report`: 672/672 bài, 6152 phút.
- `pack.py check --decode` 656 bài cũ: 0 vấn đề, giải mã trọn 656, 5937,9 phút (chạy 02:47→05:45 giờ máy; **không** video/`build_report` nào ngoài BNX đổi sau mốc bắt đầu, kiểm bằng `find -newermt`). BNX: giải mã lại 16/16 sau lần dựng cuối. `pack.py check` toàn kho: **672 bài, 0 vấn đề**.
- `check_xref` **0** (sau sửa, xem §6); `check_meta` 0; `check_course_refs` 0; verify_jva 110/110; verify_bnk 21/21; verify_cs112 FAIL 0; verify_cs112_p2 37/0; test_lint 0 FAIL; mẫu `.tpl` 0 lệch (CS112, DMS, CS115); video phỏng vấn 92/92 trùng byte.
- `scan_ctrl`: **59** lượt (LS1 ghi 8). Đã phân loại: 8 JVA cố ý + 51 BNX, **tất cả là TAB (0x9)** nằm trong khối mã `show` của L06/L07/L10 (đầu ra nguyên văn của sqlcmd/sqlplus/Kafka). Kiểm bằng máy: 0 TAB nằm trong công thức, trong lời đọc, hay đứng trước `ext{`/`imes`/`heta`; ca đối chứng dương 4/4. Mốc mới = 59.

## 5. Còn mở / NOT_VERIFIED
1. **Tai người**: phát âm chỉ ASR-checked; chưa ai nghe 16 bài BNX.
2. **Sản phẩm không chạy thật**: Elasticsearch, Couchbase, RabbitMQ, Schema Registry, cụm Kubernetes, GitLab runner, Oracle In-Memory/Sharding (bản Free INMEMORY_SIZE=0),
   JDBC với ojdbc (đã chạy tay một lần ngoài kho, không trong cổng), máy chủ ủy quyền OAuth thật. Bài nói rõ phần mô phỏng/giản lược.
3. **Pháp lý chỉ nguồn thứ cấp**: nguyên văn TT 40/2024 Điều 26 (loại giao dịch tính hạn mức), TT 41/2025 (300 triệu là nâng hạn mức hay hạn mức riêng),
   TT 64/2024 Phụ lục 01, TT 19/2021 Điều 20. Phải đọc lại văn bản gốc trước khi dùng ngoài video.
4. **Sổ mã SQL Server** có tên máy chủ container `461d1255632f` trong `expect_stdout`: dựng lại container mới → phải sinh lại các mục đó.
   Cổng screen_code của BNX (và `audit_all`) cần `docker start bnx-ora bnx-mss`; thiếu thì FAIL có nhãn NOT_VERIFIED.
5. Bài BNX dài 11,5–15,8 phút (BNK 7–10 phút): đánh đổi để đủ điều kiện áp dụng mà người đọc đòi; có thể tách L06, L02 nếu người học thấy nặng.
6. Hiệu quả ghi nhớ của trang trên chính người học: NOT_VERIFIED (cơ sở là nghiên cứu chung: Roediger & Karpicke 2006, Cepeda và cs. 2006, Dunlosky và cs. 2013).
7. Chưa commit (chờ người dùng).

## 6. Lỗi do chính đợt này gây ra và cổng đã bắt được
Chi tiết ở `knowledge-graph_LF1_20261111T0500Z.md` (bảng LE-1…LE-6). Hai điều đáng nhớ:
- **`check_xref` (cổng "bài tự đứng được", yêu cầu người dùng 2026-11-09) báo 77 lượt ở BNX** mà báo cáo trước của tôi không liệt kê. Phân loại: 11 vi phạm thật (câu "như đã học ở khoá trước" trong lời đọc 9 bài; cổng còn bỏ sót một cụm "khoá học về hệ thống ngân hàng trước") và 66 dương tính giả ("CAS" = Compare-And-Swap của Couchbase trùng mã khoá CAS; "INT" = kiểu số nguyên SQL trùng mã khoá INT). Đã sửa 11 chỗ trong nguồn bài và dựng lại 9 video; vá cổng **hẹp** (hai mã mơ hồ chỉ tính khi sau "khoá/bài" hoặc trước "Lxx"; thêm tên tắt "hệ thống ngân hàng"), ca đối chứng 11/11 đúng: vẫn bắt "khoá CAS", "bài CAS L05", "khoá học về hệ thống ngân hàng".
- **Bẫy lặp lại từ LS1**: `build` không sinh `preview.html` (9 bản cũ sau dựng lại) → `pack.py preview`; và `TaskStop` trên Windows không dừng cây tiến trình (hàng dựng cũ chạy song song) → `taskkill /T`.
