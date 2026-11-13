# plan_AF3 — việc còn lại để đạt bản final "chỉ học qua video, từ con số 0 tới senior" (viết 2026-11-13 sau đợt AF2)

Đã làm ở AF2 (chi tiết: `handover_AF2_*.md`): cổng mới (E51/E53, lab_gate, arith_scan, check_next_refs, check_legal), khoá mới FND (11) + JV2 (10), nâng JVA (13) và BNK (15) lên chuẩn AF2 (cảnh Tự làm + lab chạy thật + thuật ngữ tại chỗ + cảnh quy mô), sửa 26 phát hiện của mẫu F, thiết kế lại `HOC_TAP.html`, xếp dãy học không còn lệch lời hẹn "Bài sau". **Chuẩn AF2 mới phủ 49/701 bài.** Phần còn lại là AF3.

## Thứ tự ưu tiên (lý do: người học đi theo `HOC_TAP.html` từ trên xuống)
| WP | Việc | Vì sao trước | Chuẩn nghiệm thu |
|---|---|---|---|
| **A1** | **Khoá PYT** — Python từ con số 0 (≈ 12 bài), đặt trước BNX trong dãy học | `sample_f` đo: Python xuất hiện ở 79 bài (BNX 18, PLC 9, SDP 9, ESY 8…) mà không khoá nào dạy; BNX L00–L01 dùng f-string, `re`, comprehension chỉ giảng một câu | như FND/JV2 (`BRIEF_AF2.md` + `BRIEF_FND.md` làm mẫu bộ sinh); lab `.py`; `verify_pyt` chạy thật; thêm `PYT` vào `pack.py STAGES` (chặng 1 hoặc đầu chặng 3), `BNX:L00 requires_ext PYT:Lxx` |
| **A2** | **Nâng BNX L00–L23 (24 bài)** lên AF2 (Tự làm, cảnh quy mô, thuật ngữ tại chỗ: `ed25519`, `-noenc`, socket, `Thread`…, bỏ giả định bash/Python) | BNX L00 là chỗ kẹt cứng đầu tiên khi tự làm (đo ở AF1); BNX L05 còn 3 SHOULD | `BRIEF_BNK.md` làm mẫu; Docker `bnx-ora/mss` cho lab Oracle/SQL Server; mỗi lab chạy qua `labs/cham.sh` |
| **A3** | INT (8) + ACB (9): ôn phỏng vấn → mỗi bài có bài tập mô phỏng câu hỏi (đáp án mẫu có số), không cần Docker | hoàn tất "đường nhanh" Chặng 1–4 | `interview_sync_video --check` 100% |
| **B1** | **Chặng 5** (DMS 21, CS112 30, CS115 46 = 97 bài): nâng AF2 — lab giấy-bút có số khác ví dụ + lab Python cho phần thuật toán/học máy (sau PYT) | nền toán/thuật toán của "senior CS" | lab `.py`/`.md`; `verify_*` hiện có giữ nguyên |
| **B2** | **Chặng 6–8** (CSA, OSY, NET, SWF, SDP, DBS, DVO, WEB, SEC, DSY, EVT, DEN, CLD, CLC, SAR ≈ 250 bài): AF2; các lab cần Docker/Linux ghi rõ; sản phẩm chỉ mô phỏng (ES, Couchbase, RabbitMQ, K8s, GitLab runner) phải nói rõ trên màn hình | độ sâu "senior hệ thống" | như trên |
| **B3** | **Chặng 9–11** (AI/ML: AIF, LLM, AGT, MLO, RLN, CVI, IRS, DAN, DSC; chuyên gia: TOC, PLC, PAR, HCI, SEP, CAS; mở rộng: RBM, ESY, ROB, GFX, BCH) ≈ 250 bài: AF2 + **khoá MLP** (Học máy thực hành ≈ 14 bài: scikit-learn, PyTorch, huấn luyện MLP/CNN nhỏ, tinh chỉnh, gọi API mô hình ngôn ngữ, đánh giá, tái lập) đặt sau CS115 L22–L23 | 16 khoá AI/dữ liệu 0 khối mã (đo `logs/stats.out`) | như trên |
| **C1** | **Bài dự án cuối mỗi chặng** (11 bài; đề + thang chấm + lời giải mẫu + "khi quy mô ×1000") | "thực nghiệm đi kèm", ghép kiến thức cả chặng | `lab_gate` + người đọc độc lập |
| **C2** | Cổng còn thiếu: **E52** (thuật ngữ tại chỗ: sổ `tools/registry/glossary.<KHOÁ>.yaml`, lint FAIL khi thuật ngữ dùng trước định nghĩa trong bài/ôn nền), **E55** (một thuật ngữ một cách viết liên khoá) | P1 vẫn là điểm yếu chính (mẫu F: 7/38 bài đạt) | ca thử trong `tests/test_lint.py` + đối chứng dương |
| **D** | Pháp lý: mở văn bản gốc (Công báo/vbpl.vn) cho Luật 108/2025/QH15, TT 77/2025, TT 46/2024/TT-BTC, NĐ 23/2025, NĐ 52/2024 (có thể đã thay bởi NĐ 320/2025), TT 14/2017, 48/2018, 49/2018; cập nhật `audit/legal/registry.yaml`; `check_legal.py --strict` 0 FAIL | 6 văn bản còn `CHUA_KIEM` | registry không còn `CHUA_KIEM` |
| **E** | Đo lại: mẫu G (hạt giống mới, 1 bài/khoá kể cả FND, JV2, PYT, MLP), 4 người đọc độc lập, **lưu báo cáo nguyên văn ra tệp NGAY khi nhận** (nhật ký tác vụ có thể rỗng); đường đi người mất gốc lần hai (FND → … → BNX L01); người dùng nghe thử | chốt "final" | ngưỡng: MUST 0; P1 = 2 ≥ 80%; P8 = 2 ≥ 90% |

