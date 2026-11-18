# knowledge-graph_AF3_20261113T1240Z — đồ thị chứng cứ của lượt rà và lập kế hoạch AF3-PLAN

Phiên chỉ rà và lập kế hoạch: không sửa bài, không dựng video. Tệp đổi trong kho: `plan_AF3_20261113T1240Z.md`, tệp này, `handover_AF3_20261113T1240Z.md`, một dòng đầu `plan_AF3_next.md`, `STATE.md`, đầu `HANDOVER.md`.
Môi trường (OBSERVED 2026-11-13T12:24Z): Windows 11; Git Bash; JDK 21.0.13; Python hệ thống 3.11.9, `.venv` 3.13.5 (không có scikit-learn/torch); gcc 16.2.0; Node 25.8.0; ffmpeg 8.0.1; git 2.53.0; Docker: `bnx-ora`, `bnx-mss` Up, ảnh redis 8, kafka 3.9.0, oracle-free 23, mssql 2022; WSL Ubuntu 22.04; GPU RTX 2060 6 GB. Commit: `eb64a29` "Update v3.1".
Giờ UTC lấy từ `date -u`. Nhật ký cổng của phiên: scratchpad `gates_af3_pre.out` (chép số vào bảng dưới; tệp scratchpad không tồn tại qua phiên).

