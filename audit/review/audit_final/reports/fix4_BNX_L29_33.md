# fix4 BNX L29–L33 (tác tử con nhóm B, 2026-11-15)

## Tiến độ
- Xong 5/5 bài: L29, L30, L31, L32, L33. Sửa NGUỒN `audit/bnx/src/l29..l33.py`, chạy `gen.py` từng bài (không sửa tay YAML).
- **Cả 5 bài đều đổi nội dung (lời đọc + màn hình) nên CẦN DỰNG LẠI** (tts, asr, render, build). Khung PNG `out/BNX/Lxx/frames` đã dựng lại bằng `lv.py render` (chỉ để xem; mp4/srt cũ).

## Số liệu cổng (đo thật 2026-11-15)
| Bài | lint | từ lời đọc (lint) | render | verify_bnx | screen_fast |
|---|---|---|---|---|---|
| L29 | 0 FAIL 0 WARN | 2294 | 110 khung, 0 vấn đề | 24/24 PASS (+1 kiểm mới: trigger bị lách) | 24 PASS, FAIL/STALE/MISSING/ORPHAN 0 |
| L30 | 0/0 | 2285 | 114 khung, 0 | 22/22 PASS (+2 kiểm mới) | 26 PASS, 0 |
| L31 | 0/0 | 2297 | 117 khung, 0 | 21/21 PASS (+1; chạy lại Prometheus 3.16.0 thật bằng docker qua trình chạy của bài) | 32 PASS, 0 |
| L32 | 0/0 | 2287 | 124 khung, 0 | 19/19 PASS (+1; Vault 2.2.2 thật) | 22 PASS, 0 |
| L33 | 0/0 | 2292 | 124 khung, 0 | 15/15 PASS (+1; Tomcat 10.1.61 thật) | 26 PASS, 0 |
- Cổng chung (chạy sau khi xong 5 bài; các nhóm A, C có thể đang sửa song song): `tests/test_e52.py` 0 FAIL; `arith_scan.py BNX` 58 phép tính, 0 FAIL; `check_course_refs.py BNX` 0 vấn đề; `check_next_refs.py` 550 lời hẹn, 0 lệch; `lv.py curriculum curriculum/bnx.yaml` (chạy lại sau mọi sửa) 39 bài, 39 có đặc tả, 0 lỗi; `lab_gate.py BNX` 39 PASS · 0 FAIL (196 lab).
- Mỗi bài: `say` mới đều 4–38 từ, không chữ Latin/Anh (lint WARN “không phải âm tiết tiếng Việt” đã xử lý: đổi lời đọc, không thêm lexicon).

## MUST (L30: 2/2 đã sửa)
- **L30 "bốn nghìn" → "bốn trăm"**: tiêu đề cảnh hook (và `chapters.txt` sinh từ tiêu đề). Đã quét `audit/bnx/src/l30.py` và YAML sinh: không còn "bốn nghìn" ở đâu khác (thân bài đã đúng 400 và 40 000). `ver/l30.py` có kiểm "tiêu đề không còn 'bốn nghìn'".
- **L30 example step 3 lời đọc**: nay đúng nhật ký: ba cuộc đầu hỏng nên mở ở 1000; cuộc ở 1500 bị chặn; ở 2000 cho thử một cuộc, vẫn hỏng nên mở lại, cuộc ở 2500 lại bị chặn; ở 3000 thử tốt nên đóng; tổng bảy gọi thật, hai bị chặn. `ver/l30.py` dựng bảng chuyển trạng thái độc lập và kiểm 1500 chặn / 2000 hỏng→MO / 2500 chặn / 3000 tốt→DONG, lời đọc khớp, "hai cuộc kế tiếp bị chặn" không còn.

