# Nguồn bài HCI L06 — Kiểm thử khả dụng: bao nhiêu người thử là đủ

Đọc và tra cứu 2026-11-03. Nhãn dùng trong `source:` của bài.

## [NL93] J. Nielsen, T. K. Landauer, “A mathematical model of the finding of usability problems”, INTERCHI ’93 (Proceedings of the INTERACT ’93 and CHI ’93 Conference on Human Factors in Computing Systems), trang 206–213, 1993
| Công thức / kết quả (trạng thái đối chiếu nguồn 2026-11-09; **chưa đọc được toàn văn [NL93]**) | Dùng ở |
|---|---|
| “$\text{Found}(i) = N(1 - (1 - \lambda)^i)$” — trong đó $i$ (hoặc $n$) là số người thử độc lập, $\lambda$ là xác suất trung bình một người thử gặp và bộc lộ một vấn đề khả dụng — **NOT_VERIFIED nguyên văn trong [NL93]**; dạng tương đương có trong bài nhắc lại của chính Nielsen [NN00]: số vấn đề tìm được với $n$ người là $N(1-(1-L)^n)$ (công thức dạng ảnh), “where *N* is the total number of usability problems in the design and *L* is the proportion of usability problems discovered while testing a single user.” — **VERIFIED theo [NN00]** | cảnh suy ra công thức, ví dụ, tự kiểm |
| Giá trị trung bình $\lambda \approx 0{,}31$ (31%) — **VERIFIED theo [NN00]**, nguyên văn: “The typical value of L is 31%, averaged across a large number of projects we studied.” Chưa đối chiếu được con số và số dự án trong chính [NL93] | hook, ví dụ 5 người ($1 - 0{,}69^5 \approx 84{,}4\%$) và 15 người ($1 - 0{,}69^{15} \approx 99{,}6\%$) |
| Chia ngân sách thành nhiều vòng thử nhỏ — **VERIFIED theo [NN00]** (không phải [NL93]), nguyên văn: “The ultimate user experience is improved much more by 3 studies with 5 users each than by a single monster study with 15 users.” và “After the first study with five participants has found 85% of the usability problems, you will want to fix these problems in a redesign.” Phần “lợi ích kinh tế giảm dần” trong [NL93]: NOT_VERIFIED | ví dụ so sánh 1 vòng 15 người với 3 vòng 5 người |
| Giá trị $\lambda$ khác nhau đáng kể giữa các dự án — **NOT_VERIFIED** (không đọc được [NL93]; [NN00] không nêu khoảng dao động của L) | cảnh lỗi thường gặp (`fix` của giáo án) |

## [NN00] J. Nielsen, “Why You Only Need to Test with 5 Users”, Nielsen Norman Group, 18/3/2000
URL: https://www.nngroup.com/articles/why-you-only-need-to-test-with-5-users/ (truy cập 2026-11-09). Bài ghi nguồn: Nielsen & Landauer, Proceedings of ACM INTERCHI’93 (Amsterdam, 24–29/4/1993), pp. 206–213.

## Điều KHÔNG dạy / NOT_VERIFIED
- Không dạy công thức chi phí – lợi ích đầy đủ có tham số chi phí cố định và chi phí biến đổi trên mỗi người thử của [NL93] (không cần cho mục tiêu bài).
- Các con số tổng số lỗi cụ thể trên một sản phẩm giả định (ví dụ 20 lỗi ở vòng 1, sửa xong lộ thêm 10 lỗi ở vòng 2, và trường hợp lỗi khó có $\lambda = 0{,}10$) là **SỐ MINH HOẠ** được kiểm chứng bằng `alg.hci_nielsen_found` trong `checks`.
- Không đọc tên riêng `Nielsen`, `Landauer`, `INTERCHI` trong `say:` — chỉ hiển thị trên màn hình; lời đọc nói “hai nhà nghiên cứu năm 1993”.

## Đối chiếu nguồn mở 2026-11-09 (BN-0040)
- [NL93]: không đọc được toàn văn. dl.acm.org (DOI 10.1145/169059.169166) trả trang kiểm tra Cloudflare/HTTP 403; course.ccs.neu.edu/is4800/ssl/nielsen93.pdf chuyển về trang chủ khoá học; web.archive.org trả 429 và không có bản lưu. Mọi dòng gán cho [NL93] để NOT_VERIFIED ở mức nguyên văn.
- [NN00] đọc được: xác nhận công thức $N(1-(1-L)^n)$, L = 31% “averaged across a large number of projects we studied”, 5 người tìm được 85%, khuyên 3 vòng × 5 người thay cho 1 vòng 15 người; bài ghi trang 206–213 cho [NL93] (khớp tiêu đề tệp này).
- Số liệu bài: $1 - 0{,}69^5 \approx 0{,}844$ khớp “85%” làm tròn của [NN00]. Không thấy mâu thuẫn; chỉ cần ghi đúng là ý “3 vòng 5 người” đến từ bài năm 2000, không phải bài báo 1993.
