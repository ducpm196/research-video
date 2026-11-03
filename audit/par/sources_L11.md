# Nguồn PAR L11 — huấn luyện phân tán

Đọc nguyên văn 2026-11-02.

## [GO17] P. Goyal, P. Dollár, R. Girshick, P. Noordhuis, L. Wesolowski, A. Kyrola, A. Tulloch, Y. Jia, K. He, “Accurate, Large Minibatch SGD: Training ImageNet in 1 Hour”, arXiv 1706.02677 (2017)
https://arxiv.org/pdf/1706.02677 (curl + pdftotext, scratchpad par_work/src/goyal17.txt).
- “Linear Scaling Rule: When the minibatch size is multiplied by k, multiply the learning rate by k.” → quy tắc nhân.
- Phần giải thích: so k bước SGD với lô nhỏ, tốc độ học η, với một bước lô kn, tốc độ học η̂ — “we may hope the linear scaling rule to apply” khi gradient gần như nhau → làm thử 4 bước nhỏ / 1 bước lớn của bài (bài nêu điều kiện “khi các gradient gần giống nhau”).
- “we use n = 32 which has performed well” (lô mỗi máy); “kn=256, η = 0.1” là mốc trong bảng 1 → mốc của bài.
- “we start from a learning rate of η and increment it by a constant amount at each iteration such that it reaches η̂ = kη after 5 epochs” → khởi động dần trong 5 lượt dữ liệu.
- Bảng: “kn=256, η = 0.1, 23.60%”; “kn= 8k, η = 3.2, 24.84%” (không khởi động); “25.88%” (khởi động hằng); “23.74%” (khởi động dần); “The gradual warmup variant has a validation error within 0.14% of the baseline” → Lỗi 2.
- “as soon as the gradient for a layer is computed, it is aggregated across workers, while gradient computation for the next layer continues … This is possible because there is no data dependency between gradients across layers.” → hình chồng tính với gộp.
- “Remark 3: Normalize the per-worker loss by total minibatch size kn, not per-worker size n.” → Lỗi 4.
- “90% scaling efficiency when moving from 8 to 256 GPUs” (chỉ nhắc ở bài 13, không dùng ở đây).

## Điều KHÔNG dạy
- Hành trình 29 giờ → 1 giờ, 256 thẻ là của bài 13; bài này chỉ dùng quy tắc và các mốc lô 256, η = 0,1.
- C = 100 ms, G = 30 ms, O = 20 ms, 150 triệu tham số, 35 GB/s, 10 GB/s, “cần thêm 10% lượt” là SỐ MINH HOẠ.
- Không khẳng định quy tắc nhân luôn đúng: nguồn ghi nó gãy ở đầu huấn luyện với lô rất lớn (vì vậy cần khởi động dần) và chỉ thử tới 8k.
