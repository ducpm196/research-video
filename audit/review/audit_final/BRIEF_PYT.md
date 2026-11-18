# BRIEF_PYT — soạn khoá PYT "Python từ con số 0" (14 bài, L00–L13) — 2026-11-13

Đọc trước (BẮT BUỘC): `audit/review/audit_final/BRIEF_AF2.md` (chuẩn bài AF2: `af2: true`, `covers`, cảnh `practice`/Tự làm + lab, thuật ngữ tại chỗ, cảnh quy mô), `audit/review/audit_final/BRIEF_FND.md` (cách dựng một khoá mới: bộ sinh + verify + lab), `labs/ENV.md`, `audit/fnd/lib.py` + `gen.py` + `verify_fnd.py` + `src/l03.py` (mẫu mới nhất), `audit/jva/lib.py` (hàm `prog`, `code_block`, `out_block`: mẫu khai chương trình chạy thật), `audit/labkit.py`, `.claude/skills/lecture-video/SKILL.md` + `references/pedagogy.md`.

## Người học và vị trí
Mất gốc. Đã học FND (dòng lệnh Git Bash, tệp, lỗi, CSV/JSON/YAML, HTTP, SQL, Git); **không giả định đã học JVA/JV2** (khoá sau Java cũng như trước Java đều phải đọc được PYT) — vì vậy mỗi khái niệm lập trình (biến, kiểu, vòng lặp, hàm, lớp…) được **giảng lại tại chỗ** bằng Python, ngắn, có số cụ thể; không viết "như trong Java". `requires_ext` của PYT chỉ gồm FND (L04, L05 cho L00; chọn bài FND đúng nhất, kiểm bằng `lv.py curriculum`). Mọi khoá sau dùng Python (BNX L00–L01 dùng f-string, `re`, comprehension, JSON; PLC, SDP, ESY, DSC, AIF, LLM, MLP…) phải đọc được mã nhờ PYT.

## Danh sách bài (đổi tên/tách gộp được nếu có lý do sư phạm, nhưng đủ nội dung)
| Bài | Nội dung | Lab (kết quả mong đợi tự đối chiếu; số liệu KHÁC ví dụ trong bài) |
|---|---|---|
| L00 | chạy `python`, REPL và tệp `.py`; giá trị, biến, kiểu (`int float str bool`), phép toán, `print`, `input`; số thực dấu phẩy động `0.1 + 0.2` | tính tiền lãi từ ba biến, in có định dạng |
| L01 | rẽ nhánh `if/elif/else`, so sánh, `and/or/not`; vòng `for`, `while`, `range`, `break/continue`; đọc lỗi thụt lề | phân loại giao dịch theo mức tiền, tổng và đếm bằng vòng lặp |
| L02 | hàm: `def`, tham số, giá trị trả về, tham số mặc định/có tên, phạm vi biến, hàm là giá trị, `lambda` | viết 3 hàm thuế/phí + hàm nhận hàm |
| L03 | `list`, `tuple`, `dict`, `set`; cắt lát; sao chép nông; sắp xếp với `key`; comprehension; độ phức tạp tra cứu (`in` trên list vs set, đo thời gian ở 10³ và 10⁶) | đếm tần suất, gộp hai danh sách theo khoá |
| L04 | chuỗi: cắt, tìm, thay, `split/join`, f-string và định dạng số, mã hoá UTF-8 và byte; biểu thức chính quy `re` (`search`, `findall`, nhóm) | trích số tiền và mã từ dòng nhật ký |
| L05 | tệp: `open`, `with`, đọc/ghi văn bản và UTF-8, `csv`, `json`, `pathlib`; đọc tệp lớn từng dòng | đọc CSV giao dịch, ghi JSON báo cáo |
| L06 | lớp, đối tượng, `__init__`, phương thức, `__repr__`, `dataclass`, kế thừa vs hợp thành, so sánh | lớp `TaiKhoan` có rút/nạp và kiểm số dư |
| L07 | ngoại lệ `try/except/finally`, `raise`, ngoại lệ tự định nghĩa; đọc traceback; `pdb`, `breakpoint()`, `logging` | sửa chương trình hỏng + bắt đúng loại ngoại lệ |
| L08 | mô-đun và gói, `import`, `if __name__ == "__main__"`, môi trường ảo `venv`, `pip install -r`, ghim phiên bản, `requirements.txt` | tạo venv, cài, chạy, in phiên bản (đối chiếu `labs/requirements-py.txt`) |
| L09 | `numpy`: mảng, hình dạng, phép toán theo phần tử, lan truyền (broadcasting), tổng/trung bình theo trục, vì sao nhanh hơn vòng lặp (đo ở 10⁶) | tính trung bình, độ lệch chuẩn, chuẩn hoá cột |
| L10 | `pandas`: `DataFrame`, đọc CSV, chọn lọc, `groupby`, `merge`, giá trị thiếu, kiểu ngày; vì sao bộ nhớ tăng theo số dòng | thống kê giao dịch theo loại/ngày |
| L11 | `matplotlib`: cột, đường, phân tán, histogram; ĐỌC biểu đồ đúng; ba cách biểu đồ đánh lừa (trục cắt, gộp, tỉ lệ); lưu ảnh (`Agg`) | vẽ và mô tả đúng một biểu đồ (lab kiểm số liệu vẽ, không so ảnh) |
| L12 | kiểm thử với `pytest`: ca kiểm, `assert`, `parametrize`, ca biên, vì sao kiểm thử cứu bạn khi mã lớn dần | viết ca kiểm cho hàm cho sẵn, bắt lỗi lệch một |
| L13 | tình huống chuyên gia: dự án phân tích tệp giao dịch 1 000 → 10⁶ → 10⁸ dòng: đọc cả tệp vs từng dòng vs pandas theo khối; đo thời gian/bộ nhớ ở từng quy mô; vì sao thiết kế phải đổi; cấu trúc dự án (mô-đun + kiểm thử + `requirements.txt`) | dự án nhỏ chấm bằng thang cho sẵn |

