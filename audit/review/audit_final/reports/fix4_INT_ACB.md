# fix4 INT+ACB — sửa theo R2_INT_ACB (P1 thuật ngữ tại chỗ + SHOULD + QĐ 2345) — 2026-11-15

## Tiến độ: 18/18 bài đã sửa (4 mảnh, 2 đợt). TẤT CẢ 18 BÀI ĐỔI => CẦN DỰNG LẠI (build/tts/asr). Mới chạy lv.py render (khung PNG mới), chưa có mp4/srt mới; `chapters.txt` cũ của INT L06 còn tên cảnh cũ đến khi dựng lại.
Chi tiết từng bài: `fix4_INT_ACB_A.md` (INT L00–L03), `fix4_INT_ACB_B.md` (INT L04–L08, có đề xuất đổi tên L07), `fix4_INT_ACB_C.md` (ACB L00–L03), `fix4_INT_ACB_D.md` (ACB L04–L08).

## Cổng thật (điều phối chạy lại sau khi cả 4 mảnh xong)
- lv.py lint 18/18 bài: 0 FAIL, 0 WARN (INT 35/32/26/34/31/39/30/37/44 PASS; ACB 31/28/35/27/29/32/29/34/30).
- lv.py curriculum int.yaml và acb.yaml: 9 bài, 0 lỗi mỗi khoá. tests/test_e52.py: 0 FAIL.
- verify_int 208 PASS 0 FAIL; verify_acb 262/262 PASS. lab_gate INT 9 PASS, ACB 9 PASS (195 lab).
- screen_code INT: 60 khối, PASS 83, FAIL/STALE/MISSING/ORPHAN 0 (điều phối chạy lại). ACB: PASS 83, 0 FAIL (số của fork C và D; lần chạy lại của điều phối còn chạy nền).
- arith_scan 245 phép 0 FAIL (fork B, D); check_course_refs INT 0, ACB 0 (fork); check_legal (INT) 113 lượt dẫn 0 FAIL (fork B).
- Không còn TAB thật trong 18 YAML (grep -P "\t": 0).
- Lời đọc (tổng say, trước -> sau, trần 2300): INT 2236->2293, 1998->2146, 2016->2133, 2023->2157, 1963->2148, 2139->2257, 1898->1991, 1759->1794, 1875->2144; ACB 2066->2227, 1841->1917, 2076->2225, 1802->1947, ->1876, ->2259, ->2102, ->2242, ->2159.
- check_xref / check_meta / check_next_refs / lv.py build: không chạy (ngoài danh mục được phép).

## Đã làm (tóm tắt)
- P1: thuật ngữ nền giảng tại chỗ (lời đọc + màn hình) ở cả 18 bài; term mới INT: int_cong_tich_hop, int_chi_muc, int_luong, int_hex; ACB: acb_napas, acb_core, acb_tcp, acb_spring, acb_jms, acb_microservice, acb_consumer, acb_byte, acb_unique, acb_partition; `assumes` đã thêm cho các bài sau. Fork D không đăng ký thêm term cho L04–L08 (L06–L08 không là tiên quyết của nhau nên term mới buộc mọi bài dùng chữ đó tự giới thiệu); các từ được giảng bằng chữ tại chỗ. P1 dự kiến 2 ở phần lớn bài, chờ người đọc vòng 3 xác nhận.
- SHOULD: toàn bộ danh sách (TAB ACB L05, INT L06 tiêu đề minh hoạ, INT L07 hoà vốn k≈3,67, INT L03 nhãn Kafka, INT L02 pause/hook, bảng check ACB L01–L03 (L04, L06 cũng sửa), "ngưỡng chờ", "(số minh hoạ)" 50 nghìn, ACB L07 say vs O(N²), INT L08 cùng đơn vị, ACB L06 giả định/Luật 91/2025/QH15 hạ mức, INT L01 hook, nhãn SVG, ACB L08 chữ chạm viền, quiz ACB cân độ dài, pause check INT, quiz L00/L07 pause 25).
- QĐ 2345/TT 50/77: INT L05, L06 `source:` thêm TT 50 (đã được sửa đổi bởi TT 77/2025), QĐ 2345, ghi "chưa đọc nguyên văn", không bịa số điều; ACB L06 nêu 10/20 triệu "báo chí nêu, có nơi gắn QĐ 2345, có nơi gắn Phụ lục 02 TT 50, chưa đối chiếu Phụ lục sau TT 77".

## Không sửa / mở
- Việc cần người có văn bản gốc: đọc Phụ lục sau TT 77/2025 rồi ghi số điều/khoản ở CẢ INT L05, L06 và ACB L06 cùng lúc.
- Đổi tên `L07_salary_negotiation_50m_gross.yaml`: không làm; đề xuất ở cuối fix4_INT_ACB_B.md.
- P3 hình cơ chế (SAGA/Outbox/2PC/B-Tree, sơ đồ 4 tầng INT L06): chưa vẽ mới (ngoài danh mục). INT L08 lab chưa có bài hai con trỏ (bù bằng ví dụ chạy tay trên video; thêm vào lab phải đổi de/mong_doi/loi_giai).
- ASR: câu mới/đổi chưa nghe bằng tai người; 2 mục asr_reviewed mồ côi ở ACB L02 đã xoá.
