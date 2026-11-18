# Sửa BNX L31–L36 theo báo cáo người đọc R_BNX_L31_36 (2026-11-14)

Nguồn sửa: `audit/bnx/src/l31.py … l36.py` → `gen.py`. Không chạy build/tts/asr/audit_all/git. Docker chỉ `docker run --rm` ảnh ghim băm, mỗi lần một ảnh (Prometheus 3.16.0 cho L31, Vault 2.2.2 cho L32 trong `verify_bnx`); không chạm `bnx-ora`, `bnx-mss`. L31 và L36 do tác tử chính sửa; L32+L33 và L34+L35 do hai tác tử nhánh sửa theo cùng brief (tôi đã đọc báo cáo của họ và chạy lại toàn bộ cổng ở cuối).

## 1. Bài đã đổi
L31, L32, L33, L34, L35, L36 (nguồn `src/lNN.py`, `ver/lNN.py`, `screen/lNN.yaml` sinh bằng `gen-screen`, `lessons/bnx/Lxx_*.yaml` sinh bằng `gen.py`), `labs/BNX/L33/de.md`, `labs/BNX/L35/de.md`, `labs/BNX/L36/de.md` (do `write_lab` sinh lại), `curriculum/bnx.yaml` (Edit nhỏ ở L32 mục tiêu 3, L35 `example`, L36 mục tiêu 6), `tools/registry/symbols.BNX.yaml` (thêm mục sổ `term:`), `audit/bnx/sources_l36.md` (hai dòng S4, S5: điều kiện "For API v1").

Lời đọc (từ, ≤ 2 300): L31 2 298 · L32 2 284 · L33 2 293 · L34 2 268 · L35 2 287 · L36 2 293. Mỗi bài thêm câu giảng đều cắt chỗ khác (lời hook/tổng kết/đáp án/lặp lại điều đã có trên màn hình); không bỏ `covers`.

## 2. MUST (1) và SHOULD — từng mục
### L31
| Mục | Kết quả |
|---|---|
| MUST: khối "Chạy thật: NhatKy.py" thiếu 2 lệnh `ghi` | ĐÃ SỬA. Mã nén 2 dòng trống → 16 dòng; step 1 hiện 11 dòng đầu = đủ 6 lệnh `ghi(...)` (có `ghi("sc","a1","loi",ma="HET_GIO")` và `ghi("cong","a1","tra",http=504)`); step 2 hiện dòng 12–13 (in từng dòng) + 6 dòng kết quả; step 3 hiện dòng 14–16 (lọc `cid = a1`) + 35 ms. Chạy lại đúng mã hiện ra: 6 dòng, `cong:nhan > tt:tru-tien > sc:loi > cong:tra`, 35 ms. Kiểm mới ở `ver/l31.py` (đếm 6 lệnh `ghi` trong 11 dòng hiện) |
| SHOULD byte 324 không đếm lại được | ĐÃ SỬA. Bước 4 hiện đủ 8 dòng văn bản chỉ số (có `# HELP`, 47 byte → 277 + 47 = 324); `XuatChiSo.java` hiện 2 khung (dòng 1–10, 11–22); lệnh đo `for n in 0 100 10000 … grep -vc '^#' … wc -c` hiện ở quymo step 2 và lời nói rõ "đếm dòng không phải chú thích, đếm byte cả trang gồm dòng chú thích". Kiểm mới: 8 dòng = 324 byte, 5 dòng không chú thích |
| mục tiêu 1 lệch nội dung | Hết nhờ sửa MUST (mục tiêu giữ nguyên) |
| P1 JSON, biểu thức chính quy, Docker | JSON giảng ở formula step 1 (cặp tên:giá trị trong ngoặc nhọn) và gỡ chữ JSON khỏi hook/hình trước đó; biểu thức chính quy giảng ở formula step 1 (mẫu chữ) và `code=~"5.."` giảng ở step luật cảnh báo (`=~` khớp mẫu, `5..` = mọi mã 500–599); ảnh Docker giảng ở hình chỉ số (gói chương trình đóng sẵn). E52: `bnx_bieu_thuc_chinh_quy` (`introduces` ở formula step 1). KHÔNG đăng ký `term:` cho JSON và Docker: L27, L28 (tác tử khác đang sửa) dùng hai chữ này không `introduces`, đăng ký sẽ làm lint hai bài ấy hỏng; chúng vẫn giảng tại chỗ ở L31 |

