# Nguồn PAR L09 — nhân ma trận chia khối

Đọc nguyên văn 2026-11-02.

## [BPG] NVIDIA, CUDA C++ Best Practices Guide (docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html), mục “Shared Memory in Matrix Multiplication (C=AB)”
Tải bằng curl, bỏ thẻ HTML (scratchpad par_work/srcB/bpg.txt).
- “The effective bandwidth of this kernel is 119.9 GB/s on an NVIDIA Tesla V100.” (simpleMultiply, không tối ưu)
- “for each iteration i, all threads in a warp read the same value from global memory for matrix A … there is wasted bandwidth in the transaction, because only one 4-byte word out of 8 words in a 32-byte cache segment is used.”
- “The performance on a device of any compute capability can be improved by reading a tile of A into shared memory” … “This kernel has an effective bandwidth of 144.4 GB/s on an NVIDIA Tesla V100.”
- “The repeated reading of the B tile can be eliminated by reading it into shared memory once” … “The effective bandwidth of this routine is 195.5 GB/s on an NVIDIA Tesla V100. Note that the performance improvement is not due to improved coalescing in either case, but to avoiding redundant transfers from global memory.”
- Bảng “Performance Improvements Optimizing C = AB Matrix Multiply”: 119.9 / 144.4 / 195.5 GB/s.
- “a multiprocessor’s shared memory is also partitioned between resident thread blocks” (mục Register Pressure / occupancy) → Lỗi 3.
- “Medium Priority: Use shared memory to avoid redundant transfers from global memory.”

## [NI08] Nickolls, Buck, Garland, Skadron, ACM Queue 2008 (bản chép grothoff.org, xem sources_L08.md)
- “The 16KB SM shared memory has very low access latency and high bandwidth similar to an L1 cache”
- “CUDA programs copy data to shared memory when it must be accessed multiple times by a thread block.”

## Điều KHÔNG dạy
- Ví dụ của hướng dẫn dùng khối 32 = cỡ nhóm luồng và ma trận A có w cột; bài KHÔNG chép mã của hướng dẫn, chỉ dẫn ba con số băng thông.
- “16 KB mỗi cụm” là của thế hệ năm 2008; bài ghi rõ năm, không nói đây là dung lượng của thẻ hiện nay. 48 KB của quiz là số minh hoạ.
- Không khẳng định khối 16 nhanh hơn khối 32 (hay ngược lại): bài nói “phải đo”.
- Số đọc 2n³/b không tính ghi C (n² lần) — ghi trong quy ước đầu tệp bài.
