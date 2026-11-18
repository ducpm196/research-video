# Lab INT L07 — Trả lời một câu phỏng vấn có số: so hai đề nghị bằng tổng đãi ngộ (giấy bút, `loi_giai.md`)

Bài giấy bút: không chạy mã, và `cham.sh` không chấm tệp `.md`. Tính tay, ghi từng dòng đúng định dạng dưới đây, rồi tự so với `loi_giai.md`.

Số liệu (số minh hoạ, không phải mức lương của ngân hàng nào; đơn vị triệu đồng): cả hai đề nghị đều có tháng 13 cố định và thưởng **k = 2** tháng lương. **Offer A**: lương cứng **38**, không phụ cấp. **Offer B**: lương cứng **34**, phụ cấp **2** mỗi tháng. Giả định thưởng và tháng 13 tính trên lương cứng, phụ cấp không được tính vào thưởng.

Công thức: T = L × (13 + k) + 12 × P.

Viết bốn dòng:
1. `offer A tong nam (k=2): <số> trieu`
2. `offer B tong nam (k=2): <số> trieu`
3. `chenh lech A hon B: <số> trieu`
4. `phu cap B can de bang A: <số> trieu/thang` — phụ cấp mỗi tháng P' để tổng đãi ngộ của B bằng của A (giữ nguyên lương cứng 34).

Tự kiểm bằng Python (không bắt buộc, sau khi đã tính tay): chạy `python -c "print(38*15, 34*15+12*2, 38*15-(34*15+24), (38*15-34*15)/12)"` rồi so bốn số với bốn dòng.
