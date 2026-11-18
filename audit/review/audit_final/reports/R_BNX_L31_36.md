# S01 BNX L31–L36: đã đọc 6/6 bài (đọc trọn YAML, lab chạy như người học, video + khung hình đã có)

Ngày đọc: 2026-11-14. Người đọc độc lập (không mở báo cáo/plan/handover/sources_l*.md trước đó). Python 3.11, JDK 21.0.13, Tomcat nhúng 10.1.61 (jar ở `audit/bnx/deps/l33`). Không chạy Docker, git, build/tts/render. Tệp tạm chỉ ở scratchpad.

Ghi chú minh bạch: để biết vì sao số byte 324 ở L31 không khớp văn bản trên màn hình tôi đã liếc `audit/bnx/src/l31.py` (mã nguồn do nhà sản xuất video, không phải báo cáo); không mở gì khác trong `audit/bnx/src`.

## 1. Kết luận theo ngưỡng

| Ngưỡng | Kết quả |
|---|---|
| MUST = 0 | **KHÔNG ĐẠT: 1 MUST** (L31, mã trên màn hình không cho kết quả bài nói) |
| P1 = 2 ≥ 90% | **KHÔNG ĐẠT**: 0/6 bài P1 = 2 (4 bài P1 = 1, 2 bài P1 = 0) |
| P8 = 2 = 100% | **ĐẠT**: 6/6 |

## 2. Bảng chuẩn xác (chỉ lỗi có bằng chứng)

