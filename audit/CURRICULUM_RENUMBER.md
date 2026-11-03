# Đánh số lại lộ trình CS115 & luật trích dẫn bài khác — 2026-10-24

Yêu cầu của người dùng:
- Số thứ tự bài phải tịnh tiến, dễ nắm bắt.
- Bổ sung bài còn thiếu.
- Không nhắc bài sau một cách khó hiểu. Nhắc bài trước phải nói lại rõ ràng.

Nhãn: OBSERVED = chạy hoặc đọc trong phiên này; INFERRED = suy luận.

## 1. Bảng đổi số (số hiệu = thứ tự học)

| Mới | Cũ | Bài |
|---|---|---|
| L00–L08 | L00–L08 | không đổi (Bức tranh lớn … Gradient Descent) |
| L09 | L17 | Nesterov, Adagrad, RMSprop, Adadelta |
| L10 | L18 | Tối ưu lồi & phương pháp Newton |
| **L11** | — | **mới:** hàm mũ eˣ & logarit |
| L12 | L09 | Xác suất rời rạc (thêm định lý Bayes) |
| **L13** | — | **mới:** biến liên tục, hàm mật độ, phân phối chuẩn một chiều |
| L14 | L10 | Phân phối chuẩn nhiều chiều & hiệp phương sai |
| L15 | L11 | SVD & PCA |
| L16 | L12 | MLE, MAP, Bayes |
| L17 | L13 | Hồi quy tuyến tính |
| L18 | L19 | Quá khớp, L1/L2, cross-validation |
| L19 | L14 | Logistic, Softmax, Cross-Entropy |
| L20 | L15 | Đồ thị tính toán & lan truyền ngược |
| L21 | L20 | MLP, Batch normalization, hyperparameters |
| L22 | L21 | Lagrange & KKT |
| L23 | L22 | SVM |
| L24 | L23 | LDA |
| **L25** | — | **mới:** KNN |
| L26 | L24 | Phân cụm |
| L27 | L25 | GMM & EM |
| L28 | L26 | Cây quyết định |
| L29 | L16 | Tổng ôn |

Kiểm bằng máy (OBSERVED):
- `lv.py curriculum curriculum/cs115.yaml` → `30 bài, 6 đã có đặc tả, 0 lỗi` (03:55:29Z).
- Từ nay công cụ còn chặn số hiệu không tịnh tiến hoặc bị trùng.

## 2. Vì sao thêm 3 bài (bằng chứng: `grep` trên tex, OBSERVED 03:5xZ)

| Bài | Chỗ hổng | Dòng tex dùng mà chưa bài nào dạy |
|---|---|---|
| L11 Hàm mũ & logarit | Đạo hàm của eˣ và ln; ln biến tích thành tổng | exp: 300, 301, 324, 346, 351; ln/log: 325, 327, 348 |
| L13 Biến liên tục, mật độ | Xác suất = diện tích dưới mật độ; tích phân hiểu theo trực giác; mật độ có thể lớn hơn 1 | Mật độ chuẩn: 300; tích phân: 317 |
| L25 KNN | KNN có trong bảng tổng kết nhưng chưa bài nào dạy | 405 (A14) |

Không thêm:
- t-SNE: không có trong nguồn nào.
- NMF: chỉ có ở slide 2024. Đây là **quyết định mở cho người dùng**.

## 3. Luật trích dẫn bài khác (pedagogy.md luật 17; lint E22–E23)

- **E22 (FAIL):** “bài N” mà lộ trình không có bài đó.
- **E22 (FAIL):** nhắc bài sau mà step chưa có `forward_ref: true`.
- **E22 (WARN):** nhắc bài sau giữa phần giảng, tức không nằm trong hook/in_ai/recap.
- **E23 (WARN):** nhắc bài trước mà sau khi bỏ cụm “(như/theo/ở) bài N”, câu còn dưới 6 từ.
- Có test cho cả 4 trường hợp trên trong `tests/test_lint.py`.
- Giới hạn của máy: lint không biết số đúng chủ đề hay không, cũng không biết lời giải thích có đủ dễ hiểu không. Hai việc đó phải đọc lại bằng người (mục 4).

## 4. Rà soát L01–L06 (đọc từng chỗ)

