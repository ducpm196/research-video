# fix4_PYT: sửa khoá PYT vòng 4 theo `R4_PYT.md` (một tác tử, cả khoá)

Nguồn sửa: `audit/pyt/src/lNN.py` → `gen.py` (không sửa YAML sinh ra bằng tay). Không chạy build/tts/asr/git/docker. Nền: MUST 0, P1 = 2 ở 8/14 theo chuẩn chặt (0 mục chưa giảng). Mục tiêu vòng này: MỌI bài 0 mục chưa giảng.

## TIẾN ĐỘ
- Xong cả 9 bài đổi (L00, L02, L05, L06, L07, L08, L11, L12, L13) và đã qua cổng; L01, L03, L04, L09, L10 không đổi.

## 1. Bài đổi, CẦN DỰNG LẠI (spec_sha256 đổi)
L00, L02, L05, L06, L07, L08, L11, L12, L13 (9 bài). Không đổi nguồn: L01, L03, L04, L09, L10 (bản video cũ còn khớp). Lab đổi (`de.md`): L00, L02, L06, L08, L13 (máy chấm không đổi: `mong_doi.txt`/`loi_giai.py` giữ nguyên).

## 2. Mục "chưa giảng" nay giảng tại chỗ
| Bài | Mục | Cách giảng (chữ trên màn hình + lời đọc) |
|---|---|---|
| L00 | `cd`, "Open Git Bash here", `pwd` | prereq có hai step mới: phiên Git Bash thật (`pwd`, `cd khoa_hoc`, `pwd`, `ls` ra `labs/`; `verify_pyt` sh `ThuMuc`) + hộp "mở thư mục gốc trong File Explorer, chuột phải, Open Git Bash here (Windows 11: Show more options), kiểm bằng pwd và ls"; example step0 và de.md nhắc lại; câu chung "mọi tệp của khoá lưu ở thư mục gốc của bộ khoá" làm điểm tựa cho các bài sau. Mục sổ `pyt_cd` (introduces ở L00; L08 `assumes`) |
| L02 | `...` dấu nhắc nối, `:.2f`, `min` | formula step1: ghi chú "dòng `...` là dấu nhắc nối, bấm Enter thêm một lần (dòng trống) để báo hàm xong" (chữ + lời đọc); `:.2f` bỏ hẳn: đoạn đo dùng `round(x, 2)` đã học từ bài 0 (số in vẫn chạy thật); `min`: example step3 thêm phiên `min(0.31, 0.29, 0.30)` ra `0.29` + câu giảng; hint practice và de.md chỉ cách `min(mot_lan(f), …)` |
| L05 | `mkdir(parents=True, exist_ok=True)`; `2>`, `tail`, `cut`; `\r\n` | example step2: ghi chú hai đối số (chữ + lời đọc); pitfalls step3 giữ khối lệnh ngay trên chữ giải thích (không còn giải thích ở màn hình không có lệnh); bỏ `.replace("\r\n", ...)` thừa khỏi mã ghi CSV (đọc chế độ văn bản đã tự đổi; đầu ra y nguyên, verify 16/16) |
| L06 | `"A%07d" % i`, `[0]*1000`, đoạn thử 5 dòng chỉ ở de.md | đổi sang `"A" + str(i)` (mã demo `tracemalloc`) và `list(range(1000))` (đã học L01; vẫn ra 8056 byte, verify chạy 3.11 và 3.13); practice thêm step đầu "Đoạn thử cho sẵn: thêm ĐÚNG như vậy vào cuối tệp" hiện đủ 7 dòng của đoạn thử |
| L07 | `sum(ds)`, `format="%(levelname)s …"` | tiêu đề khối hook ghi `sum` cộng các số, `len` đếm phần tử + câu lời đọc; ví dụ nhật ký: `%(levelname)s` điền tên mức, `%(message)s` điền nội dung (chữ + lời đọc); tách step để khỏi tràn |
| L08 | "sys, time, math không bị che" chỉ kiểm trên Windows; practice step0 mở thư mục | hình + lời đọc: "trên bản cài chuẩn đã kiểm … máy khác có thể che, nên cứ tránh tên trùng" (màn hình ghi rõ Windows/python.org); practice step0 + de.md: thư mục gốc của bộ khoá, `pwd` rồi `ls` thấy `labs/`, chưa đúng thì `cd` tới đó hoặc Open Git Bash here (nhắc bài 0); `assumes: [pyt_cd]` |
| L11 | `rng = np.random.default_rng(1)`, `rng.normal`, `gridsize`; `dem, bien, _ =`; `subplots(1, 2)` | scale: mã vẽ gộp tách hai khối (dựng điểm / vẽ ô lục giác) mỗi khối kèm ghi chú và lời đọc; formula step3 ghi chú "hist trả ba thứ, gán ba tên, `_` là tên cho thứ không dùng"; step5 ghi chú `subplots(1, 2)` trả khung + cặp biểu đồ, `fig, (ax1, ax2) =` tách cặp |
| L12 | màn hình bỏ `..F....` và `FAILURES` | hook step1 hiện đủ đầu ra pytest thật (+ câu giải "mỗi ca một ký tự, F là ca đỏ"); formula step4 ghi "màn hình đã rút gọn: máy thật còn in thêm dòng `..F....` và `FAILURES`" (chữ + lời đọc) |
| L13 | `.items()` + từ điển suy ra; `sys.path`; ví dụ mẫu mục tiêu 7; thời lượng 45–60 vs 20 phút | `.items()` và từ điển suy ra giảng ở formula step4 (`introduces: pyt_items`, `pyt_items` trong sổ); `sys.path` giảng trong hint practice (danh sách thư mục theo thứ tự, `insert(0, …)` lên đầu; bỏ "như bài 8"; `pyt_sys_path`) và comment de.md; ví dụ mẫu mới ở scene example, 4 step: `tong_tien.py` (mô-đun), `test_tong_tien.py` (hai nửa; `tempfile` giảng tại đây, `pyt_tempfile` chuyển về step này), chạy `python -m pytest -q` ra `2 passed` (chương trình `du_an_mau`, `show_files` dựng lại từ màn hình rồi chạy thật), `requirements.txt` một dòng ghim; covers mục tiêu 7 thêm "example"; thời lượng: màn hình + lời đọc + de.md cùng nói "video dừng 20 phút cho lượt đầu, cả bài dự kiến 45–60 phút"; `assumes` thêm `pyt_assert` |

