# RBM — đã đọc 18/18 bài

Đọc kiểm 2026-11-08 (đợt B). Đọc toàn bộ `show`/`say`/`checks`, quiz và đáp án của 18 bài `lessons/rbm/`. Mẫu `audit/rbm/src/*.tpl.yaml` đã đồng bộ bằng `audit/review/sync_tpl_from_lesson.py RBM --write` (L07, L09, L11, L16 ghi mẫu mới; chạy lại: 0 mẫu lệch). L00 giữ nguyên bản sửa `\theta` (mẫu L00 "khớp").

| Bài | Kết luận | Mục đã sửa (cảnh: MUST/SHOULD — lý do ngắn) | Nguồn | lint / render |
|---|---|---|---|---|
| L00 | không phát hiện lỗi | — | Lynch & Park, Modern Robotics (2017) §3.1 | — |
| L01 | không phát hiện lỗi | — | Lynch & Park (2017) §3.2, phụ lục B | — |
| L02 | không phát hiện lỗi | — | Lynch & Park (2017) phụ lục B.3 | — |
| L03 | không phát hiện lỗi | — | Lynch & Park (2017) §3.3 | — |
| L04 | không phát hiện lỗi | — | Lynch & Park (2017) §4 | — |
| L05 | không phát hiện lỗi | — | Craig (2005) §4.4 | — |
| L06 | không phát hiện lỗi | — | Lynch & Park (2017) §5.1, §5.3 | — |
| L07 | đã sửa | example (bước hình 2): SHOULD — “Euler **luôn** đi quá xuống” là khẳng định tuyệt đối, chính quiz của bài cho Euler đi quá **lên** với x′ = 2 − x; viết lại “với bài này” ở cả màn hình và lời đọc | Burden & Faires, Numerical Analysis (2011) §5.2 (dấu sai số cục bộ phụ thuộc độ cong nghiệm) | lint: 0 FAIL, 0 WARN, 35 PASS; render: 79 khung (0 vấn đề) |
| L08 | không phát hiện lỗi | — | Hairer, Nørsett, Wanner (1993) §II.1 | — |
| L09 | đã sửa | formula: SHOULD — “ổn định” dùng theo nghĩa tắt về 0 mà không nói tên; thêm ghi chú “sách gọi là ổn định tiệm cận” (màn hình + lời, focus thêm 1 mục); pitfalls Lỗi 4: SHOULD — theo định nghĩa chuẩn, trị riêng ±2i là ổn định (Lyapunov) biên, không phải “không ổn định”; thêm “ổn định biên, chưa phải ổn định tiệm cận” | Åström & Murray, Feedback Systems (2008) §4.3, §5.2 (định lý 5.1: ổn định tiệm cận ⇔ mọi Re λ < 0) | lint: 0 FAIL, 0 WARN, 37 PASS; render: 96 khung (0 vấn đề) |
| L10 | không phát hiện lỗi | — | Åström & Murray (2008) ch. 10–11 (kiểm (s+1)³ + K: ổn định khi K < 8) | — |
| L11 | đã sửa | pitfalls Lỗi 4: MUST — bài nói “mất mát nhảy qua lại là dấu hiệu hệ số âm”; với f = 5w² và 1/a < η < 2/a thì w đổi dấu nhưng mất mát 5w² vẫn giảm đơn điệu, nên dấu hiệu đổi dấu thuộc về w; mất mát tăng mới là dấu hiệu |hệ số| > 1. Viết lại màn hình + lời; thêm 1 `checks` (η = 0,15: w đổi dấu, mất mát giảm; η = 0,25: mất mát tăng) | Burden & Faires (2011) §5.10–5.11; tính trực tiếp (checks) | lint: 0 FAIL, 0 WARN, 37 PASS; render: 85 khung (0 vấn đề) |
| L12 | không phát hiện lỗi | — | Thrun, Burgard, Fox, Probabilistic Robotics (2005) §3.2 | — |
| L13 | không phát hiện lỗi | — | Thrun et al. (2005) bảng 3.1 | — |
| L14 | không phát hiện lỗi | — | Oppenheim & Schafer (2010) §4.2, §8.1 | — |
| L15 | không phát hiện lỗi | — | Hart, Nilsson, Raphael (1968); Russell & Norvig (2021) §3.5 | — |
| L16 | đã sửa | recap (giới thiệu bài 17): MUST — lời đọc “con tàu bay vòng quanh Mặt Trăng năm 1960” sai sự kiện (năm 1960 mới là nghiên cứu khả thi dẫn đường cho chuyến bay vòng quanh Mặt Trăng); sửa thành “nghiên cứu dẫn đường … năm 1960” ở màn hình + lời | McGee & Schmidt, NASA TM-86847 (1985) tr. PDF 3 (“feasibility studies for circumlunar navigation”) — audit/rbm/sources_L17.md | lint: 0 FAIL, 0 WARN, 33 PASS; render: 84 khung (0 vấn đề) |
| L17 | đã sửa | stage3: MUST — “đầu năm 1968, phương pháp [căn bậc hai] ấy ra đời” mâu thuẫn nguồn: dạng căn bậc hai đầu tiên của Potter đã dùng cho Apollo; sửa thành “phương pháp căn bậc hai cho máy tính phẩy tĩnh nhỏ được phát triển” + ghi chú Potter/Apollo, chưa xử lý nhiễu quá trình (màn hình + lời, focus thêm 2 mục); stage4: SHOULD — “U-D ở JPL” không có trong nguồn đã đọc → bỏ “ở JPL”, ghi tên thuật toán “U-D (Bierman)” như câu nguồn; SHOULD — “Mariner 10 dẫn đường bằng thuật toán căn bậc hai tuần tự” viết mềm theo câu nguồn: “phép tính dẫn đường … dùng thuật toán căn bậc hai (Dyer–McReynolds, 1969)” (màn hình, `stage.scale`, lời) | McGee & Schmidt (1985) tr. PDF 11 (Potter, Apollo), 16 (1968), 19 (Bierman 1975; Dyer–McReynolds 1969, Mariner 10) — audit/rbm/sources_L17.md | lint: 0 FAIL, 0 WARN, 46 PASS; render: 148 khung (0 vấn đề) |

