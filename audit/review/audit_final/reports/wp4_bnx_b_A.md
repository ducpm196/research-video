# WP4 BNX-B nhánh A — nâng BNX L16–L19 lên chuẩn AF2 (2026-11-14)

## Tiến độ
- L16, L17, L18, L19: nguồn viết lại (lib2 + prog + labkit), lab đủ `de.md` + `mong_doi.txt` + `loi_giai.*`, cảnh `quymo` + `practice`, `af2: true` + `covers`. Cổng cuối: xem mục "Cổng" bên dưới.

## Việc đã làm cho mỗi bài
| bài | lời đọc (từ) | lab | cảnh quy mô (số đo thật) | covers |
|---|---|---|---|---|
| L16 Đa luồng Java | 2 282 | `labs/BNX/L16` (Java: bể 3 luồng + hàng 5 chỗ, 14 việc → nhận 8/từ chối 6; 5 lượt; 32 việc lá) | `HangQuyMo.java` chạy thật: hàng không giới hạn giữ 6 / 996 / 99 996 việc ở 10 / 1 000 / 100 000 việc (×1, ×100, ×10 000), hàng 2 chỗ từ chối 4 / 994 / 99 994; chờ tính từ số đo (200 ms; 25 s; 42 phút, 100 ms mỗi việc: số minh hoạ) | 1 practice, 2 example, 3 example, 4 formula |
| L17 Spring Security + Cloud | 2 076 | `labs/BNX/L17` (Python: bảng quyết định 401/403 cho `/chuyen-tien`, 250 yêu cầu chia cho 3 bản khoẻ trong 4) | `CuaSoLoi.java` (MÔ PHỎNG, ghi rõ): bản chết còn 45 giây trong danh sách: 1 500 / 150 000 / 15 000 000 yêu cầu lỗi ở 100 / 10 000 / 1 000 000 yêu cầu mỗi giây | 1 example, 2 formula, 3 formula, 4 practice |
| L18 JUnit + Mockito | 2 295 | `labs/BNX/L18` (Java thuần, không jar: ca kiểm tự viết, cổng giả đếm lời gọi, `Clock.fixed`) | `BoCa.java`: bảng phí k = 2 / 200 / 2 000 mốc, bộ ca giữa khoảng (k + 1 ca) bỏ lọt k lỗi nhầm dấu, bộ ca sát mốc (2k + 1 ca) bỏ lọt 0; thời gian chạy suy ra (số minh hoạ) | 1 practice, 2 example, 3 example, 4 pitfalls |
| L19 Redis nâng cao | 2 296 | `labs/BNX/L19` (Python: khe/nút cụm 4 nút, khử trùng hạn 90 s, danh sách đen) | `PhanBo.py`: 3 000 và 300 000 khoá chia cho 3 nút (994/994/1 012; 100 008/99 949/100 043), thẻ băm chung dồn về một nút; số mục khử trùng sống cùng lúc = tốc độ × 60 s (mô hình, 6 000 / 600 000 / 60 000 000) | 1 example, 2 formula, 3 practice, 4 example |

Chung: lời đọc cắt từ 3 214–4 034 từ xuống ≤ 2 300 (bỏ ví dụ thừa, gộp step, bỏ các bảng "câu hỏi tiếp theo hay gặp" ở recap L16–L19 và cảnh "mô phỏng đồng hồ giả" của L19). Sổ mã: `audit/bnx/screen_keep.py` (mới) giữ mục viết tay theo sha và khoá `of`/`prelude_keys`/`files`.

## Cổng (số thật, máy tải 100% CPU nên ghi cả lần chạy lại)
| cổng | L16 | L17 | L18 | L19 |
|---|---|---|---|---|
| `lv.py lint` | 0 FAIL 0 WARN 71 PASS | 0/0, 71 PASS | 0/0, 54 PASS | 0/0, 76 PASS |
| `lv.py render` | 0 vấn đề (119 khung) | 0 (103) | 0 (117) | 0 (112) |
| `screen_fast.py` | 35 PASS | 33 PASS | 23 PASS | 20 PASS |
| `verify_bnx.py` | 31/31 PASS | 34/34 PASS | 26/26 PASS | 37/37 PASS (có Redis thật trong Docker) |
| lời đọc (từ) | 2 299 | 2 076 | 2 295 | 2 296 |

Cổng chung: `lab_gate.py BNX` 37 PASS · 0 FAIL; `lv.py curriculum curriculum/bnx.yaml` 37 bài, 0 lỗi; `check_curricula_graph.py` BNX 0 tham chiếu hỏng (dòng 2 báo `WEB:L04` FAIL: không thuộc phạm vi); `tests/test_e52.py` 0 FAIL; `check_next_refs.py` 551 lời hẹn, 0 lệch; `arith_scan.py` 240 phép, 0 FAIL; `check_xref.py` BNX 14 lượt đều ở L33 (`WEB-INF`) và curriculum L33, không ở L16–L19; `check_course_refs.py` chỉ báo R4 ở BNX L00 (không thuộc phạm vi); `check_meta.py` 1 vấn đề ở khoá khác.

