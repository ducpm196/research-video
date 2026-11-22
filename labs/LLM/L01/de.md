# Lab LLM L01 — Mô hình n-gram, làm trơn cộng một và độ hỗn loạn

Một câu `3` bước dự đoán có xác suất `8/27`: tính độ hỗn loạn `(8/27)^(-1/3)`. Sau đó tính xác suất cặp chưa từng gặp khi ngữ cảnh đứng trước đã xuất hiện `3` lần trong kho và bộ từ vựng có `V = 7` từ (làm trơn cộng 1: `(0 + 1) / (3 + 7)`).

Định dạng đầu ra (1 dòng):
`perplexity=<3 chữ số> add1_unseen=<3 chữ số>`
