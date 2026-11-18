# fix2_S01 JVA: sửa vòng 2 theo báo cáo người đọc S01b_JVA (2026-11-14)

Nguồn sửa: `audit/jva/src/l02.py, l04.py, l07.py, l08.py, l10.py, l11.py, l12.py`; bộ kiểm mới `audit/jva/verify_l12_screen.py` (gọi từ `audit/jva/verify_jva.py`). `lessons/jva/*.yaml`, `labs/JVA/L12/*` do `gen.py` sinh lại; sổ mã màn hình `audit/review/screen_code/JVA.yaml` sinh lại bằng `screen_code.py gen-jva` + `screen_hand.py`. Không chạy build/tts/asr/audit_all/docker; không sửa YAML bằng tay.

## 1. Bài đã đổi (để dựng lại)

L02, L04, L07, L08, L10, L11, L12 (lời đọc đổi ở cả 7 bài, nên cả 7 cần dựng lại; L00, L01, L03, L05, L06, L09 không đổi trong vòng này).
Lab đổi: `labs/JVA/L12/de.md` (thêm kết quả trung gian). Giáo án `curriculum/jva.yaml` không đổi.

## 2. MUST (L12): đã kiểm lại bằng chạy thật rồi sửa

Báo cáo đúng. Nguyên nhân gốc: ghép nguyên văn bảy phần của cảnh `tep` làm rơi hai dòng trống (trước `chuyen`, và trước `public class` của hàm chính), nên `So.java` ghép được lệch 1–2 dòng so với tệp mà dấu vết trên màn hình được tính (53/48/70 thay vì 54/49/72). Ngoài ra tên tệp/lớp trên màn hình (SoLoi/CuoiNgay/TuChuyen) khác So.java, và biến thể CuoiNgay không dặn giữ lỗi `a + l.tien()`.

Cách sửa (chọn "hiện đủ mã + dặn đúng chỉnh sửa", giữ cam kết số dòng):
- Cảnh `tep` chia lại thành 8 phần (tách phần cộng tổng và phần lấy số dư để khung không tràn); mọi dòng trống nằm TRONG một phần (phần 1, 2, 3, 4, 6 kết thúc bằng một dòng trống, tiêu đề ghi "dòng cuối là dòng trống, giữ nó"); lời đọc phần một nói rõ phải giữ dòng trống vì dòng trống được đếm khi báo số dòng. Ghép 8 phần ra đúng 83 dòng, giống từng chữ tệp `So` đã chạy thật.
- Chữ nhỏ ở Lỗi 1, 3, 4 viết lại thành các bước làm cụ thể, áp lên So.java đã sửa: sao thành `SoLoi.java` / `CuoiNgay.java` / `TuChuyen.java`, đổi tên lớp; Lỗi 1: `b + l.tien()` thành `a + l.tien()`; Lỗi 3: GIỮ lỗi gài `a + l.tien()`, bỏ `kiem();` trong `chuyen`, thêm `so.kiem();` ngay sau dòng in `Tong`; Lỗi 4: giữ `b + l.tien()`, bỏ ba dòng chặn `l.tu().equals(l.den())`, thay bốn dòng `ds.add` bằng đúng một dòng A → A. Mỗi bước thêm một câu lời đọc (mới, ≥ 8 từ).
- Dấu vết trên màn hình giữ nguyên số (SoLoi 54/49/72, CuoiNgay 53/81, TuChuyen 51/46/66): giờ ghép + chỉnh sửa ra đúng các số này.
- Kiểm mới trong `verify_jva` (`verify_l12_screen.py`): lấy các khối mã trên màn hình từ đặc tả (HTML thật), ghép nguyên văn, so với tệp So (83 dòng), biên dịch và chạy; rồi áp đúng các chỉnh sửa ghi trong chữ nhỏ, biên dịch + chạy ba biến thể, và so TỪNG DÒNG (kết quả in + dấu vết có số dòng) với khối kết quả chiếu trên màn hình. 5 kiểm, đều PASS; kiểm sẽ FAIL nếu một phần mất dòng trống hoặc số dòng lệch.
- Lab L12 (SHOULD): `de.md` thêm "Kết quả trung gian": mốc 1 in `Mo xong: tong 4000000`; mốc 2 (hàm chính `throws Exception`, thử P → Q 500000 và Q → R 2000000) ra ba dòng `Mo xong: tong 4000000` / `P=1500000 Q=1300000` / `TU CHOI Q chi co 1300000`. Hai chương trình mốc khai bằng `prog(...)` (`SoCaiMoc1`, `SoCaiMoc2`), chạy thật PASS; khung `practice` nhắc "kết quả trung gian ghi trong de.md".

