# Bàn giao cuối AF5 — Đủ 53 khoá / 806 bài học (2026-11-27)

- **Kế hoạch đối chiếu:** [plan_AF5_20261123T0110Z.md](plan_AF5_20261123T0110Z.md) (`WP-0..WP-7`)
- **Trạng thái tổng thể:**
  - **100% đạt chuẩn máy, kiểm đọc độc lập và thực thi (`DONE`)**: 53/53 khoá (`806/806` bài học + `806/806` video MP4 + `806/806` lab + `61/61` verifier + `26/26` cổng AF5 + `WP-7` 66/66 mẫu phân tầng `0 MUST` + web học tập `HOC_TAP.html`).
  - **Còn mở theo ràng buộc quy trình (`PARTIAL` chỉ cho thao tác con người):**
    1. **`BN-08` (Nghe tai người):** Âm thanh của 806 video đã được kiểm tự động toàn bộ bằng ASR (`tools/lv_fast.py asr` + `asr_flags_all = 0 FAIL`) và tốc độ đọc (`tts_speed_scan 0.22 = 0 < 0.22`), nhưng **tai người chưa nghe thử** (`NOT_VERIFIED bằng tai người` trong `asr_reviewed` & [quality.yaml](../learn_start/quality.yaml)). Bạn có thể mở [NGHE_THU.html](../../../NGHE_THU.html) để nghe kiểm mẫu 80 câu qua 5 chặng.
    2. **`BN-15` (Commit Git):** Theo quy tắc không tự ý `git commit`, toàn bộ thay đổi AF5 (bao gồm `git rm` 26 tệp rác ở gốc) đang ở trạng thái working tree / index để bạn kiểm tra và `git commit` một lần.

---

## 1. Bằng chứng 26/26 cổng kiểm định (`final_gates_af5.sh day_du`)

Nhật ký đầy đủ: [final_gates_day_du_20261127.log](logs/af5_exec/final_gates_day_du_20261127.log) — thoát mã **`0` (`0 cổng FAIL`)**:

| Cổng | Nội dung kiểm tra | Kết quả đo thật (2026-11-27) |
|---|---|---|
| `[1]` `check_xref` | Tham chiếu chéo giữa các khoá | `0` lỗi tham chiếu (cho phép có lý do: `31`) |
| `[2]` `check_meta` | Siêu dữ liệu bài học | `0` vấn đề |
| `[3]` `check_course_refs` | Tham chiếu trong khoá | `0` vấn đề |
| `[4]` `check_next_refs` | Lời hẹn bài kế tiếp | `593` lời hẹn, `0` lệch dãy học |
| `[5]` `check_legal` | Trích dẫn văn bản pháp lý | `114` lượt dẫn, `22` văn bản trong sổ (`0 CHUA_KIEM`), `0 FAIL` |
| `[6]` `arith_scan` | Kiểm tra số học trong bài | `1498` phép tính kiểm được, `0 FAIL` |
| `[7]` `check_curricula_graph` | Đồ thị tiên quyết 53 lộ trình | `53` lộ trình, `806` bài, `2688` cạnh (`951 lab.requires`), `0` hỏng, `0` chu trình |
| `[8]` `verify_plan_curricula` | Bộ xác minh toán/mã giáo án | `641 PASS · 0 FAIL` |
| `[9]` `lv.py curriculum` | Kiểm toàn bộ giáo án | `0 FAIL` |
| `[10]` `test_lint + test_e52` | Bộ kiểm quy tắc lint & E52/E55 | `0 FAIL` |
| `[11]` `tests mới` | `check_xref`, `test_frozen` (`56/56`), `test_content_gates` (`32` bài mẫu), `test_cham.sh` (`16/16`) | `0 FAIL` |
| `[12]` `scan_ctrl` | Ký tự điều khiển | `90` tab hợp lệ, `0` lỗi |
| `[13]` `sync_tpl_from_lesson --all` | Đồng bộ mẫu `.tpl.yaml` ↔ YAML bài | `tổng: 0 mẫu lệch bài` |
| `[14]` `interview_sync_video --check` | Đồng bộ sổ phỏng vấn & video | `99` cặp, `99` khớp, `0` lệch |
| `[15]` `af2_cover S01..S11` | Độ phủ `af2` + `practice` + `lab` cả 11 chặng | `100.0%` trên đủ 11 chặng (`0` chặng chưa phủ) |
| `[16]` `find_stale_all` | Đối chiếu `spec_sha256` + `tts_sha256` | `TOTAL_STALE=0` |
| `[17]` `pack check --decode` | Giải mã từng khung hình bằng `ffmpeg -xerror` | `806 bài có video · có vấn đề 0 · chưa có video 0 · tổng 10474.9 phút · giải mã trọn 806` |
| `[18]` `tts_speed_scan 0.22` | Tốc độ đọc tối thiểu từng câu | `86102` câu, `0` câu `< 0.22 s/từ` |
| `[19]` `asr_flags` (53 khoá) | Cờ ASR chưa xem xét toàn kho | `asr_flags_all: 0 FAIL` (`0` khoá còn câu chưa xem xét) |
| `[20]` `content_gates --ratchet` | Cổng nội dung + khoá đã chốt | `806` bài, `0 FAIL` nền, `0` hồi quy mới, `0` lỗi khoá `ĐÃ CHỐT` |
| `[21]` `lab_gate` | Chấm thật mọi lab + ca ẩn + chống hardcode | `806 PASS · 0 FAIL` (`806` lab được bài tham chiếu) |
| `[22]` `verifiers_all` (`verify_*.py`) | Bộ kiểm độc lập từng khoá | `61/61 PASS, 0 FAIL` |
| `[23]` `screen_code check` | Kiểm chạy thật các khối mã trên màn hình | `3700` khối — `PASS 4715 · FAIL 0 · STALE 0 · MISSING 0 · ORPHAN 0 · WARN 0` (`216 NOT_VERIFIED` máy có ghi nhận hợp lệ) |
| `[24]` `pedagogy_scan` | Quét chỉ số sư phạm toàn kho | `PASS` (đã cập nhật `audit/review/pedagogy_scan.tsv`) |
| `[25]` `audit_all` | Rà soát lint & dựng 53 khoá | `806` bài, `806` đã dựng (`0` FAIL; còn ghi chú `WARN` nhẹ ở `288` bài không chặn cổng) |
| `[26]` `verify_spb` | Dự án Spring Boot / Testcontainers (`SPB L00..L12`) | `TỔNG SPB: 14 PASS · 0 FAIL` (kể cả `SPB:L10` Docker/Postgres/Redis/Kafka) |
| Bổ sung | `video_gap_scan.py` (quét mất slide / lệch hình) | `kiểm 806 video, hỏng 0` |

