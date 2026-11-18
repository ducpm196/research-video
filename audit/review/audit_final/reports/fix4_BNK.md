# fix4 BNK — sửa khoá BNK (L00–L14) theo R2_BNK, 2026-11-15

## TIẾN ĐỘ
- XONG cả 15 bài L00–L14 trong một phiên. Nguồn sửa: `audit/bnk/src/l00..l14.py` (khoá do máy sinh: sửa NGUỒN rồi `audit/bnk/gen.py`, không sửa tay YAML). Không chạy build/tts/asr/git/docker.
- **Bài cần dựng lại (build/tts/asr): cả 15 bài** (mọi `say` hoặc màn hình đã đổi; câu `say` mới/đổi là câu TTS mới; `asr_reviewed` cũ của câu đã đổi bị gen bỏ theo luật có sẵn, câu mới cần ASR lại).

## CỔNG THẬT (chạy sau lần sinh cuối)
| Cổng | Kết quả |
|---|---|
| `lv.py lint` 15 bài | 15/15: 0 FAIL, 0 WARN |
| `lv.py render` 15 bài | 15/15: 0 vấn đề (đã xem khung L06 intuition 39/48 và code 68, L13 SVG1 37, L03 prereq 14) |
| `audit/bnk/verify_bnk.py` | 48/48 PASS (thêm 4 dòng kiểm: L10 hai trường hợp hỏi trước, L11 bit 1 và range(2,65), L00 MB=1048576, L04 byte UTF-8) |
| `audit/bnk/screen_gen.py` + `screen_code.py check --course BNK` | 104 khối, PASS 152, FAIL 0, STALE 0, MISSING 0, ORPHAN 0 (sổ `audit/review/screen_code/BNK.yaml` đã sinh lại từ nguồn) |
| `audit/review/lab_gate.py BNK` | 15 PASS, 0 FAIL (195 lab được bài tham chiếu) |
| `tests/test_e52.py` | 0 FAIL |
| `lv.py curriculum curriculum/bnk.yaml` | 15 bài, 15 có đặc tả, 0 lỗi (mục tiêu không đổi nên không chạy lại `gen_curriculum.py`) |
| `check_course_refs.py BNK` | 0 vấn đề |
| `check_legal.py` | 1 FAIL duy nhất là INT L05/L06 (50/2024 dẫn trơn), KHÔNG liên quan BNK; BNK L13 vẫn ghi "sửa đổi bởi TT 77/2025" |
| `arith_scan.py` | 244 phép, 0 FAIL |
| `check_xref.py`, `check_meta.py`, `audit/check_curricula_graph.py` | không lỗi liên quan BNK (check_meta 0 vấn đề) |

## MUST / SHOULD
- MUST 1 (L10 chay_that "cả bốn trường hợp"): ĐÃ SỬA thành "cả hai trường hợp hỏi trước đều đúng một lần"; grep "cả bốn" toàn khoá: không còn; có dòng kiểm trong verify_bnk. Các bài khác không có câu tương tự.
- SHOULD (20): đã sửa hết.
  - L00: MB thống nhất 1 MB = 1048576 (RoRi.java chia 1_048_576, mảng 1_048_576, chạy thật true/false giữ nguyên); chú thích G1 thêm "từ 2 bộ xử lý và từ 2 GB bộ nhớ"; quiz câu 2 ghi "cùng heap ở câu 1".
  - L01: nói rõ `sleep` trong khoá chỉ để giả lập; cơ số 1000/1024 nêu ở ⑧ ("chính xác 1024, ta làm tròn 1000").
  - L02: hook tách hai nhãn (hàm ghi vết mang nhãn riêng).
  - L03: bảng khoá "64 byte mỗi dòng: khoá + phản hồi".
  - L04: byte ("1 byte cho chữ không dấu, 2–3 byte chữ có dấu", bỏ "tức mười sáu ký tự"); ghi chú dạng sqlrun.py khác dạng cây của `sqlite3`.
  - L05: cột "cặp gây bế tắc kỳ vọng (giả định)", xác suất 0,0001 nói đã gồm khả năng chồng thời gian.
  - L08: hook sửa lời hứa (hai dòng đầu đọc từ nhật ký bước, hai dòng sau từ cơ sở dữ liệu); Saga.java hiện đủ 18 dòng (import, class, main, `}`), chia hai khung, chạy thật khớp.
  - L09: cảnh check dùng `but_toan(gd, tien)` như cảnh chạy thật và lab.
  - L11: `range(2, 65)` (chữ, lời, mã nhất quán); PCI DSS: BIN 6 số, 8 số với thẻ từ 16 số, 4 số cuối, và nhật ký lưu lâu phải làm số thẻ không đọc được (nguồn trong chuỗi `source` thêm Req. 3.5.1; PLAUSIBLE, chưa kiểm bản PCI gốc vì kho không có).
  - L12: hook "ở phần chạy thật"; "phải qua bước duyệt" (quy trình điển hình).
  - L13: khối PIN "TDES với định dạng 0; AES đi với định dạng 4"; chi tiết "tính lại sau mỗi lần xác thực mạnh" BỎ khỏi chữ và lời, thay bằng nhãn CHƯA KIỂM (registry không có chi tiết đó); ngưỡng 10/20 triệu giữ nguyên nhãn CHƯA KIỂM như registry; SVG1 sửa (ô cao hơn, chữ tách dòng) — đã xem khung.
  - L14: thêm mẫu STAR đầy đủ (bảng S/T/A/R từ chính tình huống r7/r7b, ghi "minh hoạ, không phải sự cố có thật") ở cảnh sym; quiz câu 3 trỏ tới mẫu.
  - Hiển thị: L06 (nhãn mũi tên đặt riêng có viền, chú thích mã ngắn lại), L08 (nhãn "đọc sau", tiêu đề cảnh), L10 (nhãn "M7"/"tương quan = M7" đặt riêng), L01 (chú thích mã ngắn), L03 (mũi tên "tra" đổi hướng, "lần 3" nối bảng; cờ `-s` không tách dòng).

