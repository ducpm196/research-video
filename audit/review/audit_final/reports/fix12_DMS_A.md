# fix12 DMS L00–L10 (sửa theo R8_DMS_A) — 2026-11-17

Không chạy build/tts/asr/render/git/docker. Không thử được `lv.py render` (lệnh render bị từ chối quyền ở lượt trước, không đi vòng): khung chưa xem; mọi bảng thêm đều ≤ 4 hàng/step.

## Bài đổi (requeue) và việc đã làm
| Bài | Việc | Từ |
|---|---|---|
| L01 | practice: thêm step bảng cú pháp (3 hàng) `from itertools import product`, `product((True, False), repeat=n)` (đọc `repeat=n`), `f(*dong)` có `clear: true`; lời đọc gợi ý trỏ tới bảng; bỏ câu "đã giải thích trong de.md" | 2205 |
| L03 | quymo: thêm hàng `if điều_kiện:`; bảng tách 3 + 3; mã in thêm tổng số cặp (`tong`) cạnh `dem`, nhãn "co ... cap tong chan" suy ra được từ số in; SHOULD "số thực không thuộc ℚ" (chữ + lời); bỏ câu chào cuối recap để vừa 2300 | 2281 |
| L04 | practice: thêm hàng `def tong(n): … return …` vào bảng gợi ý + một câu lời đọc | 2186 |
| L05 | quymo: thêm hàng `if điều_kiện:` (bảng 8 hàng tách 4 + 4, đổi "bảy" thành "tám ký hiệu") | 2117 |
| L06 | "nhị phân = viết bằng hai chữ số 0 và 1" ở hàng bảng + lời đọc; practice: step bảng thêm (3 hàng) cho từ điển `{1: 'a', 2: 'b'}`, `from itertools import combinations`, `for chon in combinations(range(1, 13), k):`; gợi ý trỏ tới bảng; cắt bớt câu để giữ ≤ 2300 (câu "Giải pháp bảng cố định…", "Hẹn gặp bạn…", vài cụm) | 2288 |
| L07 | quymo: thêm hàng `if điều_kiện:` (bảng 7 hàng tách 4 + 3) | 2260 |
| L08 | quymo: thêm hàng `if điều_kiện:` vào bảng "đợt hai" (4 hàng) | 2239 |
| L09 | SHOULD "2 ngày" / "2,5 ngày": ghi chú trên màn hình "máy bỏ phần lẻ: 2 ngay nghĩa là hơn 2 ngày, thật ra khoảng 2,5 ngày" + lời đọc "máy bỏ phần lẻ, nên hiện 2 ngày, thật ra khoảng hai ngày rưỡi" | 2090 |
| L10 | practice: step bảng thêm (4 hàng) `def pascal(n)… return`, `from math import factorial`, `for nhom in combinations(nguoi, 3)`, `d = [[1] * 5 for _ in range(4)]` + `d[r][c]`; bỏ một câu thừa ở quymo.2 và mệnh đề chú giải để giữ ≤ 2300 | 2285 |
| L00, L02 | không đổi | — |

Nguồn sửa: `audit/dms/af2/l01,l03…l10.py` (sinh lại bài) và `fix6lib.py` (thêm `add_read_step`); bài `lessons/dms/*` sinh lại từ script. Số mục chưa giảng ước còn lại: 0 cho 10 mục chắc+vừa của reader (mục "yếu" ngoài phạm vi yêu cầu không động tới).

## Cổng
lint từng bài L00–L10: 0 FAIL, 0 WARN. curriculum dms: 21 bài, 0 lỗi. test_e52: 0 FAIL. verify_dms: 324 PASS · 0 FAIL. screen_code DMS: 72 khối, PASS 95, FAIL/STALE/MISSING/ORPHAN 0. lab_gate DMS: 21 PASS. arith_scan: 258 phép, 0 FAIL. Số hàng tối đa mỗi bảng đọc mã sau sửa: L00 và L02 6 hàng (hai bài đã dựng thành công, không đổi), các bài khác ≤ 4.
