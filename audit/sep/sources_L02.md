# Nguồn đã đọc nguyên văn cho SEP L02 (công bằng có định lượng)

Đọc ngày 2026-11-02 (curl + pdftotext; câu chép nguyên văn từ bản trích). Hai nhóm A, B, bộ lọc hồ sơ, chương trình hỗ trợ học phí
là SỐ MINH HOẠ, tính lại trong `checks` và `audit/sep/verify_parts/L02.py`. Bài không dùng số liệu thật của công cụ nào, không nêu
tên công cụ, không bàn vụ việc cụ thể trong hai bài báo.

## [C17] A. Chouldechova, *Fair prediction with disparate impact: A study of bias in recidivism prediction instruments*, arXiv:1703.00056v1, 28/2/2017
Tải: https://arxiv.org/pdf/1703.00056 (200)
- Tóm tắt: “This paper discusses several fairness criteria that have recently been applied to assess the fairness of recidivism prediction
  instruments. We demonstrate that the criteria cannot all be simultaneously satisfied when recidivism prevalence differs across groups.”
- Định nghĩa 2 (Predictive parity): “… positive predictive value (PPV) of the classifier … be the same across groups.”
- §2.3: “When the recidivism prevalence—i.e., the base rate P(Y = 1 | R = r)—differs across groups, any instrument that satisfies
  predictive parity at a given threshold sHR must have imbalanced false positive or false negative errors rates at that threshold.”
- §2.3: “… the prevalence (p), positive predictive value (PPV), and false positive and negative error rates (FPR, FNR) are related via the
  equation FPR = p/(1 − p) · (1 − PPV)/PPV · (1 − FNR). (2.6)”
- §2.3: “From this simple expression we can see that if an instrument satisfies predictive parity—that is, if the PPV is the same across
  groups—but the prevalence differs between groups, the instrument cannot achieve equal false positive and false negative rates across
  those groups.”
- Bài giảng dùng 1 − FNR = TPR (tỉ lệ dương thật), cùng nghĩa.

## [K16] J. Kleinberg, S. Mullainathan, M. Raghavan, *Inherent Trade-Offs in the Fair Determination of Risk Scores*, arXiv:1609.05807v2, 17/11/2016
Tải: https://arxiv.org/pdf/1609.05807 (200)
- Tóm tắt: “We formalize three fairness conditions that lie at the heart of these debates, and we prove that except in highly constrained
  special cases, there is no method that can satisfy these three conditions simultaneously.”
- Định lý 1.1: “Consider an instance of the problem in which there is a risk assignment satisfying fairness conditions (A), (B), and (C).
  Then the instance must either allow for perfect prediction (with p equal to 0 or 1 for all …) or have equal base rates.”
- Ba điều kiện của [K16] (hiệu chỉnh trong nhóm, cân bằng cho lớp dương, cân bằng cho lớp âm) không trùng hệt ba tiêu chí trong bài;
  bài chỉ dẫn kết luận chung “chỉ đạt cùng lúc khi dự đoán hoàn hảo hoặc tỉ lệ nền bằng nhau”.

## [ACM18] ACM Code of Ethics (2018), nguyên tắc 1.4
Tải: https://www.acm.org/binaries/content/assets/about/acm-code-of-ethics-and-professional-conduct.pdf
- “Fairness requires that even careful decision processes provide some avenue for redress of grievances.”
- “The use of information and technology may cause new, or enhance existing, inequities.”

## Điều KHÔNG dạy (nguồn không ghi hoặc chưa đọc)
- Không dạy số liệu của công cụ chấm điểm tái phạm mà hai bài báo phân tích (bối cảnh tư pháp hình sự Mỹ) — ngoài phạm vi bài.
- Không khẳng định tiêu chí nào là “đúng” chung cho mọi bối cảnh; bảng “bối cảnh → nên ưu tiên” là lập luận theo hậu quả, ghi rõ là lựa chọn.
- Không dạy quy định pháp luật về phân biệt đối xử (chưa đọc văn bản).