## P1 — thuật ngữ và cú pháp tại chỗ (đã làm, bài tự đủ, không có "như đã học ở khoá…")
- Cú pháp được giảng bằng 1 câu lời thường + ví dụ nhỏ ở cảnh prereq/sym hoặc ngay lời đọc của khối mã: L00 khung `class/main/for/println/import`, chuỗi, hàm, dịch vụ/yêu cầu/bộ xử lý, JDK 21 và cửa sổ lệnh; L01 `throws Exception`, `Runnable`, mili giây; L02 `interface/implements`, người nạp lớp, `Class<?>[]`, `(p, m, a) ->`, hàng đợi; L03 `throws IOException`, bản đồ chữ sang chữ, `java MayChu.java`, `WHERE`, máy chủ ở hook; L04 `SELECT *`, "tầng", tải, mở cửa sổ lệnh, hàm `abs`, nối tìm nhị phân với cây chỉ mục; L05 `try/catch/finally`, `boolean[]`, lambda, `?:`, `/` và `||` của PL/SQL, kiểu số, luồng; L06 `Map<Integer, Long>`, `1000L`, `%`, mili giây, nhóm kết nối, hàng đợi, t đệm = c; L07 `while/continue/!`, `?:`, hai vòng `for`, bộ đọc/Kafka ở hook; L08 `List/break`, UPDATE/INSERT/SELECT/khoá chính, Outbox giảng ngay ở hook; L09 UPDATE và khoá hàng giảng ngay ở pitfalls, số âm không phải nợ; L10 `?:`, `!`, chuỗi, hàng đợi và mã tương quan giảng ngay ở hook; L11 list comprehension, `range`, `|=`, `>>` trước `&`, `print/len`, băng thông, lấy mẫu, đặc tả; L12 `and/not in/==/!=`, `print` nhiều đối số, tải ×100, song song/tuần tự, byte/MB/GB; L13 `def/return/for/if/import/join/ljust/%d%s`, XOR giảng trước khi dùng, HSM/MAC giảng ngay ở hook; L14 `SELECT/FROM/WHERE/ORDER BY`, tài khoản đối ứng, sao kê, ngưỡng.
- Mã trên màn hình hiện ĐỦ khung `import/class/main` (chia khung ≤ 14 dòng; xác nhận bằng screen_code: khối trên màn hình là đoạn/đầu ra của nguồn chạy thật).
- Sổ: thêm 2 mục riêng BNK vào `tools/registry/symbols.BNK.yaml`: `bnk_outbox` (introduces L08 hook.1), `bnk_tuong_quan` (introduces L10 hook.0). Không sửa sổ/lexicon dùng chung. Không thêm `term:` cho từ phổ thông (dịch vụ, hàm...) vì sẽ buộc mọi bài khác khai lại.
- **Điểm P1 dự kiến: chưa đo, KHÔNG khẳng định đạt ngưỡng ≥ 90%.** Ước lượng thận trọng: 11–13/15 bài đạt 2; rủi ro còn lại là phần giảng cú pháp chủ yếu bằng lời đọc + bảng (người đọc độc lập cần đo lại). L00 vẫn dựa vào người học cài được JDK 21 (đã có hướng dẫn kiểm `java -version` ở màn hình và de.md).