Mỗi bài có cảnh quy mô/thời gian (P9): số đo THẬT từ `verify_pyt` (thời gian, bộ nhớ, số bước) ở ≥ 2 mức; số thời gian ghi làm tròn và "(đo trên máy kiểm, số minh hoạ)" vì máy người học khác.

## Môi trường (hợp đồng lab)
- Python tối thiểu **3.11**; kho kiểm trên **3.11.9 (`labs/.venv-pyt`: numpy 2.4.6, pandas 3.1.1, matplotlib 3.11.2, pytest 9.2.0, ghim ở `labs/requirements-py.txt`)** và **3.13.5 (`.venv`, chỉ thư viện chuẩn + numpy)**.
- L00–L08 và L12 chỉ cần thư viện chuẩn (L12 cần `pytest`) — `verify_pyt` chạy mã THẬT trên cả 3.11 và 3.13 và so từng dòng. Bài dùng numpy/pandas/matplotlib/pytest chỉ kiểm trên venv 3.11. `labs/cham.sh` đã được vá để dùng `labs/.venv-pyt` khi python hệ thống thiếu thư viện (lab dùng `import numpy|pandas|matplotlib|pytest`). Kết quả số thực: in bằng `round()` hoặc định dạng cố định; không in đối tượng có địa chỉ bộ nhớ, thời gian, đường dẫn tuyệt đối. Seed cố định cho mọi ngẫu nhiên.
- Mọi lệnh người học gõ là Git Bash trên Windows (`python`, không `python3`; nói rõ `py` của Windows); cài đặt Python thuộc FND L00 (không dạy lại, chỉ kiểm `python --version`).
- Bài nào cần cài thêm: L08 dạy cài; lab L09–L12 ghi ở dòng đầu `de.md` "cần: pip install -r labs/requirements-py.txt".

