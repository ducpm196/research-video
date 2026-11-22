# Báo cáo kiểm định ĐỘC LẬP 100% — Khoá Stage 11 BCH (`L00–L12`, 13 bài) theo chuẩn AF4

## 1. Kết luận: **NO-GO**
Toàn khoá **đạt 13/13 về toán học/mật mã lõi, `checks`, `verify_bch.py` (13/13 PASS), `spec_sha256 == lv.spec_digest`, `SRT == say`, và hiển thị PNG (0 lỗi đè chữ/cắt khung/KaTeX)**, nhưng **KHÔNG ĐẠT chuẩn AF4** do lỗi hệ thống trên cả 13 bài:
1. **P1=0 ở 13/13 bài**: không dạy Python/bash trước khi dùng trong `practice` và `labs/BCH/L*/de.md`; 10/13 bảng `practice#0` thiếu phần lớn cú pháp thực dùng ở `practice#1` (3 bài `L01, L02, L08` không có bảng `practice#0`); ngoài ra thân bài còn sót thuật ngữ/ký hiệu chưa giảng (`ms`, `bit`, `SHA`, `RFC 6962`, `0x00`/`0x01`, `đường cong elip`, `e`, `Poisson`, `RAM`, `GB`, `TWh`).
2. **P8<2 ở 13/13 bài**: 10/13 bài (`L00, L03, L04, L05, L06, L07, L09, L10, L11, L12`) **lộ nguyên văn `loi_giai.py` (`practice#1`) và `mong_doi.txt` (`practice#2`) TRƯỚC `pause: 30` (`practice#3`)**; 13/13 `labs/BCH/L*/de.md` không tự đứng được (thiếu định dạng `stdout` ở 13/13 bài; thiếu dữ liệu/công thức ở `L00, L01, L03, L04, L05, L08, L09, L10, L12`; trùng số ví dụ ở `L02, L04, L06, L07, L08, L09, L10, L12`; lộ đáp án trên tiêu đề `de.md` ở `L06, L08, L10`).
3. **P9=0/1 ở 13/13 bài**: **0/13 bài** có `<p class="note"><b>Hai mức quy mô:</b>` ở `recap`.
4. **E51 `covers:` sai cảnh thực dạy ở 13/13 bài**: điền khuôn mẫu `1→example, 2→check, 3→practice` (L12: `1→stage1, 2→stage2, 3→practice`), trỏ sai cảnh thật dạy mục tiêu.
5. **Thời lượng & hạ tầng**: **6/13 bài dưới 9 phút** (`L00: 8.86p, L01: 7.82p, L02: 8.58p, L04: 8.51p, L08: 8.68p, L11: 8.99p`); `audit/layout_BCH.tsv` rỗng (2 byte); `audit/review/screen_code/BCH.yaml` gắn sai `kind: other, lang: text` cho 10/10 khối mã Python `practice 1 0`; `out/BCH/L*/xem.html` (13/13) cũ chưa cập nhật phân cảnh `practice`; 2 câu có `"càng "` trong `say` (`L08`, `L10`); 53 câu ASR còn `NOT_VERIFIED bằng tai người` (tập trung ở 8 bài).

---

## 2. Bảng tóm tắt tổng
| Hạng mục kiểm định | Kết quả | Chi tiết |
|---|---:|---|
| **MUST=0 (theo chuẩn AF4)** | **0/13** | Kiến thức toán/mật mã thuần đúng **13/13**, nhưng cả **13/13** mắc lỗi MUST AF4 (E51 `covers:` trỏ sai cảnh 13/13; lộ `loi_giai.py`+`mong_doi.txt` trước `pause: 30` ở 10/13; `de.md` không tự đứng được ở 13/13; 6/13 bài `< 9 phút`) |
| **P1 = 2 (chuẩn chặt)** | **0/13** | 0 bài đạt 2; 0 bài đạt 1; **13/13 bài đạt 0** (`≥ 3` mục chưa giảng nếu tính cả thân bài + `practice` + `de.md`) |
| **P8 = 2 (thực nghiệm)** | **0/13** | 0 bài đạt 2; **3/13 bài đạt 1** (`L01, L02, L08`: không lộ trước pause nhưng `de.md` thiếu dữ liệu/stdout/trùng số); **10/13 bài đạt 0** (lộ trước `pause: 30` + `de.md` thiếu) |
| **P9 = 2 (quy mô/thời gian)** | **0/13** | 0 bài đạt 2; **9/13 bài đạt 1** (`L02, L03, L05, L06, L07, L08, L10, L11, L12`); **4/13 bài đạt 0** (`L00, L01, L04, L09`); **0/13** có `<p class="note"><b>Hai mức quy mô:</b>` ở `recap` |
| **spec_sha256 == lv.spec_digest** | **13/13** | Mọi `out/BCH/L*/build_report.json` khớp 100% (`built_at`: `2026-11-20T06:51..07:20Z`), có `tts_sha256` |
| **L*.srt == say (từng câu)** | **13/13** | Khớp 100% mọi câu ở cả 13 bài |
| **ASR (`asr_report.md`)** | **13/13*** | `thiếu audio=0` và `chưa xem xét=0` ở 13/13 bài; nhưng **8/13 bài còn 53 câu `NOT_VERIFIED bằng tai người`** (`L01:3, L02:12, L03:6, L05:3, L06:3, L09:2, L10:10, L12:14`) |
| **checks & `verify_bch.py`** | **13/13** | `lv.lint` 0 lỗi, 0 cảnh báo trên 13/13 bài; `verify_bch.py` đạt `13/13 PASS` |
| **lab (`loi_giai.py` vs `mong_doi.txt`)** | **13/13*** | Chạy thật `.venv\Scripts\python.exe` khớp từng ký tự `mong_doi.txt` 13/13 bài; nhưng `de.md` thiếu dữ liệu/stdout ở 13/13 và `L09` không mô phỏng reentrancy thật |
| **Thời lượng (`≥ 9p`, trần `16p` trừ L12)** | **7/13** | Đạt: `L03, L05, L06, L07, L09, L10, L12 (journey 18.64p)`. Thiếu `< 9p`: `L00 (8.86p), L01 (7.82p), L02 (8.58p), L04 (8.51p), L08 (8.68p), L11 (8.99p)` |
| **SHOULD / Hạ tầng khác** | **13/13** | `layout_BCH.tsv` rỗng; `screen_code/BCH.yaml` sai `kind/lang` ở 10 khối `practice 1 0`; `xem.html` cũ ở 13/13; 2 câu `"càng "` (`L08, L10`); tiền tố `"Bài N — "` ở `title` khác `curriculum/bch.yaml` |

