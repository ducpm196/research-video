# Lab OSY L09 — Dịch địa chỉ ảo (VPN + offset) và tính EAT với TLB

Đọc `stdin` `pt=<k:v,...> va=<hex> page_bits=<int> tlb_hit=<f> tlb_ns=<f> ram_ns=<f>`. Tách số trang ảo (`VPN = va >> page_bits`) và độ dời (`offset`), ghép khung vật lý thành `pa`, và tính thời gian truy cập hiệu dụng (`EAT = tlb_hit*(tlb_ns + ram_ns) + (1 - tlb_hit)*(tlb_ns + 2*ram_ns)`, lưu ý cộng `tlb_ns` vào cả nhánh trúng lẫn trượt TLB).

In đúng 3 dòng: `va=0x<XXXX> vpn=<d> offset=0x<XXX>`, `pa=0x<XXXX>`, `eat_ns=<.1f>`.
Chấm tự động: `bash labs/cham.sh OSY L09 duong_dan/bai_cua_ban.py`
