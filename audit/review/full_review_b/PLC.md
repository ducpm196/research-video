# PLC — đã đọc 14/14 bài

Đọc kiểm 2026-11-08: đọc mọi cảnh, mọi `show`/`say`/`checks`, quiz và đáp án của từng bài (bản trích chữ, bỏ mã SVG nhưng giữ chữ trong hình). Tổng: 7 bài đã sửa, 1 mục MUST, 11 mục SHOULD.

| Bài | Kết luận | Mục đã sửa (cảnh: MUST/SHOULD — lý do ngắn) | Nguồn | lint / render |
|---|---|---|---|---|
| L00_cac_pha_bien_dich | không phát hiện lỗi | — (chỉ sửa giáo án: thứ tự pha trong `objectives` đổi thành “tối ưu, sinh mã” cho khớp bài) | Aho và cộng sự, Compilers 2nd ed. (2006), mục 1.2 | — |
| L01_phan_tich_tu_vung | đã sửa | rules: SHOULD — luật “mẫu khai báo trước thắng” cho `if` là từ khoá, nhưng bảng ký hiệu xếp TEN trước KHOA mà bài không nói thứ tự khai báo, người học suy ngược ra “tên thắng”; thêm “bộ cắt khai báo mẫu từ khoá trước mẫu tên” (màn hình + lời đọc). automaton, recap: SHOULD — “tuyến tính theo độ dài mã” nói tuyệt đối; khớp dài nhất có lùi có thể tốn bậc hai trong trường hợp xấu → “với các mẫu từ tố thông thường… nhanh” (lời đọc vốn đã có điều kiện này) | T. Reps, “Maximal-munch tokenization in linear time”, ACM TOPLAS 20(2), 1998; Aho và cộng sự (2006) mục 3.5.3 | lint: 0 FAIL, 0 WARN, 24 PASS; render: 73 khung (0 vấn đề) |
| L02_dequy_xuong | không phát hiện lỗi | — | — | — |
| L03_cay_cu_phap | đã sửa | assoc.1: SHOULD — “cộng và nhân kết hợp được nên thứ tự gộp không đổi kết quả” sai với số thực dấu phẩy động (chính bài 11 cho ví dụ 0,1 + 0,2 + 0,3); thêm “với số nguyên… số thực dấu phẩy động có thể lệch do làm tròn”. Mẫu `audit/plc/src/L03_cay_cu_phap.tpl.yaml` đã đồng bộ | D. Goldberg, “What Every Computer Scientist Should Know About Floating-Point Arithmetic”, ACM Computing Surveys 23(1), 1991; IEEE 754-2019 | lint: 0 FAIL, 0 WARN, 23 PASS; render: 71 khung (0 vấn đề) |
| L04_pham_vi | không phát hiện lỗi | — | — | — |
| L05_kieu_du_lieu | đã sửa | hook: SHOULD — bảng đặt Java “lỗi biên dịch” cạnh JavaScript “ra "31"” mà không nói trong Java `"3" + 1` cũng ra chuỗi `"31"` (lỗi chỉ ở phép gán vào `int`) → người học hiểu sai rằng Java cấm cộng chuỗi với số; thêm ghi chú (màn hình + lời đọc). example.1: SHOULD — đọc bit số thực qua con trỏ ép kiểu trình bày như C “cho phép”; theo chuẩn đây là truy cập vi phạm luật bí danh, kết quả không được bảo đảm; thêm “chuẩn C không bảo đảm cách đọc này, nhưng trình biên dịch vẫn dịch” | JLS SE 17 §15.18.1 (String Concatenation Operator +); ISO/IEC 9899:2018 §6.5 đoạn 7 | lint: 0 FAIL, 0 WARN, 18 PASS; render: 78 khung (0 vấn đề) |
| L06_suy_luan_kieu | đã sửa | hook: MUST — “Haskell, OCaml, Rust trong thân hàm vẫn biết `nhan_doi` nhận số nguyên, trả số nguyên”: Haskell suy ra `Num a => a -> a` (không phải Int → Int), Rust bắt buộc ghi kiểu ở chữ ký hàm nên không suy ra được kiểu của chính hàm này; chỉ OCaml (phép `+ : int -> int -> int`) khớp đúng ví dụ → “như OCaml, nơi phép + chỉ dành cho số nguyên” | OCaml manual, Stdlib `( + ) : int -> int -> int` (truy cập 2026-11-08, no revision given); Haskell 2010 Report §6.4 (lớp Num); The Rust Reference, mục Functions (kiểu tham số bắt buộc) (truy cập 2026-11-08, no revision given) | lint: 0 FAIL, 0 WARN, 18 PASS; render: 65 khung (0 vấn đề) |
| L07_bao_dong | không phát hiện lỗi | — | — | — |
| L08_bo_nho | không phát hiện lỗi | — | — | — |
| L09_truyen_tham_so | đã sửa | pitfalls.0: SHOULD — lời đọc “cho mặc định là rỗng” trong khi màn hình ghi `acc=None`; “rỗng” dễ hiểu thành danh sách rỗng `[]`, chính là cái bẫy → “một giá trị đánh dấu không có gì, rồi mỗi lần gọi mới tạo danh sách mới” | Python Language Reference, mục 8.7 Function definitions (giá trị mặc định tính một lần) | lint: 0 FAIL, 0 WARN, 21 PASS; render: 73 khung (0 vấn đề) |
| L10_sinh_ma_ngan_xep | không phát hiện lỗi | — | — | — |
| L11_toi_uu | không phát hiện lỗi | — | — | — |
| L12_lap_trinh_ham | đã sửa | recap.2: SHOULD — giới thiệu bài sau ghép “khoảng 70% (2019)” của Microsoft với “dưới 20% (2025)” của Android như cùng một chuỗi số; Android 2019 là 76% → “ở Android, lỗi bộ nhớ từ 76% lỗ hổng (2019) xuống dưới 20% (2025)” | [AN22], [AN25] trong audit/plc/sources_L13.md | lint: 0 FAIL, 0 WARN, 22 PASS; render: 76 khung (0 vấn đề) |
| L13_hanh_trinh_an_toan_bo_nho | đã sửa | sym: SHOULD — “Rust an toàn nhờ kiểm lúc biên dịch” bỏ sót phần kiểm lúc chạy mà nguồn ghi → “chủ yếu nhờ kiểm lúc biên dịch, cộng một số phép kiểm lúc chạy”. stage5.0: SHOULD — “tràn bộ đệm… ở khối không an toàn” không có trong [AN25] (đã đọc lại nguyên văn: chỉ “a linear buffer overflow in CrabbyAVIF”) → bỏ, viết “trong một thư viện đọc ảnh”. stage5.2, pitfalls.1: SHOULD — “chính nó chặn / chỉ bị chặn nhờ bộ cấp phát” nói quá: lỗi được sửa trước khi phát hành, trang canh làm nó “non-exploitable” → “làm lỗi suýt lọt không khai thác được” | [AR21] (“compile-time checks … and runtime checks”), [AN25] (đọc lại 2026-11-08 tại blog.google/security/rust-in-android-move-fast-fix-things/) | lint: 0 FAIL, 0 WARN, 32 PASS; render: 118 khung (0 vấn đề) |