## Hợp đồng khoá
1. `tools/lv.py new-course PYT --title "Python từ con số 0"` (xem `references/new-domain.md`); `curriculum/pyt.yaml` viết SAU CÙNG (bẫy E37); `tools/registry/lexicon_vi.PYT.yaml` + `symbols.PYT.yaml`. KHÔNG sửa `pack.py`, `tracks.yaml`, `curriculum/bnx.yaml` (người điều phối làm).
2. Bộ sinh `audit/pyt/` (lib.py, gen.py, src/l00.py…l13.py, verify_pyt.py) theo mẫu `audit/fnd/` + hàm `prog`/`code_block`/`out_block` kiểu JVA nhưng cho Python (`py(name, code, out, files, expect, stdin)`); verify chạy bằng tiến trình con, thư mục tạm sạch. Hàm mới trong `tools/checklib.py` (nếu cần) có tiền tố `pyt_`; chạy `audit/check_checklib_dupes.py`.
3. Chuẩn AF2 đầy đủ mỗi bài (BRIEF_AF2 mục 1–10): `af2: true`, `covers`, 10 cảnh + `practice` + lab `labs/PYT/Lxx/{de.md,mong_doi.txt,loi_giai.py|md}`; thuật ngữ giảng tại chỗ; không nhắc khoá khác trong màn hình/lời đọc ("như đã học ở khoá…" bị `check_xref` cấm; tên khoá/mã bài khác không xuất hiện trừ ghi chú `requires_ext` trong giáo án); câu hẹn "bài sau" chỉ ở hook/recap, `forward_ref: true`.
4. Lời đọc: không từ khoá Python bằng tiếng Anh (`if`, `for`, `while`, `def`, `import`, `class`, `return`, `try`, `with`, `lambda`…) — gen từ chối; đọc thành "câu lệnh rẽ nhánh", "vòng lặp đếm", "khai báo hàm"… Tên riêng (Python, pandas, numpy, matplotlib, pytest, JSON, CSV) **dò ASR** bằng `audit/cs112/probe_terms.py` trước khi dùng trong lời; < 7/8 thì chỉ hiện trên màn hình. Số đọc bằng chữ.
5. Độ dài mỗi bài 9–16 phút; L13 có thể dài hơn.
6. Mọi con số trên màn hình có `checks` và nằm trong verify; mã trên màn hình = mã chạy thật = lời giải lab (khối khác ví dụ).
7. Sổ `screen_code` cho PYT: tác tử không tạo (người điều phối làm với tác tử khác).

## Cổng cho mỗi bài (sạch mới sang bài sau)
```
cd /d/research-video
PYTHONIOENCODING=utf-8 .venv/Scripts/python -B audit/pyt/verify_pyt.py Lxx
PYTHONIOENCODING=utf-8 .venv/Scripts/python -B audit/pyt/gen.py Lxx
PYTHONIOENCODING=utf-8 .venv/Scripts/python -B tools/lv.py lint lessons/pyt/Lxx_*.yaml      # 0 FAIL, 0 WARN
PYTHONIOENCODING=utf-8 .venv/Scripts/python -B tools/lv.py render lessons/pyt/Lxx_*.yaml    # 0 vấn đề; tràn thì tách step + clear: true
PYTHONIOENCODING=utf-8 .venv/Scripts/python -B audit/review/lab_gate.py PYT
```
Cuối khoá: `tools/lv.py curriculum curriculum/pyt.yaml`, `audit/check_curricula_graph.py`, `check_xref.py`, `check_meta.py`, `check_course_refs.py`, `check_next_refs.py`; mở ≥ 3 khung PNG mỗi bài (render) kiểm bằng mắt. KHÔNG chạy `build`/`tts`/`asr`/`audit_all`/git/docker.
Bẫy: chuỗi có `\` (regex, `\n`) qua heredoc bash/python bị hỏng → dùng Edit/Write rồi `grep -c` ký tự điều khiển; `$` trên màn hình bọc `<span>&#36;</span>` (như FND `esc`); đầu ra chương trình viết không dấu ASCII; không `cat > file` không stdin.

## Báo cáo
Tin nhắn cuối ≤ 40 dòng: bài xong + cổng nào PASS (số thật), bài chưa xong và vì sao. Báo cáo dài ghi vào `audit/review/audit_final/reports/pyt.md`. Không kể quá trình. Làm theo thứ tự L00 → L13; nếu bị ngắt, ghi tiến độ vào đầu `reports/pyt.md`.
