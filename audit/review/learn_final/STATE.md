# STATE đợt LF2 (cập nhật liên tục; phiên khác đọc tệp này + plan_LF2_*.md + findings_LF2.md là đủ làm tiếp)

Cập nhật: 2026-11-11 ≈ 06:50Z.

## Sổ tác tử (cập nhật sau lần ngắt hạn mức thứ hai; tiếp tục bằng SendMessage tới id, KHÔNG mở tác tử mới cho cùng việc)
Hạn mức 5 giờ đã cạn hai lần vì chạy 12–16 tác tử cùng lúc. Từ nay: tối đa 4 tác tử cùng lúc; ưu tiên áp sửa → bài CV → đọc lô mới.
| Việc | id tác tử | Trạng thái |
|---|---|---|
| B01 đọc + áp sửa | a07b12d79109adae0 | đọc xong; áp sửa bị ngắt giữa chừng (CSA L01, L03, L07, L11 đã đổi) |
| B02 | ab5cf31d64d00c5c9 | đọc xong; ÁP XONG (CSA L13, L14, L16; OSY L00, L03, L04) |
| B03 | a4a191f39baa92994 | đọc xong; áp sửa bị ngắt (OSY L14, L15 đã đổi) |
| B04+B05 | aca9c7d9c412d148c | đọc xong; áp sửa bị ngắt (NET L14, L15 đã đổi) |
| B06 | a63a070a835835e24 | đọc xong; ÁP XONG (TOC L02, L03; PLC L02, L07). Sổ screen_code PLC L07 sym step 0 cần cập nhật (`list(map(...))`) |
| B07 | ae2bd2c828a87e72a | đọc xong; áp sửa bị ngắt |
| B08 | aa9cc5bb3b1ba9a65 | đọc xong; áp sửa bị ngắt |
| B09 | a4b5cc64b189590f9 | đọc 11/13 (thiếu DBS L04, L05); đã nhắn đọc nốt rồi áp; bị ngắt |
| B10 | a66df228cee95c163 | đọc 3/11 (DBS L06–L08); đã nhắn đọc nốt DBS L09–L16; bị ngắt |
| B11 | a431ba0bf1c1c22b9 | đọc xong; áp sửa bị ngắt |
| B12 | a956216ec4e88939e | đọc xong; áp sửa bị ngắt |
| B13 | a7d6d8632919b2a05 | đọc xong; ÁP XONG (DVO L01; CLD L01, L02) |
| B14 | af1b3e827c5f902ba | đọc xong; áp sửa bị ngắt |
| B15 | af453cc38858c9b48 | đọc xong; ÁP XONG (WEB L15; thêm [R14] RFC 7230 vào audit/web/sources_L15.md; cân nhắc thêm 7230 vào `fix` của curriculum/web.yaml L15) |
| B16 | add51bfc894745214 | đọc xong; ÁP XONG (SEC L10) |
| Soạn BNX L16 | a137b67bec546e012 | bị ngắt |
| Soạn BNX L18 | a186e82694cb00201 | bị ngắt |
| Soạn BNX L19 | a4484e81648abda64 | bị ngắt |
| Soạn BNX L21 | ad508d04454a1165f | bị ngắt |
Chưa giao: lô B17–B48; bài BNX L17, L20, L22, L23 (giáo án đã có trong curriculum/bnx.yaml, brief `audit/bnx/BRIEF_CV.md`).
Lời nhắn áp sửa: "đọc và làm đúng audit/review/learn_final/BRIEF_APPLY.md". Lời nhắn đọc: xem BRIEF_FINAL.md (báo cáo đầy đủ trong tin nhắn văn bản + `date -u`, câu trả lời cuối gọn); trích báo cáo bằng `save_reports.py <tasks> Bxx=<id>`.
Báo cáo đã lưu: reports/B01, B02, B03, B04, B06, B07, B08, B11, B12, B13, B14, B15, B16 (B09, B10 chưa đủ lô nên chưa lưu).

