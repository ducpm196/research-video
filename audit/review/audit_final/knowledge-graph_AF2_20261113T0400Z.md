# knowledge-graph_AF2_20261113T0400Z — đồ thị chứng cứ của đợt AF2

Môi trường: Windows 11; Git Bash 5.2; `.venv` Python 3.13; Python hệ thống 3.11.9; JDK 21.0.13; gcc 16.2.0; Docker `bnx-ora`, `bnx-mss`; ffmpeg; edge-tts (NamMinh). Giờ UTC từ `date -u`. OBSERVED = chạy trong phiên này; CITED = báo cáo tác tử hoặc nguồn ngoài (ghi rõ).

| ID | Khẳng định | Phương pháp | Quan sát | basis | validity |
|---|---|---|---|---|---|
| AF2-01 | Mốc đầu đợt tái lập LF2 | `final_gates.sh` | screen_code PASS 1089 FAIL 0; pack 680/0; verify bnx 493/493 (`logs/BASELINE_AF2.md`) | OBSERVED | VALID |
| AF2-02 | Lint chặn "mục tiêu không dạy" và thiếu Tự làm với bài `af2: true` | `tools/lv.py lint_af2` + ca đối chứng (dry-run JVA L04) | 49 bài PASS E51/E53 | OBSERVED | VALID |
| AF2-03 | Mọi lab chạy lời giải qua `cham.sh` ra đúng `mong_doi.txt`; bản cố tình sai bị chấm KHÁC | `lab_gate.py` | 49 PASS · 0 FAIL (`gates_af2.out`) | OBSERVED | VALID |
| AF2-04 | Dãy học không còn lời hẹn "Bài sau (bài N)" lệch | `check_next_refs.py` (trước: 93/551 lệch với xếp dãy cũ) | 551 lời hẹn, 0 lệch; 0 vi phạm tiên quyết; 701/701 bài có chỗ | OBSERVED | VALID |
| AF2-05 | Phép tính hiển thị đúng số đang hiện | `arith_scan.py` (bắt LLM L05 `12,9 + 34,4 = 47,2`, đã sửa) | 226 phép tính kiểm được, 0 FAIL | OBSERVED | VALID (phủ giới hạn: chỉ chữ/bảng thường, không công thức KaTeX) |
| AF2-06 | Văn bản pháp lý được dẫn có mục hiệu lực | `check_legal.py` + registry 20 văn bản | 78 lượt dẫn, 0 FAIL; 6 văn bản `CHUA_KIEM` | OBSERVED | VALID; nội dung Luật 108/2025 + NĐ 356/2025 CITED thứ cấp (expertis.vn, pwc/ey/luatvietnam, 2026-11-12, no revision given) |
| AF2-07 | FND (11 bài) chạy thật trên Git Bash, sổ mã sạch | `verify_fnd.py`; `screen_code check --course fnd` | 70/70 PASS; 186 khối PASS 267 FAIL 0 | OBSERVED (screen_code: CITED báo cáo tác tử, chạy lại toàn kho trong gates) | VALID |
| AF2-08 | JV2 (10 bài) chạy thật JDK 21 + JUnit jar | `verify_jv2.py`; screen_code | 85/85 PASS; 200 khối PASS 295 FAIL 0 | OBSERVED | VALID (jar JUnit sha256 trong `labs/ENV.md`, khớp Maven Central theo tác tử: CITED) |
| AF2-09 | JVA (13) và BNK (15) nâng AF2, mã chạy thật | `verify_jva` 143/143; `verify_bnk` 36/36; screen_code JVA 372 khối, BNK 90 khối | PASS, FAIL 0 | OBSERVED | VALID; BNK L06/L07/L10 là mô phỏng (ghi trên màn hình) |
| AF2-10 | 26 bài mẫu F đã sửa và dựng lại | `reports/fixf_A.md`, `fixf_B.md`; lint/render; dựng; ASR | 26 bài 0 FAIL; 7 phát hiện kiểm trên tệp thật bởi người điều phối ở AF1 | OBSERVED (sửa) + CITED (kiểm nguồn của tác tử: man7, Ioffe & Szegedy, He et al., thư Pathfinder) | VALID |
| AF2-11 | Mọi video khớp đặc tả, giải mã trọn BNX | `pack.py check` / `--course BNX --decode` | 701 bài 0 vấn đề, 6803,6 phút; BNX 24/24 giải mã trọn | OBSERVED | VALID (giải mã trọn 677 bài khác: CITED LF1/LS1/LF2, không chạy lại) |
| AF2-12 | ASR: 0 câu chưa xem xét ở mọi khoá đã dựng; câu ≤ 7 từ điểm < 0,7 đã viết lại | `asr_flags.py` từng khoá + `hand_all.py` | 0 chưa xem xét; 0 `⚠ NGẮN` sau lần dựng cuối | OBSERVED | VALID; lý do đều `NOT_VERIFIED bằng tai người` |
| AF2-13 | Trang học dùng được | Playwright (Edge) 42/42 phép thử chức năng, 0 lỗi JS; `pack.py page` | 701 bài, 5198 liên kết tệp, chết 0, 49 bài có Tự làm; tương phản ≥ 5,9:1 | CITED (tác tử, 42 phép thử) + OBSERVED (page, ảnh chụp ở `final_ui`, 0 lỗi console) | VALID |
| AF2-14 | Khung hình đọc được, tương phản phần mờ đạt AA | tính tỉ lệ tương phản 0,38 → 2,21; 0,66 → ≈ 4,8 | số học OBSERVED; người điều phối xem 5 khung FND/JV2/JVA | OBSERVED | VALID |
| AF2-15 | BNX L19 chập chờn lần chạy lạnh đầu | `screen_code check --course bnx` ×6 | lần 1 FAIL (CROSSSLOT), các lần sau PASS 360 | OBSERVED | VALID (nguyên nhân khởi động Redis cụm: INFERRED) |

## Phụ thuộc
AF2-02 → AF2-07, 08, 09 (cảnh Tự làm) → AF2-03 (lab) → AF2-12 (dựng + ASR) → AF2-11 → AF2-13 (trang). AF2-04 → AF2-13 (thứ tự trang). AF2-06 → AF2-10 (BNX L12).

## Contract bottleneck
Bảng đóng/mở ở `handover_AF2_*.md` §3. Mở: CB-LF2-3/CB-AF1-5 (tai người), CB-AF1-2 phần còn lại (6 văn bản `CHUA_KIEM`, chưa mở Công báo), CB-AF1-8 (sản phẩm mô phỏng), CB-AF2-1 (PYT), CB-AF2-2 (49/701 bài AF2, chưa đo lại bằng người đọc độc lập), CB-AF2-3 (BNX L19).
