# Lab CSA L03 — Giải mã 3 trường IEEE 754 float32 và so sánh gần đúng

Viết chương trình C chuẩn C11 tách bit dấu, mũ (đã trừ bias 127) và phần định trị hexa của `float x = -6.5f`, đồng thời kiểm tra `fabs(0.1 + 0.2 - 0.3) < 1e-9`, in đúng 3 dòng:
1. `sign=1 exp_unbiased=2 mant_hex=0x500000`
2. `close_03=1`
3. `hex32=0xC0D00000`

Chấm tự động:
```bash
bash labs/cham.sh CSA L03 duong_dan/bai_cua_ban.c
```