---

## 3. Bảng chi tiết 13 bài (`L00..L12`)
*(Ghi chú: Tổng = P1+P2+P3+P4+P5+P6+P7 trên thang 14; Mất gốc: ĐỦ ≥12 & không 0, GẦN 9–11 hoặc ≥12 có một mục 0, CHƯA ≤8)*

| Bài | sha16 lúc đọc | Phút | P1 | P2 | P3 | P4 | P5 | P6 | P7 | Tổng | P8 | P9 | Mất gốc | Chỗ thiếu chính (MUST / SHOULD / P1 / P8 / P9) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| **L00** | `7767a2991a75711c` | **8.86** | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | 0 | 0 | **GẦN** | `<9p`; lộ `loi_giai.py`+`mong_doi.txt` trước pause; `de.md` thiếu công thức/stdout & dùng `BFT`; `covers:` sai cả 3 mục tiêu; `practice#0` sai lệch mã; `ms` chưa giải; thiếu P9 |
| **L01** | `05848ac5be6ac4d4` | **7.82** | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | 1 | 0 | **GẦN** | `<9p`; thiếu bảng `practice#0`; `de.md` thiếu input (`"gen"`, `"tx1..3"`, `"FAKE"`, `\|`, `[:10]`) & stdout; `covers:` sai obj#2,#3; chưa giảng `bit`, `SHA`, Python; thiếu P9; 3 ASR NOT_VERIFIED |
| **L02** | `20b76d1f9f28ef6f` | **8.58** | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | 1 | 1 | **GẦN** | `<9p`; thiếu bảng `practice#0`; `de.md` trùng số ví dụ (`1024`/`320`) & thiếu stdout; `covers:` sai obj#1,#2,#3; chưa giảng `RFC 6962`, `0x00`/`0x01`, Python; thiếu `recap` P9; 12 ASR NOT_VERIFIED |
| **L03** | `a0b95275bdd910ca` | 10.04 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | 0 | 1 | **GẦN** | Lộ code+output trước pause; `de.md` thiếu `m=42`, `99`, stdout; `covers:` sai obj#3; `practice#0` thiếu `=`, `pow`, `==`, `int`; chưa giảng `RSA`, `tx`, `đường cong elip`, `≡`; thiếu `recap` P9; 6 ASR NOT_VERIFIED |
| **L04** | `c81e721b77b5184c` | **8.51** | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | 0 | 0 | **GẦN** | `<9p`; lộ code+output trước pause; `de.md` trùng số ví dụ & thiếu input xu/stdout; `covers:` sai obj#3; chưa giảng `UTXO`, `[500,300]`, `;`, `:.1f`; thiếu P9 |
| **L05** | `81240a5462b95544` | 9.88 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | 0 | 1 | **GẦN** | Lộ code+output trước pause; `de.md` thiếu `"blk1:{nonce}"` & stdout; `covers:` sai obj#3; chưa giảng hằng số `e`, `PoW`, `hex`, `while/break/+=`, `hashlib`, `[:6]`; thiếu `recap` P9; 3 ASR NOT_VERIFIED |
| **L06** | `f108f33926225636` | 12.33 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | 0 | 1 | **GẦN** | Lộ code+output trước pause; `de.md` trùng số ví dụ, lộ kết quả trên tiêu đề, thiếu stdout; `covers:` sai obj#1,#3; chưa giảng `Poisson`, `e`, `;`, `**`, `math.exp/factorial`; thiếu `recap` P9; 3 ASR NOT_VERIFIED |
| **L07** | `3a8a5f0ef0a9cc10` | 9.49 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | 0 | 1 | **GẦN** | Lộ code+output trước pause; `de.md` trùng `N=100` & thiếu stdout; `covers:` sai obj#3; chưa giảng `BFT`, `Proof of Stake`, `validator`, `//`, `;`; thiếu `recap` P9 |
| **L08** | `583cb4a308a5a8f7` | **8.68** | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | 1 | 1 | **GẦN** | `<9p`; thiếu bảng `practice#0`; `de.md` trùng ví dụ (`21000×20`), lộ đáp án trên tiêu đề, thiếu stdout; `covers:` sai obj#1,#2,#3; câu `"càng "` ở `example.3`; chưa giảng `Ethereum`, `21_000`, `1e-9`; thiếu `recap` P9 |
| **L09** | `196e0929049c0dee` | 9.67 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | 0 | 0 | **GẦN** | Lộ code+output trước pause; `de.md` trùng số & thiếu `bal=1`/stdout; `loi_giai.py` không mô phỏng callback gọi lại; `covers:` sai obj#2,#3; chưa giảng `Reentrancy`, `Checks-Effects-Interactions`, `-=`, `>=`; thiếu P9; 2 ASR NOT_VERIFIED |
| **L10** | `93581fb333ec7467` | 9.28 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | 0 | 1 | **GẦN** | Lộ code+output trước pause; `de.md` trùng số, lộ `~6.7 TPS` ở tiêu đề, thiếu `250 B` ở thân & stdout; `covers:` sai obj#2,#3; câu `"càng "` ở `prereq.2`; chưa giảng `Layer-1`, `tx`, `B`, `TPS`, `1_000_000`, `:.2f`; thiếu `recap` P9; 10 ASR NOT_VERIFIED |
| **L11** | `b788ff07bafae048` | **8.99** | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | 0 | 1 | **GẦN** | `<9p` (539.5s); lộ code+output trước pause; `de.md` thiếu stdout; `covers:` sai obj#1,#3; chưa giảng `sorted`, `[...]`, `//`, `<=`, `int(...)`; thiếu `recap` P9 |
| **L12** | `62b783ea47988c14` | 18.64 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | 0 | 1 | **GẦN** | Lộ code+output trước pause; `de.md` trùng ví dụ chặng 1, hứa "so với dữ liệu đầy khối" nhưng `loi_giai.py` không làm, thiếu stdout; `covers:` sai cả 3 mục tiêu; chưa giảng `RAM`, `GB`, `TWh`, `header`, `80B`, `1e6`, `:.2f`; thiếu `recap` P9; 14 ASR NOT_VERIFIED |

