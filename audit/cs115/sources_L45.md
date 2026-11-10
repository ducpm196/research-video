# Nguồn đã đọc nguyên văn cho CS115 L45 (bài hành trình: Adam → lỗi hội tụ → AdamW → thư viện)

Đọc ngày 2026-11-02 (curl + trích văn bản). Chỉ trích các câu bài giảng dựa vào (CITED); mọi con số khác là phép tính lại (VER, `checks`
của bài và `audit/verify_plan_curricula.py` CS115:L45) hoặc ghi rõ “(số minh hoạ)”. Không nêu tên cá nhân trong lời đọc; tên tác giả chỉ
ở `source:` và màn hình nguồn (theo luật 18: “bài báo năm 2015 của hai tác giả đề xuất Adam”).
Bản PDF arXiv của Adam (v9) trích văn bản bị chồng chữ → đọc nguyên văn từ mã nguồn TeX chính thức của arXiv (e-print, bản v8, 7/2015;
v9 chỉ có PDF). AdamW và Reddi: bản HTML ar5iv.labs.arxiv.org (chuyển từ TeX của arXiv).

## [KB15] D. P. Kingma, J. Ba, *Adam: A Method for Stochastic Optimization*, ICLR 2015, arXiv:1412.6980
Tải: arxiv.org/e-print/1412.6980v8 (2_algorithm.tex, 3_initbiascorrection.tex); trang arxiv.org/abs/1412.6980: “[v1] Mon, 22 Dec 2014”,
“Comments: Published as a conference paper at the 3rd International Conference for Learning Representations, San Diego, 2015”.
- Algorithm 1: “Good default settings for the tested machine learning problems are α=0.001, β1=0.9, β2=0.999 and ε = 10^-8.”
- Algorithm 1: “m_t ← β1·m_{t−1} + (1−β1)·g_t (Update biased first moment estimate)”; “v_t ← β2·v_{t−1} + (1−β2)·g_t^2 (Update biased second raw
  moment estimate)”; “m̂_t ← m_t/(1−β1^t)”; “v̂_t ← v_t/(1−β2^t)”; “θ_t ← θ_{t−1} − α·m̂_t/(√v̂_t + ε) (Update parameters)”.
- §2.1: “The effective magnitude of the steps taken in parameter space at each timestep are approximately bounded by the stepsize setting α,
  i.e., |Δt| ≲ α.” “The effective stepsize Δt is also invariant to the scale of the gradients”.
- §3: “these moving averages are initialized as (vectors of) 0's, leading to moment estimates that are biased towards zero” … “What is left is
  the term (1−β2^t) which is caused by initializing the running average with zeros. In algorithm 1 we therefore divide by this term”.
- §3: “it is exactly this case of small β2 where a lack of initialisation bias correction would lead to initial steps that are much larger.”
- §6.4 “Experiment: bias-correction term” (6_experiments_durk.tex, \input ngay sau 6_experiments_jimmy.tex có 3 tiểu mục 6.1–6.3; đọc
  2026-11-10): “Values of β2 close to 1, required for robustness to sparse gradients, results in larger initialization bias; therefore we
  expect the bias correction term is important in such cases of slow decay, preventing an adverse effect on optimization.” và “values β2
  close to 1 indeed lead to instabilities in training when no bias correction term was present, especially at first few epochs of the
  training. The best results were achieved with small values of (1−β2) and bias correction”.
  → Câu §3 viết “small β2” nhưng §6.4 cho thấy ý tác giả là (1−β2) nhỏ, tức β2 gần 1; bài nói “khi β2 gần 1, các bước đầu sẽ dài hơn nhiều”
  = §3 (“initial steps that are much larger”) + §6.4 (“β2 close to 1”, “first few epochs”). Thí nghiệm là VAE, β2 ∈ {0,99; 0,999; 0,9999}.
(Bài viết v_t của bài báo thành s_k theo quy ước CS115 bài 9.)

## [LH19] I. Loshchilov, F. Hutter, *Decoupled Weight Decay Regularization*, ICLR 2019, arXiv:1711.05101
Tải: ar5iv.labs.arxiv.org/html/1711.05101; trang abs: “[v1] Tue, 14 Nov 2017”, “Comments: Published as a conference paper at ICLR 2019”.
- Abstract: “L2 regularization and weight decay regularization are equivalent for standard stochastic gradient descent (when rescaled by the
  learning rate), but as we demonstrate this is not the case for adaptive gradient algorithms, such as Adam.”
- Abstract: “common implementations of these algorithms employ L2 regularization (often calling it “weight decay” in what may be misleading
  due to the inequivalence we expose)”.
- Proposition 1: “Standard SGD with base learning rate α executes the same steps on batch loss functions f_t(θ) with weight decay λ … as it
  executes without weight decay on f_t^reg(θ) = f_t(θ) + λ′/2 ‖θ‖², with λ′ = λ/α.”