## Mục đã thay đổi ngoài bài (đều là Edit nhỏ)
- `audit/bnx/screen_keep.py`: thêm remap khoá cho trường `files` (sổ cũ ghim các tệp theo khoá khối: thiếu remap thì `example 9 0` của L18 trỏ tới khối không tồn tại).
- `tools/registry/symbols.BNX.yaml`: mục `# ── L16–L19 ──` thêm 6 thuật ngữ (`bnx_forkjoin`, `bnx_consul`, `bnx_junit`, `bnx_mockito`, `bnx_khe_bam`, `bnx_the_bam`), `introduces` đúng step giảng. Không đăng ký "bể luồng", "CompletableFuture", "hàng đợi", "đối tượng giả", "Spring Cloud" vì L33/L20/L23/L36 hoặc cảnh forward_ref dùng.
- `tools/checklib_bnx/l16.py, l18.py, l19.py`: hàm `bnx_l16_backlog/rejected/last_start_ms`, `bnx_l18_cases_mid/edge/survivors_*/suite_ms`, `bnx_l19_node_counts/live_dedup`.
- `audit/bnx/ver/l16,l17,l18,l19.py`: thêm chạy lại chương trình cảnh quy mô (`lib2.find(...).execute()`), mô phỏng/đếm lại bằng đường khác, lab qua `labs/cham.sh`; L19 thêm nạp 3 000 khoá vào cụm Redis thật so `DBSIZE` từng nút (994/994/1 012 và 0/0/3 000).
- Không sửa `curriculum/bnx.yaml` (mục tiêu giữ nguyên chữ, `covers` trỏ đủ).

## Điều không làm / hạn chế (đã biết)
1. **Mã Spring ở L17 chỉ hiện từng đoạn** (CauHinh.java 46 dòng + ChayThu.java 53 dòng; ≥ 9 khung nếu hiện đủ không vừa 2 300 từ): người học không gõ lại nguyên tệp từ màn hình được (đoạn import không hiện). Đề xuất **tách L17 thành hai bài**: "Spring Security: chuỗi bộ lọc, 401/403, máy chủ tài nguyên" (hiện đủ mã) và "Spring Cloud: cổng, sổ đăng ký, cấu hình tập trung, bản chết còn trong danh sách". Chưa tự tách (không đánh số lại).
2. L19 cũng ở sát trần (cụm + khoá + khử trùng + danh sách đen + 4 lỗi): nếu cần thêm nội dung thì tách "cụm 16384 khe" khỏi "khoá/khử trùng/danh sách đen". Đã bỏ khỏi video: bảng "câu hỏi tiếp theo hay gặp" ở recap L16–L19, mô phỏng đồng hồ giả (`PY_SIM`, giữ trong bộ kiểm; phần "giây 30/61" nay chứng minh bằng Redis thật hạn 2 giây ở cảnh check), `orTimeout`/`CompletionException` của L16 (giữ ở bộ kiểm).
3. Mã dài ở L16/L18/L19 hiện **trọn vẹn nhiều khung liên tiếp** (L16 mọi chương trình từ dòng 1; L18 mọi tệp; L19 hiện từng đoạn của lệnh bash/Docker như cũ).
4. **Đồng hồ thật**: `GhepLoiGoi` và `DungChung` (L16) dùng `Thread.sleep`; lúc máy tải 100% CPU lệch thứ tự ~30% lần (đo 10 lần). Đã sửa cho bền: chốt xuất phát chung và phóng thời gian ×4 (`K`, đo chia lại K); sau sửa 12/12 lần chạy giống ở cùng điều kiện tải. Vẫn nên chạy cổng khi máy nhàn.
5. Cảnh quy mô: số "đo thật" là số đếm tất định (hàng đợi, số ca, số khoá); thời gian (25 giây, 42 phút, 40 giây, 2 giờ, 6 000/600 000/60 000 000 mục) tính từ số đo với tham số "(số minh hoạ)"; L17 `CuaSoLoi` là mô phỏng Java thuần (ghi rõ "MÔ PHỎNG" trên màn hình và trong lời), không phải Spring Cloud thật. Dòng 1 triệu yêu cầu/giây của L19 và 30 000 000 khoá ghi "(mô hình, chưa đo)".
6. P1 dự kiến: L16 = 2, L18 = 2, L19 = 2 (CRC16, mod, thẻ băm, hạn sống giảng tại chỗ; `jti`, `exp` chỉ ở bảng prereq), L17 = 1–2 (nhiều tên Spring; `iss/exp/nbf/aud`, "nhãn" giảng ngắn).
