# findings_LF2: sổ phát hiện của đợt đọc chốt chặng 6–11 (2026-11-11)

Quy ước cột **Xử lý**: `CHỜ` (chưa kiểm lại) · `SỬA` (người điều phối đã kiểm lại và đã sửa) · `BÁC: <lý do>` · `GHI` (ghi nhận, không sửa ở phiên bản chốt).
Chuỗi cũ / chuỗi mới nguyên văn nằm ở mục chi tiết bên dưới từng lô. Chỉ `show` = không đổi lời đọc (vẫn phải dựng lại video vì khung hình đổi).

## Tiến độ đọc (AC-2)
| Lô | Bài | ĐÃ ĐỌC | MUST | BLOCK | SHOULD |
|---|---|---|---:|---:|---:|
| B03 | OSY L08–L15, NET L00–L02 | 11/11 | 1 | 1 | 1 |
| B06 | TOC L00–L04, L06, L07; PLC L00–L04, L07 | 13/13 | 0 | 4 | 2 |
| B01 | CSA L00–L12 | 13/13 | 1 | 3 | 2 |
| B02 | CSA L13–L16; OSY L00–L07 | 12/12 | 0 | 6 | 3 |
| B07 | PLC L12; SWF L00–L11 | 13/13 | 0 | 2 | 3 |
| B08 | SWF L12, L13; SDP L00–L10 | 13/13 | 1 (SDP L05 `QuyTac()` không chạy; chỉ show) | 7 | 3 |
| B04+B05 | NET L03–L15 | 13/13 | 0 | 5 (4 ở L15, 1 ở L12) | 3 |

Báo cáo nguyên văn từng lô (chuỗi cũ/mới đầy đủ): `audit/review/learn_final/reports/Bxx.md` (chép từ scratchpad `lf2/Bxx/report.md`). Bảng F-0xx dưới đây mới tóm tắt B01, B02, B03, B06, B07; B04 và B08 xem tệp báo cáo.