| ID | Khẳng định | Phương pháp (lệnh đã chạy) | Quan sát | basis | validity |
|---|---|---|---|---|---|
| AF3-01 | Kho có 701 đặc tả ở 45 khoá, 701 mp4, 45 giáo án; chuẩn AF2 (`af2: true` + cảnh `practice` + thư mục lab) phủ 49 bài, chỉ ở BNK 15, FND 11, JV2 10, JVA 13 | script đếm `lessons/*/*.yaml`, `out/<KHOÁ>/*/*.mp4`, `labs/<KHOÁ>/*`, `curriculum/*.yaml` (12:24Z) | TOTAL n 701 · af2 49 · practice 49 · labs 49 · mp4 701 · 45 khoá; bài có khối mã 185 (phép đếm thô theo chuỗi `class="code`, `<pre`) | OBSERVED | VALID |
| AF3-02 | Cổng nhẹ chạy lại trên trạng thái hiện tại | xem mục "Cổng chạy lại" bên dưới | xem bảng | OBSERVED | xem bảng |
| AF3-03 | Ổ D còn 4,4 GB / 444 GB (100%); ổ C còn 51 GB; AF2 đã được commit `eb64a29` (407 tệp), cây làm việc chỉ còn tệp của phiên này | `df -h /d`, `df -h /c`, `git log -1 --format='%h %cI %s'`, `git status --short` | `D: 444G 439G 4.4G 100%`; `C: 476G 426G 51G 90%`; `eb64a29 2026-11-13T19:24:04+07:00 Update v3.1`; 2 dòng trạng thái (plan mới, plan_AF3_next) | OBSERVED | VALID |
| AF3-04 | Ba tệp sinh tự động đã lệch với kho | `grep -c "FND\|JV2\|BNX" curriculum/TRACKS.md`; đầu `curriculum/STATUS.md`; `grep -c "" audit/review/pedagogy_scan.tsv`; `ls -la` | TRACKS.md: 0 lần (sinh 05/11); STATUS.md: "700 hoàn thiện", FND L03 WARN, sinh từ `audit_all.tsv` 03:39Z (trước lần sửa cuối của AF2); pedagogy_scan.tsv: 657 dòng (656 bài, ngày 10/11) | OBSERVED | VALID |
| AF3-05 | Không khoá nào dạy con trỏ/mô hình bộ nhớ bằng mã | `grep -c "con trỏ" lessons/*/*.yaml` gộp theo khoá | số bài có từ này: hci 6 (con trỏ chuột), plc 3, cs112 3, int 3, evt 3, osy 2, web 2, còn lại ≤ 1; không có khoá C | OBSERVED | VALID (suy ra "thiếu khoá": INFERRED từ danh sách giáo án) |
| AF3-06 | Toán nền được ôn tại chỗ, chưa thấy cần khoá toán phổ thông riêng | đọc tiêu đề + cảnh `prereq` DMS L00, tiêu đề/ mục tiêu CS112 L00 | DMS L00 ôn chẵn lẻ, luỹ thừa 2, liệt kê; CS112 L00 dạy làm tròn, lôgarit cơ số 2, tổng Sigma | OBSERVED (2 bài) | NOT_VERIFIED cho cả chặng 5 → cần lượt đọc đường đi (plan mục 7 WP5) |
| AF3-07 | Khung hình bài cũ và bài AF2 đọc được, không tràn/đè | mở `out/AIF/L03/frames/00039.png`, `out/FND/L03/frames/00110.png` | hai khung rõ, phụ đề khớp nội dung; AIF L03 có 9 cảnh không có `practice`, FND L03 có 12 cảnh gồm `practice`, `concept`, `formula` | OBSERVED (2 khung) | VALID cho 2 khung; không suy rộng |
| AF3-08 | `out/_tpl_backup` và `out/_probe` còn được dùng; `_stale_renumber_*`, `DEMO` chỉ còn trong ghi chú lịch sử | `grep -rln "_stale_renumber\|_tpl_backup\|out/DEMO\|out/_probe" tools audit/*.py audit/review/*.py tests .claude` | `sync_tpl_from_lesson.py` ghi vào `_tpl_backup`; `lexicon_vi.yaml` dẫn `out/_probe`; `production.md` dòng 106 nhắc chuyện đánh số lại | OBSERVED | VALID |
| AF3-09 | Kho chiếm ≈ 41 GB trên ổ D; phần còn lại của 439 GB nằm ngoài dự án | `du -sh out lessons audit labs archive resources interview state skills examples`; `du -sh .venv`; `ls /d/` | out 39G · lessons 25M · audit 578M · labs 372K · archive 224K · resources 6.4M · interview 418M · .venv 626M; ổ D còn có AI_Factory, Bot, Dify, VPS, TTNT, SV, CS115… (chưa đo, ngoài phạm vi) | OBSERVED | VALID; dung lượng riêng `_stale_renumber_*`, `DEMO`, `_cache` chưa đo: NOT_VERIFIED |
| AF3-10 | Số liệu AF2 (verify fnd 70/70, jv2 85/85, jva 143/143, bnk 36/36, bnx 494/494, screen_code 1419 khối, audit_all 701, ASR 0 chưa xem xét) | đọc `logs/gates_af2.out` | như bàn giao AF2 | CITED (2026-11-13T03:52Z) | VALID lúc đó; chưa chạy lại phiên này (cổng nặng, > 20 phút, tranh Docker) |
| AF3-11 | Số đo mẫu F (MUST 3/38; P1 = 2 ở 7/38; P8 = 2 ở 2/38; P9 = 2 ở 18/38) | đọc `audit/review/sample_f/REPORT.md` | như báo cáo | CITED (2026-11-12T18:10Z, commit `df811558`) | STALE với 26 bài đã sửa ở AF2; vẫn là số đo gần nhất của ≈ 650 bài chưa nâng |
| AF3-12 | Docker còn 20,49 GB build cache thu hồi được | `docker system df` | Build Cache 501 mục, 20.49GB reclaimable | OBSERVED | VALID |
| AF3-13 | Ổ D đã được mở rộng, không còn chặn việc dựng | `df -h /d /c` (13:11Z) | `D: 932G 417G 515G 45%`; `C: 476G 384G 93G 81%` | OBSERVED | VALID → AF3-03 phần "ổ D còn 4,4 GB" nay STALE |
| AF3-14 | JD mới thêm phần VPBank; 13 nhóm chủ đề chưa có bài | `git diff df81155 eb64a29 -- resources/job/JD.md` (+124 dòng); `grep -rlE "<từ khoá>" lessons --include=*.yaml` đếm số bài | 0 bài: JPA, Hibernate, Spring Data, ELK/Logstash/Kibana, Prometheus, Grafana, SOAP, SFTP, Jenkins, Gradle, GitOps, ArgoCD, Vault, JSP, JBoss, "tài liệu thiết kế"; ít: Maven 1, OLA 1, CQRS 2, Event Sourcing 2, MongoDB 2, Spring Security 2, Spring Cloud 2, Tomcat 2, AOP 2, Circuit Breaker 3, Servlet 3, CIC 3; có: Kafka 19, Redis 14, cân bằng tải 14, Kubernetes 10, Docker 9 | OBSERVED | VALID (đếm theo từ khoá; "có từ khoá" không chứng minh "dạy đủ") |
| AF3-15 | Sau khi làm tươi: mọi bài hoàn thiện theo định nghĩa của STATUS; video khớp đặc tả | `audit_all.py` (không tham số) → `status_report.py` → `pedagogy_scan.py` → `pack.py check`, 13:13–14:06Z; rồi `tracks.py` 14:06Z | `audit_all: 701 bài, 701 đã dựng, 0 bài có vấn đề`; `status_report: 701/701 bài hoàn thiện, 6804 phút`; `pedagogy_scan.tsv` 701 dòng, mức E39 "ĐỦ" 701/701; `pack.py check: 701 bài có video · có vấn đề 0 · tổng 6803.6 phút`; `tracks.py` lần đầu AssertionError (`prefer` thiếu ACB, BNK, BNX, FND, INT, JV2, JVA) → thêm 7 mã vào `prefer` của `tracks.yaml` → chạy lại ghi `TRACKS.md` (13 nghề, ví dụ cs-core 169 bài) | OBSERVED | VALID. Lưu ý: E39 "ĐỦ" đo cấu trúc bài, không đo thuật ngữ tại chỗ hay thực hành (mẫu E đã ghi) |
| AF3-16 | Dọn dẹp không làm hỏng trang học và video | xoá `out/_stale_renumber_2026-10-24`, `_2026-10-27`, `out/DEMO`, 67 nhật ký cũ ở `audit/review/`, 28 `__pycache__`, `.pytest_cache`; `git mv` 20 script → `archive/one_off_generators/`; `git rm resources/job/anh-cv.jpg` (sau `cmp` = trùng `avatar.jpg`); rút `HANDOVER.md`; sau đó chạy `audit_all` + `pack.py check` (AF3-15) | `ls out` chỉ còn `_cache`, `_probe`, `_tpl_backup` + 45 khoá; `audit_all` 0 vấn đề; `pack.py check` 701/0; `HANDOVER.md` 45 dòng, 292 dòng lịch sử ở `archive/handovers/HANDOVER_den_2026-11-11.md` | OBSERVED | VALID |

