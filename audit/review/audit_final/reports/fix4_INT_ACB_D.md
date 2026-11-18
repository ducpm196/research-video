# fix4 ACB L04–L08 (fork D, đợt 2) — 2026-11-15

Cả 5 bài đổi => CẦN DỰNG LẠI (build/tts/asr): ACB L04, L05, L06, L07, L08. Mới chạy `lv.py render` (khung trong out/ACB/Lxx/frames là bản mới; chưa có mp4/srt mới).
Công cụ: sửa YAML bằng bộ sửa theo vị trí nút YAML (giữ CRLF, không sed/heredoc với dấu `\`). Không đụng L00–L03, INT, sổ chung, symbols.ACB.yaml.

## Cổng thật (sau khi sửa cả 5 bài)
- `lv.py lint`: L04 29 PASS, L05 32, L06 29, L07 34, L08 30; mỗi bài 0 FAIL, 0 WARN. `lv.py render`: 0 vấn đề (98/117/111/120/106 khung).
- `audit/acb/verify_acb.py`: 262/262 PASS (không phải sửa kiểm nào; chỉ chỉnh chữ nguồn L06 để không chứa "Điều N" theo kiểm có sẵn).
- `lab_gate.py ACB`: 9 PASS, 0 FAIL. `tests/test_e52.py`: 0 FAIL. `arith_scan`: 245 phép, 0 FAIL. `lv.py curriculum curriculum/acb.yaml`: 9 bài, 0 lỗi. `check_course_refs.py ACB`: 0 vấn đề.
- `screen_code.py check --course ACB`: 62 khối, PASS 83, FAIL/STALE/MISSING/ORPHAN 0. Cách làm: đổi khoá sổ tay `ACB L06 symbol 0 0` -> `1 0`, `ACB L07 symbol 0 0` -> `1 0` (+ `twin_of` của nguồn `L07_hmac`) vì thêm step giảng ở đầu cảnh symbol; chạy lại `audit/acb/gen_sc_acb.py` cho cảnh `code` L05 (thêm step).
- `grep -P "\t"` trên 5 bài: 0 dòng (TAB của L05 đã hết).
- `check_legal.py --strict` (chỉ báo cáo): 2 FAIL, đều ngoài phạm vi ACB: `50/2024/TT-NHNN` dẫn trơn ở `lessons/int/L05, L06` (fork B) và `23/2025/NĐ-CP` ở `interview/*.md`. ACB không có FAIL.
- Khung PNG đã xem: L04 21, 27, 62; L05 53, 65; L06 1, 14, 40; L07 29, 43, 97; L08 2, 21 (không tràn, không đè).

## Số từ lời đọc (tổng `say`; trần 2300)
| Bài | trước | sau |
|---|---|---|
| L04 | 1773 | 1876 |
| L05 | 2263 | 2259 (cắt 3 chỗ trùng để thêm gloss) |
| L06 | 1889 | 2102 |
| L07 | 2093 | 2242 |
| L08 | 2069 | 2159 |
Mọi câu mới 8–38 từ, không chữ Latin ngoài lexicon (lint 0 WARN).

## Từng bài
**L04** — `assumes` + acb_core. P1 tại chỗ (màn hình + lời): sổ cái (prereq.0), HTTP và mã 409/200 (concept.0, nhắc lại ở example.2), SELECT FOR UPDATE và khoá dòng (concept.1), adapter = bộ chuyển đổi trung gian (concept.2), Timeout = hết giờ chờ (check.0). Bảng check: hàng 3 "Gây thất thoát..." (hậu quả đặt dưới cột hành động) -> hành động sai thật "Đoán kết quả rồi hạch toán mà không hỏi lại T24". Quiz: A không còn dài nhất, nhiễu B/C/D hợp lý hơn.
**L05** — `assumes` + acb_napas, acb_core, acb_partition. TAB thật ở example.3 sửa: màn hình hiện `1 000 000 × 9 / 30 = 300 000` đúng (khung 53). P1: tiến trình = chương trình đang chạy (hook.0), thống nhất "luồng" -> "tiến trình"; PL/SQL = ngôn ngữ riêng của Oracle; mảng = danh sách xếp liền; thêm 1 step ngắn dạy cách kiểm vòng chờ (`cho.get(cho["A"]) == "A"`) vì lab đòi phát hiện vòng chờ (step chữ, không phải khối mã nên không vào sổ mã màn hình). Quiz cân độ dài.
**L06** — `assumes` + acb_core, acb_napas. Pháp lý: (a) hook.0: con số 10/20 triệu nêu là "báo chí/ngân hàng nêu; có nơi gắn QĐ 2345, có nơi gắn Phụ lục 02 TT 50, một nguồn thứ cấp nói còn điều kiện đi kèm (vd chuyển cho tài khoản người khác); bài chưa đối chiếu phụ lục sau TT 77/2025, chưa kiểm điều kiện" (màn hình + lời); bỏ "Phụ lục 01" khỏi màn hình; (b) `source:` viết lại cùng mức: TT 50 đã đọc bản gốc theo registry, phụ lục chứa 10/20 sau sửa đổi và số điều CHƯA đối chiếu, QĐ 2345 giữ nguyên "chưa đọc nguyên văn, chưa rõ còn áp dụng", không số điều; (c) "tổng cộng dồn về 0": giữ nhãn giả định, thêm câu "thực tế phải hỏi ngân hàng hoặc đọc văn bản hiện hành xem tổng ngày có được tính lại hay không" ở prereq.0 (màn hình + lời) và nhãn ở cảnh code; KHÔNG đổi lab/mong_doi (đủ bằng nhãn + cảnh báo); (d) "Không đưa số CCCD vào vé (Luật 91/2025/QH15)" -> "Nên tránh đưa số CCCD vào vé, theo nguyên tắc giảm thiểu dữ liệu (Luật ... 91/2025/QH15, chưa kiểm số điều)". P1: step mới đầu cảnh symbol giảng JSON, băm, chữ ký số; API/SDK (hook.1); chứng chỉ số/TLS (concept.1); 403 + API Gateway (check.1); so khớp một-một (example.1). Bảng check.0 cột "hệ thống yếu kém" sửa hai hàng thành hành động sai thật. Quiz cân độ dài.
**L07** — `assumes` + acb_napas, acb_core, acb_unique. Pitfall: lời đọc "nghẽn bộ nhớ" -> "thời gian đối soát tăng theo bình phương số bản ghi" (khớp O(N²)). Dấu hai chấm mồ côi cảnh quymo hết (rút câu dẫn). P1: step mới đầu cảnh symbol giảng HTTP (mã 200/500), POST/đường dẫn, header/payload; lệnh Redis `SET ... NX EX 120` (example.0); topic (example.1); B-Tree (pitfall, chỉ mục dạng cây); hash join (quiz.2). Quiz cân độ dài. Cắt câu quiz.2 quá dài (46 từ) thành hai câu.
**L08** — `assumes` + acb_core, acb_napas, acb_unique. Concept: "Chuyển tiền qua NAPAS 247" -> "Chuyển qua NAPAS 247", "Cấp hạn mức thấu chi CASA" -> "Hạn mức thấu chi CASA" (hết chạm viền hộp 4, khung 21). P1: sổ cái + phong tỏa (hook.0), CASA (prereq.0), tất toán (prereq.1, check.1), ghi chú AZ/CASA/Partial Debit/B2B dưới sơ đồ + lời về AZ và trích nợ từng phần (concept.0). Nhóm 2 (TT 31/2024): màn hình quiz.1 thêm "định nghĩa rút gọn... còn có trường hợp điều chỉnh kỳ hạn", lời thêm câu "Đó là cách nói rút gọn...". Quiz và phương án check cân độ dài.

## Mục không sửa / ghi chú
- Không thêm term mới vào symbols.ACB.yaml: L06/L07/L08 không có nhau trong bao đóng tiên quyết (và L04 không nằm trong bao đóng của L06–L08), nên term đăng ký mới (HTTP, băm, CASA, hash join...) sẽ buộc mọi bài dùng chữ đó phải tự `introduces`/`assumes`; các thuật ngữ đã giảng tại chỗ bằng chữ trên màn hình + lời đọc, `assumes` chỉ dùng term đã có (acb_core, acb_napas, acb_partition, acb_unique).
- L05 lab: không đổi; đã thêm step dạy cách kiểm vòng chờ.
- L06 lab/mong_doi không đổi (giữ quy tắc tổng về 0 như giả định đã gắn nhãn).
- INT/ACB nhất quán QĐ 2345: ACB giữ "chưa đọc nguyên văn, chưa rõ còn áp dụng", không số điều; ngày 18/12/2023 và 01/07/2024 chỉ "theo bài phỏng vấn đã lưu". INT L05/L06 `source:` do fork B (chưa kiểm).
- `asr_reviewed`: không xoá/đổi câu nào đã xem xét (giữ nguyên các câu gốc, chỉ thêm câu mới); câu mới/đổi cần ASR khi dựng lại.
- Chưa chạy `check_xref/check_meta/check_next_refs` (ngoài danh mục được phép của nhiệm vụ).
