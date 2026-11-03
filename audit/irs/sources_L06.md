# Nguồn bài IRS L06 — Lọc cộng tác theo láng giềng

Đọc nguyên văn ngày 2026-11-03 (pdftotext).

## [BA08] Baluja và cộng sự (WWW 2008) — URL ở sources_L13.md.
- "Co-view information provides a simple basis for video recommendations. A straightforward system, often used as the basis of item-based collaborative filtering systems [5, 1], can be built as follows. Imagine that User U watches two videos, J and K. ... Therefore, the videos we may recommend to U, based on his watches of J and K can simply be the union of the two co-view sets: L, M, N, O, P, Q."
- "if users u1 and u2 both watched a popular video, even though they have no interests in common, we will end up recommending videos watched by u2 to user u1"

## [KO09] Y. Koren, R. Bell, C. Volinsky — Matrix Factorization Techniques for Recommender Systems. IEEE Computer 42(8), 2009, tr. 42–49.
URL: https://datajobs.com/data-science-repo/Recommender-Systems-%5BNetflix%5D.pdf (bản chép; trang in “44 computer”, “46 computer” khớp bản tạp chí)
- "As the Netflix Prize competition has demonstrated, matrix factorization models are superior to classic nearest-neighbor techniques for producing product recommendations"

## [HU08] Y. Hu, Y. Koren, C. Volinsky — Collaborative Filtering for Implicit Feedback Datasets. ICDM 2008.
URL: http://yifanhu.net/PUB/cf.pdf (trang của tác giả)
- "If no action was observed r_ui is set to zero, thus meaning in our examples zero watching time, or zero purchases on record."

## Ghi chú
- Cosin giữa hai người dùng và trung bình có trọng số: toán, kiểm bằng `checks` và verify_parts/L06.py. Cosin đã dạy ở LLM bài 3 — chỉ ôn nhanh.
- Không gán tên, năm cho “GroupLens / Resnick 1994” vì chưa đọc nguyên văn (NOT_VERIFIED) — bài không nêu.
