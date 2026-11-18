# Sổ "mã trên màn hình" khoá PYT — 297 khối (L00–L13), 2026-11-14

## Kết quả cổng (chạy thật, lần cuối)
- `python -B audit/review/screen_code.py check --course PYT -v` → `screen_code: 297 khối — PASS 474 · FAIL 0 · STALE 0 · MISSING 0 · ORPHAN 0 · WARN 0` (297 khối + 177 nguồn; `loại: output 180, fragment 59, run 57, other 1`; `unverified_claims 16`).
- `check --course JVA` → `390 khối — PASS 536 · FAIL 0 · STALE 0 · MISSING 0 · ORPHAN 0 · WARN 0` (không đổi).
- `check --course FND` → `193 khối — PASS 278 · FAIL 2`: cả hai là `FND L00 practice 1 0` và nguồn `LAB_L00` (lời giải lab L00 in `THIEU sqlite3` vì máy này **không có sqlite3 CLI**; `which sqlite3` rỗng). Không liên quan thay đổi lần này (khối bash, không đi qua nhánh python; FND/JVA/JV2 không có mục `lang: python`, đã grep). Ghi để người điều phối biết; không sửa.
- Bài PYT **không bị sửa**: không khối nào sai hay chạy ra khác điều bài nói (không có lỗi MUST/SHOULD cần sửa nguồn `audit/pyt/src`). Không chạy build/tts/asr/git/docker.

## Số khối theo kind
| Bài | khối | run | syntax | fragment | output | pseudo | other |
|---|---|---|---|---|---|---|---|
| L00 | 28 | 3 | 0 | 3 | 22 | 0 | 0 |
| L01 | 32 | 12 | 0 | 1 | 19 | 0 | 0 |
| L02 | 21 | 6 | 0 | 1 | 14 | 0 | 0 |
| L03 | 23 | 6 | 0 | 3 | 14 | 0 | 0 |
| L04 | 17 | 1 | 0 | 2 | 14 | 0 | 0 |
| L05 | 22 | 8 | 0 | 1 | 13 | 0 | 0 |
| L06 | 25 | 3 | 0 | 9 | 13 | 0 | 0 |
| L07 | 26 | 7 | 0 | 5 | 14 | 0 | 0 |
| L08 | 12 | 0 | 0 | 10 | 1 | 0 | 1 |
| L09 | 17 | 3 | 0 | 0 | 14 | 0 | 0 |
| L10 | 33 | 5 | 0 | 11 | 17 | 0 | 0 |
| L11 | 19 | 1 | 0 | 8 | 10 | 0 | 0 |
| L12 | 11 | 0 | 0 | 2 | 9 | 0 | 0 |
| L13 | 11 | 2 | 0 | 3 | 6 | 0 | 0 |
| **Cộng** | **297** | **57** | **0** | **59** | **180** | **0** | **1** |

Khối `>>>` (cửa sổ tương tác) là `output of` nguồn phát lại phiên; vì vậy `output` nhiều. 295/297 khối do máy sinh, 2 khối `hand: true` (xem dưới).

