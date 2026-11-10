# MLO — đã đọc 15/15 bài

Đọc toàn bộ `show`, `say`, `checks`, quiz và đáp án của 15 bài `lessons/mlo/`. Khoá không có mẫu `*.tpl.yaml` (`audit/mlo/src/` không tồn tại) nên không cần đồng bộ mẫu. Tổng: 11 bài sửa, 1 mục MUST, 16 mục SHOULD.

| Bài | Kết luận | Mục đã sửa (cảnh: MUST/SHOULD — lý do ngắn) | Nguồn | lint / render |
|---|---|---|---|---|
| L00 | đã sửa | sym: SHOULD — “nơi phần lớn lỗi xảy ra” không có trong bài báo, đổi thành “hạ tầng rộng lớn và phức tạp, nơi tích tụ phần lớn công sức duy trì”; pitfalls bước 3: SHOULD — “làm hỏng nhiều hơn chọn sai thuật toán” là khẳng định tuyệt đối, thêm “thường” | Sculley và cộng sự, Hidden Technical Debt in ML Systems, NIPS 2015, §5 (“only a small fraction … ML code … surrounding infrastructure is vast and complex”) | lint: 0 FAIL, 0 WARN, 19 PASS; render: 69 khung (0 vấn đề) |
| L01 | đã sửa | pitfalls bước 2: SHOULD — “bộ xử lý đồ hoạ cộng theo thứ tự thay đổi mỗi lần” là tuyệt đối; sửa thành “một số phép tính … có thể đổi giữa các lần chạy” | PyTorch docs, Reproducibility (pytorch.org/docs/stable/notes/randomness.html, truy cập 2026-11-08, no revision given) | lint: 0 FAIL, 0 WARN, 25 PASS; render: 74 khung (0 vấn đề) |
| L02 | đã sửa | quiz đáp án 1: SHOULD — xác suất trùng 1/2^48 chỉ đúng cho một cặp tệp; thêm “kho hàng triệu tệp phải giữ đủ 256 bit” (nghịch lý ngày sinh); pitfalls bước 3: SHOULD — “sửa 10 lần là 50 GB” thành “có thể tới 50 GB, vì tệp dữ liệu lớn thường nén kém”; xoá 1 mục `asr_reviewed` cũ (E30), sửa `focus` | FIPS 180-4 (SHA-256 256 bit); Pro Git, §10.4 Packfiles (git-scm.com, truy cập 2026-11-08, no revision given) | lint: 0 FAIL, 0 WARN, 22 PASS; render: 64 khung (0 vấn đề) |
| L03 | đã sửa | recap tư duy: SHOULD — “kiểm thử hành vi cho biết nó đúng vì lý do đúng” nói quá; sửa thành “giúp kiểm xem … đạt chưa chứng minh, trượt thì chắc chắn có lỗi” | Ribeiro và cộng sự, CheckList, ACL 2020, §1 (kiểm thử hành vi tìm lỗi, không chứng minh đúng) | lint: 0 FAIL, 0 WARN, 22 PASS; render: 65 khung (0 vấn đề) |
| L04 | không phát hiện lỗi | — | — | — |
| L05 | đã sửa | pitfalls bước 1: SHOULD — “nguồn lệch phổ biến nhất” không có nguồn; đổi thành “một nguồn lệch hay gặp” (sửa kèm `curriculum/mlo.yaml` L05 `fix`) | Zinkevich, Rules of ML (2017), quy tắc 32 (dùng chung mã giữa huấn luyện và phục vụ; không xếp hạng “phổ biến nhất”) | lint: 0 FAIL, 0 WARN, 20 PASS; render: 63 khung (0 vấn đề) |
| L06 | không phát hiện lỗi | — | — | — |
| L07 | đã sửa | example bước 1: SHOULD — “đúng 5 lần trên 100 thì báo nhầm” thiếu điều kiện “khi thật ra không có khác biệt”; pitfalls bước 1 và recap: SHOULD — “chỉ thử nghiệm hai nhóm trả lời được” tuyệt đối, đổi thành “cách đáng tin nhất” (tách câu dài cho phụ đề) | Kohavi, Tang, Xu, Trustworthy Online Controlled Experiments (2020), ch. 1–2 (thử nghiệm có đối chứng là chuẩn vàng, không phải cách duy nhất) | lint: 0 FAIL, 0 WARN, 20 PASS; render: 70 khung (0 vấn đề) |
| L08 | không phát hiện lỗi | — | — | — |
| L09 | đã sửa | quiz đáp án 2: SHOULD — đáp án nói “trôi khái niệm” và “trôi dữ liệu nếu…”; nhưng đổi cách viết chắc chắn đổi P(x), nên sửa thành “thường là cả hai”, và nói rõ tỉ lệ rác không đổi chỉ cho biết P(y) không đổi | Gama và cộng sự, A Survey on Concept Drift Adaptation, ACM CSUR 46(4), 2014, §2.1 (phân biệt trôi P(x), P(y\|x), P(y)) | lint: 0 FAIL, 0 WARN, 21 PASS; render: 73 khung (0 vấn đề) |
| L10 | đã sửa | pitfalls bước 2: SHOULD — “mạng lớn thường nói 0,99 cho cả những ca nó sai (Guo 2017)” không phải điều bài báo viết; sửa thành “thường quá tự tin: độ tự tin trung bình cao hơn tỉ lệ đúng thật” | Guo, Pleiss, Sun, Weinberger, On Calibration of Modern Neural Networks, ICML 2017, §1–3 | lint: 0 FAIL, 0 WARN, 21 PASS; render: 68 khung (0 vấn đề) |
| L11 | đã sửa | example bước 1 và quiz đáp án 1: MUST — màn hình ghi 1,3 / 0,01575 ≈ 82,55 và −0,7 / 0,01575 ≈ −44,45, trong khi chia cho 0,01575 cho 82,54 và −44,44; đổi thành chia cho 2/127 (đúng 82,55 và −44,45), thêm `checks` | tính lại (Python): 1,3·127/2 = 82,55; −0,7·127/2 = −44,45 | lint: 0 FAIL, 0 WARN, 25 PASS; render: 62 khung (0 vấn đề) |
| L12 | đã sửa | pitfalls bước 1: SHOULD — “mô hình vẫn đối xử khác nhau; ta không còn đo được” tuyệt đối; sửa thành “có thể vẫn…”, và thêm: giữ cột nhạy cảm để đo theo nhóm; pitfalls bước 4: SHOULD — “chênh lệch là thật” đổi thành “khó là do may rủi” (khoảng tin cậy không chứng minh) | Hardt, Price, Srebro, Equality of Opportunity, NeurIPS 2016, §1 (bỏ thuộc tính nhạy cảm không đủ vì thuộc tính thay thế; cần thuộc tính để đo) | lint: 0 FAIL, 0 WARN, 19 PASS; render: 65 khung (0 vấn đề) |
| L13 | không phát hiện lỗi | — | — | — |
| L14 | đã sửa | stage2 nhánh thử nghiệm: SHOULD — “thường chỉ một phần nhỏ [nhánh đang chạy]” không có nguồn, bỏ; stage3: SHOULD — “mỗi tập huấn luyện có hàng trăm tỉ mẫu” đổi thành “một tập điển hình” theo nguồn; intuition và recap (lời đọc): SHOULD — “mã học máy chỉ chiếm khoảng 5%” đổi thành “có thể chỉ chiếm nhiều nhất 5%” như [SC15]. Đã kiểm thêm (PDF TX17 qua pdftotext): “trading off slower model-loads” và khởi động ấm “same quality … fewer resources” đúng nguồn; ghi bổ sung vào `audit/mlo/sources_L14.md` | [SC15] §5 (“might end up being (at most) 5% machine learning code”); [TX17] §6.1, §4.1, §7 (“The typical training dataset size is hundreds of billions of examples”) | lint: 0 FAIL, 0 WARN, 32 PASS; render: 129 khung (0 vấn đề) |