## Đối chiếu nguồn bài L13 (bài hành trình)
Đã tải lại và đọc nguyên văn [AQ19], [AN22], [AN24], [AN25] ngày 2026-11-08. Đã khớp nguồn:
- 90% lỗ hổng mức cao năm 2018 là UAF / tràn số nguyên / ngoài biên ([AQ19] “high severity vulnerabilities by component and cause from 2018”);
- 2 chỗ dùng `unsafe` trong UWB, việc soát tìm ra một khả năng tranh chấp ([AN22]);
- 24% năm 2024 “well below the 70% industry norm”, “majority of code still being unsafe (but… getting progressively older)”, stack canaries / CFI, sanitizers + fuzzing, 3,4x theo Alexopoulos và cộng sự (USENIX Security 2022) ([AN24]);
- năm 2023 số tuyệt đối tăng nhẹ vì “Vulnerability reports were unusually high that year” ([AN24], chú thích 3);
- “more than 1000x reduction”, lượng Rust mới “rivals that of C++”, cấp CVE-2025-48530 và hậu kiểm, lỗ hổng báo sự cố sập chưa rõ là tràn bộ đệm và đã được sửa ([AN25]).

Ngoài ba chỗ đã sửa ở trên, mọi con số và sự kiện trong năm chặng đều khớp `audit/plc/sources_L13.md`.

## Không sửa và vì sao
- L00 hook “chia cho 0: chỉ biết khi chạy”: với hằng số (`1/0`) một số trình biên dịch có cảnh báo sớm, nhưng ví dụ của bài là `a / b` với biến, nên đúng trong ngữ cảnh.
- L02 lỗi 4: “1000 lớp ngoặc → tràn ngăn xếp” thật ra là giới hạn đệ quy mặc định (1000) của trình thông dịch dùng trong `checks`, không phải giới hạn chung. Bài đã nói đúng phạm vi (“bộ phân tích vừa viết”), và `checks` chạy thật.
- L05 bước 1 xếp Java vào ô “tĩnh và mạnh” dù Java tự đổi số thành chuỗi khi ghép. Bài đã ghi “mạnh/yếu không có định nghĩa chuẩn duy nhất”, và ghi chú mới ở hook nói rõ điều này. Không đổi cách xếp ô.
- L08 “đánh dấu–quét… có lúc dừng chương trình”: các bộ thu gom gia tăng/đồng thời giảm việc dừng này, nhưng cách nói “có lúc” không sai ở mức nhập môn.
- L11 lỗi 2 “trình biên dịch chỉ đổi nhóm số thực khi bạn bật tuỳ chọn cho phép rõ ràng”: đúng với GCC/Clang (`-ffast-math`, `-Ofast` cũng là bật rõ ràng). Có thể có trình biên dịch khác mặc định khác; chưa đủ căn cứ để sửa.
- L12 hook “khoá thì chậm và dễ gây khoá chết”: là cách nói khái quát, có lý do ở khoá OSY; không phải con số hay khẳng định kiểm được.
- L13 chặng 4 bước 3 “3,4 lần ứng với tuổi thọ ≈ 4,1 năm”: đây là phép tính lại của bài (5 / ln 3,4), không phải số của nguồn. Nó đã được trình bày là phép tính và có `checks`.

## Kết quả cuối
- `audit/plc/verify_plc.py`: **67/67 PASS**
- `tools/lv.py curriculum curriculum/plc.yaml`: **curriculum: 14 bài, 14 đã có đặc tả, 0 lỗi**
- `audit/review/sync_tpl_from_lesson.py plc --write`: L03 lệch → đã ghi mẫu mới; L02, L08, L11 khớp.
- `audit/review/scan_ctrl.py`: 8 lượt, đều ở `lessons/jva/L12_so_chuyen_khoan.yaml` (khoá khác); **0 lượt ở PLC**.
- `prune_stale_asr.py`: đã xoá 1 mục `asr_reviewed` cũ ở L01 (câu luật ưu tiên đã viết lại).
- `verify_plan_curricula.py` / `rec()`: không cần đổi (không bài nào đổi số).
