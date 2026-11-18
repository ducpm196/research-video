# Lab INT L04 — Trả lời một câu phỏng vấn có số: bản đồ bit, khối PIN, vòng quay STAN, tin đang chờ (giấy bút, `loi_giai.md`)

Bài giấy bút: không chạy mã, và `cham.sh` không chấm tệp `.md`. Tính tay, ghi từng dòng đúng định dạng dưới đây, rồi tự so với `loi_giai.md`.

Số liệu (số minh hoạ, không phải số của ngân hàng nào):
- bản tin ISO 8583 chỉ có các trường **3, 7, 11, 41**; bản đồ bit gồm 64 bit, bit thứ k bằng 1 khi có trường k, đếm từ bit 1 ở ngoài cùng bên trái; viết ở hệ mười sáu (16 chữ số);
- khối PIN định dạng 0: PIN **5821**, số thẻ **5412345678901234**; trường PIN = `0` + độ dài PIN + PIN + đệm `F` cho đủ 16 chữ số; trường số thẻ = `0000` + 12 chữ số bên phải của số thẻ sau khi bỏ chữ số cuối cùng; khối PIN rõ là XOR từng chữ số hệ mười sáu của hai trường;
- một bên gửi **4 000** giao dịch mỗi giây; STAN có sáu chữ số (1 000 000 giá trị) và quay vòng đều; khoá khử trùng chỉ có STAN sống **300** giây;
- mỗi tin chờ phản hồi **1,5** giây.

Viết năm dòng:
1. `bitmap: <16 chữ số hệ mười sáu, chữ hoa>`
2. `khoi PIN: <16 chữ số hệ mười sáu, chữ hoa>`
3. `STAN quay vong sau: <số> giay` — 1 000 000 chia số giao dịch mỗi giây.
4. `chan nham: <co|khong>` — `co` khi STAN quay lại sớm hơn thời gian sống của khoá.
5. `tin dang cho: <số>` — số giao dịch mỗi giây nhân số giây chờ.

Tự kiểm bằng Python (không bắt buộc, sau khi đã tính tay): chạy `python -c "print(format(sum(1<<(64-b) for b in (3,7,11,41)),'016X'), 10**6/4000, 4000*1.5)"` để so bản đồ bit, vòng quay STAN và số tin chờ; khối PIN: `python -c "print(format(int('045821FFFFFFFFFF',16) ^ int('0000'+'5412345678901234'[-13:-1],16),'016X'))"`.
