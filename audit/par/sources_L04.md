# Nguồn PAR L04 — cân bằng tải (đọc nguyên văn 2026-11-03)

## [OMP] OpenMP API Specification Version 5.0 (November 2018), mục 2.9.2 “Worksharing-Loop Construct”, bảng 2.5
https://www.openmp.org/spec-html/5.0/openmpsu41.html (WebFetch đọc được; trang 5.2 openmpsu48 là mục khác — initializer clause).
- static: “the chunks are assigned to the threads in the team in a round-robin fashion in the order of the thread number.”
  “Each chunk contains chunk_size iterations, except for the chunk that contains the sequentially last iteration.”
- dynamic: “Each thread executes a chunk of iterations, then requests another chunk, until no chunks remain to be distributed.”
  “When no chunk_size is specified, it defaults to 1.”
- guided: “Each thread executes a chunk of iterations, then requests another chunk, until no chunks remain to be assigned.”
→ bài dạy (Lỗi 4, màn hình): chuẩn này có sẵn lịch tĩnh và lịch động có cỡ khúc. Lời đọc nói “chuẩn lập trình song song bộ nhớ chung
  phổ biến”, tên OpenMP chỉ trên màn hình.

## Kiến thức của khoá (không cần nguồn ngoài, chứng minh ngay trong bài và kiểm bằng máy)
- Cận dưới C ≥ max(T₁/n, việc dài nhất); cận trên của chia động C ≤ T₁/n + việc dài nhất (suy ra trong bài: lúc việc cuối bắt đầu,
  mọi lõi đều bận). verify_parts/L04.py thử mọi danh sách nhỏ để xác nhận cận trên.

## Số minh hoạ (ghi rõ trên màn hình)
- 8 ảnh dài 8…1 giây; 1000 việc 1 mi li giây, lấy việc 0,1 mi li giây; khúc 10 việc; 1 việc 30 giây giữa 100 việc 1 giây;
  8 việc 7, 6, 5, 4, 3, 3, 2, 2 giây ở quiz.

## Điều KHÔNG dạy
- Không nêu tên và cận 4/3 của Graham cho “việc dài trước” (chưa đọc nguyên văn bài báo 1969).
- Không nêu chi phí thật của một lần xin khúc trong các bản cài đặt OpenMP (chưa đọc số đo).
- Không nói “việc dài trước luôn tối ưu”: bài chỉ nói trên ví dụ nó đạt cận dưới / bằng kết quả thử hết.
