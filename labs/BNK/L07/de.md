# Lab BNK L07 — Bảy phân vùng, chín bộ đọc

Một chủ đề có **7 phân vùng** `P0 … P6`, một nhóm có **9 bộ đọc** `0 … 8`. Chia đều: mỗi bộ nhận `phanVung / bo` phân vùng, và **bộ có số thứ tự nhỏ hơn `phanVung % bo`** nhận thêm một; phân vùng phát liên tiếp từ `P0`.

Viết chương trình `NguoiNgoiKhong` (tệp `NguoiNgoiKhong.java`):
1. Với mỗi bộ đọc in một dòng `bo doc <số>:` rồi danh sách phân vùng (mỗi cái ` P<số>`), hoặc ` ngoi khong` nếu bộ không nhận phân vùng nào.
2. Dòng cuối: `so nguoi ngoi khong: <số>`.

Chạy: `javac NguoiNgoiKhong.java && java NguoiNgoiKhong`. Chấm: `bash labs/cham.sh BNK L07 NguoiNgoiKhong.java`.
