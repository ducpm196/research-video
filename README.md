# research-video — xưởng video giảng giải cho người mới / mất gốc: AI, khoa học máy tính, dữ liệu, công nghệ thông tin

Chương trình gồm 38 khoá, 575 bài, chia 8 tầng từ toán nền tới tình huống chuyên gia.
Xưởng dùng chung được cho chủ đề khác qua **hồ sơ chuyên ngành** (`tools/profiles/`): STEM (mặc định), ngoại ngữ, kỹ năng mềm,
xã hội–đời sống–triết học, phân tích phim, video giới thiệu sản phẩm có tiếp thị liên kết. Mỗi hồ sơ có một bài mẫu có nguồn ở
`examples/profiles/`. Kiến trúc mã: [`tools/README.md`](tools/README.md); cách dùng: `.claude/skills/lecture-video/references/profiles.md`.
- Kiến trúc chương trình và tầm nhìn: [`curriculum/ROADMAP.md`](curriculum/ROADMAP.md).
- Hiện trạng từng khoá, sinh tự động: [`curriculum/STATUS.md`](curriculum/STATUS.md).
- Lộ trình theo nghề, sinh tự động: [`curriculum/TRACKS.md`](curriculum/TRACKS.md).

Video của mọi khoá nằm ở `out/<KHOÁ>/<id>/<id>.mp4`, kèm `<id>.srt` (phụ đề), `chapters.txt` (mục lục) và `preview.html` (duyệt nhanh bằng ←/→, không cần mạng).
Đặc tả bài ở `lessons/<khoá>/`, lộ trình ở `curriculum/<khoá>.yaml`. Mỗi bài ghi khoá trong trường `course`; không ghi thì là CS115.
Mở một chuyên ngành mới: `.venv/Scripts/python tools/lv.py new-course <KHOÁ> --title "…" [--profile language|softskill|humanities|film|affiliate]`, rồi làm theo `.claude/skills/lecture-video/references/new-domain.md`.

## CS115

