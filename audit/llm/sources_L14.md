# Nguồn đã đọc nguyên văn cho LLM L14 (bài hành trình: từ kiến trúc chú ý 2017 tới huấn luyện tối ưu tính toán 2022)

Đọc ngày 2026-11-02: tải PDF chính thức từ arXiv bằng curl (`https://arxiv.org/pdf/<mã>`), trích chữ bằng `pdftotext -enc UTF-8`, tìm câu
bằng grep. Chỉ trích các câu bài giảng dựa vào (CITED); mọi con số khác trong bài là phép tính lại (VER, `checks` của bài và
`audit/llm/verify_llm.py` L14) hoặc ghi rõ “(số minh hoạ)”. Không nêu tên cá nhân trong lời đọc; tên tác giả chỉ ở `source:` và màn hình nguồn.
Cả bốn nguồn đều là bản arXiv do chính nhóm tác giả đăng (không phải bản hội nghị/tạp chí); số trang theo bản arXiv.

## [V17] A. Vaswani và cộng sự, *Attention Is All You Need*, arXiv:1706.03762 (bản v7, 2/8/2023; bản đầu 6/2017; NeurIPS 2017)
- Abstract: “We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and
  convolutions entirely. Experiments on two machine translation tasks show these models to be superior in quality while being more
  parallelizable and requiring significantly less time to train. Our model achieves 28.4 BLEU on the WMT 2014 English-to-German translation task,
  improving over the existing best results, including ensembles, by over 2 BLEU.”
- §1: “This inherently sequential nature precludes parallelization within training examples, which becomes critical at longer sequence lengths,
  as memory constraints limit batching across examples. … The fundamental constraint of sequential computation, however, remains.”
- §1: “The Transformer allows for significantly more parallelization and can reach a new state of the art in translation quality after being
  trained for as little as twelve hours on eight P100 GPUs.”
- §4, Table 1 (Sequential Operations): self-attention O(1), recurrent O(n). “a self-attention layer connects all positions with a constant
  number of sequentially executed operations, whereas a recurrent layer requires O(n) sequential operations.”
- §5.1: “We trained on the standard WMT 2014 English-German dataset consisting of about 4.5 million sentence pairs. Sentences were encoded using
  byte-pair encoding [3], which has a shared source-target vocabulary of about 37000 tokens.”
- §5.2: “We trained our models on one machine with 8 NVIDIA P100 GPUs. For our base models … each training step took about 0.4 seconds. We trained
  the base models for a total of 100,000 steps or 12 hours. For our big models, … step time was 1.0 seconds. The big models were trained for
  300,000 steps (3.5 days).”
- Table 2, Training Cost (FLOPs) EN-DE: Transformer (base model) 3.3 · 10^18; Transformer (big) 2.3 · 10^19.
- §6.1: “We estimate the number of floating point operations used to train a model by multiplying the training time, the number of GPUs used, and
  an estimate of the sustained single-precision floating-point capacity of each GPU.” Chú thích 5: “We used values of 2.8, 3.7, 6.0 and 9.5 TFLOPS
  for K80, K40, M40 and P100, respectively.”
- Table 3 (cột params ×10^6): base 65, big 213.
- Lưu ý: bản v7 ghi EN-FR 41.8 ở tóm tắt và Table 2 nhưng 41.0 ở §6.1 → bài KHÔNG dùng con số EN-FR.

## [K20] J. Kaplan và cộng sự, *Scaling Laws for Neural Language Models*, arXiv:2001.08361 (v1, 23/1/2020)
- Abstract: “The loss scales as a power-law with model size, dataset size, and the amount of compute used for training, with some trends spanning
  more than seven orders of magnitude.”
- §1.1 “Universality of overfitting: Performance improves predictably as long as we scale up N and D in tandem … The performance penalty depends
  predictably on the ratio N^0.74/D, meaning that every time we increase the model size 8x, we only need to increase the data by roughly 5x”.
- §1.1 “Universality of training: … By extrapolating the early part of a training curve, we can roughly predict the loss that would be achieved if we
  trained for much longer.”
- §1.1 “Convergence is inefficient: When working within a fixed compute budget C … we attain optimal performance by training very large models and
  stopping significantly short of convergence”.
- §2.1: “Accounting for the backwards pass (approximately twice the compute as the forwards pass), we then define the estimated non-embedding compute
  as C ≈ 6N floating point operators per training token.” Table 1: “Cforward = 2N + 2nlayer nctx dattn”; §2.1 “N ≈ 2 dmodel nlayer (2dattn + dff)
  = 12 nlayer dmodel^2 with the standard dattn = dff/4 = dmodel”.