## Sửa và dựng lại
- Ảnh chụp trước khi sửa: scratchpad phiên `…/scratchpad/snap/lessons`, `snap/curriculum`. `changed.py <snap/lessons> [--queue Bxx…]` liệt kê bài đã đổi và đưa bài của lô ĐÃ ÁP XONG vào `rebuild.queue`.
- Hàng dựng: `bash audit/review/learn_final/rebuild_lf2.sh a|b` (đọc `rebuild.queue`, ghi `rebuild.done`, log `logs/rebuild.<luồng>.out`, dừng bằng `rebuild.stop`). Luồng ghi `.done` cả khi FAIL → luôn grep "FAIL" trong log.
- Đã sửa tay theo văn bản gốc: BNX L12 (`audit/bnx/src/l12.py`, hạn mức ví), BNK L13 (`audit/bnk/src/l13.py`, TT 50/2024); cả hai gen + lint 0/0. BNK L13 đổi → sau khi dựng phải `interview_sync_video.py` (bản sao video phỏng vấn) và `interview_gen_tables.py`.
- Chưa làm: `audit/bnx/sources.md` (đổi [TT40], [TT41], [TT64], [TT19] từ "thứ cấp" sang nguồn gốc, số liệu ở cuối findings_LF2.md); MASTER Mục 7 dòng 3, 10; interview/04, 06; verify_bnx L12 và screen_code sau khi gen lại; sau mỗi đợt dựng: rà ASR (HAND), `pack.py preview`.
- Cổng trước khi sửa: `logs/gates_pre.out` sạch toàn bộ (07:34Z).

## Yêu cầu người dùng (hai tin nhắn trong phiên)
1. Rà kỹ, kiểm bằng chứng, xử lý contract bottleneck, đánh giá kho đã đủ chuẩn xác để học chưa, chốt phiên bản, viết bàn giao; lộ trình 0 → senior/chuyên gia theo `interview/MASTER_CURRICULUM_INDEX.md` và `HOC_TAP.html`.
2. Bổ sung: phần liên quan JD **không chỉ theo JD mà còn theo CV**; mọi thứ ghi trên CV phải có bài dạy đủ để bị hỏi là trả lời được.

## Đã làm
- Cổng cuối trước khi sửa: `bash audit/review/learn_full/final_gates.sh > audit/review/learn_final/logs/gates_pre.out` (chạy nền; lúc ghi tệp này đã qua tới check_meta, tất cả sạch; **không sửa bài nào trước khi cổng này chạy xong**).
- Chia 537 bài chặng 6–11 thành 48 lô: `batches.py` → `batches.json`. Brief người đọc: `BRIEF_FINAL.md`.
- Đợt đọc 1 XONG: B01, B02, B03, B04+B05, B06, B07, B08 = 88 bài. Báo cáo nguyên văn: `reports/Bxx.md` (trích bằng `save_reports.py` từ nhật ký tác vụ; người đọc phụ KHÔNG ghi được tệp, đừng yêu cầu họ ghi hay gửi lại báo cáo). Tổng: MUST 3 (OSY L14 hiển thị, CSA L11 lời đọc "8 nghìn byte", SDP L05 `QuyTac()` không chạy), còn lại BLOCK-TERM và SHOULD.
- Đợt đọc 2 ĐANG CHẠY: B09–B16 (8 người đọc nền).
- Pháp lý: đã đối chiếu văn bản gốc TT 40/2024 (VBHN 76), TT 31/2024, TT 50/2024, TT 64/2024, TT 19/2021. Kết quả và việc phải sửa: bảng cuối `findings_LF2.md`.
- Độ phủ CV: `cv_scan.py` → `logs/cv_scan.out`.

## Việc tiếp theo (theo thứ tự)
1. Chờ `gates_pre.out` xong, đọc từng dòng tổng.
2. Sửa theo `reports/Bxx.md`: mọi MUST; BLOCK và SHOULD có tin cậy CONFIRMED; PLAUSIBLE chỉ khi kiểm lại được. Cách đã dùng tốt ở các đợt trước: gọi lại chính người đọc (SendMessage) để tự áp phát hiện của mình rồi chạy `lv.py lint`; người điều phối kiểm diff, đồng bộ mẫu `.tpl` (`sync_tpl_from_lesson.py --write`), sổ `screen_code`, `asr_reviewed`.
3. Sửa pháp lý: BNX L12 (`audit/bnx/src/l12.py` → gen), BNK L13 (`audit/bnk/src/l13.py` → gen), `audit/bnx/sources.md`, MASTER Mục 7 dòng 3 và 10, interview/04, 06.
4. Giao tiếp các lô B17–B48 (mỗi đợt 8 người đọc). Lời nhắn mẫu: xem lời nhắn của B09 trong lịch sử; chỉ đổi id lô và thư mục scratchpad `…/scratchpad/lf2/Bxx`.
5. Khoá bổ sung theo CV (mục dưới).
6. Dựng lại mọi bài đã đổi (hàng dựng: `audit/review/learn_start/rebuild_ls1.sh` là mẫu), rà ASR, `pack.py preview`, cổng cuối → `logs/gates_post.out`, `pack.py check --decode` cả kho.
7. Bàn giao: `handover_LF2_<ts>.md`, `knowledge-graph_LF2_<ts>.md`, đầu `HANDOVER.md`, bộ nhớ `production-progress.md`.