## SHOULD đã sửa (kiểm bằng mã thật)
- L29: trigger "chặn mọi lệnh sửa và xoá" hạ giọng: ghi chú giới hạn và lời đọc nêu `INSERT OR REPLACE` ghi đè sự kiện cùng seq, `DROP TRIGGER`/`DROP TABLE` vẫn chạy (đo trên SQLite 3.49.1: `ver/l29.py` chạy đúng 2 trigger của bài và xác nhận ghi đè 300→900, DROP TABLE xoá bảng); pitfalls#1, example step 2 sửa cùng giọng. Nhãn "theo thứ tự" hình 00016 bị cắt: tách hai dòng "theo" / "thứ tự", khung đã xem. Quiz câu 3: đơn vị "mỗi lần hỏi phát lại hàng nghìn sự kiện, 100 000 khách hỏi mỗi giây".
- L30: CauDao.java hiện đủ hàm ghi (tách 2 step: `choPhep` 7 dòng, `ghi` 10 dòng: nhánh nửa mở, tốt xoá bộ đếm, hỏng `++hong >= NGUONG` rồi MO); hình 00016: mũi tên "thử hỏng/thử tốt" thành đường gấp khúc chạm đúng hộp MO và DONG, nhãn không bị gạch (đã xem khung); mục tiêu #3 đổi thành "So sánh cầu dao tự cài với Resilience4j thật: cùng ba trạng thái, khác cách đếm hỏng" (khớp bài: thư viện mở sau 4 hỏng, tự cài sau 3).
- L31: test.yml hiện đủ (tách `promql_expr_test` 7 dòng, `alert_rule_test` 6 dòng gồm `exp_labels`, ca thứ hai 8 dòng); dòng gán `IMG=prom/prometheus@sha256:…` hiện cùng bảng đọc lệnh `docker run`; Grafana: câu lời đọc "bảng điều khiển vẽ mỗi ô từ một truy vấn" (P7: Grafana vẫn chỉ giảng khái niệm, nói rõ).
- L32: mật khẩu tĩnh vs thẻ: hook, Bước 6, bảng quymo và CV đổi thành "mật khẩu tĩnh vẫn sống sau khi thẻ hết hạn, chỉ bí mật động tự hết hạn"; `s3:Get*` chỉ khớp việc có tên bắt đầu bằng `Get`, không gồm `s3:ListBucket` (kiểm `fnmatch`); ChinhSach.py hiện 9 dòng gồm đường ra `tu choi (mac dinh)`.
- L33: Cu.java hiện 7 dòng (`EOF`, `javac -cp "lib/*"`, `sed -i` đổi `import jakarta.servlet.http.HttpServlet;`) kèm chú thích; "mỗi trang dịch một lần" ghi rõ là mặc định (trang bị sửa thì dịch lại; biên dịch trước thì 0 lần) ở Bước 4, quiz câu 2; pitfall 4 bỏ câu "bản cũ hết hỗ trợ bảo mật" không kiểm được nguồn, thay bằng "nợ nâng cấp tích tụ" và nhắc xem trang phiên bản được hỗ trợ của Tomcat.

## P1 (giảng tại chỗ bằng bảng "viết trong mã / nghĩa / ví dụ nhỏ", đặt ngay trước khối mã đầu tiên dùng cú pháp)
- L29: `VALUES (?, ?, ?)`, `try/except … as e`, `.fetchone()[0]`; `enumerate(…, 1)`, f-string, `reduce(ap_dung, kho, 0)`; `global da_xu_ly`, `while`; hàng `CREATE TRIGGER … BEFORE UPDATE ON … BEGIN … END` ở bảng sym.
- L30: bảng cấu hình Resilience4j (`.slidingWindowType(COUNT_BASED)`, `.minimumNumberOfCalls(4)`, `.failureRateThreshold(50)`, `executeRunnable(() -> { … })`, `try … catch (CallNotPermittedException e)`); "dịch bit" `goc << (lan - 1)` giải nghĩa bit và 100 → 200 → 400.
- L31: SLO (giải nghĩa ở step Tự làm; lời đọc "mục tiêu độ sẵn sàng"); `**them`, `next(gio)`; `docker run --rm -i --entrypoint sh $IMG -c '…'` + `tar cf - … |` + `$IMG` có giá trị; `wget -qO- --post-data … | sed …`, `seq/sleep`; PromQL (hàng `rate(x[5m])` ở sym, "ngôn ngữ truy vấn của hệ thu thập").
- L32: `git("ls-tree","--name-only","HEAD")`, `git("show","HEAD:"+t)`, `t[:-5]`; `global cuoi`, `moi, cuoi = rev != cuoi, rev`; bảng khai báo Argo CD (`kind`, `source`, `destination`, `syncPolicy.automated`); `export VAULT_ADDR… VAULT_TOKEN=root`, `vault server -dev … &`, `for … $(seq …)`; `cat-file --batch` giải nghĩa ở pitfall 3.
- L33: "Tomcat nhúng" (bảng prereq + lời đọc), `new Tomcat()`/`setPort(0)`/`addWebapp`/`start`; `jar --create --file app.war -C war .`, `java -cp "lib/*" May app.war app app/chao …`; `<%@ page contentType=… %>`, `request.getParameter("ten")`, `?ten=An`; "phiên" ở pitfall 2.
- Lưu ý kỹ thuật: ký tự `$` trong ô bảng bị KaTeX coi là công thức (đã gặp ở L31): viết `&#36;` trong ô bảng.
- Điểm P1 dự kiến: tự đánh giá 5/5 bài có thể đạt 2 với chuẩn chặt (mọi mục trong danh sách P1 của báo cáo R2 đã có giảng ở lần xuất hiện đầu, trước khối mã). Rủi ro còn lại: cú pháp rất nền (`for`, `if`, `class`, `new`) vẫn không giảng riêng; người đọc chặt có thể tìm thêm mục mới.
- `introduces/assumes`: không thêm mục sổ `term:`. Chỉ thêm `assumes=["bnx_ma_bam"]` ở L31 (bài L26 đã `introduces`, L31 dùng "ghim bằng băm" trên màn hình) và `assumes=["bnx_sed_i"]` ở L33 (L18 đã `introduces`). Cả hai đều chỉ là mục đã có ở bài đứng trước trong dãy; `lv.py curriculum` không lỗi.

