# Lab LLM L12 — Sinh có truy xuất (RAG): chỉ mục và tìm kiếm

Cho vector câu hỏi `q = [2, 1, 0]`, hai đoạn văn trong kho `'docA': [3, 2, 1]` và `'docB': [0, 1, 4]`, trong đó nhãn đúng là `'docA'`. Viết mã tìm đoạn có độ tương tự cosin lớn nhất và tự kiểm tra `best == 'docA'` để tính `recall@1` (không gán cứng `1.0`).

Định dạng đầu ra (1 dòng):
`top1=<tên đoạn> cos=<3 chữ số> recall_at_1=<1 chữ số>`