| Bạn muốn | Mở / chạy |
|---|---|
| Xem video bài 0 (bức tranh lớn: 4 bước AI tự học, bài mở đầu) | `out/CS115/L00/L00.mp4` (+ `out/CS115/L00/L00.srt`, `out/CS115/L00/chapters.txt`) |
| Xem video bài 1 | `out/CS115/L01/L01.mp4` (+ phụ đề `out/CS115/L01/L01.srt`, mục lục `out/CS115/L01/chapters.txt`) |
| Xem video bài 2 (ma trận) | `out/CS115/L02/L02.mp4` (+ `out/CS115/L02/L02.srt`, `out/CS115/L02/chapters.txt`) |
| Xem video bài 3 (hệ phương trình tuyến tính: phép khử, hạng) | `out/CS115/L03/L03.mp4` (+ `out/CS115/L03/L03.srt`, `out/CS115/L03/chapters.txt`) |
| Xem video bài 4 (trực chuẩn, Gram-Schmidt) | `out/CS115/L04/L04.mp4` (+ `out/CS115/L04/L04.srt`, `out/CS115/L04/chapters.txt`) |
| Xem video bài 5 (trị riêng, vector riêng) | `out/CS115/L05/L05.mp4` (+ `out/CS115/L05/L05.srt`, `out/CS115/L05/chapters.txt`) |
| Xem video bài 6 (đạo hàm, đạo hàm riêng, gradient) | `out/CS115/L06/L06.mp4` (+ `out/CS115/L06/L06.srt`, `out/CS115/L06/chapters.txt`) |
| Xem video bài 7 (Jacobian, Hessian, quy tắc chuỗi) | `out/CS115/L07/L07.mp4` (+ `out/CS115/L07/L07.srt`, `out/CS115/L07/chapters.txt`) |
| Xem video bài 8 (tìm cực trị: điểm dừng, độ cong, tiêu chuẩn định thức con) | `out/CS115/L08/L08.mp4` (+ `out/CS115/L08/L08.srt`, `out/CS115/L08/chapters.txt`) |
| Xem video bài 9 (Gradient Descent, SGD, Momentum, Adam) | `out/CS115/L09/L09.mp4` (+ `out/CS115/L09/L09.srt`, `out/CS115/L09/chapters.txt`) |
| Xem video bài 10 (tối ưu thích nghi: Nesterov, Adagrad, RMSprop, Adadelta, Adam) | `out/CS115/L10/L10.mp4` (+ `out/CS115/L10/L10.srt`, `out/CS115/L10/chapters.txt`) |
| Xem video bài 11 (tối ưu lồi & Newton; ba cách thay thế khi Hessian quá đắt: tựa Newton, gradient liên hợp, Levenberg-Marquardt) | `out/CS115/L11/L11.mp4` (+ `out/CS115/L11/L11.srt`, `out/CS115/L11/chapters.txt`) |
| Xem video bài 12 (hàm mũ eˣ & lôgarit: tính chất, đạo hàm) | `out/CS115/L12/L12.mp4` (+ `out/CS115/L12/L12.srt`, `out/CS115/L12/chapters.txt`) |
| Xem video bài 13 (Xác suất rời rạc: có điều kiện, định lý Bayes, kỳ vọng, phương sai) | `out/CS115/L13/L13.mp4` (+ `out/CS115/L13/L13.srt`, `out/CS115/L13/chapters.txt`) |
| Xem video bài 14 (Biến ngẫu nhiên liên tục, hàm mật độ & phân phối chuẩn một chiều) | `out/CS115/L14/L14.mp4` (+ `out/CS115/L14/L14.srt`, `out/CS115/L14/chapters.txt`) |
| Xem video bài 15 (Phân phối chuẩn nhiều chiều & ma trận hiệp phương sai) | `out/CS115/L15/L15.mp4` (+ `out/CS115/L15/L15.srt`, `out/CS115/L15/chapters.txt`) |
| Xem video bài 16 (SVD & PCA: nén dữ liệu bằng cái bóng dài nhất) | `out/CS115/L16/L16.mp4` (+ `out/CS115/L16/L16.srt`, `out/CS115/L16/chapters.txt`) |
| Xem video bài 17 (Ước lượng tham số: MLE, MAP, Bayes) | `out/CS115/L17/L17.mp4` (+ `out/CS115/L17/L17.srt`, `out/CS115/L17/chapters.txt`) |
| Xem video bài 18 (Hồi quy tuyến tính, hàm MSE & nghiệm đóng (normal equation)) | `out/CS115/L18/L18.mp4` (+ `out/CS115/L18/L18.srt`, `out/CS115/L18/chapters.txt`) |
| Xem video bài 19 (Quá khớp, chính quy hoá L1/L2 (Lasso, Ridge) & cross-validation) | `out/CS115/L19/L19.mp4` (+ `out/CS115/L19/L19.srt`, `out/CS115/L19/chapters.txt`) |
| Xem video bài 20 (Logistic, Softmax & Cross-Entropy (vì sao không dùng MSE)) | `out/CS115/L20/L20.mp4` (+ `out/CS115/L20/L20.srt`, `out/CS115/L20/chapters.txt`) |
| Xem video bài 21 (Đánh giá mô hình phân loại: ma trận nhầm lẫn, accuracy, precision, recall, F1) | `out/CS115/L21/L21.mp4` (+ `out/CS115/L21/L21.srt`, `out/CS115/L21/chapters.txt`) |
| Xem video bài 22 (Đồ thị tính toán & lan truyền ngược (backpropagation)) | `out/CS115/L22/L22.mp4` (+ `out/CS115/L22/L22.srt`, `out/CS115/L22/chapters.txt`) |
| Xem video bài 23 (Mạng perceptron nhiều lớp (MLP): hàm kích hoạt, khởi tạo, Batch normalization & hyperparameters) | `out/CS115/L23/L23.mp4` (+ `out/CS115/L23/L23.srt`, `out/CS115/L23/chapters.txt`) |
| Xem video bài 24 (Tối ưu có ràng buộc: nhân tử Lagrange & điều kiện KKT (cầu nối sang SVM)) | `out/CS115/L24/L24.mp4` (+ `out/CS115/L24/L24.srt`, `out/CS115/L24/chapters.txt`) |
| Xem video bài 25 (Support Vector Machine: lề lớn nhất, hinge loss & kernel) | `out/CS115/L25/L25.mp4` (+ `out/CS115/L25/L25.srt`, `out/CS115/L25/chapters.txt`) |
| Xem video bài 26 (Phân tích phân biệt tuyến tính (LDA) — tiêu chí Fisher) | `out/CS115/L26/L26.mp4` (+ `out/CS115/L26/L26.srt`, `out/CS115/L26/chapters.txt`) |
| Xem video bài 27 (K láng giềng gần nhất (KNN): học lười, khoảng cách L1/L2, chọn K) | `out/CS115/L27/L27.mp4` (+ `out/CS115/L27/L27.srt`, `out/CS115/L27/chapters.txt`) |
| Xem video bài 28 (Cây quyết định & rừng ngẫu nhiên (entropy, chỉ số Gini)) | `out/CS115/L28/L28.mp4` (+ `out/CS115/L28/L28.srt`, `out/CS115/L28/chapters.txt`) |
| Xem video bài 29 (Phân cụm: K-Means, phân cụm phân cấp & phân cụm phổ (ma trận Laplacian)) | `out/CS115/L29/L29.mp4` (+ `out/CS115/L29/L29.srt`, `out/CS115/L29/chapters.txt`) |
| Xem video bài 30 (Mô hình hỗn hợp Gauss (GMM) & thuật toán EM) | `out/CS115/L30/L30.mp4` (+ `out/CS115/L30/L30.srt`, `out/CS115/L30/chapters.txt`) |
| Xem video bài 31 (Phân rã ma trận không âm (NMF): học “các phần” của dữ liệu) | `out/CS115/L31/L31.mp4` (+ `out/CS115/L31/L31.srt`, `out/CS115/L31/chapters.txt`) |
| Xem video bài 32 (t-SNE: trực quan hoá dữ liệu nhiều chiều bằng xác suất láng giềng) | `out/CS115/L32/L32.mp4` (+ `out/CS115/L32/L32.srt`, `out/CS115/L32/chapters.txt`) |
| Xem video bài 33 (Tổng ôn: bảng thuật toán & 3 câu hỏi vàng) | `out/CS115/L33/L33.mp4` (+ `out/CS115/L33/L33.srt`, `out/CS115/L33/chapters.txt`) |
| Xem video bài 34 (mở rộng) (Phép tích chập & mạng nơ-ron tích chập (CNN)) | `out/CS115/L34/L34.mp4` (+ `out/CS115/L34/L34.srt`, `out/CS115/L34/chapters.txt`) |
| Xem video bài 35 (mở rộng) (Mạng nơ-ron hồi tiếp (RNN), lan truyền ngược theo thời gian & LSTM) | `out/CS115/L35/L35.mp4` (+ `out/CS115/L35/L35.srt`, `out/CS115/L35/chapters.txt`) |
| Xem video bài 36 (mở rộng) (Boosting: AdaBoost & gradient boosting (so với rừng ngẫu nhiên)) | `out/CS115/L36/L36.mp4` (+ `out/CS115/L36/L36.srt`, `out/CS115/L36/chapters.txt`) |
| Xem video bài 37 (mở rộng) (Autoencoder: nén phi tuyến bằng mạng nơ-ron (so với PCA)) | `out/CS115/L37/L37.mp4` (+ `out/CS115/L37/L37.srt`, `out/CS115/L37/chapters.txt`) |
| Xem video bài 38 (mở rộng) (Phân tích thành phần độc lập (ICA): tách các nguồn bị trộn lẫn) | `out/CS115/L38/L38.mp4` (+ `out/CS115/L38/L38.srt`, `out/CS115/L38/chapters.txt`) |
| Xem video bài 39 (mở rộng) (Học tăng cường: quá trình quyết định Markov, phương trình Bellman & Q-learning) | `out/CS115/L39/L39.mp4` (+ `out/CS115/L39/L39.srt`, `out/CS115/L39/chapters.txt`) |
| Xem video bài 40 (mở rộng) (UMAP: giảm chiều bằng đồ thị láng giềng (so với t-SNE)) | `out/CS115/L40/L40.mp4` (+ `out/CS115/L40/L40.srt`, `out/CS115/L40/chapters.txt`) |
| Xem video bài 41 (mở rộng) (Cơ chế attention & Transformer) | `out/CS115/L41/L41.mp4` (+ `out/CS115/L41/L41.srt`, `out/CS115/L41/chapters.txt`) |
| Xem video bài 42 (mở rộng) (Mô hình sinh (1): Variational Autoencoder & GAN) | `out/CS115/L42/L42.mp4` (+ `out/CS115/L42/L42.srt`, `out/CS115/L42/chapters.txt`) |
| Xem video bài 43 (mở rộng) (Mô hình sinh (2): mô hình khuếch tán (diffusion)) | `out/CS115/L43/L43.mp4` (+ `out/CS115/L43/L43.srt`, `out/CS115/L43/chapters.txt`) |
| Xem video bài 44 (bổ sung — nên học ngay sau bài 21) (Thống kê: trung bình mẫu, định lý giới hạn trung tâm, khoảng tin cậy, so sánh hai mô hình) | `out/CS115/L44/L44.mp4` (+ `out/CS115/L44/L44.srt`, `out/CS115/L44/chapters.txt`) |
| Duyệt nhanh nội dung bài (không cần mạng) | `out/CS115/L00/preview.html`, `out/CS115/L01/preview.html`, `out/CS115/L02/preview.html`, `out/CS115/L03/preview.html`, `out/CS115/L04/preview.html`, `out/CS115/L05/preview.html`, `out/CS115/L06/preview.html`, `out/CS115/L07/preview.html`, `out/CS115/L08/preview.html`, `out/CS115/L09/preview.html`, `out/CS115/L10/preview.html`, `out/CS115/L11/preview.html`, `out/CS115/L12/preview.html` … `out/CS115/L44/preview.html` (đủ L00–L44) trong trình duyệt, phím ←/→ |
| Biết câu nào cần người nghe lại | `out/<khoá>/<id>/asr_report.md`; tổng hợp ở `audit/REVIEW_L02.md` §4, `audit/REVIEW_L03.md`, `audit/REVIEW_L04.md`, `audit/REVIEW_L05.md`, `audit/REVIEW_L06.md`, `audit/REVIEW_L07.md`, `audit/REVIEW_L00.md`, `audit/REVIEW_L03_he_phuong_trinh.md`, `audit/REVIEW_L09.md`, `audit/REVIEW_L10.md`, `audit/REVIEW_L11.md`, `audit/REVIEW_L12.md`, `audit/REVIEW_L13.md` … `audit/REVIEW_L43.md` (REVIEW cũ giữ số hiệu lúc viết — tra `orig`/`prev` trong curriculum) |
| Cài môi trường trên máy mới | `python -m venv .venv` rồi `.venv/Scripts/python -m pip install -r requirements.txt` (venv không mang sang máy khác được) |
| Xem lỗi của tài liệu gốc CS115 | `audit/AUDIT_CS115.md` (kiểm bằng `audit/verify_cs115_tex.py`) |
| Xem lộ trình 45 bài: L00–L33 chính, L34–L43 mở rộng tuỳ chọn, L44 thống kê (bổ sung, nên học ngay sau bài 21); số hiệu là thứ tự dựng, `not_included` trống | `curriculum/cs115.yaml`; căn cứ: `audit/SYLLABUS_CS115.md`, bảng đổi số: `audit/CURRICULUM_RENUMBER.md` |
| Làm bài tiếp theo | Nhờ Claude: “rà soát/sửa bài Lxx theo skill lecture-video” (đủ 45 bài L00–L44 đã có video), hoặc tự làm theo `.claude/skills/lecture-video/SKILL.md` |