## Không sửa và vì sao
- L01 hook: “hôm qua 93,3%, hôm nay 86,7%, không ai sửa mã” ngầm hiểu là sổ ghi chép không cố định hạt giống; cảnh hình dung nói rõ hai con số là hạt giống 5 và 7, nên không sửa.
- L03 lỗi 2: “đổi đơn vị mét sang xăng-ti-mét … dự đoán sai hết”, “sai hết” hơi mạnh, nhưng đây là ví dụ minh hoạ về sai lệch hệ thống và vẫn đúng về hướng. Không sửa vì đây là chuyện văn phong.
- L05 tư duy: “mô hình chỉ đúng với đúng thứ nó đã thấy lúc học” là câu khẩu hiệu nói quá về tổng quát hoá; giữ vì ngữ cảnh là lệch huấn luyện–phục vụ.
- L06 lỗi 1: màn hình ghi “như CLD”, lời đọc nói “khoá Hệ thống hướng dịch vụ”, đúng tên khoá CLD (`curriculum/cld.yaml`), nên không lệch.
- L13 cảnh đầu vào đối kháng: dời 0,15 trên giá trị 0,1 thì không còn “rất nhỏ”, nhưng đây là mô hình đồ chơi tuyến tính và có nói rõ ở cảnh ký hiệu. Giữ.
- L14: “nền tảng 2007 chạy khoảng 14 năm rồi ngừng” khớp nguyên văn [TH20] (“in production for ~14 years”, mục “Sibyl (2007 – 2020)”), dù 2007 + 14 lệch một năm so với 2020. Giữ theo nguồn.
- `rec()` của `audit/verify_plan_curricula.py` cho MLO không cần đổi: không bài nào đổi số chính.

## Kết quả bộ kiểm
- `audit/mlo/verify_mlo.py`: `TỔNG: 20 PASS · 0 FAIL`
- `tools/lv.py curriculum curriculum/mlo.yaml`: `curriculum: 15 bài, 15 đã có đặc tả, 0 lỗi`
- `audit/review/scan_ctrl.py`: không có lượt nào ở `lessons/mlo/` (8 lượt còn lại đều thuộc `lessons/jva/`, khoá khác).
