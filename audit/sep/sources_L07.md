# Nguồn đã đọc nguyên văn cho SEP L07 (công bố lỗ hổng có phối hợp)

Đọc ngày 2026-11-02 (tải bằng curl, bỏ thẻ HTML; câu dưới đây chép nguyên văn). Ngày báo 1/1/2025 và 10/3/2025 là SỐ MINH HOẠ;
mọi ngày tháng tính lại bằng lịch thật trong `checks` (datetime) và `audit/sep/verify_parts/L07.py` (đếm số thứ tự ngày trong năm).
Chính sách có thể đổi: bài ghi rõ “đọc ngày 2/11/2026”.

## [PZ] Google Project Zero, *Vulnerability Disclosure Policy* — mục “90+30 policy”
Tải: https://googleprojectzero.blogspot.com/p/vulnerability-disclosure-policy.html
- “Project Zero follows a 90+30 disclosure deadline policy, which means that a vendor has 90 days after Project Zero notifies them about a
  security vulnerability to make a patch available to users. If they make a patch available within 90 days, Project Zero will publicly
  disclose details of the vulnerability 30 days after the patch has been made available to users.”
- “If a vendor patches a security issue 47 days after Project Zero notified the vendor about the vulnerability, details would be made
  public on day 77.”
- “If a vendor patches a security issue 83 days after Project Zero notified the vendor about the vulnerability, details would be made
  public on day 113.”
- “If a vendor is unable to patch an issue within the initial 90 days, Project Zero will make the details of the vulnerability public at
  the end of the 90-day period.”
- “If a vendor is unable to make a patch available in 90 days, but will make a patch available within an additional 14 days (i.e., within
  104 days since the vulnerability was disclosed to the vendor), Project Zero may grant a grace period to the vendor upon request.”
- “if Project Zero finds evidence that a vulnerability is being actively exploited against real users “in the wild”, a 7-day disclosure
  policy replaces the 90-day policy. However, the 30-day window still applies, meaning that Project Zero will publicly release details of
  the vulnerability 30 days after a patch is made available to users, as long as a patch was made available by the end of the 7-day deadline.”
- “In any of the above cases, Project Zero and the relevant vendor can mutually agree to release details of a vulnerability earlier than
  the date indicated by policy.”

## [HB] heartbleed.com, *The Heartbleed Bug*
Tải: https://heartbleed.com/
- “The Heartbleed bug allows anyone on the Internet to read the memory of the systems protected by the vulnerable versions of the OpenSSL software.”
- “Bug was introduced to OpenSSL in December 2011 and has been out in the wild since OpenSSL release 1.0.1 on 14th of March 2012.
  OpenSSL 1.0.1g released on 7th of April 2014 fixes the bug.”
- “Immediately after our discovery of the bug on 3rd of April 2014, NCSC-FI took up the task of verifying it, analyzing it further and
  reaching out to the authors of OpenSSL, software, operating system and appliance vendors, which were potentially affected. However,
  this vulnerability had been found and details released independently by others before this work was completed.”

## [ACM18] ACM Code of Ethics (2018), nguyên tắc 2.9
Tải: https://www.acm.org/binaries/content/assets/about/acm-code-of-ethics-and-professional-conduct.pdf
- “As threats can arise and change after a system is deployed, computing professionals should integrate mitigation techniques and
  policies, such as monitoring, patching, and vulnerability reporting. Computing professionals should also take steps to ensure parties
  affected by data breaches are notified in a timely and clear manner, providing appropriate guidance and remediation.”

## Điều KHÔNG dạy (nguồn không ghi, nghĩa không rõ, hoặc thuộc phạm vi tấn công)
- Không dạy con số “120 ngày” của câu ân hạn: nguồn viết “120 days after the vulnerability was initially disclosed to the public”,
  mâu thuẫn với cách đếm từ ngày báo cho bên sửa — chỉ nói “xin thêm 14 ngày ân hạn”.
- Không nêu tên người hay công ty phát hiện lỗi; không mô tả cách khai thác (chỉ “đọc trộm bộ nhớ” như nguồn ghi).
- “Giữ kín mãi thì bên sửa ít động lực vá” là lập luận của bài (giáo án `fix`), không gán cho Project Zero.
- Không nói mọi tổ chức đều dùng 90+30; đây là chính sách của một nhóm, đọc ngày 2/11/2026.
