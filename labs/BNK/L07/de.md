# Lab BNK L07 — Bảy phân vùng, chín bộ đọc

Một chủ đề có **7 phân vùng** `P0 … P6`, một nhóm có **9 bộ đọc** `0 … 8`. Chia đều: mỗi bộ nhận `phanVung / bo` phân vùng, và **bộ có số thứ tự nhỏ hơn `phanVung % bo`** nhận thêm một; phân vùng phát liên tiếp từ `P0`.

Viết chương trình `NguoiNgoiKhong` (tệp `NguoiNgoiKhong.java`):
1. Với mỗi bộ đọc in một dòng `bo doc <số>:` rồi danh sách phân vùng (mỗi cái ` P<số>`), hoặc ` ngoi khong` nếu bộ không nhận phân vùng nào.
2. Dòng cuối: `so nguoi ngoi khong: <số>`.

Chú ý khoảng trắng: mỗi phân vùng bắt đầu bằng một dấu cách (` P0`), và chữ ` ngoi khong` cũng có dấu cách đứng trước.

Chạy: `javac NguoiNgoiKhong.java && java NguoiNgoiKhong`. Chấm: `bash labs/cham.sh BNK L07 NguoiNgoiKhong.java`.

## Phần thêm (không chấm): thứ tự ghi nhớ
Thư mục `ghi_nho/` có `GhiNho.java` đầy đủ (đúng như trong video) và `ket_qua.txt`. Cần JDK 21.
1. `cd ghi_nho`, rồi `javac GhiNho.java && java GhiNho`.
2. **Đoán trước**: đổi chỗ sập từ thông điệp 2 thành thông điệp 3 (hai chỗ `m == 2`), thì mảng số lần xử lý của hai cách ra gì?
3. Sửa, chạy lại và so với đoán.
