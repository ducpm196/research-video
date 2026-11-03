# Nguồn đã đọc nguyên văn cho CAS L05 (Knight Capital, 1/8/2012)

Đọc ngày 2026-11-02. Bản tải để ở thư mục nháp của phiên, không đưa vào kho. Chỉ trích câu bài giảng dựa vào (CITED); số khác là phép
tính lại (VER: `checks`, `audit/cas/ver/L05.py`, `audit/verify_plan_curricula.py` CAS:L05) hoặc ghi “(số minh hoạ)”.
Giáo án ghi “trang sec.gov chặn tải” (phiên 2026-10-30, đọc qua bản tóm của J. R. Varma). Phiên này **tải được bản PDF chính thức** →
bài dạy từ lệnh của SEC, không dùng bản tóm. Trang thông cáo www.sec.gov/news/press-release/2013-222 vẫn trả **403** (không cần).

## [SEC13] U.S. SEC, Release No. 34-70694 / October 16, 2013, Administrative Proceeding File No. 3-15570, In the Matter of Knight Capital Americas LLC
Tải: www.sec.gov/litigation/admin/2013/34-70694.pdf (HTTP 200, 98 373 byte; pdftotext).
- ¶1: “On August 1, 2012, Knight Capital Americas LLC ("Knight") experienced a significant error in the operation of its automated routing
  system for equity orders, known as SMARS. While processing 212 small retail orders that Knight had received from its customers, SMARS
  routed millions of orders into the market over a 45-minute period, and obtained over 4 million executions in 154 stocks for more than 397
  million shares. By the time that Knight stopped sending the orders, Knight had assumed a net long position in 80 stocks of approximately
  $3.5 billion and a net short position in 74 stocks of approximately $3.15 billion. Ultimately, Knight lost over $460 million”
- ¶3: “the speed with which automated trading systems enter orders into the marketplace can turn an otherwise manageable error into an
  extreme event”.
- ¶9 D: “Knight did not have technology governance controls and supervisory procedures sufficient to ensure the orderly deployment of new code
  or to prevent the activation of code no longer intended for use … but left on its servers”.
- ¶10: “While Knight's technology staff worked to identify and resolve the issue, Knight remained connected to the markets and continued to
  send orders”; “in approximately forty-five minutes”.
- ¶11: “Knight's aggregate trading … generally represented approximately ten percent of all trading in listed U.S. equity securities. SMARS
  generally represented approximately one percent or more”.
- ¶12: SMARS “receive orders passed from other components … ("parent" orders) and then, as needed based on the available liquidity, send one or
  more representative (or "child") orders to external venues”.
- ¶13: “This unused code previously had been used for functionality called "Power Peg," which Knight had discontinued using many years earlier.
  Despite the lack of use, the Power Peg functionality remained present and callable … The new RLP code also repurposed a flag that was
  formerly used to activate the Power Peg code.”
- ¶14: “a cumulative quantity function counted the number of shares of the parent order that had been executed. This feature instructed the
  code to stop routing child orders after the parent order had been filled completely. In 2003, Knight ceased using the Power Peg
  functionality. In 2005, Knight moved the tracking of cumulative shares function … Knight did not retest the Power Peg code”.
- ¶15: “Beginning on July 27, 2012, Knight deployed the new RLP code in SMARS in stages by placing it on a limited number of servers in SMARS on
  successive days. During the deployment of the new code, however, one of Knight's technicians did not copy the new code to one of the eight
  SMARS computer servers. Knight did not have a second technician review this deployment … Knight had no written procedures that required
  such a review.” (Bài KHÔNG nêu người: nói “ở một máy, bản mới không được chép lên”.)
- ¶16: “The seven servers that received the new code processed these orders correctly. However, orders sent with the repurposed flag to the
  eighth server triggered the defective Power Peg code … this server continuously sent child orders, in rapid sequence, for each incoming
  parent order without regard to the number of share executions … Although one part of Knight's order handling system recognized that the
  parent orders had been filled, this information was not communicated to SMARS.”
- ¶17: “resulting in 4 million executions in 154 stocks for more than 397 million shares in approximately 45 minutes … Knight realized a $460
  million loss”.
- ¶18: “for 75 of the stocks, Knight's executions comprised more than 20 percent of the trading volume and contributed to price moves of greater
  than five percent.”
- ¶19: “beginning at approximately 8:01 a.m. ET, an internal system at Knight generated automated e-mail messages … identified an error
  described as "Power Peg disabled." Knight's system sent 97 of these e-mail messages … before the 9:30 a.m. market open. Knight did not
  design these types of messages to be system alerts, and Knight personnel generally did not review them”.
- ¶21: “Knight did not have sufficient controls to monitor the output from SMARS … Knight also did not have procedures in place to halt
  SMARS's operations in response to its own aberrant activity.”
- ¶25: PMON “relied entirely on human monitoring and did not generate automated alerts … PMON experienced delays during high volume events”.
- ¶26: “Knight did not have written code development and deployment procedures for SMARS … and Knight did not require a second technician to
  review code deployment”.
- ¶27: “Knight uninstalled the new RLP code from the seven servers where it had been deployed correctly. This action worsened the problem,
  causing additional incoming parent orders to activate the Power Peg code that was present on those servers”.

## Phép tính của bài (VER)
- 460 / 45 > 10,2 triệu đô la mỗi phút; 4 000 000 / 2700 s ≈ 1481 lần khớp mỗi giây; 397 / 4 ≈ 99 cổ phiếu mỗi lần; 80 + 74 = 154;
  3,5 + 3,15 = 6,65 tỉ; 2012 − 2003 = 9 năm; 8:01 → 9:30 = 89 phút.
- Số minh hoạ: lệnh mẹ 100 cổ phiếu, lệnh con 10, 100 lệnh con mỗi giây (→ 6000 lệnh, 600 lần trong 1 phút); 1% sót mỗi máy, 8 / 20 máy
  (7,7% / 18,2%; thêm phép kiểm độc lập → ≈ 0,2%).
- Mã kiểm đồng nhất trên màn hình: chép nguyên văn từ tệp bài và chạy (`ver/L05.py` L05h).

## Điều KHÔNG dạy
- Tốc độ gửi lệnh con thật, kích thước lệnh con thật: lệnh không ghi → số minh hoạ.
- Chi tiết về tài khoản “33 Account”, PMON, mức phạt 12 triệu đô la, vi phạm Regulation SHO: có trong lệnh nhưng bài không dùng (giữ trọng
  tâm triển khai và lớp phòng vệ); không mâu thuẫn với bài.
- “Bản tóm của J. R. Varma (2013)” mà giáo án nhắc: không cần, không trích.
- Tên/chức danh người: không nêu.
