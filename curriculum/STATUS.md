# Hiện trạng sản xuất (SINH TỰ ĐỘNG — không sửa tay)

Sinh bởi `audit/review/status_report.py` từ `audit/review/audit_all.tsv` (chạy lúc 2026-11-02T00:15Z) và `out/*/*/build_report.json`.
“Hoàn thiện” = đã dựng, lint 0 FAIL 0 WARN, video khớp dấu băm đặc tả và lời đọc hiện tại, đúng một giọng, ASR 0 câu chưa xem xét.

**Tổng:** 575 bài trong 38 lộ trình · 476 có đặc tả · **475 hoàn thiện** · 3740 phút video hoàn thiện.

| Khoá | Tên | Bài | Đặc tả | Hoàn thiện | Phút | Bộ kiểm độc lập | Còn lại |
|---|---|---|---|---|---|---|---|
| AGT | AI agent | 12 | 12 | 12 | 94.8 | verify_agt.py 12/12 PASS | — |
| AIF | Nền tảng trí tuệ nhân tạo | 14 | 14 | 13 | 81.2 | verify_aif.py 20/20 PASS | 1 bài: L11: ASR chưa xem xét 1: Xác suất vừa mưa vừa mang ô bằng xác suất trời mưa |
| BCH | Blockchain và sổ cái phân tán | 12 | 12 | 12 | 95.6 | verify_bch.py 12/12 PASS | — |
| CAS | Tình huống chuyên gia: phân tích sự cố có thật | 12 | 0 | 0 | 0.0 | chưa soạn bài (giáo án: verify_plan_curricula.py) | — |
| CLC | Điện toán đám mây | 12 | 12 | 12 | 71.2 | verify_clc.py 12/12 PASS | — |
| CLD | Hệ thống hướng dịch vụ | 16 | 16 | 16 | 124.2 | verify_cld.py 20/20 PASS | — |
| CS112 | Phân tích & Thiết kế Thuật toán | 29 | 29 | 29 | 263.2 | verify_cs112.py 47/47 PASS; verify_cs112_p2.py 37/37 PASS | — |
| CS115 | Toán cho Khoa học Máy tính | 45 | 45 | 45 | 438.3 | verify_cs115_tex.py 59/59 PASS; verify_cs115_l44.py 16/16 PASS | — |
| CSA | Hệ thống máy tính | 16 | 16 | 16 | 126.8 | phép kiểm `checks` trong từng bài (lint) | — |
| CVI | Thị giác máy tính | 12 | 0 | 0 | 0.0 | chưa soạn bài (giáo án: verify_plan_curricula.py) | — |
| DAN | Phân tích dữ liệu | 12 | 12 | 12 | 84.2 | verify_dan.py 12/12 PASS | — |
| DBS | Cơ sở dữ liệu | 17 | 17 | 17 | 146.6 | verify_dbs.py 37/37 PASS | — |
| DEN | Kỹ thuật dữ liệu | 14 | 14 | 14 | 103.3 | verify_den.py 14/14 PASS | — |
| DMS | Toán rời rạc | 20 | 20 | 20 | 174.1 | phép kiểm `checks` trong từng bài (lint) | — |
| DSC | Khoa học dữ liệu | 15 | 15 | 15 | 106.5 | verify_dsc.py 25/25 PASS | — |
| DSY | Hệ phân tán và dữ liệu lớn | 15 | 15 | 15 | 118.6 | verify_dsy.py 27/27 PASS | — |
| DVO | DevOps: tích hợp, triển khai liên tục và vận hành | 13 | 13 | 13 | 94.6 | verify_dvo.py 15/15 PASS | — |
| ESY | Hệ thống nhúng và thời gian thực | 15 | 15 | 15 | 121.3 | verify_esy.py 66/66 PASS | — |
| EVT | Kiến trúc hướng sự kiện | 11 | 11 | 11 | 79.0 | verify_evt.py 11/11 PASS | — |
| GFX | Đồ hoạ máy tính (lĩnh vực GIT của CS2023) | 13 | 0 | 0 | 0.0 | chưa soạn bài (giáo án: verify_plan_curricula.py) | — |
| HCI | Tương tác người–máy | 12 | 0 | 0 | 0.0 | chưa soạn bài (giáo án: verify_plan_curricula.py) | — |
| IRS | Truy hồi thông tin và hệ gợi ý | 13 | 0 | 0 | 0.0 | chưa soạn bài (giáo án: verify_plan_curricula.py) | — |
| LLM | Mô hình ngôn ngữ lớn | 14 | 14 | 14 | 85.0 | verify_llm.py 14/14 PASS | — |
| MLO | MLOps: đưa mô hình học máy vào vận hành | 14 | 14 | 14 | 97.3 | verify_mlo.py 16/16 PASS | — |
| NET | Mạng máy tính | 15 | 15 | 15 | 125.2 | verify_net.py 75/75 PASS | — |
| OSY | Hệ điều hành | 15 | 15 | 15 | 124.2 | phép kiểm `checks` trong từng bài (lint) | — |
| PAR | Tính toán song song và GPU | 13 | 0 | 0 | 0.0 | chưa soạn bài (giáo án: verify_plan_curricula.py) | — |
| PLC | Ngôn ngữ lập trình và trình biên dịch | 13 | 13 | 13 | 96.6 | verify_plc.py 59/59 PASS | — |
| RBM | Toán cho robot và hệ động lực | 17 | 17 | 17 | 155.6 | verify_rbm.py 80/80 PASS | — |
| RLN | Học tăng cường | 13 | 0 | 0 | 0.0 | chưa soạn bài (giáo án: verify_plan_curricula.py) | — |
| ROB | Robot tự hành | 13 | 13 | 13 | 106.4 | verify_rob.py 13/13 PASS | — |
| SAR | Kiến trúc hệ thống | 13 | 13 | 13 | 99.0 | verify_sar.py 14/14 PASS | — |
| SDP | Kỹ thuật lập trình và mẫu thiết kế | 17 | 17 | 17 | 115.9 | verify_sdp.py 32/32 PASS | — |
| SEC | An toàn thông tin | 15 | 15 | 15 | 105.7 | verify_sec.py 20/20 PASS | — |
| SEP | Xã hội, đạo đức và nghề nghiệp trong tin học | 11 | 0 | 0 | 0.0 | chưa soạn bài (giáo án: verify_plan_curricula.py) | — |
| SWF | Nền tảng phần mềm đúng đắn | 13 | 13 | 13 | 74.3 | verify_swf.py 42/42 PASS | — |
| TOC | Lý thuyết tính toán | 14 | 14 | 14 | 112.4 | verify_toc.py 94/94 PASS | — |
| WEB | Ứng dụng web và di động | 15 | 15 | 15 | 119.1 | verify_web.py 15/15 PASS | — |