## Khoảng trống CV đã xác nhận bằng quét chữ + từ đồng nghĩa (chưa bài nào dạy)
ForkJoinPool, CompletableFuture (ExecutorService chỉ có ở INT L01) · Spring Security, Spring Cloud (gateway, cấu hình tập trung, Consul) · JUnit 5, Mockito · Redis Cluster (16384 khe băm), danh sách đen JWT trong Redis, khử trùng `transId` TTL 60 s · Go và Fiber như một ngôn ngữ (chỉ ACB L04 nhắc) · AEM (OSGi, Sling, HTL, JCR) · Scikit-Learn (fit/predict; ONNX chỉ có ở INT L05) · LOS/LMS, chấm điểm tín dụng, thẩm định, ECM, dấu vân tay thiết bị, 2FA · trường đa trị của T24.
Hướng xử lý: thêm bài vào khoá BNX (L16 trở đi), cùng quy trình `audit/bnx/BRIEF.md` (src → gen → lint → render → verify → screen_code), mã chạy thật khi máy có công cụ (JDK 22, Go, Docker, Python).

## Cập nhật ≈ 13:2xZ (2026-11-11)
- ÁP XONG thêm: B01, B03, B04+B05, B07, B08, B11, B12, B14 (đã vào rebuild.queue). Còn dở: B09 (đọc nốt DBS L04, L05 rồi áp), B10 (đọc nốt DBS L09–L16).
- Mục "ĐỂ LẠI" của người đọc (PLAUSIBLE, cần nguồn ngoài): OSY L15 cgroup v2; NET L12 "bộ đệm" DNS; NET L14 ổ khoá Chrome; SWF L01 hình đô-mi-nô; SWF L13 "chạy sạch/dựng/luật dựng"; SDP L08 "thể hiện"; SWF L12 "bộ đệm"; CSA L16 "trình cắm"; PLC L01 bảng TEN/KHOA; DVO L13 chặng 5; SAR L00 kịch bản sáu phần; DBS L17 MySQL 64 phiên bản.
- Giáo án đã đổi theo bài: curriculum/web.yaml L02 objectives; curriculum/dsy.yaml L00 example (150 mili giây). CLD L10 có mẫu audit/cld/src/L10_hang_doi.tpl.yaml (đã sửa cùng).
- CV: BNX L16 XONG 5 cổng; L18 XONG 5 cổng (jar ở audit/bnx/deps/l18, có thể bị gitignore); L21 soạn xong, đang render lại với tiêu đề rút gọn; L19 (a4484e81648abda64), L17 (aa6d514bc2f1eacd1), L20 (a9339390c18c6985d) đang soạn. Chưa giao: L22, L23.
- Tiêu đề L17, L19, L21 trong curriculum/bnx.yaml đã rút gọn (tiêu đề > ~80 ký tự làm dòng đầu trang xuống 2 dòng).
- Việc người điều phối sau khi các bài CV xong: `audit/bnx/screen_try.py --merge` (gộp sổ), gộp audit/bnx/sources_lNN.md vào sources.md, thêm `rec("BNX:L16…L23")` vào audit/verify_plan_curricula.py, đổi `spec_planned` → `spec` trong curriculum/bnx.yaml, giao 2 người đọc độc lập 8 bài mới (BRIEF_READ.md của bnx), rồi dựng.
- 13:27:43Z: BNX L19, L21 XONG 5 cổng. L23 đang soạn (ae8b7c37ceb3c581c), L22 (a168a5b97780a0be8). 40 bài FAIL lúc 20:03–20:04 giờ máy do tên trùng bnx_fee ở checklib_bnx/l18.py (đã hết) → đã đưa lại vào hàng.

## 2026-11-11T18:50Z — ĐỌC TRƯỚC: plan_LF2_20261111T1800Z.md và handover_LF2_20261111T1800Z.md thay cho mọi mục "Việc tiếp theo" phía trên. Hai luồng dựng đã dừng (rebuild.stop còn đó). Cổng giữa đợt: logs/gates_mid.out, gates_mid_detail.out, audit_all_mid.out.

