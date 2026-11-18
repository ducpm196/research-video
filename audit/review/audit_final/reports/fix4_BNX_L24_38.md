# fix4 BNX L24–L38 (tác tử sửa, 2026-11-15)

Chi tiết từng nhóm: `fix4_BNX_L24_28.md` (nhóm A), `fix4_BNX_L29_33.md` (nhóm B), `fix4_BNX_L34_38.md` (nhóm C). Tệp này là tổng hợp.

## Tiến độ
- XONG 15/15 bài: L24–L38. Sửa NGUỒN `audit/bnx/src/l24..l38.py`, `gen.py Lnn` từng bài (không sửa tay YAML). Không sửa tệp dùng chung (symbols.BNX.yaml, gen.py, lib*.py, sổ BNX.yaml). Duy nhất `curriculum/bnx.yaml` được sửa 3 mục tiêu (xem dưới).
- **CẦN DỰNG LẠI (tts, asr, render, build): cả 15 bài L24, L25, L26, L27, L28, L29, L30, L31, L32, L33, L34, L35, L36, L37, L38.** Khung PNG `out/BNX/Lxx/frames` đã render lại để xem; mp4, srt, chapters.txt còn là bản cũ (chapters.txt L30 còn chữ "bốn nghìn" cho tới khi dựng lại; YAML thì đã sạch).

## Số liệu cổng (đo thật 2026-11-15)
| Bài | lint | từ lời đọc | render | verify_bnx | screen_fast |
|---|---|---|---|---|---|
| L24 | 0 FAIL 0 WARN | 2292 | 0 | 22/22 | PASS |
| L25 | 0/0 | 2294 | 0 | 16/16 | PASS |
| L26 | 0/0 | 2288 | 0 | 41/41 | PASS |
| L27 | 0/0 | 2289 | 0 | 21/21 | PASS |
| L28 | 0/0 | 2275 | 0 | 21/21 (PostgreSQL 17, MongoDB 8, MySQL 8.4, Oracle, SQL Server thật) | PASS |
| L29 | 0/0 | 2294 | 0 | 24/24 | PASS |
| L30 | 0/0 | 2285 | 0 | 22/22 (Resilience4j 2.3.0 thật) | PASS |
| L31 | 0/0 | 2297 | 0 | 21/21 | PASS |
| L32 | 0/0 | 2287 | 0 | 19/19 | PASS |
| L33 | 0/0 | 2292 | 0 | 15/15 | PASS |
| L34 | 0/0 | 2289 | 0 | 28/28 | PASS |
| L35 | 0/0 | 2292 | 0 | 28/28 | PASS |
| L36 | 0/0 | 2299 | 0 | 29/29 | PASS |
| L37 | 0/0 | 2295 | 0 | 24/24 (SQL Server + Java JDBC Oracle thật, không SKIP) | PASS |
| L38 | 0/0 | 2290 | 0 | 23/23 (Oracle thật) | PASS |
- `screen_fast`: L24–28 gộp 93 khối PASS 149 (FAIL/STALE/MISSING/ORPHAN 0); L29–33 PASS 24+26+32+22+26, mọi cột lỗi 0; L34–38 100 khối PASS 133, lỗi 0.
- Cổng toàn khoá BNX do các nhóm chạy: `tests/test_e52.py` 0 FAIL (chạy lại ở điều phối cuối: 0 FAIL); `arith_scan BNX` 58 phép 0 FAIL; `check_course_refs BNX` 0 vấn đề; `check_next_refs` 550 lời hẹn 0 lệch; `lab_gate BNX` 39 PASS 0 FAIL; `lv.py curriculum curriculum/bnx.yaml` 39 bài 0 lỗi (nhóm C và B báo). Lần chạy lại cuối khi đã sửa giáo án: xem mục "Cổng chạy lại cuối".

## MUST (3/3 đã sửa)
- **L30 hook**: "bốn nghìn" → "bốn trăm" (tiêu đề cảnh; grep YAML 0 chỗ còn). Màn hình và lời đọc đều nhất quán 400 và 40 000.
- **L30 example step 3**: lời đọc khớp nhật ký: 1500 bị chặn; 2000 cho thử một cuộc, hỏng nên mở lại; 2500 lại bị chặn; 3000 thử tốt nên đóng. `ver/l30.py` kiểm bằng bảng chuyển trạng thái Python viết riêng.
- **L37 example step 4**: thêm hai bước "Dựng lại bảng" (khối `MSS_BASE`) trước ⑤ và trước ⑥. Kiểm trên SQL Server thật qua `dbrun`: ⑥ chạy tiếp từ ⑤ in 1800000; dựng lại rồi ⑥ in 1300000. `ver/l37.py` có dòng kiểm mới.

