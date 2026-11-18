# Lab CS115 L00 — Chọn trọng số w bằng cách thử

Cần: Python 3 (không cần thư viện ngoài). Tạo tệp `thu_w.py`.

Mô hình giống bài: giá đoán = `w * diện tích + 2 * phòng - 1 * khoảng cách` (diện tích tính theo chục mét vuông, giá tính theo trăm triệu đồng). Hai ngôi nhà (số minh hoạ, khác các nhà trong bài):

| nhà | diện tích | phòng | khoảng cách | giá thật |
|---|---|---|---|---|
| P | 3 | 2 | 2 | 12 |
| Q | 8 | 1 | 3 | 26 |

1. Với mỗi w trong `2, 3, 4, 5` (đúng thứ tự đó), tính sai số bình phương của nhà P, của nhà Q và tổng hai số ấy. In một dòng dạng `w=<w> P=<số> Q=<số> tong=<số>` (số nguyên, không chữ thừa).
2. In dòng `w tot nhat: <w>` (w có tổng nhỏ nhất) rồi dòng `tong nho nhat: <tổng>`.
3. In dòng cuối cho biết w làm riêng từng nhà đoán đúng hoàn toàn, viết bằng phân số: `P dung khi w = <phân số>, Q dung khi w = <phân số>` (gợi ý: `from fractions import Fraction`, giải `w * diện tích + 2 * phòng - 1 * khoảng cách = giá thật` tìm w).

Chạy: `python thu_w.py`. Chấm (từ thư mục gốc của bộ khoá, nơi có thư mục `labs`): `bash labs/cham.sh CS115 L00 thu_w.py`.
