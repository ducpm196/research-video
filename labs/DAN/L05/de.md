# Lab DAN L05 — Phễu chuyển đổi từng bước & ước lượng nâng bước 2

Đọc `stdin` `steps=<s0,s1,s2,s3> new_s2=<float>`. Tính phần trăm từng bước, toàn phễu hiện tại và toàn phễu ước lượng khi bước 2 đạt tỉ lệ `new_s2`.

In 1 dòng: `step_pct=<list> overall=<.1f>% overall_step2_38=<.1f>%`.
Chấm tự động: `bash labs/cham.sh DAN L05 duong_dan/bai_cua_ban.py`

> Gợi ý đọc `stdin`: `kv = dict(t.split("=") for t in sys.stdin.read().split())`, tách `steps` qua `[int(x) for x in kv["steps"].split(",")]`.