## CS112 — Phân tích & Thiết kế Thuật toán

| Bạn muốn | Mở / chạy |
|---|---|
| Xem video bài 0 (Đếm số bước của thuật toán: số lần so sánh, làm tròn lên/xuống, lôgarit và các tổng Sigma) | `out/CS112/L00/L00.mp4` (+ `.srt`, `chapters.txt`, `preview.html`) |
| Xem video bài 1 (Ký hiệu tiệm cận O, Ω, Θ (và o, ω): định nghĩa chặt và phương pháp giới hạn) | `out/CS112/L01/L01.mp4` (+ `.srt`, `chapters.txt`, `preview.html`) |
| Xem video bài 2 (Xếp hạng tốc độ tăng của các hàm: từ log n đến n! và bẫy đổi cơ số mũ) | `out/CS112/L02/L02.mp4` (+ `.srt`, `chapters.txt`, `preview.html`) |
| Xem video bài 3 (Mảng, mảng động & danh sách liên kết: địa chỉ ô nhớ và chi phí khấu hao) | `out/CS112/L03/L03.mp4` (+ `.srt`, `chapters.txt`, `preview.html`) |
| Xem video bài 4 (Ngăn xếp & hàng đợi: vào sau ra trước, vào trước ra trước, và ngăn xếp lời gọi hàm) | `out/CS112/L04/L04.mp4` (+ `.srt`, `chapters.txt`, `preview.html`) |
| Xem video bài 5 (Cây nhị phân, cây tìm kiếm nhị phân & cây AVL tự cân bằng) | `out/CS112/L05/L05.mp4` (+ `.srt`, `chapters.txt`, `preview.html`) |
| Xem video bài 6 (Bảng băm & đống nhị phân (hàng đợi ưu tiên): vì sao dựng đống chỉ tốn Θ(n)) | `out/CS112/L06/L06.mp4` (+ `.srt`, `chapters.txt`, `preview.html`) |
| Xem video bài 7 (Đồ thị: ma trận kề, danh sách kề, duyệt theo chiều rộng (BFS) và chiều sâu (DFS)) | `out/CS112/L07/L07.mp4` (+ `.srt`, `chapters.txt`, `preview.html`) |
| Xem video bài 8 (Hệ thức truy hồi & phương pháp thế ngược: bài toán Tháp Hà Nội) | `out/CS112/L08/L08.mp4` (+ `.srt`, `chapters.txt`, `preview.html`) |
| Xem video bài 9 (Hàm sinh: giải hệ thức truy hồi bằng chuỗi lũy thừa) | `out/CS112/L09/L09.mp4` (+ `.srt`, `chapters.txt`, `preview.html`) |
| Xem video bài 10 (Đếm đúng số lời gọi đệ quy & chứng minh quy nạp có phần dư) | `out/CS112/L10/L10.mp4` (+ `.srt`, `chapters.txt`, `preview.html`) |
| Xem video bài 11 (Đổi biến số: giải T(n) = √n · T(√n) + n) | `out/CS112/L11/L11.mp4` (+ `.srt`, `chapters.txt`, `preview.html`) |
| Xem video bài 12 (Chia để trị & định lý thợ (Master theorem)) | `out/CS112/L12/L12.mp4` (+ `.srt`, `chapters.txt`, `preview.html`) |
| Xem video bài 13 (Giảm để trị & biến đổi để trị: sắp xếp chèn, tìm kiếm nhị phân, sắp xếp trước) | `out/CS112/L13/L13.mp4` (+ `.srt`, `chapters.txt`, `preview.html`) |
| Xem video bài 14 (Quay lui: cây trạng thái và bước trả lại đánh dấu) | `out/CS112/L14/L14.mp4` (+ `.srt`, `chapters.txt`, `preview.html`) |
| Xem video bài 15 (Nhánh cận: bài toán người du lịch với ma trận rút gọn) | `out/CS112/L15/L15.mp4` (+ `.srt`, `chapters.txt`, `preview.html`) |
| Xem video bài 16 (Tham lam (1): bài toán cái túi phân số) | `out/CS112/L16/L16.mp4` (+ `.srt`, `chapters.txt`, `preview.html`) |
| Xem video bài 17 (Tham lam (2): xếp lịch hội trường — chọn hoạt động kết thúc sớm nhất) | `out/CS112/L17/L17.mp4` (+ `.srt`, `chapters.txt`, `preview.html`) |
| Xem video bài 18 (Bản chất quy hoạch động: bài toán con gối nhau, ghi nhớ từ trên xuống và lập bảng từ dưới lên) | `out/CS112/L18/L18.mp4` (+ `.srt`, `chapters.txt`, `preview.html`) |
| Xem video bài 19 (Quy hoạch động theo đoạn: đặt dấu ngoặc cho biểu thức và nhân chuỗi ma trận) | `out/CS112/L19/L19.mp4` (+ `.srt`, `chapters.txt`, `preview.html`) |
| Xem video bài 20 (Quy hoạch động kinh điển: dãy con tăng dài nhất và xâu con chung dài nhất) | `out/CS112/L20/L20.mp4` (+ `.srt`, `chapters.txt`, `preview.html`) |
| Xem video bài 21 (Quy hoạch tuyến tính hai biến: miền chấp nhận được và nghiệm tại đỉnh) | `out/CS112/L21/L21.mp4` (+ `.srt`, `chapters.txt`, `preview.html`) |
| Xem video bài 22 (Thuật toán đơn hình: đi từ đỉnh này sang đỉnh tốt hơn) | `out/CS112/L22/L22.mp4` (+ `.srt`, `chapters.txt`, `preview.html`) |
| Xem video bài 23 (Sắp xếp nhanh và giới hạn của sắp xếp bằng so sánh) | `out/CS112/L23/L23.mp4` (+ `.srt`, `chapters.txt`, `preview.html`) |
| Xem video bài 24 (Đường đi ngắn nhất: Dijkstra và Bellman-Ford) | `out/CS112/L24/L24.mp4` (+ `.srt`, `chapters.txt`, `preview.html`) |
| Xem video bài 25 (Cây khung nhỏ nhất: Kruskal, Prim và cấu trúc hợp–tìm) | `out/CS112/L25/L25.mp4` (+ `.srt`, `chapters.txt`, `preview.html`) |
| Xem video bài 26 (P, NP và quy dẫn: khi nào nên thôi tìm thuật toán nhanh) | `out/CS112/L26/L26.mp4` (+ `.srt`, `chapters.txt`, `preview.html`) |
| Xem video bài 27 (Bài tập lớn: so sánh thuật toán có đo đạc, ghi minh bạch phần việc của AI) | `out/CS112/L27/L27.mp4` (+ `.srt`, `chapters.txt`, `preview.html`) |
| Xem video bài 28 (Tổng ôn: bản đồ các dạng bài và những bẫy toán học đã gặp) | `out/CS112/L28/L28.mp4` (+ `.srt`, `chapters.txt`, `preview.html`) |
| Xem lộ trình 29 bài (số hiệu = thứ tự học) | `curriculum/cs112.yaml` |
| Khoá DMS · Toán rời rạc (20 bài, 115,8 phút) | lộ trình `curriculum/dms.yaml`, bài `lessons/dms/`, video `out/DMS/<id>/`, báo cáo `audit/dms/AUDIT_DMS.md` |
| Bản đồ 38 khoá, lộ trình theo nghề, hiện trạng | `curriculum/ROADMAP.md`, `curriculum/TRACKS.md`, `curriculum/STATUS.md` |
| Xem lỗi đã sửa so với bản thảo giáo án | `audit/cs112/AUDIT_CS112.md` (kiểm bằng `audit/cs112/verify_cs112.py`; bản thảo gốc giữ nguyên văn ở `audit/cs112/CS112_ban_thao_goc.yaml`) |
| Xem bằng chứng cách đọc từ ngoại (Theta, Omega, AVL, Fibonacci…) | `audit/cs112/probes/*.md`; luật đọc riêng CS112: `tools/registry/lexicon_vi.CS112.yaml` |
| Biết câu nào cần người nghe lại | `out/CS112/<id>/asr_report.md`, tổng hợp ở `audit/cs112/REVIEW_CS112.md` |
| Chạy lại toàn bộ (dựng + nghe lại) | `.venv/Scripts/python -u audit/cs112/run_queue.py build:lessons/cs112/L00_dem_so_buoc.yaml asr:lessons/cs112/L00_dem_so_buoc.yaml …` (TTS bị chặn thì tự chờ 1 giờ rồi thử lại) |

