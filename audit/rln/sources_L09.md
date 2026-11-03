# Nguồn bài RLN L09 — tối ưu chính sách gần kề (cắt tỉ số)

Đọc 2026-11-02: PDF arXiv `https://arxiv.org/pdf/1707.06347` (WebFetch trả nhị phân → lưu và trích chữ bằng `pdftotext`, bản v2).
Ký tự Hy Lạp mất khi trích, ghi lại trong ngoặc vuông.

**[PPO17]** J. Schulman, F. Wolski, P. Dhariwal, A. Radford, O. Klimov, *Proximal Policy Optimization Algorithms*, arXiv:1707.06347 (2017).

| Mục | Câu trích nguyên văn | Dùng ở |
|---|---|---|
| Tóm tắt | “Whereas standard policy gradient methods perform one gradient update per data sample, we propose a novel objective function that enables multiple epochs of minibatch updates.” | hook: một bước mỗi lô → nhiều lượt |
| 2.1 | “doing so is not well-justified, and empirically it often leads to destructively large policy updates” | hook, lỗi 4 |
| 3, (7) | “L^CLIP([θ]) = Ê_t[ min(r_t([θ])Â_t, clip(r_t([θ]), 1 − [ε], 1 + [ε])Â_t) ]” và “where epsilon is a hyperparameter, say, [ε] = 0.2.” | ký hiệu, công thức, ví dụ |
| 3 | “Finally, we take the minimum of the clipped and unclipped objective, so the final objective is a lower bound (i.e., a pessimistic bound) on the unclipped objective. With this scheme, we only ignore the change in probability ratio when it would make the objective improve, and we include it when it makes the objective worse.” | hình, ví dụ (cắt phía có lợi, phạt đủ phía bất lợi), lỗi 1 |
| 3 | “clipping the probability ratio, which removes the incentive for moving r_t outside of the interval [1 − [ε], 1 + [ε]]” | lỗi 2: cắt bỏ lực kéo, không giữ cứng ρ |
| 6.1 | “we used 7 simulated robotics tasks … We do one million timesteps of training on each one.” ; “Each algorithm was run on all 7 environments, with 3 random seeds on each.” ; “We shifted and scaled the scores for each environment so that the random policy gave a score of 0 and the best result was set to 1, and averaged over 21 runs” | hook (thang điểm), lỗi 4 |
| Bảng 1 | “No clipping or penalty … -0.39”; “Clipping, [ε] = 0.1 … 0.76”; “Clipping, [ε] = 0.2 … 0.82”; “Clipping, [ε] = 0.3 … 0.70”; “Adaptive KL dtarg = 0.01 … 0.74” | hook −0,39 / 0,82; lỗi 4 (0,76 / 0,82 / 0,70) |
| 6.1 | “the score is negative for the setting without clipping or penalties, because for one environment (half cheetah) it leads to a very negative score, which is worse than the initial random policy.” | hook “tệ hơn cả chính sách ngẫu nhiên” |
| Bảng 3 | “Horizon (T) 2048, Adam stepsize 3 × 10^-4, Num. epochs 10, Minibatch size 64, Discount ([γ]) 0.99, GAE parameter ([λ]) 0.95” (thiết lập 1 triệu bước mô phỏng robot) | lỗi 4: 2048 / 64 · 10 = 320 bước gradient (phép tính lại) |

## Điều KHÔNG dạy (nguồn không ghi)
- Không nói “30 lượt làm hỏng” bằng số đo: 960 bước là phép tính, bài nói “dễ trôi xa”; bài báo không đo 30 lượt.
- “40% mẫu ngoài đoạn” trong câu đố là SỐ MINH HOẠ; ngưỡng dừng sớm theo độ lệch là thực hành phổ biến, bài báo chỉ ghi phương án phạt độ lệch
  thích nghi (mục 4) và Hình 2 “KL divergence of about 0.02 … this is the point at which L^CLIP is maximal” — bài giảng không nêu ngưỡng số.
- Ví dụ hai hành động (0,5 / 0,5 → 0,6 / 0,4) và bốn mẫu ρ, A là SỐ MINH HOẠ, kiểm bằng checks và verify_parts/L09.py.