## Quy mô lời đọc
Mọi bài ≤ 2300 từ (2285–2297, đo bằng lint). Đã cắt câu thuật lại, câu lặp bảng, đoạn "của người mới/đã đi làm" ở pitfalls; giữ nguyên số câu có `focus`.

## Việc điều phối cần làm
1. **Giáo án `curriculum/bnx.yaml` L30 `objectives` (mục thứ 3)**: đổi "So sánh cầu dao tự cài với Resilience4j thật trên cùng một kịch bản" thành "So sánh cầu dao tự cài với Resilience4j thật: cùng ba trạng thái, khác cách đếm hỏng" (đồng bộ với `covers`/E51; em không sửa tệp giáo án).
2. Sổ `screen_code`: em đã chạy `screen_keep.py` + `screen_fast.py` cho L29–L33 (sinh lại `audit/bnx/screen/l29..l33.yaml`, mọi khối được khớp lại theo sha/chương trình, FAIL/STALE/MISSING/ORPHAN 0, không sửa tay mục nào). Điều phối gộp vào sổ chung khi gộp các nhóm.
3. ASR/TTS: mọi câu `say` mới/đổi là câu TTS mới; tên cần dò: "ngôn ngữ truy vấn", "bộ chứa", "Tomcat nhúng", "dấu và", "dấu gạch đứng", "mã chốt", "bí mật động", "dịch sang trái". Không có chữ Latin trong lời đọc nên không đòi thêm lexicon.
4. Docker: L31 (Prometheus ghim băm) và L32 (Vault ghim băm) khi chạy `verify_bnx` tự dùng `docker run --rm` ảnh chính thức qua trình chạy chương trình của bài như các vòng trước; em không chạy docker thủ công, không chạm Oracle/SQL Server.

## Không sửa / hạn chế
- L32: khẳng định "mật khẩu tĩnh vẫn sống sau khi thẻ hết hạn" là suy luận từ chính ví dụ (chương trình Vault chỉ đọc bằng thẻ hết hạn, không đọc lại bằng thẻ gốc sau 6 giây); em không đổi chương trình Vault (sẽ đổi đầu ra thật trên màn hình), nên ghi chú rõ đây là logic KV chứ không phải đầu ra đo thêm.
- L33 "bản cũ hết hỗ trợ bảo mật": bỏ khẳng định thay vì tìm nguồn (không có trong `sources_l33.md`).
- L31 P7 (Grafana chỉ giảng): giữ nguyên, nói rõ trên màn hình và lời đọc là chỉ giảng khái niệm.
- L30 "Semaphore" (NOT_VERIFIED trong báo cáo người đọc) không đổi; kiểm lại bằng chạy `ChayTuCai` thật: PASS (vách ngăn 2 chỗ → từ chối 3).
- Khung "ghi, buoc" trong L32 example step 1 hiện hàm dùng nhưng `ghi/buoc` chỉ nằm một phần ở màn hình (không nằm trong danh sách báo cáo; không sửa).

## Tệp đã sửa
`audit/bnx/src/l29.py … l33.py`; `audit/bnx/ver/l29.py, l30.py, l31.py, l32.py, l33.py` (thêm kiểm); `lessons/bnx/L29…L33_*.yaml` (do gen sinh); `labs/BNX/L29…L33` (write_lab ghi lại cùng nội dung); `audit/bnx/screen/l29…l33.yaml` (sinh lại bằng screen_keep); `out/BNX/L29…L33/frames`. Không sửa tệp dùng chung (symbols.BNX.yaml, gen.py, lib*.py, sổ BNX.yaml, curriculum/bnx.yaml).