## SHOULD (CONFIRMED) đã sửa, kiểm bằng mã thật
- L24: bể kết nối cạn vì giữ lâu (chỉ 1 kết nối trong giao dịch); thêm chương trình thật `DemTrang` cho phân trang + `join fetch` (HHH90003004, cắt trong bộ nhớ 1500 so với 60) và cách chữa.
- L25: REPEATABLE_READ ghi "trên H2" (Oracle ORA-02179; SQL Server khoá khiến UPDATE của B chờ, đo qua dbrun); hiện `chuyenKiem`/`chuyenKiemHoanTac`; điều kiện cho "300 luồng"; de.md và màn hình ghi "mô phỏng".
- L26: de.md và màn hình ghi "mô phỏng"; nhãn "cần" bị mũi tên gạch, dòng `for … done`; mục tiêu 6, 7.
- L27: điều kiện RAM cho "24 GB"; mục tiêu 2, 3.
- L28: thêm T-SQL (`SET LOCK_TIMEOUT 0` + `WITH (UPDLOCK, ROWLOCK)`) và hộp "`FOR UPDATE NOWAIT` báo Msg 1003" (đo thật); hook MongoDB hạ giọng.
- L29: trigger không chặn `INSERT OR REPLACE` và `DROP TABLE` (đo SQLite 3.49.1, thêm vào `ver/l29.py`), bài hạ giọng và nêu; nhãn hình 00016 không cắt.
- L30: `CauDao.java` hiện đủ nhánh quyết định (2 step); mũi tên hình 00016 chạm đúng hộp; mục tiêu 3 khớp bài.
- L31: `test.yml` đầy đủ, `$IMG` có giá trị; Grafana nói rõ chỉ ở mức khái niệm.
- L32: phân biệt mật khẩu tĩnh/thẻ/bí mật động; `s3:Get*` không phủ `s3:ListBucket`; `ChinhSach.py` có đường ra mặc định.
- L33: `Cu.java` đủ `EOF`, `javac -cp`, import jakarta; "dịch một lần" là mặc định; bỏ câu "bản cũ hết hỗ trợ bảo mật" (không nguồn).
- L34: bảng ngưỡng có bậc doanh nghiệp, "hội đồng"/"giám đốc khối" giảng tại chỗ, hiện `WHERE tt = ?`, lược đồ/BAC/HANG.
- L35: giả định P3 nêu rõ (42 < 43,2), bỏ "10 lần" không nguồn, dòng print tràn khung.
- L36: hằng số 10/2000/500 hiện; quiz 62,4 (62,5 nếu chưa làm tròn); `KhoaLuyDang.py` đủ câu; "231" là trung bình.
- L37: `public class Goi {`, nêu ojdbc và `BNX_PASS`, "ghép chuỗi chuỗi" lặp chữ.
- L38: không có SHOULD.

## P1 (chuẩn chặt)
Mọi mục trong danh sách P1 của R2 cho 15 bài đã có bảng "viết trong mã / đọc là / ví dụ nhỏ" (kèm lời đọc) ngay trước khối mã đầu tiên dùng cú pháp đó, hoặc định nghĩa tại chỗ; phụ thuộc chéo đã gỡ: L34 giảng `?` tại chỗ, L35 giảng "đối soát" tại chỗ, L37 bỏ mọi "bài 6" (bảng mô tả bảng/thủ tục thay vì tham chiếu). Không thêm mục `term:` nào. Hai `assumes` thêm vào (đều có bài tiên quyết đã giảng): L31 `bnx_ma_bam` (L26), L33 `bnx_sed_i` (L18).
Điểm P1 dự kiến: tự đánh giá 14–15/15 bài đạt 2; cần người đọc chấm lại. Rủi ro: cú pháp rất nền (`for`, `def`, `class`, `with`, `if`, `new`) không có bảng riêng; L37 mã tạo bảng/thủ tục Oracle `bnx_l06_*` chỉ mô tả bằng bảng (hết ngân sách lời đọc).

## Giáo án đã sửa (curriculum/bnx.yaml, Edit, `covers` không đổi)
- L26 mục 6, 7; L27 mục 2, 3; L30 mục 3 đổi cho khớp `objectives` của bài. Đã so sánh bằng mã 15 bài L24–L38: objectives giáo án = objectives bài.

## Việc điều phối cần làm (sổ/tệp dùng chung)
1. Gộp `audit/bnx/screen/l24..l38.yaml` (sinh bằng `screen_keep.py`, không mục viết tay, "chưa khớp 0") vào sổ chung `BNX.yaml` bằng cách điều phối vẫn dùng.
2. L28: `introduces=["bnx_explain"]` đã chuyển sang step `sym` (bảng thứ hai) trong bài; không thêm mục sổ.
3. Dựng lại 15 bài (tts, asr, render, build); ASR dò lại mọi câu `say` mới/đổi (byte, ln... theo báo cáo nhóm; nhóm C: "hàng đợi nâng cao", "bế tắc", "đối soát"; nhóm A/B: tên riêng như Hibernate, Tomcat, Argo, Vault, Resilience).
4. Khung PNG đã xem: nhóm A (L25 chỉ 2, L27 chỉ 1 khung; thiếu so với ≥ 3 mỗi bài) — người đọc kế tiếp nên xem thêm khung của L25 và L27.
5. `ver/l37.py` tạo DB `bnx_l37` (SQL Server) và bảng/thủ tục `bnx_l06_*` (Oracle) như vòng trước; không có đối tượng mới.

## Mục không sửa và lý do
- L26 khung nhấn 00033: không tái hiện sau khi sửa.
- L32: câu "mật khẩu tĩnh sống sau khi thẻ hết hạn" là suy luận từ chính ví dụ; không đổi chương trình Vault (sẽ đổi đầu ra thật trên màn hình). L32 example step 1 `ghi`/`buoc` chưa hiện đủ: ngoài danh sách báo cáo.
- L37 mã tạo bảng/thủ tục Oracle không hiện (xem P1).

## Cổng chạy lại cuối
Chạy lại ở điều phối sau khi sửa giáo án (2026-11-15): `lv.py curriculum curriculum/bnx.yaml` 39 bài, 39 có đặc tả, 0 lỗi; `tests/test_e52.py` 0 FAIL; `check_course_refs BNX` 0 vấn đề; `check_next_refs` 550 lời hẹn 0 lệch; `arith_scan BNX` 58 phép 0 FAIL. `lab_gate BNX` không chạy lại (nhóm C đã chạy: 39 PASS 0 FAIL; lab không đổi sau đó).
