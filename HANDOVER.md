# Bàn giao khoá học video — AF6: rà soát sau AF5, kho `PARTIAL` (2026-11-27T16:08Z)

> **Đọc trước tiên:** [handover_AF6_20261127T1608Z.md](audit/review/audit_final/handover_AF6_20261127T1608Z.md) → [plan_AF6_20261127T1608Z.md](audit/review/audit_final/plan_AF6_20261127T1608Z.md) → [knowledge-graph_AF6_20261127T1608Z.md](audit/review/audit_final/knowledge-graph_AF6_20261127T1608Z.md).

Lượt AF6 chỉ rà soát và lập kế hoạch (không sửa bài/lab/video/cổng, không commit), mốc git `a3039c1f`.

- **Tuyên bố "53/53 khoá ĐÃ CHỐT, 806/806 bài 0 lỗi bắt buộc sửa" ở phần dưới KHÔNG đứng được.** Bộ cổng máy đạt thật (cổng nhanh chạy lại: 0 trượt), nhưng Mẫu K (32 bài, 4 người đọc mới, có chạy mã và chấm lab) ra 48 lỗi bắt buộc sửa ở 26/32 bài; hồ sơ `read_af5` ghi 0 cho cả 32 bài.
- **Học ngay được:** 196 bài soạn tay của Chặng 1–5 (`FND`, `JVA`, `JV2`, `PYT`, `BNK`, `BNX`, `INT`, `ACB`, `DMS`, `CS112`, `CS115 L00–L21`, `L44–L46`).
- **Xem phần giảng được, bỏ phần Tự làm:** 536 bài lớp C (Chặng 6–11); coi chừng câu cuối mỗi đoạn lời (7 934 câu được nối thêm ở 614 bài, có câu sai).
- **Chưa nên học:** `CPR`, `LNX`, `MLP`, `PRJ` (45 bài) và `SPB`, `BEP`, `AIP` (29 bài).
- **Nguyên nhân gốc:** sàn độ dài tạo câu độn; cảnh Tự làm thay khuôn cũ bằng khuôn mới (378 bài); 443/806 lab là bài tính công thức; người đọc của đợt thực thi chấm nhẹ; 5 359 cờ phát âm được duyệt tự động; nhãn chất lượng dùng chung một câu chứng cứ.
- **Kế hoạch AF6:** gỡ nhãn `ĐÃ CHỐT`, nhãn ba trục theo bài; mọi khác biệt so với mốc `5d7f329` phải có phán quyết giữ/xoá/khôi phục; thực hành hai tầng tách khỏi video (luyện nhanh + lab nghề dùng công cụ thật); web lộ trình tương tác có bản đồ, 5 bước mỗi bài, phần thưởng theo bằng chứng; đọc độc lập có mục vàng cài mù và phân xử; sửa theo đúng thứ tự người học đi. Kế hoạch đã qua một vòng phản biện (22 phát hiện, đã sửa); bản sửa chưa được phản biện lần hai.
- **Cần người dùng:** quyền commit ở phiên thực thi; xem ma trận năng lực (mục 8 kế hoạch); tiếp tục nghe thử (tệp `nghe_thu_ket_qua.json` là của người dùng, phiên thực thi chỉ đọc).

---

# (Bản trước, 2026-11-27 — tuyên bố "100%" đã bị lượt AF6 bác; giữ để đối chiếu) Bàn giao khoá học video — Hoàn thiện AF5 (`806 / 806` bài · `53 / 53` khoá)

> **Cập nhật 2026-11-27:** Hoàn tất 100% các công việc kỹ thuật và kiểm định của kế hoạch AF5 (`WP-0..WP-7`). Mở [HOC_TAP.html](HOC_TAP.html) để bắt đầu học ngay. Xem báo cáo chi tiết tại [handover_AF5_final_20261127.md](audit/review/audit_final/handover_AF5_final_20261127.md).

## Kết quả đã xác nhận (2026-11-27)

