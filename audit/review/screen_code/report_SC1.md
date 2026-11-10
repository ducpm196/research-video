# report_SC1: cổng "mã trên màn hình chạy được nguyên văn" (việc 1), 2026-11-10

**Kết luận: `DONE`** cho phạm vi đã cam kết ở `plan_SC1_20261110T1047Z.md`. Mọi khối mã người học thấy trong 656 bài đều đã được kiểm nguyên văn; lỗi nghiêm trọng tìm thấy đã sửa và video đã dựng lại.
Phần ngoài phạm vi vẫn **chưa** được bảo đảm, xem §5.

## 1. Kết quả cổng (OBSERVED)
- `screen_code.py check -v` (log `logs/check_all_final.out`, checked_at 2026-11-10T12:42:16Z): **541 khối — PASS 724 · FAIL 0 · STALE 0 · MISSING 0 · ORPHAN 0 · WARN 0**. Con số 724 gồm 541 khối và 183 nguồn chạy thật.
- `audit_all.py` toàn kho, đã gồm cổng mã màn hình của từng khoá (log `logs/audit_all_final.out`, xong 2026-11-10 ≈13:08Z): **656 bài, 656 đã dựng, 0 bài có vấn đề**.
- `negative_controls.py`: **30/30 ca đúng kết luận**. Các loại lỗi cấy: cú pháp, thiếu hàm, sai kết quả, khẳng định trống, thiếu lý do, đoạn trích không thuộc nguồn, đầu ra sai, đầu ra là chuỗi con, dòng cắt cụt không có "…", sqlite, C có hoặc không có chú thích, node, go, java, stderr có "…". Mỗi loại kèm ca dương để chứng minh nhánh kiểm chạy thật.

### Số khối theo kiểu kiểm
| kind | khối | nghĩa |
|---|---:|---|
| run | 121 | chạy nguyên văn: python 88, sqlite 23, node 6, bash 3, go 1. Mỗi khối có khẳng định kết quả bài nói |
| fragment | 198 | đoạn trích. 190 khối JVA được chứng minh là dãy dòng liên tiếp của một trong 110 chương trình chạy thật |
| output | 117 | khối đầu ra, so **cả dòng** với kết quả chạy thật |
| syntax | 20 | chỉ kiểm cú pháp: C 10 (pycparser), java 5, node 2, python 2, go 1 |
| pseudo | 42 | mã giả tiếng Việt. Điều bài nói kiểm bằng bản Python dịch sát (`twin_of`), độ trung thực INFERRED |
| other | 43 | định dạng không có trình kiểm (bit/CRC, hợp ngữ, PL/SQL, ksql, HTTP, Dockerfile, OFS…). Có `read_check`; phần lớn được một nguồn Python đọc nguyên văn để tính lại |
| **Tổng** | **541** | |

Điều bài nói mà máy **không** kiểm được (NOT_VERIFIED): **122**, liệt kê đủ trong `logs/check_all_final.out`, dòng `NOT_VERIFIED`. Lý do chính:
- mã C không chạy được (máy không có trình biên dịch C);
- hệ thống ngoài: Redis/Spring/Oracle/Kafka/Cassandra/Docker/EVM/RTOS;
- bản dịch mã giả có độ trung thực INFERRED.

## 2. Lỗi đã sửa trong bài (theo bằng chứng chạy máy)
**MUST: 17 lỗi (tính theo khối) ở 15 bài** (đếm lại bằng Python). Mỗi lỗi là mã trên màn hình không chạy được, hoặc khác điều bài nói / khác điều máy in:
| Bài | Lỗi cũ | Bằng chứng |
|---|---|---|
| SDP L02 | lớp `TaiKhoan` thiếu `nap`, trong khi bảng và quiz dùng | AttributeError |
| SDP L04 | `class CaPhe:   def gia…` viết một dòng | SyntaxError |
| SDP L03 | thiếu `import math`, `__init__`, `TamGiac`, `cac_hinh` | NameError/TypeError |
| SDP L06 | thiếu `__init__`, mà bảng ghi "cao 0" | AttributeError |
| SDP L07 (2 khối) | thiếu `from datetime import date` | NameError |
| SDP L08 | lớp `Dem` chỉ có trong `checks` | NameError |
| SDP L11 | `{…, ...}` | SyntaxError |
| SDP L12 | thiếu `import functools` | NameError |
| PLC L11 | `return` ngoài hàm | SyntaxError |
| PLC L12 (2 khối) | thiếu `reduce`, `lru_cache` | NameError |
| CVI L00 | thiếu `import numpy as np` | NameError |
| WEB L04 | `const u` khai báo hai lần | SyntaxError |
| ACB L04 | `fiber.Map` thiếu dấu phẩy | gofmt: missing ',' |
| JVA L00 | thông báo javac trên màn hình khác máy in | javac 22.0.2 in `class Chao is public, should be declared…` |
| JVA L11 | như trên | javac 22.0.2 in hai dòng `phi(long) in MienPhi cannot implement…` |

