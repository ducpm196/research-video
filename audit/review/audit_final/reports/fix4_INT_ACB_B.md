# fix4 INT phần B — INT L04–L08 (fork B, đợt 2, 2026-11-15)

Cả 5 bài đã đổi => CẦN DỰNG LẠI (build/tts/asr) L04, L05, L06, L07, L08. Mới chạy `lv.py render` (khung PNG mới; chưa có mp4/srt mới; `chapters.txt` cũ của L06 vẫn ghi tên cảnh cũ cho đến khi dựng lại).
Nguồn sửa: YAML viết tay (python thay chuỗi giữ CRLF), không đổi tên tệp. Không sửa L00–L03, không sửa ACB.

## Cổng thật (sau khi sửa xong cả 5 bài)
- lv.py lint cả 9 bài INT: 0 FAIL, 0 WARN (L04 31 PASS, L05 39, L06 30, L07 37, L08 44). lv.py render L04–L08: 0 vấn đề (90/97/89/89/97 khung).
- `lv.py curriculum curriculum/int.yaml`: 9 bài, 0 lỗi. E52: `tests/test_e52.py` 0 FAIL.
- verify_int: 208 PASS, 0 FAIL. Sửa 2 chỗ trong `audit/int/verify_int.py`: (1) trần lời đọc L04 2100 -> 2300 từ (trần mới của fix4; L04 đạt 2148, các kiểm ký tự giữ nguyên); (2) thêm kiểm "L08 bảng chạy tay hai con trỏ khớp mô phỏng thật" (mô phỏng lại 4 bước, dừng ở i,j = 3,3, còn dư 107 và 109, so từng dòng với YAML).
- lab_gate INT: 9 PASS, 0 FAIL. arith_scan: 245 phép, 0 FAIL. check_course_refs INT: 0 vấn đề (9 lỗi R4 "bài cuối khoá" ở L04 hook.1/recap.0 và L07 recap.1 là lỗi thật: L04/L07 không phải bài cuối; đã đổi thành "chuyên đề 8 của khoá").
- screen_code INT: 60 khối, PASS 83, FAIL/STALE/MISSING/ORPHAN 0. Đổi khoá sổ `INT L08 example 2 0` -> `4 0` (+ sha mới 66b027f2b1ca3bb9 và `twin_of` của `src:INT:L08_hai_con_tro`) vì chèn 2 step chạy tay trước mã giả, và mã giả có thêm dòng khởi tạo `i = 0; j = 0;` (viết dạng gán trung tính để vẫn là JavaScript hợp lệ cho `node --check`).
- check_legal: 113 lượt dẫn, 0 FAIL (lần đầu FAIL vì `source:` của L05/L06 dẫn "50/2024/TT-NHNN" trơn; đã đổi thành "đã được sửa đổi bởi Thông tư 77/2025 ... chưa đọc nguyên văn, cần đối chiếu bản hợp nhất"). 2345/QĐ-NHNN và 37/2025 vẫn CHUA_KIEM trong sổ (không đụng sổ).
- Khung PNG đã xem: L04 00017, 00024, 00070; L05 00010, 00016, 00028; L06 00014, 00022; L07 00044, 00045; L08 00050, 00053, 00059.

## Số từ lời đọc (tổng `say`, trước -> sau; trần 2300)
L04 1963 -> 2148 · L05 2139 -> 2257 · L06 1898 -> 1991 · L07 1759 -> 1794 · L08 1875 -> 2144. Mọi câu <= 38 từ, lint 0 WARN.

