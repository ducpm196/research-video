# Khoá BNX, phần mở rộng theo CV (L16–L23) — bản giao việc soạn bài (đợt LF2, 2026-11-11)

**Vì sao có phần này.** Người dùng yêu cầu (2026-11-11): bài học không chỉ phủ JD mà phủ cả **CV** (`resources/job/PHAM-MINH-DUC-SENIOR-INTEGRATION-CV.md`), để bị hỏi bất cứ dòng nào trên CV cũng trả lời được. Máy đo `audit/review/learn_final/cv_scan.py` (kết quả `audit/review/learn_final/logs/cv_scan.out`) cho thấy các mục sau có trên CV mà chưa bài nào dạy: ForkJoinPool, CompletableFuture, Spring Security, Spring Cloud, JUnit 5, Mockito, Redis Cluster, Go/Fiber, AEM (OSGi, Sling, HTL, JCR), Scikit-Learn, LOS/LMS, chấm điểm tín dụng, ECM, dấu vân tay thiết bị, trường đa trị T24.

**Luật nền: đọc trọn và làm đúng `audit/bnx/BRIEF.md`** (khung 10 cảnh, mã chạy nguyên văn, checks, bộ kiểm độc lập, luật lời đọc, 5 cổng, phạm vi tệp được sửa). Tệp này chỉ thêm các điểm riêng của L16–L23.

## Điểm riêng
1. **Người học** đã học JVA, BNK, BNX L00–L15. Bài phải tự đủ; không viện "khoá trước", "như đã học ở…" (cổng `check_xref` chặn): nhắc lại nội dung bằng một mệnh đề ngay tại chỗ.
2. **Góc phỏng vấn theo CV.** Mỗi bài có trong cảnh `recap` (hoặc step cuối của `quiz`) một bảng "Nếu bị hỏi về dòng này trên CV": 3 câu hỏi người phỏng vấn hay hỏi và ý trả lời một dòng cho mỗi câu, bám đúng điều bài vừa dạy. Không bịa số liệu của OCB, MAFC, ACB hay bất kỳ tổ chức thật nào; không nói ứng viên "đã làm X ở quy mô Y". Số minh hoạ ghi "(số minh hoạ)".
3. **Kinh nghiệm vận hành theo thời gian.** Cảnh `pitfall` phải có ít nhất một lỗi "người đã đi làm" gắn với giai đoạn: lúc mới dựng, lúc tải tăng, lúc vận hành lâu dài (ví dụ: bể luồng không giới hạn hàng đợi lúc tải tăng; khoá Redis hết hạn khi tiến trình dừng lâu; ca kiểm phụ thuộc đồng hồ thật).
4. **Mã chạy thật.** Máy có JDK 21/22, Go, Python 3.13, Node, Docker, git, openssl, curl. Thư viện ngoài (JUnit Platform Console Standalone, Mockito, byte-buddy, objenesis, Spring, redis, scikit-learn, skl2onnx, onnxruntime…): được tải bằng `curl` từ Maven Central hoặc `pip install` vào **thư mục riêng `audit/bnx/deps/lNN/`** (không cài vào `.venv`, không sửa `requirements.txt`). Ghi phiên bản và sha256 của từng tệp tải về vào `audit/bnx/deps/lNN/README.md`. Bộ kiểm `ver/lNN.py` và mục sổ `screen/lNN.yaml` gọi đúng các tệp đó; thiếu tệp thì trả SKIP (cổng FAIL có nhãn NOT_VERIFIED), không PASS lặng lẽ. Container Docker mới đặt tên `bnx-lNN-*`, tự dựng và tự gỡ trong bộ kiểm (như `bnx-kafka` của L10); không chạm `bnx-ora`, `bnx-mss`.
   Thứ không chạy thật được trên máy (ví dụ một máy chủ AEM) thì dạy bằng mô phỏng Python nhỏ + trích nguyên văn tài liệu chính thức, và **nói rõ trên màn hình** phần nào là mô phỏng.
5. **Nguồn.** Dữ kiện về sản phẩm (mặc định, phiên bản, hành vi) chỉ lấy từ tài liệu chính thức bạn mở và đọc nguyên văn trong phiên (WebFetch), thêm dòng vào cuối `audit/bnx/sources.md`: mã, dữ kiện trích nguyên văn, URL, ngày đọc 2026-11-11, mức CITED. Không mở được nguồn thì không dạy dữ kiện đó.
6. **Lời đọc.** Tên ngoại chưa có luật trong `tools/registry/lexicon_vi.BNX.yaml` thì không viết trong `say`; nói bằng tiếng Việt, tên gốc hiện trên màn hình (ví dụ "bể luồng", "lời hứa kết quả", "bộ khung kiểm thử", "đối tượng giả", "cụm Redis" nếu Redis đã có luật, "ngôn ngữ Gâu" KHÔNG được: nói "ngôn ngữ thứ hai trên CV, tên hiện trên màn hình").
7. **Giáo án.** Mục của bài bạn trong `curriculum/bnx.yaml` do người điều phối viết (tiêu đề, mục tiêu, ví dụ, fix). Chép NGUYÊN VĂN tiêu đề và mục tiêu. Nếu khi chạy thật bạn thấy một con số trong `example` sai (ví dụ số khe băm), **đừng sửa giáo án**: dạy con số đúng, và báo lại trong báo cáo cuối để người điều phối sửa giáo án và VER.
8. **Không chạy** `build`, `tts`, `asr`. `lv.py render` tốn RAM: chạy từng bài một, không chạy song song hai lệnh render.

## Bài và phạm vi
| Bài | Chủ đề | Dòng CV được phủ |
|---|---|---|
| L16 | Đa luồng Java nâng cao: ExecutorService, CompletableFuture, ForkJoinPool | "Java advanced multithreading (ForkJoinPool, CompletableFuture, ExecutorService)" |
| L17 | Spring Security và Spring Cloud | "Spring Cloud, Spring Security", "Spring Security OAuth2", "Consul" |
| L18 | JUnit 5 và Mockito | "automated tests (JUnit 5, Mockito)" |
| L19 | Redis nâng cao: cụm, khoá SET NX EX, khử trùng theo mã giao dịch, danh sách đen mã truy cập | "Redis Cluster", "Redis Mutex SET … NX EX 300", "transId 60s TTL", "JWT blacklist in Redis" |
| L20 | Go cho backend: goroutine, kênh, dịch vụ HTTP nhỏ, Fiber | "Go (Golang)", "Fiber (Go)" |
| L21 | Hệ thống cho vay số: LOS/LMS, chấm điểm, thẩm định DTI, ký số và lưu hồ sơ, chống gian lận, trường đa trị T24 | "LOS/LMS", "credit scoring, underwriting decision engine", "Cloud CA … ECM document sync", "2FA, device fingerprinting", "multi-value fields (OfsDataField)" |
| L22 | Adobe Experience Manager: JCR, Sling, HTL, OSGi | "AEM Sites 6.4/6.5, OSGi bundles, Sling Models, HTL components, JCR" |
| L23 | Từ scikit-learn tới ONNX Runtime: rừng cô lập cho phát hiện bất thường | "Scikit-Learn, ONNX Runtime, Isolation Forest" |