*(Ghi chú thêm: `L07` sha16 = `3a8a5f0ef0a9cc10`, đã kiểm trực tiếp từ file `lessons/bch/L07_bang_chung_co_phan.yaml`)*

---

## 4. Chi tiết `MUST` / `SHOULD` / `INFO` (trích nguyên văn, đường dẫn & số dòng)

### A. Lỗi `MUST` (chặn phát hành AF4)
1. **E51 `covers:` trỏ sai cảnh thực dạy ở 13/13 bài (`L00..L12`)**:
   - Toàn khoá dùng mẫu cứng `1→example, 2→check, 3→practice` (`L12`: `1→stage1, 2→stage2, 3→practice`) bất kể mục tiêu nói gì:
     - `lessons/bch/L00_so_cai_phan_tan.yaml:268-274`: objective 1 (`"Phát biểu bài toán chi tiêu hai lần..."`) trỏ `scene: example` (dạy 4 câu hỏi quyết định, không dạy double-spend); objective 2 (`"Dùng câu hỏi quyết định..."`) trỏ `scene: check` (đếm $2^4=16$); objective 3 (`"Biết chuỗi khối không làm dữ liệu đúng"`) trỏ `scene: practice` (tính `bft_quorum_4`, nội dung "dữ liệu đúng" nằm ở `pitfalls#0` dòng 170).
     - `L01:258-264`: obj#3 (`"Hiểu liên kết băm phát hiện chứ không ngăn sửa"`) trỏ `practice` thay vì `pitfalls` (dòng 176).
     - `L02:274-280`: obj#1 (`"Dựng cây Merkle"`) trỏ `example` (kiểm tx 357), obj#2 (`"Kiểm một giao dịch..."`) trỏ `check` (dựng gốc), obj#3 (`"Biết bằng chứng chỉ có giá trị khi gốc đáng tin"`) trỏ `practice` thay vì `pitfalls` (dòng 188).
     - `L03:292-298`: obj#3 (`"Giải thích địa chỉ là băm của khoá công khai"`) trỏ `practice` (chỉ ký/kiểm `m=42`, không đả động địa chỉ; địa chỉ ở `sym` dòng 88 & `quiz` dòng 238).
     - `L04:272-278`: obj#3 (`"So sánh với mô hình số dư tài khoản"`) trỏ `practice` (chỉ tính tiền thừa UTXO; so sánh ở `sym` dòng 68).
     - `L05:297-303`: obj#3 (`"Hiểu tính ngẫu nhiên của thời gian tìm khối"`) trỏ `practice` (đào 1 khối `'00'`, không dạy phân phối ngẫu nhiên; ở `example` bước 4 dòng 160 & `pitfalls` dòng 205).
     - `L06:330-336`: obj#1 trỏ `example`, obj#3 (`"Chọn số xác nhận theo giá trị giao dịch"`) trỏ `practice` (ở `pitfalls` dòng 239).
     - `L07:273-279`: obj#3 (`"So sánh tính cuối cùng xác suất và tính cuối cùng tất định"`) trỏ `practice` (chỉ tính `f=33, quorum=67`; so sánh ở `prereq` dòng 44 & `pitfalls` dòng 174).
     - `L08:256-262`: obj#1 (`"Mô hình hoá hợp đồng như máy trạng thái"`) trỏ `example` (chỉ tính phí gas; máy trạng thái ở `sym` dòng 71 & `intuition` dòng 89); obj#3 (`"Biết vì sao hợp đồng phải tất định"`) trỏ `practice` (ở `sym` dòng 72 & `pitfalls` dòng 161).
     - `L09:284-290`: obj#2 trỏ `check` (đếm `d*(q//d)` trên bản lỗi), obj#3 (`"Nhận ra lỗi tràn số và lỗi thiếu kiểm quyền"`) trỏ `practice` (chỉ trừ `bal -= 1`, không hề có tràn số hay kiểm quyền; ở `pitfalls` dòng 174, 181 & `quiz` dòng 206).
     - `L10:291-297`: obj#2 (`"Giải thích ý tưởng xử lý ngoài chuỗi..."`) trỏ `check` (đếm 576 000 tx/ngày), obj#3 (`"Thấy đánh đổi giữa thông lượng và phi tập trung"`) trỏ `practice` (tính TPS `6.67`; đánh đổi ở `pitfalls` dòng 199).
     - `L11:255-261`: obj#1 trỏ `example`, obj#3 (`"Nêu hệ quả quyền riêng tư của sổ cái công khai"`) trỏ `practice` (chỉ tính trung vị; quyền riêng tư ở `pitfalls` dòng 164, 169).
     - `L12:559-565`: obj#1 (`"...qua năm chặng..."`) trỏ `stage1` (chỉ chặng 1); obj#2 (`"Tính lại dung lượng tiêu đề..., trọng lượng..., ngưỡng tín hiệu, số ngày chạy song song và độ dài một kỷ nguyên"`) trỏ `stage2` (chỉ trọng lượng); obj#3 (`"Chọn cách nâng cấp hợp với quy mô mạng..."`) trỏ `practice` (chỉ tính tiêu đề 2008; lựa chọn theo quy mô nằm ở `quiz` dòng 464–514).

