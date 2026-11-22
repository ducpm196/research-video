# Lab MLP L10 — PyTorch CPU Autograd, zero_grad & khớp hồi quy tuyến tính

Viết chương trình Python (chạy bằng `labs/.venv-ml` qua `cham.sh`): (1) kiểm chứng `(x**2).backward()` 2 lần liên tiếp tại `x=3.0` cho `12.0` và sau `zero_()` cho `6.0`; (2) huấn luyện `torch.nn.Linear(1, 1)` với `torch.manual_seed(42)`, `SGD(lr=0.2)` 120 bước trên `y = 3x + 2`, in đúng 3 dòng:
1. `grad_accum=12.0`
2. `grad_reset=6.0`
3. `fitted_wb=3.00_2.00`

Chấm tự động:
```bash
bash labs/cham.sh MLP L10 duong_dan/bai_cua_ban.py
```
