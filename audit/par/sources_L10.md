# Nguồn PAR L10 — gộp toàn phần theo vòng và máy chủ tham số

Đọc nguyên văn 2026-11-02.

## [PY09] P. Patarasuk, X. Yuan, “Bandwidth Optimal All-reduce Algorithms for Clusters of Workstations”, J. Parallel and Distributed Computing 69(2), 2009
Bản tác giả: https://www.cs.fsu.edu/~xyuan/paper/09jpdc.pdf (curl + pdftotext, scratchpad par_work/srcB/patarasuk09.txt).
- “The all-reduce operation combines values from all processes and distributes the results to all processes.”
- “We derive a tight lower bound of the amount of data that must be communicated in order to complete this operation and propose a ring-based algorithm that only requires tree connectivity to achieve bandwidth optimality.”
- “Lemma 3: The minimum number of partial results to be communicated to complete a one-item all-reduce operation on N processes over all algorithms is 2 × (N - 1).”
- Lemma 4/5: một tiến trình phải gửi ít nhất 2 × (N − 1)/N × X × itsize; thuật toán vòng gửi đúng lượng đó “which is the theoretical optimal”.
- “realizing the all-reduce operation by a reduce-scatter operation followed by an all-gather operation” → hai pha của bài.
- “One limitation of the proposed algorithm is that it is only optimal in the bandwidth term, but not the latency term: the number of communication rounds is proportional to the number of processes.” → Lỗi 2, quiz câu 2.
- “Another issue in the ring-based algorithm is that the reduction results are computed with different "bracketing", which may cause problems in the presence of rounding errors.” → tự kiểm, Lỗi 4.

## [HO18] A. Sergeev, M. Del Balso, “Horovod: fast and easy distributed deep learning in TensorFlow”, arXiv 1802.05799 (2018)
https://arxiv.org/pdf/1802.05799 (scratchpad par_work/src/horovod18.txt). Chỉ dùng một câu ở hook (hành trình chi tiết thuộc bài 13):
- “For example, we lost about half of our resources due to communication overhead when training on 128 GPUs.”
- “Workers process the training data, compute gradients, and send them to parameter servers to be averaged.”
- “each of N nodes communicates with two of its peers 2 ∗ (N - 1) times … In the first N - 1 iterations, received values are added … In the second N - 1 iterations, received values replace the values held in the node's buffer.”

## Điều KHÔNG dạy
- Không nêu tên công ty, tên thư viện trong lời đọc; hook nói “một đội lớn, năm 2018”.
- Băng thông 10 GB/s, 25 GB/s, trễ 0,05 ms và 5 ms là số minh hoạ. Máy chủ tham số giả định nhận rồi gửi nối tiếp qua một đường (màn hình ghi thêm trường hợp hai chiều cùng lúc).
- Không nói vòng luôn nhanh nhất: bài nêu điều kiện gói nhỏ / trễ cao.
- Không dạy cây hay thuật toán bướm (butterfly) chi tiết; chỉ nhắc “một cách gộp ít lượt”.