## Bảng phát hiện
| ID | Bài | Mức | Chỗ | Tóm tắt | Tin cậy | Xử lý |
|---|---|---|---|---|---|---|
| F-001 | OSY L14 | MUST (hiển thị) | quiz · step 1 · show | `\text{rw-r-----}` bị KaTeX gộp gạch thành gạch dài (khung 00065), không đếm được 9 ký tự | CONFIRMED | CHỜ |
| F-002 | OSY L15 | BLOCK-TERM | sym · step 1 · show + say | "tác vụ" dùng suốt bài mà chưa giảng | CONFIRMED | CHỜ |
| F-003 | OSY L15 | SHOULD | stage3 · step 1 · show | 2048/1024 là thang `cpu.shares` cgroup v1; v2 dùng `cpu.weight` 1–10000 mặc định 100 | PLAUSIBLE (cần nguồn) | CHỜ |
| F-004 | TOC L02 | BLOCK-TERM | sym · step 0 · show | chữ tắt "NFA" chưa giải nghĩa | CONFIRMED | CHỜ |
| F-005 | TOC L03 | BLOCK-TERM | pitfalls · step 2 · show | `(.+)\1`: `.`, `+`, `\1` chưa giảng | PLAUSIBLE | CHỜ |
| F-006 | PLC L02 | BLOCK-TERM/QUIZ | example · step 1 · show | "dạng tiền tố" `(* 2 3)` chưa định nghĩa, quiz lại dùng | CONFIRMED | CHỜ |
| F-007 | PLC L07 | BLOCK-TERM | hook · step 0 · show | `nonlocal n` trong mã mở bài chưa giảng | CONFIRMED | CHỜ |
| F-008 | PLC L07 | SHOULD | sym · step 0 · show | `map(...)` → `[2, 4, 6]` sai với Python 3 (trả đối tượng lặp); cần `list(map(...))` | CONFIRMED | CHỜ |
| F-009 | PLC L01 | SHOULD | sym · step 0 · show | bảng xếp TEN trên KHOA, ngược luật "mẫu khai báo trước thắng" dạy ở cảnh sau | PLAUSIBLE | CHỜ |
| F-010 | CSA L11 | MUST | quiz · step 0 · say (dòng 205) + `asr_reviewed` (dòng 27) | lời đọc "8 nghìn byte" trong khi màn hình 8 KiB, lời giải 8192/32 = 256 dòng (8000/32 = 250) | CONFIRMED | CHỜ |
| F-011 | CSA L07 | BLOCK-TERM | hook · step 1 · say + show | "hợp ngữ" (tên bài) chưa định nghĩa | CONFIRMED | CHỜ |
| F-012 | CSA L07 | BLOCK-TERM | example · step 3 · say + show | "tập lệnh" (tên bài) chưa định nghĩa | CONFIRMED | CHỜ |
| F-013 | CSA L03 | BLOCK-STEP | verify · step 0 · say + show | 24 bit độ chính xác so với 23 bit phần định trị: thiếu "số 1 ghép trước" | CONFIRMED | CHỜ |
| F-014 | CSA L03 | SHOULD | compare · step 0 · say + show | ngưỡng tương đối không dùng được khi so với 0 (cần ngưỡng tuyệt đối) | CONFIRMED | CHỜ |
| F-015 | CSA L01 | SHOULD | pitfalls · step 1 · say + show | "cách cắt do trình biên dịch quy định" lỗi thời với C++20 (thu hẹp có dấu = modulo 2^N); C vẫn vậy | CONFIRMED (chuẩn) | CHỜ |
| F-016 | CSA L13 | BLOCK-TERM | hook · step 0 · show + say | "lõi" chưa giảng (đỡ luôn OSY L01, L04) | CONFIRMED | CHỜ |
| F-017 | CSA L16 | BLOCK-TERM | stage2 · step 0 · show + say | "bóng bán dẫn", "định luật Moore" chưa giảng | CONFIRMED | CHỜ |
| F-018 | CSA L16 | BLOCK-TERM | stage2 · step 0 · show + say | "dòng rò" chưa giảng | CONFIRMED | CHỜ |
| F-019 | CSA L16 | BLOCK-TERM | stage5 · step 0 · show + say | "phân tích tĩnh" chưa giảng | CONFIRMED | CHỜ |
| F-020 | CSA L16 | BLOCK-TERM | quiz · step 2 · show + say | "trình cắm", "máy ảo dùng chung" chưa giảng | PLAUSIBLE | CHỜ |
| F-021 | OSY L00 | BLOCK-TERM | example · step 0 · show + say | "chuyển ngữ cảnh" dùng ở mục tiêu, quiz mà không câu nào gọi tên | CONFIRMED | CHỜ |
| F-022 | OSY L03 | SHOULD | sym · step 0 · show + say | thời gian chờ: gán cho bài 2 định nghĩa khác; công thức "bắt đầu − đến" chỉ đúng khi chạy liền mạch | CONFIRMED | CHỜ |
| F-023 | OSY L04 | SHOULD | intuition · step 0 · say | lời đọc "mũi tên đi xuống từ x là đọc" lệch hình (khung 00025: đọc đi lên, ghi đi xuống) | CONFIRMED | CHỜ |
| F-024 | CSA L14 | SHOULD | sym · step 0 · say; quiz · step 0 · say (cả `asr_reviewed`) | "trang 4 nghìn byte" trong khi màn hình 4 KiB = 4096 | PLAUSIBLE | CHỜ |
| F-025 | SWF L00 | BLOCK-TERM | pitfalls · step 2 · show + say | "lệnh khẳng định" chưa giảng | CONFIRMED | CHỜ |
| F-026 | SWF L10 | BLOCK-TERM | hook · step 0 · show + say | "bộ nhớ đệm còn lạnh", "biên dịch khi chạy" chưa giảng | CONFIRMED | CHỜ |
| F-027 | SWF L07 | SHOULD | sym · step 0 · say | lời đọc bất biến cây tìm kiếm thiếu vế nút < phải | CONFIRMED | CHỜ |
| F-028 | SWF L09 | SHOULD | recap · step 0 · show + say | "dữ liệu chung + có ghi = tranh chấp" tuyệt đối sai (thiếu "không khoá") | CONFIRMED | CHỜ |
| F-029 | SWF L01 | SHOULD | intuition · step 0 · show (SVG) + say | hình gán "bước kết thúc" cho "mọi quân đều đổ" | PLAUSIBLE | CHỜ |
| N-001 | PLC L12 | ghi chú | — | gọi deadlock là "khoá chết" trong khi OSY/SWF gọi "bế tắc"; biến `l` trong bảng giống số 1 (khung 00074) | — | GHI |

