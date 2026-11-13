# Báo cáo BNK → chuẩn AF2 (15 bài L00–L14), 2026-11-13

**Kết luận: 15/15 bài xong.** Không dựng (`build`/`tts`/`asr`), không chạy `audit_all.py`, `final_gates.sh`, git.

## Cổng đã chạy (lần cuối, sau mọi sửa)
| Cổng | Kết quả |
|---|---|
| `lv.py lint` 15 bài (`af2: true`, E51/E53) | 0 FAIL, 0 WARN ở cả 15 |
| `lv.py render` 15 bài | 0 vấn đề ở cả 15 |
| `screen_code.py check --course BNK` | 90 khối trên màn hình, 47 nguồn chạy thật: PASS 137, FAIL 0, STALE 0, MISSING 0, ORPHAN 0, WARN 0 |
| `lab_gate.py BNK` | 15 PASS, 0 FAIL (đường chấm `labs/cham.sh`) |
| `audit/bnk/verify_bnk.py` | 36/36 PASS (21 cũ + 15 dòng mới: số ở cảnh quy mô tính lại độc lập) |
| `check_xref.py --course BNK` | 0 lượt tham chiếu sang khoá khác |
| `check_legal.py` | không còn lỗi liên quan BNK (1 FAIL còn lại: `interview/MASTER_CURRICULUM_INDEX.md` dẫn trơn TT 50/2024; ngoài phạm vi) |
| `check_next_refs.py` | 0 lệch dãy học |
| `scan_ctrl.py` | 0 lượt ở `lessons/bnk`; `grep -c 0x08` ở `audit/bnk/*.py`, `audit/bnk/src/*.py`: 0 |

Thời lượng lời đọc ước lượng (lint): L00 15,2 · L01 14,1 · L02 13,7 · L03 13,7 · L04 12,5 · L05 14,3 · L06 14,2 · L07 13,9 · L08 13,0 · L09 12,8 · L10 13,5 · L11 15,4 · L12 13,2 · L13 14,8 · L14 13,4 phút (đều trong 9–16).

## Mã chạy thật trên màn hình (trước: 0/15 bài)
Mỗi bài có cảnh `chay_that` (kind example) với khối mã ≤ 12 dòng/khung và đầu ra thật; mã khai bằng `prog(...)` trong `audit/bnk/lib.py`, sổ `audit/review/screen_code/BNK.yaml` sinh bằng `audit/bnk/screen_gen.py` (mỗi chương trình là một nguồn `src:BNK:…` chạy nguyên văn; khối màn hình là `fragment`/`output` của nguồn).
| Bài | Công cụ chạy thật | Ghi chú |
|---|---|---|
| L00 | JDK 21: `WeakReference` + `System.gc()`, `Runtime`, static map giữ heap, `BigDecimal`, `==` / `equals` | 5 chương trình |
| L01 | JDK 21: race `dem++` (sai), `synchronized` (đúng 2 000 000), 10 000 luồng ảo | |
| L02 | JDK 21 `java.lang.reflect.Proxy` mô phỏng proxy; ghi rõ "Spring thật dùng cơ chế này" | Spring jar ở `audit/bnx/deps` là của BNX L17+, không có `spring-tx`/CSDL nên không dùng |
| L03 | JDK 21 `com.sun.httpserver` + `curl` thật (6 lệnh) + sqlite `PRIMARY KEY` | máy chủ chạy nền trong bash, dọn bằng `trap … wait` |
| L04 | sqlite 3.49: `CREATE INDEX`, `EXPLAIN QUERY PLAN` (SCAN → SEARCH → SCAN) | nhắc bản sqlite < 3.36 ghi `SCAN TABLE` |
| L05 | **Oracle 26ai Free thật** (container `bnx-ora`, PL/SQL `FOR UPDATE` theo thứ tự id) + Java `ReentrantLock.tryLock` mô phỏng bế tắc | một cổng Oracle tại một thời điểm; bảng `bnk_tk` |
| L06 | Java mô phỏng cache-aside và mã chặn (Redis không chạy; ghi rõ là mô phỏng) | |
| L07 | Java mô phỏng chia phân vùng và thứ tự ghi nhớ (Kafka không chạy; ghi rõ) | |
| L08 | Java SAGA + sqlite Outbox (`BEGIN … COMMIT` / `ROLLBACK`) | |
| L09 | sqlite sổ cái, `GROUP BY`, bút toán đảo | |
| L10 | Java mô phỏng mã tương quan và hết giờ chờ (T24, IBM MQ không có trên máy; ghi rõ) | |
| L11 | Python 3.13 dựng và đọc bản tin ISO 8583 | |
| L12 | Python 3.13 đối soát hai sổ bằng hai từ điển | |
| L13 | Python 3.13: khối PIN `041225EEEEEEEEEE`, che số thẻ, HMAC-SHA256 (khoá thử), Luhn (lab) | |
| L14 | sqlite: đối soát mã thừa, bút toán đảo, kiểm số dư | |

