# fix4 BNX L12–L23 (tác tử sửa, 2026-11-15)

## Tiến độ
- Xong 12/12 bài: L12, L13, L14, L15, L16, L17, L18, L19, L20, L21, L22, L23. Đã sửa NGUỒN `audit/bnx/src/l12..l23.py`, chạy `gen.py` từng bài (không sửa tay YAML).
- **Mọi bài L12–L23 đã đổi nội dung nên đều CẦN DỰNG LẠI** (tts, asr, render, build). Khung PNG `out/BNX/Lxx/frames` đã dựng lại bằng `lv.py render` (chỉ để xem; mp4 và srt cũ).

## Số liệu cổng (đo thật 2026-11-15)
| Bài | lint | từ lời đọc | render | verify_bnx |
|---|---|---|---|---|
| L12 | 0 FAIL 0 WARN | 2293 | 0 vấn đề | 30/30 PASS |
| L13 | 0/0 | 2294 | 0 | 24/24 PASS |
| L14 | 0/0 | 2297 | 0 | 25/25 PASS |
| L15 | 0/0 | 2299 | 0 | 24/24 PASS |
| L16 | 0/0 | 2297 | 0 | 31/31 PASS |
| L17 | 0/0 | 2256 | 0 | 34/34 PASS |
| L18 | 0/0 | 2299 | 0 | 26/26 PASS |
| L19 | 0/0 | 2295 | 0 | CHƯA chạy (cần Docker/Redis; chỉ đổi lời và bảng, mã Redis không đổi) |
| L20 | 0/0 | 2285 | 0 | 33/33 PASS |
| L21 | 0/0 | 2299 | 0 | 32/32 PASS |
| L22 | 0/0 | 2300 | 0 | 33/33 PASS |
| L23 | 0/0 | 2298 | 0 | 49/49 PASS (thêm 2 kiểm biên mới) |
- `tests/test_e52.py`: 0 FAIL. `arith_scan.py BNX`: 57 phép tính, 0 FAIL. `check_course_refs.py BNX`: 0 vấn đề. `lv.py curriculum curriculum/bnx.yaml`: 39 bài, 39 có đặc tả, 0 lỗi. `lab_gate.py BNX`: 39 PASS · 0 FAIL (195 lab được bài tham chiếu).
- verify_bnx chạy lại cuối phiên (sau mọi sửa): L12 30/30, L13 24/24, L14 25/25, L15 24/24, L16 31/31, L17 34/34, L18 26/26, L20 33/33, L21 32/32, L22 33/33, L23 49/49 (tất cả PASS, không SKIP); L19 chưa chạy (cần Docker).
- Sổ mã trên màn hình, chạy `screen_fast.py` theo bài (chỉ khối của bài; KHÔNG chạy `screen_code check` cả khoá vì mất ~12 phút và cần Docker): L12 17 PASS, L13 19, L14 9, L15 10, L16 35, L18 23, L20 52, L21 24, L22 28, L23 37 — mọi bài FAIL 0, STALE 0, MISSING 0, ORPHAN 0. **L17: 37 PASS, MISSING 1** (xem mục "Cổng chung"). L19 chưa kiểm (khối Docker).

## MUST (2/2 đã sửa)
- **L17** example: "21 tệp" → "20 tệp jar" ở SHOW và SAY ("hai mươi tệp"); thêm địa chỉ tải `repo1.maven.org/maven2`. Đã đếm lại: `audit/bnx/deps/l17` có đúng 20 `.jar` (README.md là tệp thứ 21).
- **L18** quymo, hàng "ca sát mốc + đối tượng giả": đổi thành "2k + 1 ca; sinh từ bảng mốc: mỗi mốc hai ca (đúng mốc, liền dưới) cộng một ca dưới mốc đầu" (khớp BoCa.java: 5/401/4001); lời đọc nói "mỗi mốc hai ca".