## Chi tiết chuỗi (để áp)

### F-001 · lessons/osy/L14_bao_ve_phan_quyen.yaml
- cũ: `<p>① $\hl{\text{rw-r-----}}$. Nhóm có r-- → bit w = 0 → <b>không</b> sửa được.</p>`
- mới: `<p>① $\hl{\texttt{rw-r-----}}$. Nhóm có r-- → bit w = 0 → <b>không</b> sửa được.</p>` (nếu `\texttt` vẫn gộp: `<b class="red">rw-r-----</b>` ngoài công thức). Quét cùng mẫu `\text{…--…}` toàn kho.

### F-002 · lessons/osy/L15_hanh_trinh_bo_lap_lich_linux.yaml
- show cũ: `<td>con số nói một tác vụ hay một nhóm được mấy phần CPU so với bên khác: trọng số gấp đôi thì phần gấp đôi</td>`
- show mới: `<td>con số nói một tác vụ (một việc được lập lịch, như một tiến trình) hay một nhóm được mấy phần CPU so với bên khác: trọng số gấp đôi thì phần gấp đôi</td>`
- say cũ: `Trọng số là con số nói một tác vụ hay một nhóm được mấy phần bộ xử lý so với bên khác, trọng số gấp đôi thì phần cũng gấp đôi.`
- say mới: `Trọng số là con số nói một tác vụ, tức một việc được lập lịch như một tiến trình, hay một nhóm được mấy phần bộ xử lý so với bên khác, trọng số gấp đôi thì phần cũng gấp đôi.`

### F-003 · cùng tệp OSY L15
- cũ: `<p class="note">Thực hành: chia công bằng cho nhóm trước, rồi mới tới tác vụ. Điều kiện: máy thật sự được chia cho nhiều người hay nhiều dịch vụ.</p>`
- mới: thêm câu `Con số 2048 và 1024 theo ví dụ của hướng dẫn; giao diện nhóm đời sau dùng thang số khác, điều cần giữ là tỉ lệ 2 : 1.` (cần mở tài liệu nhân `admin-guide/cgroup-v2` trước khi nhận)

### F-004 · lessons/toc/L02_nfa_tap_con.yaml
- cũ: `<p>Ở NFA, $\delta(q, a)$ là một <b>tập</b> trạng thái:`
- mới: `<p>Ở NFA (viết tắt của ôtômat hữu hạn không đơn định), $\delta(q, a)$ là một <b>tập</b> trạng thái:`

### F-005 · lessons/toc/L03_bieu_thuc_chinh_quy.yaml
- cũ: `<code>(.+)\1</code> khớp $0101$ (một chuỗi viết hai lần)`
- mới: `<code>(.+)\1</code> — <code>.+</code> là một đoạn bất kỳ dài ít nhất 1, <code>\1</code> đòi lặp lại đúng đoạn trong ngoặc — khớp $0101$ (một chuỗi viết hai lần)`

### F-006 · lessons/plc/L02_dequy_xuong.yaml
- cũ: `lấy <code>3</code> → trả cây <code>(* 2 3)</code>.</p>`
- mới: `lấy <code>3</code> → trả cây <code>(* 2 3)</code> <span class="note">(dạng tiền tố: dấu phép viết trước, rồi con trái, con phải)</span>.</p>`

### F-007 · lessons/plc/L07_bao_dong.yaml
- cũ: `<code>n</code> sống ở đâu?</p>`
- mới: `<code>n</code> sống ở đâu?<br><span class="note"><code>nonlocal n</code>: dòng báo rằng <code>n</code> là biến của hàm bao ngoài, không phải biến mới của <code>inc</code>.</span></p>`

### F-008 · cùng tệp PLC L07
- cũ: `<code>map(lambda x: x * 2, [1, 2, 3])</code> → <code>[2, 4, 6]</code>`
- mới: `<code>list(map(lambda x: x * 2, [1, 2, 3]))</code> → <code>[2, 4, 6]</code>` (kiểm sổ `audit/review/screen_code/PLC.yaml`: khối đổi sha → cập nhật sổ)

