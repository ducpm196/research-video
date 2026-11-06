# HANDOVER — Cập nhật phiên 2026-11-05 03:20

> **Báo cáo bàn giao mới nhất**: Vui lòng đọc file [handover_2026-11-05_0320.md](file:///D:/research-video/handover_2026-11-05_0320.md) để xem chi tiết đầy đủ về bằng chứng thực nghiệm (EVIDENCE), bảng xử lý nút thắt hợp đồng (Contract Bottlenecks), phòng tránh lỗi thường gặp, và cột mốc lịch sử **CÁN ĐÍCH 100% TOÀN DỰ ÁN — 38 KHOÁ HỌC, 611/611 BÀI ĐÃ DỰNG THÀNH CÔNG (5,259 phút video ~87.65 giờ, 48,191 câu thoại sạch, 0 lỗi giật cụt, hoàn tất 14/14 bài khoá IRS L00–L13)**.

---

# HANDOVER — phiên 2026-11-01 → 2026-11-03

Đọc nhanh: phần 1 (trạng thái) và phần 4 (việc làm ngay). Số liệu dưới đây là kết quả chạy lệnh ngày 2026-11-03 (~12:15Z), không phải ước đoán.
Nhớ dài hạn: `C:\Users\AI_Worker\.claude\projects\D--research-video\memory\` (đặc biệt `production-progress.md`) và `curriculum/ROADMAP.md` §8.1.

## 1. Trạng thái hiện tại

### Đã xong (kiểm bằng lệnh)
- **Đợt A + B (đào sâu `depth: full`)**: 23 + 8 khoá đã dựng lại, mọi bài `PASS`, ASR sạch.
- **Đợt C — bài hành trình theo trục thời gian**: 29 khoá đã có bài mới, đã dựng, ASR sạch (DBS L17, DSY L15, EVT L11, NET/WEB/SEC L15, SAR L13, SDP L17, DVO L13, DEN L14, SWF L13, CLC L12, LLM L14, AIF L14, MLO L14, DSC L15, DAN L12, AGT L12, BCH L12, PLC L13, OSY L15, CSA L16, TOC L14, CS112 L29, CS115 L45, DMS L20, RBM L17, ROB L13, ESY L15; CLD L15 từ trước). Mỗi bài có `audit/<khoá>/sources_<id>.md` (câu trích nguyên văn + mục "Điều KHÔNG dạy").
- **Khoá mới đã dựng xong (video PASS)**: SEP (12 bài), CAS (12), PAR (14), RLN (14; lô 49).
- **Khoá mới đã soạn đặc tả, CHƯA dựng**: IRS (14 bài L00–L13), CVI (13 bài L00–L12).
- Cổng toàn kho vừa chạy: `tests/test_lint.py` → `tests: 0 FAIL`; `audit/verify_plan_curricula.py` → `474 PASS · 0 FAIL`; `check_curricula_graph.py` → 609 bài, tham chiếu hỏng 0, chu trình 0, VER lệch 0; `check_course_refs.py` → 0; `check_meta.py` → 0; `sync_tpl_from_lesson.py --all` → `0 mẫu lệch bài`; `check_checklib_dupes.py` → không trùng; `verify_irs.py` 123/123 PASS; `verify_cvi.py` 112/112 PASS; `layout_scan.py` IRS 1262 khung / CVI 1178 khung → 0 lỗi; lint mọi bài IRS/CVI → 0 FAIL 0 WARN; `lv.py curriculum` IRS 14 bài / CVI 13 bài → 0 lỗi.

### Đang làm dở
1. **ASR RLN chưa rà**: 71 câu chưa xem xét (RLN L00–L11 vừa dựng xong ở lô 49). Chưa chạy quy trình HAND.
2. **ASR PAR L13**: 1 câu chưa xem xét — "Mỗi thẻ đồ hoạ khi ấy chỉ có 3 GB bộ nhớ, nên cả mạng không vừa trong một thẻ." (khớp 1,0, chỉ cần lý do "GB đọc ghi-ga-byte, ASR viết 3GB"; bài vừa dựng lại ở lô 50).
3. **IRS và CVI chưa dựng video** (chưa xếp hàng, chưa có `out/IRS`, `out/CVI` đầy đủ). Cả hai do tác tử soạn nhưng tác tử dừng vì giới hạn tuần trước khi gửi báo cáo cuối → **chưa ai tự xem khung hình / đọc nguồn của hai khoá này**. Phải làm bước kiểm tay ở §4 trước khi dựng.
4. **HCI (12 bài) và GFX (13 bài)**: mới có giáo án `status: planned` (`curriculum/hci.yaml`, `curriculum/gfx.yaml`), chưa có `lessons/hci`, `lessons/gfx`.
5. **AIF L11**: 1 câu chờ tai người — "Xác suất vừa mưa vừa mang ô bằng xác suất trời mưa, nhân với xác suất mang ô khi đã biết trời mưa." Cố ý để `chưa xem xét`; đừng cho `asr_hand_gen` tự ghi lý do (đã gỡ tay một lần).

### Blocker
- **Giới hạn sử dụng tuần của tác tử**: reset **7/11 lúc 14:00 (Asia/Ho_Chi_Minh)**. Trước đó không gọi được tác tử con (Agent/SendMessage trả 429). Việc nhẹ làm trực tiếp được; việc soạn HCI/GFX cần chờ.
- **Bộ nhớ máy**: 2026-11-03 hệ thống từng tự dừng 3 lệnh chờ nền vì thiếu RAM (còn ~17/32 GB sau đó). Chỉ chạy **một** hàng dựng + tối đa 1–2 tác tử; render phải tuần tự (xem §3).
- **Cần người nghe (NOT_VERIFIED bằng tai)**: câu AIF L11 ở trên; câu CSA L01 "…dãy bit 1 1 0 0, 1 0 0 0…" (medium nghe nhầm nhóm số, small đúng 3/4); tên đọc chưa chắc: "quaternion" (RBM, 4/8), Amazon (PARTIAL), Netflix/Microsoft (PARTIAL), Cloudflare "Cờ-lao-phle-ơ" (6/8), SHA-1 "ét-hát-a một" (7/8), flash (6/8), Twitter "Tuýt-tơ" (7/8). Phát âm mới chỉ là ASR-checked.
- **Git**: chưa commit gì. `git status` hiện **2740 tệp ở trạng thái `A` (đã staged)** — toàn bộ kho nằm trong index từ đầu phiên (không script nào trong `audit/`, `tools/`, `.claude/` chạy `git add`; tìm thấy 0 chỗ). Đừng chạy lệnh đổi index khi chưa hỏi người dùng; commit chỉ khi người dùng yêu cầu.
- **CS115 là khoá mặc định** nên không nạp `lexicon_vi.CS115.yaml` → "AdamW" chỉ hiện trên màn hình, lời đọc nói "bộ Adam tách rời"; muốn đọc được phải sửa lexicon dùng chung (ảnh hưởng mọi khoá — chưa làm).

## 2. Tệp vừa tạo / sửa (theo nhóm; danh sách đầy đủ: `git status`)
- **Bài mới**: `lessons/<khoá>/` — 29 bài hành trình (liệt kê ở §1); `lessons/sep/L00–L11`, `lessons/cas/L00–L11`, `lessons/par/L00–L13`, `lessons/rln/L00–L13`, `lessons/irs/L00–L13`, `lessons/cvi/L00–L12`.
- **Bài cũ sửa nội dung/câu nối**: bài áp chót/bài cuối của từng khoá có hành trình (recap trỏ bài sau, `forward_ref: true`); CSA L14, OSY L13, DMS L18/L19, CS112 L28, TOC L13, CS115 L43/L00 (bản đồ khoá); ESY L10 (hook cơ chế Pathfinder: tác vụ cao chờ khoá do tác vụ thấp giữ) và ESY L15; AIF L13 (bảng bản đồ); CLC L12, SEP L09, PAR L08/L11/L13 (viết lại câu ngắn); nhiều bài đợt A/B (xem `audit/review/batch*.log`).
- **Nguồn & kiểm theo khoá**: `audit/<khoá>/sources_*.md`, `audit/<khoá>/verify_<khoá>.py` (+ `verify_parts/`, `ver/` ở SEP/CAS/PAR/RLN/IRS/CVI), `audit/<khoá>/probes/*` (thử phát âm).
- **Giáo án / lộ trình**: `curriculum/<khoá>.yaml` (thêm bài hành trình; `spec_planned`→`spec` cho CAS/SEP/PAR/RLN/IRS/CVI), `curriculum/ROADMAP.md` (§8.1 mục 3 đánh ✅ + tiến độ 2026-11-02/03), `curriculum/STATUS.md` (SINH TỰ ĐỘNG — sinh lại, đừng sửa tay).
- **Công cụ dùng chung**:
  - `tools/checklib.py` (+ hàm tiền tố `rx_/bt_/thompson_`, `cas_`, `par_`, `rln_`, `irs_`, `cvi_`, mô phỏng `goodness_scan/cfs_*/eevdf_run`),
  - `tools/registry/lexicon_vi.<KHOÁ>.yaml`, `symbols.<KHOÁ>.yaml` (khoá mới + khoá có hành trình),
  - `audit/verify_plan_curricula.py` (chỉ thêm dòng `rec("<KHOÁ>:Lxx")`, sửa bằng Edit),
  - `audit/dms/asr_review_dms.py` (HAND blocks nhãn "Đợt A/B/C…"; **đã sửa** nhận `asr_reviewed:   # chú thích` và bài chưa có khoá — thêm trước `scenes:`),
  - `audit/review/sync_tpl_from_lesson.py`, `sync_tpl_asr.py` (khớp mẫu tên ngắn, bỏ qua bài không mẫu),
  - `audit/cs112/probe_terms.py` (tên tệp giữ chữ số — sha1/sha256 từng ghi đè nhau).
- **Tệp tạm** (ngoài repo): `C:\Users\AI_WOR~1\AppData\Local\Temp\claude\D--research-video\5a369d5e-0041-45d9-9718-0254d5033c30\scratchpad\` — `brief_waveC.md`, `brief_newcourse.md` (brief giao tác tử), `fix_reasons.py` (sửa lý do HAND theo lexicon), `hand_triage.py`, `render_locked.py` (khoá render tuần tự).

## 3. Lệnh test / build (chạy từ `D:\research-video`, đặt `PYTHONIOENCODING=utf-8`)
```
# cổng toàn kho
.venv/Scripts/python tests/test_lint.py                       # kỳ vọng "tests: 0 FAIL"
.venv/Scripts/python audit/verify_plan_curricula.py | tail -1  # kỳ vọng 0 FAIL
.venv/Scripts/python audit/check_curricula_graph.py            # hỏng 0, chu trình 0
.venv/Scripts/python audit/review/check_course_refs.py         # 0 vấn đề (luật R4: "bài cuối" ở bài áp chót)
.venv/Scripts/python audit/review/check_meta.py                # 0 vấn đề
.venv/Scripts/python audit/review/sync_tpl_from_lesson.py --all   # 0 mẫu lệch bài
.venv/Scripts/python audit/review/audit_all.py && .venv/Scripts/python audit/review/tts_speed_scan.py && .venv/Scripts/python audit/review/status_report.py

# một bài
.venv/Scripts/python tools/lv.py lint   lessons/<k>/<bài>.yaml     # 0 FAIL 0 WARN
.venv/Scripts/python tools/lv.py render lessons/<k>/<bài>.yaml     # 0 vấn đề (KHÔNG chạy song song nhiều render: ffmpeg/ASR hết RAM)
.venv/Scripts/python tools/lv.py verify lessons/<k>/<bài>.yaml     # PASS (STALE nếu lời đọc/lexicon đổi sau lúc dựng)

# dựng hàng đợi (tuần tự, một giọng, nền)  — log: audit/review/batchNN.log
bash audit/.build_queue_run.sh <KHOÁ> L00 L01 ...                  # ví dụ IRS
grep -E "→ (PASS|FAIL)|FAIL sau|BLOCKED" audit/review/batchNN.log

# rà ASR sau khi dựng (quy trình HAND)
audit/review/asr_flags.py <KHOÁ>
audit/review/asr_hand_gen.py <KHOÁ> "<nhãn>" <tệp>   # 3 tham số
hand_triage.py <tệp>           # ở scratchpad: lọc NGẮN ≤7 từ <0,7 / THẤP <0,7 / SAI-NHÓM
fix_reasons.py <tệp> '{"tiền_tố/":"lý do đúng"}'   # sửa lý do tự sinh cho tên riêng/đơn vị theo lexicon
audit/review/asr_hand_insert.py <tệp> "<nhãn>" → audit/dms/asr_review_dms.py --course <KHOÁ> <ids> → audit/review/sync_tpl_asr.py <KHOÁ> <ids> → lv.py asr <bài>
```
Nếu TTS bị chặn/hết quota: chờ theo giờ (không kiểm mỗi phút); hàng dựng tự thử lại 3 phút/lượt rồi dựng lại bằng giọng gốc, cả bài cùng một giọng.

## 4. Bước tiếp theo ngay khi mở phiên mới
1. `git status --short | cut -c1-2 | sort | uniq -c` (đừng đổi index) và `ls out/_render.lock` — nếu có thư mục khoá mồ côi thì `rmdir out/_render.lock`. Chạy bộ cổng ở §3 để xác nhận mốc trên còn đúng.
2. **Việc nhẹ, làm trực tiếp (không cần tác tử)**:
   a. Rà ASR **RLN** (71 câu): `asr_hand_gen.py RLN "Khoá mới: RLN" <tệp>` → triage → sửa lý do cho tên đã định (epsilon đã đổi "xác suất khám phá"; theta "tê-ta"; PPO/UCB chưa có trong lời) → insert → `asr_review_dms.py --course RLN L00 … L13` → `sync_tpl_asr.py` → `lv.py asr` từng bài → `asr_flags.py RLN` phải "0 câu chưa xem xét". Câu ngắn ≤7 từ <0,7 thì viết lại, rồi xếp dựng lại bài đó.
   b. **PAR L13**: thêm lý do 1 câu còn lại (GB → "ghi-ga-byte", ASR viết "3GB") theo cùng quy trình.
3. **Kiểm tay IRS và CVI trước khi dựng** (tác tử chưa báo cáo): với mỗi khoá đọc `audit/<khoá>/sources_*.md` (câu trích có nguyên văn? mục "Điều KHÔNG dạy"?), chạy `render`, mở bằng Read khung đầu / mọi khung SVG / pitfall / khung cuối (`out/<KHOÁ>/<id>/frames/`), soát: nhãn đè hình, số bị ngắt dòng (dùng `&nbsp;`), tên ngoại dưới 7/8 có bị đọc trong lời không, thời lượng ≤ ~12 phút (bài hành trình IRS L13, CVI L12 ≤ ~18 phút). Kiểm riêng nDCG (lỗi thật từng gặp: 0,986 vs 0,985) và các công thức IoU/NMS/Otsu. Sửa rồi mới `bash audit/.build_queue_run.sh IRS L00 … L13` và `CVI L00 … L12`, rồi rà ASR như 2a.
4. **Sau khi tác tử dùng lại được (từ 7/11 14:00)**: soạn **HCI** (12 bài) rồi **GFX** (13 bài) bằng `scratchpad\brief_newcourse.md` (mỗi lần tối đa 1–2 tác tử, render qua `render_locked.py`; tác tử không được chạy lệnh git). Thêm bài hành trình cuối cho mỗi khoá nếu giáo án chưa có (HCI: Hawaii 2018 theo báo cáo FCC là ứng viên sự cố; xem `references/case-lessons.md`).
5. **Cuối đợt**: chạy cổng toàn kho + `audit_all.py`, `tts_speed_scan.py`, `status_report.py` (sinh `curriculum/STATUS.md`), cập nhật `curriculum/ROADMAP.md` và `memory/production-progress.md` (không chép số tay).
6. Báo người dùng danh sách câu cần nghe bằng tai (§1 "Cần người nghe"). Chỉ commit khi người dùng yêu cầu.

## 5. Lỗi thường gặp đã gặp phiên này (tránh lặp)
- Thêm bài cuối ⇒ câu "bài cuối của khoá" ở bài **áp chót** sai (R4); bài 0 (bản đồ khoá) phải thêm bài mới (E37) — đừng xoá số bài khỏi lời đọc để qua lint.
- `asr_hand_gen` xếp nhầm tên riêng/đơn vị (KiB/MiB, theta, Hz, Kleene, Turing, Amazon, flash, "ki-lô-gam") vào "lệch âm" → luôn sửa lý do theo lexicon trước khi chèn.
- `medium` hay lặp nhóm chữ số vừa nghe ("1100, 1100"): probe lại bằng `small` trước khi kết luận TTS sai.
- Render song song ⇒ ffmpeg `Cannot allocate memory` (đã gặp SAR L13). Thiếu RAM ⇒ lệnh nền bị dừng — chạy lại, đừng dựng song song.
- Trang bị chặn (403/429): dùng bản chính thức khác/đường dẫn "suy ra" ghi rõ; **không** dùng dịch vụ lách chặn; không dạy chi tiết chỉ có ở nguồn không đọc được.
- Số có dấu cách nghìn trong ô bảng bị ngắt dòng ⇒ `50&nbsp;000`. Câu >38 từ hoặc `focus` sai số mục ⇒ lint E31/WARN.