---

## 2. Kiểm đọc 100%, `WP-7`, Gói học & Các sửa chữa trọng tâm

- **Kiểm đọc `read_af5` (`806/806`):** `READ_AF5_ALL: ok=806 missing=0 stale_sha=0 must=0`, `BUILD_NEEDED=0 ALREADY_FRESH=806` (mọi báo cáo khớp `sha16` YAML cuối cùng).
- **Kiểm mẫu đối chứng cuối `WP-7`:** 66 bài phân tầng (`6` bài/chặng cho đủ `S01..S11`, hạt giống `20261127`) tại [REPORT.md](../sample_final/REPORT.md) (và 3 phần [S01..S04](../sample_final/part_s01_s04.md), [S05..S08](../sample_final/part_s05_s08.md), [S09..S11](../sample_final/part_s09_s11.md)) đạt **`66 / 66 = 0 MUST`**, `66/66` khớp `sha16` + `lv.py lint` 0 FAIL + `0 boiler_deny`.
- **Các sửa chữa lớn thực hiện trong chặng chốt:**
  - Sửa `curriculum/dbs.yaml` (`lab.requires: [PYT:L04, FND:L08]`, `L04`/`L07` tiên quyết `[L02, L03]`), gọn lại gợi ý `labs/DBS/{L00,L06,L07,L08,L09}/de.md` không lộ nguyên câu SQL đáp án, sửa `lessons/dbs/L06_thiet_ke_er.yaml` (`example.0` & `focus`).
  - Sửa `lessons/toc/L01_dfa.yaml` (`Bước 6 → Bước 5`, `covers` obj 2 trỏ `example` hợp lệ `E51`) và `lessons/toc/L05_toi_thieu_hoa.yaml` (công thức $n(n-1)/2$, bậc $n^2$).
  - Làm sạch toàn bộ câu đệm lệch màn hình / sai kiến thức (`content-box` ở `WEB/L02 prereq.0`, `macrotask` ở `WEB/L03` + `de.md`, `WEB/L00..L03`, `WEB/L06`, `WEB/L08` `prereq`/`pitfalls`/`quiz`), gỡ lộ đáp án ở `labs/WEB/L06/de.md`, và bổ sung khung đọc `stdin` Node theo `plan_AF5` §5.2 vào `labs/WEB/{L06,L08}/de.md`.
  - Cập nhật `audit/review/screen_code/{DSC,MLO,NET,WEB}.yaml` (đồng bộ output + gọi hàm `taiTuanTu()`/`taiDongThoi()` trong `post` của `WEB/L04`).
  - Áp dụng `asr_reviewed` (+208 mục) và làm mới báo cáo ASR tuần tự bằng `tools/lv_fast.py asr` cho 344 bài (`344/344 OK`), đồng bộ 44 mẫu `.tpl.yaml` kể cả `audit/rbm/src/L01_quay_3d_euler.tpl.yaml`.
  - Dựng lại toàn bộ các bài thay đổi bằng `tools/lv_fast.py` (NVENC 10fps + libyaml + ASR song song).
