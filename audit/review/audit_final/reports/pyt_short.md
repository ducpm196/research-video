# PYT: sửa câu NGẮN bị ASR gắn cờ (2026-11-14)

Nguồn sửa: `audit/pyt/src/lNN.py` (YAML sinh lại bằng `gen.py` qua `gates.sh`, không sửa tay). Mỗi câu mới đều >= 8 từ và <= 38 từ, giữ nguyên số/tên/mã trên màn hình.

| Bài | Câu cũ | Câu mới (cách sửa) |
|---|---|---|
| L00 #153 | Tạo một tệp chấm py. | Bây giờ tới phần bạn tự làm, tạo một tệp chấm py. (gộp câu trước) |
| L01 #84 | Máy báo lỗi thụt lề. | ...dòng hai kết thúc bằng dấu hai chấm, nên máy báo lỗi thụt lề. (gộp câu trước) |
| L02 #55 | Ta ráp lại thành một tệp. | Ta ráp lại thành một tệp, trong đó hàm tính thuế nhận giá và thuế suất mặc định mười. (gộp câu sau) |
| L03 #66 | Máy in tên kèm tổng tiền. | ...tra tên bằng khoá, rồi máy in tên kèm tổng tiền. (gộp câu trước) |
| L03 #109 | Chọn tập hợp. | Còn quyết định cuối thì thế này, ta chọn tập hợp. (gộp câu trước) |
| L04 #26 | Dấu phẩy ngăn hàng nghìn. | Dấu phẩy ngăn hàng nghìn, giúp số tiền lớn dễ đọc hơn nhiều. (thêm vế; focus giữ 6 mục) |
| L04 #41 | Chuỗi tiền có bốn ký tự. | Hình này giải thích vì sao số ký tự khác số byte, chuỗi tiền có bốn ký tự. (gộp câu trước) |
| L04 #61 | Chuỗi tiền có bốn ký tự. | Chuỗi tiền có bốn ký tự, mã hoá bằng quy ước phổ biến ra các byte. (tách lại câu sau cho khỏi quá dài) |
| L04 #91 | Bảng này cho thấy cái bẫy. | Bảng này cho thấy cái bẫy rất rõ qua thời gian chạy của từng độ dài. (thêm vế) |
| L05 #46 | Bước ba, đọc tệp bảng. | Bước ba, đọc tệp bảng, ở đây bộ đọc cho mỗi dòng một từ điển với khoá là tên cột. (gộp câu sau) |
| L05 #16 | Chế độ đọc là mặc định. | Lệnh mở nhận tên tệp, chế độ và bảng mã, trong đó chế độ đọc là mặc định. (gộp câu trước; focus bớt một mục "1.2": 8 -> 7 câu) |
| L06 #61 | In ra đọc được ngay. | In ra đọc được ngay, và hai giao dịch cùng nội dung bằng nhau, nhưng vẫn là hai đối tượng khác nhau. (gộp câu sau) |
| L08 #38 | Bước hai, gói. | Bước hai, gói, thư mục có tệp đánh dấu đặc biệt nên máy coi nó là gói, và cho nạp mô-đun bên trong bằng dấu chấm. (gộp câu sau) |
| L11 #56 | Bước bốn, gộp. | Bước bốn là gộp, với hai kênh và tỉ lệ thành công theo giao dịch nhỏ và lớn. (gộp câu sau) |
| L13 #100 | Thêm một tệp thư viện ghim. | Ngoài ra, thêm một tệp thư viện có dòng ghim phiên bản. (thêm vế) |

Tổng 14 câu theo danh sách (13 điểm L00..L13 ghi trong yêu cầu + L04 hai chỗ). Lưu ý: L05 `focus` của step "Bảng đầu là mở tệp" khớp lại số câu (7).

## Ghi chú Python 3.13 (L04, cửa sổ `>>>` đầu tiên có traceback)

Phiên `>>>` đầu tiên có traceback hiển thị trong PYT là L04 (Bước 1, `R_FIX`: `s[0] = "C"`); `R_TUPLE` ở L03 chỉ dùng để verify, không hiện trên màn hình. Thêm một step ngắn ngay sau Bước 1 (khung `box key`, `clear: true`): màn hình ghi "Python 3.13 trở lên: cửa sổ >>> in lỗi dạng <python-input-N> kèm dòng mã; khi chạy tệp .py thì giống video. Nội dung lỗi giống nhau." Lời đọc một câu (không dùng từ khoá tiếng Anh vì `SAY_FORBIDDEN`): "Lưu ý, vì từ phiên bản ba chấm mười ba cửa sổ gõ lệnh in lỗi kèm dòng mã, nên hình có thể khác video, còn chạy tệp thì giống, nội dung lỗi vẫn thế." Không đổi đầu ra mà `verify_pyt` kiểm.

## Cổng

- `gates.sh` L00, L01, L02, L03, L04, L05, L06, L08, L11, L13: verify PASS, gen ghi YAML, lint 0/0, render 0 vấn đề, lab_gate 14 PASS 0 FAIL.
- Hai lần đầu L04 và L11 FAIL verify ở phép đo thời gian (`l04_redos`, `l11_plot`: lệch quá x8) do máy đang chạy nhiều tiến trình; chạy lại khi máy rảnh thì PASS (L04 15/15, L11 9/9).
- Vòng sửa L04: lời đọc ban đầu có chữ "Python"/"input" bị gen từ chối; câu quá 38 từ (lint WARN); khung tràn bảng khi nhét ghi chú vào Bước 1, nên tách step riêng; thiếu từ chỉ lý do (lint WARN) nên thêm "vì ... nên". Cuối cùng L04 sạch.
- Toàn khoá: `verify_pyt.py` 183/183 PASS; `lv curriculum curriculum/pyt.yaml` 14 bài, 0 lỗi.
- `screen_code check --course PYT`: lần đầu STALE 2 / MISSING 1 / ORPHAN 1 vì step ghi chú mới ở L04 làm lệch chỉ số step trong sổ mã; chạy `screen_code.py gen-pyt` (tái sinh sổ từ nguồn) rồi check lại: PASS 474, FAIL 0, STALE 0, MISSING 0, ORPHAN 0.

Việc còn lại cho người dùng: câu `say` đổi là câu TTS mới, cần chạy lại TTS/ASR cho 10 bài đã đổi (L00-L06, L08, L11, L13).