2. **P8 — Lộ nguyên văn `loi_giai.py` và `mong_doi.txt` TRƯỚC `pause: 30` ở 10/13 bài**:
   - Ở cả 10 bài `L00, L03, L04, L05, L06, L07, L09, L10, L11, L12`, `practice#1` in nguyên mã `loi_giai.py` dưới tiêu đề `"Cài đặt kiểm chứng BCH:Lxx bằng Python"`, và `practice#2` in nguyên `mong_doi.txt` dưới tiêu đề `"Đầu ra chạy thật (1 dòng)"`, trước khi tới `practice#3` (`pause: 30`):
     - `L00:232-245`, `L03:256-269`, `L04:236-249`, `L05:261-274`, `L06:294-307`, `L07:237-250`, `L09:248-261`, `L10:255-268`, `L11:219-232`, `L12:523-536`.

3. **P8 — `labs/BCH/L*/de.md` không tự đứng được ở 13/13 bài**:
   - **13/13 `de.md` thiếu định dạng `stdout`** (tên khoá `key=value`, thứ tự, dấu cách, số chữ số thập phân) nên người học tự đọc `de.md` không thể qua được bài chấm tự động.
   - **Thiếu dữ liệu đầu vào / công thức**:
     - `labs/BCH/L00/de.md:3`: `"So sánh chi phí 1 nút trung gian tin cậy với cần xác nhận đa số BFT giữa n=4 bên độc lập."` → thiếu công thức `(2 * n // 3) + 1`, hơn nữa `BFT` chưa học ở L00 (L07 mới dạy, và L07 dùng `n - (n-1)//3` chứ không dùng `2*4//3 + 1`).
     - `labs/BCH/L01/de.md:3`: `"Dùng hashlib.sha256 tạo chuỗi 4 khối rồi sửa khối 3..."` → thiếu chuỗi đầu vào (`"gen"`, `"tx1"`, `"tx2"`, `"tx3"`, `"FAKE"`), dấu nối `"|"`, cắt `[:10]`.
     - `labs/BCH/L03/de.md:3`: thiếu `m = 42` và giá trị sửa `99` (trong `loi_giai.py:2,5`).
     - `labs/BCH/L04/de.md:1,3`: chỉ ghi `"đầu vào 5 + 3 = 8, trả 6, phí 0.1 -> tiền thừa 1.9"` trên tiêu đề; thân đề không cho số xu `[500, 300], 600, 10`.
     - `labs/BCH/L05/de.md:3`: thiếu chuỗi tiền tố `"blk1:{nonce}"` (`loi_giai.py:4`).
     - `labs/BCH/L06/de.md:1`, `L08/de.md:1`, `L10/de.md:1`: **lộ đáp án ngay trong tiêu đề `# Lab...`** (`≈ 0.00024`, `= 0.00042 ETH`, `-> ~6.7 TPS`), thân `L08/de.md:3` và `L10/de.md:3` thiếu tham số đầu vào (`21 000, 20`; `250 B`).
     - `labs/BCH/L09/de.md:3`: thiếu số tiền gửi `bal = 1`; và `labs/BCH/L09/loi_giai.py:1-7` chỉ viết `bal -= 1; vault -= 1` trong 1 hàm tuần tự, không mô phỏng hàm/đối tượng gọi lại.
     - `labs/BCH/L12/de.md:3`: hứa `"và so với dữ liệu đầy khối"` nhưng `labs/BCH/L12/loi_giai.py:1-3` KHÔNG tính phép so sánh đó.
   - **Trùng số ví dụ trong bài**: `L02, L04, L06, L07, L08, L09, L10, L12` (8/13 bài).

