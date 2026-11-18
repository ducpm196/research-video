# Báo cáo khoá PYT · Python từ con số 0 (14 bài L00–L13) — 2026-11-13/14

## Kết quả cổng (đo thật, cuối phiên)
| cổng | kết quả |
|---|---|
| `audit/pyt/verify_pyt.py` (cả khoá) | **183/183 PASS**: chương trình `py` chạy THẬT trên Python 3.11.9 và 3.13.5 (mỗi bản hai hạt giống băm, bốn đầu ra phải giống hệt), cửa sổ `>>>` bằng `code.InteractiveConsole`, phiên Git Bash (`python` lần lượt 3.11 / 3.13), bài dùng numpy/pandas/matplotlib/pytest chạy trên `labs/.venv-pyt` (3.11); L05 + L13 đo lại sau khi tách đo thời gian khỏi tracemalloc: 21/21 PASS |
| `tools/lv.py lint lessons/pyt/*.yaml` | 14/14 bài **0 FAIL, 0 WARN** (L00 34, L01 24, L02 20, L03 23, L04 23, L05 20, L06 20, L07 19, L08 20, L09 26, L10 22, L11 24, L12 26, L13 21 kiểm PASS) |
| `tools/lv.py render` | 14/14 bài **0 vấn đề** (L00 177 khung … L13 121 khung); đã mở xem bằng mắt ≥ 2–3 khung mỗi bài (cảnh trực giác, bảng quy mô, khối mã) |
| `audit/review/lab_gate.py PYT` | **14 PASS · 0 FAIL** (L00–L13; lời giải chạy qua `labs/cham.sh`) |
| `tools/lv.py curriculum curriculum/pyt.yaml` | 14 bài, 14 đã có đặc tả, 0 lỗi |
| `audit/check_curricula_graph.py` | 46 lộ trình, 0 tham chiếu hỏng, 0 chu trình; thứ tự khoá …FND → INT → DMS → RBM → JVA → **PYT** → CSA… |
| `check_xref.py` | **0 lượt** tham chiếu sang khoá khác ở 0 tệp (lần đầu bắt 1 cụm «các khoá khác» ở L13 recap, đã sửa) |
| `check_meta.py` | 1 vấn đề, KHÔNG thuộc PYT (`BNX L30` có đặc tả mà không có trong lộ trình) |
| `check_course_refs.py` | **CHƯA CÓ KẾT QUẢ**: quét cả kho, chạy > 15 phút (máy đang tải) vẫn chưa in gì; người điều phối chạy lại khi máy rảnh. Phần liên quan PYT đã tự kiểm bằng lint E22–E24/E37 (14 bài 0 FAIL, 0 WARN) |
| `check_next_refs.py` | **FAIL ngoài phạm vi**: `AssertionError: chu trình tiên quyết trong S03` trong `audit/review/learn_start/pack.py` (người điều phối sửa `pack.py STAGES`/`tracks.yaml`; PYT chưa có chỗ trong dãy) |

Độ dài lời đọc (ước 150 từ/phút): L00 15,9 phút (2 387 từ) · L01 13,7 · L02 12,8 · L03 13,6 · L04 13,7 · L05 12,4 · L06 13,5 · L07 12,7 · L08 13,1 · L09 12,5 · L10 12,0 · L11 13,5 · L12 12,6 · L13 12,9.
Mỗi bài: `af2: true`, `covers` đủ, 12 cảnh (hook, prereq, sym, intuition, formula, example, check, scale, pitfalls, quiz, practice, recap), ≥ 1 cảnh quy mô có số đo ≥ 2 mức và ngoại suy, lab `labs/PYT/Lxx/{de.md, mong_doi.txt, loi_giai.py}`.