## 2026-11-12T01:3xZ — phiên tiếp (agent cũ KHÔNG khôi phục được: "No transcript found"; mở agent mới)
Sổ tác tử mới (≤ 4 cùng lúc). Báo cáo đọc lấy từ tin nhắn của người đọc rồi `save_reports.py <thư mục tasks> Bxx=<id>`.
| Việc | id | Trạng thái |
|---|---|---|
| BNX L17 | aac01e1dbc1fe7147 | XONG 5 cổng (lint 0/0, render 169 khung 0, verify 28/28, screen_try 24 khối PASS); tab `\text` đã sửa; cần gộp sổ screen/l17.yaml + sources_l17.md |
| BNX L22 | aed4039320e35bd9a | đang soạn |
| BNX L20 | af093f52affaf048c | đang soạn |
| BNX L23 | acacc5ef177dfde9d | đang soạn |
| B09 đọc lại đủ 13 bài | a92e3e5ccfb27b850 | đang đọc (báo cáo cũ mất; có MUST SDP L11/L17 chưa áp) |
Đã làm bởi người điều phối: BNX L14/L15 hết câu "bài cuối của khoá" (gen+lint 0/0, cần dựng lại L14, L15); VER DSY:L00; HAND CLD L01 (asr_flags CLD = 0); BNK L13 thêm TT 77/2025 trên màn hình (cần dựng lại + interview_sync_video). Pháp lý TT 77: findings_LF2.md mục cuối.

## 2026-11-12T02:1xZ — cập nhật sổ
- XONG soạn 8/8 bài CV (L16–L23; L20 verify 25/25, L22 24/24, L23 35/35 PASS); curriculum/bnx.yaml: spec cho L16–L23 (L22 tiêu đề rút gọn; L23 tiêu đề/mục tiêu/example theo bài: 11 nhãn −1 chứ không 10); verify_plan_curricula 570 PASS 0 FAIL (rec BNX:L16–L23 + DSY:L00); check_meta 0; check_curricula_graph 0.
- B09 ĐÃ SỬA (SDP L11, L17; DBS L03, L05) → dựng lại PASS L17, L03, L05 (xem rebuild.a.out). B10 ĐÃ SỬA (DBS L06, L08, L09, L10, L12, L13, L16) → đã vào rebuild.queue.
- Người đọc BNX: L16–L18 (ac5a93b5074b67417) đọc xong, MUST F1 (commonPool điều kiện), F2 (orTimeout không nhả luồng), F3 (đối số ThreadPoolExecutor chưa dạy), F10 (L17 Consul/LoadBalancer: lọc bản trượt chỉ khi bật query-passing hoặc health-check; mặc định không) → đang áp sửa. L19–L22 (ae06e901e4a555863) đang đọc. L23 (ae86b8effccf27e62) đang đọc.
- Còn: gộp sổ screen BNX (`screen_try.py --merge`) + gộp sources_lNN vào sources.md (CHỈ chạy khi không ai dùng docker bnx-ora; 5 khối L07 từng FAIL ORA-24001 do chạy chồng); dựng BNX L16–L23 sau khi đọc+sửa xong; B17–B48 chưa giao.

## 2026-11-12T02:5xZ — cập nhật sổ (giữa phiên)
- BNX L16–L23: soạn + đọc độc lập + sửa XONG; verify_bnx L16 23/23, L17 29/29, L18 20/20, L19 29/29, L20 25/25, L21 24/24, L22 25/25, L23 38/38 PASS; sổ screen BNX đã gộp (331 khối, PASS 360, 0 FAIL/STALE/MISSING/ORPHAN); sources_l16–23 đã gộp vào audit/bnx/sources.md; curriculum/bnx.yaml `spec` cho L16–L23; verify_plan_curricula 570/0; check_meta 0. BNX L16–L23 + L14 + L15 đã vào rebuild.queue (cần docker bnx-ora/bnx-mss chạy).
- Bẫy Oracle: lần chạy chồng làm bảng hàng đợi BNX_L07_QT ở trạng thái INVALID; AQ_CLEAN nuốt lỗi (WHEN OTHERS NULL) nên L07 FAIL 5 mục. Sửa: `DBMS_AQADM.DROP_QUEUE_TABLE(queue_table=>'bnx_l07_qt', force=>TRUE)` (script logs/aqclean.py). Đừng chạy hai verify BNX Oracle cùng lúc.
- Đọc độc lập đã đủ lô: B01–B08, B09, B10, B11–B16, B17, B18, B19, B20, B21 (đã áp B09–B20; B21 đang áp 2 SHOULD). Đang đọc: B22 (ad96fbd0c8f6c0311), B23 (a17e460fe21f3aefd), B24 (aab7a397ffb087e72). Chưa giao: B25–B48.
- Hàng dựng: 2 luồng a, b (`rebuild_lf2.sh`), log logs/rebuild.{a,b}.out; luôn grep "FAIL sau"; DBS L16 từng FAIL (tràn khung → thêm `clear: true`, đã dựng lại).

