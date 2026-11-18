# HANDOVER — Cập nhật 2026-11-13 (chiều): lượt rà + kế hoạch AF3 — kho vẫn `PARTIAL` (49/701 bài đạt chuẩn "Tự làm"); chưa phải bản final

> **Phiên mới đọc theo thứ tự**: [`audit/review/audit_final/handover_AF3_20261113T1240Z.md`](file:///D:/research-video/audit/review/audit_final/handover_AF3_20261113T1240Z.md) → [`plan_AF3_20261113T1240Z.md`](file:///D:/research-video/audit/review/audit_final/plan_AF3_20261113T1240Z.md) (9 gói việc, 6 quyết định, 12 contract bottleneck, ngưỡng chốt từng chặng) → [`knowledge-graph_AF3_20261113T1240Z.md`](file:///D:/research-video/audit/review/audit_final/knowledge-graph_AF3_20261113T1240Z.md) → [`STATE.md`](file:///D:/research-video/audit/review/audit_final/STATE.md).
> - **Phiên này chỉ rà và lập kế hoạch**: không sửa bài, không dựng video. Mốc git: `eb64a29` (AF2 đã commit).
> - **Bản sửa 2 (14:10Z)**: ổ D đã mở rộng (trống 515 GB, hết chặn). JD mới thêm phần VPBank: 13 nhóm chủ đề chưa có bài → kế hoạch thêm **BNX L24–L36**. Đã dọn tệp dư (sản phẩm cũ trong `out/`, 67 nhật ký, bộ đệm, 20 script sinh một lần → `archive/one_off_generators/`) và làm tươi `audit_all` 701/0, `STATUS.md` 701/701, `TRACKS.md`, `pedagogy_scan.tsv`.
> - **Cổng nhẹ chạy lại 12:27–12:52Z: 11/11 PASS** (xref, meta, course_refs, next_refs 551/0, legal, arith 226/0, đồ thị, plan_curricula 570/0, test_lint, lab_gate 49/0, `pack.py check` 701/0). Cổng nặng chưa chạy lại (số AF2 03:52Z).
> - **Đổi thứ tự so với bản phác cũ**: làm cổng E52 (thuật ngữ tại chỗ) và E55 **trước** khi nâng hàng loạt; chốt cuốn chiếu từng chặng (nhãn "ĐÃ CHỐT" trên `HOC_TAP.html`), Chặng 1 trước.
> - **Khoá mới theo kế hoạch**: PYT 12 (Python), CPR 10 (C và bộ nhớ), LNX 10 (Linux và Docker), MLP 14 (học máy thực hành), PRJ 11 (một hệ thống lớn dần qua 11 chặng).
> - **Còn lệch**: ROADMAP §2–§3 (bảng số ngày 31/10); nền chung của `tracks.yaml` chưa có FND/JV2.
> - **Còn mở**: 652 bài chưa có Tự làm; 49 bài AF2 chưa qua người đọc độc lập; lab chưa thử máy sạch; tai người; 6 văn bản pháp lý `CHUA_KIEM`; sản phẩm chỉ mô phỏng.
---

# HANDOVER — (lịch sử) 2026-11-13 sáng: đợt AF2 (thực hiện kế hoạch) — PARTIAL: 49/701 bài đạt chuẩn "Tự làm"; trang học mới; AF3 còn lại

> **Phiên mới đọc theo thứ tự**: [`audit/review/audit_final/handover_AF2_20261113T0400Z.md`](file:///D:/research-video/audit/review/audit_final/handover_AF2_20261113T0400Z.md) → [`plan_AF3_next.md`](file:///D:/research-video/audit/review/audit_final/plan_AF3_next.md) (việc còn lại, thứ tự ưu tiên: PYT → BNX → INT/ACB → chặng 5 → 6–8 → 9–11 + MLP → dự án chặng → E52/E55 → pháp lý → mẫu G) → [`STATE.md`](file:///D:/research-video/audit/review/audit_final/STATE.md) → `knowledge-graph_AF2_*.md`.
> - **Bắt đầu học**: mở [`HOC_TAP.html`](file:///D:/research-video/HOC_TAP.html) (thiết kế lại): 701 bài, 113,4 giờ, 11 chặng. Chặng 1 = **FND (11) → JVA (13) → JV2 (10)**, 34 bài, 8,3 giờ. Chuẩn bị máy: `labs/ENV.md`, `bash labs/check_env.sh`. Mỗi bài AF2 có cảnh **Tự làm** + `labs/<KHOÁ>/<Lxx>/` chấm bằng `bash labs/cham.sh`.
> - **Đã làm**: cổng mới (E51/E53 trong lint, `lab_gate`, `arith_scan`, `check_next_refs`, `check_legal` + sổ `audit/legal/registry.yaml`); khoá mới FND, JV2; nâng JVA, BNK (49 bài, 12,0 giờ, lab 49/49 PASS); sửa 26 bài theo mẫu F; xếp dãy học không lệch "Bài sau" (551 lời hẹn, 0 lệch); `.dim` tương phản 2,2 → 4,8:1; dọn 16 bàn giao cũ vào `archive/`; README viết lại.
> - **Cổng cuối** (`audit/review/audit_final/logs/gates_af2.out`): verify fnd 70/70, jv2 85/85, jva 143/143, bnk 36/36, bnx 494/494; `pack.py check` 701 bài 0 vấn đề; ASR 0 câu chưa xem xét; screen_code FAIL 2 = BNX L19 chập chờn lần chạy lạnh (chạy lại: 0 FAIL).
> - **Còn mở (nói thẳng)**: 652 bài chưa có Tự làm; chưa có khoá PYT (Python từ đầu) — BNX dùng Python ở 18 bài; tai người chưa nghe; 6 văn bản pháp lý `CHUA_KIEM` + chưa mở Công báo; BNK L06/L07/L10 là mô phỏng; chưa đo lại bằng người đọc độc lập (mẫu G) nên chưa gọi "final".
> - **Chưa commit git**: chờ người dùng.
---

# HANDOVER — (lịch sử) 2026-11-13: đợt rà AF1 (chỉ rà, không sửa) — CHƯA đạt bản final; kế hoạch AF2 đã viết

> **Phiên mới đọc theo thứ tự**: [`audit/review/audit_final/handover_AF1_20261112T1810Z.md`](file:///D:/research-video/audit/review/audit_final/handover_AF1_20261112T1810Z.md) → [`plan_AF1_20261112T1810Z.md`](file:///D:/research-video/audit/review/audit_final/plan_AF1_20261112T1810Z.md) (kế hoạch AF2, 8 gói việc, 6 quyết định, 8 contract bottleneck) → [`audit/review/sample_f/REPORT.md`](file:///D:/research-video/audit/review/sample_f/REPORT.md) → `knowledge-graph_AF1_20261112T1810Z.md`.
> - **Cổng chạy lại phiên này đều sạch**: xref/meta/course_refs 0; đồ thị lộ trình 0 lỗi; VER 570/0; lint tự kiểm 0 FAIL; `pack.py check` 680 bài 0 vấn đề. Các cổng nặng (`audit_all`, `screen_code`, `verify_<khoá>`) chưa chạy lại, vẫn là số của LF2.
> - **Mẫu F (38 bài, đọc độc lập)**: MUST 3/38 (AGT L04, DVO L03: giáo án hứa điều bài không dạy; BNX L12: Luật Quản lý thuế 38/2019 có vẻ đã bị thay, chờ văn bản gốc); 37 SHOULD ở 28 bài; thuật ngữ giảng đủ tại chỗ chỉ 7/38 bài; có việc tự làm kèm kết quả đối chiếu chỉ 2/38 bài.
> - **Đường đi người mất gốc**: JVA theo được trọn; hụt nền từ BNK L02 (Spring, CSDL, HTTP chưa dạy); kẹt khi thực hành ở BNX L00 (bash, cài Git, Python). Sau JVA L00 không bài nào giao việc tự gõ; không có bài tập, không có dự án; 532/680 bài không có khối mã; không có khoá Python, Java trung cấp, học máy thực hành.
> - **Môi trường trôi**: JDK trên PATH là 21.0.13 (LF2 ghi 22.0.2); `gcc 16.2.0` đã có (LF2 ghi không có trình biên dịch C).
> - **Chưa commit** các tệp AF1 (chờ người dùng).
---

# HANDOVER — Cập nhật 2026-11-12: đợt LF2 XONG (đọc chốt chặng 6–11 + phủ CV) — phiên bản học đã chốt

> **Phiên mới đọc theo thứ tự**: [`audit/review/learn_final/handover_LF2_20261112T1620Z.md`](file:///D:/research-video/audit/review/learn_final/handover_LF2_20261112T1620Z.md) (bàn giao cuối) → [`report_LF2.md`](file:///D:/research-video/audit/review/learn_final/report_LF2.md) (báo cáo ngắn, đánh giá chất lượng) → [`knowledge-graph_LF2_20261112T1620Z.md`](file:///D:/research-video/audit/review/learn_final/knowledge-graph_LF2_20261112T1620Z.md) (chứng cứ LF2-01…17) → `audit/review/learn_final/STATE.md`.
> - **Học ngay**: mở [`HOC_TAP.html`](file:///D:/research-video/HOC_TAP.html): 680 bài, 11 chặng, 105,2 giờ video, liên kết chết 0. Chặng 3 có BNX 24 bài (L16–L23 theo CV).
> - **Số đo (cổng cuối `logs/gates_post.out`, 2026-11-12T16:18Z)**: đọc độc lập 537/537 bài chặng 6–11, MUST đã sửa; 226 bài dựng lại 226/226 PASS; verify_bnx 493/493; verify_plan_curricula 570/0; screen_code FAIL 0 STALE 0; check_xref/meta/course_refs 0; `pack.py check` 680 bài 0 vấn đề; `audit_all` 680/680 0 vấn đề; interview 92/92; ASR 0 câu chưa xem xét.
> - **Còn mở (nói thẳng)**: tai người nghe (mọi lý do ASR `NOT_VERIFIED`); Elasticsearch, Couchbase, RabbitMQ, Kubernetes, GitLab runner, AEM chỉ mô phỏng, không có trình biên dịch C; TT 77/2025 chỉ qua bản hợp nhất, TT 46/2024/TT-BTC chưa đọc; jar/venv của `audit/bnx/deps/` bị `.gitignore` (README có lệnh tải + sha256); hiệu quả học thật chưa đo.
> - **Chưa commit git**: chờ người dùng yêu cầu.
> - Quy trình sửa một bài và các bẫy: `handover_LF2_20261112T1620Z.md` §5 và §7. Cổng cuối chạy lại: `docker start bnx-ora bnx-mss` rồi `bash audit/review/learn_full/final_gates.sh > audit/review/learn_final/logs/gates_post.out 2>&1`.
---

# Lịch sử cũ hơn (2026-11-01 → 2026-11-11)

> Các mục LF1, LS1, SC1, mẫu C/D/E, rà soát đợt B/C, khoá JVA, bộ phỏng vấn ACB: [`archive/handovers/HANDOVER_den_2026-11-11.md`](archive/handovers/HANDOVER_den_2026-11-11.md). Bàn giao chi tiết từng đợt vẫn ở `audit/review/learn_*/`, `audit/review/sample_*/`, `interview/HANDOVER_INTERVIEW.md`.