- Figure 14 (chú thích): “Optimal model size grows very rapidly with Cmin, increasing by 5x for each 10x increase in compute. The number of data
  examples processed makes up the remainder of the increase, growing relatively modestly by only 2x.”

## [B20] T. B. Brown và cộng sự, *Language Models are Few-Shot Learners*, arXiv:2005.14165 (v4, 22/7/2020; bản đầu 5/2020)
- Abstract: “we train GPT-3, an autoregressive language model with 175 billion parameters, 10x more than any previous non-sparse language model”.
- §2.1 Table 2.1: GPT-3 175B: nlayers 96, dmodel 12288, batch 3.2M; “All models were trained for a total of 300 billion tokens.”
  “All models use a context window of nctx = 2048 tokens.”
- §2.1: “Previous work [KMH+20] suggests that with enough training data, scaling of validation loss should be approximately a smooth power law as a
  function of size”.
- §2.2: “we took 3 steps to improve the average quality of our datasets: (1) we downloaded and filtered a version of CommonCrawl based on similarity
  to a range of high-quality reference corpora, (2) we performed fuzzy deduplication at the document level … (3) we also added known high-quality
  reference corpora”. “constituting 45TB of compressed plaintext before filtering and 570GB after filtering, roughly equivalent to 400 billion
  byte-pair-encoded tokens.”
- Table 2.2: Common Crawl (filtered) 410 billion tokens, weight in training mix 60%.
- §2.2: “Unfortunately, a bug in the filtering caused us to ignore some overlaps, and due to the cost of training it was not feasible to retrain the
  model.”
- §2.3: “All models were trained on V100 GPU’s on part of a high-bandwidth cluster provided by Microsoft.”
- §3.1: “language modeling performance follows a power-law when making efficient use of training compute. After extending this trend by two more
  orders of magnitude, we observe only a slight (if any) departure from the power-law.”
- Appendix D, Table D.1, GPT-3 175B: total train compute 3.64E+03 PF-days, 3.14E+23 flops; params 174,600 (M); training tokens 300 (billions);
  flops per param per token 6. Chú thích: “each token is involved in a single addition and a single multiply for each active parameter in the
  forward pass (ignoring attention). Then we add a multiplier of 3x to account for the backwards pass”.

## [H22] J. Hoffmann và cộng sự, *Training Compute-Optimal Large Language Models*, arXiv:2203.15556 (v1, 29/3/2022)
- Abstract: “We find that current large language models are significantly undertrained, a consequence of the recent focus on scaling language models
  whilst keeping the amount of training data constant. By training over 400 language models ranging from 70 million to over 16 billion parameters on
  5 to 500 billion tokens, we find that for compute-optimal training, the model size and the number of training tokens should be scaled equally: for
  every doubling of model size the number of training tokens should also be doubled.”
- Abstract: “Chinchilla, that uses the same compute budget as Gopher but with 70B parameters and 4× more more data. Chinchilla uniformly and
  significantly outperforms Gopher (280B), GPT-3 (175B), Jurassic-1 (178B), and Megatron-Turing NLG (530B) … This also means that Chinchilla uses
  substantially less compute for fine-tuning and inference … Chinchilla reaches a state-of-the-art average accuracy of 67.5% on the MMLU
  benchmark, greater than a 7% improvement over Gopher.”
- §1: “Since it is typically only feasible to train these large models once, accurately estimating the best model hyperparameters for a given
  compute budget is critical”.
- §1: “given a 10× increase computational budget, they suggests that the size of the model should increase 5.5× while the number of training tokens
  should only increase 1.8×. Instead, we find that model size and the number of training tokens should be scaled in equal proportions.”
- §1: “many of the recently trained large models have been trained for approximately 300 billion tokens (Table 1)”. Table 1: GPT-3 175 Billion /
  300 Billion; Gopher 280 Billion / 300 Billion; Chinchilla 70 Billion / 1.4 Trillion.
- §1: “for the compute budget used to train Gopher, an optimal model should be 4 times smaller, while being training on 4 times more tokens. …
  Chinchilla, on 1.4 trillion tokens. … its reduced model size reduces inference cost considerably and greatly facilitates downstream uses on
  smaller hardware. The energy cost of a large language model is amortized through its usage for inference an fine-tuning.”
- Table 3 (Approach 1): 1 Billion → 20.2 Billion tokens; 10 Billion → 205.1 Billion; 67 Billion → 5.76e+23 FLOPs, 1.5 Trillion tokens;
  175 Billion → 3.7 Trillion; 1 Trillion → 21.2 Trillion.
