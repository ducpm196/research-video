# CS112 phần 2: bốn bài nền tảng bổ sung (2026-10-27)

**Yêu cầu.** Người dùng muốn hoàn thiện giáo án CS112 và CS115 để kiến thức nền tảng thật vững.

**Nhãn bằng chứng:**
- **OBSERVED:** máy chạy hoặc đọc thấy trong phiên này.
- **CITED:** có nguồn tra được.
- **INFERRED:** suy luận.
- **NOT_VERIFIED:** chưa kiểm được.

## 1. Vì sao thêm bài (OBSERVED)

- **Kết quả tìm trong 25 bài CS112 cũ** (`grep -il` trên `lessons/cs112/*.yaml`, 2026-10-27):

  | Từ khoá | Số bài nhắc tới |
  |---|---|
  | Dijkstra, Kruskal, Prim | 0 |
  | quicksort, Bellman-Ford | 0 |
  | union-find, P/NP | 0 |
  | merge (sắp xếp trộn) | 4 |
  | cây B | 2 |

- **Bản thảo** (`audit/cs112/CS112_ban_thao_goc.yaml`) cũng không có các chủ đề này.
- **Vì sao vẫn cần (INFERRED, theo kiến thức chuẩn của môn):**
  - Đây là các chủ đề cốt lõi của mọi môn thuật toán; CLRS dành cho chúng các chương 7–8, 21–24 và 34.
  - Môn tiếp theo như mạng máy tính (định tuyến) và hệ điều hành cần chúng.
- **Quyết định:**
  - Thêm 4 bài mới, đặt ngay trước bài tập lớn.
  - Bài tập lớn L23 thành **L27**, tổng ôn L24 thành **L28**.
  - Đây chính là quy trình đánh số lại trong SKILL Bước 2.

## 2. Bốn bài mới

| Bài | Nội dung | Kiểm chứng (`audit/cs112/verify_cs112_p2.py`) |
|---|---|---|
| L23 | Phân hoạch Lomuto, sắp xếp nhanh, cận dưới log₂ n! bằng cây quyết định, sắp xếp đếm | Q1–Q11: vết phân hoạch; tệ nhất n(n−1)/2 (n = 1..12, cả mảng toàn số bằng nhau); trung bình 2(n+1)H_n − 4n đúng khi vét cạn **mọi** hoán vị n ≤ 7; log₂ n! ≥ (n/2)log₂(n/2) (n ≤ 2000); cây quyết định sinh từ chính thuật toán (`dtree_svg.py`, assert đủ 6 lá, cao 3) |
| L24 | Dijkstra, phản ví dụ cạnh âm, Bellman-Ford, chu trình âm | D1–D7: bảng d sau mỗi lần chốt; vét cạn mọi đường đi đơn; thứ tự cạnh xấu cần đủ n − 1 vòng; phát hiện chu trình âm |
| L25 | Tính chất lát cắt, Kruskal với hợp–tìm, Prim | K1–K8: vét cạn mọi bộ 4 cạnh không chu trình (tổng 11, duy nhất); cây khung nhỏ nhất ≠ cây đường đi ngắn nhất (6 so với 8); nén đường đi |
| L26 | P, NP, chứng chỉ, quy dẫn tập độc lập ↔ phủ đỉnh, NP-đầy đủ, giả đa thức | N1–N5: chứng chỉ TSP dùng lại ma trận của bài 15 (tổng 28, khớp vét cạn); cả 32 tập con của chu trình 5 đỉnh; cái túi 0/1 cho 220; 19! phép thử ≈ 3,9 năm |

**Thư viện tham chiếu.** `tools/checklib.py` là bộ thuật toán tham chiếu dùng trong `checks` dưới tên `alg`. Mục X1 đối chiếu nó với phần cài độc lập và với vét cạn.

**Kết quả chạy lần cuối (OBSERVED):** **37 PASS · 0 FAIL**.

**Lỗi tự bắt khi soạn:**
- **Hai con số kỳ vọng ban đầu ghi sai:**
  - log₂(1000!) ≈ 8529,4, tôi ghi 8530;
  - tổng số so sánh ở bài tự làm L23 là 8, tôi ghi 9.

  Script báo FAIL và tôi đã sửa. Đây là lý do mọi con số phải để máy kiểm.
- **Lời giảng về nén đường đi chưa khớp đoạn mã.**
  - Bản đầu viết mã "nén một nửa" (`cha[x] = cha[cha[x]]`) nhưng lời giảng nói "mọi nút trỏ thẳng về gốc".
  - Check của lint báo FAIL.
  - Đã đổi sang nén trọn vẹn (`cha[x] = find(cha[x])`), cả trong bài lẫn trong `checklib`.

## 3. Phát âm (OBSERVED: `audit/cs112/probes/p5_do_thi.md`)

Mỗi cách viết được nghe 4 ngữ cảnh × 2 mô hình. Ngưỡng nhận là 7/8.

