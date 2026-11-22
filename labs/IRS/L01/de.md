# Lab IRS L01 — Độ lợi tích lũy có chiết khấu và chuẩn hoá (nDCG)

Tính độ lợi tích lũy có chiết khấu tại 4 vị trí đầu (`DCG@4`) cho dãy mức liên quan `[2, 3, 1, 2]` và bản lý tưởng toàn kho `IDCG@4` cho dãy sắp xếp giảm dần theo công thức `sum(rel / log2(vị trí + 1))` với vị trí đếm từ 1. Không làm tròn trung gian.

Định dạng đầu ra (1 dòng):
`DCG=<5 chữ số> IDCG=<5 chữ số> nDCG=<5 chữ số>`