4. **P1=0 ở 13/13 bài** (chi tiết từng mục ở Mục 5 bên dưới).

5. **Thời lượng `< 9 phút` ở 6/13 bài** (`out/BCH/L*/build_report.json` & `_frames.txt`):
   - `L00`: `531.3s = 8.86p`
   - `L01`: `469.3s = 7.82p`
   - `L02`: `514.6s = 8.58p`
   - `L04`: `510.3s = 8.51p`
   - `L08`: `520.5s = 8.68p`
   - `L11`: `539.5s = 8.99p`

---

### B. Lỗi `SHOULD`
1. **P9 thiếu ở cả 13/13 bài (`recap` không có `<p class="note"><b>Hai mức quy mô:</b>`)**; ngoài ra 4 bài (`L00, L01, L04, L09`) chưa có 2 mức quy mô kèm định lượng + đánh đổi ngay trong thân bài.
2. **Hạ tầng kiểm định `audit/layout_BCH.tsv` và `audit/review/screen_code/BCH.yaml`**:
   - `D:\research-video\audit\layout_BCH.tsv`: rỗng (`2` byte, không có dữ liệu layout của 13 bài).
   - `D:\research-video\audit\review\screen_code\BCH.yaml`: cả **10/10** khối mã Python thật `BCH Lxx practice 1 0` (`L00, L03, L04, L05, L06, L07, L09, L10, L11, L12` — dòng `117, 204, 222, 240, 258, 276, 309, 327, 345, 363`) đều bị gắn sai `kind: other`, `lang: text`, `reason: Đầu ra mong đợi chính xác của lab...`.
3. **Trang `out/BCH/L*/xem.html` lỗi thời ở 13/13 bài**: thiếu phân cảnh `practice` trong mục lục và ghi `Thời lượng` cũ ngắn hơn video `L*.mp4` hiện tại (ví dụ `out/BCH/L00/xem.html:25,27` ghi `Thời lượng 7:42`, thực tế `531.3s = 8:51`).
4. **Cụm `"càng "` trong `say` (2 chỗ)**:
   - `lessons/bch/L08_hop_dong_thong_minh.yaml:132` (`example.3`): `"nên mã càng ghi ít thì phí càng thấp."`
   - `lessons/bch/L10_mo_rong.yaml:92` (`prereq.2`): `"và truyền càng lâu thì càng dễ có hai khối ra cùng lúc, tạo nhánh như ở bài 6."`
5. **53 câu ASR còn `NOT_VERIFIED bằng tai người`** trong `out/BCH/L*/asr_report.md` (`L01:3, L02:12, L03:6, L05:3, L06:3, L09:2, L10:10, L12:14`; chủ yếu do đọc thô `byte` → `"bay/bai"`, `Merkle` → `"mơ cổ"`, chữ cái riêng `s/d/e/z/k/p`, `lôgarit`).
6. **Không nhất quán `title` với `curriculum/bch.yaml`**: 13/13 spec thêm tiền tố `'Bài N — '` so với `curriculum/bch.yaml` (ví dụ `L00:4` vs `curriculum/bch.yaml:14`).