## Mỗi bài còn có
- Cảnh `practice` (Tự làm) trước `recap` + `labs/BNK/Lxx/{de.md, mong_doi.txt, loi_giai.*}` (8 Java, 3 Python, 4 SQL), số liệu khác ví dụ, `af2: true` + `covers` (mục tiêu viết đúng điều bài làm; mục tiêu đổi động từ "Giải thích/Vẽ/Mô tả" thành "Nêu/Nhận ra" khi bài không dạy làm).
- Cảnh `quy_mo` (P9): số ở ×1, ×100, ×10 000, giải pháp cũ gãy ở đâu, đánh đổi; số minh hoạ ghi "(số minh hoạ)"; mọi số có `checks` và dòng riêng trong `verify_bnk.py`.
- P1 tại chỗ: thêm bảng định nghĩa trong `prereq` cho mọi thuật ngữ/cú pháp mới (máy khách–máy chủ, đối tác, `Thread`/`start`/`join`, `curl` và cờ, tiêu đề, cổng, câu SQL, khoá chính, Map, mô phỏng, nhịp báo còn sống, tác dụng phụ, phép dịch bit, từ điển/danh sách lọc, cắt chuỗi, HMAC…). Không dùng "như đã học ở khoá X".
- Thuật ngữ thống nhất: "hàm tạo" (L02), "nhãn (annotation)", "từ khoá `this`"; L01 tách "luồng nền (platform thread)" và "luồng chạy (carrier thread)".
- Pháp lý (L13): bỏ Quyết định 2345/QĐ-NHNN (không có trong `audit/legal/registry.yaml`); dẫn TT 50/2024/TT-NHNN **sửa đổi bởi TT 77/2025/TT-NHNN (hiệu lực 01/3/2026)**, nguồn registry (Công báo 1279+1280; bản hợp nhất 25/VBHN-NHNN). `interview_gen_tables.py` / `interview_sync_video.py` KHÔNG chạy: người điều phối chạy sau dựng (tài liệu phỏng vấn có thể còn nhắc QĐ 2345 và "BNK L13").

## Ghi chú cho người điều phối
- File mới/sửa: `audit/bnk/lib.py` (prog, code_block, out_block, add_steps, covers; cảnh practice: step gợi ý thay kết quả mong đợi để khỏi tràn), `audit/bnk/gen.py`, `audit/bnk/src/l00–l14.py`, `audit/bnk/screen_gen.py`, `runprog.py`, `fillout.py`, `frame_of.py`, `af2_gate.py`, `verify_bnk.py`, `labs/BNK/**`, `audit/review/screen_code/BNK.yaml`, `curriculum/bnk.yaml` (sinh lại bằng `gen_curriculum.py`; id, `requires`, `requires_ext: JVA:L12` giữ nguyên — lộ trình mới FND → JVA → JV2 → BNK có thể cần thêm `JV2:<bài cuối>` vào `requires_ext`, việc của người điều phối), `lessons/bnk/*.yaml` (sinh bằng `gen.py`).
- Sổ `BNK.yaml` do `screen_gen.py` ghi đè toàn bộ mỗi lần chạy (mục tay còn khớp sha được giữ: 1 mục L09). Đừng chạy `screen_code.py gen-jva` lẫn với BNK (nó chỉ ghi JVA.yaml).
- Nội dung lời đọc: không dùng tên "Python", "sqlite", "curl" trong `say` (chỉ hiện trên màn hình; lời đọc dùng tiếng Việt, theo `lexicon_vi.BNK.yaml`). Chưa dò ASR bằng `probe_terms.py` (không chạy `asr`).
- Chưa làm (ngoài khả năng không dựng): nghe thử giọng đọc; mở 3 khung PNG cho đủ từng bài (đã mở: L00 ×3, L03, L05, L07, L09, L11, L13; mọi bài `render` 0 vấn đề).
