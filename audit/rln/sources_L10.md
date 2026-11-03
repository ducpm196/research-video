# Nguồn bài RLN L10 — học phần thưởng từ sở thích của người

Đọc 2026-11-02: PDF arXiv tải qua WebFetch (nhị phân → lưu, trích chữ bằng `pdftotext`).

**[C17]** P. Christiano, J. Leike, T. B. Brown, M. Martic, S. Legg, D. Amodei, *Deep Reinforcement Learning from Human Preferences*,
arXiv:1706.03741 (NeurIPS 2017), `https://arxiv.org/pdf/1706.03741`.
**[O22]** L. Ouyang và cộng sự, *Training language models to follow instructions with human feedback*, arXiv:2203.02155 (2022),
`https://arxiv.org/pdf/2203.02155`.

| Nguồn, mục | Câu trích nguyên văn | Dùng ở |
|---|---|---|
| [C17] 3.2 | “The Hopper robot performing a sequence of backflips (see Figure 4). This behavior was trained using 900 queries in less than an hour.” | hook: 900 lần hỏi, chưa tới một giờ |
| [C17] 2.2.3 | “This follows the Bradley-Terry model (Bradley and Terry, 1952) for estimating score functions from pairwise preferences … Just as the difference in Elo points of two chess players estimates the probability of one player defeating the other …” | mô hình so sánh cặp, chỉ hiệu điểm có nghĩa |
| [C17] 3.1 | “Contractors responded to the average query in 3-5 seconds, and so the experiments involving real human feedback required between 30 minutes and 5 hours of human time.” | (bối cảnh, không đọc số) |
| [O22] Hình 1 | “outputs from our 1.3B PPO-ptx model are preferred to those from the 175B GPT-3.” | (bối cảnh; bài không đọc số này) |
| [O22] 3.5, (1) | “loss([θ]) = −1/(K choose 2) E_(x,yw,yl)~D [log([σ](r_[θ](x, yw) − r_[θ](x, yl)))]” ; “yw is the preferred completion out of the pair of yw and yl” | ký hiệu, công thức mất mát |
| [O22] 3.5 | “we present labelers with anywhere between K = 4 and K = 9 responses to rank. This produces (K choose 2) comparisons for each prompt … we found that if we simply shuffle the comparisons into one dataset, a single pass over the dataset caused the reward model to overfit. Instead, we train on all (K choose 2) comparisons from each prompt as a single batch element.” | lỗi 3 (người đã đi làm): 6 và 36 cặp là phép tính lại |
| [O22] 3.5 | “In addition, we add a per-token KL penalty from the SFT model at each token to mitigate overoptimization of the reward model.” | phạt độ lệch, lỗi 2 và 4 |
| [O22] (2) | “objective([φ]) = E[ r_[θ](x, y) − [β] log( [π]^RL_[φ](y | x) / [π]^SFT(y | x) ) ] + [γ] E[log([π]^RL_[φ](x))]” ; “The KL reward coefficient, [β], … control[s] the strength of the KL penalty” | công thức r − β·ln(π / π_gốc) (bài bỏ số hạng thứ hai) |
| [O22] Phụ lục C.4 | “These models are also used to compute the KL reward, in the same way as Stiennon et al. (2020), with [β] = 0.02 (see Equation 2).” ; “The PPO clip ratio is set to 0.2” | β = 0,02; nối bài 9 |
| [O22] Phụ lục E | “Both 0 and 2 for KL reward coefficient result in poor performance. The optimal value is around 0.01 and 0.02.” | ghi chú bảng phạt độ lệch |

## Điều KHÔNG dạy (nguồn không ghi)
- Không nói “mô hình phần thưởng là một bảng hai số”: ví dụ học thẳng r_A, r_B là đơn giản hoá (đạo hàm theo điểm giống hệt), ghi rõ ở quy ước bài.
- Hai câu A / B (điểm 2 và 1,5; xác suất 0,5 / 0,05) và β = 0,1 / 1 là SỐ MINH HOẠ; chỉ β = 0,02 và “0 và 2 đều kém” là CITED.
- Không nêu tỉ lệ lỗi của người chấm, số người chấm, hay “10% trả lời ngẫu nhiên” của [C17] (có trong nguồn, bài không dùng).