**Trước khi sửa** (OBSERVED, 03:52Z): 60 lần nhắc bài sau và 84 lần nhắc bài trước, tính cả bảng lẫn lời đọc. Lint mới báo 25 step nhắc bài sau thiếu đánh dấu. Ba kiểu lỗi:
1. **Nhắc bài sau giữa phần giảng, làm đứt mạch** (7 step):
   - L02 “định thức… sẽ học kỹ ở các bài sau”;
   - L04 verify “dùng ở bài 11”;
   - L05 “điểm dừng (bài 7)”, “bài 7 chứng minh…”;
   - L06 “(bài 7)” ở 3 chỗ, “bài 7 sẽ dùng điều này”.

   Sửa: nói trọn ý tại chỗ, bỏ số bài.
2. **Thuật ngữ người học chưa biết:**
   - L04 (học *trước* đạo hàm) nói “ma trận đạo hàm cấp 2”, “ma trận hiệp phương sai”, “cực tiểu”.
   - L01 nhắc Gram-Schmidt, PCA, hồi quy trống không.
   - L06 kể “hàm mũ” trong các hàm trơn (bài 11 mới dạy).
   - L06 nói “tiêu chuẩn Sylvester”, “yên ngựa”.

   Sửa: giải thích bằng lời thường, ví dụ “ma trận mô tả độ cong”, “PCA, một cách nén dữ liệu”, “yên ngựa: lên theo hướng này, xuống theo hướng kia”.
3. **Số bài sai sau khi đánh số lại:** 11 → 15, 13 → 17, 15 → 20, 18 → 10.
4. **Nhắc bài trước nói tắt** (7 câu):
   - L06 “Bài 5 đã có gradient.”
   - L03 “theo đúng công thức của bài 1”, “theo định nghĩa ở bài 2”.
   - L04 “Công cụ cần dùng đều có ở bài 2.”, “Ôn lại ba công cụ của bài 2.”
   - L05 “xét trị riêng như bài 4”.
   - L02 “cái bóng của bài 1”.

   Sửa: nói lại nội dung, ví dụ “theo công thức cái bóng của bài 1, tức tích vô hướng chia cho độ dài bình phương”.

**Sau khi sửa** (OBSERVED):
- Lint 0 FAIL, 0 WARN cả 6 bài (04:00–04:01Z).
- Nhắc bài sau chỉ còn trong hook/in_ai/recap: 17 step, tất cả có `forward_ref: true` (`grep -c`: L01 1, L02 2, L03 1, L04 5, L05 4, L06 4).
- Quét thuật ngữ của bài sau trong thân bài: chỉ còn L02 example.4, câu “ý tưởng của hồi quy tuyến tính, học trọng số từ dữ liệu”, đã tự giải thích nên giữ.

Script sửa (scratchpad, áp dụng 1 lần; mỗi thay thế phải khớp đúng 1 lần): `refs_fix.py`, `refs_fix2.py`. Bản sao trước khi sửa: `bak_L0*.yaml`.

## 5. Lỗ hổng L00 (người dùng phát hiện, 2026-10-24 ~11:10Z)

- **Hiện trạng trước khi sửa** (OBSERVED 11:11Z): `curriculum/cs115.yaml` có `L00` (bức tranh lớn) nhưng không có `spec`; `lessons/` chỉ có L01–L07; `out/` không có `L00`. Lệnh `curriculum` vẫn báo `0 lỗi` vì chỉ đếm số bài có spec.
- Không bài nào trong L01–L07 nhắc tới “bài 0” (`grep -n "bài 0\|L00" lessons/*.yaml`: 0 kết quả); L01 có `assumes: []` và tự dạy lại từ đầu → thiếu L00 không làm sai lời đọc của L01–L07, chỉ làm thiếu bài mở đầu.
- **Sửa:** viết `lessons/L00_buc_tranh_lon.yaml` (chỉ số học phổ thông; ký hiệu mới: `·`, `ŷ`; sửa A7 bằng ví dụ 2 ngôi nhà: sai số tổng nhỏ nhất 4/61 > 0); gắn `spec` trong lộ trình.
- **Chặn tái phát:** `lv.py curriculum` báo lỗi khi một bài đứng trước bài cuối đã làm mà thiếu `spec`, khi `spec` không tồn tại, hoặc khi `id` trong spec khác lộ trình. Đối chứng dương: chạy trước khi gắn spec L00 → `[FAIL] L00 chưa có đặc tả (spec) dù các bài sau nó đã làm` (11:22:33Z); sau khi gắn → `30 bài, 8 đã có đặc tả, 0 lỗi` (11:22:40Z). Ca thử cố định trong `tests/test_lint.py`.
- Bảng “bản đồ khoá học” trong L00 (scene `in_ai_map`) đối chiếu từng `title` của lộ trình: bài 1–4 và 15 (biểu diễn), 5–10 (tự sửa), 11–14 và 16 (hàm mũ, logarit, xác suất), 17–19 (mô hình đầu tiên, đo sai số), 20–28 (mạng nơ-ron, mô hình khác, công cụ toán), 29 (tổng ôn).