| Bài | Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng đã chạy | Đề xuất sửa | Tin cậy |
|---|---|---|---|---|---|---|
| L31 | **MUST** | `example` step 1 "Chạy thật: NhatKy.py" (khung 46, 4:25) | màn hình có 4 lệnh `ghi(...)`: a1 nhan, b2 nhan, a1 tru-tien, b2 doc-so-du; step 2 "Kết quả chạy thật" in **6 dòng**, gồm `{"dv":"sc","cid":"a1","ev":"loi","ma":"HET_GIO"}` và `{"dv":"cong","cid":"a1","ev":"tra","http":504}`; step 3 "a1 mat 35 ms", lời "xen kẽ qua ba dịch vụ" | Tôi chạy đúng mã trên màn hình: ra 4 dòng, đường đi a1 chỉ `cong:nhan > tt:tru-tien`, 14 ms (1014−1000), không có dịch vụ `sc`, không có lỗi HET_GIO. Thêm tay 2 lệnh `ghi("sc","a1","loi",ma="HET_GIO")` và `ghi("cong","a1","tra",http=504)` thì ra đúng 6 dòng, `cong:nhan > tt:tru-tien > sc:loi > cong:tra`, 35 ms. Khối mã không ghi "(trích)" nên người học không tái hiện được số 35 ms, "ba dịch vụ" và "lỗi nằm ở sổ cái" | thêm 2 dòng `ghi(...)` vào khối mã (hoặc ghi "(trích)" và hiện đủ) | CONFIRMED |
| L31 | SHOULD | `quymo` step 2 | "0 gia tri nhan user: 5 chuoi, 324 byte" | Văn bản chỉ số hiện ở step 4 (formula) dài 7 dòng = **277 byte** (tôi đếm). 324 chỉ đúng khi tính thêm dòng `# HELP http_requests_total ...` (47 byte) mà màn hình không hiện; `XuatChiSo.java`, `wc -c`, `grep -vc '^#'` và dòng nhãn `user="uN"} 1` cũng không hiện nên người học không tự đo lại được | hiện đủ dòng HELP hoặc ghi "chưa tính dòng HELP"; hiện lệnh đo | CONFIRMED |
| L32 | SHOULD | `formula` Bước 4 + `example` Vault | "ban moi nhat: xyz789 / ban 1: abc123"; "s3:GetObject bao-cao/rieng/b.csv -> tu choi (Deny ro rang)" | Các lệnh `vault kv put` ghi hai bản (abc123, xyz789), `kv get -version=1`, khởi động `vault server -dev`, và danh sách `CHINH_SACH` (Allow/Deny với `bao-cao/*`, `bao-cao/rieng/*`) không hiện trên màn hình: người học thấy kết quả mà không thấy đầu vào. Đường dẫn `secret/data/...` (KV v2 chèn `data`) và ký tự `*` trong `s3:Get*` không được giảng | hiện lệnh ghi hai phiên bản và bảng chính sách; một câu giải thích `*` và `/data/` | CONFIRMED (đọc màn hình + YAML) |
| L32 | SHOULD | `formula` "Bước 3 (tiếp)" | tiêu đề "đồng bộ tự động mặc định KHÔNG xoá, KHÔNG chữa" trên khối YAML có `automated: {prune: true, selfHeal: true}` | Tiêu đề nói mặc định tắt nhưng mã bật cả hai; lời đọc có giải thích ("trừ khi bật hai công tắc như ở dòng cuối") nên chỉ lệch nhẹ; đúng với tài liệu Argo CD | đổi tiêu đề thành "bật cả hai công tắc (mặc định đều tắt)" | CONFIRMED |
| L33 | SHOULD | `example` bước 1, `quymo` | "java -cp "lib/*" May app.war app app/chao ..."; "4 yeu cau, 4 luong: dong thoi toi da 4, thoi gian >= 100 ms: true" | `May.java` (khởi động Tomcat nhúng, `maxThreads=4`, Servlet ngủ 100 ms, đếm đồng thời) không hiện; màn hình chỉ in `true`, không in số ms thật. Tôi tự viết bộ khởi động và tái hiện: đồng thời tối đa 4/4/4, 243 / 1 360 / 6 190 ms (≥ 100/1 000/5 000). Kết luận bài đúng, nhưng thí nghiệm này người học không làm lại được | hiện `May.java` tối thiểu hoặc ghi rõ "mã khởi động nằm ở nguồn bài" | CONFIRMED |
| L34 | SHOULD | `hook` vs `quiz`/`formula` | hook: "dưới 100 triệu thì chuyên viên ... từ 100 đến 500 cần trưởng phòng"; quiz: "≤ 100 chuyên viên, ≤ 500 trưởng phòng"; mã `tong <= tran` | Hai cảnh nói khác nhau đúng tại biên 100 (và 500): hook cho 100 → trưởng phòng, mã/quiz cho 100 → chuyên viên. Không số nào của bài rơi đúng biên nên chưa làm sai đáp án | hook đổi thành "không quá 100 triệu ... trên 100 đến 500" | CONFIRMED |
| L34 | SHOULD | `quymo` | "SQL = "SELECT COUNT(*) FROM ls WHERE tick() AND khach = 7"" | Khối mã không có `CREATE INDEX`, không có định nghĩa `tick()` (hàm đếm dòng đọc); người học không dựng lại được cặp số 1 000 000 vs 5. Tôi dựng lại: SCAN đọc 1 000 / 1 000 000, `SEARCH ... USING COVERING INDEX (khach=?)` đọc 5, khớp | hiện `create_function("tick", ...)` và `CREATE INDEX` | CONFIRMED |
| L35 | SHOULD | `hook` | "nối tiếp với hai dịch vụ nữa cũng 99,9% thì độ sẵn sàng chung còn bao nhiêu?" | Hook hỏi 3 dịch vụ 99,9% (= 99,7003%); bài chỉ trả lời cho 99,95/99,9/99,9 = 99,7502%. Đáp án câu hỏi hook không bao giờ xuất hiện | sửa hook thành 99,95% + 99,9% + 99,9% hoặc thêm số 99,7003% | CONFIRMED (tính lại) |
| L35 | SHOULD | `intuition` hình 1 (khung 21) | thanh "99%: 432" dài 1 380, "99,9%: 43,2" dài 690, "99,95%: 21,6" dài 345, "99,99%: 4,32" dài 69; chú thích "Mỗi chữ số 9 thêm vào chia ngân sách cho 10" | Thanh không theo tỉ lệ: 43,2 là 1/10 của 432 nhưng thanh dài 1/2; 4,32 là 1/100 nhưng thanh 1/20; ô thanh thứ tư không có chữ bên trong. Hình mâu thuẫn chú thích | vẽ thanh theo tỉ lệ (hoặc thang log) hoặc bỏ thanh | CONFIRMED (đọc SVG và khung) |
| L35 | SHOULD | mục tiêu 2 (giáo án) | "Phân biệt chỉ số, mục tiêu, thoả thuận mức dịch vụ và thoả thuận nội bộ bằng ví dụ có số" | Chỉ SLI/SLO có ví dụ định tính ("≥ 99,9%"); SLA và OLA chỉ có định nghĩa chữ, không có ví dụ số nào cho OLA; "phân loại sự cố theo mức" (mục tiêu 5) chỉ có bảng P1–P4, không có ca để phân loại | thêm 1 ví dụ số cho SLA vs OLA và 1 ca phân loại | CONFIRMED |
| L36 | SHOULD | `practice` + `labs/BNX/L36/de.md` | "Trung bình = ... (1 chữ số thập phân); đỉnh = trung bình × hệ số đỉnh (làm tròn số nguyên)" | Cách đọc "nhân trung bình đã làm tròn" cho `dinh 18/s` và `18518/s`, lệch mong đợi `19` và `18519`. Tôi tính cả hai cách: chỉ cách dùng trung bình chưa làm tròn mới ĐÚNG | thêm một câu "dùng trung bình chưa làm tròn" | CONFIRMED |
| L36 | SHOULD | `quymo` step 1 | "gio = so * 10 / 60" | Giả định "10 phút xử lý tay mỗi lệnh lệch" và "100 đồng treo mỗi lệnh lệch" chỉ có trong mã/đầu ra, lời đọc và chữ trên màn hình không nêu; số 0,3 và 33,3 giờ phụ thuộc giả định này (tính lại đúng nếu 10 phút) | nêu "giả định 10 phút mỗi lệnh" (số minh hoạ) | CONFIRMED |
| L36 | SHOULD | `formula` Bước 3 vs `sym` | `sym`: "409: mã HTTP báo xung đột"; Bước 3: "bản nháp tiêu chuẩn của IETF nêu mã 422" | Bản nháp idempotency-key dùng 422 cho khoá trùng nội dung khác, 409 cho yêu cầu trùng khoá đang xử lý (đã đối chiếu nguồn). Bài chỉ giảng 409 ở bảng ký hiệu rồi dùng 422 ở bước 3, mã Python in "xung dot" không mã số → người học dễ lẫn | một câu: 409 = đang xử lý, 422 = khác nội dung | CONFIRMED (nguồn IETF) |
| L36 | SHOULD | `english` câu 4, 5 | "Retries with the same key return the saved response, including 500 errors." / "Stripe saves the status code and body of the first request ..." | Nguyên văn khớp trang Stripe hiện hành nhưng cả hai nằm trong đoạn mở đầu "For API v1, ..."; trang nay nói API v2 khác ("retries don't repeat successful operations"). Thiếu điều kiện áp dụng | thêm "(Stripe API v1)" | CONFIRMED (đối chiếu trang Stripe) |
| L36 | SHOULD | `english` | "Bốn bước đọc một câu" | Bốn bước chỉ được áp cho 1 câu mẫu (`key MUST be unique`); 10 câu còn lại chỉ có bản dịch và đầu ra của bộ lọc, không câu nào được đi qua 4 bước | đi qua 4 bước cho 1–2 câu nữa | CONFIRMED |
| L33 | SHOULD | `intuition` hình 2 | "kèm EJB, giao dịch (JTA)… theo chuẩn Jakarta EE", "Tomcat = bộ chứa Servlet, JSP, EL, WebSocket…" | Khái niệm then chốt của mục tiêu 7 (máy chủ ứng dụng đầy đủ khác bộ chứa) chỉ được nêu bằng các chữ viết tắt EJB, JTA, EL, WebSocket, "đặc tả"; lời đọc chỉ nói "thành phần doanh nghiệp" | một câu giảng EJB và giao dịch phân tán bằng lời thường | CONFIRMED |

Không có lỗi tên ngân hàng (grep 6 YAML sạch), không dạy .NET, không dạy chấm điểm tín dụng thật; có "Lưu ý pháp lý" ở L34.

### Sự kiện/phiên bản/trích dẫn đã đối chiếu
- Prometheus 3.16.0: CONFIRMED (GitHub releases, 2026-11-04). Vault 2.2.2: CONFIRMED (releases.hashicorp.com/vault có `vault_2.2.2`). Tomcat 10.1.61: CONFIRMED (jar chạy thật).
- Argo CD: automated sync mặc định không prune, không selfHeal: khớp tài liệu (đọc từ kiến thức; PLAUSIBLE, không tải lại trang). AWS IAM "mặc định từ chối, Deny rõ ràng thắng Allow": PLAUSIBLE (kiến thức, không tải trang).
- NIST "no user should be given enough privileges to misuse the system on their own": CONFIRMED (csrc.nist.gov glossary, Separation of Duty).
- SRE Book "with consequences of meeting (or missing) the SLOs", Nygard "not just the positive ones": PLAUSIBLE (không tải lại; quen thuộc).
- 10 câu tiếng Anh L36 so nguyên văn: câu 1 (RFC 9110 §15.5.10, đủ đầu câu), 3 (draft idempotency-key), 4 và 5 (Stripe), 6 và 7 (PostgreSQL 17), 8 (SRE Book), 9 (RFC 9110), 10 (RFC 9110 §9.2.2) = **khớp 9/10 CONFIRMED**; câu 2 chỉ xác nhận được phần đầu "An idempotency key is a unique value generated by the client which the resource uses to recognize subsequent retries" (công cụ tải cắt phần cuối "of the same request") nên phần đuôi PLAUSIBLE. Câu 4/5 lược "For API v1," (xem trên). Bộ lọc tôi dựng lại cho ra đúng 1 cấm+bắt buộc, 1 bắt buộc, 2 nên, 6 mô tả.

## 3. Bảng độ sâu

| Bài | sha16 | Phút (lời đọc / cả video có dừng) | P1 | P2 | P3 | P4 | P5 | P6 | P7 | P8 | P9 | Tổng (P1–P7) | Mất gốc | Cần biết trước | Chỗ thiếu chính |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L31 | 612665a399fb88ff | 11,9 / 15,4 | 1 | 1 | 2 | 2 | 2 | 2 | 1 | 2 | 2 | 11 | GẦN | JSON, biểu thức chính quy (`code=~"5.."`), Docker/ảnh Docker | mã NhatKy.py thiếu 2 dòng (MUST); đo byte không hiện lệnh |
| L32 | 6d0d427007c88e1d | 12,0 / 15,6 | 1 | 1 | 2 | 2 | 2 | 2 | 1 | 2 | 2 | 11 | GẦN | bộ cân bằng tải, `*` trong chính sách, KV v2 `/data/`, namespace/manifest | lệnh Vault và bảng CHINH_SACH không hiện; mục tiêu 3 "chạy kho bí mật" chỉ xem kết quả |
| L33 | 0bf1afc4620303b9 | 11,9 / 16,6 | 0 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 12 (có một mục 0) | GẦN | EJB, JTA, EL, WebSocket, đặc tả, Spring Boot (câu 3) | khái niệm máy chủ ứng dụng đầy đủ chưa giảng; May.java không hiện |
| L34 | b66c0069917a9b00 | 12,2 / 15,4 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | SQL, "kho đọc", "bộ đệm", "nhóm bên liên quan" | `tick()`/CREATE INDEX không hiện; biên 100 hook lệch |
| L35 | 30fcfdecd4a5821d | 11,4 / 15,0 | 1 | 2 | 1 | 2 | 2 | 2 | 1 | 2 | 2 | 11 | GẦN | p95, hàng đợi (tin nhắn), Decimal/Fraction, "lỗi độc lập" | hình thanh không theo tỉ lệ; hook hỏi 3×99,9% nhưng đáp số khác; SLA/OLA không có số |
| L36 | fa59992bc5f466a8 | 12,4 / 15,7 | 0 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 11 | GẦN | sổ cái, hàng đợi, cầu dao, thử lại có lùi, bản sao đọc, chia theo khoá, giao dịch cơ sở dữ liệu, mức cô lập, lỗi tuần tự hoá | bốn bước đọc tiếng Anh chỉ áp cho 1 câu; thuật ngữ hạ tầng dùng không giảng |

Phút lời đọc = cuối SRT trừ tổng `pause` (210/210/270/190/210/190 s); lời đọc ≤ 16 phút ở cả 6 bài (SRT khớp `say` từ-từ-từ, độ khớp 1,0; đây chỉ là bản ghi chữ, không kiểm được TTS đọc thế nào; ASR có 7/3/14/3/4/3 câu "gắn cờ chưa xem xét", `asr_reviewed: []`, phần lớn do ASR nghe sai "Tomcat", "Python"). L33 cả video 16:34 vì có 270 s chờ.

Giải thích điểm: P1 = số thuật ngữ dùng để dạy mà không giảng ở bất cứ đâu trong bài (≥3 hoặc khái niệm then chốt → 0). P2: L31/L32 có bước người học không thấy đầu vào; L36 bốn bước đọc chỉ làm cho một câu. P3 L35: hình thanh sai tỉ lệ. P7: L31 mục tiêu 1 không đạt do MUST; L32 mục tiêu 3 "Chạy" chỉ xem kết quả; L35 mục tiêu 2 và 5 thiếu số/ca.

### Đối chiếu mục tiêu giáo án ↔ video (E51 `covers`)
Cả 6 bài có đủ `covers` cho 8 (L34: 7) mục tiêu và cảnh trỏ tới thật sự dạy nội dung đó (đã kiểm từng cặp). Lệch nội dung (đã nêu ở bảng 2): L31 mục tiêu 1; L32 mục tiêu 3; L35 mục tiêu 2, 5; L36 mục tiêu 6 (chỉ 1 câu đi qua 4 bước). Mô tả `example` trong `curriculum/bnx.yaml` L31–L36 khớp số trên màn hình (đã đối chiếu từng số).

## 4. Lab (làm như người học: đọc de.md, tự viết, `bash labs/cham.sh BNX Lxx <tệp>`, mới so loi_giai khi cần)

| Bài | Tự làm được | Thời gian | Kẹt ở đâu | mong_doi khớp |
|---|---|---|---|---|
| L31 | có | chấm 2,7 s; viết ước tính 5–8 phút (ước tính, không bấm giờ) | không kẹt; cần biết `round`, `sorted(key=)` (có gợi ý trên màn hình) | ĐÚNG lần đầu |
| L32 | có | chấm 2,2 s; ước tính 8–10 phút | không kẹt; hai hàm phải nhớ thứ tự `sua`/`tao` trước `xoa` | ĐÚNG lần đầu |
| L33 | có | chấm 6,1 s (javac); ước tính 10–15 phút | thứ tự `destroy` "theo thứ tự tạo": đề không nhắc `LinkedHashMap`; tôi dùng `HashMap` và qua do thứ tự băm (/vi trước /en) — có thể sai ở JDK/chuỗi khác | ĐÚNG lần đầu (với `HashMap`, may) |
| L34 | có | chấm 2 s; ước tính 5–8 phút | không kẹt | ĐÚNG lần đầu |
| L35 | có (giấy bút, đối chiếu `loi_giai.md`) | ước tính 10 phút | khung ADR: danh mục kiểm nằm trong `loi_giai.md`, phải mở loi_giai mới thấy; cham.sh không hỗ trợ `.md` (đúng như lời bài) | 4 dòng khớp `mong_doi.txt` (tôi tính tay: 89,28; 99,4005; 5,72) |
| L36 | phần | chấm 2 s; ước tính 8–10 phút | làm tròn đỉnh: dùng trung bình đã làm tròn thì sai (18 vs 19, 18518 vs 18519) | ĐÚNG sau khi dùng trung bình chưa làm tròn |

Đề đủ để tự làm: có cả 6 (chỉ cần thư viện chuẩn). P8 = 2 cho cả 6: đều có việc cụ thể, số khác ví dụ bài, kết quả mong đợi hiện ngay trên màn hình.

## 5. Người học kẹt ở đâu (một dòng mỗi bài)
- L31: `example` step 1, khối NhatKy.py (khung 46, 4:25): chạy đúng mã trên màn hình ra 4 dòng, không ra "a1 mat 35 ms"; trước đó chỉ vấp nhẹ ở `code=~"5.."`.
- L32: `intuition` hình 2: "cổng vào (bộ cân bằng tải)" chưa giảng; và `example` Vault: không thấy lệnh ghi hai phiên bản.
- L33: `intuition` hình 2: "kèm EJB, giao dịch (JTA)…" không giảng, khiến mục tiêu "phân biệt Tomcat với JBoss" chỉ còn là thuộc lòng.
- L34: `quymo` step 1: `WHERE tick() AND khach = 7` (`tick` không định nghĩa, không thấy chỉ mục được tạo).
- L35: `formula` Bước 5, phiếu mẫu: "p95 độ trễ 4,2 giây (bình thường 0,8)" chưa giảng p95; và hook hỏi 3×99,9% mà đáp số khác.
- L36: `formula` Bước 4: "việc lưu khoá và ghi sổ nằm trong một giao dịch cơ sở dữ liệu" (giao dịch CSDL chưa giảng); sau đó Bước 6 "chia theo khoá", "bản sao đọc".

## 6. Số đã tính lại / mã đã chạy
- Số tính lại bằng Python (Decimal/Fraction/float) và so với màn hình + lời đọc: ≈ 150 con số (L31 ≈ 18, L32 ≈ 20, L33 ≈ 18, L34 ≈ 26, L35 ≈ 32, L36 ≈ 36). Khớp: **tất cả phép tính số học đều khớp**; ngoại lệ không phải số học: byte 324 (L31) chỉ khớp khi có dòng HELP không hiện (277 + 47 = 324).
  - Ví dụ đã kiểm: 30/6 000 = 0,005; 0,005/0,001 = 5 → 6 ngày; quiz 216 phút, 4, 7,5 ngày, 6 000 và 6 000 000 chuỗi; 4×100+1 = 401, 4×10 000+1 = 40 001; 1+n lần gọi Git (11/201/10 001); 10 001 × 30 ms = 5,0005 phút; 90×24 = 2 160, 720/0,25 = 2 880; 7 lần thử = 5 + 2; 270 = 90+90+90; 220/40; 10⁹; 432/43,2/21,6/4,32; 0,9995×0,999² = 0,997502 → 99,7502% → 107,91 phút; 47−43,2 = 3,8; 99,8912%; 90,4792%, 0,0045%, 4 113,0 và 43 198,0 phút; 89,28 / 99,4005 / 5,72; 2,3/23, 231,5/2 315/2 nút, 23 148,1/231 481/116 nút; 0,1/10/1 000 GB; 125/54; 200/33,3 giờ; quiz 10,4/62,5/1 nút; lab 19/18 519/38 nút.
- Mã đã chạy: NhatKy.py (L31; chỉ khi thêm 2 dòng mới ra kết quả trên màn hình); chỉ mục đảo (1/2 và 1 000/2 000); vòng đối chiếu L32 (mô phỏng 8 bước, git thay bằng danh sách phiên bản — **không chạy git** theo BRIEF; kết quả 8 dòng khớp, kể cả lệch 1 ở bước 3 và 7); Tomcat nhúng 10.1.61 thật (L33): init 1 lần, bộ đếm 1-2-3, .war có các mục như màn hình, JSP 0 → 2 tệp và yêu cầu hai không thêm tệp, mã sinh ra có `extends HttpJspBase` và dòng 122–125 `out.write/out.print` trùng, `javac` báo đúng "package javax.servlet.http does not exist", bể 4 luồng: đồng thời tối đa 4 cho 4/40/200 yêu cầu, 243/1 360/6 190 ms; máy trạng thái + tra cứu có đồng ý + SCAN/SEARCH bằng sqlite3 (L34); toàn bộ Decimal/Fraction L35; ước lượng, khoá lũy đẳng, bộ lọc 10 câu (L36). 6/6 lab ĐÚNG.
- **Không chạy được/không chạy**: promtool và Prometheus 3.16.0 (không có, cấm Docker), Vault 2.2.2 (Docker), Argo CD, AWS, JBoss/WildFly; các kết quả này (up = 1, SUCCESS, thẻ 4 giây…) chỉ kiểm bằng lý luận (luật cảnh báo `for: 2m` bắn ở phút 4 hợp lý với chuỗi `0+995x12`) và đọc mã: "chưa kiểm chạy". Phiên bản đã kiểm bằng nguồn (mục 2).

Về "chạy thật" và "mô phỏng": L31 hình 1 và 2 ghi rõ "MÔ PHỎNG phần lập chỉ mục bằng Python / Grafana chỉ giảng", lời đọc nhắc lại; L32 ghi rõ "MÔ PHỎNG ... không chạy Argo CD hay Kubernetes", "mô phỏng, không phải AWS", "chế độ này chỉ để học" cho Vault dev; L33 ghi "Chạy thật: Tomcat nhúng" (đúng, tôi tái hiện) và "JBoss/WildFly chỉ giảng"; L34 "Python + sqlite" thật (đúng); L35/L36 mã Python thật (đúng) và số đều ghi "số minh hoạ". Không phát hiện chỗ nói "chạy thật" mà không có thật, ngoại trừ phần không kiểm được ở trên (Docker).

## 7. Khung hình đã xem (≥ 5 mỗi bài) và lỗi hiển thị
- L31: 00000, 00019, 00025, 00046, 00055, 00071, 00102, 00112 (8).
- L32: 00021, 00048, 00053, 00059, 00064, 00071, 00103 (7).
- L33: 00023, 00035, 00051, 00067, 00099 (5).
- L34: 00019, 00033, 00054, 00070, 00109 (5).
- L35: 00021, 00028, 00046, 00068, 00094 (5).
- L36: 00027, 00052, 00079, 00085, 00115 (5).
Lỗi hiển thị: L35 khung 21 (thanh không theo tỉ lệ, ô thanh thứ tư trống chữ). L34 khung 19: chữ đỏ "nhảy cóc thẳng tới giải ngân..." nằm sát đường nét đứt nhưng đọc được. Không thấy chữ tràn/đè/cắt ở các khung còn lại; cỡ chữ đọc được; phụ đề dưới khớp lời đọc. Mã trên màn hình khớp YAML; riêng L31 khung 46 là bằng chứng của MUST.

## 8. Nhận xét chung
- Số học, ước lượng và quy mô (P9) của 6 bài đều đúng và có hai ba mức quy mô; điểm yếu duy nhất về số là các giả định ẩn (10 phút/lệnh, 100 đồng treo, byte tính cả dòng HELP).
- Lỗi cần sửa trước khi phát: khối mã `NhatKy.py` L31 (thiếu 2 lệnh); đây là điểm duy nhất vi phạm "mã trên màn hình phải cho kết quả bài nói".
- Mẫu lặp lại: kết quả "chạy thật" hiện đủ nhưng đầu vào (lệnh Vault, bảng chính sách, `May.java`, `tick()`, `XuatChiSo.java`) không hiện; người học xem được mà không tái hiện được. Nên hiện đầu vào tối thiểu hoặc nói rõ "mã nằm ở nguồn".
- P1 là chỗ tụt ngưỡng: thuật ngữ hạ tầng/CSDL (EJB, JTA, bộ cân bằng tải, hàng đợi, cầu dao, bản sao đọc, chia theo khoá, giao dịch CSDL, p95) được dùng mà không giảng, dù cảnh `prereq`/`sym` đã cố gắng; L33 và L36 thấp nhất.
- Không có tên ngân hàng, .NET, chấm điểm tín dụng thật hay trích điều luật; số tiền/bậc/nhóm nợ đều ghi "số minh hoạ"; có lưu ý pháp lý. Trích dẫn tiếng Anh đúng nguyên văn (kèm điều kiện áp dụng của Stripe v1 cần thêm).
- Ba lỗi nhỏ về nhất quán nội bộ dễ sửa: hook L34 (biên 100), hook L35 (3×99,9% vs 99,95/99,9/99,9), hình thanh L35.
- Lab đều chấm được, cả 6 qua ngay; cải thiện đề: L36 (làm tròn), L33 (thứ tự destroy), L35 (danh mục kiểm nằm trong lời giải).
- Chưa kiểm tai người (TTS đọc "Tomcat", "Python", "Prometheus"); chưa kiểm chạy Prometheus/promtool/Vault vì cấm Docker.