- **Phạm vi sản xuất & khớp 1-1:** `53/53` khoá, `806/806` bài giảng YAML, `806/806` video MP4 tươi (`BUILD_NEEDED=0`, `TOTAL_STALE=0`, tổng `10474.9` phút), `0` bài dư / `0` bài thiếu (`video_gap_scan.py`: `kiểm 806 video, hỏng 0`).
- **Bộ 26 cổng kiểm định AF5 ([final_gates_af5.sh](audit/review/audit_final/final_gates_af5.sh) `day_du`):** **`26 / 26 PASS · 0 cổng FAIL`** ([nhật ký](audit/review/audit_final/logs/af5_exec/final_gates_day_du_20261127.log)):
  - `check_curricula_graph`: `53` lộ trình, `806` bài, `2688` cạnh tiên quyết, `0` tham chiếu hỏng, `0` chu trình.
  - `verify_plan_curricula`: `641 PASS · 0 FAIL`; `arith_scan`: `1498` phép tính / `0 FAIL`; `check_legal`: `114` dẫn / `0 FAIL`; `verifiers_all`: `61/61 PASS`; `verify_spb`: `14/14 PASS` (gồm `SPB:L10` Docker Testcontainers).
  - `lab_gate`: **`806 PASS · 0 FAIL`** (`806` lab được bài tham chiếu, kèm ca ẩn và chống in cứng).
  - `screen_code check`: **`3700` khối — `PASS 4715 · FAIL 0 · STALE 0 · MISSING 0 · ORPHAN 0 · WARN 0`**.
  - `pack check --decode`: giải mã trọn `806/806` MP4 (`có vấn đề 0`).
  - `asr_flags_all`: **`0` câu chưa xem xét trên toàn `53/53` khoá**; `tts_speed_scan 0.22`: `86102` câu, `0 < 0.22 s/từ`.
  - `sync_tpl_from_lesson --all`: **`tổng: 0 mẫu lệch bài`**; `interview_sync_video`: `99/99` khớp.
- **Kiểm đọc `read_af5` & mẫu đối chứng `WP-7`:**
  - `READ_AF5_ALL`: **`ok=806 · missing=0 · stale_sha=0 · must=0`**.
  - `WP-7` mẫu phân tầng `S01..S11` (`66` bài, hạt giống `20261127`): **`66/66 = 0 MUST`** ([REPORT.md](audit/review/sample_final/REPORT.md)).
- **Gói học & chất lượng:**
  - [quality.yaml](audit/review/learn_start/quality.yaml): **`53/53` khoá `ĐÃ CHỐT`**.
  - [HOC_TAP.html](HOC_TAP.html) (`6.26 MB`, `0` liên kết chết), [HOC_TAP.md](HOC_TAP.md) (`0` liên kết chết), [NGHE_THU.html](NGHE_THU.html) (`5` chặng, `80` câu mẫu, `0` chết).
- **Dọn dẹp chỗ lộn xộn tại gốc:**
  - Đã xoá `cuahang.jar` (`39,69 GiB`), `Tong.class`, `out.bin` (untracked) và `out/shop/` dư.
  - Đã `git rm` `26` tệp rác đã commit tại gốc (`Tong.java`, `tinh.py`, `cua_hang/`, `vp/`, `src/shop/`, `tien_ich/chao_ban`, ...).
  - Giữ nguyên cấu trúc `audit/` (`4.713` tệp tracked) trong bản chốt AF5 để tránh gãy cổng và `test_frozen` (`56/56`).

## Lưu ý mở còn lại cho người vận hành

1. **`BN-08` (Nghe kiểm bằng tai người):** Toàn bộ âm thanh đã qua kiểm tra máy (ASR + tốc độ đọc), nhưng chưa qua tai người (`NOT_VERIFIED bằng tai người`). Nghe mẫu qua [NGHE_THU.html](NGHE_THU.html).
2. **`BN-15` (Commit Git):** Theo quy tắc bàn giao, chưa chạy `git commit`. Kiểm tra `git status` rồi commit một lần toàn bộ thành quả AF5 + `26` tệp rác đã `git rm`.