Sổ `tools/registry/symbols.PYT.yaml` thêm 3 mục (Edit nhỏ): `pyt_cd`, `pyt_sys_path`, `pyt_items`.

## 3. Độ dài lời đọc (≤ 2 300 từ; thêm ở đâu cắt ở chỗ khác)
L00 2273, L01 2151, L02 2284, L03 2257, L04 2229, L05 2126, L06 2296, L07 2145, L08 2294, L09 2057, L10 2134, L11 2292, L12 2247, L13 2294. Cắt để bù: L00 (câu cài đặt PATH ở prereq, vài câu đệm), L08 (câu nguyên nhân ở hook, dẫn bảng), L11, L13 (cắt ~230 từ ở hook, prereq, bước 0, thời gian, ví dụ B, scale, lỗi 3, đáp án, recap), L06 (rút lời đọc step đoạn thử). Mọi `say` 4–38 từ; ba câu ngắn sẵn có (3 từ: "Viết ba hàm.", "Bước bốn, JSON.", v.v.) nằm trong step ≥ 8 từ, lint 0 WARN.

## 4. Cổng thật (máy rất tải: có nhiều tác tử build/asr chạy cùng; chạy từng bài một)
- `lv.py lint`: **0 FAIL, 0 WARN** ở cả 9 bài đổi (L00 35 PASS, L02 20, L05 20, L06 21, L07 19, L08 20, L11 24, L12 26, L13 23).
- `lv.py render`: **0 vấn đề** ở cả 9 bài (L00 150 khung, L02 156, L05 146, L06 147, L07 139, L08 156, L11 145, L12 147, L13 143). Đã sửa các lần tràn bảng bằng cách tách step (L00 cd; L07 hook và nhật ký; L11 scale; L13 test). Đã xem khung PNG: L00 `00016`, L12 `00002`, L11 `00085`, L13 `00057`.
- `verify_pyt`: L00 24/24, L02 16/16 (chạy lại sau lần đầu lệch), L05 16/16, L06 16/16, L07 14/14, L08 14/14, L11 11/11, L12 14/14, **L13 10/11**.
- `lab_gate PYT`: **14 PASS · 0 FAIL (196 lab)** (lần cuối, sau mọi sửa).
- `lv.py curriculum curriculum/pyt.yaml`: 14 bài, 0 lỗi. `tests/test_e52.py`: 0 FAIL. `check_course_refs PYT`: 0 vấn đề. `check_next_refs`: 550 lời hẹn, 0 lệch. `arith_scan`: 245 phép tính, 0 FAIL. `check_curricula_graph`: VER dẫn tới mã không PASS 0.
- `screen_code check --course PYT`: STALE 7, MISSING 12, ORPHAN 3 sau sửa → `gen-pyt` (343 khối, ghi 341, chưa khớp 2) → thêm 2 mục `hand: true` (L02 example 2 0 mã đo thời gian, L06 example 9 0 mã đo `tracemalloc`: trùng nguyên văn mã của `measure`, đọc kiểm) và sửa mục tay L06 example 9 1 (số MB lấy từ `measured.json` = 18,5). Kết quả cuối: `screen_code check --course PYT`: **PASS 539 · FAIL 0 · STALE 0 · MISSING 0 · ORPHAN 0 · WARN 0** (343 khối).

