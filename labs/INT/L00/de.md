# Lab INT L00 — Trả lời một câu phỏng vấn có số: tải, độ sẵn sàng, nhóm vai trò (giấy bút, `loi_giai.md`)

Bài giấy bút: không chạy mã, và `cham.sh` không chấm tệp `.md`. Tính tay, ghi từng dòng đúng định dạng dưới đây, rồi tự so với `loi_giai.md`.

Số liệu (số minh hoạ, không phải số đo của ngân hàng nào): cổng thanh toán nhận **8 000 giao dịch mỗi giây**; mỗi giao dịch ở lại hệ thống **25 mili giây**; mục tiêu sẵn sàng **99,95%**; một năm có 365 ngày. Tin tuyển dụng yêu cầu: JBoss, JSP, MS SQL, sở hữu một mảng nghiệp vụ, hỗ trợ mức 3 theo SLA (lưu ý: hỗ trợ mức 3 và bản thiết kế có ở cả hai nhóm nên không dùng để phân loại).

Viết ba dòng:
1. `dang xu ly do: <số>` — số yêu cầu đang xử lý dở cùng lúc (trung bình) = giao dịch mỗi giây × số giây ở lại.
2. `ngung toi da 99.95%: <số> phut/nam` — số phút ngừng tối đa mỗi năm.
3. `nhom tin tuyen dung: <A hoặc B>` — tin nghiêng về nhóm A (dịch vụ nhỏ hiện đại) hay nhóm B (hệ cũ và nghiệp vụ).

Tự kiểm bằng Python (không bắt buộc, sau khi đã tính tay): chạy `python -c "print(8000*0.025, round(525600*(1-0.9995),1))"` rồi so hai số với dòng 1 và dòng 2.