- **Gói học & Nhãn chất lượng:**
  - [quality.yaml](../learn_start/quality.yaml): **`53/53` khoá đạt nhãn `ĐÃ CHỐT`** (cập nhật `2026-11-27`).
  - [HOC_TAP.html](../../../HOC_TAP.html) (`6.26 MB`, `806/806` bài có video, `8227` liên kết tệp, `2938` neo, `0` chết), [HOC_TAP.md](../../../HOC_TAP.md) (`807` liên kết, `0` chết), `out/<C>/<Lxx>/xem.html` (`806` trang, `7417` liên kết, `0` chết), [NGHE_THU.html](../../../NGHE_THU.html) (`5` chặng, `80` câu mẫu, `0` chết).

---

## 3. Dọn dẹp repo & Tổ chức hậu AF5

1. **Đã xử lý ở thư mục gốc & `out/`:**
   - Đã xoá các tệp untracked rác chiếm dung lượng/gây nhiễu: `cuahang.jar` (`42.617.720.792` byte / `39,69 GiB` — bản chụp dư `out/`), `Tong.class` (`854 B`), `out.bin` (`64 B`), và thư mục biên dịch dư `out/shop/`. Xác nhận `curriculum=53 / lessons=53 / out=53`, `806/806` bài khớp 1-1 không dư/thiếu.
   - Đã chạy `git rm` cho toàn bộ **`26` tệp rác đã commit ở gốc** (`Tong.java`, `bao_cao.json`, `bieu_do.png`, `chao.sh`, `doc.py`, `don.json`, `giao_dich.csv`, `lenh.txt`, `main.go`, `may_chu.py`, `so_cai.csv`, `tep.txt`, `test_tong.py`, `tinh.py`, `tong.py`, `cua_hang/*` [4], `vp/*` [4], `src/shop/*` [2], `tien_ich/chao_ban`) và xoá thư mục rỗng tương ứng. Đang giữ chưa `git commit` theo `BN-15`.
2. **Thư mục `audit/` (khuyến nghị giữ nguyên trong nhánh AF5, tách ở v7):**
   - `audit/` hiện có `4.713` tệp tracked (`1.505` trong `review/`, `53` thư mục khoá, `118` tệp trực tiếp gồm `layout_*.tsv`, `REVIEW_L*.md`, `_frozen.py`, ...). Nhiều đường dẫn trong đó được hardcode trong `final_gates_af5.sh`, `tests/test_frozen.py`, `tools/lv.py` (`audit/layout_scan.py`), `curriculum/*.yaml` và `lessons/*.yaml`.
   - Để tránh làm gãy 26 cổng AF5 và `56/56 test_frozen`, `audit/` được giữ nguyên cấu trúc trong bản bàn giao AF5; sau khi bạn `git commit` và gắn tag chốt AF5, có thể tách sạch sang bố cục `gates/`, `verifiers/`, `reports/`, `archive/audit_logs/` trong một PR tái cấu trúc riêng.

---

## 4. Việc cần làm tiếp (dành cho người vận hành)

1. Mở [NGHE_THU.html](../../../NGHE_THU.html) nghe rà 80 câu mẫu qua 5 chặng để xác nhận tai người (`BN-08`).
2. Kiểm tra `git status` và commit toàn bộ trạng thái đã chốt AF5 (bao gồm 26 tệp rác đã `git rm` và diff lưu tại [wp_final_diff_stat.txt](logs/af5_exec/wp_final_diff_stat.txt)).
