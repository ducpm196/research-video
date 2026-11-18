# fix2_S01_FND — sửa khoá FND vòng 2 theo `reports/S01b_FND.md` — 2026-11-14

Nguồn sửa: `audit/fnd/src/l01..l10.py` → `audit/fnd/gen.py` (không sửa YAML sinh ra bằng tay). Không chạy build/tts/asr/audit_all/docker; không tải gì từ mạng. Có một lệnh `git diff --stat` chỉ đọc (để đếm tệp đổi), không ghi gì. Bài đổi lời đọc hoặc hình: L01 đến L10 (L00 không đổi); người điều phối dựng lại L01..L10 (TTS cho câu mới/đổi, ASR).

## Bản `sqlite3` đã dùng để kiểm
`sqlite3.exe` 3.46.0 (2024-05-23, 64-bit) mượn từ `C:\Program Files\NVIDIA Corporation\Nsight Systems 2025.1.3\host-windows-x64\`, chép vào scratchpad (`…\scratchpad\sqlbin\`), đặt vào PATH chỉ trong phiên chạy; KHÔNG chép vào kho. Mọi số "thật" dưới đây là chạy bằng bản này, không qua `audit/fnd/shim` (shim chỉ được `runner.py` tự thêm khi máy thiếu sqlite3; ở phiên này có sqlite3 nên không dùng). Người điều phối chạy lại `verify_fnd.py`, `lab_gate.py FND`, `screen_code.py check --course FND` bằng sqlite3 chính thức.

## MUST (1/1 đã sửa)
| Bài | Kiểm lại | Sửa |
|---|---|---|
| L08 ví dụ ② → ③, ⑤ và check step 1 | Đúng như báo cáo: phiên liền cùng `$DB`, ② đổi tên An thành An Le và xoá giao dịch 2, nhưng ③ ⑤ và check dùng các phiên riêng dựng lại từ `dung.sql` nên in `An`, `400000`, `1000000`. Phiên `PhienNH` giờ kéo dài thành MỘT phiên thật: sau ② có bước `rm -f $DB; sqlite3 $DB < dung.sql` (dựng lại, hiện trên màn hình trong khung ③, kèm câu giải thích và câu `say` mới), rồi ③ ④ ⑤ chạy tiếp cùng phiên (các bước 9 tới 13), và check step 1 hiện các lệnh 14 và 15 của chính phiên đó | `verify_fnd` chạy lại cả phiên: PASS, đầu ra từng bước khớp màn hình. Hook (`gd`) và pitfalls (`qwhere`, `nul`, `kgd`) vẫn là phiên độc lập, không nói là cùng phiên nên không mâu thuẫn |

## SHOULD (đã sửa 9/9 nhóm của báo cáo)
- L01, L03 "bốn điều" → "năm điều" (câu `say` mở rộng thành "Ta ôn lại năm điều đã biết trước khi vào bài." để đủ 8 từ).
- L02 hình `>`/`>>` (khung 00040): ô cao hơn (140 và 180 px), nhãn đưa lên trên đường nối bằng đường gấp khúc, không còn bị mũi tên cắt; đã xem khung PNG: không đè chữ.
- L06 "bốn kiểu giá trị" → "sáu kiểu: bốn kiểu đơn giản, cộng đối tượng và mảng" (bảng và lời đọc).
- L07: ví dụ đánh số lại ①..⑥, tiêu đề "sáu phép làm" (hết nhãn ④ trùng); check step 1 Cách 2 giờ cùng địa chỉ `/khong_co` với Cách 1: `curl -s -i $U/khong_co | head -n 1` ra `HTTP/1.1 404 Not Found` (phiên mới `PhienKiemMa`, chạy thật).
- L08: (a) formula step 4 và lời đọc nói hai bảng số dư dựng riêng, không cần khớp; (b) cảnh quy mô tách thêm 2 step: hiện `CREATE INDEX idx_id ON g(id)` rồi tra lại (kết quả giống hệt), và một khung giảng "tìm nhị phân" bằng lời thường (xem hàng giữa, bỏ nửa) kèm nói "chỉ mục thật của SQLite là cây B, số bước là cận trên theo tìm nhị phân"; tiêu đề cột bảng đổi thành "cận trên theo tìm nhị phân"; (c) giảng `.import` là lệnh riêng của sqlite3, và vì chưa có bảng nên dòng đầu thành tên cột (đã chạy thật: đếm ra 70 000).
- L09: bước 0 thêm `git config --global core.autocrlf false` (phiên `PhienCauHinh`, 4 lệnh) kèm một đoạn giải thích cảnh báo `LF will be replaced by CRLF` (nối với bài 5); thêm giảng "con trỏ" (mũi tên chỉ tới một lần chốt) và "tua nhanh" (gộp chỉ là dời con trỏ `main`), nói rõ hình vẽ trường hợp có chốt gộp còn ví dụ là tua nhanh.
- L04: hook hiện nội dung `chao.sh`; formula thêm "Bước 0" dựng `tien_ich/chao` và `hai/chao` bằng lệnh thật (`mkdir`, `echo … >`, `chmod +x`, `cat`; phiên `PhienTaoChao`, giảng `chmod +x` là quyền chạy).
- L05: hiện `loi.py`, `Quote.java`; cảnh check hiện cả lệnh `printf` tạo `crlf.sh` và `tr -d` (đường tạo tệp đầy đủ). Hai cảnh pitfalls và check tách step để khỏi tràn.
- L06: hiện `kh_ngoac.csv` (pitfalls 3) và `loi_nhay.json` (ví dụ ⑤).
- L10: `so_tay.sh` chia ba khung tự đủ (dòng 1 đến 9, 10 đến 17, 18 đến 21: mỗi khung tự đóng `EOF`, có ghi chú ghép liền thành tệp 21 dòng, không còn `EOF` mồ côi đầu khung); pitfalls 3 hiện đầu `so_tay_loi.sh` (khác `so_tay.sh` ở chỗ nào).

## P1 (thuật ngữ tại chỗ) — các mục biên của báo cáo
- L02 "biến": giảng ngay ở ví dụ ⑥ (lời thường: "cái tên mang một giá trị, như `DIR=du_an`").
- L08 "tìm nhị phân" và `.import`: giảng tại chỗ (xem trên).
- L09 "con trỏ", "tua nhanh": giảng tại chỗ (xem trên).
- Thêm (không bắt buộc): L03 `wc -l` đếm dòng, `wc -c` đếm byte; L07 "hàng đợi" (các yêu cầu xếp hàng chờ tới lượt) và "giãn dần khoảng cách" (chờ 1 giây, rồi 2, rồi 4); L10 "máy chủ cơ sở dữ liệu" (chương trình chạy sẵn, nhiều người hỏi qua mạng, như máy chủ ở bài 7); L04 `chmod +x`.
Điểm P1 dự kiến: 2 ở 11/11 bài (≥ 90%); P8 giữ 2 ở 11/11. NOT_VERIFIED: điểm do người đọc độc lập chấm lại. Không thêm mục sổ E52 mới (các thuật ngữ vừa giảng không bị bài khác của khoá dùng trước: lint E52 sạch).

## Lab L10 khi thiếu sqlite3
`loi_giai.sh` (từ `LAB_SOL` trong `l10.py`) thêm ngay trước phần SQL: `command -v sqlite3 > /dev/null || { echo "thieu sqlite3, cai theo bai L00"; exit 1; }`. Kiểm: chạy `loi_giai.sh` với `PATH=/usr/bin:/bin` (không có sqlite3) → in `thieu sqlite3, cai theo bai L00`, mã thoát 1, không còn in `LECH:`. `de.md` L10 ghi cùng điều. Với sqlite3 có mặt kết quả không đổi (`lab_gate` PASS).

## Cổng (số thật, sqlite3 3.46.0)
- `verify_fnd.py`: **78/78 PASS** (bản đầy đủ lần đầu; chạy lại L07 tới L10 sau sửa lời đọc: 25/25 PASS). Phiên mới: `PhienKiemMa` (L07), `PhienTaoChao` (L04), phiên L08 kéo dài (ba phiên cũ vẫn dùng cho hook và pitfalls), thêm `CREATE INDEX` vào `PhienQuyMo` L08, thêm `autocrlf` vào `PhienCauHinh` L09.
- `lv.py lint` cả 11 bài: **0 FAIL, 0 WARN** (lần đầu có 1 FAIL E29 "dòng N" ở L05/L10, 1 FAIL E31 focus L07, 3 WARN: đã sửa).
- `lv.py render`: **0 vấn đề** ở cả 11 bài (L05, L06, L10 lần đầu tràn khung ở pitfalls/check: đã tách step).
- Khung PNG đã xem: L02 (00040), L08 (00064 ③ dựng lại, 00090 tìm nhị phân), L09 (00036 con trỏ/tua nhanh), L04 (00037 bước 0), L07 (00069 check), L10 (00037 ba khung so_tay.sh). Không chữ đè/tràn.
- `audit/review/lab_gate.py FND`: **11 PASS · 0 FAIL**.
- `screen_code.py gen-fnd` (201 khối, chưa khớp 0; sổ cũ lưu ở scratchpad `FND_screen_code_before2.yaml`) + `check --course FND`: **PASS 290 · FAIL 0 · STALE 0 · MISSING 0 · ORPHAN 0** (với sqlite3 3.46.0 mượn nên không có 2 FAIL do thiếu CLI).
- `tools/lv.py curriculum curriculum/fnd.yaml`: 11 bài, 0 lỗi (giáo án không đổi: mục tiêu của bài không đổi). `audit/check_curricula_graph.py`: 46 lộ trình, 0 tham chiếu hỏng, 0 chu trình. `python tests/test_e52.py`: 0 FAIL. Thêm: `arith_scan.py` 240 phép, 0 FAIL; `check_course_refs.py fnd` 0 vấn đề; `check_xref.py` 14 lượt ở 2 tệp (BNX, không thuộc FND).

## Không sửa / ghi chú
- Nhận xét chung của báo cáo (nhãn SVG nhỏ 20 px, nửa dưới khung trống): không sửa, không phải lỗi, đổi bố cục toàn khoá ngoài phạm vi.
- L00: hướng dẫn các lựa chọn trong trình cài Git/JDK (báo cáo ghi là "chỗ thiếu", P1 vẫn 2) và mục "Git/Java/Python chỉ nêu là công cụ": không sửa vì không thể thử trình cài trên máy này, thêm chỉ dẫn từng ô lựa chọn sẽ là điều chưa kiểm được.
- L04 `cut -f1-2`, `2>&1`; L05 `sed -i`, `2>&1`; L06 "nén"; L07 `2>&1`: không sửa, P1 vẫn 2 và các lệnh này đã nằm ở gợi ý của lab hoặc đã giải nghĩa ở bài trước.
- `labs/cham.sh` (dùng chung JV2/JVA) vẫn còn nhánh dự phòng `sqlrun.py`: không đụng (như vòng 1).
- `check_next_refs.py` không chạy (như vòng 1: `pack.stages` chưa có PYT; FND không có lời hẹn "Bài sau (bài N)").
- Việc người điều phối: dựng lại 11 bài (TTS cho câu mới/đổi, ASR); chạy lại ba cổng có sqlite3 bằng bản chính thức.