### L32 (tác tử nhánh; đã kiểm lại cổng)
| Mục | Kết quả |
|---|---|
| lệnh `vault kv put` (2 phiên bản) | ĐÃ SỬA: khung `export VAULT_ADDR … vault kv put ×2 … echo (kèm -version=1)` hiện ở Bước 4 trước khung chính sách |
| bảng CHINH_SACH | ĐÃ SỬA: hiện ở Bước 5, tách khỏi khung `quyet_dinh` |
| tiêu đề YAML "mặc định KHÔNG xoá" trên `prune: true` | ĐÃ SỬA: "bật cả hai công tắc ở dòng cuối (mặc định đều tắt…)" |
| giảng `*` trong chính sách và `/data/` của KV v2 | ĐÃ SỬA: `s3:Get*` = mọi việc đọc, `bao-cao/*` = mọi tệp trong thư mục; chữ trên màn hình ghi `secret/data/thanh-toan`; lời nói "tự chèn thêm một đoạn vào giữa đường dẫn" (không đọc tên `data` vì chưa dò phát âm) |
| mục tiêu 3 "Chạy" chỉ xem kết quả | ĐÃ SỬA bằng đổi mục tiêu thành "Đọc lệnh và kết quả chạy kho bí mật…" ở `l32.py` và `curriculum/bnx.yaml` (người học không tự chạy được Vault; lệnh và kết quả thật nay hiện đủ); `covers` giữ nguyên |
| P1 bộ cân bằng tải, namespace/manifest | Giảng tại chỗ; E52 `bnx_bo_can_bang_tai` |

### L33 (tác tử nhánh)
| Mục | Kết quả |
|---|---|
| hiện `May.java` (khởi động Tomcat `maxThreads=4`) | ĐÃ SỬA MỘT PHẦN: `May.java` hiện 2 khung (main, dòng 28–47), `Tai.java` hiện 3 khung (thấy `setMaxThreads(4)`). Không hiện `import` và các hàm phụ `lay`, `dem`, `chep`: tệp 49–51 dòng không vừa khung ≤ 12 dòng; màn hình ghi "nằm ở nguồn bài" |
| hiện số ms | KHÔNG đổi sang in số ms, lý do cụ thể: thời gian đo đổi theo từng máy và từng lần chạy, đầu ra phải TẤT ĐỊNH để cổng `screen_code` so được; khung cuối nói rõ "màn hình chỉ in đúng hay sai, số ms thật đổi theo từng máy" (người đọc tái hiện được 243 / 1 360 / 6 190 ms, cùng kết luận) |
| giảng EJB/JTA/EL | Bỏ EL, WebSocket và chữ "đặc tả" khỏi hình 2; giữ "EJB (thành phần doanh nghiệp)", "JTA (giao dịch phân tán)" và giảng bằng lời thường; E52 `bnx_ejb` |
| lab nhắc `LinkedHashMap` | ĐÃ SỬA: `LAB_DE` nhắc `LinkedHashMap` (mục 1, 3), ghi `HashMap` không bảo đảm thứ tự; `loi_giai.java` không đổi |
| Spring Boot (quiz câu 3) | Lời đọc giải thích "bộ khung Java dựng dịch vụ mới" |