### C. Ghi nhận `INFO` (đã đạt)
- **Toán học, mật mã, chuỗi khối & nguồn `L12`**: 13/13 `verify_bch.py` PASS; mọi `checks` trong YAML đều chạy ra `True` (0 lỗi, 0 cảnh báo từ `lv.lint`); mọi con số và khẳng định trong `L12` khớp nguyên văn nguồn `[N08], [B141], [B9], [B91], [BC16], [BC17], [E22], [E22e], [E22p], [E25], [CS]` trong `audit/bch/sources_L12.md`.
- **Đồng bộ dựng video**: 13/13 `build_report.json` có `spec_sha256 == lv.spec_digest`, `L*.srt == say` từng câu, `asr_report.md` có `thiếu audio=0, chưa xem xét=0`.
- **Chính tả `SPELL_CANON` & LaTeX trong `say`**: 0 lỗi `SPELL_CANON`, 0 công thức LaTeX thô trong `say`.
- **Hiển thị PNG**: 42/42 khung hình đã đọc trực tiếp rõ nét, tương phản tốt, KaTeX sắc nét, không đè chữ, không cắt khung.

---

## 5. Kiểm chuẩn P1 nghiêm ngặt — Mục chưa giảng & Bảng phủ `practice#0`

### A. Từng mục chưa giảng theo từng bài (Thân bài + `practice` + `de.md`)
*(Cột cuối: bảng `practice#0` có phủ không)*

| Bài | Cảnh / Tệp:dòng | Trích chữ / Ký hiệu chưa giảng | Thuộc bảng `practice#0`? | Bảng `practice#0` có phủ không? |
|---|---|---|---|---|
| **L00** | `prereq.2` (`L00:57-60`) | `ms` (`0 ms`, `10 ms` — màn hình viết `ms`, không chú thích = mi-li-giây) | Không | N/A |
| **L00** | `practice.1` (`L00:232`) | `=` (gán biến), `//` (chia lấy nguyên), `f"...{var}"` (chèn biến không có `:.3f`) | Có trong mã `practice#1` | **KHÔNG** (`practice#0` chỉ có `f"{val:.3f}"`, `print(...)`) |
| **L00** | `practice.3` (`L00:238`), `L00/de.md:3,7` | `BFT`, `n=4`, `bash labs/cham.sh ... .py` | Lệnh/đề | **KHÔNG** |
| **L01** | `prereq.1` (`L01:57`) | `bit` (`4 bit`, `256 bit` — dùng đơn vị `bit` mà không giảng `bit` là gì) | Không | N/A |
| **L01** | `sym.0` (`L01:70-71`) | `SHA` trong `SHA-256`; chỉ số mảng `mã[i]` | Không | N/A |
| **L01** | `practice.0` (`L01:228`), `L01/de.md:3,7`, `loi_giai.py:1-6` | `hashlib.sha256`, `bash`, `import`, `lambda`, `.encode()`, `.hexdigest()`, `[:10]`, `for...range`, `.append()`, `!=`, `int(...)`, `f"{...}"`, `print` | Bài **không có bảng `practice#0`** | **KHÔNG** |
| **L02** | `pitfalls.1` (`L02:193`) | `RFC 6962` (`RFC`), tiền tố hex `0x00`, `0x01` | Không | N/A |
| **L02** | `practice.0` (`L02:244`), `L02/de.md:3,7`, `loi_giai.py:1-4` | `log2(1024)`, `bash`, `import math`, `math.log2`, `int(...)`, `f"{...}"`, `print` | Bài **không có bảng `practice#0`** | **KHÔNG** |
| **L03** | `example.0` (`L03:118`), `quiz.1` (`L03:229`) | `đường cong elip` (chỉ nhắc tên), phép đồng dư `≡ ... (mod n)` (chưa định nghĩa rõ nghĩa `≡`) | Không | N/A |
| **L03** | `practice.1` (`L03:256`), `practice.3`, `L03/de.md:1,3,7` | `n, e, d = ...`, `# comment`, `tx`, `pow(m, d, n)`, `==`, `int(...)`, `f"{...}"`, `RSA`, `bash` | Có trong mã/đề | **KHÔNG** (`practice#0` chỉ có `f"{val:.3f}"`, `print`) |
| **L04** | `practice.1` (`L04:236`), `practice.3`, `L04/de.md:1,3,7` | `[500, 300]`, `;` (hai lệnh 1 dòng), `f"{...:.1f}"` (bảng ghi `.3f`), `UTXO`, `->`, `bash` | Có trong mã/đề | **KHÔNG** (`practice#0` thiếu list, `;`, `:.1f`) |
| **L05** | `example.4` (`L05:169`), `check.1` (`L05:193`), `quiz.0` (`L05:227`) | Hằng số `e` (`1/e ≈ 0,368`, `e^{-2}`, `e^{-x}` — chưa bao giờ giảng `e ≈ 2,718`) | Không | N/A |
| **L05** | `practice.1` (`L05:261`), `practice.3`, `L05/de.md:1,3,7` | `while True:`, `break`, `+=`, `hashlib.sha256(...).encode().hexdigest()`, `.startswith()`, `d[:6]`, `f"{...}"`, `PoW`, `hex`, `bash` | Có trong mã/đề | **KHÔNG** (`practice#0` chỉ có `import`, `if`, `:.3f`, `print`) |
| **L06** | `sym.0` (`L06:100`) | `phân phối Poisson`, hằng số `e` (`e^{-\lambda}`) | Không | N/A |
| **L06** | `practice.1` (`L06:294`), `practice.3`, `L06/de.md:7` | `print(...)` (thiếu ngay cả `print`!), `;`, `range(...)`, `math.exp`, `math.factorial`, `**`, `-=`, `:.6f`, `:.4f`, `bash` | Có trong mã/đề | **KHÔNG** (`practice#0` chỉ có `def`, `import`, `for`, `:.3f`) |
| **L07** | `practice.1` (`L07:237`), `practice.3`, `L07/de.md:1,3,7` | `//`, `;`, `f"{...}"`, `BFT`, `Proof of Stake`, `validator`, `N`, `(N-1)//3`, `bash` | Có trong mã/đề | **KHÔNG** (`practice#0` chỉ có `:.3f`, `print`) |
| **L08** | `practice.0` (`L08:226`), `L08/de.md:3,7`, `loi_giai.py:1-3` | `Ethereum`, `bash`, `gas, gwei = 21_000, 20`, `1e-9`, `f"{...:.5f}"`, `print` | Bài **không có bảng `practice#0`** | **KHÔNG** |
| **L09** | `practice.1` (`L09:248`), `practice.3`, `L09/de.md:1,7` | `vault, bal = 10, 1`, `>=`, `-=`, `# Effects / Interactions / fail`, `f"{...}"`, `Reentrancy`, `Checks-Effects-Interactions`, `bash` | Có trong mã/đề | **KHÔNG** (`practice#0` chỉ có `def`, `if`, `:.3f`, `print`) |
| **L10** | `practice.1` (`L10:255`), `practice.3`, `L10/de.md:1,7` | `1_000_000`, `f"{tps:.2f}"`, `Layer-1`, `tx`, `B`, `TPS`, `bash` | Có trong mã/đề | **KHÔNG** (`practice#0` chỉ có `:.3f`, `print`) |
| **L11** | `practice.1` (`L11:219`), `practice.3`, `L11/de.md:3,7` | `sorted([...])`, `vals[len(vals) // 2]`, `int(100 <= med <= 103)`, `f"{...}"`, `[100..103]`, `bash` | Có trong mã/đề | **KHÔNG** (`practice#0` chỉ có `:.3f`, `sum/len/max/min`, `print`) |
| **L12** | `stage1.1` (`L12:187`), `stage4.2` (`L12:338`) | `RAM`, `GB` (`RAM 2 GB`), `TWh` (`21 TWh`, `0,0026 TWh` — `say` đọc "tỉ số điện" nhưng màn hình không giải `TWh`) | Không | N/A |
| **L12** | `practice.1` (`L12:523`), `practice.3`, `L12/de.md:1,3,7` | `1e6`, `f"{...:.2f}"`, `80B`, `header`, `bash` | Có trong mã/đề | **KHÔNG** (`practice#0` chỉ có `:.3f`, `print`) |