- Table 4 (MMLU 5-shot): GPT-3 43.9%, Gopher 60.0%, Chinchilla 67.6% (tóm tắt ghi 67.5% → bài dùng 67,5% của tóm tắt).
- Phụ lục, đoạn trước Table A4: “a comparison between our calculation and that using the common approximation C = 6DN (Kaplan et al., 2020) … We find the differences
  in FLOP calculation to be very small”.
- §5: “Due to the cost of training large models, we only have two comparable training runs at large scale (Chinchilla and Gopher) … we observe some
  concavity … This suggests that we may still be overestimating the optimal size of large models. Finally, the training runs for our analysis have
  all been trained on less than an epoch of data; future work may consider the multiple epoch regime.”
- §5: “our analysis suggests an increased focus on dataset scaling is needed. Speculatively, we expect that scaling to larger and larger datasets is
  only beneficial when the data is high-quality. … Larger datasets will require extra care to ensure train-test set overlap is properly accounted
  for”.

## Con số tính lại (VER) — không có nguyên văn trong nguồn
- 100 000 bước × 0,4 s = 40 000 s ≈ 11,1 giờ (nguồn ghi “12 hours”); 300 000 × 1,0 s = 300 000 s ≈ 3,47 ngày (nguồn “3.5 days”).
- 12 giờ × 8 thẻ × 9,5·10¹² ≈ 3,3·10¹⁸; 3,5 ngày × 8 × 9,5·10¹² ≈ 2,3·10¹⁹ — khớp Table 2 của [V17].
- 8^0,74 ≈ 4,66 ≈ “roughly 5x” [K20]; 5 × 2 = 10 [K20 Fig. 14].
- 12 · 96 · 12288² ≈ 1,74·10¹¹ ≈ 174 600 triệu [B20 Table D.1]; 6 · 1,746·10¹¹ · 3·10¹¹ ≈ 3,14·10²³; chia 10¹⁵ · 86 400 ≈ 3637 PF-ngày ≈ 3,64·10³.
- 570 GB / 45 TB ≈ 1,3% giữ lại (đổi 1 TB = 1000 GB); 300 / 175 ≈ 1,7 từ tố mỗi tham số ở GPT-3.
- 6 · 70·10⁹ · 1,4·10¹² = 5,88·10²³ ≈ 5,76·10²³ (lệch ≈ 2%); 1,4·10¹² / 70·10⁹ = 20; 280 / 70 = 4; 1,4 nghìn tỉ / 300 tỉ ≈ 4,7.
- Tỉ lệ “≈ 20 từ tố mỗi tham số” là tỉ lệ ĐỌC RA từ Table 3 [H22] (20,2; 20,5; 22,4; 21,1; 21,2) — nguồn không viết câu “20 tokens per parameter”.
- Đi tới ≈ 2N phép tính mỗi từ tố [K20 Table 1]: 2 · 70·10⁹ so với 2 · 280·10⁹ → mô hình nhỏ rẻ hơn 4 lần mỗi từ tố.
- 67,5 − 60,0 = 7,5 điểm (“greater than a 7% improvement”).

## Điều KHÔNG dạy (nguồn không ghi)
- Chi phí bằng tiền của GPT-3 hay Chinchilla, số thẻ, số ngày huấn luyện của GPT-3: [B20] không ghi số thẻ, số ngày → không dạy.
- “20 từ tố mỗi tham số” như một câu của [H22]: không có; chỉ nói “bảng ước lượng năm 2022 cho tỉ lệ khoảng 20”.
- Mô hình huấn luyện vượt điểm tối ưu (nhỏ hơn, lâu hơn) để suy luận rẻ: [H22] chỉ nói mô hình nhỏ hơn làm suy luận rẻ hơn và chi phí năng lượng
  “amortized through its usage”; bài chỉ tính so sánh bằng 2N mỗi từ tố, không khẳng định công ty nào làm gì sau 2022.
- Huấn luyện nhiều lượt trên cùng dữ liệu (nhiều epoch): [H22] ghi là chưa thử → bài nói “ngoài vùng đã kiểm”.
- Con số EN-FR của [V17]: hai chỗ trong bản v7 ghi khác nhau (41.8 / 41.0) → không dùng.
- Chi tiết lỗi lọc dữ liệu của GPT-3 ngoài câu đã trích (nguyên nhân kỹ thuật cụ thể): §C chỉ ghi “filtering described above failed on long
  documents such as books” — bài chỉ nói “một lỗi trong bước lọc”, không quy cho cá nhân.
- Sự kiện sau 2022 (các mô hình mới, tỉ lệ dữ liệu mới): không đọc nguồn nào → không dạy.
