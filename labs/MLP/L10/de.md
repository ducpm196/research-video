# Lab MLP L10 — PyTorch CPU Autograd, zero_grad & khớp hồi quy tuyến tính

Đọc từ `stdin`:
`x0=<float> seed=<int> w_true=<float> b_true=<float> lr=<float> steps=<int>`

Yêu cầu: (1) tại `x0` gọi `(x**2).backward()` hai lần liên tiếp lấy `grad_accum`, rồi gọi `zero_()` và `.backward()` lấy `grad_reset`; (2) huấn luyện `torch.nn.Linear(1, 1)` với `torch.manual_seed(seed)`, `SGD(lr=lr)` đúng `steps` bước trên `y = w_true * x + b_true` (`x = linspace(-1, 1, 20)`). In đúng 3 dòng: `grad_accum=<.1f>`, `grad_reset=<.1f>`, `fitted_wb=<w:.2f>_<b:.2f>`.

Chấm tự động: `bash labs/cham.sh MLP L10 duong_dan/bai_cua_ban.py`
