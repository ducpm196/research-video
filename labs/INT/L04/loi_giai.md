# Lời giải lab INT L04

1. Chia 64 bit thành 8 nhóm, mỗi nhóm 8 bit; trong nhóm, bit thứ nhất = 0x80, thứ hai = 0x40, thứ ba = 0x20, ..., thứ tám = 0x01.
   - Nhóm 1 (bit 1–8): trường 3 là bit thứ 3 → 0x20; trường 7 là bit thứ 7 → 0x02; cộng lại 0x22.
   - Nhóm 2 (bit 9–16): trường 11 là bit thứ 3 của nhóm → 0x20.
   - Nhóm 6 (bit 41–48): trường 41 là bit thứ 1 của nhóm → 0x80.
   - Các nhóm còn lại bằng 00. Ghép: 22 20 00 00 00 80 00 00.
   bitmap: 2220000000800000
2. Trường PIN: `0` + `4` (độ dài) + `5821` + 10 chữ F = `045821FFFFFFFFFF`.
   Số thẻ bỏ chữ số cuối: `541234567890123`; lấy 12 chữ số bên phải: `234567890123`; trường số thẻ = `0000234567890123`.
   XOR từng chữ số hệ mười sáu: 04⊕00=04, 58⊕00=58, 21⊕23=02, FF⊕45=BA, FF⊕67=98, FF⊕89=76, FF⊕01=FE, FF⊕23=DC (hai chữ số một lần, ghép theo cặp).
   khoi PIN: 045802BA9876FEDC
3. 1 000 000 ÷ 4 000 = 250 giây.
   STAN quay vong sau: 250 giay
4. 250 giây < 300 giây: STAN quay lại trong lúc khoá cũ còn sống, nên một giao dịch mới trùng STAN bị chặn nhầm.
   chan nham: co
5. 4 000 × 1,5 = 6 000 tin.
   tin dang cho: 6000
