# Nguồn bài IRS L00 — Đo chất lượng truy hồi: độ chuẩn xác, độ phủ và hạng nghịch đảo trung bình

Đọc nguyên văn ngày 2026-11-03 (PDF tải bằng curl, trích chữ bằng `pdftotext`). Định nghĩa P@k, R@k, RR là toán, kiểm bằng `checks` và
audit/irs/verify_parts/L00.py; sự kiện có thật chỉ lấy từ câu trích dưới đây.

## [JK02] K. Järvelin, J. Kekäläinen — Cumulated Gain-Based Evaluation of IR Techniques. ACM TOIS 20(4), 10/2002, tr. 422–446.
URL: https://www.fi.muni.cz/~xkohout7/Research/clanky_cizi/evaluation/p422-jarvelin.pdf (bản chép trên trang Đại học Masaryk; chân trang in “ACM Transactions on Information Systems, Vol. 20, No. 4, October 2002”; dl.acm.org trả trang chặn Cloudflare)
- "The seventh Text Retrieval Conference (TREC-7) had an ad hoc track in which the participants produced queries from topic statements--50 altogether--and ran those queries against the TREC text document collection. The collection included about 528,000 documents, or 1.9 GB data. Participants returned lists of the best 1000 documents retrieved for each topic."
- "TREC is based on binary relevance judgments with a very low threshold for accepting a document as relevant--the document needs to have at least one sentence pertaining to the request to count as relevant"
- "More often relevance is conflated into two categories at the analysis phase because of the calculation of precision and recall"

## [BA08] S. Baluja và cộng sự — Video Suggestion and Discovery for YouTube (WWW 2008). URL ở sources_L13.md.
- "we will measure (variants of) precision and recall (respectively, whether the user watched what the algorithm recommended, and whether the algorithm recommended everything the user watched)."
- "Recall at t, given by recall t(W, R) = |W ∩ Rt|/|W|."
- "(1) Hindsight is not 20/20: If a suggestion is made to a user that the user did not view in the evaluation period, marking it incorrect is not necessarily appropriate."

## [CO16] P. Covington, J. Adams, E. Sargin (RecSys 2016). URL ở sources_L13.md.
- "During development, we make extensive use of offline metrics (precision, recall, ranking loss, etc.) to guide iterative improvements to our system."

## NOT_VERIFIED
- E. Voorhees, The TREC-8 Question Answering Track Report (1999), trec.nist.gov/pubs/trec8/papers/qa_report.pdf và qa8.pdf: bản PDF là ảnh quét (pdftotext ra 6 byte và 119 từ) → không dạy chi tiết cách chấm của hội nghị (số câu trả lời, độ dài), chỉ dạy định nghĩa hạng nghịch đảo.
- Manning, Raghavan, Schütze, Introduction to Information Retrieval (2008), chương 8 (gộp kết quả để chấm): nlp.stanford.edu không kết nối được (hết giờ cổng 443), web.archive.org trả 429 → lời giảng KHÔNG khẳng định quy trình gộp của một hội nghị cụ thể; chỉ suy ra bằng số (50 câu hỏi × 528 000 tài liệu = 26,4 triệu cặp) rằng không thể chấm hết, nên độ phủ trên kho lớn chỉ ước lượng được (INFERRED).
