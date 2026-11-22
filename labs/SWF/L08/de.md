# Lab SWF L08 — Máy trạng thái hữu hạn đèn giao thông có kiểm chứng chuyển tiếp

Viết chương trình Python cài FSM đèn giao thông (`RED -> GREEN -> YELLOW -> RED`): kiểm chuỗi bước `['GREEN', 'YELLOW', 'RED']` từ `RED` và từ chối nhảy tắt `RED -> RED` hoặc `GREEN -> RED`, in đúng 3 dòng:
1. `valid_cycle_ok=1`
2. `skip_green_to_red_rejected=1`
3. `final_state=RED`

Chấm tự động:
```bash
bash labs/cham.sh SWF L08 duong_dan/bai_cua_ban.py
```
