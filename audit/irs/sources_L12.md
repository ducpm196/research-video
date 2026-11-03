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

## Không dạy
- Ngân sách 100 ms, 0,05 ms mỗi ứng viên, 20 ms mạng: số minh hoạ, không gán cho công ty nào.
