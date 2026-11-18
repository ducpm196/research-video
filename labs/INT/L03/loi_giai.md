# Lời giải lab INT L03

1. 24 000 / 2 000 = 12 lô.
   so lo: 12
2. Từng dòng: 24 000 dòng × 2 lần đổi ngữ cảnh = 48 000.
   doi ngu canh tung dong: 48000
3. Theo lô: 12 lô × 2 = 24.
   doi ngu canh theo lo: 24
4. Cam kết hai pha giữ khoá qua 2 vòng hỏi đáp: 2 × 15 = 30 mili giây.
   giu khoa 2PC: 30 ms
5. Một dòng nóng chỉ phục vụ lần lượt từng giao dịch: 1 / 0,030 = 33,33, lấy phần nguyên 33 giao dịch mỗi giây.
   toi da 2PC tren mot dong nong: 33 giao dich/giay
6. SAGA giữ khoá 3 mili giây = 0,003 giây: 1 / 0,003 = 333,33, lấy phần nguyên 333 giao dịch mỗi giây.
   toi da SAGA tren mot dong nong: 333 giao dich/giay

Ghi chú: các con số là số minh hoạ để tập tính; thực tế phải đo thời gian giữ khoá bằng công cụ theo dõi của cơ sở dữ liệu.