### B. Tóm tắt bảng phủ `practice#0` trên 13 bài
- **3/13 bài (`L01, L02, L08`)**: KHÔNG có bước `practice#0` giải thích cú pháp.
- **10/13 bài còn lại**: dùng 4 mẫu bảng `practice#0` sao chép chung toàn kho (nên đều có dòng thừa `f"{val:.3f}"` không dùng trong mã!), **0/10 bảng phủ hết cú pháp của `practice#1`** (thiếu `=`, `//`, `;`, `[...]`, `**`, `+=`, `-=`, `==`, `>=`, `<=`, `while/break`, `range`, `pow`, `sorted`, `int`, `hashlib`, `.encode()`, `.hexdigest()`, `.startswith()`, `[:k]`, `1_000_000`, `1e-9`, `:.1f/.2f/.4f/.5f/.6f`, và thậm chí `L06 practice#0` thiếu cả `print(...)`).

---

## 6. Danh sách 42 ảnh PNG đã mở xem trực tiếp bằng `read_file`
1. `D:\research-video\out\BCH\L00\frames\00022.png` (SVG), `00067.png` (practice code), `00073.png` (recap)
2. `D:\research-video\out\BCH\L01\frames\00019.png` (SVG), `00062.png` (practice), `00066.png` (recap)
3. `D:\research-video\out\BCH\L02\frames\00018.png` (SVG), `00061.png` (practice), `00065.png` (recap)
4. `D:\research-video\out\BCH\L03\frames\00019.png` (SVG), `00070.png` (practice code), `00076.png` (recap)
5. `D:\research-video\out\BCH\L04\frames\00017.png` (SVG), `00066.png` (practice code), `00072.png` (recap)
6. `D:\research-video\out\BCH\L05\frames\00028.png` (SVG), `00038.png` (KaTeX example), `00071.png` (practice code), `00077.png` (recap)
7. `D:\research-video\out\BCH\L06\frames\00024.png` (KaTeX sym), `00032.png` (SVG), `00080.png` (quiz), `00092.png` (practice code), `00099.png` (KaTeX recap)
8. `D:\research-video\out\BCH\L07\frames\00021.png` (KaTeX sym), `00022.png` (SVG), `00065.png` (practice code), `00071.png` (recap)
9. `D:\research-video\out\BCH\L08\frames\00021.png` (SVG), `00066.png` (practice), `00070.png` (recap)
10. `D:\research-video\out\BCH\L09\frames\00021.png` (SVG), `00074.png` (practice code), `00080.png` (recap)
11. `D:\research-video\out\BCH\L10\frames\00026.png` (SVG), `00067.png` (practice code), `00073.png` (recap)
12. `D:\research-video\out\BCH\L11\frames\00019.png` (SVG), `00064.png` (practice code), `00070.png` (recap)
13. `D:\research-video\out\BCH\L12\frames\00019.png` (SVG trục thời gian), `00023.png` (SVG tách chữ ký), `00073.png` (chặng 4), `00123.png` (quiz), `00141.png` (practice code), `00147.png` (recap)

