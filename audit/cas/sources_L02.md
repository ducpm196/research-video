# Nguồn đã đọc nguyên văn cho CAS L02 (Ariane 5, chuyến bay 501, 4/6/1996)

Đọc ngày 2026-11-02. Bản tải để ở thư mục nháp của phiên, không đưa vào kho. Chỉ trích câu bài giảng dựa vào (CITED); số khác là phép
tính lại (VER: `checks`, `audit/cas/ver/L02.py`, `audit/verify_plan_curricula.py` CAS:L02) hoặc ghi “(số minh hoạ)”.

## [IB96] Inquiry Board, *ARIANE 5 Flight 501 Failure — Report by the Inquiry Board*, Paris, 19/7/1996
- Bản chính thức: esamultimedia.esa.int/docs/esa-x-1819eng.pdf (HTTP 200, 2 168 608 byte, 60 trang, **bản quét không có lớp chữ** — đã
  đọc ảnh các trang bìa, lời nói đầu, mục lục, trang 1–2 và trang 4–5 của báo cáo bằng công cụ đọc ảnh; nội dung khớp từng câu với bản chép).
- Bản chép toàn văn (để tìm chữ): www-users.cse.umn.edu/~arnold/disasters/ariane5rep.html (HTTP 200, 39 937 byte; ghi “originally appeared
  at http://www.esrin.esa.it/htdocs/tidc/Press/Press96/ariane5rep.html”). sunnyday.mit.edu: hết thời gian kết nối.
- Lời nói đầu: “On 4 June 1996, the maiden flight of the Ariane 5 launcher ended in a failure. Only about 40 seconds after initiation of the
  flight sequence, at an altitude of about 3700 m, the launcher veered off its flight path, broke up and exploded.”
- 1.1: “nominal behaviour of the launcher up to H0 + 36 seconds”; “the Inertial Reference Systems, which obviously ceased to function almost
  simultaneously at around H0 + 36.7 seconds.”
- 2.1: “There are two SRIs operating in parallel, with identical hardware and software. One SRI is active and one is in "hot" stand-by”
- “The design of the Ariane 5 SRI is practically the same as that of an SRI which is presently used on Ariane 4, particularly as regards the software.”
- “The launcher started to disintegrate at about H0 + 39 seconds because of high aerodynamic loads due to an angle of attack of more than 20
  degrees”; “This angle of attack was caused by full nozzle deflections of the solid boosters and the Vulcain main engine.”
- “Part of these data at that time did not contain proper flight data, but showed a diagnostic bit pattern of the computer of the SRI 2,
  which was interpreted as flight data.”
- “The internal SRI software exception was caused during execution of a data conversion from 64-bit floating point to 16-bit signed integer
  value. The floating point number which was converted had a value greater than what could be represented by a 16-bit signed integer. This
  resulted in an Operand Error. The data conversion instructions (in Ada code) were not protected from causing an Operand Error, although
  other conversions of comparable variables in the same place in the code were protected.”
- “This software module computes meaningful results only before lift-off. As soon as the launcher lifts off, this function serves no purpose.”
- “The alignment function is operative for 50 seconds after starting of the Flight Mode of the SRIs which occurs at H0 - 3 seconds for
  Ariane 5. Consequently, when lift-off occurs, the function continues for approx. 40 seconds of flight. This time sequence is based on a
  requirement of Ariane 4 and is not required for Ariane 5.”
- “The Operand Error occurred due to an unexpected high value of an internal alignment function result called BH, Horizontal Bias, related
  to the horizontal velocity sensed by the platform.” “The value of BH was much higher than expected because the early part of the trajectory
  of Ariane 5 differs from that of Ariane 4 and results in considerably higher horizontal velocity values.”
- 2.2: “not all the conversions were protected because a maximum workload target of 80% had been set for the SRI computer.” … “operations
  involving seven variables were at risk of leading to an Operand Error. This led to protection being added to four of the variables …
  three of the variables were left unprotected. No reference to justification of this decision was found directly in the source code.”
- “further reasoning indicated that they were either physically limited or that there was a large margin of safety, a reasoning which in
  the case of the variable BH turned out to be faulty. It is important to note that the decision to protect certain variables but not others
  was taken jointly by project partners at several contractual levels.”
- “There is no evidence that any trajectory data were used to analyse the behaviour of the unprotected variables, and it is even more
  important to note that it was jointly agreed not to include the Ariane 5 trajectory data in the SRI requirements and specification.”
- “In the event of any kind of exception, the system specification stated that: the failure should be indicated on the databus, the failure
  context should be stored in an EEPROM memory …, and finally, the SRI processor should be shut down.” “Restart is not feasible since attitude
  is too difficult to re-calculate after a processor shutdown”. “the culture within the Ariane programme of only addressing random hardware
  failures”. “this resulted in the switch-off of two still healthy critical units of equipment.”
- “it was maintained for commonality reasons, presumably based on the view that, unless proven necessary, it was not wise to make changes in
  software which worked well on Ariane 4.”
- “The Board is in favour of the opposite view, that software should be assumed to be faulty until applying the currently accepted best
  practice methods can demonstrate that it is correct.”
- 2.3: “no test was performed to verify that the SRI would behave correctly when being subjected to the count-down and flight time sequence
  and the trajectory of Ariane 5.” “In a programme of this size, literally thousands of problems and potential failures are successfully
  handled in the review process”.
- 3.1 d) “22 seconds after H0 (command for main cryogenic engine ignition)”; e) “At 36.7 seconds after H0 (approx. 30 seconds after lift-off)
  the computer within the back-up inertial reference system … became inoperative.” f) “Approx. 0.05 seconds later the active inertial
  reference system, identical to the back-up system in hardware and software, failed for the same reason.”
