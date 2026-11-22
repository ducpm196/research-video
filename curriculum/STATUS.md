# Hiện trạng sản xuất (SINH TỰ ĐỘNG — không sửa tay)

Sinh bởi `audit/review/status_report.py` từ `audit/review/audit_all.tsv` (chạy lúc 2026-11-22T10:13Z) và `out/*/*/build_report.json`.
“Hoàn thiện” = đã dựng, lint 0 FAIL 0 WARN, video khớp dấu băm đặc tả và lời đọc hiện tại, đúng một giọng, ASR 0 câu chưa xem xét.

**Tổng:** 777 bài trong 50 lộ trình · 777 có đặc tả · **776 hoàn thiện** · 9241 phút video hoàn thiện.

| Khoá | Tên | Bài | Đặc tả | Hoàn thiện | Phút | Bộ kiểm độc lập | Còn lại |
|---|---|---|---|---|---|---|---|
| ACB | Phỏng vấn Kỹ sư Tích hợp ACB | 9 | 9 | 9 | 148.9 | verify_acb.py 312/312 PASS | — |
| AGT | AI agent | 13 | 13 | 13 | 140.5 | verify_agt.py 15/15 PASS | — |
| AIF | Nền tảng trí tuệ nhân tạo | 15 | 15 | 15 | 153.5 | verify_aif.py 26/26 PASS | — |
| BCH | Blockchain và sổ cái phân tán | 13 | 13 | 13 | 139.0 | verify_bch.py 13/13 PASS | — |
| BNK | Nền tảng Backend Ngân hàng cho người mất gốc | 15 | 15 | 15 | 233.2 | verify_bnk.py 48/48 PASS | — |
| BNX | Backend ngân hàng mở rộng theo JD | 39 | 39 | 38 | 581.3 | verify_bnx.py 1011/1011 PASS | 1 bài: L19: FAIL    BNX L19 check 3 0 [output/-] of BNX L19 check 2 0 không PASS:  |
| CAS | Tình huống chuyên gia | 12 | 12 | 12 | 149.1 | verify_cas.py 93/93 PASS | — |
| CLC | Điện toán đám mây | 13 | 13 | 13 | 116.1 | verify_clc.py 13/13 PASS | — |
| CLD | Hệ thống hướng dịch vụ | 16 | 16 | 16 | 149.0 | verify_cld.py 20/20 PASS | — |
| CPR | Lập trình C và bộ nhớ: con trỏ, cấp phát động, tệp và gcc | 10 | 10 | 10 | 56.5 | verify_cpr.py 37/37 PASS | — |
| CS112 | Phân tích & Thiết kế Thuật toán | 30 | 30 | 30 | 559.6 | verify_cs112.py 53/53 PASS; verify_cs112_p2.py 37/37 PASS | — |
| CS115 | Toán cho Khoa học Máy tính | 47 | 47 | 47 | 703.0 | verify_cs115_tex.py 59/59 PASS; verify_cs115_l44.py 16/16 PASS | — |
| CSA | Hệ thống máy tính | 17 | 17 | 17 | 162.9 | phép kiểm `checks` trong từng bài (lint) | — |
| CVI | Thị giác máy tính | 13 | 13 | 13 | 168.2 | verify_cvi.py 112/112 PASS | — |
| DAN | Phân tích dữ liệu | 13 | 13 | 13 | 138.2 | verify_dan.py 13/13 PASS | — |
| DBS | Cơ sở dữ liệu | 18 | 18 | 18 | 180.9 | verify_dbs.py 42/42 PASS | — |
| DEN | Kỹ thuật dữ liệu | 15 | 15 | 15 | 152.4 | verify_den.py 15/15 PASS | — |
| DMS | Toán rời rạc | 21 | 21 | 21 | 392.0 | verify_dms.py ? PASS | — |
| DSC | Khoa học dữ liệu | 16 | 16 | 16 | 169.6 | verify_dsc.py 30/30 PASS | — |
| DSY | Hệ phân tán và dữ liệu lớn | 16 | 16 | 16 | 152.2 | verify_dsy.py 33/33 PASS | — |
| DVO | DevOps: tích hợp, triển khai liên tục và vận hành | 14 | 14 | 14 | 128.9 | verify_dvo.py 18/18 PASS | — |
| ESY | Hệ thống nhúng và thời gian thực | 16 | 16 | 16 | 173.7 | verify_esy.py 72/72 PASS | — |
| EVT | Kiến trúc hướng sự kiện | 12 | 12 | 12 | 119.0 | verify_evt.py 12/12 PASS | — |
| FND | Nền thực hành: dòng lệnh, tệp, dữ liệu, HTTP, SQL, Git | 11 | 11 | 11 | 204.2 | verify_fnd.py 83/83 PASS | — |
| GFX | Đồ hoạ máy tính | 14 | 14 | 14 | 153.0 | verify_gfx.py 19/19 PASS | — |
| HCI | Tương tác người–máy | 13 | 13 | 13 | 134.0 | verify_hci.py 27/27 PASS | — |
| INT | Giáo trình Phỏng vấn Senior Banking ACB | 9 | 9 | 9 | 139.2 | verify_int.py ? PASS | — |
| IRS | Truy hồi thông tin và hệ gợi ý | 14 | 14 | 14 | 210.6 | verify_irs.py 150/150 PASS | — |
| JV2 | Java trung cấp | 10 | 10 | 10 | 168.9 | verify_jv2.py 88/88 PASS | — |
| JVA | Lập trình Java từ con số 0 | 13 | 13 | 13 | 176.7 | verify_jva.py 153/153 PASS; verify_l12_screen.py ? PASS | — |
| LLM | Mô hình ngôn ngữ lớn | 15 | 15 | 15 | 153.3 | verify_llm.py 18/18 PASS | — |
| LNX | Linux và Container thực chiến | 10 | 10 | 10 | 56.9 | verify_lnx.py 37/37 PASS | — |
| MLO | MLOps: đưa mô hình học máy vào vận hành | 15 | 15 | 15 | 158.5 | verify_mlo.py 20/20 PASS | — |
| MLP | Học máy Thực hành | 14 | 14 | 14 | 80.9 | verify_mlp.py 42/42 PASS | — |
| NET | Mạng máy tính | 16 | 16 | 16 | 158.9 | verify_net.py 89/89 PASS | — |
| OSY | Hệ điều hành | 16 | 16 | 16 | 166.2 | phép kiểm `checks` trong từng bài (lint) | — |
| PAR | Tính toán song song và GPU | 14 | 14 | 14 | 166.7 | verify_par.py 96/96 PASS | — |
| PLC | Ngôn ngữ lập trình và trình biên dịch | 14 | 14 | 14 | 143.8 | verify_plc.py 72/72 PASS | — |
| PRJ | Dự án tổng hợp cuối mỗi chặng | 11 | 11 | 11 | 62.1 | verify_prj.py 28/28 PASS | — |
| PYT | Python từ con số 0 | 14 | 14 | 14 | 296.1 | verify_pyt.py 228/228 PASS | — |
| RBM | Toán cho robot và hệ động lực | 18 | 18 | 18 | 215.7 | verify_rbm.py 92/92 PASS | — |
| RLN | Học tăng cường | 14 | 14 | 14 | 176.0 | verify_rln.py 94/94 PASS | — |
| ROB | Robot tự hành | 14 | 14 | 14 | 155.9 | verify_rob.py 14/14 PASS | — |
| SAR | Kiến trúc hệ thống | 14 | 14 | 14 | 144.4 | verify_sar.py 15/15 PASS | — |
| SDP | Kỹ thuật lập trình và mẫu thiết kế | 18 | 18 | 18 | 151.2 | verify_sdp.py 36/36 PASS | — |
| SEC | An toàn thông tin | 16 | 16 | 16 | 140.4 | verify_sec.py 26/26 PASS | — |
| SEP | Xã hội, đạo đức và nghề nghiệp trong tin học | 12 | 12 | 12 | 141.0 | verify_sep.py 71/71 PASS | — |
| SWF | Nền tảng phần mềm đúng đắn | 14 | 14 | 14 | 107.1 | verify_swf.py 47/47 PASS | — |
| TOC | Lý thuyết tính toán | 15 | 15 | 15 | 160.3 | verify_toc.py 102/102 PASS | — |
| WEB | Ứng dụng web và di động | 16 | 16 | 16 | 151.6 | verify_web.py 16/16 PASS | — |
