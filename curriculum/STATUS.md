# Hiện trạng sản xuất (SINH TỰ ĐỘNG — không sửa tay)

Sinh bởi `audit/review/status_report.py` từ `audit/review/audit_all.tsv` (chạy lúc 2026-11-08T12:23Z) và `out/*/*/build_report.json`.
“Hoàn thiện” = đã dựng, lint 0 FAIL 0 WARN, video khớp dấu băm đặc tả và lời đọc hiện tại, đúng một giọng, ASR 0 câu chưa xem xét.

**Tổng:** 656 bài trong 42 lộ trình · 656 có đặc tả · **655 hoàn thiện** · 5589 phút video hoàn thiện.

| Khoá | Tên | Bài | Đặc tả | Hoàn thiện | Phút | Bộ kiểm độc lập | Còn lại |
|---|---|---|---|---|---|---|---|
| ACB | Phỏng vấn Kỹ sư Tích hợp ACB | 9 | 9 | 9 | 50.5 | phép kiểm `checks` trong từng bài (lint) | — |
| AGT | AI agent | 13 | 13 | 13 | 110.3 | verify_agt.py 15/15 PASS | — |
| AIF | Nền tảng trí tuệ nhân tạo | 15 | 15 | 14 | 95.8 | verify_aif.py 25/25 PASS | 1 bài: L11: ASR chưa xem xét 1: Xác suất vừa mưa vừa mang ô bằng xác suất trời mưa |
| BCH | Blockchain và sổ cái phân tán | 13 | 13 | 13 | 112.1 | verify_bch.py 13/13 PASS | — |
| BNK | Nền tảng Backend Ngân hàng cho người mất gốc | 15 | 15 | 15 | 115.1 | verify_bnk.py 17/17 PASS | — |
| CAS | Tình huống chuyên gia | 12 | 12 | 12 | 124.1 | verify_cas.py 93/93 PASS | — |
| CLC | Điện toán đám mây | 13 | 13 | 13 | 86.5 | verify_clc.py 13/13 PASS | — |
| CLD | Hệ thống hướng dịch vụ | 16 | 16 | 16 | 124.8 | verify_cld.py 20/20 PASS | — |
| CS112 | Phân tích & Thiết kế Thuật toán | 30 | 30 | 30 | 281.1 | verify_cs112.py 53/53 PASS; verify_cs112_p2.py 37/37 PASS | — |
| CS115 | Toán cho Khoa học Máy tính | 46 | 46 | 46 | 457.6 | verify_cs115_tex.py 59/59 PASS; verify_cs115_l44.py 16/16 PASS | — |
| CSA | Hệ thống máy tính | 17 | 17 | 17 | 142.9 | phép kiểm `checks` trong từng bài (lint) | — |
| CVI | Thị giác máy tính | 13 | 13 | 13 | 141.5 | verify_cvi.py 112/112 PASS | — |
| DAN | Phân tích dữ liệu | 13 | 13 | 13 | 99.4 | verify_dan.py 13/13 PASS | — |
| DBS | Cơ sở dữ liệu | 18 | 18 | 18 | 162.1 | verify_dbs.py 42/42 PASS | — |
| DEN | Kỹ thuật dữ liệu | 15 | 15 | 15 | 122.3 | verify_den.py 15/15 PASS | — |
| DMS | Toán rời rạc | 21 | 21 | 21 | 193.3 | phép kiểm `checks` trong từng bài (lint) | — |
| DSC | Khoa học dữ liệu | 16 | 16 | 16 | 121.8 | verify_dsc.py 30/30 PASS | — |
| DSY | Hệ phân tán và dữ liệu lớn | 16 | 16 | 16 | 133.6 | verify_dsy.py 33/33 PASS | — |
| DVO | DevOps: tích hợp, triển khai liên tục và vận hành | 14 | 14 | 14 | 110.4 | verify_dvo.py 18/18 PASS | — |
| ESY | Hệ thống nhúng và thời gian thực | 16 | 16 | 16 | 137.2 | verify_esy.py 72/72 PASS | — |
| EVT | Kiến trúc hướng sự kiện | 12 | 12 | 12 | 95.1 | verify_evt.py 12/12 PASS | — |
| GFX | Đồ hoạ máy tính | 14 | 14 | 14 | 122.2 | verify_gfx.py 19/19 PASS | — |
| HCI | Tương tác người–máy | 13 | 13 | 13 | 107.8 | verify_hci.py 27/27 PASS | — |
| INT | Khung Chuẩn Phỏng vấn Kỹ sư Tích hợp Ngân hàng | 8 | 8 | 8 | 44.8 | phép kiểm `checks` trong từng bài (lint) | — |
| IRS | Truy hồi thông tin và hệ gợi ý | 14 | 14 | 14 | 162.1 | verify_irs.py 123/123 PASS | — |
| JVA | Lập trình Java từ con số 0 | 13 | 13 | 13 | 106.9 | verify_jva.py 110/110 PASS | — |
| LLM | Mô hình ngôn ngữ lớn | 15 | 15 | 15 | 99.7 | verify_llm.py 18/18 PASS | — |
| MLO | MLOps: đưa mô hình học máy vào vận hành | 15 | 15 | 15 | 112.8 | verify_mlo.py 20/20 PASS | — |
| NET | Mạng máy tính | 16 | 16 | 16 | 138.5 | verify_net.py 89/89 PASS | — |
| OSY | Hệ điều hành | 16 | 16 | 16 | 139.9 | phép kiểm `checks` trong từng bài (lint) | — |
| PAR | Tính toán song song và GPU | 14 | 14 | 14 | 143.8 | verify_par.py 96/96 PASS | — |
| PLC | Ngôn ngữ lập trình và trình biên dịch | 14 | 14 | 14 | 112.3 | verify_plc.py 67/67 PASS | — |
| RBM | Toán cho robot và hệ động lực | 18 | 18 | 18 | 173.7 | verify_rbm.py 92/92 PASS | — |
| RLN | Học tăng cường | 14 | 14 | 14 | 147.9 | verify_rln.py 94/94 PASS | — |
| ROB | Robot tự hành | 14 | 14 | 14 | 122.3 | verify_rob.py 14/14 PASS | — |
| SAR | Kiến trúc hệ thống | 14 | 14 | 14 | 114.9 | verify_sar.py 15/15 PASS | — |
| SDP | Kỹ thuật lập trình và mẫu thiết kế | 18 | 18 | 18 | 131.5 | verify_sdp.py 36/36 PASS | — |
| SEC | An toàn thông tin | 16 | 16 | 16 | 119.4 | verify_sec.py 26/26 PASS | — |
| SEP | Xã hội, đạo đức và nghề nghiệp trong tin học | 12 | 12 | 12 | 122.2 | verify_sep.py 66/66 PASS | — |
| SWF | Nền tảng phần mềm đúng đắn | 14 | 14 | 14 | 88.2 | verify_swf.py 47/47 PASS | — |
| TOC | Lý thuyết tính toán | 15 | 15 | 15 | 129.9 | verify_toc.py 102/102 PASS | — |
| WEB | Ứng dụng web và di động | 16 | 16 | 16 | 131.0 | verify_web.py 16/16 PASS | — |