## LAB
- Thêm khung chạy được vào de.md: L00 (PhiLech, JDK), L01 (TongBaLuong, thử bỏ khoá thấy mất cập nhật), L10 (GhepPhanHoi). L07 nhắc dấu cách đầu ` P`/` ngoi khong`; L12 mẹo `print` nhiều đối số.
- Kỹ năng cốt lõi chưa được lab chấm luyện → thêm "Phần thêm (không chấm)" kèm tệp chạy được trong thư mục lab (không đổi mong_doi chấm, lab_gate vẫn 15 PASS): L04 EXPLAIN QUERY PLAN trước/sau chỉ mục (de.md); L05 `be_tac/BeTac.java` (+ket_qua.txt) thử thứ tự khoá; L06 `ma_chan/MaChan.java` thử đổi mã chặn; L07 `ghi_nho/GhiNho.java` thử đổi chỗ sập; L11 hàm che số thẻ; L13 lab nay đòi cả hàm `che(so)` (loi_giai.py đổi, đầu ra vẫn `True/False/550000******5559`). Màn hình "Tự làm" của mỗi bài này nhắc phần thêm (+1–2 câu lời đọc).

## LỜI ĐỌC (số từ, `say`, tổng theo `lv.py lint`)
L00 2389 · L01 2367 · L02 2304 · L03 2260 · L04 2116 · L05 2382 · L06 2313 · L07 2301 · L08 2308 · L09 2077 · L10 2280 · L11 2326 · L12 2217 · L13 2361 · L14 2328 (trước sửa 2007–2299). **Mức ≤ 2300 chưa đạt ở 10/15 bài (L00, L01, L02, L05, L06, L07, L08, L11, L13, L14)** (vượt 1–4%, nhiều nhất L00 2389, L05 2382, L01 2367, L13 2361): bù bằng cắt các câu lặp nhưng phần giảng cú pháp P1 dài hơn phần cắt được mà không mất nội dung. Ước tính ≈ 15,3–15,8 phút ở 150–155 từ/phút (< 16 phút); nếu người điều phối muốn cứng ≤ 2300 thì cần một đợt cắt riêng.

## KHÔNG SỬA / CÒN MỞ (lý do)
- L00 P3: cảnh formula/example nói "ở hình trước" nhưng màn hình chỉ có chữ — chưa vẽ lại đồ thị A–F vào formula/example (không thuộc danh sách việc giao, và sẽ thêm ≥ 1 cảnh hình).
- L02 P3: chưa có hình cho REQUIRES_NEW và cạn hộp kết nối (như trên).
- L05 P7: mục tiêu 4 (xử lý ORA-00060) chỉ có chữ ở pitfalls, chưa có mã EXCEPTION/câu quiz vì Oracle không chạy được ở máy kiểm.
- L03 mục tiêu 3 (thiết kế bảng khoá) vẫn đưa sẵn DDL; L14 quiz câu 1–2 vẫn là tính số; L12 khung "kết quả mong đợi" vẫn chỉ hiện sau lúc dừng — chưa làm.
- L04: EXPLAIN không đưa vào phần CHẤM của lab (đổi đầu ra chấm), chỉ thêm ở "Phần thêm".
- Không nghe được âm thanh; không chạy `sqlite3` CLI (không có ở máy kiểm) nên câu "dạng cây của sqlite3" ở L04 là PLAUSIBLE.
- L11/L13 nguồn PCI DSS và TT 50/2024 chi tiết cộng dồn: chưa có bản gốc trong kho; đã hạ giọng/gắn nhãn thay vì khẳng định.

## TỆP ĐÃ ĐỔI
- `audit/bnk/src/l00.py … l14.py`, `audit/bnk/verify_bnk.py`; sinh: `lessons/bnk/L00..L14_*.yaml`, `audit/review/screen_code/BNK.yaml` (qua `audit/bnk/screen_gen.py`); `tools/registry/symbols.BNK.yaml` (+2 mục); `labs/BNK/L00,L01,L04,L05,L06,L07,L10,L11,L12,L13/de.md`, `labs/BNK/L13/loi_giai.py`, mới `labs/BNK/L05/be_tac/`, `labs/BNK/L06/ma_chan/`, `labs/BNK/L07/ghi_nho/`. `curriculum/bnk.yaml` KHÔNG đổi.
- Việc điều phối còn lại: dựng lại 15 bài (build, tts, asr), chạy `interview_gen_tables.py`/`interview_sync_video.py` nếu BNK L13 được INT dẫn; đo lại P1.
