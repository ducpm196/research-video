# Sửa BNX L26 theo R_BNX_L24_30 (2026-11-14)

Nguồn sửa: `audit/bnx/src/l26.py`, `audit/bnx/ver/l26.py`, `tools/checklib_bnx/l26.py`, `audit/bnx/sources_l26.md` (mục MVHELP), `curriculum/bnx.yaml` (mục L26: mục tiêu 1 và ví dụ), nhóm `# ── L26 ──` của `tools/registry/symbols.BNX.yaml`. YAML sinh bằng `gen.py L26`.

## MUST (1 mục của L26)
| Mục báo cáo | Kiểm lại | Đã sửa |
|---|---|---|
| "6 pha" ở formula step 2, bảng sym, example step 3, giáo án | Đúng: chạy `mvn -B help:describe -Dcmd=package` (Maven 3.9.11) cho 17 pha tới `package`, chỉ 6 pha có MỤC TIÊU của phần mở rộng gắn vào; dòng `--- plugin:phiên-bản:mục-tiêu ---` của `mvn package` là mục tiêu | formula step 2: bảng pha → mục mục tiêu (process-resources → resources:resources … package → jar:jar), nói rõ "pha chỉ là chặng, việc làm thật do mục tiêu gắn vào pha", công thức "gọi package ⇒ 17 pha, 6 mục tiêu"; bảng sym thêm dòng "mục tiêu (goal)" và sửa "pha"; example step 3: "6 mục tiêu của phần mở rộng chạy đúng thứ tự"; mục tiêu giáo án 1 và `example` ở `curriculum/bnx.yaml` đổi "pha" → "mục tiêu của phần mở rộng", đồng bộ `objectives` của bài. Lời đọc khớp ("sáu mục tiêu"). ver thêm kiểm `help:describe` thật (17 pha, 6 cặp pha-mục tiêu khớp bảng trên màn hình) |

## SHOULD
| Mục | Đã sửa / lý do |
|---|---|
| Jenkinsfile thiếu khối `post` | Tách formula step 5 thành 2 khung: phần 1 (dòng 1–9, `agent any`, hai `stage`) và phần 2 (dòng 10–17: Deploy + khối `post { failure … }`), giải thích `failure` chỉ chạy khi có giai đoạn hỏng |
| `agent any`, `sh`, Groovy không giải thích | Giảng tại chỗ ở step 5 phần 1 (xem P1) |
| Cây `dependency:tree` ghép 2 lệnh | `SH_CAY` đổi: lệnh thường rồi `echo` nhãn rồi lệnh `-Dverbose` có `cat` nguyên văn (không còn `grep omitted`); màn hình giờ in đúng cả hai cây, dòng omitted nằm dưới commons-text. Chạy lại thật; ver kiểm cấu trúc 4 dòng (dòng omitted là con của commons-text, lang3 3.9 là nhánh riêng) |
| "Kết quả chạy thật" trên mô phỏng Python | Tiêu đề đổi "Kết quả mô phỏng (Python, không phải Jenkins)" |
| Hook "vì sao máy bạn chạy được mà máy chủ dựng thì không?" không có cảnh trả lời | Sửa hook thành câu hỏi bài trả lời trực tiếp: "Làm sao biết bản nào đang chạy, và làm sao để máy bạn và mọi máy khác dựng ra cùng một sản phẩm?" (cây phụ thuộc ở example 1; dựng tái lập ở step 6 và example 3) |
| Nhãn MÔ PHỎNG chữ nhỏ (L26/00020) | Chữ 34 px đậm cam "MÔ PHỎNG — Jenkins không chạy trên máy này" + dòng phụ |
| Mũi tên "hỏng" không chạm ô post failure (00020) | Dời ô `post failure` xuống, mũi tên kết thúc ở mép ô; đã xem lại khung |
| Tiêu đề "cây phụ thuộc và đường ống dựng" chỉ hiện đường ống ở khung 2 | KHÔNG sửa: cảnh có hai step, step 1 là cây, step 2 là đường ống; tiêu đề cảnh đúng, chỉ khung đơn lẻ thấy một nửa |
| 00042 tiêu đề "Chạy thật" chỉ hiện mã | Đổi tiêu đề thành "Mã dựng hai lần … (kết quả ở khung sau)" |
| 00086 chữ xám trên nền cam (ghi chú lab) | Bỏ lớp `note` ở đoạn ghi chú của cảnh Tự làm |
| Không dựng lại được số gói 1/9/34 (người đọc: CHƯA KIỂM) | ver chạy lại thật: `dependency:tree` đếm ra 1, 9, 34 (khớp `dependency:list`) — PASS |
| Lab `de.md` | Không mâu thuẫn trong L26; không đổi |

## P1 (thuật ngữ tại chỗ, id E52 trong `symbols.BNX.yaml`)
| Thuật ngữ | Giảng ở | id |
|---|---|---|
| Gradle (công cụ dựng thứ hai cho Java, đọc `build.gradle`) | hook | `bnx_gradle` (regex loại cụm "Gradle và Jenkins" của cảnh forward_ref ở L25) |
| Jenkins, máy chủ dựng (máy riêng dựng tự động khi có mã mới) | bảng sym, dòng Jenkinsfile | `bnx_jenkins`, `bnx_may_dung` |
| Groovy, `agent any`, `sh '…'` | formula step 5 (phần 1) | `bnx_groovy`, `bnx_agent`, `bnx_sh` |
| mã băm (sha256) | formula step 6 | `bnx_ma_bam` |
Lời đọc không nói tên tiếng Anh chưa dò phát âm (nói "công cụ dựng thứ hai", "dòng chọn máy"). Thay phần forward_ref cuối bài ("SOAP/WSDL và SFTP") bằng "tích hợp hệ cũ bằng phong bì XML và truyền tệp lô" để L26 không dùng thuật ngữ L27 trước khi giảng (L27 đã đăng ký `bnx_soap`/`bnx_sftp`).
**Việc cho người điều phối (ngoài phạm vi L26):** L27 và L30 dùng "mã băm" → cần `assumes: ["bnx_ma_bam"]` (hoặc `introduces` tại chỗ) vì L26 đứng trước trong dãy.

## Độ dài
Lời đọc 2 291 từ (≤ 2 300; trước đó 2 271). Cắt chỗ khác (cảnh intuition, quiz đề, check, quymo, recap, formula step 1/3/4, practice) tương ứng; không bỏ mục tiêu `covers`.

## Cổng thật
Xem tin nhắn cuối: lint 0/0, render 0 vấn đề, `verify_bnx.py L26` 25/25 PASS (có thêm 2 kiểm mới: cây chi tiết, `help:describe`), `gen-screen` 18 khối chưa khớp 0, `screen_fast.py L26` PASS 37 · FAIL 0, `lab_gate.py BNX` 13 PASS · 0 FAIL. Khung đã xem: 00014 (sym), 00020 (Jenkinsfile mô phỏng), 00025 (bảng pha–mục tiêu), 00033 (step 5 phần 1), 00041 (hai cây phụ thuộc).