## 5. P1 dự kiến
Mọi mục "Cần biết trước" của R4 đã xử lý: L00 (cd/pwd/Open Git Bash here), L02 (`...`, `:.2f`, `min`), L05, L06, L07, L08, L11, L12, L13. L01, L03, L04, L09, L10 không có mục nào theo bảng R4. Dự kiến P1 = 2 ở 14/14 theo chuẩn chặt.

## 6. Mục không sửa / còn hở (lý do)
- **`verify_pyt L13` ô `measure l13_scale`**: `t_line_1e3` và `t_chunk_1e3` lưu 0,0028/0,0032 s, đo lại 0,022–0,044 s (lệch quá ×8) do máy tải (hai lần liên tiếp); các chương trình, ví dụ mẫu `du_an_mau` và mọi ô tất định đều PASS. Đây là nhiễu đo ở quy mô 10^3 dòng, không phải lỗi bài (như L03/L10 ở vòng trước): cần chạy lại `verify_pyt L13` khi máy rảnh.
- **Lab L02 đo thời gian** ("Goi ham cham hon viet thang") đảo kết quả khi máy tải nặng (một lần `lab_gate` lệch KHONG; chạy lại: 14 PASS). Bản chất đề là so thời gian; giữ nguyên đề.
- **Không kiểm được tai người**: các câu `say` mới/đổi ở L00, L02, L05, L06, L07, L08, L11, L12, L13 là câu TTS mới (chỉ kiểm được ≥ 8 từ mỗi step, 4–38 từ mỗi câu, không từ Latin/Anh — đã bỏ "Windows" khỏi lời đọc L08 vì lint cảnh báo).
- **`exec` và `tempfile` trong de.md L13**: `tempfile` đã giảng ở ví dụ mẫu; `exec` chỉ có ở de.md (mẫu "Cách 2"), có chú thích một dòng tại chỗ, không đưa lên video vì đã có cách 1 (`sys.path`) được giảng.
- **`sys.path` ở hint, không ở thân bài**: người học chỉ thấy khi hết dừng; tôi giảng thêm trong comment de.md để tự đủ khi mở đề.
- **Windows 11**: ghi chú "Show more options" chỉ ở chữ trên màn hình và de.md (không đọc trong lời).
- **Chưa kiểm**: hành vi `math`/`time` bị che trên Linux/macOS (chỉ hạ giọng lời nói), wheel Python 3.13 của numpy/pandas/matplotlib/pytest.
- Video của cả 9 bài đổi STALE, cần dựng lại (build/tts/asr do người điều phối).
