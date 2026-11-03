# Nguồn PAR L07 — mô hình mái nhà (roofline)

Đọc nguyên văn 2026-11-02 (curl + pdftotext, bản chép ở scratchpad par_work/srcB/roofline08.txt).

## [WWP08] S. Williams, A. Waterman, D. Patterson, “Roofline: An Insightful Visual Performance Model for Floating-Point Programs and Multicore Architectures”, UC Berkeley Technical Report UCB/EECS-2008-134, 17/10/2008
URL: https://www2.eecs.berkeley.edu/Pubs/TechRpts/2008/EECS-2008-134.pdf (bản tạp chí: CACM 52(4), 2009 — không đọc bản CACM).

Câu trích:
- “we use the term operational intensity to mean operations per byte of DRAM traffic. We define total bytes accessed as those that go to the main memory after they have been filtered by the cache hierarchy.” → bài dạy: byte đếm SAU bộ nhớ đệm.
- “Attainable GFlops/sec = Min(Peak Floating Point Performance, Peak Memory Bandwidth x Operational Intensity)” → công thức của bài.
- “If we think of operational intensity as a column that hits the roof, either it hits the flat part of the roof, which means performance is compute bound, or it hits the slanted part of the roof, which means performance is ultimately memory bound.”
- “The x-coordinate of the ridge point is the minimum operational intensity required to achieve maximum performance.” → điểm gãy.
- “The system being modeled has a peak double precision floating-point performance of 17.6 GFlops/sec and a peak memory bandwidth of 15 GBytes/sec from our benchmark.” (Opteron X2, máy hai chip)
- “This stencil will do 8 floatingpoint operations for every 24 bytes of compulsory memory traffic on write-allocate architectures, yielding an operational intensity of 0.33.” → bài tính lại min(17,6; 15 · 0,33) ≈ 5.
- “Fallacy: Doubling cache size will increase operational intensity.” … “size helps only with capacity misses and possibly conflict misses” → Lỗi 4.
- “The advice is generally to improve operational intensity of the kernel before other optimizations.”

## Điều KHÔNG dạy (nguồn không ghi, hoặc lệch)
- Bài báo ghi điểm gãy của Opteron X2 là “1.0”, trong khi 17,6 / 15 ≈ 1,17 — bài KHÔNG nêu điểm gãy của máy này, chỉ dùng hai con số đỉnh và băng thông.
- Không dùng tên hãng trong lời đọc (AMD chưa dò ở PAR); màn hình ghi “Opteron X2”.
- Máy ví dụ 10 nghìn tỉ phép/s, 1 nghìn tỉ byte/s và hai thẻ X, Y là SỐ MINH HOẠ, ghi trên màn hình.
- Không nói “GPU luôn bị chặn bởi băng thông” hay một tỉ lệ chung nào.
