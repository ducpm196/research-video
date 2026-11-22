# Lab BCH L09 — Mô phỏng lỗi gọi lại (Reentrancy) và bản sửa Checks-Effects-Interactions

Cài lớp `Vault(pool=10, safe=...)` và `Attacker` có phương thức `recv(self, vault)` tự gọi lại `vault.withdraw(self)`. Chạy kịch bản kẻ gửi `2` đồng rút từ kho `10` đồng ở hai chế độ: `safe=False` (gửi tiền trước khi trừ số dư) và `safe=True` (trừ số dư trước khi gọi ra ngoài).
In đúng 1 dòng `unsafe_stolen=... safe_withdrawn=...`.

Chấm tự động:
```bash
bash labs/cham.sh BCH L09 duong_dan/bai_cua_ban.py
```
