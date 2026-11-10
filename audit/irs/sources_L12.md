# Nguồn bài IRS L12 — Tình huống chuyên gia: thiết kế hệ gợi ý hai tầng trong ngân sách 100 ms

Bài tình huống loại “quyết định nghề nghiệp” (case-lessons §1): con số là SỐ MINH HOẠ, phép tính kiểm bằng `checks` và
verify_parts/L12.py. Khung hai tầng lấy từ nguồn đọc nguyên văn ngày 2026-11-03:

## [CO16] Covington và cộng sự (RecSys 2016) — URL ở sources_L13.md.
- "The system is comprised of two neural networks: one for candidate generation and one for ranking."
- Hình 2: "video corpus — millions — candidate generation — hundreds — ranking — dozens"
- "Scoring millions of items under a strict serving latency of tens of milliseconds requires an approximate scoring scheme sublinear in the number of classes."
- "During ranking, we have access to many more features describing the video and the user's relationship to the video because only a few hundred videos are being scored rather than the millions scored in candidate generation." (đã đối chiếu nguyên câu ở bản trích không giữ cột)
- "The trade-off, however, is server CPU time needed for inference. The configuration of a 1024-wide ReLU followed by a 512-wide ReLU followed by a 256-wide ReLU gave us the best results while enabling us to stay within our serving CPU budget."
## [ZH19] Zhao và cộng sự (RecSys 2019)
- "At the candidate generation stage, we retrieve a few hundred candidates from a a huge corpus. Our ranking system provides a score for each candidate and generates the final ranked list."
- "An overly complicated model, which significantly increases the latency in generating recommended items, can decrease user satisfaction and live metrics. Therefore, we generally prefer a simpler and more straight-forward model architecture."
## [YI19] Yi và cộng sự (RecSys 2019)
- "these systems connect billions of users to items from an extremely large corpus of content, often in the scale of millions to billions, under stringent latency requirements."

## Đợt C (2026-11-09)
- Phần ôn không còn nhắc khoá khác: tự giảng ước lượng nhanh (thời gian = số việc × thời gian mỗi việc), đổi ms ↔ giây, và phân vị 99
  (thứ hạng gần nhất trên 100 lần đo) bằng hai bộ đo minh hoạ (1…99 và 250 → TB 52, p99 99; 95 lần 10 + 5 lần 200 → TB 19,5, p99 200).
- Móc câu nói rõ kho 10 triệu (trước mâu thuẫn “danh mục 10 000” với cái phễu “kho 10 triệu”); thanh ngân sách vẽ đúng tỉ lệ 10 ms = 80 điểm ảnh.
- Lời hẹn bài sau: [BA08] không ghi tổng số người dùng năm 2008 (5,4 triệu chỉ là mẫu) → đổi thành “kho hơn 45 triệu video năm 2008 tới hơn 1 tỉ người dùng năm 2016”.

## Không dạy
- Ngân sách 100 ms, 0,05 ms mỗi ứng viên, 20 ms mạng: số minh hoạ, không gán cho công ty nào.