- 4: “R1 Switch off the alignment function of the inertial reference system immediately after lift-off. More generally, no software function
  should run during flight unless it is needed.” “R3 Do not allow any sensor, such as the inertial reference system, to stop sending best
  effort data.” “R10 Include trajectory data in specifications and test requirements.”

## [ESA96] ESA, Press Release N° 33–1996 “Ariane 501 – Presentation of Inquiry Board report”, 23/7/1996
www.esa.int/Newsroom/Press_Releases/Ariane_501_-_Presentation_of_Inquiry_Board_report (HTTP 200). Khớp [IB96]: “Only about 40 seconds after
initiation of the flight sequence, at an altitude of about 3700 m …”; “simultaneous failure of the two inertial reference systems”.

## Phép tính của bài (VER)
- 16 bit có dấu: −2¹⁵ … 2¹⁵ − 1 = −32 768 … 32 767; quay vòng 40 000 → −25 536, 50 000 → −15 536 (số minh hoạ).
- Căn chỉnh: −3 + 50 = H0 + 47 s; cất cánh ≈ H0 + 7 s (suy từ “36,7 s … khoảng 30 s sau cất cánh”) → ≈ 40 s bay (khớp “approx. 40 seconds”).
- 7 − 4 = 3 biến không bảo vệ ≈ 43%.

## Điều KHÔNG dạy (nguồn không ghi hoặc mâu thuẫn nhẹ)
- Giá trị thật của BH và ngưỡng trên Ariane 4: báo cáo không ghi → 20 000 / 40 000 / 50 000 là số minh hoạ, ghi trên màn hình.
- Khoảng cách giữa hai lần hỏng: 2.1 ghi bộ dự phòng hỏng “during the previous data cycle (72 milliseconds period)”, 3.1 f ghi “approx.
  0.05 seconds later” → bài chỉ nói “khoảng 0,05 giây” (theo mục kết luận), không nêu 72 ms.
- Báo cáo kỹ thuật “restricted circulation”: không đọc được → không dạy chi tiết mã.
- Tên người (chủ tịch, thành viên hội đồng): chỉ ở `source`, không trong lời.
