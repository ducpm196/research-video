# Sửa BNX L30 theo R_BNX_L24_30 (nhánh L30)

Nguồn sửa: `audit/bnx/src/l30.py` (+ `audit/bnx/ver/l30.py`, `tools/checklib_bnx/l30.py`, nhóm L30 của `tools/registry/symbols.BNX.yaml`). YAML sinh bằng `gen.py L30`.

## P1 (thuật ngữ tại chỗ)
| Thuật ngữ | Chỗ giảng | E52 |
|---|---|---|
| luồng | prereq ④ "đồng thời và luồng": một dây việc chạy riêng, mỗi cuộc gọi chờ giữ một luồng (ví dụ 500 cuộc chờ = 500 luồng); nhắc lại tự đứng được (không phụ thuộc L25) | không đăng ký (L33 dùng 44 lần) |
| cổng API | formula step 5: cửa chung mọi yêu cầu từ ngoài đi qua trước khi vào các dịch vụ | không đăng ký (L36 dùng) |
| cân bằng tải | formula step 6: chia yêu cầu đến cho nhiều máy cùng làm một việc | không đăng ký (L32 dùng) |
| luỹ đẳng | pitfalls Lỗi 2: mã gắn vào lệnh, gửi lại nhiều lần vẫn chỉ xử lý một lần | không đăng ký (L36 dùng 35 lần) |
| burst | formula step 5: "đợt dồn (burst)" | `bnx_burst`, `introduces` ở step 5 |
| ngoại lệ | hàng sym giải thích; `assumes: [bnx_ngoai_le]` (L24 giảng, L30 ở chuỗi tiên quyết) | từ L24 |
Lý do không đăng ký 4 thuật ngữ: các bài L32/L33/L36 (af2, ngoài phạm vi) dùng cùng từ mà không đứng sau L30 trong bao đóng tiên quyết có `introduces` ⇒ đăng ký sẽ làm lint của họ FAIL.

## SHOULD
| Mục | Xử lý |
|---|---|
| `permittedNumberOfCallsInHalfOpenState(1)` không hiện | Cảnh `check` tách 3 khung mã `R4j.java` (import + cấu hình 10 dòng; vòng 6 cuộc hỏng; ngủ 1 100 ms + cuộc tốt + đầu ra thật). Bảng so thêm hàng "nửa mở thử mấy cuộc: phải đặt (1); mặc định cho thử nhiều hơn nên sau 1 cuộc tốt vẫn nửa mở". `ver/l30.py` biên dịch R4j bỏ dòng đó rồi chạy Resilience4j 2.3.0 thật: kết quả HALF_OPEN (PASS). |
| "mô hình đúng" quá mạnh | Lời: "thư viện đi đúng ba trạng thái ta vừa cài, nhưng chỉ ở kịch bản này"; "ba trạng thái giống nhau ở cấu hình đã chọn, chưa chứng minh đúng với mọi cấu hình". |
| "thử lại tối đa 5 lần" mơ hồ (tổng gọi vs thử lại) | Thống nhất: prereq ② "r lần thử lại = 1 + r lần gọi; tối đa 4 lần gọi = lần đầu + 3 thử lại" (khớp `toiDa` của ThuLai.java và 1 + r của formula step 3). Quiz 1: "gọi tối đa 5 lần (lần đầu + 4 thử lại)" → 750 ms; "nếu đề nói thử lại 5 lần" = 6 lần gọi → chờ thêm 800, tổng 1550 (đáp án hiện cả hai). |
| quiz 3: 95% từ chối, giả định 5 000 luồng | Bảng đáp án: "50 chỗ × giữ tối đa 2 giây nên chỉ ≤ 25 yêu cầu/giây qua được: ≈ 95% (475/500) bị từ chối; cuộc 3–4 giây vẫn quá hạn"; "5 000 luồng chờ nếu cuộc gọi treo tới hết hạn chót (chỉ chậm 3,5 giây thì ≈ 1 750)"; lời đọc nêu cần câu trả lời dự phòng. `ver` tính 25, 95, 5 000, 1 750. |
| CanBang.java trích không hiện thời điểm đến | Bỏ hai biến thừa (`het`, `hang`) ở nguồn, thêm chú thích "yêu cầu i đến lúc i × 10 ms", tách step: khung 12 dòng từ `static int[] chay` tới việc chọn máy; tiêu đề nêu 8 yêu cầu, việc đầu 100 ms, sau 10 ms; đầu ra không đổi (xoay vòng 2/1, ít kết nối nhất 1/1). |
| nhãn MÔ PHỎNG nhỏ; thiếu ở 00094 | Hộp lớn (cỡ chữ 1,25 em, khung đỏ) ở example step 1 ("MÔ PHỎNG: thử lại, cầu dao, xô token, cân bằng tải; THẬT: vách ngăn (luồng, Semaphore) và Resilience4j") và ở practice step 1 (đồng hồ giả, không ngủ thật); lời đọc nói "mô phỏng". Nhãn của L26/L27 thuộc nhánh khác. |
| số lời đọc mà màn hình không hiện (00086 "chín yêu cầu", tốc độ nạp; 00054 "sáu cuộc hỏng", "một giây mười") | Quiz đáp án câu 2 hiện "mỗi đợt 9 yêu cầu; xô đầy 4 token; nạp 1 token mỗi giây nên đến 2 000 ms thêm 2 token"; check hiện mã vòng 6 cuộc hỏng và `Thread.sleep(1100)`. |
| cột 3 trộn OPEN/HALF_OPEN/CLOSED | "mở (OPEN) → nửa mở (HALF_OPEN) → đóng (CLOSED)". |
| Không sửa: "cầu dao ba trạng thái mở sau 3 so 4 cuộc" (đã là dòng riêng trong bảng và lời đọc từ trước); lab (cổng chỉ so đầu ra, lời giải hard-code) — đề xuất lab chạy thư viện thật ngoài phạm vi 16 phút/mục tiêu. |

## Độ dài
Lời đọc 2 264 → 2 285 từ (≤ 2 300); thêm ~230 từ (luồng, cổng API, cân bằng tải, luỹ đẳng, 3 khung R4j, bảng đáp án) và cắt ~210 từ ở sym, intuition, formula, quiz, pitfalls, recap, quymo. `covers` giữ nguyên 7/7. Không cần đề xuất tách.

## Cổng thật (2026-11-13)
- lint 0 FAIL, 0 WARN (33 PASS); render 109 khung, 0 vấn đề (lần đầu 4 khung tràn ở formula step 6 → tách step).
- `verify_bnx.py L30`: 20/20 PASS (thêm: 1550 ms, 25/95%/5 000/1 750, R4j mặc định = HALF_OPEN).
- `gen-screen L30`: 15 khối, ghi 15, chưa khớp 0. `screen_fast.py L30`: PASS 25 · FAIL 0 · STALE 0 · MISSING 0 · ORPHAN 0.
- `lab_gate.py BNX`: 13 PASS · 0 FAIL.
- Khung đã xem: 00040 (CanBang), 00041 (nhãn MÔ PHỎNG), 00053, 00057 (check: cấu hình R4j, bảng so), 00093 (practice).
