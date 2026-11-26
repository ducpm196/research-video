# Lab IRS L01 — Độ lợi tích lũy có chiết khấu và chuẩn hoá (nDCG)

Đọc từ đầu vào chuẩn (`stdin`, dạng `khoá=giá_trị`) `rels=<r1,r2,...>` là dãy mức liên quan cách nhau dấu phẩy. Tính `DCG = sum(rel / log2(i + 2))` theo chỉ số `i` bắt đầu từ `0`, tính `IDCG` trên dãy `rels` sắp giảm dần và tỷ số `nDCG = DCG / IDCG`.

In 1 dòng đúng nhãn (`<.5f>` là số thực lấy đúng 5 chữ số sau dấu chấm): `DCG=<.5f> IDCG=<.5f> nDCG=<.5f>`.
Chấm tự động: `bash labs/cham.sh IRS L01 duong_dan/bai_cua_ban.py`
