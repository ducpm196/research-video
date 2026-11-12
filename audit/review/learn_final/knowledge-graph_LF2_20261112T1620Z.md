# knowledge-graph_LF2_20261112T1620Z: đồ thị chứng cứ của đợt LF2 (đọc chốt chặng 6–11, phủ CV, chốt phiên bản học)

Chỉ ghi nút OBSERVED (máy chạy trong phiên 2026-11-11 → 11-12, giờ UTC) hoặc CITED (báo cáo tác tử / đợt trước / văn bản thứ cấp). Môi trường: Windows 11; `.venv` Python 3.13.5; JDK 22.0.2; Go và venv riêng cho BNX L20, L23 (`audit/bnx/deps/`); Docker `bnx-ora` (Oracle AI Database 26ai Free), `bnx-mss` (SQL Server 2022); ffmpeg/ffprobe; TTS edge-tts giọng vi-VN-NamMinhNeural.

| ID | Khẳng định | Phương pháp | Quan sát | validity | checked_at |
|---|---|---|---|---|---|
| LF2-01 | 537/537 bài chặng 6–11 có người đọc độc lập đọc trọn (48 lô) | cộng dòng `ĐÃ ĐỌC K/K` trong `reports/B01…B48.md` (B05 gộp B04) | mọi lô K/K = số bài của lô trong `batches.json`; 4 lô B21, B22, B45, B46 khôi phục nguyên văn từ bản ghi phiên | VALID (CITED: báo cáo tác tử; số lô OBSERVED) | 2026-11-12 |
| LF2-02 | Mọi bài có MUST đã sửa và dựng lại, không bài nào lệch đặc tả | đối chiếu 40 dòng MUST ở `reports/` ↔ `rebuild.queue`/`rebuild.done` ↔ `pack.py check` | 40/40 bài MUST nằm trong hàng dựng và có `verify … PASS`; `pack.py check` 0 STALE | VALID | 2026-11-12T16:1xZ |
| LF2-03 | Hàng dựng lại hoàn tất: 226 bài, 0 bài FAIL tồn | `queue_remaining.sh` = 0; với mỗi dòng `FAIL sau` kiểm có `verify … PASS` về sau | 226/226; 41 bài FAIL tạm (tên hàm trùng `bnx_fee`, DBS L16 tràn khung) đều đã PASS về sau | VALID | 2026-11-12T13:52Z |
| LF2-04 | 8 bài BNX L16–L23 (CV) soạn, kiểm chạy thật, dựng | `verify_bnx` + `screen_try.py --merge` + dựng `rebuild_lf2.sh` | `verify_bnx: 493/493 PASS`; sổ screen BNX 331 khối PASS; dựng PASS, ASR khớp TB 0,94–0,97 | VALID | 2026-11-12T14:59Z |
| LF2-05 | Không có âm thanh bị cắt cụt ở BNX | `tts_speed_scan.py 0.22 BNX` | `3586 câu, 0 câu < 0.22 s/từ` | VALID | 2026-11-12T13:5xZ |
| LF2-06 | Máy nghe: 0 câu chưa xem xét ở mọi khoá dựng lại | `asr_flags.py <khoá>` cho 38 khoá; `asr_review_dms.py` ghi 79 lý do (BNX 76, AIF 1, BCH 1, RBM 1) rồi `lv.py asr` | sau ghi: BNX/AIF/BCH/RBM 0; còn lại 0; `audit_all` 0 vấn đề | VALID (lý do đều `NOT_VERIFIED bằng tai người`) | 2026-11-12T13:55Z |
| LF2-07 | Cổng cuối sạch trên kho sau sửa/dựng cuối | `final_gates.sh` → `logs/gates_post.out` | verify_jva 110/110; bnk 21/21; bnx 493/493; cs112_p2 37/0; plan_curricula 570/0; xref/meta/course_refs 0; lint 0 FAIL; sync_tpl 0 lệch; screen_code PASS 1089 FAIL 0 STALE 0; scan_ctrl 59 (mốc đã biết) | VALID | 2026-11-12T16:18Z |
| LF2-08 | Toàn kho: 680 bài có video, khớp đặc tả, không vấn đề | `pack.py check`; `audit_all.py` (không tham số); `status_report.py` | `680 bài có video · có vấn đề 0 · 6312,0 phút`; `audit_all: 680/680, 0`; `680/680 hoàn thiện` | VALID | 2026-11-12T16:1xZ |
| LF2-09 | BNX giải mã trọn bằng ffmpeg | `pack.py check --decode --course BNX` | `24 bài có video · có vấn đề 0 · tổng 365,4 phút · giải mã trọn 24` | VALID | 2026-11-12T16:1xZ |
| LF2-10 | Trang học đúng kho, không liên kết chết | `pack.py preview`, `pack.py page` | `HOC_TAP.html: 680 bài, 4220 liên kết tệp, 1575 neo, chết 0; câu+đáp án 680/680; khung hình 680/680; 3,94 MB`; `xem.html 6257 liên kết chết 0` | VALID | 2026-11-12T16:1xZ |
| LF2-11 | Bản sao video phỏng vấn trùng byte | `interview_sync_video.py`, `--check` | `92 pairs, 92 identical, 0 mismatched` (BNK L13 đã dựng lại) | VALID | 2026-11-12 |
| LF2-12 | MASTER_CURRICULUM_INDEX khớp kho: 680 bài, 105,2 giờ; BNX 24 bài | `master_sections.py` sinh LF_STAGES/LF_TIERS/LF_BNX + sửa tay Mục 2A/7/8, sơ đồ | `đã ghi [LF_STAGES, LF_TIERS, LF_BNX]; 680 bài có video, 105.2 giờ`; BNX 365,36 phút | VALID | 2026-11-12 |
| LF2-13 | Mọi thuật ngữ kỹ thuật trên CV có bài dạy | `cv_scan.py` | còn 2 mục "MỎNG" (CQRS, DLQ) do đếm từ khoá; bài chính EVT L05 (tách ghi–đọc, nhắc CQRS 1 lần) và EVT L02 (kênh thư chết, nhắc DLQ 7 lần) | VALID (đọc lại bằng tay) | 2026-11-12 |
| LF2-14 | Nhóm nợ, ngưỡng định danh, thuế điện tử… khớp văn bản gốc | đối chiếu TT 40/2024 (VBHN 76), 31/2024, 50/2024, 64/2024, 19/2021 trong `findings_LF2.md` | khớp; BNX L12, BNK L13 đã sửa theo nguyên văn | VALID | 2026-11-11 |
| LF2-15 | TT 77/2025/TT-NHNN: ngưỡng cá nhân $10$ và $20$ triệu giữ nguyên, hiệu lực 01/03/2026 | đọc văn bản hợp nhất 25/VBHN-NHNN | khớp nội dung BNK L13 sau sửa | PARTIAL (CITED: bản hợp nhất, chưa mở Công báo) | 2026-11-12 |
| LF2-16 | `audit/bnx/deps/` tái lập được | `sha256sum` 27 jar so với README | 27/27 khớp; README ghi lệnh dựng lại venv, Go module | VALID (jar/venv/vendor nằm trong `.gitignore`) | 2026-11-12 |
| LF2-17 | TTS Edge chặn khi nhiều luồng tạo câu mới | 4 luồng song song BNX → `NoAudioReceived`; sau ≥ 1 giờ 2 luồng chạy được | BNX L16 dựng 19 phút (94 lần thử lại); sau đó bài có cache chạy 4 luồng ổn | VALID (quy tắc vận hành) | 2026-11-12 |
| LF2-18 | 575 bài của 37 khoá có bài dựng lại giải mã trọn bằng ffmpeg, không lỗi | `pack.py check --decode --course <37 khoá> --tsv logs/check_decode_post.tsv` | `# 575 bài có video · có vấn đề 0 · chưa có video 0 · tổng 5219.4 phút · giải mã trọn 575` | VALID | 2026-11-13 |

## Điểm nghẽn hợp đồng
- CB-LF2-1 CLOSED (LF2-01, 02). CB-LF2-2 CLOSED một phần (LF2-14, 15). CB-LF2-6 CLOSED (LF2-04, 08). CB-LF2-7 CLOSED (LF2-06, 08). CB-LF2-8 CLOSED một phần (LF2-16).
- **OPEN**: CB-LF2-3 (tai người nghe; chỉ người dùng đóng được), CB-LF2-4 (sản phẩm Elasticsearch, Couchbase, RabbitMQ, Kubernetes, GitLab runner, AEM chỉ mô phỏng; không có trình biên dịch C), CB-LF2-5 (văn bản gốc TT 77/2025 và TT 46/2024/TT-BTC; QĐ 2345 sau TT 50/2024), hiệu quả học thật trên người học.

## Phụ thuộc giữa nút
LF2-01 → LF2-02 (đọc → sửa) → LF2-03 (dựng) → LF2-06, 05 (máy nghe) → LF2-07, 08 (cổng) → LF2-10, 11, 12 (trang học, bản sao, MASTER). LF2-04 → LF2-13 (CV) và LF2-12.
