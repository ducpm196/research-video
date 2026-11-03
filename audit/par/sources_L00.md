# Nguồn PAR L00 — Vì sao song song: định luật Amdahl và phần tuần tự

Đọc nguyên văn 2026-11-02. Văn bản tải về: scratchpad `par_work/src/amdahl67.pdf` (pdftotext).

## [AM67] G. M. Amdahl, “Validity of the Single Processor Approach to Achieving Large Scale Computing Capabilities”
- Bản đọc: bản in lại trong IEEE SSCS News, Summer 2007, tr. 19–20 (ghi “Reprinted from the AFIPS Conference Proceedings, Vol. 30
  (Atlantic City, N.J., Apr. 18–20), AFIPS Press, Reston, Va., 1967, pp. 483–485”), tải từ
  https://www3.cs.stonybrook.edu/~rezaul/Spring-2019/CSE613/reading/Amdahl-1967.pdf (bản chép của một khoá học; bản gốc AFIPS
  không có bản mở; bản Berkeley inst.eecs đòi đăng nhập).
- Câu trích dùng trong bài:
  - Lời ban biên tập: “This article was the first publication by Gene Amdahl on what became known as Amdahl's Law. Interestingly, it
    has no equations and only a single figure.” → bài nói “bài báo ngắn ấy không có một phương trình nào; công thức mang tên ông được
    viết ra về sau”.
  - “The first characteristic of interest is the fraction of the computational load which is associated with data management
    housekeeping. This fraction has been very nearly constant for about ten years, and accounts for 40% of the executed instructions
    in production runs.” → “khoảng 40% số lệnh là việc quản lý dữ liệu”.
  - “The nature of this overhead appears to be sequential so that it is unlikely to be amenable to parallel processing techniques.”
    → “có vẻ tuần tự, nên khó song song hoá”.
  - “A fairly obvious conclusion which can be drawn at this point is that the effort expended on achieving high parallel processing
    rates is wasted unless it is accompanied by achievements in sequential processing rates of very nearly the same magnitude.”
    (ý “sửa phần tuần tự trước” của bài; không trích nguyên câu trong lời đọc).

## Điều KHÔNG dạy (nguồn không ghi hoặc không kiểm được)
- Công thức S(n) = 1/((1 − p) + p/n) KHÔNG có trong bài báo 1967 (lời ban biên tập: “no equations”); bài dạy nó như cách viết về
  sau (đã học ở khoá CSA bài 13), không nói “Amdahl viết công thức này”.
- Câu “thông lượng tối đa năm tới bảy lần” của bài báo dựa trên giả định riêng của tác giả (việc quản lý chạy trên một bộ xử lý
  riêng) — không dạy, vì không suy lại được từ 40% bằng công thức của bài.
- Đoạn bình luận cuối bản in lại (25% tuần tự, 10% chi phí phối hợp) là của người viết lời bình năm 2007, không phải của Amdahl —
  không dạy.
- Mọi con số khác trong bài (chương trình 100 s, 120 s, 16/32 lõi, giá thuê gấp 4, chi phí phối hợp 0,005 mỗi lõi, 130 s) là SỐ
  MINH HOẠ, ghi “(số minh hoạ)” trên màn hình; mọi phép tính có `checks` và audit/par/verify_parts/L00.py.
