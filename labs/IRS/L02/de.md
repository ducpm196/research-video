# Lab IRS L02 — Mô hình không gian vector: trọng số từ hiếm và cosin

Cho kho 3 văn bản `docs = ['xe dap nhanh', 'xe dien ben', 'xe dien dep']` với câu hỏi `'xe dien'`. Viết mã đếm số văn bản chứa mỗi từ (`df`), tính độ hiếm `idf = ln(N / df)` cho mọi từ trong từ vựng `['xe', 'dap', 'nhanh', 'dien', 'ben', 'dep']`, dựng vector TF-IDF (`tf * idf`) của câu hỏi và hai văn bản `'xe dien ben'`, `'xe dien dep'`, rồi tính độ tương tự cosin giữa câu hỏi với từng văn bản đó.

Định dạng đầu ra (1 dòng):
`idf_xe=<1 chữ số> idf_dien=<3 chữ số> cos_d2=<3 chữ số> cos_d3=<3 chữ số>`
