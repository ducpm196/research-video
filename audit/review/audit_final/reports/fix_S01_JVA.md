# fix_S01 JVA: sửa khoá JVA (13 bài L00–L12) theo báo cáo người đọc S01 (2026-11-13)

Nguồn sửa: `audit/jva/src/l00.py … l12.py`, `audit/jva/lib.py` (thêm `code_block(..., keep_indent=True)`), `tools/registry/symbols.JVA.yaml` (4 mục sổ thuật ngữ E52), `curriculum/jva.yaml` (2 mục tiêu đồng bộ). Các tệp `lessons/jva/*.yaml`, `labs/JVA/L11`, `L12`, `L08` do `gen.py` sinh lại; không sửa YAML bằng tay. Không chạy build/tts/asr/audit_all/git/docker.

## 1. MUST / SHOULD

MUST: 0 (báo cáo S01 không có MUST; không có gì để kiểm lại).

SHOULD: 12/12 mục báo cáo đã xử lý (11 sửa hết, 1 sửa một phần: L09 mục c).

| # | Bài | Mục | Cách sửa | Kiểm |
|---|---|---|---|---|
| 1 | L00 | "ba/bốn điều" | tiêu đề cảnh prereq + câu ghép đổi thành "bốn điều" (bảng ①–④, lời đọc, tiêu đề cùng một số) | lint |
| 2 | L02 | thứ tự ưu tiên | thêm bước ở cảnh `sym`: chuỗi ngoặc → `* / %` → `+ -` → so sánh → `&&` → `\|\|` + hai ví dụ tính tay (a = 17; 300000 / 5 > 50000) + `checks` | verify 13/13; ví dụ trùng quiz |
| 3 | L04 | `TongArgs` thiếu dòng in | hiện cả tệp (9 dòng, có `System.out.println(args.length + …)`); `TongNhap` hiện đủ `import` + khung + vòng lặp (tách 2 step: dòng 1–6, 7–14) | verify |
| 4 | L05 | `Tong:`/`Lon nhat:` không hiện lệnh in; `KiemMang` thiếu `tong` | step cuối cảnh example hiện hai lệnh in; `KiemMang` hiện từ `long tong = 0;` | verify |
| 5 | L06 | không có tệp đủ lớp + hàm + `main` | cảnh `sym` hiện tệp `Phi.java` trọn vẹn trong 2 phần (dòng 1–9: lớp + hàm; phần 2: `main` cạnh hàm + dấu `}` đóng lớp), lời đọc nói "hàm nằm trong lớp, cạnh hàm chính"; cảnh quymo hiện cả tệp `SotChoSua` | render, khung 00010/00012 xem bằng mắt |
| 6 | L08 | (a) thiếu import (b) `DocTep` không có (c) `Files.size`, `timTen`, `s`/`n`/`daChep` | (a)(b) step `tep` hiện cả tệp `DocTep.java` có hai `import` và `throws Exception`, tiêu đề tệp trùng tên trong `de.md`; `de.md` + đề `practice` liệt kê ba `import` (`Files`, `Path`, `Locale`); (c) `timTen` hiện đủ định nghĩa, `NoiChuoi` hiện từ khai `n`, `s`, `daChep` tới dòng in, `DungLuong` tách 2 step (dựng nội dung / ghi và `Files.size`) | verify 13/13; khung 00052 |
| 7 | L09 | (a) thiếu import `HashMap` (b) "hàm băm" (c) bản đồ "~1 bước" không đo | (a) bảng có dòng `import java.util.HashMap;`, đầu tệp `Tong.java` hiện dòng nhập; (b) giảng hàm băm bằng một câu ("công thức biến khoá thành số ngăn; tra thì mở thẳng ngăn đó"); thêm hàng "thứ tự khi duyệt" (bản đồ không bảo đảm thứ tự); (c) KHÔNG đo: xem mục 4 | lint |
| 8 | L10 | `throws`, `chia`, `rut` không hiện | `HaiLuong` hiện `class` + `main … throws Exception` (tách 2 step); `ThuTu` hiện hàm `chia`; `QuyMoNuot` hiện hàm `rut` ở step riêng trước vòng lặp | verify 13/13; khung 00070 |
| 9 | L11 | mục tiêu kế thừa hứa hơn dạy | thêm cảnh `kethua` (3 step: lớp cha, lớp con có `extends`, `super(...)`, `@Override`, `super.phiThuongNien() / 2`; chạy thật `50000 25000` và `1000000`); mục tiêu 2 viết lại đúng điều dạy và `covers` trỏ cảnh `kethua`; lab thêm `LaiUuDai extends LaiCoDinh` (ghi đè + `super.lai(goc) / 2`) và dòng `Uu dai: 20000` trong `mong_doi` | verify; `lab_gate` JVA 13 PASS |
| 10 | L12 | `tu == den` và không hoàn tác | `chuyen` thêm điều kiện `l.tu().equals(l.den())` ném `IllegalArgumentException("Khong chuyen cho chinh minh")`; thêm "Lỗi 4" (chương trình `TuChuyen` chạy thật: `Lech tong 3100000 != 3000000`, tiền tự sinh 100 000) và nêu "`kiem()` báo lỗi sau khi đã sửa, sổ không tự hoàn tác, hệ thống thật hoàn tác bằng giao dịch cơ sở dữ liệu"; `de.md` mốc 2 ghi điều kiện | verify; trace tính từ mã |
| 11 | L12 | dấu vết trỏ vào tệp không hiện | ghi chú trên màn hình: số dòng đếm cả dòng trống; gõ lại thành `So.java` rồi gài lỗi thì dấu vết hiện `So.java` đúng các số dòng ấy. Đã kiểm thật: `So.java` có lỗi gài cho `So.java:54 / 49 / 72` = số của `SoLoi.java` trên màn hình; biến thể `CuoiNgay.java`, `TuChuyen.java` có ghi chú mô tả cách dựng | script `chk_so.py` (scratchpad) |
| 12 | L12 | thụt lề phần 3, 4 của `So.java` | `code_block` bị `textwrap.dedent` khi hiện từng đoạn; thêm tham số `keep_indent=True`, dùng cho cả 7 phần của cảnh `tep` | khung 00063 |

