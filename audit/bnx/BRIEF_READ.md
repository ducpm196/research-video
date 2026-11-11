# Đọc độc lập khoá BNX trước khi dựng video (đợt LF1, 2026-11-11)

Tiêu chí, quyền hạn và cách trả lời: **đúng như `audit/review/learn_start/BRIEF_LS1.md`** (đọc trọn tệp đó; mọi mục áp dụng), với các khác biệt sau.

- **Chưa có video.** Chưa có `<Lxx>.mp4`, `.srt`, `chapters.txt`. Đọc đặc tả `lessons/bnx/Lxx_*.yaml` (đủ `show`, `say`, `checks`, quiz) và mở ≥ 5 khung PNG
  trong `out/BNX/Lxx/frames/` (mỗi câu lời đọc là một khung, đánh số từ 00000 theo thứ tự câu). Cột "Phút" ghi số phút ước lượng (lint in "≈ … phút").
- **Lộ trình đứng trước** bài BNX: khoá JVA (Java từ con số 0: biến, rẽ nhánh, vòng lặp, mảng, hàm, lớp, chuỗi, danh sách/bản đồ, ngoại lệ, giao diện, record, enum),
  khoá BNK (bộ nhớ/GC, đa luồng, Spring Boot proxy và giao dịch, REST + khoá lũy đẳng, SQL/chỉ mục/kế hoạch thực thi, PL/SQL/khoá hàng/ORA-00060, Redis,
  Kafka phân vùng/offset, SAGA/outbox, sổ cái bút toán kép, T24/OFS/IBM MQ, ISO 8583, đối soát hai bên, khối PIN/HSM/MAC) và các bài BNX số nhỏ hơn
  (giáo án `curriculum/bnx.yaml`). Thuật ngữ chưa có ở đó thì bài phải tự giảng.
- **Nguồn của khoá**: `audit/bnx/sources.md` (được phép đọc). Dữ kiện pháp lý/chuẩn/sản phẩm không có trong đó và không do bạn tự kiểm được bằng nguồn có thẩm quyền → báo SHOULD "không nguồn".
- **Lời đọc**: chỉ JSON, YAML và các từ có trong `tools/registry/lexicon_vi.BNX.yaml` được đọc bằng tiếng nước ngoài; từ ngoại khác xuất hiện trong `say` là SHOULD.
- Mã trên màn hình đã qua cổng chạy nguyên văn (git, Python, openssl, Oracle, SQL Server). Bạn vẫn đọc xem mã có **đúng ý bài nói** không.
- Không mở `audit/bnx/screen/`, `audit/bnx/ver/`, báo cáo của người soạn (để giữ độc lập). Được đọc `audit/bnx/src/lNN.py` nếu cần hiểu cách sinh.
- Tệp tạm chỉ đặt trong thư mục scratchpad ghi trong lời nhắn. Không chạy `build`, `tts`, `asr`, `render`, `gen`, git ghi.
