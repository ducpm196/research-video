# Lab DVO L06 — Quét rò rỉ bí mật và kiểm tra bí mật tồn tại trong lịch sử commit

Viết chương trình Python quét 3 bản ghi lịch sử `['API_KEY=sk_live_987654', 'API_KEY=env_only', 'PORT=8080']`: chứng minh ở trạng thái cuối (`HEAD`) chuỗi sạch nhưng lịch sử vẫn giữ khoá ở mục 1, và viết regex phát hiện định dạng khoá `sk_live_...`, in đúng 3 dòng:
1. `head_has_secret=0`
2. `history_leaked_commits=1`
3. `rotation_required=1`

Chấm tự động:
```bash
bash labs/cham.sh DVO L06 duong_dan/bai_cua_ban.py
```