## Từng bài
**L04**
- P1 tại chỗ (màn hình + lời đọc): hệ mười sáu (prereq step 1: 16 ký hiệu, một chữ số = 4 bit, ví dụ 0011 -> 3) `introduces: int_hex`; XOR theo từng cặp chữ số hex có ví dụ số (3 XOR 1 = 2; 4 XOR 9 = D; cặp 34 và 19 cho 2D) ở prereq step 2, bù cho lab đòi XOR tay; "bể luồng chặn" giảng ở quymo step 1; Redis (kho khoá-giá trị chạy trong bộ nhớ) và UNIQUE (cột không cho hai hàng cùng giá trị, hàng thứ hai bị từ chối) giảng ở pitfall step 1 và quiz step 2.
- SHOULD: check step 0 phương án C và giải thích: 0400/0420 chỉ đảo khi biết chắc thất bại là điều kiện của luồng chuyển khoản 247 (cần kiểm đặc tả); với giao dịch thẻ đảo khi hết giờ chờ là thông lệ. Pitfall + quiz B: thời điểm trong khoá là thời điểm gốc (trường 7), giữ nguyên khi gửi lại.
- `assumes: int_luong`. R4: "bài cuối khoá" -> "chuyên đề 8 của khoá" (hook, recap).
**L05**
- P1: bảng prereq viết lại bằng lời thường (bỏ L1/L2/L3, bỏ tên Debezium; phân vùng bảng, Kafka, bộ giới hạn tốc độ, bắt thay đổi dữ liệu đều có chú thích; sinh trắc học = khuôn mặt, vân tay); đồng bộ/bất đồng bộ ở concept step 0 (màn hình + lời); tích vô hướng, độ dài véc tơ, "véc tơ = dãy số" ở symbol step 0 và step 2 (ví dụ 1·2 + 2·3 = 8; độ dài căn 5, căn 13); độ lệch chuẩn ở example step 1.
- Sơ đồ đường dẫn kép: thêm mũi tên nối nhánh -> kết quả và đầu vào -> nhánh; nhãn "Kafka topic payment.events" -> "hàng đợi Kafka, chạy ngầm". Font nhãn SVG ~ 21 px trên khung 1920 (đạt >= 20).
- `source:` thêm TT 50/2024/TT-NHNN (đã được sửa đổi bởi TT 77/2025/TT-NHNN; nguồn thứ cấp, chưa đọc nguyên văn, cần đối chiếu bản hợp nhất), QĐ 2345/QĐ-NHNN (chưa đọc nguyên văn, chưa rõ còn áp dụng, không nêu số điều), công thức UCB1 theo Auer, Cesa-Bianchi, Fischer 2002. Không bịa số điều/Phụ lục. `assumes: int_luong`.
**L06**
- P1: B-Tree ("chỉ mục dạng cây"), luồng ảo, SAGA, Outbox, CDC, Kafka có chú thích ngay trong bảng hook, bảng prereq và sơ đồ 4 tầng (nhãn SVG + ghi chú + lời đọc tầng điều phối/truyền dữ liệu); bỏ "thanh ghi"; kế hoạch truy vấn; bế tắc khoá, ORA-00060, tệp vết (.trc), Deadlock Graph giải nghĩa ở example step 0-1.
- Trung thực hồ sơ: tiêu đề cảnh example đổi thành "Khung kể một sự cố (ví dụ minh hoạ, không phải kinh nghiệm của bạn)" (cũng đổi `example:` trong `curriculum/int.yaml`); câu "Tôi lập tức..." thành "Hành động trong tình huống minh hoạ (câu mẫu, không phải kinh nghiệm của bạn)", lời đọc "trong tình huống minh hoạ này, người kỹ sư...".
- Bỏ "hỗ trợ mức 3" khỏi bảng hai nhóm vai trò (vẫn giải thích ở ghi chú; cho vừa khung), rút ghi chú. `source:` thêm TT 50/77, QĐ 2345 (như L05) và sách SRE (Google, 2016). `assumes: int_luong, int_chi_muc, int_cong_tich_hop`.
**L07**
- Quiz tính `pause: 5 -> 25`; check scene thêm `pause: 15`.
- Đòn 3: nêu điều kiện "cùng mức thưởng k thì 36 thua"; hoà vốn 36 x (13 + k) = 600 khi k ≈ 3,67; k = 5 cho 648; hỏi k có được bảo đảm không (màn hình + lời đọc). Thêm 2 phép `checks` (648; 3,67). Bỏ ô "Tâm lý nhân sự" thành chú thích trong tiêu đề để vừa khung.
- R4: "bài cuối khoá" -> "chuyên đề 8 của khoá".
**L08**
- P1: mảng/chỉ số/con trỏ/i++/vòng lặp giảng bằng ví dụ chạy tay trên hai danh sách (core 5 ô, napas 3 ô), tách 2 step (định nghĩa; bảng 5 bước) trước mã giả; mã giả có khởi tạo i, j. CASA ở prereq step 0 (màn hình + lời); "sắp xếp ngoài bộ nhớ" giải nghĩa ở quymo step 1; nhóm 2 TT 31/2024 ghi "định nghĩa rút gọn" (màn hình, lời, `source:`).
- Cùng đơn vị: nêu rõ vòng lặp lồng nhau tính MỘT cặp danh sách (đủ hai cặp thì gấp đôi), cột sắp xếp tính cả 3 danh sách (so sánh có lợi cho vòng lặp lồng nhau, kết luận không đổi). Không đổi số để khỏi đổi lab. Pitfall: "quy tắc kinh nghiệm" cho thời gian sống khoá >= 2 lần thời gian chờ. Thêm 2 phép `checks` cho bảng chạy tay.

