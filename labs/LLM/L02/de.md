# Lab LLM L02 — Tách từ tố: mã hoá cặp byte (BPE)

Trên từ điển tần suất `{'s t a r </w>': 7, 's t a r t </w>': 4, 'c a r </w>': 3, 'f a r </w>': 2}`, chạy 2 bước học luật gộp liên tiếp. Quy tắc: chọn cặp liền nhau có tổng tần suất cao nhất; nếu nhiều cặp hoà tần suất thì chọn cặp xuất hiện đầu tiên.

Định dạng đầu ra (2 dòng):
`merge1=<a+b> freq=<số nguyên>`
`merge2=<a+b> freq=<số nguyên>`