## Cách làm (máy sinh `gen-pyt`, không chép tay)
`python -B audit/review/screen_code.py gen-pyt` (≈ 6 phút) sinh `audit/review/screen_code/PYT.yaml` từ `audit/pyt/src` (`lib.PROGS/REPLS/SHS`), **177 nguồn** chạy thật: 96 chương trình `py`, 64 phiên `repl`, 10 phiên `sh`, 5 `term`, 2 `echo`. Mỗi mục được thử bằng chính cổng trước khi ghi. Thứ tự thử cho một khối: (1) bằng CẢ chương trình → `run` (kèm `expect_stdout` / `expect_exception` + `expect_stderr_contains`, `stdin`, tệp dữ liệu `fs`); (2) dãy dòng liên tiếp của mã hoặc của tệp `fs` (csv, `phi.py`, `test_*.py`) → `fragment within`; (3) dãy con có thứ tự của đầu ra thật → `output of`. Ưu tiên nguồn cùng cảnh/bài.
- **repl**: nguồn là chương trình phát lại từng câu bằng `code.InteractiveConsole` (đúng harness `verify_pyt`), in lại phiên `>>> …`/`... `/đầu ra; khối màn hình là `output of` nó (mỗi dòng phải khớp cả dòng, đúng thứ tự).
- **echo** (`L00_nhap_echo`, `L00_nhap_sai_echo`): cùng chương trình + `stdin`, prelude (có `prelude_reason`) in lại dòng vừa gõ như terminal, để khớp khối `io_block` hiện dòng gõ ngay dưới lời nhắc.
- **term** (5 nguồn L12): cửa sổ `$ python -m pytest -q --tb=short` chạy ĐÚNG lệnh đó (tiến trình con `sys.executable -m pytest`) trên các tệp của chương trình bọc `pytest.main`; khối màn hình là `output of` nó.
- **sh**: phiên Git Bash như FND (`profile: fnd`, `python` = bản trong PATH).
- Python: `std` chạy trên `.venv` 3.13 (`verify_pyt` đã so 3.11 = 3.13); `venv` chạy `labs/.venv-pyt` 3.11.9 (numpy/pandas/matplotlib/pytest ghim), `MPLBACKEND=Agg COLUMNS=80 TZ=UTC`.

## Khối làm tay (`hand: true`, giữ qua các lần sinh)
| Khối | kind | Vì sao |
|---|---|---|
| `PYT L03 practice 0 0` | fragment (không `within`) | đề rút gọn bằng `…` (2 trong 6 giao dịch); dòng `ten = …` và hai bộ đầu khớp nguyên văn lời giải lab (`src:PYT:L03_lab_l03`, chạy thật) |
| `PYT L08 example 1 0` | other/bash, `read_check` | `source …/activate`, `pip install -r requirements.txt`, `python chay.py`: bước `pip install` cần mạng |

## Thay đổi ở `audit/review/screen_code.py` (cộng thêm, không đổi hành vi mục cũ)
Thêm lệnh `gen-pyt` (+ `_pyt_sources`, `cmd_gen_pyt`, `_render_repl`, `_sub_match`). Nhánh `run python` của cổng thêm các khoá tuỳ chọn, chỉ có tác dụng khi mục khai chúng: `python: venv` (dùng `labs/.venv-pyt`), `stdin` (đưa vào python), `env` (biến môi trường thêm), `fs: {đường dẫn: nội dung}` (ghi tệp dựng sẵn NGUYÊN VĂN cạnh chương trình; `within: "src:PYT:<tên>#<tệp>"` hoạt động như phiên FND), `normalize: [[regex, thay]]` (số đo đổi mỗi lần, ví dụ `in 0.05s` của pytest), và: khi `expect_exception` là `SyntaxError/IndentationError/TabError` thì bỏ bước `compile` nguyên văn (để python báo lỗi thật; trước đây khối lỗi cú pháp cố ý không thể `run`). Docstring đầu tệp chưa cập nhật (nên thêm một dòng nếu người điều phối muốn).

Kiểm chứng cổng (âm/dương, `negctl.py` trong scratchpad): 8 nguồn đúng → PASS; sai stdout, thiếu dòng gõ ở echo, thiếu stdin, `normalize` lệch/bỏ, sai loại lỗi, chương trình hợp lệ mà mong IndentationError, phiên repl sai kết quả, tệp csv sai, khối output có dòng lạ, đổi một ký tự khối fragment → **đều FAIL** đúng.

