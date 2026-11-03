# Nguồn đã đọc nguyên văn cho CAS L01 (Patriot, Dhahran, 25/2/1991)

Đọc ngày 2026-11-02. Bản tải để ở thư mục nháp của phiên, không đưa vào kho. Chỉ trích câu bài giảng dựa vào (CITED); số khác là phép
tính lại (VER: `checks` của bài, `audit/cas/ver/L01.py`, `audit/verify_plan_curricula.py` CAS:L01) hoặc ghi “(số minh hoạ)”.

## [GAO92] U.S. General Accounting Office, *Patriot Missile Defense: Software Problem Led to System Failure at Dhahran, Saudi Arabia*, GAO/IMTEC-92-26, B-247094, 4/2/1992
Tải: www.gao.gov/assets/imtec-92-26.pdf (HTTP 200, 1 780 377 byte; bản quét có lớp chữ OCR, đọc bằng pdftotext và xem ảnh trang 15).
Trang www.gao.gov/products/imtec-92-26 trả **403** (không cần: PDF là bản chính thức).
- “On February 25, 1991, a Patriot missile defense system operating at Dhahran, Saudi Arabia, during Operation Desert Storm failed to track
  and intercept an incoming Scud. This Scud subsequently hit an Army barracks, killing 28 Americans.”
- “This problem led to an inaccurate tracking calculation that became worse the longer the system operated. At the time of the incident, the
  battery had been operating continuously for over 100 hours. By then, the inaccuracy was serious enough to cause the system to look in the
  wrong place for the incoming Scud.”
- “The Patriot had never before been used to defend against Scud missiles nor was it expected to operate continuously for long periods of time.”
- “The Patriot system was originally designed to operate in Europe … To avoid detection it was designed to be mobile and operate for only a
  few hours at one location.”
- “The Patriot's weapons control computer used in Operation Desert Storm is based on a 1970s design with relatively limited capability to
  perform high precision calculations.”
- “Time is kept continuously by the system's internal clock in tenths of seconds but is expressed as an integer or whole number (e.g.,
  32,33, 34...). The longer the system has been running, the larger the number representing time. To predict where the Scud will next appear,
  both time and velocity must be expressed as real numbers. Because of the way the Patriot computer performs its calculations and the fact
  that its registers are only 24 bits long, the conversion of time from an integer to a real number cannot be any more precise than 24 bits.”
- “The effect of this inaccuracy on the range gate's calculation is directly proportional to the target's velocity and the length of time
  the system has been running.”
- Range gate: “calculates an area in the air space where the system should next look for it”; “The target needs to be in the center of the
  range gate to ensure the highest probability of tracking the target.”
- “First, the Patriot was not equipped with an embedded (internal) data recorder … Second, although portable, external data recorders were
  available, U.S. commanders decided not to use them because they believed the recorders could cause an unanticipated system shutdown.”
- “On February 11, 1991, the Patriot Project Office received Israeli data identifying a 20 percent shift in the Patriot system's radar range
  gate after the system had been running for 8 consecutive hours.”
- “the Patriot system will not track a Scud when there is a range gate shift of 50 percent or more. Because the shift is directly
  proportional to time, extrapolating the Israeli data … determined that the range gate would shift 50 percent after about 20 hours”
- “rebooting the system … every few hours. Rebooting, which takes about 60 to 90 seconds, … reinitializes the computer's clock, setting the
  time back to zero.”
- “they assumed other Patriot users were not running their systems for 8 or more hours at a time.” … “a software change which compensated
  for the inaccurate time calculation. This change allowed for extended run times and was included in the modified software version that was
  released on February 16, 1991. However, Army officials did not use the Israeli data to determine how long the Patriot could operate before
  the inaccurate time calculation would render the system ineffective.”
- “On February 21, 1991, the Patriot Project Office sent a message to Patriot users stating that very long run times could cause a shift in
  the range gate … However, the message did not specify what constitutes very long run times.”
- “On February 26, the next day, the modified software … arrived in Dhahran. … the delay … was due to the time it took to arrange for air and
  ground transportation in a wartime environment.”
- “Further, an endurance test has been conducted to ensure that extended run times do not cause other system difficulties.” (đoạn “In
  September 1991…”, tức SAU sự cố)
- Phụ lục II (tr. 15, xem ảnh trang ở 300 dpi): Hours / Seconds / Calculated Time / Inaccuracy / Shift (m):
  0/0/0/0/0; 1/3600/3599.9966/.0034/7; 8/28800/28799.9725/.0275/55; 20/72000/71999.9313/.0687/137; 48/172800/172799.8352/.1648/330;
  72/259200/259199.7528/.2472/494; 100/360000/359999.6667/.3433/687. Chú thích: “Continuous operation exceeding about 20 hours—target
  outside range gate”; “Alpha Battery ran continuously for about 100 hours”.

## Phép tính của bài (VER) và phát hiện khi đối chiếu
- Mô hình “0,1 cắt sau 23 bit phần lẻ” (0,1 ≈ 838 860 / 2²³, sai 0,8 / 2²³ ≈ 9,54·10⁻⁸ s mỗi nhịp) **không có trong [GAO92]** — báo cáo chỉ
  ghi thanh ghi 24 bit. Bài gọi đây là “mô hình của bài” và kiểm: khớp cả 6 hàng cột Inaccuracy tới 4 chữ số; mô hình 24 bit phần lẻ cho
  0,1287 s ở 100 h, không khớp.
- **Bảng tự mâu thuẫn ở một ô**: Seconds − Inaccuracy khớp cột Calculated Time ở 5 hàng, nhưng hàng 100 giờ: 360 000 − 0,3433 = 359 999,6567,
  bảng in 359 999,6667 (đã xem ảnh trang, không phải lỗi OCR). Bài nêu điều này ở phần tự kiểm, không suy đoán nguyên nhân.
- Mét / giây ở các hàng ≥ 8 h đều ≈ 2000 (55/0,0275 = 2000; 687/0,3433 ≈ 2001): khớp câu “directly proportional”. Bài KHÔNG gán 2000 m/s
  cho vận tốc tên lửa (báo cáo ghi Scud ≈ MACH 5, 3750 mph — không khớp 2000 m/s; báo cáo không giải thích hệ số).
- 8 × 50 / 20 = 20 giờ (khớp “about 20 hours”).

## Điều KHÔNG dạy (nguồn không ghi hoặc không đọc được)
- Chi tiết mã máy, chỗ phép đổi được sửa ở chỗ này mà không ở chỗ khác (hay được kể lại trong các bài phân tích sau 1992): [GAO92] không ghi.
- Vận tốc tên lửa dùng để tính cột mét: không ghi → không dạy.
- Tên khẩu đội chỉ ở màn hình theo báo cáo (“Alpha Battery”): không nêu trong bài; không nêu tên người.
- Bộ dữ liệu Israel: chỉ dạy 20% sau 8 giờ như báo cáo ghi.