### L34 (tác tử nhánh)
| Mục | Kết quả |
|---|---|
| biên 100/500 hook vs mã/quiz | ĐÃ SỬA: hook "không quá 100 / trên 100 đến 500", bảng "≤ 100 / ≤ 500", khớp `tong <= tran` và quiz |
| `tick()` và `CREATE INDEX` | ĐÃ SỬA: chương trình nén 22 dòng, hiện 2 khung (1–10, 11–22), có `create_function("tick", …)`, `CREATE INDEX`, `EXPLAIN QUERY PLAN`; kết quả ở step riêng; kiểm mới ở `ver/l34.py` |
| P1 SQL, kho đọc, bộ đệm, nhóm bên liên quan | Giảng tại chỗ; E52 `bnx_nhom_ben_lien_quan`, `bnx_kho_doc`; `assumes=["bnx_explain"]` (L28 đã giảng, E52 đòi khi `EXPLAIN` hiện trên màn hình) |
| render: tràn khung 29–31 | Rút gọn một đoạn, render sạch |

### L35 (tác tử nhánh)
| Mục | Kết quả |
|---|---|
| hook 3×99,9% vs đáp số 99,7502% | ĐÃ SỬA: hook hỏi 99,9% nối tiếp 99,95% và 99,9% (= 99,7502%), khớp đáp số |
| hình thanh ngân sách sai tỉ lệ, ô thứ tư trống | ĐÃ SỬA: thanh vẽ đúng tỉ lệ (1380 : 138 : 69 : 14 cho 432 : 43,2 : 21,6 : 4,32), chữ nằm cạnh thanh nhỏ; tiêu đề "thanh vẽ đúng tỉ lệ" |
| mục tiêu 2: SLA vs OLA có số | ĐÃ SỬA bằng sửa bài: bảng SLI/SLO/SLA/OLA có số (OLA 99,95% × 99,95% = 0,99900025 ≥ 0,999) |
| mục tiêu 5: ca phân loại sự cố | ĐÃ SỬA bằng sửa bài: 2 ca (tra số dư chậm 15% yêu cầu = P2, báo 09:10 phản hồi trước 09:40; xuất sao kê PDF lỗi = P3, hạn 4 giờ) |
| P1 p95, hàng đợi, Decimal, lỗi độc lập | Giảng tại chỗ (không đăng ký `term:` vì L25/L26 đã dùng "hàng đợi"; p95, Decimal không có ở bài BNX trước) |
| lab ADR | `de.md` có danh mục kiểm (a)(b)(c) và nói `cham.sh` không chấm `.md` |
| trích SRE tiếng Anh ở step 1 | Bỏ (chưa kiểm lại nguyên văn; tiết kiệm lời) |

### L36 (tác tử chính)
| Mục | Kết quả |
|---|---|
| `de.md` làm tròn | ĐÃ SỬA: ghi "trung bình CHƯA làm tròn × hệ số đỉnh, chỉ làm tròn khi in; từ trung bình đã làm tròn ra số khác (×1: 18 thay vì 19)"; gợi ý trên màn hình và lời đọc cùng nói; kiểm mới: 19 / 18 519 vs 18 / 18 518 |
| giả định 10 phút mỗi lệnh lệch | ĐÃ SỬA: ghi chú trên màn hình (500 lệnh một lệch, 100 đồng treo, 10 phút, giờ = số lệch × 10 : 60) và lời đọc; kiểm khớp hằng trong mã |
| 409 vs 422 | ĐÃ SỬA: bảng ký hiệu và bảng Bước 3 (4 kết quả: 409 = yêu cầu cùng khoá còn xử lý dở; 422 = cùng khoá nội dung khác); chương trình in `422: cung khoa, noi dung khac` thay vì "xung dot" |
| Stripe câu 4–5 thêm "For API v1" | ĐÃ SỬA: câu 5 trích đủ cụm "For API v1, Stripe saves…", nhãn nguồn "Stripe, API v1", bản dịch "với API v1…", lời nói "chỉ với phiên bản một"; `sources_l36.md` S4/S5 cập nhật; kiểm nguyên văn 10/10 khớp |
| bốn bước đọc tiếng Anh chỉ áp cho 1 câu | ĐÃ SỬA: step mới áp bốn bước cho câu 3 và câu 4 (bảng 4 bước × 2 câu, bước 4 trỏ về kết quả đã chạy); mục tiêu 6 đổi thành "áp bốn bước vào hai câu và chạy bộ lọc trên cả 10 câu" ở `l36.py` và `curriculum/bnx.yaml` (không hứa 10 câu đều qua 4 bước) |
| P1 sổ cái, hàng đợi, cầu dao, thử lại có lùi, bản sao đọc, chia theo khoá, giao dịch CSDL, mức cô lập, lỗi tuần tự hoá | Giảng tại chỗ lần đầu xuất hiện (sổ cái và hàng đợi ở hình trung tâm thanh toán; cầu dao, thử lại có lùi ở Bước 5; bản sao đọc, chia theo khoá ở Bước 6; giao dịch CSDL ở Bước 4; mức cô lập, lỗi tuần tự hoá ở câu 6–7). Bỏ "sổ cái" khỏi bảng hook (trước khi giảng). E52: `bnx_giao_dich_csdl`, `bnx_ban_sao_doc`, `bnx_chia_theo_khoa`, `bnx_tuan_tu_hoa` |

