# Sổ tác tử — sửa BNX L00–L11 (2026-11-14)

Điều phối: tác tử chính (L00, L01, L04, L05 + việc chung: bản đồ L00, lời hẹn L36, pack.py, kiểm cuối).

| Tác tử | Phạm vi | Trạng thái |
|---|---|---|
| F1 | L06 (cắt còn ≤ 2 300 từ) + bài mới L37 | đã giao |
| F2 | L07 (cắt còn ≤ 2 300 từ) + bài mới L38 | đã giao |
| F3 | L08, L09, L10, L11 | đã giao |

Quy tắc dùng chung: chỉ Edit nhỏ ở `curriculum/bnx.yaml`, `tools/registry/symbols.BNX.yaml`, `audit/verify_plan_curricula.py`; không chạy build/tts/asr/audit_all/git; Oracle: mỗi tác tử dùng bảng tiền tố riêng `bnx_lNN_`.