## Bài đã xong (cả 14)
- **L00** chạy `python` (cửa sổ `>>>` và tệp `.py`), giá trị/kiểu/biến, phép toán, `print`/`input`, f-string; `0.1 + 0.2`, `12 000 000 × 0.072 = 863999.9999999999` (mất 1 đồng); quy mô: sai số số thực ở 1 / 10^6 / 10^15, `2**53`. Lab: lãi tiết kiệm 3 biến.
- **L01** `if/elif/else`, so sánh, `and/or/not`, `for`/`while`/`range`/`break`/`continue`, IndentationError; số lượt lặp và thời gian ở 10^3, 10^6, 10^7 (+ ngoại suy 10^9). Lab: phân loại giao dịch theo mức + tổng + đếm.
- **L02** hàm (tham số, trả về, mặc định, gọi có tên, phạm vi, hàm là giá trị, `lambda`); quy mô: số chỗ phải sửa 1/10/100 (2%/chỗ là giả định minh hoạ) và chi phí một lần gọi. Lab: 3 hàm phí/thuế + hàm nhận hàm.
- **L03** `list`/`tuple`/`dict`/`set`, cắt lát, sao chép nông, `sorted(key=)`, comprehension; `in` danh sách vs tập hợp ở 10^3 và 10^6 (+ 10^8 ngoại suy), bộ nhớ. Lab: đếm tần suất + gộp theo khoá.
- **L04** chuỗi (tách/ghép/tìm/thay), f-string và định dạng số, UTF-8 và byte (`len('tiền') = 4`, 6 byte), `re` (`search/findall/nhóm`); quy mô: mẫu `(a+)+b` gấp đôi mỗi ký tự (17/21/25 ký tự đo thật). Lab: trích mã và tiền từ nhật ký.
- **L05** `open`/`with`, UTF-8, `csv`, `json`, `pathlib`, đọc từng dòng; đọc cả tệp vs từng dòng (bộ nhớ 10^4, 10^6 dòng đo, ngoại suy 10^8). Lab: CSV → báo cáo JSON.
- **L06** lớp/đối tượng, `__init__`, `__repr__`, `dataclass`, kế thừa vs hợp thành, `==` vs `is`; bộ nhớ 10^5 và 10^6 đối tượng (lớp thường, `__slots__`, bộ ba). Lab: lớp `TaiKhoan` có thấu chi.
- **L07** `try/except/finally`, `raise`, ngoại lệ tự định nghĩa, đọc traceback, `logging` (pdb/`breakpoint()` chỉ mô tả, không chạy); chi phí ngoại lệ ở 0%/1%/50% dòng hỏng (10^6 chuỗi). Lab: sửa chương trình hỏng.
- **L08** mô-đun/gói, `__name__`, `venv` (tạo, kích hoạt, kiểm `sys.prefix`), `requirements.txt` ghim (`labs/requirements-py.txt`, 17 dòng), trùng tên thư viện chuẩn; thời gian nạp thư viện. Lab: tạo venv, cài, in số phiên bản chính (xem ghi chú).
- **L09** `numpy`: mảng, hình dạng, theo phần tử, lan truyền, theo trục, mặt nạ, độ lệch chuẩn từ định nghĩa; nhanh gấp trăm lần vòng lặp (10^4/10^6/10^7), tràn int32, view vs copy. Lab: chuẩn hoá cột.
- **L10** `pandas`: `read_csv`, mặt nạ, `groupby`, `merge`, giá trị thiếu, ngày; bộ nhớ theo số dòng, kiểu `category`. Lab: thống kê theo loại/ngày.
- **L11** `matplotlib` (Agg): bốn loại biểu đồ, ĐỌC biểu đồ, ba cách đánh lừa (trục cắt 1,03 vs 4,0; gộp 90,0/33,3 vs 88,9/20,0 nhưng chung 39,0 vs 82,0; thang loga), lưu ảnh; 10^3/10^5/10^6 điểm (thời gian, tệp SVG). Biểu đồ trên màn hình vẽ lại bằng SVG từ đúng số liệu mà chương trình đọc từ `ax`. Lab: kiểm số liệu vẽ.
- **L12** `pytest`: ca kiểm, `assert`, `parametrize`, ca biên, `approx`, đọc ca đỏ; chạy 10^2/10^3/10^4 ca. Lab: viết ca bắt lỗi lệch một (`range(1, n)`).
- **L13** tình huống chuyên gia: tệp 10^3 → 10^6 → 10^8 dòng; cả tệp vs từng dòng vs pandas theo khối (thời gian + đỉnh bộ nhớ đo ở 10^3, 10^6); bẫy quên cộng dồn; thống kê gộp được/không gộp được; cấu trúc dự án. Lab: tự dựng dự án nhỏ, hàm chấm 10 điểm cho sẵn.

## Công cụ đã dựng
`audit/pyt/`: `lib.py` (py / repl / sh / measure / M / io_block / run_block / run_slice / split_note / splitall / words / t_show / b_show), `gen.py`, `verify_pyt.py`, `autofill.py`, `frames_index.py`, `gates.sh`, `gates_all.sh`, `gen_curriculum.py`, `src/l00.py … l13.py`, `measured.json` (số đo; số thời gian chỉ cần cùng bậc độ lớn ×/÷ 8 khi kiểm lại), `probes/p1.yaml|md|log`; `tools/registry/lexicon_vi.PYT.yaml`, `symbols.PYT.yaml`; `curriculum/pyt.yaml` (viết sau cùng, `requires_ext` L00 → FND:L04, FND:L05; L05 → FND:L06; L08 → FND:L04); `labs/PYT/L00…L13`; `lessons/pyt/*.yaml`.