## 3. P1 dự kiến (tự đánh giá, chưa có người đọc mới)
Mọi thuật ngữ trong cột "Cần biết trước" của báo cáo đã được giảng bằng một câu lời thường (kèm ví dụ nhỏ khi là cú pháp) ở lần đầu xuất hiện trong bài hoặc bỏ khỏi bài; dự kiến P1 = 2 ở cả 6 bài (cần người đọc độc lập xác nhận; chưa có tai người nghe TTS).

## 4. Điểm cần người điều phối biết
- E52 chỉ đăng ký thuật ngữ không bị L24–L30 dùng; JSON, Docker, hàng đợi, chỉ mục, cầu dao, sổ cái, mức cô lập bị L24–L30 dùng nên KHÔNG đăng ký (tránh làm hỏng lint các bài do tác tử khác sửa). Nếu tác tử L24–L30 đăng ký thêm (ví dụ `bnx_cau_dao`) thì L36 (và L32 với "bộ cân bằng tải") cần `assumes` hoặc chạy lại lint L36.
- Chưa dò phát âm bằng ASR cho các từ mới trong lời (đã né tên riêng: "Stripe" bỏ khỏi lời, "EJB", "data" chỉ hiện trên màn hình).
- Chưa kiểm: promtool/Prometheus 3.16.0 và Vault 2.2.2 đã chạy lại thật qua Docker trong `verify_bnx` (PASS); Argo CD, AWS, JBoss/WildFly vẫn không chạy (đã ghi "chỉ giảng/mô phỏng" trên màn hình).
- Tai người và build/tts/asr chưa chạy (điều phối dựng một lần sau).

## 5. Kết quả cổng (số thật, chạy lại một lượt cuối sau khi cả 3 nhánh xong)
- lint L31–L36: 0 FAIL, 0 WARN ở cả 6 bài (31/26/26/31/34/28 PASS).
- render: 0 vấn đề ở cả 6 bài (114/122/118/122/109/123 khung).
- `verify_bnx.py L31…L36`: 128/128 PASS, không SKIP (L31 20/20 gồm Prometheus 3.16.0 thật, L32 Vault 2.2.2 thật).
- `lib2.py gen-screen` mỗi bài: 0 khối chưa khớp; `screen_fast.py L31…L36`: 107 khối, PASS 147 · FAIL 0 · STALE 0 · MISSING 0 · ORPHAN 0.
- `lab_gate.py BNX`: 13 PASS · 0 FAIL (76 lab được bài tham chiếu).
- `lv.py curriculum curriculum/bnx.yaml`: 37 bài, 37 đã có đặc tả, 0 lỗi.
- `audit/check_curricula_graph.py`: 46 lộ trình, 728 bài, tham chiếu hỏng 0, chu trình 0, VER không PASS 0, ví dụ có số không dẫn VER 0.
- `tests/test_e52.py`: 0 FAIL.
- Lời đọc: L31 2 298 · L32 2 284 · L33 2 293 · L34 2 268 · L35 2 287 · L36 2 293 (đều ≤ 2 300).
- Khung PNG đã xem: L31 46, 35, 71; L32 39, 41, 43, 45; L33 22, 44, 63; L34 30, 68, 71; L35 16, 25, 35; L36 33, 64, 78.