## Term đăng ký mới (tools/registry/symbols.INT.yaml, chỉ thêm)
- `int_hex` (term `(?i)hệ mười sáu|\bhex\b`) — introduces ở INT L04 prereq step 1. Chỉ L04 dùng từ này trong dãy INT (đã grep).

## Mục không sửa và lý do
- L08 lab không có bài hai con trỏ (R2 ghi): thêm bài vào lab phải đổi `de.md`, `mong_doi.txt`, `loi_giai.md`, `cham.sh`/`lab_gate` — ngoài danh mục SHOULD được giao; bù bằng ví dụ chạy tay trên video.
- L04/L05/L06 P3 (hình cơ chế): chỉ L05 thêm mũi tên; L06 sơ đồ 4 tầng vẫn là danh sách xếp chồng (vẽ luồng dữ liệu là việc vẽ mới, ngoài danh mục).
- L06 tiêu đề bài "Bộ 100 câu" mà dạy 5 tình huống: lời đọc hook đã nói rõ; không đổi tên bài (đổi id/đường dẫn).
- L04 `0400/0420` đặc tả NAPAS: vẫn "cần kiểm", không có đặc tả để xác minh.
- L06 quy tắc "tổng về 0", Luật 91/2025/QH15: thuộc ACB L06 (fork D), không sửa ở đây.
- QĐ 2345 / TT 50 / TT 77: không đọc được nguyên văn nên không nêu số điều/Phụ lục; giữ nguyên "chưa đọc nguyên văn, chưa rõ còn áp dụng". Việc đọc Phụ lục sau TT 77/2025 rồi ghi số điều ở CẢ HAI khoá (INT L05, L06, ACB L06) cần làm cùng lúc, bởi người có văn bản gốc.
- Điểm P1 dự kiến: các thuật ngữ nền nêu trong R2 của L04–L08 đều đã giảng tại chỗ; kỳ vọng P1 = 2 ở L04–L08 (người đọc vòng 3 xác nhận).

## Đề xuất đổi tên `L07_salary_negotiation_50m_gross.yaml` (KHÔNG thực hiện)
Tên tệp chứa "50m" trái với lời bài "không đưa mức lương nào". Đổi thành `L07_salary_negotiation_total_comp.yaml` cần đổi cùng lúc: `spec:` trong `curriculum/int.yaml` (dòng L07), `audit/int/verify_int.py` (glob `L07_*` vẫn chạy), `audit/review/screen_code/INT.yaml` (khoá `INT L07 ...` theo id nên không đổi, nhưng kiểm tra `src:`), đường dẫn `out/INT/L07`, `audit/review/built_status.tsv`/`audit_all` và mọi chỗ tham chiếu tên tệp. `id: L07` giữ nguyên nên `out/INT/L07`, lab `labs/INT/L07` không đổi. Làm một lần bởi người điều phối cùng đợt dựng lại, sau khi dò `grep -rn "50m_gross"` toàn kho.