## 3. SHOULD

| Bài | Mục | Xử lý |
|---|---|---|
| L04 | pitfalls[1] thiếu `}` của while | hiện thêm dòng `}` (lines 3–12); mã chiếu giờ biên dịch được |
| L10 | intuition[2] `TaiNguyen.java` thiếu 3 `}` | hiện tới hết tệp (lines 5–15) |
| L10 | pitfalls[2] `phiMoiLan` chưa định nghĩa | hiện hàm `phiMoiLan` (3 dòng) trước khối thử; thêm câu lời đọc "phí chia cho số lần, số lần là không" |
| L11 | check[0] `GiaoDichThuong` chưa khai | tách step: hiện khai lớp (5 dòng, tiêu đề "lớp thường cùng hai trường") rồi mới hiện hàm chính + kết quả; câu lời đọc mới nêu lý do (lớp thường không tự sinh phép so nội dung) |
| L08 | sym[0] "Nguyễn Văn An" lời đọc vs "Nguyen Van An" mã | lời đọc đổi thành "Nguyen Van An, viết không dấu như trong mã" |
| L02 | sym[3] bảng ưu tiên gộp `<` với `==` | chuỗi ưu tiên tách hai bậc: "so sánh lớn nhỏ: < <= > >=" rồi "so sánh bằng, khác: == !="; lời đọc nói hai bậc (ví dụ trong bài vẫn đúng: `17 > 10` trước, `== 0` sau) |
| L07 | formula[4] lý do `toString` phải `public` dựa vào kế thừa | viết lại bằng lý do đã dạy ở bài này (lệnh in nằm ngoài lớp nên phải gọi được hàm từ bên ngoài, như hàm đọc số dư) + "ta sẽ học kỹ ở bài mười một" |
| L12 | lab mốc 1–2 thiếu kết quả trung gian | đã thêm (mục 2) |

Mục không sửa: không có.

## 4. Cổng (số thật, 2026-11-14)

| Cổng | Kết quả |
|---|---|
| `verify_jva.py` (JDK 21.0.13) | toàn khoá 153/153 PASS, chạy lại sau chỉnh cuối (gồm 5 kiểm ghép-màn-hình + 2 chương trình mốc mới) |
| `gen.py` + `lv.py lint` | L02 47, L04 41, L07 24, L08 32, L10 25, L11 26, L12 43 PASS; mọi bài 0 FAIL, 0 WARN |
| `lv.py render` | 7 bài 0 vấn đề (L11 và L12 từng tràn sau khi thêm mã, đã tách step) |
| `lv.py curriculum curriculum/jva.yaml` | 13 bài, 13 có đặc tả, 0 lỗi |
| `check_curricula_graph.py` | 46 lộ trình, 728 bài; tham chiếu hỏng 0; chu trình 0; VER không PASS 0 |
| `tests/test_e52.py` | 0 FAIL |
| `screen_code.py gen-jva` + `screen_hand.py` + `check --course JVA` | 393 khối; PASS 541, FAIL 0, STALE 0, MISSING 0, ORPHAN 0, WARN 0; screen_hand còn thiếu luật 0 |
| `lab_gate.py JVA` | 13 PASS, 0 FAIL |

Khung PNG đã xem: L12 00064 (trước sửa, tràn), 00068 (phần 7/8), 00105, 00111 (Lỗi 3 với chữ nhỏ, dấu vết); L11 00070 (check: mã đủ lớp). Không chữ tràn/đè/cắt.

Điểm dự kiến: P1 = 2 ở 13/13 (không đổi so với S01b), P8 = 2 ở 13/13; MUST 0 sau sửa (NOT_VERIFIED bằng người đọc, chứng minh bằng kiểm ghép-màn-hình chạy thật).

## 5. Việc người điều phối

- Dựng lại (build/tts/asr) L02, L04, L07, L08, L10, L11, L12 (câu `say` mới/đổi đều ≥ 8 từ, ≤ 38 từ).
- `labs/JVA/L12/de.md` đổi; `loi_giai.java`, `mong_doi.txt` không đổi.
