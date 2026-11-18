# fix6 BNX_C (L26–L38, sửa theo R4_BNX_C, chuẩn P1 chặt) — bắt đầu 2026-11-16

## SỔ TÁC TỬ (ghi trước khi giao)
Người điều phối (tác tử này) chia 4 nhánh (fork), mỗi nhánh chỉ sửa `audit/bnx/src/lNN.py` (+ `ver/lNN.py`, `screen/lNN.yaml` qua `screen_keep.py`/`screen_fast.py`) của bài mình, sinh bằng `gen.py`, ghi báo cáo riêng:
| Nhánh | Bài | Báo cáo riêng |
|---|---|---|
| C1 | L26 L27 L28 | `fix6_BNX_C_p1.md` |
| C2 | L29 L30 L31 | `fix6_BNX_C_p2.md` |
| C3 | L32 L33 L34 | `fix6_BNX_C_p3.md` |
| C4 | L35 L36 L37 L38 | `fix6_BNX_C_p4.md` |
Không nhánh nào sửa `libj.py`, `lib2.py`, `lib.py`, `screen_code/BNX.yaml`, `curriculum`, registry dùng chung; mục riêng của bài (hàng bảng ngoài JROW) khai bằng bộ ba trong `lNN.py`. Việc chung do tác tử chính làm SAU khi nhánh xong: `screen_try.py --merge` (một lần), curriculum, check_curricula_graph, test_e52, lab_gate, arith_scan, tổng hợp báo cáo này.
Cấm: docker, dbrun.py, build/tts/asr/git.

Mã tác tử (giao 2026-11-16): C1=a898379e0da1c2045, C2=a1186591b675d9b57, C3=a815fd727d7bb24ed, C4=af84bf3195989a14a. Bị ngắt -> SendMessage tiếp.

## TIẾN ĐỘ
- [x] C1  - [x] C2  - [x] C3  - [x] C4  - [x] cổng chung

## KẾT QUẢ (chi tiết từng bài: fix6_BNX_C_p1..p4.md)
Bài đã đổi, CẦN DỰNG LẠI: cả 13 (L26 L27 L28 L29 L30 L31 L32 L33 L34 L35 L36 L37 L38). Lab không đổi.
| Bài | Lời đọc | Chưa giảng ước còn | asr_reviewed trước→sau | Ghi chú |
|---|---|---|---|---|
| L26 | 2294 | 0 | 1→1 | hiện đủ `M=`, `dung()`, `so()` (hai khung); ver 25/25; screen_fast PASS 38 |
| L27 | 2296 | 0 | 10→6 | đo SOAP/JSON cùng cách viết liền (203 byte, ≈10,2 lần; 246 ghi là tệp thụt dòng); ver 22/22; screen_fast PASS 25 |
| L28 | 2294 | 0 | 6→0 | bỏ `'` thừa; ver/screen_fast KHÔNG chạy (docker); sha 0 lỗi; dòng `var rut … modifiedCount;` sát mép phải (không đổi chữ khối Docker) |
| L29 | 2299 | 0 | 2→1 | nhãn "TÍNH TỪ CÔNG THỨC n mod k"; ver 24/24; screen_fast PASS 24 |
| L30 | 2299 | 0 | 16→3 | CanBang/QuyMo/ThuLai hiện đủ; bước 3 + 9 = 12; ver 22/22 (Resilience4j 2.3.0 thật); screen_fast PASS 29 |
| L31 | 2298 | 0 | 4→2 | ver 16/17 + 1 SKIP docker; screen_fast không chạy (docker); kiểm sha + Gate.check khối không docker PASS 18 |
| L32 | 2294 | 0 | 5→2 | hiện lệnh ghi thử, `sleep 6`, `git log --reverse --name-status --format=%s`; ver 15 PASS + 1 SKIP (Vault); khối Vault chỉ khớp sha |
| L33 | 2296 | 0 | 19→9 | `Tai.java` hiện đủ lớp; ver 15/15; screen_fast PASS 27; sửa thêm "(40 + 3) / 4" thành "43 chia 4 bỏ phần lẻ" (arith_scan) |
| L34 | 2280 | 0 | 6→5 | nhãn "MÔ PHỎNG: hai lần ghi nối tiếp"; ver 44/44; screen_fast PASS 27 |
| L35 | 2290 | 0 | 4→2 | import hiện đủ; dòng print tách; ver 28/28; screen_fast PASS 24 |
| L36 | 2299 | 2 | 3→1 | hiện `MUC`/`TU`; còn `DoiSoat` (`ghi_no, ghi_co = {}, {}`, `[i for i in ghi_no if i not in ghi_co]`) và `tao_hub`/`executescript` (R4 không liệt kê, hết chỗ lời đọc); ver 29/29 |
| L37 | 2295 | 1 | 8→3 | "(không đo ở bài này)"; ver KHÔNG chạy (SQL Server); chỉ sha |
| L38 | 2298 | 1 | 7→6 | ver KHÔNG chạy (Oracle); chỉ sha; hàm cục bộ `jt()` |

## Cổng chung (tác tử chính, sau khi nhánh xong)
- `screen_try.py --merge` (một lần): đã gộp vào `audit/review/screen_code/BNX.yaml`. ORPHAN cũ để nguyên. Chưa chạy `screen_code check --course BNX` đầy đủ (cần docker).
- lint 13/13: 0 FAIL, 0 WARN. render từng bài: 0 vấn đề.
- `lv.py curriculum curriculum/bnx.yaml`: 39 bài, 0 lỗi. `check_curricula_graph.py`: 0 lỗi. `tests/test_e52.py`: 0 FAIL. `lab_gate.py BNX`: 39 PASS, 0 FAIL (196 lab). `arith_scan.py BNX`: 60 phép, 0 FAIL (đã sửa 1 FAIL ở L33 quymo#6).
## Việc người điều phối còn lại
Dựng lại 13 bài (build/tts/asr, ASR các câu mới); chạy `ver/l28,l37,l38` (+ l31, l32 phần docker) và `screen_code check --course BNX` khi docker được phép; reader đo lại P1.
