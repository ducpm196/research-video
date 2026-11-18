# fix6 BNX_B nhánh B3 (L22–L24) — 2026-11-16

Nguồn sửa: `audit/bnx/src/l22.py`, `l23.py`, `l24.py` (sinh bằng `gen.py`), dùng khuôn `audit/bnx/libj.py` (`jstep`, `nowrap`; KHÔNG sửa libj/lib/lib2). Sổ: `audit/bnx/screen/l22..l24.yaml` chỉ qua `screen_keep.py`, cộng 4 sửa tay bằng Edit (xem mục Sổ). Không docker/dbrun/build/tts/asr/git.

| Bài | Từ trước → sau | asr_reviewed | lint | render | screen_fast | verify_bnx | mục chưa giảng ước còn lại |
|---|---|---|---|---|---|---|---|
| L22 | 2293 → 2292 | 4 → 4 | 0/0 | 0 vấn đề (116 khung) | PASS 28, FAIL 0 | 33/33 | 0 |
| L23 | 2297 → 2296 | 9 → 9 | 0/0 | 0 vấn đề (109 khung) | PASS 37, FAIL 0 | 49/49 | 0 |
| L24 | 2292 → 2260 | 10 → 10 | 0/0 | 0 vấn đề (115 khung) | PASS 37, FAIL 0 | 22/22 | 0 |

## Mục R4 đã xử lý
- L22: formula[3] `url[:i]`, `url[i + 1:]`, `phan[:-1]`, `phan[-1]` (hàng cắt lát), `[i for i, c in enumerate(url) if c == "."] + [len(url)]` (danh sách sinh sẵn + enumerate), `i = max(co) if co else cat[0]` (biểu thức điều kiện), `giua, gach, hau_to = s.partition("/")` (gán nhiều biến): bảng 4 hàng trước khối `tach`. formula[11] `package`, `class`, `import …*`, `@Model/@ValueMapValue`, `private String tieuDe;` + `getTieuDe()`: bảng 4 hàng trước khối Java. formula[13] `class Goi`/`__init__`/`self`, `self.a, self.b, self.c = …`, `self.vet += […]`, `raise`/`try … except … as loi`: bảng 4 hàng trước khối `Goi`. Bảng đầu formula bỏ hai hàng đã chuyển (enumerate, class).
- L23: formula[8] bảng cắt lát/`(nhan == -1).sum()` chuyển LÊN TRƯỚC khối huấn luyện (loại M); formula[14] `from skl2onnx import …`, `import onnxruntime as rt`, f-string `{lech:.1e}`, `abs(a - b).max()` (bảng 3 hàng); formula[4] `for i in (0, 1000)` và `[so_lan_cat(…) for _ in range(200)]` (bảng 2 hàng); formula[6] `return -2 ** (-h / c)` + `def` (bảng 2 hàng, nói rõ dấu trừ tính sau lũy thừa). Ghi chú phiên bản (scikit-learn 1.9.1, skl2onnx 1.20.0, onnxruntime 1.31.1) GIỮ NGUYÊN.
- L24: formula[0] `public class`, `@Id Long id; String ten;`, `List<TaiKhoan> tk = new ArrayList<>()`; example[0] `static SessionFactory mo(int n)`, `new Configuration().addAnnotatedClass(…)…setProperty(…)`; example `main` + `for (Khach k : …)`; example[5] `s.find(TaiKhoan.class, 11L)`, `a == b`, `Transaction t = …; t.commit();`; example `for (long n : new long[] {5, 50, 500})` và hằng `static final String`; check[0] `for (i,) in …fetchall()`, `INSERT … (?)` + `(i,)`, `lambda c: n.append(c)`; pitfalls[0] `try/catch (LazyInitializationException e)` + `e.getClass().getSimpleName()`. Mỗi bảng đứng TRƯỚC khối mã dùng token, có một câu mở đầu có "vì".
- SHOULD: ô "(×N)" bảng quy mô bọc `nowrap()` ở cả ba bài (L22 3 ô, L23 3 ô, L24 3 ô). L24 mã "trích": `DemSql.java` hiện ĐỦ tệp (12 dòng, một khung); `DemN1.java` hiện đủ ba khung (1/3, 2/3, 3/3, thêm một step ngắn); `Kho.java` (71 dòng) ghi rõ "đoạn đầu; mã đủ ở tệp kèm labs/BNX/L24/java/Kho.java"; `DemBan.java` ghi "đoạn … mã đủ ở tệp kèm". `build()` của `l24.py` ghi MỌI chương trình Java của bài (Khach, TaiKhoan, Kho, DemSql, DemN1, DemBan, DemLoi, DemNho, DemTrang) + `README.txt` vào `labs/BNX/L24/java/` (tất định). Tự kiểm chạy thật: nguồn `ChayHib` của sổ biên dịch và chạy đúng các tệp này bằng Hibernate 7.1.0.Final + H2 + JDK 21 → screen_fast PASS (đầu ra khớp).
- Lời đọc cắt bằng cách rút câu trùng bảng/ví dụ; câu `asr_reviewed` giữ nguyên chữ.

## Sổ chứng cứ (lưu ý cho người điều phối)
`screen_keep.py` đổi khoá khối và dịch `of`/`prelude_keys`/`files` của MỤC KHỐI, nhưng KHÔNG dịch (a) `within:` của mục `fragment` và (b) `files:` của mục nguồn `src:`. Sau khi chèn step, `screen_fast` báo FAIL tham chiếu cũ; đã sửa bằng Edit từng mục, có bằng chứng là lời `reason` của chính mục đó:
- `audit/bnx/screen/l22.yaml`: nguồn `L22_model` `files: TrangModel.java: BNX L22 formula 11 0` → `formula 13 0` (khối Bước 5 Java).
- `audit/bnx/screen/l23.yaml`: `formula 9 0 within …formula 6 0` → `formula 8 0` (khối công thức); `formula 12 0 within …8 0` → `…11 0` (khối huấn luyện); `formula 18 0 within …14 0` → `…17 0` (khối xuất ONNX).
Nếu chạy lại `screen_keep.py L22` hoặc `L23`, các tham chiếu này sẽ trở lại giá trị cũ (nó chép mục cũ theo `sha`) và phải Edit lại; hoặc người điều phối vá `screen_keep.py` để dịch `within`/`files` của nguồn. `screen_try --merge` KHÔNG chạy (để người điều phối).

## Khung PNG đã xem
L22 00027 (bảng cắt lát/điều kiện), 00047 (bảng Java); L23 00051 (bảng ONNX); L24 00055 (bảng find/==/giao dịch), 00064 (bảng Python kiểm). Không tràn. Nhận xét: khi cột "ví dụ" rỗng (nhiều hàng tôi đặt ví dụ rỗng để giữ lời đọc ngắn) cột này hẹp và trống: nếu `libj.jstep` bỏ cột khi mọi ví dụ rỗng thì đẹp hơn (không đổi nội dung).

## Chưa làm / ngoài phạm vi
- `screen_try.py --merge`, curriculum, test_e52, lab_gate, arith_scan, check_curricula_graph: để người điều phối (theo lệnh).
- `verify_bnx` L22/L23/L24 không dùng docker; L23 chạy được vì có `audit/bnx/deps/l23/venv` (sklearn/onnx); các khẳng định phụ thuộc phiên bản vẫn là "chạy ở máy dựng", không bịa nguồn.

## Bài đổi → requeue
L22, L23, L24 (lời đọc và bảng đổi ở cả 3; L24 thêm `labs/BNX/L24/java/*`).
