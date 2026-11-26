# Lab WEB L11 — Node.js: tính độ tương phản màu WCAG 2.1

Đọc `stdin` `c1=<#hex> c2=<#hex> bg=<#hex>`. Đổi từng kênh `c = v/255` sang tuyến tính (`c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4`), tính độ chói tương đối `L` và tỉ số tương phản `(L1 + 0.05) / (L2 + 0.05)` rồi kiểm đạt chuẩn `AA >= 4.5`.

In đúng 3 dòng: `ratio_777=<.2f>`, `ratio_767676=<.2f>`, `aa_pass_pair=<0|1>,<0|1>`.
Chấm tự động: `bash labs/cham.sh WEB L11 duong_dan/bai_cua_ban.js`
