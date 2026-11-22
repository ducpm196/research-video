# Lab NET L15 (Mô phỏng tắc nghẽn lịch sử) — Con số bốn chặng 1986 đến QUIC

Viết chương trình Python tính lại các con số then chốt: tỉ lệ sụp đổ năm 1986 (`32000 -> 40 bit/s`), BDP đường `10 Gbps × 100 ms`, trễ đệm `1000` gói `1500 B` ở `10 Mbps`, và cửa sổ khởi đầu QUIC (`10 × 1200 B`), in đúng 3 dòng:
1. `collapse_1986_drop=800x`
2. `bdp_10g_100ms_MB=125`
3. `bufferbloat_s=1.2 quic_iw_B=12000`

Chấm tự động:
```bash
bash labs/cham.sh NET L15 duong_dan/bai_cua_ban.py
```