- §2: “when Adam is run on a loss function f plus L2 regularization, weights that tend to have large gradients in f do not get regularized
  as much as they would with decoupled weight decay, since the gradient of the regularizer gets scaled along with the gradient of f.”
- Algorithm 2, dòng 12: “θ_t ← θ_{t−1} − η_t (α m̂_t/(√v̂_t + ϵ) + λθ_{t−1})”; dòng 6 (bản L2): “g_t ← ∇f_t(θ_{t−1}) + λθ_{t−1}”.
- §1: “achieving 15% relative improvement in test error”; §4.4: “For the default learning rate of 0.001, AdamW achieved 15% relative
  improvement in test error compared to Adam both on CIFAR-10 … and ImageNet32x32”.
- Abstract: “Our proposed decoupled weight decay has already been adopted by many researchers, and the community has implemented it in
  TensorFlow and PyTorch”.

## [RK18] S. J. Reddi, S. Kale, S. Kumar, *On the Convergence of Adam and Beyond*, ICLR 2018 (arXiv:1904.09237, “Appeared in ICLR 2018”)
Tải: ar5iv.labs.arxiv.org/html/1904.09237; trang abs: “[v1] Fri, 19 Apr 2019”, “Comments: Appeared in ICLR 2018”.
- Abstract: “it has been empirically observed that these algorithms fail to converge to an optimal solution … We show that one cause for
  such failures is the exponential moving average used in the algorithms.”
- §3: “f_t(x) = Cx, for t mod 3 = 1; −x, otherwise, where C > 2. For this function sequence, it is easy to see that the point x = −1 provides
  the minimum regret. Suppose β1 = 0 and β2 = 1/(1+C²). We show that Adam converges to a highly suboptimal solution of x = +1”.
- §3: “The algorithm obtains the large gradient C once every 3 steps, and while the other 2 steps it observes the gradient −1, which moves the
  algorithm in the wrong direction. The large gradient C is unable to counteract this effect since it is scaled down by a factor of almost C”.
- §3: “these examples of non-convergence are catastrophic insofar that Adam and RMSprop converge to a point that is worst amongst all points
  in the set [−1, 1]. … classic Sgd and Adagrad do not suffer from this problem”.
- Footnote §2: “for simplicity, we remove the debiasing step … However, our arguments also apply to the debiased version as well.”
- Algorithm 2 AMSGrad: “v̂_t = max(v̂_{t−1}, v_t)”; Discussion: “endowing the algorithms with a long-term memory of past gradients”.
- §2: “For theoretical analysis, one requires α_t = 1/√t”.

## [PT19] PyTorch v1.2.0 release notes (GitHub API, published_at 2019-08-08T16:06:38Z)
Tải: api.github.com/repos/pytorch/pytorch/releases/tags/v1.2.0.
- “`optim.AdamW`: introduce AdamW optimizer from [Decoupled Weight Decay Regularization](https://arxiv.org/abs/1711.05101). (21250)”

## [PT] PyTorch, mã nguồn hiện hành torch/optim/adam.py và adamw.py (nhánh main, đọc 2026-11-02)
Tải: raw.githubusercontent.com/pytorch/pytorch/main/torch/optim/adamw.py, …/adam.py. (Trang docs.pytorch.org chỉ trả trang chuyển hướng.)
- adamw.py: “weight_decay: float = 1e-2,”; “decoupled_weight_decay=True,”; “Implements AdamW algorithm, where weight decay does not accumulate in
  the momentum nor variance.”; công thức: “θ_t ← θ_{t−1} − γλθ_{t−1}” (γ = lr).
- adam.py: “weight_decay (float, optional): weight decay (L2 penalty) (default: 0)”; “decoupled_weight_decay (bool, optional): if True, this
  optimizer is equivalent to AdamW and the algorithm will not accumulate weight decay in the momentum nor variance. (default: False)”;
  “amsgrad (bool, optional): whether to use the AMSGrad variant of this algorithm from the paper `On the Convergence of Adam and Beyond`
  (default: False)”.

## Điều KHÔNG dạy (nguồn không ghi)
- Năm cụ thể thư viện thêm tham số `decoupled_weight_decay` cho Adam: mã nguồn không ghi ngày → chỉ nói “mã hiện hành”.
- Lời khuyên “luôn dùng AdamW” hay giá trị λ “tốt nhất”: không nguồn nào ghi → không dạy; 15% chỉ là kết quả trên CIFAR-10 và ImageNet32x32.
- AMSGrad “tốt hơn Adam trong thực tế”: [RK18] chỉ ghi “often also lead to improved empirical performance” trên thí nghiệm của họ; thư viện để
  mặc định amsgrad=False → bài không khuyên bật mặc định.
- Gradient 2, trọng số 1, λ = 0,0001, √ŝ = 10 và 0,1, 10 000 bước, α = 0,5 trong mô phỏng: SỐ MINH HOẠ, ghi rõ trên màn hình.
