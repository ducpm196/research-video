# Lab CSA L16 — Tình huống kiến trúc: Amdahl đa nhân & kênh phụ Cache Timing

Đọc `stdin` `p=<float> cores=<int> hit_ns=<float> miss_ns=<float>`. Tính speedup Amdahl với `cores` nhân, giới hạn vô cực và tỉ số thời gian `miss / hit`.

In đúng 3 dòng: `speedup_8cores_p85=<.2f>`, `limit_inf=<.2f>`, `cache_timing_ratio=<.1f>x`.
Chấm tự động: `bash labs/cham.sh CSA L16 duong_dan/bai_cua_ban.py`
