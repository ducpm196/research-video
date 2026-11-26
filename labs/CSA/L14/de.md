# Lab CSA L14 — Bộ nhớ ảo & TLB: dịch địa chỉ và tính EAT

Đọc `stdin` `va=<hex> pfn=<hex> page_bits=<int> tlb_hit=<f> tlb_ns=<f> ram_ns=<f>`. Tách VPN, offset, ghép địa chỉ vật lý và tính EAT.

In đúng 3 dòng: `vpn=0x<XX> offset=0x<XXX>`, `phys_addr=0x<XXXXX>`, `eat_ns=<.2f>`.
Chấm tự động: `bash labs/cham.sh CSA L14 duong_dan/bai_cua_ban.py`
