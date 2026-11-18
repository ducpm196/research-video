# fix_R_BNX_L12_23 — sửa BNX L12–L23 theo R_BNX_L12_23 (2026-11-14)

Quy trình mỗi bài: sửa nguồn `audit/bnx/src/lNN.py` -> `gen.py` -> lint -> render -> `verify_bnx.py` -> `screen_keep.py`/`screen_fast.py`. Không chạy build/tts/asr/audit_all/git/docker. Lời đọc (từ, tính bằng `say`): L12 2237, L13 2289, L14 2292, L15 2251, L16 2300, L17 ~2250, L18 2297, L19 2291, L20 2283, L21 2234, L22 2291, L23 ~2290 (đều <= 2300).

## MUST (2/2 sửa; mục "video cũ lệch YAML" do người điều phối)
1. L13 quymo bước 4: màn hình "tụt tới 25% sức chứa" -> "tụt 25% (còn 75% sức chứa)"; lời đọc nói rõ "tụt hai mươi lăm phần trăm, còn lại bảy mươi lăm"; curriculum `fix` cùng sửa.
2. L13 quymo bước 3: "mỗi đợt thay một phần tư" -> "một nửa số bản: một phần tư thiếu cộng một phần tư thừa".
- L15 srt "như bài 1 đã dạy": YAML L15 không còn câu nhắc khoá khác (check_xref/check_course_refs chạy cuối đợt, xem bảng cổng).

