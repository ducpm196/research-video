# Đối chiếu lộ trình CS115 với đề cương và slide môn học — 2026-10-24

Mục đích: kiểm từng ý của một bản nhận xét (người dùng dán vào chat ngày 2026-10-24) về độ phủ của `curriculum/cs115.yaml`, rồi sửa lộ trình theo phần nhận xét **có bằng chứng**.
Nhãn: OBSERVED = đọc/chạy trong phiên này; INFERRED = suy luận, chưa kiểm.

> **Đánh số lại 2 lần (2026-10-24):** số bài ở §1–§5 là số **ban đầu** (`orig` trong curriculum). Bản 2: L00–L29; bản 3 (hiện tại): L00–L33 — xem §6 và `audit/CURRICULUM_RENUMBER.md` §1, §6.
>
> **Đính chính (FAILED, phát hiện 2026-10-24 ~12:5xZ):** dòng §1 “`lagrange` … 0 kết quả” là **sai**: slide PR25 (`2025_Probability_MLE_MAP_Bayse.pdf`) có 1 lần “Lagrange multiplier to ensure that params sum to one” (MLE phân phối phân loại). Các từ khoá còn lại của dòng đó vẫn đúng 0 (đếm lại bằng `grep -i -c` trên 13 văn bản trích, §6). Hệ quả: bài Lagrange/KKT (nay L24) **có** một điểm tựa trong nguồn, không hoàn toàn “ngoài nguồn” như N2 ghi.
>
> (Cũ) số bài trong §1–§5 (L17–L26, L16 tổng ôn) là số **cũ**. Số mới (L00–L29, tịnh tiến theo thứ tự học, thêm L11 hàm mũ & logarit, L13 biến liên tục, L25 KNN) xem `audit/CURRICULUM_RENUMBER.md` §1.

## 1. Nguồn đã đọc (OBSERVED, 2026-10-24)