## SHOULD (đã sửa hết, trừ 1 mục cosmetic ghi bên dưới)
- L13: câu hỏi quay lui được trả lời (hàng bảng hook + câu ở pitfall 3: quay về bản cũ cũng là một lần cập nhật cuốn chiếu); slide lab hiện dữ liệu (`tot`, `xau`); tiêu đề kết quả `docker build --check` ghi "Docker 28".
- L12: slide lab hiện dữ liệu đề (khung riêng, lấy từ lời giải lab); recap chip rút gọn.
- L14: Điều 11 vế "trừ khi khách và ngân hàng thoả thuận khác" hạ nhãn "theo bản dịch tiếng Anh, cần kiểm lại" (registry/sources chỉ có "không quá 180 ngày", thứ cấp; không xác minh được vế ngoại lệ); slide lab ghi "mỗi bên gửi dồn 20 yêu cầu".
- L15: "mỗi khách" thêm vào prereq step 1, nhãn hình và lời intuition step 0.
- L17: ca E (mã thật hết hạn) hiện kết quả thật (401, Jwt expired) ở step riêng; cột quymo ghi "tối đa trong 45 giây" và "ước lượng: gần 0 lỗi (không mô phỏng việc thử lại)"; sửa khung chạm viền ở hình Spring Cloud (00020: nâng chiều cao SVG, dời dòng chú).
- L20: example step 5 hiện chương trình không khoá từ dòng 3 tới dòng 14 và ghi "xoá cả dòng `var khoa sync.Mutex`, nếu chỉ bỏ Lock/Unlock thì Go báo `declared and not used: khoa`"; lệnh `-race` tách step riêng.
- L21: "Ba lệnh đầu tạo hợp đồng, khoá riêng và khoá công khai" (trước ghi "hai lệnh"); gợi ý lab thêm `f"{x:.1f}"` cho "một chữ số thập phân".
- L22: quymo ghi "Trong mô phỏng, tra một đường dẫn luôn bốn bước… kho thật phụ thuộc số con của mỗi nút" (+ cột "(mô phỏng)"); khung lỗi 2 dày (00073) tách thành hai step có lời đọc riêng, phần "thành phần khai báo kiểu DS" nay có trong lời.
- L23: quy tắc đếm sửa đúng mọi biên: số điểm dưới phân vị p = p × (n−1) **làm tròn lên** (khi p × (n−1) nguyên thì giữ nguyên). Sửa prereq ③, step Bước 5, quiz câu 2, lab (de.md, lời giải dùng `math.ceil`, đầu ra không đổi). Kiểm bằng mã: `ver/l23.py` thêm 2 dòng, chạy `np.percentile` trên 10 cặp (n, p) gồm n=101 p=0,01 (thật 1; quy tắc cũ cho 2) → 10/10 khớp quy tắc mới và `alg.bnx_l23_expected_flags` (hàm này vốn đã đúng biên, không phải sửa).
- Không sửa (cosmetic, ghi lý do): L12 recap — dải chip 6 mục vẫn xuống dòng và để lại mũi tên cuối dòng đầu; do bố cục chuỗi chip của player (không điều khiển được ngắt dòng); đã rút ngắn nhãn nhưng vẫn 6 chip không vừa một hàng.
- Không sửa: L18 00044 / L19 00042 mã dài cắt bằng "…" (người đọc ghi không sai kiến thức); L14 00000 phông số KaTeX; L13 00055 nửa dưới trống (không phải lỗi nội dung).