## SHOULD đã sửa
- L12: bất biến "cuối ngày" -> "mọi lúc (cùng một thời điểm), cuối ngày đối soát để kiểm", dẫn TT40 Điều 27 khoản 1; hàng NĐ52 đổi thành "nghị định nền, bài không dẫn điều cụ thể"; mũi tên SVG1 không nhãn bỏ; thêm suy ra n(n+1)/2 (quét i phần tử), gloss ns, def/return/range/break.
- L13: "luôn 2 đợt" -> "2 đợt ở 4/40/400 bản; D chia 4 dư 3 cần 3 đợt" (ghi chú trên bảng, claims, curriculum, ver); "hơn 1 giờ 40" -> "đúng"; nhãn "Kết quả của mô hình Python (không phải cụm Kubernetes thật)" ở check, ghi chú mô hình ở example, de.md lab ghi mô hình.
- L14: 180 ngày + "trừ khi khách và ngân hàng thoả thuận khác"; hook "bắt đầu mở ... có lộ trình chuyển tiếp"; thêm hàng Điều 5/Điều 15 (API chỉ cấp cho ngân hàng/trung gian thanh toán; lộ trình tới 01/3/2027) ghi "theo bản dịch tiếng Anh, cần kiểm lại" (nguồn: người đọc dùng bản dịch, chưa mở lại bản gốc tiếng Việt); "cụm thực thể/aggregate" thống nhất thành "cụm đối tượng (aggregate)".
- L15: de.md và gợi ý ghi "nhân bằng số chưa làm tròn (41,6 vs 41,7)"; practice hiện đủ 4 chặng (cổng 12, xác thực 6, dịch vụ 25, Oracle 120, Redis 3); ghi chú quymo: 40 ms/lệnh là mô hình, số thật cao hơn (cận dưới).
- L16: nhãn dòng "số lượt" = phép tính từ công thức (không đo); "(chạy thật ở bộ kiểm)" của orTimeout -> "theo mô tả Javadoc Java SE 21; bài không chạy thử"; công thức (4)(5) tách khỏi ô nổi bật (step riêng, hai dòng riêng).
- L17: mã Spring hiện đủ để gõ lại: CauHinh 4 khung (import 1–11, 12–21, 22–30, 31–38) và ChayThu 6 khung (import+biến 1–10, hàm ký 11–18, thu 19–29, main 30–38, 39–49, 50–53), bảng 21 tệp jar + phiên bản + `-cp`; khoá đổi đúng 32 byte (kiểm len); giải thích khoá chung (bài thử) vs khoá công khai (issuer-uri); 35 s/10 s ghi "số minh hoạ" + giải thích bộ đệm; ghi chú bộ chia thật bắt đầu ngẫu nhiên; `exp`/giờ Unix, CSRF, @Configuration, lambda; lab ghi "mô hình Python". Sổ `audit/bnx/screen/l17.yaml` cập nhật bằng script (nguồn CauHinh/ChayThu theo bản mới).
- L18: nhãn lab "mô hình Java thuần, không JUnit/Mockito"; gloss classpath/jar (nguồn tải), sed -i, bảng static/lambda/Instant/Clock/binarySearch; "nên sinh từ bảng" -> cách viết ca từ bảng mốc.
- L19: hook: Cluster tách khỏi "ba dòng chặn trùng/thu hồi"; "Giây không" -> "Ở giây số không, mục chưa có nên đặt được"; bảng gloss nút chính/bản sao, ràng buộc duy nhất, thu gom rác, docker run/exec, heredoc, hàm shell, hệ 16.
- L20: "hai chỗ lược kiểm lỗi" -> ba chỗ (kể cả dòng mở cổng); quiz 3 "thường chọn" -> "nên cân nhắc"; bảng cú pháp Go (:=, defer, func(){}(), range/_, struct, &, go run, ống grep|uniq).
- L21: nhắc TT 37/2025/TT-NHNN sửa TT 31/2024 (lời + ghi chú; registry đã có mục CHUA_KIEM từ trước, không thêm); bảng cờ openssl (genrsa, .pem, 2>/dev/null, dòng error stderr) đặt TRƯỚC khung ký; gloss T24/OFS, giải ngân.
- L22: "5 nút" -> "6 nút (5 dưới gốc + nút gốc, như hàm duyet)" (check giữ (5,2) của checklib cộng 1); MANIFEST: "Trong khai báo này ... dù có cách khai từng lớp bằng dòng khác"; gloss Import-Package, BundleException, DS, Oak, XSS.
- L23: quy tắc int(p(n-1))+1 ghi "đúng khi các điểm khác nhau" (prereq, bước 5, de.md) + ghi chú dòng 1 005 (3 613 giá trị khác nhau trên 101 000 điểm, điểm trùng ở ngưỡng); nối 15,8 và 11,88 (hai thước đo); lệnh pip + phiên bản thư viện; bảng gloss numpy/ONNX/log2.
- E51: đổi động từ mục tiêu cho đúng điều bài làm (bài + `curriculum/bnx.yaml`): L13 (1: "Đọc Dockerfile ... sắp thứ tự lệnh"; 4: "Nêu cách gắn thẻ ảnh"), L14 (1,3,4 "Nêu ..."), L15 (3,4), L16 (3 "nêu cơ chế"), L17 (2 "Đọc cấu hình ..."), L18 (1,2: tự lập ca/viết cổng giả ở lab, đọc JUnit/Mockito), L20 (1,4 "Đọc ...").
- P1/E52: thêm mục sổ `tools/registry/symbols.BNX.yaml` (nhóm "L13–L23", Edit nhỏ ở cuối danh sách): bnx_workdir_expose, bnx_secret_k8s, bnx_saga_outbox, bnx_atomic_coll, bnx_csrf, bnx_classpath, bnx_sed_i, bnx_binary_search, bnx_thu_gom_rac, bnx_go_defer, bnx_genrsa, bnx_xss, bnx_ds, bnx_numpy_rng, kèm `introduces` tại step giảng; `assumes`: L15 (saga_outbox), L18 (classpath). L17 giảng base64url tại chỗ (introduces) vì chuỗi L17 không qua L03 (theo người điều phối).

## Không sửa / lưu ý
- Mục MUST "video lệch YAML": người điều phối dựng lại.
- L16 `GhepLoiGoi` chỉ in "chờ dưới 900 ms: true": giữ, không in thời gian đo (phụ thuộc máy).
- L19 Redis/Docker thật, L20 Fiber, L17 Spring Cloud: không chạy lại (không đổi nội dung kiểm).
- E52: không đăng ký thuật ngữ nhiều bài dùng (replica, lambda, Oak, pip) để khỏi buộc bài khác `assumes`.
- L21 `audit/bnx/screen/l21.yaml`: mục OFS đoạn trích có `within` trỏ khung số 11 (sửa tay vì khung đổi chỉ số); đừng chạy lại `screen_keep.py L21` trước khi kiểm.
- TT 64 Điều 5/11 khoản 6/15 chỉ dựa bản dịch tiếng Anh; registry ghi TT 64 đã đọc bản gốc OCR nhưng chưa đối chiếu các điều này: ghi "cần kiểm lại" trên màn hình và trong `source`.
