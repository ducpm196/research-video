# Lab BNX L21 — Thẩm định một hồ sơ và băm hợp đồng

Viết chương trình Python `mau.py` cho hồ sơ sau (số minh hoạ, khác ví dụ trong bài):

- thu nhập 14 000 000, đang trả 3 000 000 mỗi tháng, khoản mới trả 3 000 000 mỗi tháng; nhóm nợ 1; làm việc 30 tháng.
- **Tỉ lệ nghĩa vụ** = (đang trả + khoản mới) × 100 / thu nhập; in một chữ số thập phân.
- **Điểm** = thu nhập từ 15 000 000 trở lên 35 điểm, thấp hơn 20; nhóm nợ 1 được 25, nhóm khác 0; làm việc từ 24 tháng 20, ngắn hơn 10.
- **Quyết định**: `TU_CHOI` nếu tỉ lệ vượt 50 % (so bằng nhân chéo: `(đang trả + khoản mới) * 100 > 50 * thu nhập`) hoặc điểm dưới 70, ngược lại `DUYET`.
- **Hợp đồng**: chuỗi `"Hop dong vay 14000000 dong, ky han 24 thang\n"` (có ký tự xuống dòng cuối). Băm SHA-256 bằng `hashlib` (`import hashlib`; `hashlib.sha256(chuoi.encode()).hexdigest()`), in 12 ký tự đầu của mã băm. Rồi đổi `24` thành `25` và đếm số vị trí (trong 64 ký tự) mà hai mã băm khác nhau.

In đúng năm dòng:

```
DTI: <số> %
Diem: <số>
Quyet dinh: <TU_CHOI hoặc DUYET>
Ma bam goc: <12 ký tự>
Vi tri khac: <số>
```

Chạy: `python mau.py`. Chấm: `bash labs/cham.sh BNX L21 mau.py`.
