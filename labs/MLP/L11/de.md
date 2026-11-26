# Lab MLP L11 — Mạng MLP PyTorch CPU giải XOR & đối chứng thiếu ReLU

Đọc từ `stdin`:
`seed=<int> hidden=<int> steps_mlp=<int> lr_mlp=<float> steps_lin=<int> lr_lin=<float>`

Yêu cầu: (1) gọi `torch.manual_seed(seed)`, huấn luyện `nn.Sequential(nn.Linear(2, hidden), nn.ReLU(), nn.Linear(hidden, 2))` bằng `Adam(lr=lr_mlp)` và `nn.CrossEntropyLoss()` trên 100 mẫu XOR (25 lần 4 góc); (2) gọi lại `torch.manual_seed(seed)`, đối chứng `nn.Sequential(nn.Linear(2, hidden), nn.Linear(hidden, 2))` bằng `SGD(lr=lr_lin)` và `nn.CrossEntropyLoss()` trên 4 mẫu XOR.

In đúng 3 dòng: `n_params=<int>`, `mlp_xor_acc=<.2f>`, `no_relu_xor_acc=<.2f>`.
Chấm tự động: `bash labs/cham.sh MLP L11 duong_dan/bai_cua_ban.py`