**SHOULD: 6 lỗi đã sửa.**
- ACB L04: `RowsAffected()` trả `(int64, error)`.
- WEB L06: giá trị Idempotency-Key cần nháy kép.
- ESY L01: chú thích ghi giá trị thanh ghi sai.
- CS112 L25: `find` viết một dòng làm `return` rơi vào nhánh `if`.
- JVA L08: dòng lỗi bị cắt mà không có "…".
- GFX L12: nhãn "8 ô".

Các sửa liên quan: `audit/jva/lib.py` (`out_block` hiện thông báo javac nhiều dòng), `audit/jva/verify_jva.py` (so cả dòng, hiểu "…"), mẫu `.tpl` của PLC L11 và CS112 L25.

## 3. Kiểm sau sửa (OBSERVED)
- **Dựng lại 17 bài** (đếm lại bằng Python), tất cả PASS, ASR chưa xem xét 0, một giọng:
  - JVA L00, L08, L11
  - PLC L11, L12; CVI L00; ACB L04
  - SDP L03, L06, L07, L08, L11, L12
  - WEB L04, L06; ESY L01; CS112 L25
  - (SDP L02, L04 và GFX L12 đã dựng ở lượt mẫu E trước đó)
  - Log ở `logs/rebuild_*.out`.
- **Bộ kiểm khoá** đều 0 FAIL:

  | Bộ kiểm | Kết quả |
  |---|---|
  | verify_sdp | 36 PASS |
  | verify_web | 16/16 |
  | verify_plc | 72/72 |
  | verify_cvi | 112/112 |
  | verify_esy | 72/72 |
  | verify_cs112 | 38 PASS / 15 FIX / 0 FAIL |
  | verify_cs112_p2 | 37/0 |
  | verify_jva | 110/110 (so cả dòng) |
  | verify_gfx | 19/19 |
  | verify_dbs | 42/42 |

- Cổng phụ: check_xref 0, check_meta 0, scan_ctrl 8 (JVA cố ý).
- `status_report`: 656/656 bài hoàn thiện, 5927 phút.
- Video phỏng vấn: `interview_sync_video.py --check` cho 92/92 cặp trùng byte. `interview_gen_tables.py`: tổng 361,02 phút (không đổi).
- Chữ cổng trích ra khớp từng dòng với khung hình thật: SDP L02 khung 00023, CAS L03 khung 00062, JVA L11 khung 00059.

## 4. Kiểm độc lập (CB-3, CB-4)
2 tác tử mới, chỉ đọc, xét 304 mục sổ cùng 20 bài đổi (`verify_AB.md`). **Không có MUST, không có mục NÉ.**
- 9 phát hiện về sổ hoặc cổng đã sửa:
  - cổng so cả dòng thay cho chuỗi con;
  - 3 mục CHE, 3 mục LỎNG, 2 mục THIẾU;
  - `twin_of` dạng danh sách.
- 1 lỗi bài (JVA L08) đã sửa.

## 5. Còn mở (không thuộc "lỗi nghiêm trọng", hoặc ngoài phạm vi)
- **SHOULD mở**, mỗi mục cần sửa bài + dựng lại, chờ người dùng chọn:
  - INT L00/L02: dòng `//` trong khối lệnh redis-cli.
  - INT L02: `redis` phải là lớp bọc của ứng dụng (Spring không có kiểu nào đủ ba hàm).
  - ACB L03: định tuyến khi hồ sơ NULL.
  - ACB L04: `NOW()` với mốc mili giây, bài không nêu hệ quản trị.
  - ACB L07: header ghép bằng `|`.
  - CSA L16: chuỗi Spectre của nhân mới là "Enhanced / Automatic IBRS".
  - SDP L08: không hiện lớp YeuCau; SDP L12: lời đọc "một dòng".
  - CS112 L10: "/" là chia nguyên nhưng bài không nhắc lại.
  - ESY L11: tên hàm RTOS là tên chung.
- **Contract bottleneck CB-2 (OPEN)**: máy không có trình biên dịch C. 10 khối C mới kiểm được cú pháp; kết quả của chúng chỉ kiểm bằng bản Python đối chiếu. Phép thử đóng: cài trình biên dịch (ví dụ LLVM/clang), thêm `run/c` vào cổng, chạy lại.
- **CB-5 (OPEN)**: hệ thống ngoài không có trên máy; 122 NOT_VERIFIED ghi rõ.
- **Ngoài phạm vi việc 1**:
  - mã nội dòng `<code>` trong câu, chữ trong SVG;
  - **lỗi nội dung không phải mã**. Mẫu E đo được 2/42 bài có MUST (Wilson 1,3–15,8%). Việc 1 không chứng minh "không còn lỗi nghiêm trọng nào" cho loại này.

## 6. Cách giữ kết quả (bền vững)
- `audit_all.py` nay chạy cổng cho từng khoá. Đổi một ký tự của khối mã → sha lệch → STALE → audit_all báo vấn đề, tới khi mục sổ được kiểm lại.
- JVA: sau khi sửa `audit/jva/src` thì chạy `gen.py` → `screen_code.py gen-jva` → `check --course JVA`.
- Khoá khác: sửa khối → `screen_code.py show` → cập nhật `sha` và khẳng định trong `audit/review/screen_code/<KHOÁ>.yaml` → `check --course X`.
