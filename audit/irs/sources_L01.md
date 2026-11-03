# Nguồn bài IRS L01 — Độ lợi tích luỹ có chiết khấu và chuẩn hoá (nDCG)

Đọc nguyên văn ngày 2026-11-03 (pdftotext). Mọi con số tính lại ở `checks` và audit/irs/verify_parts/L01.py.

## [JK02] K. Järvelin, J. Kekäläinen — Cumulated Gain-Based Evaluation of IR Techniques. ACM TOIS 20(4), 2002. URL ở sources_L00.md.
- "--highly relevant documents are more valuable than marginally relevant documents, and --the greater the ranked position of a relevant document, the less valuable it is for the user, because the less likely it is that the user will ever examine the document."
- "Assume that the relevance scores 0 to 3 are used (3 denoting high value, 0 no value)."
- "G = 3, 2, 3, 0, 0, 1, 2, 2, 3, 0, . . ." ; "CG = 3, 5, 8, 8, 8, 9, 11, 13, 16, 16, . . ."
- "A discounting function is needed that progressively reduces the document score as its rank increases but not too steeply (e.g., as division by rank) to allow for user persistence in examining further documents. A simple way of discounting with this requirement is to divide the document score by the log of its rank. For example, 2log 2 = 1 and 2log 1024 = 10, thus a document at the position 1024 would still get one tenth of its face value."
- "DCG[i] = CG[i], if i < b ; DCG[i − 1] + G[i]/blog i, if i ≥ b." ; "Note that we must not apply the logarithm-based discount at rank 1 because blog 1 = 0."
- "For example, let b = 2. From G given in the preceding section we obtain DCG = 3, 5, 6.89, 6.89, 6.89, 7.28, 7.99, 8.66, 9.61, 9.61, . . ."
- "The (D)CG vectors for each IR technique can be normalized by dividing them by the corresponding ideal (D)CG vectors, component by component."
- "Note that the ideal vector is based on the recall base of the search topic rather than on the result of some IR technique."
- "The base-2 models impatient users and base-10 persistent ones."

## [BU05] C. Burges, T. Shaked, E. Renshaw, A. Lazier, M. Deeds, N. Hamilton, G. Hullender — Learning to Rank using Gradient Descent. ICML 2005.
URL: https://icml.cc/Conferences/2015/wp-content/uploads/2015/06/icml_ranking.pdf (bản đăng lại trên trang ICML)
- "N_i ≡ N_i Σ_{j=1}^{15} (2^{r(j)} − 1)/ log(1 + j) (16) where r(j) is the rating of the j'th document, and where the normalization constant N_i is chosen so that a perfect ordering gets NDCG score 1."
- "Note that unlabeled documents does not contribute to the sum directly, but will still reduce the NDCG by displacing labeled documents"

## Điều dạy khác giáo án cũ (đã ghi vào `fix` của curriculum/irs.yaml, VER IRS:L01 dòng thứ hai)
- Dạng 1/log₂(vị trí + 1) là dạng [BU05] dùng (với độ lợi 2^r − 1); dạng gốc [JK02] với b = 2 không chiết khấu vị trí 1, chia log₂ i từ vị trí 2. Bài dạy dạng phổ biến (như giáo án) và nêu dạng gốc ở step `notation_note`, kèm ví dụ của chính bài báo (3, 5, 6,89).
