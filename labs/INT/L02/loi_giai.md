# Lời giải lab INT L02

1. 16 × 2 + 2 = 34 kết nối.
   be ket noi: 34
2. Mỗi giao dịch giữ 20 mili giây = 0,020 giây kết nối. Trần = 34 / 0,020 = 1 700 giao dịch mỗi giây.
   toi da khong nhat ky: 1700 giao dich/giay
3. Có nhật ký độc lập, mỗi giao dịch giữ tổng 20 + 5 = 25 mili giây = 0,025 giây kết nối. Trần = 34 / 0,025 = 1 360 giao dịch mỗi giây.
   toi da co nhat ky REQUIRES_NEW: 1360 giao dich/giay

Ghi chú thêm: REQUIRES_NEW cần một kết nối thứ hai trong lúc kết nối chính vẫn đang giữ. Nếu cùng lúc có đủ 34 giao dịch chính, mỗi cái đang giữ một kết nối và đều chờ kết nối thứ hai, thì bể cạn và tất cả chờ nhau (bế tắc ở tầng bể kết nối), nên phải giới hạn số giao dịch chính chạy cùng lúc thấp hơn kích thước bể.