Ngoài báo cáo: L00 thêm hộp "báo `command not found` thì PATH" (rủi ro nêu ở mục 5 của báo cáo); L12 chú thích "10 nano giây = 10 phần tỉ giây" ở tiêu đề cột; L05 giảng "chỉ mục = bảng tra dựng sẵn, như mục lục sách" ở lần đầu xuất hiện.

## 2. P1 thuật ngữ tại chỗ

Sổ E52 (`tools/registry/symbols.JVA.yaml`): `jva_import`, `jva_new`, `jva_throws`, `jva_hashmap`. Giảng ở: `import`, `new`, dấu chấm gọi lệnh, `Integer.MAX_VALUE` (L01, bảng kèm cả tệp `ThapPhan.java`); `throws` (L08 cảnh `tep`); `HashMap` (L09 cảnh `sym`). Bài sau khai `assumes` và có hàng nhắc lại trong cảnh `prereq`: L03, L04, L05, L08, L09, L10, L12 (L07, L11 chỉ `jva_new`, đã có hàng nhắc sẵn). Lint E52 từng bắt 22 chỗ dùng trước khi giảng khi bật sổ (L01 pitfalls, L03 nhap, L05 sym, L08, L09, L10, L12…); tất cả đã xử lý, hiện 0.

| Bài | Mục "Cần biết trước" của báo cáo | Xử lý |
|---|---|---|
| L00 | `int soNguoi = 0` chưa giải thích kiểu; JDK/PATH | ghi chú + lời đọc "kiểu số nguyên"; hộp PATH |
| L01 | `import`, `new`, `Integer.MAX_VALUE`/`.add` | giảng (xem trên) |
| L02 | thứ tự ưu tiên so sánh/`&&` | bước thứ tự mới |
| L03 | `long phi;` chưa gán; `Scanner` | ghi chú "gán chắc chắn" ở step ví dụ; hàng nhắc `import`/`new` |
| L06 | vị trí hàm trong lớp | tệp trọn vẹn 2 phần |
| L08 | `import java.nio.file.*`, regex trong `split`, KB/MB/GB | hiện 2 `import`; thêm step "biểu thức chính quy" có chương trình `TachCham` chạy thật (`split(".")` ra mảng rỗng 0 phần, `split("\\.")` ra 2 phần, phần sau `234`); chú thích KB/MB/GB = một nghìn/triệu/tỉ byte |
| L09 | `import HashMap`, "hàm băm" | giảng |
| L10 | `System.exit`, `BufferedReader/StringReader/IOException`, `throws InterruptedException` | bảng 3 lớp + `throws Exception` hiện; `System.exit(0)` giải thích bằng lời |
| L11 | tên khung Spring/JUnit | thêm câu "khung phần mềm = bộ mã có sẵn do người khác viết, ta viết theo cách nó yêu cầu" |
| L12 | "nano giây", "chỉ mục", "giao dịch" | giải thích ngắn tại chỗ (xem trên) |

Điểm P1 dự kiến: 13/13 bài đạt 2 (100%, ngưỡng ≥ 90%): NOT_VERIFIED bằng người đọc; tôi chỉ chứng minh được bằng lint E52 + đọc lại từng mục của cột "Cần biết trước".