## P1 — thuật ngữ và cú pháp giảng tại chỗ (mục tiêu ≥ 90% bài P1 = 2)
Cách làm chung: thêm bảng "viết trong mã/nghĩa/ví dụ nhỏ" (kèm 1–2 câu lời đọc) ngay trước đoạn mã dùng cú pháp đó, hoặc chú thích tại màn hình mã; thuật ngữ nền giảng ở cột "nghĩa" lần đầu xuất hiện. Không thêm mục sổ `term:` chung (các từ nền như "xác thực", "định tuyến", "tiến trình" bị bài L24–L36 dùng, thêm sẽ buộc `assumes` chéo bài); các `introduces` đã có giữ nguyên.
- L12: `.items()`, `not in`, `g[0]`, `1 if…else -1`, `sum`, `//`, `1_000_000`, `list(range)`, "vòng lặp lồng", "bình phương", "chỉ mục", µs/ms.
- L13: "hệ tệp", "nhân hệ điều hành", khoá YAML (`apiVersion/kind/metadata/spec/template/containerPort`), "ghim", digest/"chuỗi băm", dấu `|` và `docker build -t … .`, `while`, `min`, `//`, `-(-D // 4)`, `while todo`, `continue`, `.append/.add`, `min(… for …)`; lời đọc đi từng bước vòng lặp liệt kê trạng thái.
- L14: REST/POST, xác thực, định tuyến, đối tượng, giao dịch, mô-đun, hậu phương, 5 ms; bước cú pháp Python (def/return/for/`F`/list comprehension/`min`/gán đôi/`sum(… for …)`).
- L15: Kafka, Spring Boot, "bất đồng bộ", "chuỗi bước bù trừ"; bảng đi từng dòng `cung_luc` (ví dụ 10 ms một lệnh, mỗi lệnh ở lại 40 ms → 4 lệnh chồng).
- L16: "hàm đệ quy", `?:`, generics `List<Integer>`, `var`.
- L17: "chữ ký" (dãy ký tự tính từ nội dung và khoá bí mật), "khoá công khai/khoá riêng".
- L18: `javac`/biên dịch, Maven Central, `int/long/long[]`, `?:`, `(int)`, "luồng lỗi", "bản thể/trường của lớp".
- L19: byte/bit, bảng ký hiệu CRC16 (`^`, `<<`, `&`, `0x…`, `&= 0xFFFF`), cú pháp vỏ lệnh (`for…do…done`, `until…grep -q`, `> /dev/null 2>&1`), "máy khách", "tiến trình", "lõi ngân hàng".
- L20: Go nền (`package main`, `import`, `fmt.Println`, `if err != nil`, `[]int{…}`, `len`, `continue`, `uint64`, `chan struct{}`), "ngăn xếp", JSON, cổng/TCP/127.0.0.1, "luồng hệ điều hành/rò rỉ", cgo/gcc, `cat > main.go <<'GO'`, cài Go.
- L21: Python (dict, `not in`/`raise`, `try/except`, f-string, `setdefault`, `zip`), "tất toán", "chứng thư số", RSA/bit, "luồng lỗi", CCCD, "ca kiểm", "biên".
- L22: Python (`get/isinstance`, `enumerate`, `partition/split`, `re.sub`+lambda, class), `cq:Page/jcr:content`, `@Model`, `@ValueMapValue`, "tham số đường dẫn".
- L23: "ln", c(n) (nghĩa, theo mã nguồn thư viện), "miền ai.onnx.ml", "độ trễ", `random_state`, `max_samples_`.
Điểm P1 dự kiến: cần người đọc chấm lại; tự đánh giá 11–12/12 bài đạt 2 (chỗ chặn thật theo "kẹt ở đâu" đều đã có giảng tại chỗ). Rủi ro còn lại: người đọc chấm nghiêm cú pháp Python/Java rất nền (`def`, `for`, `class`) ở L15, L16, L18.

## Quy mô lời đọc
Mọi bài ≤ 2300 từ (đo bằng ước lượng của lint: 2256–2300). Cắt chỗ khác để bù (rút câu thuật lại kết quả, bỏ câu lặp bảng).

## Tệp đã sửa
`audit/bnx/src/l12.py … l23.py`; `audit/bnx/ver/l23.py` (thêm kiểm biên); `lessons/bnx/L12…L23_*.yaml` (do gen sinh); `labs/BNX/L12…L23` (write_lab ghi lại cùng nội dung, riêng L23 `de.md` + `loi_giai.py` đổi `math.ceil`); `audit/bnx/screen/l12…l23.yaml` (sinh lại bằng `screen_keep.py`); `out/BNX/Lxx/frames`. Không sửa tệp dùng chung (symbols.BNX.yaml, gen.py, lib*.py, checklib).

## Cổng chung và việc điều phối cần làm
- Sổ `screen_code`: đã chạy `screen_keep.py` cho L12–L23 (sinh lại `audit/bnx/screen/l12…l23.yaml`; khối đổi được khớp lại theo sha/chương trình). Hai tham chiếu chéo khoá bị lệch vì bài chèn thêm step, `screen_keep` không dịch được; đã sửa tay đúng hai dòng khoá (không đổi nội dung kiểm): `screen/l21.yaml` mục `formula 11 0` `within: BNX L21 formula 12 0`; `screen/l22.yaml` nguồn `L22_model` `files.TrangModel.java: BNX L22 formula 10 0`. Điều phối nên kiểm lại hai dòng này khi gộp.
- **Còn 1 khối CHƯA có mục sổ**: `BNX L17 example 13 1` (kết quả ca E, đầu ra thật của `L17_spring`, dòng Bearer lược bằng "…"). Em không tự điền mục này (thao tác ghi tay mục mới vào sổ chứng cứ bị cổng quyền chặn); điều phối dùng `screen_code.py stub --course BNX` rồi điền `kind: output, of: src:BNX:L17_spring`. Gộp vào sổ chung bằng `screen_try.py --merge` (chưa gộp; người điều phối làm).
- L19 chưa kiểm lại bằng Docker (mã Redis không đổi); verify_bnx L19 nên chạy khi máy có Docker.
- ASR: toàn bộ câu `say` mới/đổi là câu TTS mới, cần dò lại (đặc biệt "ln", "ngăn xếp", "hệ tệp", "chuỗi băm", "nhân hệ điều hành").
