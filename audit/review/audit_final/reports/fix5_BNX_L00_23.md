# fix5 BNX L00–L23 (vòng 5, sửa theo R3_BNX_L00_23, 2026-11-15)

Hai tác tử con: A (L00–L11) và B (L12–L23). Báo cáo chi tiết từng phần: `fix5_part_A.md`, `fix5_part_B.md` (bảng từng bài, mục P1 đã giảng, từ lời đọc, cổng).
Sổ tác tử: `fix5_BNX_L00_23_ledger.md`. Cả hai tác tử bị ngắt một lần do hết hạn mức 5 giờ, được tiếp tục bằng SendMessage sau 3:10pm và đã xong.

## TIẾN ĐỘ
- [x] L00–L11 xong (phần A)
- [x] L12–L23 xong (phần B)
- [x] Cổng cuối khoá đã chạy (mục Cổng thật). Chưa chạy: build/tts/asr, git ghi, docker trực tiếp, `screen_code.py check --course BNX` (cả khoá, ≈ 12 phút, cần Docker).

## Bài đổi → CẦN DỰNG LẠI (build/tts/asr)
**Cả 24 bài L00–L23** (lời đọc và bảng màn hình đổi ở mọi bài). Lab (`labs/BNX/Lxx`, `de.md`, lời giải) không đổi nội dung; `lab_gate BNX` vẫn 39 PASS. Mọi câu `say` mới/đổi là câu TTS mới, cần nghe lại ASR, nhất là: "ổ cắm", "mã máy khách", "con trỏ", "tiêu đề", "cắt lát", "mặt nạ", "ONNX", "chữ hoa đặt thông số", "biến bằng tên thư mục". Không đọc thành tiếng chữ Latin chưa có luật (ed25519, base64url, printf, sleep, scaleb, Git).

## Kiểm lại của điều phối
`lv.py lint` chạy lại 24/24 sau khi cả hai tác tử xong: 0 FAIL, 0 WARN ở mọi bài (PASS: 36, 42, 46, 59, 37, 35, 38, 39, 41, 41, 39, 52, 52, 41, 56, 58, 71, 71, 54, 76, 53, 59, 62, 45).

## Số liệu cổng thật (do tác tử chạy)
| Cổng | Kết quả |
|---|---|
| `lv.py lint` L00–L23 | 0 FAIL, 0 WARN ở cả 24 bài (xem mục "Kiểm lại của điều phối") |
| `lv.py render` | 0 vấn đề ở cả 24 bài (L08, L10 lúc đầu có khung tràn do thêm ghi chú, đã gỡ/tách step) |
| `verify_bnx.py` | PASS hết, không SKIP: L00–L11 và L12–L18, L20–L23. **L19 KHÔNG chạy (cần Docker/Redis): NOT_VERIFIED** |
| `screen_fast.py` (khối của từng bài) | FAIL 0, STALE 0, ORPHAN 0 ở mọi bài đã chạy; **L17: 1 MISSING** (`BNX L17 example 15 1`), **L19 không chạy** (screen_keep L19: 18 khối, chưa khớp 0) |
| `lab_gate.py BNX` | 39 PASS · 0 FAIL (196 lab) |
| `tests/test_e52.py` | 0 FAIL |
| `arith_scan.py` | A: 246 phép, 0 FAIL; B: 58 phép (BNX), 0 FAIL |
| `check_course_refs.py BNX` | 0 vấn đề |
| `check_next_refs.py` | 550 lời hẹn, 0 lệch |
| `lv.py curriculum curriculum/bnx.yaml` | 39 bài, 0 lỗi (không sửa giáo án: mục tiêu/`covers` không đổi) |

## Lời đọc (đếm tách khoảng trắng toàn bộ `say`), trước → sau; mọi bài ≤ 2300
L00 2418→2297; L01 2383→2294; L02 2440→2298; L03 2445→2292; L04 2453→2288; L05 2416→2298; L06 2265→2262; L07 2329→2273; L08 2416→2299; L09 2443→2286; L10 2444→2297; L11 2398→2284; L12 2293→2298; L13 2294→2300; L14 2297→2295; L15 2299→2257; L16 2297→2290; L17 2256→2298; L18 2299→2299; L19 2295→2294; L20 2285→2296; L21 2299→2297; L22 2300→2293; L23 2298→2297. Mỗi `say` 4–38 từ, ≤ 170 ký tự (lint 0 WARN).

