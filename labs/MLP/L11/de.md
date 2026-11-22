# Lab MLP L11 — Mạng MLP 2→16→2 PyTorch CPU giải XOR & đối chứng thiếu ReLU

Viết chương trình Python (chạy bằng `labs/.venv-ml` qua `cham.sh`): với `torch.manual_seed(42)`, huấn luyện mạng `Linear(2,16) -> ReLU -> Linear(16,2)` bằng `Adam(lr=0.05)` + `CrossEntropyLoss()` 150 bước trên 100 mẫu XOR và đối chứng mạng thiếu ReLU (`SGD(lr=0.1)` 200 bước trên 4 mẫu), in đúng 3 dòng:
1. `n_params=82`
2. `mlp_xor_acc=1.00`
3. `no_relu_xor_acc=0.25`

Chấm tự động:
```bash
bash labs/cham.sh MLP L11 duong_dan/bai_cua_ban.py
```