## 6. Đánh số lại lần 2 → bản 3 (34 bài, L00–L33) — 2026-10-24 ~13:00Z

Lý do (bằng chứng ở `audit/SYLLABUS_CS115.md` §6): thêm **L03 hệ phương trình tuyến tính** (LA24, BT1; bài 4, 5, 8 dùng giải hệ mà chưa bài nào dạy), **L21 đánh giá mô hình phân loại** (ML24), **L31 NMF** và **L32 t-SNE** (người dùng yêu cầu); dời cây quyết định lên L28 để gom các mô hình có giám sát.

| Bản 2 (`prev`) | Bản 3 | | Bản 2 | Bản 3 |
|---|---|---|---|---|
| L00–L02 | L00–L02 | | L20 backprop | L22 |
| — | **L03 hệ phương trình** | | L21 MLP | L23 |
| L03–L19 | L04–L20 (+1) | | L22 Lagrange/KKT | L24 |
| — | **L21 đánh giá phân loại** | | L23 SVM | L25 |
| L26 phân cụm | L29 | | L24 LDA | L26 |
| L27 GMM/EM | L30 | | L25 KNN | L27 |
| L28 cây quyết định | L28 | | — | **L31 NMF**, **L32 t-SNE** |
| L29 tổng ôn | L33 | | | |

Ánh xạ số trong lời đọc (kiểm bằng `assert` trong `scratchpad/renum_v3.py`): ≤2 giữ; 3–19 → +1; 20–25 → +2; 26 → 29; 27 → 30; 28 → 28; 29 → 33.

**Đã làm** (OBSERVED):
- Đổi tên file `lessons/L03…L07` → `L04…L08` (`git mv` cho file đã theo dõi), `out/L03…L07` → `out/L04…L08`; `id` và tiêu đề “Bài N —” đổi theo.
- `renum_v3.py` đổi 106 dòng “bài N” ở L01, L02, L04–L08 (in từng dòng ra `renum_v3.log`); **đọc lại từng dòng**: mọi số mới khớp chủ đề trong `title` của lộ trình.
- **Lỗi bắt được khi đọc lại**: câu cuối L02 “Bài sau … Gram-Schmidt” vẫn trỏ bài cũ (không có số nên phép thay không chạm tới). Đã viết lại thành giới thiệu bài 3 hệ phương trình. Kiểm tay các câu “bài sau” không số của mọi bài: chỉ L02 sai.
- Sửa tay L00 (bản đồ khoá học có khoảng số: 1–5, 6–11, 12–15 và 17, 18–21, 22–32, 33), L04 (hook nhắc phép khử của bài 3).
- **Chặn tái phát: lint E24** — “bài sau (bài N)” phải là N = bài hiện tại + 1 (FAIL); câu về “bài sau” phải có ít nhất một cụm hai từ trong tên bài kế tiếp, bỏ các cụm có trong ≥ 3 tên bài (WARN). Đối chứng dương: L02 bản 2 (`bak_v2/`) → 1 cảnh báo E24; bản đã sửa → 0. Lần thử đầu (chưa lọc cụm chung) **không** bắt được vì “ma trận” trùng — đã sửa. Ca thử cố định trong `tests/fixtures/bad_lesson.yaml`.
- Các file `audit/REVIEW_L01…L07.md`, `REVIEW_L00.md` giữ số hiệu tại thời điểm viết (lịch sử); tra cứu bằng `orig`/`prev` trong curriculum.
