# Báo cáo khoá FND · Nền thực hành (11 bài L00–L10) — 2026-11-13

## Kết quả cổng (đo thật, cuối phiên)
| cổng | kết quả |
|---|---|
| `audit/fnd/verify_fnd.py` (chạy THẬT Git Bash, mọi phiên lệnh trong thư mục tạm) | **70/70 PASS** (L00–L10) |
| `tools/lv.py lint lessons/fnd/Lxx_*.yaml` | 11/11 bài **0 FAIL, 0 WARN** |
| `tools/lv.py render` | 11/11 bài **0 vấn đề** (tổng 1 438 khung); đã mở xem bằng mắt ≥ 2–3 khung mỗi bài (hình cơ chế, khối lệnh, cảnh Tự làm) |
| `audit/review/lab_gate.py FND` | **11 PASS · 0 FAIL** (L00–L10) — xem lưu ý PATH bên dưới |
| `tools/lv.py curriculum curriculum/fnd.yaml` | 11 bài, 11 đã có đặc tả, 0 lỗi |
| `audit/check_curricula_graph.py` | 44 lộ trình, 0 tham chiếu hỏng, 0 chu trình; FND đứng trước JVA/INT trong thứ tự khoá |
| `check_xref.py`, `check_meta.py` | 0 vấn đề |
| `check_course_refs.py` | **CHƯA CÓ KẾT QUẢ**: quét cả kho, chạy > 280 s và > 10 phút (máy đang tải) vẫn chưa in gì; người điều phối chạy lại khi máy rảnh. Phần liên quan FND đã tự kiểm bằng lint E22–E24/E37 (0 FAIL, 0 WARN) |
| `check_next_refs.py` | **FAIL do thiếu FND trong `pack.py STAGES`** (`bài không có chỗ trong dãy: FND:L00…`) — việc của người điều phối |

Số liệu từng bài (`audit/fnd/stats.py`, ≈ 135 từ/phút ở tốc độ −5%): L00 2 206 từ (≈ 16,3 phút); L01 1 880 (13,9); L02 1 852 (13,7); L03 1 738 (12,9); L04 1 840 (13,6); L05 1 923 (14,2); L06 1 684 (12,5); L07 1 934 (14,3); L08 1 880 (13,9); L09 1 776 (13,2); L10 1 905 (14,1). Mỗi bài 12 cảnh (L00: 15), có `af2: true`, `covers` đủ, cảnh `practice` + lab `labs/FND/Lxx` (de.md, mong_doi.txt, đúng một loi_giai), ≥ 1 cảnh quy mô ≥ 2–3 mức (×1/×100/×1 000…).

