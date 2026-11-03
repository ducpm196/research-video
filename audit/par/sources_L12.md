# Nguồn PAR L12 — tình huống chuyên gia “8 thẻ mà chỉ nhanh gấp 3”

Loại tình huống: QUYẾT ĐỊNH NGHỀ NGHIỆP (case-lessons.md mục 1) — dựng từ cơ chế đã học, không phải một sự cố có thật được điều tra.
Mọi số đo (100 phút, 25/75 phút, 2% sau khi sửa, 10% ở quiz, hạn 20 phút, 2 tuần công) là SỐ MINH HOẠ, ghi trên màn hình và ở đầu tệp bài.

## [AM67] G. M. Amdahl, “Validity of the Single Processor Approach to Achieving Large Scale Computing Capabilities”, AFIPS Conference Proceedings vol. 30, 1967, tr. 483–485
Bản in lại trong IEEE SSCS News, Summer 2007, tại https://www3.cs.stonybrook.edu/~rezaul/Spring-2019/CSE613/reading/Amdahl-1967.pdf
(bản tải của luồng chính, scratchpad par_work/src/amdahl67.txt; đọc lại 2026-11-02). Chỉ một chi tiết được dùng ở step “Ngôn ngữ”:
- “The first characteristic of interest is the fraction of the computational load which is associated with data management housekeeping. This fraction has been very nearly constant for about ten years, and accounts for 40% of the executed instructions in production runs.”
- “The nature of this overhead appears to be sequential so that it is unlikely to be amenable to parallel processing techniques.”

## Điều KHÔNG dạy
- Không nói “nạp dữ liệu luôn là thủ phạm”; bài nói ngân sách của TÌNH HUỐNG NÀY cho ra 25%.
- Không gắn tình huống với công ty, thư viện hay thẻ cụ thể nào; không nêu tên ai.
- Bài báo 1967 không có công thức (bản in lại ghi “it has no equations”); bài chỉ dẫn con số 40% và nhận xét “có vẻ tuần tự”.