## P1: cách chữa và ước lượng số mục chưa giảng còn lại (người đọc chấm lại mới là số chính thức)
Cách chung: bảng "viết trong mã / nghĩa / ví dụ nhỏ" đặt ngay trước khối mã hoặc lệnh dùng nó, kèm 1–3 câu lời đọc có "nên/vì". Không đổi chuỗi mã trên màn hình nào ở L00–L11 và hầu hết L12–L23 (nên `ver/lNN.py` và nội dung sổ không đổi); không bỏ mục nào khỏi màn hình (phương án b/c không dùng), trừ L15 ⑤ (đổi số, xem SHOULD).
| Bài | Đã giảng tại chỗ (tóm tắt) | P1 còn lại (ước lượng) |
|---|---|---|
| L00 | `cat`, `&&`, `git log --format="%H %s"`, SHA-1 | 0 |
| L01 | `re.compile`, biểu thức if-else, `+=`/`bool`, `.append`, `enumerate` | 0 |
| L02 | JSON, `.encode()`, dict comprehension/`.items()`, `break`, cú pháp `.proto`, def/return | 0 |
| L03 | `hmac.compare_digest` (dời lên trước example step 12), `\`, `-binary`, `echo`, gán ba biến, `json.loads` | 0 |
| L04 | `%`, base64url (nhắc ở prereq), `while`, `+=` | 0 |
| L05 | `openssl req -x509 -newkey ed25519 …`, `\`, API `ssl`/`socket`, `getattr`, `date`/`timedelta` | 0–1 |
| L06 | bảng "đọc câu SQL", `isolation_level=None`, `set_trace_callback`, `_`, `.values()` | 0 |
| L07 | bảng "đọc câu SQL", `CASE WHEN`, thoát nháy, `DROP PARTITION`, lệnh Docker | 0 |
| L08 | def/return, f-string, `enumerate`, if-else, chạy `python mau.py` | 0 |
| L09 | `while chua:`, `continue`, if-else, `_`, def/return | 0 |
| L10 | `printf … \| docker exec -i`, `--property`, `sleep`, `--bootstrap-server`, `range` 3 đối số, f-string | 0–1 |
| L11 | `scaleb`, def/return, `_`, gán đôi | 0 |
| L12 | bảng gán nhiều biến | 0 |
| L13 | gán chuỗi `c, r, k = s = …`, số nguyên làm điều kiện, "jre" | 0 |
| L14 | "HTTP" | 0 |
| L15 | `j = top = 0`, `def cung_luc(tps, w=40_000)`, "bế tắc", bảng thành phần → yêu cầu → đánh đổi | 0 |
| L16 | `throws Exception`, `extends RecursiveTask<Long>`, `import static`, `List<Integer>`/`var` | 0 |
| L17 | GET/POST, `Authorization: Bearer`, `WWW-Authenticate`, `javac -d`, `java -D`, dấu `;` | 0 |
| L18 | `import static`, `javac -d`, cờ JUnit, `--disable-banner…`, `L=lib; $L`, `\` | 0 |
| L19 | cờ docker/redis-server/redis-cli, `$D`, `r()`/`--no-raw`/`"$@"`, `sh -c`, `MSET` | 0–1 (cờ phụ redis) |
| L20 | con trỏ `*`, `Header().Set`, `strings.Cut`/`Do`/`ReadAll`, `range` trên kênh | 0–1 (`go mod`/`go get` chỉ trên màn hình) |
| L21 | `printf`/`sed`/`cp`/`>`, `openssl rsa/dgst`, `dict(a, k=v)`, `join/sorted`, `sum(x != y …)` | 0–1 |
| L22 | `MA.get(c, c)`, regex trong `re.sub` + `m.group(1)`, getter ↔ `${trang.tieuDe}`, `type(x) is dict` | 0–1 |
| L23 | cắt lát numpy, mặt nạ, `d[d <= c] if … else …`, ghi/nạp ONNX, `pip install ==` | 0–1 (`pip ==` chỉ trên màn hình) |

Tự đánh giá: P1 ≥ 1 ở cả 24 bài; P1 = 2 dự kiến ở khoảng 18–22/24 bài. Rủi ro =1: L05, L10, L19, L20, L22, L23 (cờ phụ/API chỉ tóm một dòng hoặc chỉ ghi chú trên màn hình, không đọc vì hết trần từ). Chưa có người đọc lại.

## SHOULD (đã sửa 11/11 + PLAUSIBLE nêu trong brief)
- L15 example step 4–5: ⑤ thống nhất dùng tải chưa làm tròn: 115,74 × 0,040 ≈ 4,63 (sửa src, checks, `ver/l15.py` thêm kiểm 115,74 và 4,63, đầu ra Python); kết luận "khoảng 5 lệnh" không đổi; khung quymo ghi chú tải đã làm tròn 116 × 0,040 = 4,64 chỉ chênh do làm tròn.
- L15 mục tiêu 3: thêm bảng thành phần → yêu cầu → đánh đổi (không sửa mục tiêu, không đụng `curriculum/bnx.yaml`).
- L09 formula step 5: sửa focus theo số dòng thật (`def get` ↔ `[2.4]`, `def replace` ↔ `[2.6]`). L09 quiz câu 3: "nếu 200 yêu cầu đến cùng lúc" (đề, đáp án, lời đọc).
- L21: thêm [TT37] vào `audit/bnx/sources_l21.md` (TT 37/2025/TT-NHNN ngày 31/10/2025, hiệu lực 15/12/2025, sửa đổi TT 31/2024/TT-NHNN; nguồn thứ cấp sbv.gov.vn, thuvienphapluat.vn, english.luatvietnam.vn qua người đọc R3; KHÔNG ghi số điều; mức CITED thứ cấp).
- L10 formula step 5 (trường bị xoá không có mặc định) và prereq step 0 ý 2 (số phân vùng không đổi): sửa trên màn hình + lời đọc.
- L19 example step 7: chọn cách ghi nhãn "(đã lược các dòng -> Redirected … mà redis-cli -c in thêm)" trên khung kết quả, không bịa đầu ra Redis sống.
- L00 quiz câu 2 viết rõ (nhánh X có 2 commit riêng chưa nằm trong 4 commit); L01 quymo step 4 lời đọc đúng mốc 50/500; L02 sym "đóng vai hợp đồng giữa bên gửi và bên nhận".
- L16 sym step 2 tách hai bước đọc từng hàng; L19 sym.2, L18 sym.2, L20 sym.1: đọc từng hàng.
- KHÔNG sửa (lý do): L18 sym.0/sym.1, L20 sym.0, L19 sym.0/sym.1: đã có 3–5 câu đọc theo từng hàng kèm focus, thêm nữa vượt trần 2300 từ. L19 khối `r -c SET/GET`: vẫn lược 2 dòng Redirected (đã ghi nhãn).

## Tệp đã sửa
`audit/bnx/src/l00.py … l23.py`; `lessons/bnx/L00…L23_*.yaml` (do gen.py sinh); `audit/bnx/ver/l15.py` (kiểm mới); `audit/bnx/sources_l21.md` (+[TT37]); `audit/bnx/screen/l00…l23.yaml` (sinh lại bằng `screen_keep.py`, có sửa tay khoá tham chiếu chéo, xem dưới); `out/BNX/Lxx/frames` (do render). KHÔNG sửa: `tools/registry/symbols.BNX.yaml` (không thêm `term:`), `gen.py`, `lib*.py`, `audit/review/screen_code/BNX.yaml`, `curriculum/bnx.yaml`, `tools/checklib_bnx`, `labs/`.

## Việc điều phối cần làm (thay đổi sổ chung)
1. Gộp sổ: `python -B audit/bnx/screen_try.py --merge` đưa `audit/bnx/screen/l00…l23.yaml` vào `audit/review/screen_code/BNX.yaml`. Chèn bảng/step làm lệch chỉ số step của khối mã nên các khoá cũ của L01–L11 và L12–L23 trong sổ chung hiện STALE/MISSING/ORPHAN cho tới khi gộp; sau gộp bỏ khoá mồ côi.
2. Sửa tay (trong tệp sổ riêng của bài, chỉ đổi khoá tham chiếu chéo, không đổi nội dung kiểm; kiểm lại khi gộp): `screen/l05.yaml` 3 khoá `files:` nguồn `L05_certs` → `example 1 0 / 2 0 / 3 0` (còn `note` tự do nhắc "example 6 0" cũ, không ảnh hưởng); `screen/l21.yaml` mục `formula 13 0` `within` → `BNX L21 formula 14 0`; `screen/l22.yaml` nguồn `L22_model` `TrangModel.java` → `formula 11 0`; `screen/l23.yaml` 3 mục `within` → `formula 6 0`, `8 0`, `14 0`.
3. **Còn 1 khối chưa có mục sổ**: `BNX L17 example 15 1` (kết quả ca E, đầu ra thật của `L17_spring`, dòng Bearer lược bằng "…"): chạy `screen_code.py stub --course BNX` rồi điền `kind: output, of: src:BNX:L17_spring` (ghi tay mục mới vào sổ bị chặn quyền).
4. Chạy `verify_bnx.py L19` và `screen_fast.py L19` khi máy có Docker (L19 NOT_VERIFIED); sau gộp chạy `screen_code.py check --course BNX` (≈ 12 phút, cần Docker) xác nhận cả 24 bài.
5. Dựng lại build/tts/asr cả 24 bài, nghe lại các câu `say` đổi.
6. Ghi chú: `check_xref.py` còn lỗi cũ ở L33 ("WEB-INF"), ngoài phạm vi; scratchpad dùng chung từng trùng tên tệp tạm (`gate.sh`, `g_L11.txt`) giữa các nhóm, không ảnh hưởng repo.

## NOT_VERIFIED
Redis sống (L19, các đầu ra OK/(nil)/MOVED/CROSSSLOT/DELEX/TTL), `docker build --check` (L13), nguyên văn văn bản pháp lý thứ cấp (L12, L14, L21 TT 37/2025), phát âm TTS bằng tai người.