## Bài đã xong (cả 11)
- **L00** Máy chạy chương trình thế nào · cách học · chuẩn bị máy (thang thời gian bộ nhớ/ổ thể rắn/ổ cơ ×1, ×100, ×10 000; vòng học xem–tự làm–chấm–ôn; `kiem.sh` sáu dòng ✔; lab chạy qua cham.sh).
- **L01** pwd/ls/cd, đường dẫn tuyệt đối/tương đối, cây thư mục (hình), `/c/Users/ban` ↔ `C:\Users\ban`; MAX_PATH 260 làm quy mô.
- **L02** mkdir/touch/echo/>/>>/cat/cp/mv/rm, `*`/`?` do cửa sổ lệnh mở ra (xem trước bằng echo), rm không thùng rác, biến rỗng trong `rm -rf`; lab dựng cây + `find | sort`.
- **L03** head/tail/wc/grep/cut/sort/uniq, ống, `2>`, `/dev/null`; sort -n; quy mô 12 / 1 200 / 120 000 dòng (byte đo thật); lab thống kê CSV giả.
- **L04** PATH (thứ tự thắng), biến/export, `$?`, `&&`/`||`, `set -e`, `pipefail`; xác suất ≥ 1 lỗi 1,0% / 9,5% / 63,2%; lab in phiên bản + mã thoát + lệnh trong PATH.
- **L05** UTF-8 (259 → c4 83 làm tay), LF/CRLF (`cat -A`), đọc lỗi javac/python/bash thật, lỗi gốc ≠ nơi báo; lab sửa 3 tệp hỏng.
- **L06** CSV/JSON/YAML, đường đi `hang[1].gia`, lỗi cú pháp thật (`python -m json.tool`), CSV vs JSON 2,3–2,6× dung lượng đo thật; lab viết tay JSON + đọc YAML (đáp án số).
- **L07** HTTP + `curl` tới máy chủ Python cục bộ (200/201/404/405/500, `-f`→22, `--max-time`→28), định luật Little cho số người phục vụ; lab khởi động máy chủ trong script rồi hỏi 4 câu.
- **L08** sqlite: bảng/khoá chính/NULL, SELECT/WHERE/GROUP BY, UPDATE/DELETE, giao dịch (mất 100 000 trong nháp rồi ROLLBACK), chỉ mục 7/700/70 000 hàng; lab `.sql`.
- **L09** init/add/commit/status -s/log/diff/branch/switch/merge, `.gitignore`, bí mật đã chốt vẫn đọc được, chia đôi 3/10/17 lần thử; lab dựng kho 3 lần chốt.
- **L10** dự án sổ tay giao dịch: CSV → sqlite (khung nhìn) → 3 báo cáo → kiểm SQL = awk = tay → git; chạy lại không idempotent (LECH 6 300 000 vs 3 150 000); ×1 000 (10 000 giao dịch, 248 221 byte, tổng 130 000 000); lab bash+SQL+git.

## Công cụ đã dựng (trong phạm vi được ghi)
`audit/fnd/`: `lib.py` (cmd/term_block/file_block, SAY_FORBIDDEN), `gen.py`, `runner.py` + `verify_fnd.py` (Git Bash thật; thư mục tạm → `C:/Users/ban`; HOME, cấu hình Git riêng, ngày Git cố định, alias `ls -F` như Git Bash thật; đổi `…/run.sh: line N:` → `bash:`), `explore.py`, `frames_index.py`, `stats.py`, `shim/sqlite3` + `sqlite3_shim.py` (máy kiểm chưa cài sqlite3), `assets/` (máy chủ HTTP, awk), `src/l00..l10.py`, `probes/f1.yaml|md`, `probe_terms_gpu.py`; `tools/registry/lexicon_vi.FND.yaml`, `symbols.FND.yaml`; `labs/FND/L00..L10`; `lessons/fnd/*`; `curriculum/fnd.yaml` (viết sau cùng).

## Phát âm (probe ASR, `audit/fnd/probes/f1.md`)
Chỉ HTTP (8/8, đối chứng âm 0/8) và rm (8/8, TTS đọc «rơ mờ») đạt; ls 4/8, cp 4/8, mv 4/8, csv 5/8, grep 3/8, UTF-8 4/8, sqlite 2/8, Linux 1/8, bash 2/8, curl 1/8, cat/echo 2/8; Git đã có kết quả ≤ 4/8 ở BNX x1 và DVO. **NOT_VERIFIED một phần**: ~40 ô của mẻ dò bị edge-tts trả «không có âm thanh» (lặp lại với biến thể ngắn như «ls», «cd») nên điểm thấp một phần do dịch vụ. Quyết định: lời đọc của FND KHÔNG nói tên lệnh/công cụ (Git, bash, curl, grep, sqlite, Python, Linux, Windows…), chỉ tả bằng tiếng Việt ("lệnh in vị trí", "công cụ quản lý phiên bản"); tên gốc chỉ hiện trên màn hình. Lexicon chỉ có CPU, RAM, JDK, API, SQL, JSON, YAML, Java, byte (chép từ khoá đã ASR) + `foreign_ok: [http]`. `gen.py` từ chối lời đọc có tên lệnh/từ khoá bash/SQL/Git.

