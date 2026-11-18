# Lời giải lab BNX L35

Tháng 31 ngày có 31 × 24 × 60 = 44 640 phút.

1. Ngân sách ngừng của SLA 99,8%: 44 640 × (100 − 99,8) : 100 = 89,28 phút.
   ngan sach 99.8% thang 31 ngay: 89.28 phut
2. Chuỗi hai dịch vụ nối tiếp 99,9% và 99,5%: 0,999 × 0,995 = 0,994005.
   chuoi 99.9% va 99.5%: 99.4005%
3. Hai sự cố 20 và 75 phút: 20 + 75 = 95 phút; 95 − 89,28 = 5,72 phút.
   su co 20 + 75 = 95 phut: vuot ngan sach 5.72 phut
4. Tài liệu thiết kế có đủ ba mục Bối cảnh, Quyết định, Hệ quả; quyết định viết "Chúng tôi sẽ …"; hệ quả nêu cả mặt tiêu cực.
   tai lieu thiet ke: du 3 muc, quyet dinh chu dong, he qua co mat tieu cuc

## Khung tài liệu thiết kế mẫu

```
# ADR <số>: <cụm danh từ ngắn>
Trạng thái: Đã duyệt
## Bối cảnh      (sự thật và lực kéo, trung lập)
## Quyết định    (Chúng tôi sẽ …)
## Hệ quả        (tích cực, tiêu cực, trung tính)
```
