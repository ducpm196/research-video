# Nguồn đã đọc nguyên văn cho SEP L03 (giải thích được, lý do phản chứng, nhật ký quyết định)

Đọc ngày 2026-11-02 (curl + pdftotext). Mô hình chấm điểm vay (0,5 × thu nhập + 2 × năm, ngưỡng 20), chị Hoa, anh Nam, anh Tuấn,
luật “dưới 2 năm thì từ chối”, mô hình ba thuộc tính của quiz là SỐ MINH HOẠ, tính lại trong `checks` và `audit/sep/verify_parts/L03.py`.

## [W17] S. Wachter, B. Mittelstadt, C. Russell, *Counterfactual Explanations without Opening the Black Box: Automated Decisions and the GDPR*, arXiv:1711.00399 (11/2017; sau đăng Harvard Journal of Law & Technology)
Tải: https://arxiv.org/pdf/1711.00399 (200)
- Tác giả thuộc Oxford Internet Institute (University of Oxford) và The Alan Turing Institute (London) — lời đọc nói “ba nhà nghiên cứu ở Anh”.
- §II: “"You were denied a loan because your annual income was £30,000. If your income had been £45,000, you would have been offered a loan."”
- §II: “Here the statement of decision is followed by a counterfactual, or statement of how the world would have to be different for a
  desirable outcome to occur. Multiple counterfactuals are possible, as multiple desirable outcomes can exist”
- §II: “The concept of the "closest possible world," or the smallest change to the world that can be made to obtain a desirable outcome,
  is key throughout the discussion of counterfactuals. In many situations, providing several explanations covering a range of diverse
  counterfactuals corresponding to relevant or informative "close possible worlds" rather than "the closest possible world" may be more helpful.”
- §II: “Knowing the smallest possible change to a variable or set of variables to arrive at a different outcome may not always be the most
  helpful type of counterfactual. Rather, relevance will depend also upon other case-specific factors, such as the mutability of a variable
  or real world probability of a change.”
- Tiêu đề bài báo nhắc “without opening the black box” — dùng cho ý “không cần mở hộp đen, chỉ cần hỏi mô hình với đầu vào đã đổi”.

## [ACM18] ACM Code of Ethics (2018)
Tải: https://www.acm.org/binaries/content/assets/about/acm-code-of-ethics-and-professional-conduct.pdf
- 1.3: “provide full disclosure of all pertinent system capabilities, limitations, and potential problems to the appropriate parties.”
- 1.4: “Fairness requires that even careful decision processes provide some avenue for redress of grievances.”

## Phần do bài tự lập luận (không gán cho nguồn)
- Công thức “thay đổi cần = khoảng thiếu / trọng số” là phép giải phương trình bậc nhất của mô hình tuyến tính minh hoạ.
- Lỗi 1 (mô hình xấp xỉ sai ở đúng người cần giải thích) là ví dụ dựng sẵn cho phát biểu trong `fix` của giáo án; không trích nguồn.
- Bảng nhật ký (thời điểm, phiên bản mô hình, ngưỡng, đầu vào, điểm, lý do đã gửi) là thực hành đề xuất, không phải yêu cầu của văn bản luật.

## Điều KHÔNG dạy (nguồn không ghi hoặc chưa đọc)
- “Quyền được giải thích” theo GDPR — [W17] bàn kỹ nhưng văn bản GDPR không tải được (eur-lex 202/429): NOT_VERIFIED, không dạy.
- Không dạy các phương pháp giải thích khác (giá trị đóng góp, mô hình thay thế cục bộ) ngoài lời cảnh báo chung ở Lỗi 1.