## Điều chưa nhét được / giới hạn (trung thực)
1. **Python** ở L06 (đọc JSON), L05 (traceback), L07 (máy chủ), L10 chỉ dùng như công cụ (`python -m json.tool`, tệp 5 dòng); cú pháp Python không được dạy (thuộc PYT). Lời đọc nói "ngôn ngữ thứ hai của khoá".
2. **YAML** chỉ đọc bằng mắt và so với JSON bằng `checks` (PyYAML trong lint); không có bộ đọc YAML chạy trên màn hình vì Python hệ thống của người học chưa chắc có PyYAML.
3. **Lab L01** thay "in `pwd` cuối" bằng `ls`/`ls ..` (đường dẫn tuyệt đối trong thư mục tạm không cố định, cham.sh không chuẩn hoá đường dẫn). **Lab L06** là tệp lệnh viết JSON bằng tay + `echo` đáp án YAML (không phải loi_giai.md giấy bút) để lab_gate chạy được thật. **Lab L00** in ✔ cho 6 công cụ (không in phiên bản vì phụ thuộc máy); `check_env.sh` vẫn dùng được riêng.
4. Một số nguồn trích **theo trí nhớ, chưa mở lại** (ghi NOT_VERIFIED trong `source`): Roediger & Karpicke 2006 (L00), MAX_PATH 260 của Microsoft (L01), Little 1961 (L07), Hennessy & Patterson (L00, chỉ số minh hoạ bậc độ lớn).
5. `ls` trong video xếp cột và có `/` sau thư mục (alias thật của Git Bash, đã đối chiếu `/etc/profile.d/aliases.sh` trên máy kiểm); thông báo lỗi của `javac`/`python`/`curl` đo trên JDK 21.0.13, Python 3.11.9, curl 8.x — chữ có thể khác chút ở phiên bản khác (đã tránh các thông báo đổi giữa 3.11 và 3.13).
6. Không có kiểm tai người; ASR chưa chạy cho lời đọc (đúng yêu cầu: không build/tts/asr).

## Việc còn lại cho người điều phối (ngoài phạm vi được sửa)
- **`labs/cham.sh` lỗi trên Windows có bí danh Microsoft Store**: dòng `PY=$(command -v python3 || command -v python)` chọn `python3` là *stub* Store (in "Python was not found; run without arguments to install from the Microsoft Store") ⇒ MỌI lab `.py`/`.sql` (khi chưa có sqlite3) FAIL trên máy kiểm và trên máy người học Windows. `lab_gate.py FND` chỉ PASS đủ 11 khi tôi chạy với PATH đã bỏ `WindowsApps`; chạy nguyên PATH thì L08 FAIL vì lỗi này. Đề xuất sửa cham.sh: thử `python3 --version` rồi mới dùng, hoặc ưu tiên `python`.
- `tools/registry` / `pack.py` STAGES / `curriculum/tracks.yaml`: thêm FND vào STAGES (Chặng 0, trước JVA) — **`check_next_refs.py` hiện FAIL** với `bài không có chỗ trong dãy: FND:L00…` cho tới khi làm; `JVA L00` `requires_ext` → `FND:L10` và bản đồ khoá của HOC_TAP.
- `audit/verify_plan_curricula.py`: chưa có dòng `FND:Lxx` nên `example` của curriculum/fnd.yaml không gắn "(VER FND:Lxx)" (đã ghi "số minh hoạ chạy thật bằng verify_fnd").
- Lời đọc của JVA L00 vẫn bảo dùng Command Prompt/PowerShell; nên đổi sang Git Bash (hợp đồng ENV.md) khi FND vào dãy.
- Dựng (build/tts/asr) chưa làm theo yêu cầu: sau dựng cần `asr` rà các câu có số dài.