### F-009 · lessons/plc/L01_phan_tich_tu_vung.yaml
- cũ: `<p class="note">Khoảng trắng cũng khớp một mẫu, nhưng bị bỏ đi, không thành từ tố.</p>`
- mới: `<p class="note">Khoảng trắng cũng khớp một mẫu, nhưng bị bỏ đi, không thành từ tố. Bảng xếp theo loại; trong bộ cắt, mẫu KHOA được khai báo trước mẫu TEN.</p>`

## Pháp lý đã đối chiếu văn bản gốc trong phiên này (CB-LF2-2)
Tệp tải về: scratchpad phiên `…/scratchpad/legal/` (sha256 ghi dưới; tải 2026-11-11 ≈ 06:33–06:36Z).
| Văn bản | Nguồn gốc | sha256 (16) | Kết quả đối chiếu | Việc phải sửa |
|---|---|---|---|---|
| TT 40/2024/TT-NHNN, bản hợp nhất 76/VBHN-NHNN (gồm TT 41/2025 và TT 22/2026) | datafiles.chinhphu.vn/cpp/files/vbpq/2026/7/76-vbhn-nhnn.signed.pdf | 0cf5991e9871e876 | Đ.26 k.1: tổng hạn mức qua các ví cá nhân của 01 khách tại 01 tổ chức, gồm chuyển tiền và thanh toán ở điểm b, c, d, đ k.2 Đ.25 (KHÔNG gồm rút về tài khoản liên kết của chính chủ, điểm a), tối đa 100 triệu/tháng; không áp cho ví của đơn vị chấp nhận thanh toán. Đ.26 k.3: **ngoài** hạn mức k.1, tổ chức được quy định **thêm** hạn mức cho thanh toán dịch vụ công, điện, nước, viễn thông, phí giao thông, học phí, viện phí, BHXH/BHYT, phí bảo hiểm, trả nợ tổ chức tín dụng; tổng thêm không quá 300 triệu/tháng. Đ.25 k.5: không nạp/rút tiền mặt, không cấp tín dụng, không trả lãi số dư ví. Đ.27 k.1: tổng số dư tài khoản đảm bảo ≥ tổng số dư ví | BNX L12: "nâng tới 300 triệu" → "thêm một hạn mức riêng, không quá 300 triệu, cho một số khoản thanh toán thiết yếu"; ghi loại giao dịch tính vào 100 triệu |
| TT 31/2024/TT-NHNN | Công báo số 825+826, 21-7-2024 (congbaocdn.chinhphu.vn …31-2024-tt-nhnn.pdf) | 0ab95f4c65d31eda | Đ.10 k.1: nhóm 1 quá hạn dưới 10 ngày; nhóm 2 quá hạn đến 90 ngày (trừ phần nhóm 1); nhóm 3: 91–180; nhóm 4: 181–360; nhóm 5: trên 360. Khớp bài và tài liệu phỏng vấn | Không; đổi ghi chú "nguồn thứ cấp" thành nguồn gốc |
| TT 50/2024/TT-NHNN | Công báo số 1279+1280, 30-11-2024 | 10e35c0acecfbf89 | Hiệu lực 01/01/2025 (Đ.22). Phụ lục 01 nhóm I.3: G ≤ 10 triệu và G + Tksth ≤ 20 triệu → loại A/B; G ≤ 10 triệu mà G + Tksth > 20 triệu, hoặc G > 10 triệu → loại C/D (cần sinh trắc học theo Phụ lục 02, cột khách hàng cá nhân). **Tksth tính lại bằng 0 đầu ngày hoặc ngay sau một giao dịch đã xác nhận theo loại C/D.** Đ.22 không bãi bỏ QĐ 2345 | BNK L13: thêm ghi chú "từ 01/01/2025 quy tắc nằm ở TT 50/2024; tổng cộng dồn tính lại từ 0 sau lần đã xác thực sinh trắc học"; MASTER Mục 7 dòng 10 |
| TT 77/2025/TT-NHNN (sửa TT 50/2024, hiệu lực 01/3/2026) | datafiles.chinhphu.vn/cpp/files/vbpq/2026/01/77-nhnn.pdf (bản quét) | de25dc63ac6ca27e | CHƯA đọc nội dung (OCR nhiễu) → chưa biết có đổi ngưỡng không | NOT_VERIFIED; ghi vào bàn giao |
| TT 64/2024/TT-NHNN + phụ lục | datafiles.chinhphu.vn/cpp/files/vbpq/2025/01/64-nhnn.pdf, 64-nhnn-kem.pdf (bản quét, OCR) | 1aa6a4ae3942a9b8 / 8c9b16940897f5b4 | Đ.8 "Hợp đồng giữa Ngân hàng với bên thứ ba": ngân hàng phải ký kết hợp đồng với bên thứ ba về triển khai Open API; danh mục Open API theo nhóm ở Đ.6, bảng danh mục trong phụ lục đặc tả kỹ thuật; ban hành 31/12/2024, hiệu lực 01/3/2025 (trang vanban.chinhphu.vn). Khớp BNX L14 | Không |
| TT 19/2021/TT-BTC | Công báo số 531+532, 13-4-2021 | fda4ec68af0e5964 | Đ.21 k.2: hệ thống của ngân hàng tự động tạo "số tham chiếu" của chứng từ nộp NSNN (cấu trúc ở Đ.20 k.3 điểm a), chuyển tiền + số tham chiếu tới ngân hàng nơi KBNN mở tài khoản. Khớp BNX L12. Có TT 46/2024/TT-BTC sửa đổi (chưa đọc) | Không; ghi TT 46/2024 là chưa đọc |

