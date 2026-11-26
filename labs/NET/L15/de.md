# Lab NET L15 — Tắc nghẽn lịch sử, BDP 10Gbps, Bufferbloat và QUIC

Đọc `stdin` `hi_bps=<int> lo_bps=<int> rtt_ms=<int> bloat_pkts=<int> bloat_mbps=<f> iw_pkts=<int> mss_B=<int>`. Tính 4 chỉ số qua các mốc lịch sử.

In đúng 3 dòng: `collapse_1986_drop=<d>x`, `bdp_10g_100ms_MB=<d>`, `bufferbloat_s=<.1f> quic_iw_B=<d>`.
Chấm tự động: `bash labs/cham.sh NET L15 duong_dan/bai_cua_ban.py`

> Lưu ý đề: `bdp_10g_100ms_MB` tính tích băng thông–trễ trên đường `10 Gbps` cố định (`10_000_000_000 * (rtt_ms/1000) // 8_000_000`); `quic_iw_B` dùng gói khởi đầu QUIC tối thiểu cố định `1200` byte (`iw_pkts * 1200`), còn `mss_B` dùng riêng cho tính `bufferbloat_s`.
