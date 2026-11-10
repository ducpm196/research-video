# Nguồn đã đọc nguyên văn cho LLM L06 và L09 (đóng hai mục "chưa kiểm được nguồn" của báo cáo đợt C, `audit/review/full_review_c/LLM.md`)
Đọc 2026-11-10 từ mã nguồn TeX chính thức trên arXiv (`arxiv.org/e-print/<id>`, tải vào thư mục riêng trong scratchpad, chỉ đọc bằng grep).

## [O22] L. Ouyang và cộng sự, *Training language models to follow instructions with human feedback*, arXiv:2203.02155 (2022) — LLM L09
- neurips_2021.tex dòng 287: “training labelers agree with each-other $72.6 \pm 1.5\%$ of the time, while for held-out labelers this number
  is $77.3 \pm 1.3\%$. For comparison, in the summarization work of \citet{stiennon2020learning} researcher-researcher agreement was $73 \pm 4\%$.”
- → Bài ghi “khoảng 73%” và trường `source` “người chấm đồng thuận 72,6 ± 1,5%”: KHỚP; đây là người chấm HUẤN LUYỆN đồng thuận với nhau
  (người chấm giữ riêng là 77,3 ± 1,3%), bài không dùng con số 77,3.

## [T23] H. Touvron và cộng sự, *LLaMA: Open and Efficient Foundation Language Models*, arXiv:2302.13971 (2023) — LLM L06
- acl2023.tex bảng 2 (dòng 221): “6.7B & 4096 & 32 & 32 & $3.0e^{-4}$ & 4M & 1.0T”; dòng 259: “\model-33B and \model-65B were trained on 1.4T
  tokens. The smaller models were trained on 1.0T tokens.”; dòng 136: “the performance of a 7B model continues to improve even after 1T tokens.”
- → “bản 7 tỉ tham số học 1 nghìn tỉ từ tố”: KHỚP (tên mô hình là LLaMA-7B; bảng 2 ghi chính xác 6,7 tỉ). Tỉ lệ “khoảng 143 từ tố mỗi
  tham số” = 1,0·10¹² / 7·10⁹ = 142,9 theo tên gọi 7B; theo 6,7 tỉ là 149 — bài dùng “khoảng”, chấp nhận; không đổi bài.