Các file nằm ngoài dự án (`C:\Users\AI_Worker\Downloads\`), đọc bằng `pdftotext` (bản mã dấu tiếng Việt bị lỗi nhưng đọc được). Không chép file vào dự án.

| Khoá | File | sha256 (16 ký tự đầu) | Nội dung dùng |
|---|---|---|---|
| DC23 | `CS115.O11_Đề cương_Toan cho KHMT.pdf` (đề cương, bản cập nhật 01/2023) | `0d289ba3cc37ace4` | mục 5.1 (nội dung theo tuần), 7.1 (đánh giá) |
| GT24 | `CS115_Course_Introduction.pdf` (slide giới thiệu môn) | `e7803b2264320962` | trang 6 (đánh giá), trang 9–13 (nội dung theo tuần) |
| NN | `CS115_Neuron_Network.pdf` | `f37daf072fc268d4` | mục “Advanced algorithms”: quasi-Newton, Conjugate Gradient, Levenberg-Marquardt |
| AG25 | `2025_03_CS115_Analytic Geometry.pdf` | `81f32878d2367940` | mục “Applications: Clustering”, thuật toán k-means |
| TEX | `CS115_Toan_cho_Khoa_hoc_May_tinh_Full.tex` (trong dự án) | — | bảng tổng kết dòng 395–412 |

Tìm từ khoá trên cả 13 file PDF môn CS115 trong `Downloads` (lệnh `grep -i -c` trên văn bản trích): `lagrange`, `kkt`, `karush`, `lasso`, `margin`, `mixture`, `t-sne` đều **0 kết quả**; `ràng buộc`/`constrain`/`đối ngẫu`/`dual` không có kết quả nào về tối ưu.

## 2. Nội dung đề cương (OBSERVED, DC23 mục 5.1; GT24 trang 9–13)

| Chương | Chủ đề trong đề cương | Lộ trình trước khi sửa |
|---|---|---|
| 1. Ôn tập (tuần 1–3) | Giải tích, Đại số tuyến tính, Xác suất thống kê | L00–L06, L09, L10 |
| 2. Hồi quy (tuần 4–6) | MLE, Linear regression, Logistic regression, squared-error / cross-entropy loss | L12, L13, L14 |
| 3. Tối ưu (DC23 dòng 157–168) | tối ưu lồi (giới thiệu), **phương pháp Newton**, Gradient descent, **L1, L2 Regularization**, SGD, Momentum, **Nesterov, Adagrad, RMSprop, Adadelta**, Adam | L07, L08 (chỉ GD, SGD, Momentum, Adam) |
| 4. Mạng neural (DC23 dòng 173–188) | **MLP**, đồ thị tính toán, chain rule + backprop, **Cross-validation, Batch normalization, điều chỉnh hyperparameters** | L15 (đồ thị tính toán, backprop) |
| 5. Seminar – đồ án (DC23 dòng 193–209) | **LDA**, SVD & PCA, **SVM & kernels**, **EM**, **Hierarchical, Spectral clustering**, “….”; GT24 thêm **NMF, Clustering, Decision Tree, Random Forest** | L11 (SVD, PCA) |

Đánh giá (DC23 dòng 243–264; GT24 trang 6): A1 quá trình **40%** (quiz 10% + thuyết trình/bài tập 30%); cuối kỳ **60%** = thi viết 30% + báo cáo đồ án 30%.

## 3. Kiểm từng ý của bản nhận xét

| # | Ý của nhận xét | Kết quả | Bằng chứng |
|---|---|---|---|
| N1 | Lộ trình phủ tốt đại số tuyến tính, giải tích vector, xác suất, mô hình cơ bản, SVD/PCA | Đúng | bảng mục 2 |
| N2 | Thiếu tối ưu có ràng buộc: **KKT / nhân tử Lagrange** “trong đề cương” | **Sai về nguồn**: đề cương và mọi slide không nhắc Lagrange/KKT (0 kết quả). Đề cương chỉ có “giới thiệu tối ưu lồi” | mục 1 |
| N2b | Thiếu **phương pháp Newton** | Đúng (DC23 dòng 159–160) | — |
| N2c | Thiếu **Conjugate Gradient, Levenberg-Marquardt** | Đúng nhưng nguồn là slide NN, không phải đề cương | NN “Advanced algorithms” |
| N3 | Thiếu **L1, L2 Regularization** | Đúng (DC23 dòng 163). Lasso/Ridge là tên gọi chuẩn; không có trong file nào | — |
| N4 | Thiếu **SVM & kernel**, lề 2/‖w‖, đối ngẫu Lagrange | SVM & kernel: đúng (DC23 dòng 202). Lề 2/‖w‖: đúng (kiểm T19). Đối ngẫu Lagrange: không có trong nguồn, nhưng cần nếu muốn giải thích kernel | T19 |
| N5 | Thiếu **LDA** | Đúng (DC23 dòng 193). Câu “tối đa khoảng cách giữa các lớp” (TEX dòng 410) thiếu vế phương sai trong lớp → A23 | T16 |
| N6 | Thiếu **K-Means, Hierarchical, Spectral, GMM + EM** | Hierarchical, Spectral, EM: đúng (DC23). K-Means: có ở AG25 và TEX dòng 408 (không ghi trong DC23). GMM: không ghi tên ở đâu; là ví dụ chuẩn của EM (INFERRED) | AG25; A24, T17 |
| N7 | Đề xuất **t-SNE** | **Không có trong nguồn nào** (0 kết quả) → không thêm | mục 1 |
| N8 | Đồ án & seminar chiếm 30% | Đúng (báo cáo đồ án 30%) | DC23 dòng 264 |
| N9 | “Thi viết lý thuyết (40%) lẫn báo cáo đồ án (60%)” | **Sai**: thi viết 30%, đồ án 30%, quá trình 40% | DC23 dòng 243–264; GT24 trang 6 |
| N10 | Các ghi chú sửa lỗi L00, L02/L13, L03, L07, L14, L16 | Đã có sẵn trong `curriculum/cs115.yaml` (A7, A9, A20, A1/A2, A5, A14). Hai chỗ nhận xét viết quá tay: (a) “loss = 0 dẫn đến quá khớp” — loss huấn luyện bằng 0 là **dấu hiệu nghi** quá khớp, không phải luôn luôn (A7 giữ cách viết “thường là dấu hiệu”); (b) phương trình chuẩn XᵀXw = Xᵀy **luôn có nghiệm**; chỉ **công thức** (XᵀX)⁻¹Xᵀy cần XᵀX khả nghịch (A9; T18: Ridge làm XᵀX + λI khả nghịch) | AUDIT A7, A9; T18 |
| N11 | (nhận xét **bỏ sót**) Nesterov, Adagrad, RMSprop, Adadelta; MLP; Cross-validation; Batch normalization; hyperparameters; Decision Tree / Random Forest; NMF | Đều có trong DC23 hoặc GT24 nhưng không có trong nhận xét | mục 2 |

## 4. Quyết định sửa lộ trình

Giữ nguyên số hiệu L00–L16: video L02–L05 đã nói “bài 7”, “bài 8”, “bài 11”, “bài 13”, “bài 15” (OBSERVED, `grep` trên `lessons/*.yaml`), đổi số sẽ làm sai lời đọc. Bài mới nhận số L17–L26 và được **chèn đúng vị trí học** trong danh sách (công cụ `curriculum` kiểm thứ tự theo vị trí, không theo số).

| Bài | Nội dung | Vị trí (sau) | Căn cứ |
|---|---|---|---|
| L17 | Nesterov, Adagrad, RMSprop, Adadelta (và Adam nhìn lại) | L08 | DC23 Ch3 |
| L18 | Tối ưu lồi, phương pháp Newton; quasi-Newton, Conjugate Gradient, Levenberg-Marquardt (tổng quan) | L17 | DC23 Ch3; NN |
| L19 | Quá khớp, chính quy hoá L1/L2 (Lasso, Ridge), cross-validation | L13 | DC23 Ch3, Ch4; A9, T18 |
| L20 | MLP, Batch normalization, điều chỉnh hyperparameters | L15 | DC23 Ch4 |
| L21 | Nhân tử Lagrange & điều kiện KKT (cầu nối cho SVM) | L20 | **Ngoài nguồn**; cần cho SVM đối ngẫu và kernel |
| L22 | SVM: lề lớn nhất, hinge loss, kernel | L21 | DC23 Ch5; TEX 406; T19 |
| L23 | LDA (tiêu chí Fisher) | L22 | DC23 Ch5; A23, T16 |
| L24 | Phân cụm: K-Means, phân cấp, phổ (ma trận Laplacian) | L23 | DC23 Ch5; AG25; A24, T17 |
| L25 | GMM & thuật toán EM | L24 | DC23 Ch5 |
| L26 | Cây quyết định & rừng ngẫu nhiên (entropy, Gini) | L25 | GT24; TEX 407 |
| L16 | Tổng ôn — **dời xuống cuối** vì bảng tổng kết (TEX 395–412) có SVM, K-Means, LDA, cây quyết định | cuối | TEX 395–412 |

Không thêm (ghi ở `not_included` trong curriculum):
- t-SNE: không có trong nguồn nào.
- NMF: chỉ có trong GT24 (slide), không có trong DC23. **Quyết định mở cho người dùng.**

## 5. Còn mở

- L21 (Lagrange/KKT) nằm ngoài đề cương: đề xuất giữ vì SVM dạng đối ngẫu cần nó. Người dùng có thể bỏ; khi đó L22 chỉ dạy dạng hinge loss + L2 (TEX dòng 406) và nêu kernel ở mức ý tưởng.
- NMF: chưa có bài.
- Trọng số điểm và tuần học lấy từ bản đề cương 01/2023 và slide giới thiệu; học kỳ hiện tại có thể khác (NOT_VERIFIED).

## 6. Rà soát bổ sung lần 2 — bản 3 của lộ trình (2026-10-24, theo yêu cầu “bổ sung t-SNE, NMF,… hoàn thiện giáo án”)

### 6.1 Nguồn (OBSERVED: `pdftotext -enc UTF-8` + `sha256sum`, 12:5xZ)

Văn bản trích lưu ở scratchpad `src_txt/` (ngoài dự án). Hai file tên tiếng Việt phải chép sang tên ASCII trước (`pdftotext` trên Windows không mở được tên Unicode).

| Khoá | File | sha256 (16 ký tự) | Ghi chú |
|---|---|---|---|
| LA24 | `2024_02_CS115_Linear Algebra Review.pdf` | `d2f0df88ed283d08` | lộ trình: Systems of Linear Equations → Matrices → Linear Independence → Basis and Rank → Linear Mappings; slide “Algorithms for Solving System of Linear Equations”; Dimension Reduction |
| BT1 | `Bài tập 1_Matran_He PTTT.pdf` | `afdf0d37baebfc14` | bản scan: chỉ trích được 133 byte (“Bài III. Giải các hệ phương trình tuyến tính”) — nội dung chi tiết NOT_VERIFIED (cần OCR) |
| ML24 | `2024_01_CS115_ML_Introduction.pdf` | `472fd3d5d851a2f5` | “Confusion matrix, Accuracy, Precision, Recall, F-score”; hồi quy đa thức f(x; w) = wᵀφ(x); overfitting; train/test |
| VC24 | `2024_04_CS115_Vector Caculus.pdf` | `d868ad9c04efb3a5` | Jacobian, chain rule, backprop, Taylor (bản “(1)” trùng nội dung văn bản: 10354 ký tự cả hai) |
| PR25 | `2025_Probability_MLE_MAP_Bayse.pdf` | `5c2ac0ae5584bc21` | Normal (ML → least squares), conjugate prior, **Categorical ML với nhân tử Lagrange**, MAP với prior Dirichlet |
| AG24 | `2024_03_CS115_Analytic Geometric.pdf` | `abf6298138192479` | KNN, cross-validation, hyperparameter |
| MLI | `CS115.01_Introduction to Machine Learning.pdf` | `1edff21437274391` | trùng phần lớn ML24 |
| R05 | `R_05_CS115_Linear Regression.pdf` | `f89958d4dfd04cf6` | gradient descent cho hồi quy tuyến tính |
| GT24, NN, AG25, DC23 | như §1 | `e7803b2264320962`, `f37daf072fc268d4`, `81f32878d2367940`, `0d289ba3cc37ace4` | khớp sha256 đã ghi ở §1 |

### 6.2 Quét chủ đề (OBSERVED, `scratchpad/topic_scan.py`, ~110 từ khoá × 14 văn bản gồm tex)

| Chủ đề | Số lần / nơi xuất hiện | Có trong lộ trình bản 2? | Quyết định bản 3 |
|---|---|---|---|
| Hệ phương trình tuyến tính, khử, hạng | LA24 (lộ trình + 2 slide), BT1 bài III; L03/L04/L07 bản 2 **dùng** giải hệ nhưng `grep "khử\|Gauss"` trên lessons/ = 0 | **Không** | **Thêm L03** (trước Gram-Schmidt) |
| Confusion matrix, accuracy, precision, recall, F-score | ML24 dòng 34 (văn bản trích) | Không | **Thêm L21** (sau logistic) |
| NMF | GT24: 1 dòng (2 lần) | Không (`not_included`) | **Thêm L31** theo yêu cầu người dùng; trích Lee & Seung 1999 (CITED) |
| t-SNE | **0** trên mọi nguồn | Không (`not_included`) | **Thêm L32** theo yêu cầu người dùng, ghi rõ “ngoài nguồn”; trích van der Maaten & Hinton 2008 (CITED) |
| Hồi quy đa thức, φ(x) | ML24 (11 lần) | Không nêu | Ghi vào `fix` của L18, L19 |
| Bernoulli, Categorical, Dirichlet, conjugate prior | PR25 | Không nêu | Ghi vào `fix` của L13, L17 |
| Lagrange (MLE categorical) | PR25: 1 | L24 ghi “ngoài nguồn” | Sửa `source` của L24; L17 giải bằng cách thế, L24 làm lại bằng Lagrange |
| Hàm kích hoạt, khởi tạo Xavier, dropout, triệt tiêu gradient, gradient checking | NN (activation 53, init 6, dropout 1, vanishing 1) | Chỉ có “MLP, BN, hyperparameters” | Mở rộng tên và `fix` của L23; gradient checking vào L22; dropout vào L19 |
| Sequential vs batch training, learning-rate schedule | NN | Không nêu | `fix` của L09 |
| CNN, RNN | ML24/NN: 1 lần mỗi file, chỉ nêu tên | Không | `not_included` (không có nội dung toán) |
| Reinforcement learning | ML24: 2 (một loại bài toán) | Không | `not_included` |
| UMAP, ICA, autoencoder, boosting, KL, Markov, Monte Carlo | 0 | — | Không thêm (KL dạy trong L32 vì t-SNE cần) |

DC23 Chương 5 kết thúc bằng “● ….” (danh sách chủ đề seminar mở) — chỗ dựa cho việc thêm NMF và t-SNE làm chủ đề mở rộng (INFERRED: đề cương không nêu tên chúng).

### 6.3 Thứ tự bản 3 (OBSERVED: `lv.py curriculum` → 34 bài, 0 lỗi)

Phần 1 Đại số tuyến tính L00–L05 (thêm L03) · Phần 2 Giải tích & tối ưu L06–L12 · Phần 3 Xác suất L13–L17 · Phần 4 Mô hình L18–L23 (thêm L21) · Phần 5 Có giám sát khác L24–L28 (cây quyết định dời lên L28 để gom với KNN) · Phần 6 Không giám sát L29–L32 (thêm L31 NMF, L32 t-SNE) · L33 Tổng ôn.
Bảng đổi số bản 2 → bản 3: `audit/CURRICULUM_RENUMBER.md` §6.

## 7. Phần mở rộng tuỳ chọn L34–L39 (2026-10-24 ~14:35Z, yêu cầu “bổ sung đầy đủ các topic đang cân nhắc”)

“Các topic đang cân nhắc” = các mục còn ở `not_included` của bản 3: CNN, RNN, học tăng cường, UMAP, ICA, autoencoder, boosting. Quyết định (đảo ngược được — xoá mục là bỏ):

| Bài | Chủ đề | Có trong nguồn môn học? | Trích dẫn (CITED, truy cập 2026-10-24) |
|---|---|---|---|
| L34 | Phép tích chập, CNN | chỉ nhắc tên (ML24, NN, VC24) | LeCun, Bottou, Bengio & Haffner, Proc. IEEE 86(11) (1998) 2278–2324 |
| L35 | RNN, lan truyền ngược theo thời gian, LSTM | chỉ nhắc tên (ML24, NN) | Hochreiter & Schmidhuber, Neural Computation 9(8) (1997) 1735–1780 |
| L36 | Boosting: AdaBoost, gradient boosting | 0 | Freund & Schapire, JCSS 55(1) (1997) 119–139 |
| L37 | Autoencoder | 0 | Hinton & Salakhutdinov, Science 313 (2006) 504–507 |
| L38 | ICA | 0 | Hyvärinen & Oja, Neural Networks (2000) — **số tập/trang NOT_VERIFIED** (kết quả tìm kiếm không cho) |
| L39 | Học tăng cường: MDP, Bellman, Q-learning | nêu là một loại bài toán (ML24) | Sutton & Barto, Reinforcement Learning: An Introduction, 2nd ed., MIT Press (2018) |
| (L32) | UMAP — gộp vào bài t-SNE làm phần so sánh | 0 | McInnes, Healy & Melville, arXiv:1802.03426 (2018) |

- Đặt **sau** tổng ôn L33 để không đánh số lại 10 video đã làm (L00–L09); L00 (bản đồ khoá học) được cập nhật thêm “bài 34–39: mở rộng tuỳ chọn”.
- Các phát biểu toán trong `fix` của L34–L39 được kiểm bằng máy trước khi ghi (`scratchpad/ext_checks.py`, OBSERVED): autoencoder tuyến tính học đúng không gian con PCA (góc 0,0°); α của AdaBoost = 0 tại ε = ½, dương khi ε < ½; −∂/∂ŷ ½(y − ŷ)² = y − ŷ (với (y − ŷ)² là 2(y − ŷ) → `fix` viết lại cho chính xác); công thức kích thước tích chập khớp đếm trượt ở 4 cấu hình; tương quan chéo = nhân ma trận thưa và khác `np.convolve` (có lật); 0,9⁵⁰ ≈ 0,005, 1,1⁵⁰ ≈ 117.
- Còn trong `not_included`: Transformer/attention, mô hình sinh (0 kết quả, người dùng chưa nêu).

## 8. L40–L43: làm trống `not_included` (2026-10-24 ~15:50Z, yêu cầu “bổ sung đầy đủ các topic not_included”)

| Bài | Chủ đề | Trích dẫn (CITED, truy cập 2026-10-24) | Ghi chú kiểm |
|---|---|---|---|
| L40 | UMAP (tách khỏi L32) | McInnes, Healy & Melville, arXiv:1802.03426 | “nhanh hơn, giữ cấu trúc toàn cục tốt hơn” = nhận định của tác giả |
| L41 | Attention & Transformer | Vaswani et al., arXiv:1706.03762 (NeurIPS 2017 — chỉ nguồn thứ cấp xác nhận hội nghị) | `ext2_checks.py`: hàng softmax cộng = 1; var(q·k) = 15,96 ≈ d = 16, chia √d → 0,998; hoán vị đồng biến khi không có vị trí |
| L42 | VAE & GAN | Kingma & Welling, arXiv:1312.6114 (ICLR 2014); Goodfellow et al., arXiv:1406.2661 | D* = p/(p+q), đạo hàm cấp 2 âm; −log 4 tại p_g = p_data (sympy — nguồn tìm được KHÔNG nêu −log 4, tự kiểm); KL Gauss đóng (tích phân sympy); ELBO ≤ log p(x), bằng nhau tại hậu nghiệm đúng |
| L43 | Diffusion | Ho, Jain & Abbeel, arXiv:2006.11239 (NeurIPS 2020 — nguồn thứ cấp) | gộp 2 bước: hệ số √ᾱ, phương sai 1 − ᾱ (sympy); lịch 1e-4 → 0,02, T = 1000: ᾱ_T ≈ 4·10⁻⁵ |

`not_included: []`. L00 (bản đồ khoá học) sửa thành “bài 34–43: mở rộng tuỳ chọn”. Tổng: 44 bài (L00–L33 chính, L34–L43 mở rộng).