Khối lượng: ≈ 650 bài chưa AF2 + ≈ 26 bài mới (PYT 12, MLP 14) + 11 bài dự án. Với nhịp AF2 (40 bài/phiên-dài với 4 tác tử, cộng ≈ 3 giờ dựng), ước 15–20 phiên. Nên làm theo chặng và **dựng, rà ASR, công bố HOC_TAP ngay khi xong từng chặng** để người học bắt đầu sớm (không đợi cả kho).

## Quy trình đã chạy tốt (dùng lại)
1. Tác tử soạn/nâng theo brief (`BRIEF_AF2.md` + brief khoá), ≤ 4 cùng lúc, mỗi khoá một tác tử; **viết `curriculum/<khoá>.yaml` SAU CÙNG**; tác tử không chạy build/tts/asr/audit_all/git.
2. Người điều phối: kiểm diff so với `snap/`, chạy `lab_gate`, `arith_scan`, `check_legal`, `check_next_refs`, `check_xref`; xem 3 khung PNG/bài.
3. Dựng: `bash audit/review/audit_final/rebuild_af2.sh a|b` (**chỉ 2 luồng**; 4 luồng bị Edge TTS chặn), hàng `rebuild.queue`; xong → `asr_flags.py` → câu ≤ 7 từ điểm < 0,7 (`⚠ NGẮN`) viết lại dài hơn rồi dựng lại → `asr_hand_gen/insert` + `asr_review_dms.py` (script `hand_all.py` trong scratchpad phiên AF2; chép vào `audit/review/audit_final/hand_all.py`) → `lv.py asr` làm mới báo cáo.
4. `pack.py preview` → `interview_sync_video.py` → `interview_gen_tables.py` → `pack.py check` (0 vấn đề) → `pack.py page` → `final_gates_af2.sh` (MỘT bản, bằng `run_in_background`, kiểm `Get-CimInstance Win32_Process`).

## Bẫy đã gặp ở AF2 (đừng lặp lại)
- `nohup … &` trong tool sinh bản chạy trùng (tranh `audit_all.tsv`, Docker/Redis); sửa nguồn bằng heredoc python/sed làm hỏng `\n`, `\b`, `\1` → luôn Edit/Write rồi `grep -c` ký tự 0x08/0x01.
- Lint E37 (bản đồ khoá) chỉ chạy khi `curriculum/<khoá>.yaml` tồn tại → bài viết trước khi có lộ trình có thể FAIL lúc dựng (đã gặp FND L10, JV2 L09): chạy lại `lv.py lint` sau khi có lộ trình.
- `python3` trên Windows là lối tắt Microsoft Store (`cham.sh` nay dò `--version`).
- Tác tử chờ tiến trình nền báo lặp mãi → `TaskStop` khi đã nhận báo cáo.
- `gen_curriculum.py` của JVA/BNK ghi đè `curriculum/*.yaml`: `requires_ext` liên khoá phải nằm trong bộ sinh (đã vá cho FND:L10, JV2:L09).
- `screen_code.py` toàn kho > 20 phút khi máy tải; BNX L19 (Redis cụm) chập chờn nếu chạy cùng lúc với tiến trình khác dùng Docker.
