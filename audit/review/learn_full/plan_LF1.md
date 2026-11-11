# Kế hoạch đợt LF1 — HOC_TAP.html trọn lộ trình 0 → senior (KHMT · CNTT · AI) + khoá BNX lấp khoảng trống JD

Ngày lập: 2026-11-11. Người yêu cầu: chủ kho. Nhãn bằng chứng: OBSERVED / CITED / INFERRED / NOT_VERIFIED.

## 0. Hiện trạng đo được (OBSERVED 2026-11-11)
- `HOC_TAP.html` (đợt LS1) chỉ phủ 2 lộ trình, 119/656 bài (JVA→BNK→INT→ACB; DMS→CS112→CS115 L00–L21, L44).
- `interview/MASTER_CURRICULUM_INDEX.md` chỉ có cấp 0 (6 khoá nền), 0A JVA, 1A BNK, 1B/2 (9 khoá), 3 INT, 4 ACB. **Không có tầng AI** dù kho có AIF, DSC, MLO, LLM, AGT, IRS, CVI, RLN, DAN (128 bài).
- Quét chữ trong 656 đặc tả (`grep -rlI lessons`): 0 bài nhắc JWT, OIDC/OpenID, OpenAPI/Swagger, gRPC, Protobuf, Elasticsearch, Couchbase, SWIFT,
  ví điện tử, thuế điện tử, RabbitMQ, Oracle AQ, DDD/bounded context, Open Banking; T-SQL/SQL Server 1 bài (DBS L17, chỉ nhắc); OAuth 1 bài (WEB L09, nhắc);
  Git cơ bản: không có bài (DVO L01 nói nhánh tích hợp, không dạy lệnh).
- Ổ D: còn 9,2 GB (mỗi bài ≈ 22 MB trong `out/`) → đủ. Docker 28.3.2 chạy được → có thể chạy thật Oracle Free, SQL Server, Kafka.

## 1. Phần A — HOC_TAP.html v2 (sinh bằng `audit/review/learn_start/pack.py page`)
Hợp đồng (contract) của trang:
1. **Một dãy học duy nhất**, chia 11 chặng theo cấp của MASTER_INDEX + tầng của ROADMAP; mỗi bài đúng một chỗ (nút bài trước/sau không mơ hồ).
   Mỗi chặng = bao đóng tiên quyết (requires + requires_ext) của mục tiêu chặng, trừ bài đã xếp ở chặng trước, sắp tô pô; máy kiểm
   **mọi cạnh tiên quyết trỏ về trước** trong dãy toàn cục.
2. Chặng 1–4 = đường nhanh phỏng vấn (đúng "đường học tối thiểu" của MASTER_INDEX: JVA → BNK → [BNX] → INT → ACB).
3. Phủ **mọi bài có video** trong kho (656 + bài BNX đã dựng). Bài chưa có video hiện "đang dựng", không có liên kết.
4. Ghi nhớ lâu (chỉ dùng localStorage, có xuất/nhập tệp sao lưu):
   - tự kiểm ngay sau bài: câu hỏi + đáp án lấy nguyên từ cảnh `quiz` của đặc tả (lời đọc, không công thức thô);
   - ôn ngắt quãng theo hộp Leitner 1, 3, 7, 14, 30, 60, 120 ngày; hàng "Ôn hôm nay";
   - thẻ "chuỗi logic" từ cảnh `recap`, "lỗi hay gặp" từ cảnh `pitfall`;
   - ô "giải thích lại bằng lời của bạn" (kỹ thuật Feynman) mỗi bài;
   - nhập dấu tick cũ của LS1 (`hoc_tap_done_v1`).
5. Bảng đối chiếu JD → bài (mọi mã bài phải có thật, máy kiểm).
6. Cổng: mọi liên kết sống; `pack.py check` 0 vấn đề trên mọi bài trong trang; `--decode` chạy nền.

## 2. Phần B — Khoá BNX "Backend ngân hàng mở rộng theo JD" (khoảng trống đã đo ở §0)
Ưu tiên theo JD acbjobs (Software Engineer): Stored Procedure Oracle/MS SQL (bắt buộc), Swagger, gRPC, Oracle mới (Sharding, Queue, In-Memory, JSON),
Couchbase, Elasticsearch, Kafka/RabbitMQ, Git/Docker/K8s/GitLab CI, nghiệp vụ thanh toán quốc tế, ngoại tệ, ví điện tử, thuế điện tử; tin Lead: DDD, API Gateway, Open Banking.
Mỗi bài: nguồn Python `audit/bnx/src/lNN.py` → YAML; `verify_bnx.py` tính lại bằng đường khác; mã trên màn hình chạy thật khi máy có công cụ
(git, Python, openssl, Docker Oracle/SQL Server/Kafka); dữ kiện pháp lý chỉ từ nguồn ghi ngày, nguồn thứ cấp ghi rõ.

## 3. Rủi ro & cách chặn
- Bài mới sai dữ kiện → nguồn ghi trong `source`, `audit/bnx/sources.md`; người đọc độc lập trước khi dựng.
- Phát âm từ ngoại (JWT, gRPC…) → dò ASR bằng `audit/cs112/probe_terms.py`, không bịa phiên âm; từ không đạt → nói bằng tiếng Việt, tên gốc chỉ hiện trên màn hình.
- Trang quá nặng → dữ liệu nhúng JSON, vẽ bằng JS; đo kích thước.
- Đổi pack.py làm hỏng cổng LS1 → giữ lệnh `check`, `preview`; chạy lại trên toàn bộ.