## Phát âm
Probe p1 (`audit/pyt/probes/p1.md`; small + medium, 4 ngữ cảnh, GPU; 10 ô edge-tts «không có âm thanh» tính là trượt): Python «Phai-thơn» 7/8 (đối chứng «Bát-cô» 0/8) → luật trong `lexicon_vi.PYT.yaml`; numpy ≤ 3/8, pandas ≤ 4/8, matplotlib 0/8, pytest ≤ 1/8, mọi cách viết khác của Python ≤ 5/8 → KHÔNG đọc: lời đọc nói «thư viện tính trên mảng / bảng dữ liệu / vẽ biểu đồ / kiểm thử», tên gốc chỉ hiện trên màn hình. `gen.py` từ chối lời đọc có từ khoá/tên hàm tiếng Anh của Python (if, for, self, test, UTF…); không đọc tên lệnh (grep, curl…).

## Điều chưa nhét được / giới hạn (trung thực)
1. **Không có kiểm tai người; ASR chưa chạy** (đúng yêu cầu: không build/tts/asr). «Phai-thơn» chỉ có bằng chứng ASR 7/8.
2. **pdb/`breakpoint()`** (L07) chỉ mô tả bằng bảng lệnh, không có đầu ra chạy thật trên màn hình: đầu ra của `python -m pdb` chứa đường dẫn tuyệt đối viết thường, không ổn định.
3. **Số thời gian/bộ nhớ là số minh hoạ đo trên máy kiểm đang tải** (có lúc chậm 4–5 lần); `verify_pyt` chỉ buộc cùng bậc độ lớn (×/÷ 8). Số bộ nhớ ngoại suy 10^8 là tuyến tính. L05/L13 phải đo lại vì lần đầu đo thời gian khi `tracemalloc` đang bật làm thời gian phình 20–40 lần (đã tách hai lượt đo).
4. **`lab_gate` chạy lab dùng thư viện bằng python trong PATH** (có numpy/pandas/matplotlib bản khác bản ghim) chứ không phải `labs/.venv-pyt`, vì `labs/cham.sh` chỉ chuyển sang venv khi python hệ thống thiếu thư viện. Vì vậy lab L08 chỉ in số phiên bản CHÍNH (3/2/3/9) thay vì `==` đầy đủ; các lab L09–L11 chỉ in số làm tròn, độ lệch giữa phiên bản không đổi kết quả (đã PASS). Đề nghị người điều phối sửa `cham.sh` ưu tiên `labs/.venv-pyt` khi có.
5. **Lab L08/L09–L13 cần `pip install -r labs/requirements-py.txt` (mạng)**; bước `pip install` của L08 không chạy trong video (không có mạng ổn định), kết quả của nó là cái bài tự làm kiểm.
6. Một số nguồn trích **theo trí nhớ, chưa mở lại** (ghi NOT_VERIFIED trong `source`): Gamma et al. 1994 (ưu tiên hợp thành, L06), Tufte 1983 (cột bắt đầu từ 0, L11), Simpson 1951 (đảo kết luận khi gộp, L11), Myers 1979 (giá trị biên, L12); OWASP ReDoS (L04) chỉ nêu khái niệm. Mọi số tiền là số minh hoạ; tình huống L13 là giả định minh hoạ, không phải sự cố có thật.
7. Python 3.11 và 3.13 cho đầu ra giống hệt ở mọi chương trình thư viện chuẩn; chỉ một khác biệt đã gặp và tránh: tệp tên `traceback.py` làm 3.13 nạp chính nó (đó cũng là ví dụ «trùng tên thư viện chuẩn» của L08).
8. Mục tiêu hứa-và-dạy: động từ LÀM được ánh xạ tới cảnh `example/formula/check/practice`; vài mục tiêu «Nêu…» ánh xạ tới `scale`, `quiz`, `pitfalls`, `intuition`.

## Việc còn lại cho người điều phối (ngoài phạm vi được sửa)
- `pack.py STAGES` / `curriculum/tracks.yaml`: thêm PYT sau FND (Chặng 0–1, trước các khoá dùng Python); `check_next_refs.py` hiện FAIL do `S03` (không do PYT).
- `curriculum/bnx.yaml` (và PLC, SDP, ESY, DSC, AIF, LLM, MLP…): thêm `requires_ext` trỏ PYT (BNX L00–L01 dùng f-string, `re`, comprehension, JSON → `PYT:L04`, `PYT:L05`, `PYT:L03`).
- `audit/verify_plan_curricula.py`: chưa có dòng `PYT:Lxx` nên `example` của `curriculum/pyt.yaml` không gắn «(VER PYT:Lxx)».
- Sổ `screen_code` cho PYT (tác tử không tạo theo hợp đồng).
- Dựng (build/tts/asr) chưa làm; sau dựng cần `asr` rà các câu có số dài và «Phai-thơn».
- `labs/cham.sh`: ưu tiên `labs/.venv-pyt` (xem mục 4 ở trên).