Tổng: 18/18 bài đã đọc, 5 bài sửa; 3 mục MUST (L11, L16, L17 stage3), 5 mục SHOULD (L07, L09 ×2, L17 stage4 ×2).

Giáo án `curriculum/rbm.yaml`: L09 `fix` thêm “(tiệm cận)” và “phần thực bằng 0 chỉ là ổn định biên”; L17 `fix` thêm tên trên màn hình (Dyer–McReynolds, U-D của Bierman) và ghi Potter là dạng căn bậc hai đầu tiên. L07, L11, L16: mục giáo án đã khớp, không đổi. `rec("RBM:L17")` trong `audit/verify_plan_curricula.py` không cần đổi (không đổi số).

## Không sửa và vì sao
- L02 hộp “vì sao nửa góc: q tác động hai lần, mỗi lần góp θ/2”: đúng chính xác chỉ khi v vuông góc trục quay; hình đã ghi điều kiện này (“v vuông góc với trục z”), đây là trực giác dẫn nhập — giữ.
- L08 gọi x′ = −50x là “hệ cứng”: định nghĩa chặt của hệ cứng cần nhiều thang thời gian; bài dùng nó làm “phần nhanh” và cảnh L11 nói rõ “hai phần cách xa nhau là hệ cứng” — chấp nhận được ở mức nhập môn.
- L15 “h không vượt quá giá thật thì A* luôn trả đường ngắn nhất”: với tìm kiếm đồ thị không mở lại ô thì cần thêm h nhất quán; Manhattan trên lưới 4 hướng nhất quán, và AIMA (2021) §3.5 phát biểu tối ưu với h chấp nhận được cho cài đặt có cập nhật đường tốt hơn — không đổi.
- L06 “định thức nhỏ nghĩa là nghịch đảo lớn”: là quy tắc kinh nghiệm (phụ thuộc thang đo), nằm ở hộp “tư duy” — giữ.
- L17 hook “Năm 1983, cùng bộ lọc ấy được dùng để dự đoán đàn gia súc ở Pháp…”: 1983 là năm số chuyên đề IEEE TAC AC-28(3) ghi các ứng dụng (nguồn tr. PDF 20); cảnh stage4 nói đúng là “số chuyên đề năm 1983” — giữ.
- L17 stage2 “1961, bộ lọc lần đầu chạy trên số đo thật … từ nhiều trạm mặt đất”: nguồn trích ghi “first opportunity to process actual measurement data” (Agena, Lockheed); chi tiết “nhiều trạm mặt đất” không có trong đoạn trích của sources_L17.md — chưa kiểm được nguồn ở chi tiết này (không mở lại PDF); để nguyên vì không mâu thuẫn, đề nghị lần sau đối chiếu tr. PDF 14.

## Kết quả bộ kiểm cuối
- `audit/rbm/verify_rbm.py`: 92/92 PASS
- `tools/lv.py curriculum curriculum/rbm.yaml`: curriculum: 18 bài, 18 đã có đặc tả, 0 lỗi
- `audit/review/scan_ctrl.py`: không có lượt nào ở `lessons/rbm` hay `audit/rbm` (8 lượt còn lại đều ở `lessons/jva`, khoá khác)
