# Lab DVO L03 (Mô phỏng tích hợp liên tục CI) — Xác suất đường ống đỏ vì bài kiểm thử chập chờn (flaky)

Viết chương trình Python tính xác suất ít nhất 1 trong `300` test độc lập lỗi với `p = 0.005`, và so với khi giảm `p` xuống `0.0005` trên cùng `300` test, in đúng 3 dòng:
1. `flaky_fail_pct_300=77.8%`
2. `flaky_fail_pct_p0005=13.9%`
3. `pipeline_always_green_pct=22.2%`

Chấm tự động:
```bash
bash labs/cham.sh DVO L03 duong_dan/bai_cua_ban.py
```