## Độ phủ CV → bài (yêu cầu bổ sung của người dùng, 2026-11-11)
Máy đo: `cv_scan.py` → `logs/cv_scan.out` (79 thuật ngữ trên CV; 64 CÓ, 15 yếu). Mục yếu, chờ người điều phối đọc lại bằng từ đồng nghĩa tiếng Việt rồi quyết bài bổ sung:
ForkJoinPool · CompletableFuture · chấm điểm tín dụng/thẩm định · ECM · trường đa trị T24 · Spring Cloud · Spring Security · CQRS · Redis Cluster · DLQ · dấu vân tay thiết bị · JUnit 5/Mockito · AEM · OSGi/Sling/HTL/JCR · Scikit-Learn.

## Cập nhật 2026-11-12 (phiên LF2-tiếp) — TT 77/2025/TT-NHNN (CB-LF2-5, đóng một phần)
- Nguồn đọc: luatvietnam.vn, trang văn bản hợp nhất 25/VBHN-NHNN (2026) — bản chữ do trang thứ cấp đăng lại, mức CITED; bản PDF chính thức trên datafiles.chinhphu.vn là ảnh quét, trang SBV cần đăng nhập. Đọc 2026-11-12.
- Điều 12 của TT 77/2025 (trích trong bản hợp nhất): Điều 3 và Điều 10 áp dụng từ 01/07/2026 với đơn vị phục vụ cả cá nhân và tổ chức; từ 01/10/2026 với đơn vị chỉ phục vụ khách hàng tổ chức. TT hiệu lực 01/03/2026.
- Phụ lục 01 nhóm I.3 (chuyển tiền, ví điện tử, khách hàng cá nhân): mốc G = 10 triệu và G + T ksth = 20 triệu còn nguyên; T ksth về 0 đầu ngày hoặc sau khi xác nhận bằng loại C/D (sinh trắc học). Nhóm II.2 (tổ chức): 50 triệu (G) và 100 triệu (G + T ksth).
- Việc đã làm: BNK L13 step 3 ghi thêm "sửa bởi Thông tư 77/2025 (01/03/2026), ngưỡng cá nhân vẫn 10 và 20 triệu" (chỉ màn hình; lời đọc giữ nguyên); gen + lint 0/0 + render 0 vấn đề. Cần dựng lại BNK L13 rồi `interview_sync_video.py`.
- Còn mở: đọc bản gốc chính thức (không phải trang thứ cấp) khi có; TT 46/2024/TT-BTC (sửa TT 19/2021) chưa đọc.
