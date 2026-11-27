# Bàn giao cho tác tử Antigravity — ghi lúc 2026-11-26 21:38 (+07)

Người dùng đã duyệt: cài bản sửa mất slide; Antigravity sửa, dựng lại và tiếp tục công việc.

## Hiện trạng (đã kiểm)
- `tools/lv_fast.py` đã đổi lúc 21:23:01 (sha256 2dd084764fdd4d59…): đưa ảnh khung RGBA về RGB trước khi ghép; video thiếu slide/hụt hình → đổi tên `*.broken.mp4` và build FAIL với dòng `[lv_fast] VIDEO HỎNG`.
- Hàng `build_queue.py` (khởi động 16:12) vẫn đang chạy và dùng bản mới từ DVO/L11. DVO/L11, L12, L13 đã kiểm đạt.
- Lỗi mất slide có sẵn từ `lv.py`, `verify` không bắt. Chi tiết: `KIEM_ANTIGRAVITY.md` cùng thư mục.
- Bạn không có hoạt động nào từ 16:42:56; hẹn giờ đặt lúc 16:31 không thấy báo về. Kiểm lại trạng thái thật trước khi làm.

## Ràng buộc
- KHÔNG dừng, không khởi động lại, không mở hàng thứ hai khi hàng đang chạy.
- KHÔNG sửa `tools/lv.py`, `tools/lv_fast.py` khi hàng đang chạy nếu người dùng chưa đồng ý.
- Dùng `tools/lv_fast.py` để dựng. `tools/lv.py` đã được sửa lúc 21:51:42 (người dùng yêu cầu): render đưa ảnh về RGB; `verify` FAIL khi video mất slide, nên 34 video hỏng cũ nay verify FAIL là ĐÚNG, không sửa cổng để cho qua.
- Quy tắc giọng: NamMinh trước; không ổn định thì cả bài VieNeu; không trộn.

## Việc 1 — làm ngay được: 3 bài BUILD_FAIL (hàng không quay lại)
CSA/L11, DEN/L04, DVO/L10, ESY/L03 (lỗi thêm lúc 21:49): render báo `nội dung TRÀN bảng` → tách step hoặc dùng `clear: true` trong tệp giáo án, giữ nguyên nội dung giảng và cổng lint.
Sửa tệp giáo án thì làm ngay; **dựng** thì đợi hàng xong (tránh tranh máy), lệnh:
`.venv\Scripts\python.exe -B tools\lv_fast.py build <tệp>` rồi `... lv_fast.py asr <tệp>`.
Xem lại log hàng xem còn BUILD_FAIL mới không và xử lý như trên. Xong: mỗi bài in `verify: ... PASS`.

## Việc 2 — SAU khi log hàng có dòng DONE: dựng lại video mất slide
Lúc 21:37 quét thấy 34 video hỏng: hàng sẽ tự dựng lại 20 bài; 14 bài hàng không quay lại:
BNX/L09, CLC/L11, CS115/L04, CVI/L09, DEN/L05, DEN/L07, DSC/L09, DSY/L00, DSY/L05, DSY/L11, DVO/L06, DVO/L07, PYT/L00, PYT/L13.
Danh sách đổi theo thời gian, nên lấy từ công cụ quét (đã thử phần lấy danh sách trên PowerShell 5.1):

```powershell
Set-Location D:\research-video
$bad = .venv\Scripts\python.exe -B audit\perf\fast_pipeline_20261126\fix_rgba\video_gap_scan.py | Select-String '^([A-Z0-9]+)/(L\d+):' | ForEach-Object { $_.Matches[0].Groups[1].Value + '/' + $_.Matches[0].Groups[2].Value }
foreach ($l in $bad) {
  $c, $id = $l.Split('/')
  $f = (Get-ChildItem "lessons\$($c.ToLower())\$($id)_*.yaml").FullName
  .venv\Scripts\python.exe -B tools\lv_fast.py build $f
  if ($LASTEXITCODE -ne 0) { "BUILD_FAIL $l"; continue }
  .venv\Scripts\python.exe -B tools\lv_fast.py asr $f
}
.venv\Scripts\python.exe -B audit\perf\fast_pipeline_20261126\fix_rgba\video_gap_scan.py
```
`asr` trả mã 1 nghĩa là có câu gắn cờ, không phải lỗi chạy.
Xong khi lệnh quét cuối in `hỏng 0` và mã thoát 0. Nếu một video dựng bằng bản mới vẫn bị báo hỏng: dừng việc này và báo người dùng.

## Việc 3 — theo quy trình sẵn có của bạn
- Xem xét cờ máy nghe (lúc 21:37: 84 bài, 484 câu trong đợt từ 16:12), rồi `af5_reviewer` cho các khoá đã dựng xong.
- Đặt lại hẹn giờ theo dõi hàng; sau mỗi khoá chạy `video_gap_scan.py <KHOÁ>`.

## Gợi ý sửa build_queue.py (không gấp; chỉ có hiệu lực ở lần chạy sau)
- Dòng bỏ qua ASR đang đếm bài còn cờ chưa xem vào `asr_ok`; nên đếm riêng.
- Thiếu vòng chờ 1 giờ khi cả hai giọng bị chặn như `audit/build_queue.sh`.

## Báo lại cho người dùng
Số bài BUILD_FAIL còn lại, kết quả lệnh quét (số video hỏng), số câu cờ đã xem xét. Không commit nếu người dùng chưa yêu cầu.