## Cổng chạy lại (AF3-02)

Lệnh: `.venv/Scripts/python -B <cổng>` lần lượt, bắt đầu 2026-11-13T12:27:03Z, đầu ra ở scratchpad `gates_af3_pre.out`.

| Cổng | Dòng tổng | Kết quả |
|---|---|---|
| `check_xref.py` | `0 lượt tham chiếu sang khoá khác ở 0 tệp` | PASS |
| `check_meta.py` | `0 vấn đề` | PASS |
| `check_course_refs.py` | `0 vấn đề` | PASS |
| `check_next_refs.py` | `551 lời hẹn, 0 lệch dãy học` | PASS |
| `check_legal.py` | `78 lượt dẫn, 20 văn bản trong sổ (6 CHUA_KIEM: 46/2024/TT-BTC, 23/2025/NĐ-CP, 52/2024/NĐ-CP, 14/2017, 48/2018, 49/2018/TT-NHNN), 0 FAIL` | PASS (chế độ thường; `--strict` chưa chạy) |
| `arith_scan.py` | `226 phép tính kiểm được, 0 FAIL` | PASS |
| `check_curricula_graph.py` | `45 lộ trình, 701 bài, 1428 cạnh tiên quyết; tham chiếu hỏng: 0; chu trình: 0; VER không PASS: 0` | PASS |
| `verify_plan_curricula.py` | `TỔNG: 570 PASS · 0 FAIL` | PASS |
| `tests/test_lint.py` | `tests: 0 FAIL` (checked_at=2026-11-13T12:44:21Z) | PASS |
| `lab_gate.py` | `49 PASS · 0 FAIL (49 lab được bài tham chiếu)` | PASS |
| `pack.py check` | `701 bài có video · có vấn đề 0 · chưa có video 0 · tổng 6803.6 phút` (xong 12:52:08Z; không giải mã) | PASS |

## Phụ thuộc
AF3-01 → kết luận "49/701" của plan mục 1. AF3-03 → CB-AF3-1 (ổ đĩa), CB-AF3-2 (mốc). AF3-04 → WP0 bước 7. AF3-05, AF3-06 → mục 5 (khoá mới). AF3-08 → D-AF3-2. AF3-10, AF3-11 (CITED) → chỉ dùng để xếp ưu tiên, không dùng để tuyên bố hoàn thành.

## Contract bottleneck
Bảng đủ 7 trường ở `plan_AF3_20261113T1240Z.md` mục 6 (CB-AF3-1…12). Đã đóng trong phiên: CB-AF3-1 ổ đĩa (AF3-13), CB-AF3-2 phần mốc đầu (AF3-03). Mở mới ở bản sửa 2: CB-AF3-13 (JD VPBank, AF3-14). Còn lại OPEN.