## 2026-11-12T03:3xZ — TTS Edge bị chặn (NoAudioReceived) khi 4 luồng dựng chạy song song bài BNX mới
- Đã dừng cả 4 luồng (taskkill /T), gỡ claims BNX_L16..L19 để dựng lại sau. Hàng dựng còn ~70 bài (rebuild.queue − rebuild.done). Làm tiếp: chờ ≥ 1 giờ (quy tắc quota-wait-hourly), thử MỘT luồng `bash audit/review/learn_final/rebuild_lf2.sh a` (nền, không timeout); nếu NoAudioReceived còn → chờ tiếp. Bài đã có cache giọng dựng nhanh; bài BNX L16–L23 có nhiều câu mới nên dựng sau cùng hoặc dựng riêng từng bài.
- Đọc/áp sửa vẫn tiếp tục (không cần TTS): đã áp B01–B33; B34–B37 đang đọc/áp.

## 2026-11-12T06:1xZ — sau lần chạm hạn mức thứ hai của phiên (TTS đã trở lại, đã chạy 2 luồng dựng a, b)
- Đọc độc lập xong + áp sửa: B01–B44 (reports/Bxx.md đủ). Đang áp: B45 (a8e8cc2a83bdeceb7), B46 (a997c878e10d47fa7). Đang đọc: B47 (ace7f48ed15c0f626, từng bị 429), B48 (ae2f77dd26e709eb0). Khi xong B45–B48 là đủ 537/537.
- Hàng dựng: `rebuild.queue` − `rebuild.done` còn ~125 dòng (gồm BNX L16–L23, L14, L15). Chạy `bash audit/review/learn_final/rebuild_lf2.sh a|b` (nền). Nếu TTS lại NoAudioReceived: dừng (rebuild.stop hoặc taskkill /T), thử `logs/tts_probe.py`, chờ ≥ 1 giờ; CHỈ 2 luồng song song.
- Còn lại sau dựng: grep "FAIL sau" logs/rebuild.*.out (DBS L16 từng FAIL tràn khung → đã sửa); rà ASR (asr_flags từng khoá); pack.py preview/check; audit_all (không tham số); sync_tpl --all; interview_sync_video (BNK L13); final_gates.sh; handover_LF2_<ts>.md; HOC_TAP/MASTER (BNX L16–L23 + đối chiếu CV); cập nhật HANDOVER.md đầu và bộ nhớ.
- Ghi nhận hệ thống: lời hẹn "Bài sau (bài N)" theo số bài trong khoá khác thứ tự học thật (batches.json) — KHÔNG sửa hàng loạt (sẽ buộc dựng lại hàng trăm video); đã sửa riêng CLC L11 (L12 học trước L11).
2026-11-12T09:53:23Z BNX L16–L23 dựng xong (PASS). Thêm luồng c, d (4 luồng).
2026-11-12T13:52:42Z HÀNG DỰNG RỖNG: 226/226 bài PASS, 0 FAIL tồn. Chuyển sang rà ASR + cổng.
2026-11-12T13:56:01Z ASR: BNX L16–L23 + AIF L14 + BCH L03 + RBM L04 HAND ghi xong, asr_flags 0; tts_speed_scan BNX 0 câu cụt; sync_tpl 0 lệch.
2026-11-12T14:11:55Z BNK L13 dựng lại PASS; pack check 680/0 vấn đề; HOC_TAP.html 680 bài 0 liên kết chết; interview_sync_video 92/92.
2026-11-12T14:14:47Z MASTER: LF blocks regenerated (680 bài, BNX 24 bài 365,36 phút), mermaid/đường tối thiểu/Mục 2A/ma trận CV hàng 3,4/Mục 8 thêm 9 dòng CV.
2026-11-12T14:58:13Z audit_all 680/680 0 vấn đề; final_gates.sh chạy nền → logs/gates_post.out
2026-11-12T16:19:59Z final_gates.sh XONG sạch (logs/gates_post.out). Đang giải mã ffmpeg các khoá dựng lại ngoài BNX → logs/check_decode_post.out
2026-11-12T16:23:01Z Đã viết handover_LF2_20261112T1620Z.md, knowledge-graph_LF2_…, report_LF2.md; cập nhật HANDOVER.md đầu và bộ nhớ.
2026-11-12T17:45:30Z Giải mã ffmpeg 575 bài (37 khoá dựng lại): 0 vấn đề, 5219,4 phút. Ghi vào handover §2 và knowledge-graph LF2-18.