| Từ | Kết quả tốt nhất | Đối chứng âm | Quyết định |
|---|---|---|---|
| NP | “en-pê” 8/8 | “em bê” 0/8 | Luật đọc `NP → en-pê` trong `lexicon_vi.CS112.yaml` |
| Dijkstra | 0/8 với mọi cách viết; máy chép “Dextra”, “Đích Chà”, “Dykstra” | 0/8 | NOT_VERIFIED |
| Kruskal | 5/8 (“Cơ-rút-can”) | 0/8 | NOT_VERIFIED |
| Prim | 3/8; máy chép “phim” | 0/8 | NOT_VERIFIED |
| Bellman | thô 6/8; “Beo-man” 8/8 nhưng là cách đọc lạ | 0/8 | NOT_VERIFIED |

Với các tên NOT_VERIFIED, tên **chỉ hiện trên màn hình**, còn lời đọc dùng tên mô tả. CS115 L39 đã làm như vậy với Bellman:
- “thuật toán chốt đỉnh gần nhất”;
- “thuật toán nới mọi cạnh n trừ 1 vòng”;
- “xét cạnh từ nhẹ đến nặng”;
- “mở rộng cây từ một đỉnh”.

## 4. Đánh số lại

| Bài cũ | Bài mới | Việc đã làm |
|---|---|---|
| L23 bài tập lớn | **L27** | `git mv` file bài; sửa `id`, tiêu đề; sửa câu nhắc bài sau “bài 24” thành “bài 28” |
| L24 tổng ôn | **L28** | `git mv` file bài; sửa `id`, tiêu đề |

**Các chỗ sửa thêm:**
- **L22:** câu nhắc bài sau đổi từ “bài 23: bài tập lớn” thành “bài 23: sắp xếp nhanh”.
- **L28 (tổng ôn):**
  - thêm nhóm ⑥ (sắp xếp, đồ thị, độ khó) và 4 bẫy mới (16–19);
  - “hai mươi bốn bài, năm nhóm” thành “hai mươi tám bài, sáu nhóm”;
  - “mười lăm bẫy” thành “mười chín bẫy”.
- **Video cũ:** `out/CS112/L23`, `L24` chuyển sang `out/_stale_renumber_2026-10-27/`, không xoá.
- **Kiểm:** `lv.py curriculum curriculum/cs112.yaml` báo 29 bài, 0 lỗi (OBSERVED, 2026-10-27T09:05Z).

## 5. NOT_VERIFIED

- **Năm công bố:** Hoare 1961, Dijkstra 1959, Bellman 1958, Ford 1956, Kruskal 1956, Prim 1957, Tarjan 1975, Cook 1971, Karp 1972, Khachiyan 1979, Clay 2000.
  - Đây là kiến thức chuẩn, tôi ghi theo trí nhớ và chưa tra lại nguồn trong phiên này.
  - Các năm này hiện trên màn hình. Nên đối chiếu với CLRS trước khi phát hành.
- **Hiệu quả sư phạm** của 4 bài mới với người học thật: chưa thử.

## 6. Dựng, máy nghe lại, xem bằng mắt (OBSERVED, 2026-10-27)

- **Dựng:** L23–L28 và L22 đều verify PASS. Thời lượng: L23 9,9 phút, L24 8,9, L25 7,0, L26 8,7, L27 6,9, L28 7,1. Toàn khoá 29 bài, 206,0 phút.
- **Giọng đọc bị từ chối:** dịch vụ từ chối 4/90 câu của L23 (“No audio received”). Hàng đợi chờ 1 giờ theo yêu cầu người dùng rồi đọc lại được hết.
- **Máy nghe lại (ASR):** mọi câu gắn cờ đều có lý do.
  - Phần lớn là lỗi chép đã biết của máy nghe: Theta thành “teta”, lôgarit thành “logarith”, tên chữ cái d, w, b.
  - Một câu quá ngắn được viết lại: “Đến lượt bạn.” ở L26.
  - NOT_VERIFIED, cần người nghe: “cận dưới … giai thừa” ở L23 và “Bẫy mười sáu” ở L28 (máy chép thành “76”, cùng lỗi bẫy/bảy đã gặp).
- **Xem bằng mắt:** khoảng 30 khung có hình, bảng hoặc khối mã. Đã sửa 2 lỗi:
  - L24 khung 41: cột chữ quá hẹp, dấu “).” rớt xuống một dòng riêng.
  - L23 khung 43: câu nói về lá cây quyết định lại làm mờ hình cây.
- **Lỗi quy trình đã gặp:** bài sinh từ mẫu `src/*.tpl.yaml` bị ghép lại sau khi đã ghi `asr_reviewed` vào bài, nên mất các ghi chú đó. Cách sửa: ghi chú máy nghe được chép cả vào mẫu, và mẫu là nguồn duy nhất.

Kiểm cuối `checked_at=2026-10-27T11:54Z`:

| Mục | Kết quả |
|---|---|
| CS112 verify | 29/29 PASS |
| CS112 lint | 0 FAIL, 0 WARN |
| CS112 lộ trình | 29 bài, 0 lỗi |
| CS112 focus | 289/289 |
| CS115 verify | 45/45 PASS (thêm L44) |
| CS115 lộ trình | 45 bài, 0 lỗi |
| CS115 focus | 623/623 |
| tests | 0 FAIL |
| Dòng đầu trang | không xuống dòng ở 74/74 bài |
| ASR | 0 câu gắn cờ chưa xem xét ở cả hai khoá |