## Lệnh
```
.venv/Scripts/python tools/lv.py new      lessons/cs115/L02_ma_tran.yaml --id L02 --title "Bài 2 — Ma trận"
.venv/Scripts/python tools/lv.py lint     lessons/cs115/L02_ma_tran.yaml
.venv/Scripts/python tools/lv.py preview  lessons/cs115/L02_ma_tran.yaml
.venv/Scripts/python tools/lv.py build    lessons/cs115/L02_ma_tran.yaml
.venv/Scripts/python tools/lv.py asr      lessons/cs115/L02_ma_tran.yaml   # máy nghe lại giọng đọc, báo câu đọc sai
.venv/Scripts/python tools/lv.py curriculum curriculum/cs115.yaml
.venv/Scripts/python tools/lv.py curriculum curriculum/cs112.yaml
.venv/Scripts/python tests/test_lint.py
.venv/Scripts/python tools/lv.py new-course GFX --title "Đồ hoạ máy tính"          # khung khoá mới
.venv/Scripts/python audit/review/audit_all.py && .venv/Scripts/python audit/review/status_report.py && .venv/Scripts/python audit/review/tracks.py
```
Giọng: mọi bài dùng `vi-VN-NamMinhNeural`. Một bài chỉ một giọng, một khoá giữ một giọng. Khi giọng gốc bị chặn, hàng đợi dựng đổi giọng dự phòng cho cả bài (`tools/registry/tts_fallback.yaml`). Tốc độ đặt bằng trường `rate` (ví dụ `-5%`).
Giọng đọc dùng dịch vụ trực tuyến edge-tts: nội dung câu đọc được gửi tới máy chủ Microsoft.