## Đối chiếu lời đọc với màn hình (heuristic, không phải cổng)
Máy sinh không điền `claims:` từng khối. Thay vào đó quét `numscan.py`: đổi số đọc bằng chữ trong `say` của mọi bước có khối mã sang số rồi so với số hiện trên màn hình cùng bước/cảnh. 43 số khác màn hình cùng bước, 27 số không có ở cả cảnh; đọc tay các số đáng ngờ (L00 `formula` 360000 và `example` 2030000; L01 `formula` 139 tháng ≈ 11,6 năm; L02 `hook` 40/37 chỗ; L07 `hook`; L08 `formula` 1100/5000/2000; L10 `check` 1 450 000/3 000 000/300 000/4 750 000; L11 `example` 42,5 %; L11 `formula` 5,5,0,0,1; L13 `example/check`) — tất cả khớp màn hình hoặc là số kể chuyện/quy mô không hiện thành mã (một triệu giao dịch…). **Không tìm thấy điều bài nói khác kết quả máy in.** Số trong lời đọc không đổi được hết thành tham chiếu máy: đây là kiểm một phần.

## NOT_VERIFIED (16 `unverified_claims`) và điều máy không kiểm được
1. **Thời gian pytest** (10 mục: 5 nguồn `L12_*`, 5 `L12_*_term`; 10 + 4 repl + 2 khối tay = 16): màn hình ghi `7 passed in 0.05s`, `1 failed, 6 passed in 0.12s`… là số đo MỘT lần; cổng chuẩn hoá `in <số>s` về đúng chữ trên màn hình (`normalize`), kiểm phần còn lại của đầu ra, KHÔNG kiểm con số giây.
2. **Tracebacks trong cửa sổ `>>>`** (4 nguồn repl: `L03_repl_Tuple`, `L04_repl_BatBien`, `L07_repl_LoaiLoi`, `L09_repl_LanTruyen`): màn hình hiện dạng ngắn `File "<stdin>", line 1, in <module>` (đúng 3.11 và cửa sổ cơ bản của 3.13). Cửa sổ tương tác MỚI của 3.13 trong terminal thật (pyrepl) in `File "<python-input-N>"` kèm dòng mã và dấu `^`. Máy dùng `code.InteractiveConsole` nên không đối chiếu được hiển thị của cửa sổ thật trên 3.13. Mức SHOULD nếu học viên dùng 3.13 trong terminal; lời bài nói "Python 3.11 trở lên". Chưa sửa bài (đổi chữ trên màn hình/lời đọc cần dựng lại).
3. `PYT L03 practice 0 0`: bốn giao dịch bị lược bằng `…` trên màn hình; phần lược không được cổng đối chiếu (nằm trong `de.md` và lời giải lab, lời giải lab chạy thật).
4. `PYT L08 example 1 0`: `pip install -r requirements.txt` cần mạng, không chạy; việc cài đúng phiên bản ghim không kiểm bằng máy ở khối này (lab L08 tự kiểm).
5. Khối `std` chỉ chạy trên 3.13 ở cổng này; việc 3.11 = 3.13 dựa vào `verify_pyt` (183/183 PASS theo báo cáo khoá), không lặp lại ở cổng. Khối `venv` chỉ trên 3.11 + phiên bản ghim.
6. Kiểm tai/mắt người, dựng video (build/tts/asr): không thuộc nhiệm vụ; chưa có.

## Gợi ý cho cổng / người điều phối
- Cập nhật docstring `screen_code.py` cho các khoá mới (`python`, `stdin`, `env`, `fs`, `normalize`, lệnh `gen-pyt`).
- FND LAB_L00 FAIL do máy thiếu sqlite3 CLI (`THIEU sqlite3`): cần cài sqlite3 hoặc cho `shim_sqlite3` nhận biết `command -v sqlite3`.
- Mỗi lần đổi `audit/pyt/src` hoặc `lessons/pyt/*`: chạy lại `gen-pyt` rồi `check --course PYT -v` (sha khối đổi → STALE nếu không sinh lại; mục `hand` chỉ giữ khi sha không đổi).

## Tệp
`audit/review/screen_code.py` (sửa), `audit/review/screen_code/PYT.yaml` (mới, sinh), `audit/review/audit_final/reports/screen_pyt.md` (báo cáo này). Không bài PYT nào đổi → không cần dựng lại.