## 3. Cổng đã chạy (số thật, 2026-11-13)

| Cổng | Kết quả |
|---|---|
| `audit/jva/verify_jva.py` (JDK Temurin 21.0.13) | 146/146 PASS trước chỉnh cuối; sau chỉnh cuối L05/L12 chạy lại từng bài PASS (L05 10/10, L12 8/8, xem lại cuối phiên) |
| `gen.py` + `lv.py lint` | 13/13 bài: 0 FAIL, 0 WARN (L00 30, L01 40, L02 47, L03 38, L04 41, L05 28, L06 24, L07 24, L08 32, L09 29, L10 25, L11 26, L12 43 PASS) |
| `lv.py render` | 13/13: 0 vấn đề (số khung: L00 160, L01 141, L02 140, L03 145, L04 140, L05 105, L06 110, L07 104, L08 125, L09 129, L10 141, L11 129, L12 146) |
| `audit/review/lab_gate.py JVA` | 13 PASS · 0 FAIL |
| `lv.py curriculum curriculum/jva.yaml` | 13 bài, 13 đã có đặc tả, 0 lỗi |
| `audit/check_curricula_graph.py` | 46 lộ trình, 715 bài; tham chiếu hỏng 0; chu trình 0; VER không PASS 0 |
| `check_xref.py` | 0 lượt tham chiếu sang khoá khác |
| `check_course_refs.py jva` | 0 vấn đề |
| `check_meta.py` | 6 vấn đề, tất cả của PYT (không liên quan JVA; lọc `jva` ra 0) |
| `arith_scan.py` | 226 phép tính, 0 FAIL |
| `tests/test_e52.py` | 0 FAIL |
| `screen_code.py gen-jva` + `screen_hand.py` + `check --course JVA` | 390 khối, PASS 536 · FAIL 0 · STALE 0 · MISSING 0 · ORPHAN 0 · WARN 0; `screen_hand`: còn thiếu luật 0 |
| `check_next_refs.py` | KHÔNG chạy được: `AssertionError: bài không có chỗ trong dãy: PYT:L00…` (khoá PYT mới chưa vào dãy học `learn_start/pack.py`); không do JVA. JVA không có câu "Bài sau (bài N)" nào (grep 0) |

Khung PNG đã xem bằng mắt: L06 00010/00012; L08 00052; L12 00063/00112; L10 00070; L11 00053; L01 00106; L00 00050 (không có chữ tràn, đè, cắt).

## 4. Không sửa / sửa một phần (lý do)

- L09 mục (c) "thêm một lần đo bản đồ": không thêm phép đo. Một phép đo xác định (đếm số lần so sánh khoá) cần lớp khoá tự viết với `equals` + `hashCode`, vượt phạm vi bài và dùng khái niệm chưa dạy; đo bằng đồng hồ thì không lặp lại được nên không đạt luật "đầu ra màn hình = đầu ra thật". Thay vào: giảng cơ chế bằng một câu (ngăn đánh số từ khoá), ghi rõ trên màn hình "con số 'khoảng 1' lấy từ mô tả `HashMap` của Java SE 21, không đo trong bài". Người đọc có thể vẫn chấm P6 của L09 = 1.
- L12 phần giải thích "giao dịch cơ sở dữ liệu" vẫn ở mức một mệnh đề ("làm trọn hoặc hoàn tác") vì là chủ đề của khoá sau, không phải của JVA.
- Khung chứa nhiều dòng: các khung giữ ≤ 12 dòng mã trừ một số khung có tiêu đề + 12–13 dòng (`render` 0 vấn đề). Các đoạn mã ngắn ở phần "lỗi hay gặp" (L06, L10) vẫn là đoạn cắt không có `class`/`main`; báo cáo chỉ yêu cầu hiện đủ tệp một lần (đã làm ở L06 `sym`, L10 `luong`, L08 `tep`).

## 5. Việc người điều phối cần làm

- Dựng lại (build/tts/asr) cho cả 13 bài: lời đọc đổi ở L00–L12 (câu mới đều ≥ 8 từ), `asr_reviewed` của câu cũ còn nguyên chỗ câu không đổi; `out/JVA/*` hiện chỉ có khung `render`, chưa có mp4/srt mới.
- Chạy lại `check_next_refs.py` khi PYT đã vào dãy học.
- Lab đổi: `labs/JVA/L08/de.md` (3 import), `L11/` (de.md, mong_doi.txt thêm `Uu dai: 20000`, loi_giai.java), `L12/` (de.md, loi_giai.java thêm điều kiện chặn); `labs/cham.sh` không đổi.
