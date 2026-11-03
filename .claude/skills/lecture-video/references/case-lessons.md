# Bài tình huống chuyên gia (dùng khi soạn bài cuối mỗi khoá và khoá CAS)

Quay lại: SKILL.md, Bước 3. Template: `tools/templates/case_lesson_template.yaml` (`lv.py new … --kind case`).
Người dùng yêu cầu (2026-10-30): bài học phải vận dụng **tình huống và kinh nghiệm cụ thể của chuyên gia**, không dừng ở định nghĩa.

## 1. Hai loại tình huống
| Loại | Dùng ở | Nguồn | Con số |
|---|---|---|---|
| **Sự cố có thật** | khoá CAS; bài cuối khoá khi có sự cố kinh điển (Hawaii 2018 ở HCI, left-pad ở SEP) | báo cáo điều tra gốc, đọc nguyên văn: cơ quan nhà nước, hội đồng điều tra, bài hậu kiểm của chính công ty | chỉ con số có trong nguồn (CITED), cộng với con số tính lại được từ cơ chế (VER) |
| **Quyết định nghề nghiệp** | bài cuối các khoá còn lại (8 GPU chỉ nhanh gấp 3, gợi ý hai tầng trong 100 ms, nhấp nháy độ sâu ở xa) | tình huống tiêu biểu dựng từ cơ chế đã học | “(số minh hoạ)”; phép tính phải đúng (VER) |

## 2. Khung 6 nhịp (khớp phân cảnh bắt buộc của lint)
1. **hook:** điều đã xảy ra, hoặc quyết định phải ra, kèm con số quan sát được. Ví dụ: “8 GPU mà chỉ nhanh gấp 3”.
2. **symbol:** ngôn ngữ của người điều tra (dòng thời gian, nguyên nhân góp phần, lớp phòng vệ) hoặc của nghề (ngân sách độ trễ, phân vị 99).
3. **example:** tái hiện cơ chế bằng số. Đây là phần giá trị nhất: người học thấy con số của báo cáo tự hiện ra từ kiến thức các bài trước. Ví dụ: Patriot cắt 0,1 còn 23 bit phần lẻ thì sau 100 giờ ra đúng 0,3433 s; năm 2038 là 2³¹ − 1 giây.
4. **pitfall:** các “bài học sai” hay gặp, như đổ lỗi cá nhân, khuyên “cẩn thận hơn”, sửa triệu chứng (khởi động lại định kỳ), hay rút ra kết luận quá rộng (“đừng dùng mã nguồn mở”).
5. **quiz:** “bạn sẽ làm gì”. Đưa một biến thể của tình huống để người học ra quyết định; đáp án nêu đánh đổi, không chỉ một đáp số.
6. **recap:** thay đổi ở mức hệ thống, cộng một câu tư duy của chuyên gia. Ví dụ: “đo trước khi mua thêm phần cứng”, “sao lưu chưa khôi phục thử là giả định”.

## 3. Luật riêng
- **Chỉ khẳng định điều nguồn gốc ghi.** Chi tiết hay được kể lại mà nguồn không có thì không dạy, và ghi vào `fix` của giáo án. Ví dụ: “gói 11 dòng” của left-pad không có trong bài của npm; “bấm nhầm mục trong danh sách” ở Hawaii mâu thuẫn với báo cáo FCC (người vận hành tin là thật, còn hộp xác nhận giống hệt nhau).
- **Không nêu tên cá nhân gây lỗi**, không mỉa mai. Giọng điềm tĩnh, tôn trọng người bị ảnh hưởng.
- **Nội dung an ninh** (Heartbleed, chèn mã) chỉ ở mức khái niệm phòng thủ: điều kiện kiểm đúng, không chuỗi khai thác.
- **Nguồn ghi đủ để tra:** cơ quan, tên báo cáo, ngày. Lời đọc gọi tên nguồn như “báo cáo năm 1992 của cơ quan kiểm toán Quốc hội Mỹ”, không nói “tài liệu gốc” (E29).
- **Con số tính lại được phải được tính lại** trong VER và trong `checks`. Con số chỉ có trong nguồn thì ghi CITED, kèm trang hoặc mục của nguồn.
- **Mỗi tình huống nối về bài nền** bằng `requires_ext`, để người học thấy kiến thức nào giải thích được sự cố.

## 5. Bài hành trình theo trục thời gian (`--kind journey`, lint E40)
Người dùng yêu cầu (2026-10-31): phần nghề nghiệp phải là **best practices xây dựng từ tình huống có thật, theo trục thời gian phát triển
của chủ đề** — từ lúc khai sinh tới khi thành hệ thống lớn rất nhiều người dùng, ổn định và tiếp tục phát triển.
- **Chọn hệ thống:** một hệ thật mà chính đội làm ra đã viết lại hành trình (bài báo hội nghị, bài hậu kiểm, blog kỹ thuật của dự án).
  Mẫu: CLD L15 dùng 3 nguồn — bài báo Borg (EuroSys 2015), “Borg, Omega, and Kubernetes” (ACM Queue 2016), blog “10 Years of Kubernetes” (2024).
- **Mỗi chặng là một scene `kind: example` có `stage: {year, scale, source, practice}`**; ≥ 4 chặng, năm không giảm, tiêu đề ghi năm.
  Nguồn chặng ghi bằng nhãn ngắn `[B15]` và nhãn đó phải có trong `source:` của bài.
- **Khung một chặng:** quy mô (CITED) → điểm nghẽn → cách xử lý → thực hành tốt + điều kiện → con số tính lại (VER, `checks`).
  Ví dụ CLD L15 chặng 1: tách việc phục vụ và việc theo lô cần thêm 20–30% máy ở ô trung vị ≈ 10 000 máy → 2000–3000 máy.
- **Chặng cuối là “ổn định và tiếp tục phát triển”**: chính sách phiên bản, điểm mở rộng, nhịp phát hành, gỡ bỏ có báo trước —
  những thứ chỉ xuất hiện khi rất nhiều người cùng dùng.
- **Ghi câu trích nguyên văn** vào `audit/<khoá>/sources_<id>.md`, kèm mục “Điều KHÔNG dạy (nguồn không ghi)”.
- **Pitfall = bài học sai khi đọc lịch sử:** “có công cụ X là xong”, chép quy mô của người khổng lồ, tự chế công cụ đã được ghi là sai lầm.
- **Quiz = quyết định ở quy mô của người học** (200 máy, 5 đội), đáp án là bảng được/mất + điều kiện đổi lựa chọn.

## 4. Tự rà trước khi dựng
- [ ] Mọi sự kiện trong `show` và `say` có trong nguồn đã đọc nguyên văn; nguồn ghi ở `source`.
- [ ] Phần example tính lại ít nhất một con số của báo cáo, và kết quả khớp.
- [ ] Pitfall có ít nhất một “bài học sai” mức con người và một mức hệ thống.
- [ ] Quiz là quyết định có đánh đổi, không phải câu nhớ lại.
- [ ] Không có tên cá nhân, không có chi tiết khai thác.
