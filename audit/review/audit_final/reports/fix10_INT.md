# fix10_INT (r10): 4 việc nhỏ từ item-verifier
1. L03 quymo.1: lời đọc SAGA đổi thành "Còn SAGA, trong mô hình rút gọn này, chỉ giữ khoá dòng nóng bốn mili giây, đối tác chậm hơn cũng không đổi số đó, nên xong sau bốn mươi giây." (rút gọn hơn câu đề xuất để ≤ 170 ký tự và ≤ 2300 từ); xoá 1 mục asr_reviewed cũ (E30).
2. L04 prereq.2: màn hình "byte (nhóm 8 bit) 1 (bit 1–8) ..."; `say` "nhóm tám bit đầu, tức byte một, bật bit 3 và 4". Bớt vài chữ cuối câu để ≤ 2300 từ.
3. L05: bảng prereq.0 thêm "(hai bên giữ khoá chờ nhau mãi)" sau "bế tắc"; recap dùng cùng từ nên không thêm lần hai.
4. L08 pitfall.1: "lúc lệnh đang chạy, chưa có trả lời".
Cổng: lint 0/0 (L03, L04, L05, L08); từ L03 2300, L04 2298, L05 2287, L08 2299; verify_int 208 PASS; curriculum 0 lỗi; test_e52 0 FAIL. Render và screen_code INT: xem tin nhắn cuối.
Bổ sung: L05 recap "giảm bế tắc khoá (hai bên giữ khoá chờ nhau mãi)" cũng đã giải nghĩa.
Kết quả cuối: lint 0/0 (L03/L04/L05/L08); render L03, L04, L05 (sau cả hai sửa), L08: 0 vấn đề; screen_code INT 60 khối 0 FAIL/STALE/MISSING/ORPHAN.
