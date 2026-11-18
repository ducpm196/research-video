# Lab INT L03 — Trả lời một câu phỏng vấn có số: xử lý lô lương và thời gian giữ khoá (giấy bút, `loi_giai.md`)

Bài giấy bút: không chạy mã, và `cham.sh` không chấm tệp `.md`. Tính tay, ghi từng dòng đúng định dạng dưới đây, rồi tự so với `loi_giai.md`.

Dòng nóng = một dòng dữ liệu (ví dụ tài khoản trả lương) mà rất nhiều giao dịch cùng cần khoá, nên chúng phải xếp hàng lần lượt.

Số liệu (số minh hoạ): lô lương **24 000** dòng; xử lý theo lô **2 000** dòng; mỗi dòng (hoặc mỗi lô) tốn **2** lần đổi ngữ cảnh giữa PL/SQL và SQL; đối tác trả lời mất **15 mili giây**; cam kết hai pha giữ khoá qua **2** vòng hỏi đáp; giao dịch cục bộ của SAGA giữ khoá **3 mili giây**.

Viết sáu dòng:
1. `so lo: <số>` — 24 000 chia 2 000.
2. `doi ngu canh tung dong: <số>` — 24 000 × 2.
3. `doi ngu canh theo lo: <số>` — số lô × 2.
4. `giu khoa 2PC: <số> ms` — 2 × 15 mili giây.
5. `toi da 2PC tren mot dong nong: <số> giao dich/giay` — 1 chia cho thời gian giữ khoá (giây), lấy phần nguyên.
6. `toi da SAGA tren mot dong nong: <số> giao dich/giay` — 1 chia cho 0,003 giây, lấy phần nguyên.

Tự kiểm bằng Python (không bắt buộc, sau khi đã tính tay): chạy `python -c "print(24000//2000, 24000*2, 12*2, 2*0.015, int(1/0.03), int(1/0.003))"` rồi so với sáu dòng (thời gian giữ khoá in ra bằng giây).