---

## 7. Người học kẹt ở đâu (góc nhìn người mất gốc từ số 0)
- **L00**: `prereq.2` (`L00:57`) thấy đơn vị `ms` không rõ nghĩa; sang `practice.1` (`L00:232`) gặp `=` và `//` chưa học, rồi `de.md:3` hỏi `"đa số BFT"` chưa từng dạy trong bài và không cho công thức hay định dạng `stdout`.
- **L01**: `prereq.1` (`L01:57`) gặp `bit` và `sym.0` (`L01:70-71`) gặp `SHA-256`, `mã[i]` chưa giảng; sang `practice.0` & `de.md:3` bị bảo mở Python dùng `hashlib.sha256` nhưng bài không dạy dòng Python nào và `de.md` không cho chuỗi đầu vào hay định dạng `stdout`.
- **L02**: `pitfalls.1` (`L02:193`) gặp `0x00`, `0x01`, `RFC 6962` chưa giải thích; sang `practice.0` & `de.md:3` không biết viết Python `math.log2` và định dạng `stdout` ra sao vì không có bảng hướng dẫn mã.
- **L03**: `quiz.1` (`L03:229`) gặp ký hiệu đồng dư `(h^d)^e ≡ h (mod n)` lần đầu mà không giải thích nghĩa dấu `≡`; sang `practice.1–3` & `de.md` gặp `RSA`, `tx`, `pow(m, d, n)` và `m=42, 99` không có trong đề.
- **L04**: `practice.1–3` & `de.md:1,3` gặp `UTXO`, cú pháp list `[500, 300]`, `;` nối lệnh, `:.1f` (khác `:.3f` trong bảng), và `de.md` thiếu định dạng `stdout`.
- **L05**: `example.4` (`L05:169`) thấy `1/e ≈ 0,368` mà không biết `e` là số gì; sang `practice.1–3` & `de.md` gặp `PoW`, `hex`, `while True:`, `hashlib`, `.startswith("00")`, `[:6]` và chuỗi `"blk1:"` không ghi trong `de.md`.
- **L06**: `sym.0` (`L06:100`) gặp `phân phối Poisson` và `e^{-\lambda}` không giải thích; sang `practice.1` gặp `;`, `**`, `-=`, `math.exp`, `math.factorial`, `print` (ngay cả `print` cũng thiếu trong `practice#0`).
- **L07**: `practice.1–3` & `de.md` gặp `BFT`, `Proof of Stake`, `validator`, `//`, `;` chưa từng xuất hiện trong thân bài, và `de.md` thiếu định dạng `stdout`.
- **L08**: `practice.0` & `de.md:3` gặp `Ethereum` và phải tự code Python (`21_000`, `1e-9`, `:.5f`) mà không có bảng `practice#0` hay định dạng `stdout`.
- **L09**: `practice.1–3` & `de.md:1,3` gặp `Reentrancy`, `Checks-Effects-Interactions`, `vault, bal = 10, 1`, `>=`, `-=` chưa giảng; hơn nữa `de.md` thiếu `bal=1` và `loi_giai.py` không mô phỏng gọi lại thật.
- **L10**: `practice.1–3` & `de.md:1,3` gặp `Layer-1`, `tx`, `B`, `TPS`, `1_000_000`, `:.2f` chưa giảng; thân `de.md` thiếu kích thước giao dịch `250 B` và định dạng `stdout`.
- **L11**: `practice.1` (`L11:219`) gặp `sorted([...])`, `vals[len(vals) // 2]`, `int(100 <= med <= 103)` không có trong bảng `practice#0`, và `de.md` thiếu định dạng `stdout`.
- **L12**: `stage1.1` (`L12:187`) gặp `RAM 2 GB` và `stage4.2` (`L12:338`) gặp `TWh` chưa giải thích; sang `practice.1–3` & `de.md:3` gặp `header`, `80B`, `1e6`, `:.2f` và `de.md` yêu cầu "so với dữ liệu đầy khối" nhưng không có trong bài giải hay định dạng `stdout`.
