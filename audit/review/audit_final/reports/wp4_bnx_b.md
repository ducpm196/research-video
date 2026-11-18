# WP4 — BNX L12–L23 lên chuẩn AF2 (2026-11-14)

## Sổ tác tử (≤ 4 tác tử cùng lúc: tác tử chính + 2 nhánh + tác tử L00–L11 của người điều phối)
| tác tử | bài | báo cáo riêng |
|---|---|---|
| chính (wp4_bnx_b) | L12, L13, L14, L15 | mục "Tiến độ chính" dưới đây |
| nhánh A | L16, L17, L18, L19 | `wp4_bnx_b_A.md` |
| nhánh B | L20, L21, L22, L23 | `wp4_bnx_b_B.md` |

Công cụ dùng chung mới: `audit/bnx/screen_keep.py Lxx` (sinh lại sổ mã của bài cũ, GIỮ mục viết tay theo sha) — dùng thay `lib2.py gen-screen` cho L12–L23.

## Tiến độ chính
- L12, L13, L14, L15: nguồn viết lại (lib2 + prog + labkit), gen + lint 0/0 + verify PASS + screen_fast PASS; còn chạy cổng chung cuối phần (lab_gate, render lại, curriculum, graph, test_e52, check_*). Chi tiết ở mục cuối báo cáo.

## Chi tiết L12–L15 (tác tử chính)
Hạ tầng thêm: `audit/bnx/screen_keep.py` (sổ mã bài cũ, giữ mục viết tay theo sha), `audit/bnx/src/spk12.py` (ghép câu ngắn), hàm kiểm mới `tools/checklib_bnx/l12..l15.py`, khối `run_wp4` trong `audit/bnx/ver/l12..l15.py`, mục `term:` trong `tools/registry/symbols.BNX.yaml` (L12: tk_dam_bao, chung_tu, kho_bac, so_tham_chieu; L13: dockerfile, cuon_chieu, kho_anh, pod; L14: ngu_canh_gioi_han, ngon_ngu_chung, thung_token; L15 dùng `bnx_be_ket_noi` của L24 bằng `introduces`).

| bài | từ lời đọc | cảnh quy mô (số đo) | lab `labs/BNX/Lxx` |
|---|---|---|---|
| L12 | 2 130 | đối soát chứng từ ở 100 / 10 000 / 1 000 000: vòng lặp lồng 5 050 và 50 005 000 phép so sánh (đo thật), 500 000 500 000 (tính); bảng tra 100 / 10 000 / 1 000 000 lần tra (đo thật) | `mau.py`: chạy lại nhật ký ví (rút thiếu tiền bị từ chối), bất biến, hạn mức 50 triệu |
| L13 | 2 259 | mô phỏng (không phải cụm thật) số đợt cập nhật cuốn chiếu ở 4 / 40 / 400 bản: thiếu 1 thừa 1 = 2, 20, 200 đợt; mặc định 25% = 2 đợt; (0, 40) = 10 đợt; đối chiếu bộ điều khiển mô phỏng theo mã nguồn Kubernetes trên lưới D ≤ 60 | lớp Dockerfile phải dựng lại + số đợt (D = 12; D = 10, 25%) |
| L14 | 2 286 | 1 / 100 / 10 000 bên thứ ba × 30 yêu cầu: qua cổng 10 / 1 000 / 100 000 (cùng lúc), 14 / 1 400 / 140 000 (rải đều); phía sau 2 000/giây (số minh hoạ): 5 ms / 0,5 s / 50 s | thùng token rate 4, cap 6; 50 bên; hàng chờ |
| L15 | 2 236 | cao điểm 116 / 11 574 / 1 157 407 giao dịch/giây: đếm thật lệnh chồng nhau ở Oracle 5 / 463 / 46 297 (Little 4,64; 462,96; 46 296,28); bể 50 kết nối chịu 1 250/giây | ước lượng tải, dư ngân sách, lệnh cùng lúc, số kết nối cần |

Mã trên màn hình: mọi khối Python của L12–L15 là `prog(...)` chạy thật (đầu ra ASCII để chạy được trên Git Bash); Dockerfile/YAML của L13, YAML OpenAPI của L15 giữ mục `other` cũ (docker build --check thật). Pháp lý L12: Nghị định 52/2024 ghi "cần kiểm lại" (CHUA_KIEM), Luật Quản lý thuế 108/2025/QH15 Điều 14 khoản 5 thay luật 2019 từ 01/7/2026 (nguồn tổng hợp, cần kiểm lại), curriculum L12 đã sửa theo. `check_legal.py`: 87 lượt dẫn, 0 FAIL.

Cổng đã chạy (số thật): lint 0 FAIL 0 WARN cả 4 bài (L12 52 PASS, L13 41, L14 56, L15 57); render 0 vấn đề (L12 100 khung, L13 104, L14 105, L15 96); `verify_bnx.py` L12 30/30, L13 24/24, L14 25/25, L15 24/24; `screen_fast` PASS (L12 16, L13 18, L14 9, L15 10 mục); `lab_gate.py BNX` 35 PASS 0 FAIL; `tests/test_e52.py` 0 FAIL; đã xem ≥ 3 khung PNG mỗi bài.

Không làm / lưu ý: Kubernetes, GitLab không chạy thật (nói rõ "mô phỏng"); số 1 000 000 chứng từ ở L12 chỉ tính; thời gian ms/giây của L12, L13, L14 là số minh hoạ tính từ số đếm thật. Không đề xuất tách bài cho L12–L15 (đều ≤ 2 300 từ).

## Tổng hợp cuối (cả 12 bài)
- Nhánh A (L16–L19, từ lời đọc 2 299 / 2 076 / 2 295 / 2 296) và nhánh B (L20–L23, 2 253 / 2 130 / 2 276 / 2 273): chi tiết ở `wp4_bnx_b_A.md`, `wp4_bnx_b_B.md`.
- Cổng chung (toàn BNX): `lab_gate.py BNX` 37 PASS 0 FAIL; `lv.py curriculum curriculum/bnx.yaml` 37 bài 0 lỗi; `check_curricula_graph` 0 hỏng; `test_e52` 0 FAIL; `check_next_refs` 551 lời hẹn 0 lệch; `check_legal` 0 FAIL; `check_course_refs` chỉ còn 2 lỗi R4 ở BNX L00 (ngoài phạm vi; L23 đã sửa, bài sau là L24). Mục tiêu bài = mục tiêu giáo án ở cả 12 bài.
- Đề xuất tách (chưa làm): L17 thành "Spring Security" và "Spring Cloud" (mã Spring chỉ hiện từng đoạn); L19 nếu thêm nội dung.
- Lưu ý: L16 dùng `Thread.sleep` nên nên chạy cổng khi máy nhàn; L20 lab dùng `loi_giai.sh` (cần cài Go); L22 là mô phỏng AEM; L13 mô phỏng Kubernetes.
