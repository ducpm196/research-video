# S01 BNX L12–L23: đã đọc 12/12 bài (2026-11-14)

Người đọc: điều phối + 4 tác tử đọc độc lập (A: L12–14, B: L15–17, C: L18–20, D: L21–23). Mỗi bài: đọc trọn YAML, mục `curriculum/bnx.yaml`, lab chạy như người học (`cham.sh` ĐÚNG cả 12), tính lại số, chạy lại mã (Java 21, Python, Go 1.25.5, Spring Security 7.1.2 với jar `audit/bnx/deps/l17`, scikit-learn/ONNX trong `audit/bnx/deps/l23/venv`; không chạy docker/K8s/Redis/AEM/Spring Cloud/Fiber). Điều phối tự kiểm lại: sha YAML 12/12 khớp bản các tác tử đọc; `build_report.json` spec_sha256 khác YAML hiện tại ở 12/12 bài; L13 dòng 592, 597 trong YAML đúng như trích; 300/400 = 0,75.

## 0. Kết luận theo ngưỡng
| Ngưỡng | Kết quả |
|---|---|
| MUST = 0 | KHÔNG ĐẠT. Nội dung: L13 hai MUST (màn hình "tụt tới 25% sức chứa" vs lời "bảy mươi lăm phần trăm"; lời "mỗi đợt thay một phần tư số bản" sai, thực tế một nửa). Quy trình: video đã dựng (mp4/srt/chapters) lệch YAML ở cả 12 bài (xem 0.1). |
| P1 = 2 ≥ 90% | KHÔNG ĐẠT: 1/12 bài (L12) = 8%. P1=1: L13,14,15,16,18,19,21,22,23; P1=0: L17, L20. |
| P8 = 2 100% | ĐẠT 12/12 (lab chạy ĐÚNG lần đầu, ổn định). Lưu ý: L13/L17/L18 lab là mô hình Python/Java thuần, không đụng Docker/K8s/Spring/JUnit. |

### 0.1 Video đã dựng lệch YAML (cả 12 bài)
- YAML sửa 2026-11-14; mp4/srt/chapters/_frames.txt dựng 2026-11-10..13 (spec_sha256 trong `build_report.json` khác); thư mục `frames/*.png` đã render lại từ YAML mới. Chấm nội dung/khung hình theo YAML hiện tại; phút theo ước lượng (số từ × tốc độ SRT cũ + dừng).
- Bản dựng cũ thiếu cảnh `quymo`/`practice` (L12, L13, L14, L21, L22, L23); mục tiêu giáo án tương ứng chưa có trong video.
- Bản dựng cũ vượt trần 16 phút lời đọc: L16 17,9; L17 19,9; L19 17,7; L20 18,4; L22 17,05; L23 20,6; L18 15,74 lời / 16,78 tổng. YAML mới ước 10,8–15,7 phút (đạt) nếu dựng lại.
- L15 SRT cũ còn "như bài 1 đã dạy", "ở bài 3 và bài 5…" (nhắc khoá khác, bị cấm); YAML mới không còn.
- L12 SRT cũ khẳng định Nghị định 52/2024 như chắc chắn, không "cần kiểm lại"; YAML mới đã sửa (đúng yêu cầu CHUA_KIEM).
- Việc cần làm trước khi chốt: dựng lại 12 video, đo lại thời lượng, so SRT với `say`, rồi xem lại khung hình.

## 0.2 Tóm tắt một dòng mỗi bài
| Bài | sha16 | Phút YAML ước / bản cũ | P1..P7 | Tổng | P8 | P9 | Mất gốc |
|---|---|---|---|---|---|---|---|
| L12 | 6abee8211726b579 | 14,0 / 13,1 | 2 1 2 2 2 2 2 | 13 | 2 | 2 | ĐỦ |
| L13 | 5014e6856c92e711 | 14,6 / 12,8 | 1 2 2 2 2 2 1 | 12 | 2 | 2 | ĐỦ |
| L14 | fd52c3f3c26fc9be | 14,5 / 14,6 | 1 2 2 2 2 2 1 | 12 | 2 | 2 | ĐỦ |
| L15 | 158019698ce11e00 | 11,6 / 12,0 | 1 2 2 2 2 1 1 | 11 | 2 | 2 | GẦN |
| L16 | 904c311bd58f9103 | 12,0 / 17,9 | 1 2 1 2 2 2 1 | 11 | 2 | 2 | GẦN |
| L17 | a359137c59a1f8ef | 10,8 / 19,9 | 0 2 1 2 2 2 1 | 10 | 2 | 2 | GẦN |
| L18 | 98b729a0f8ee781e | 11,2 lời (15,7 tổng) / 15,74 | 1 2 2 2 2 1 1 | 11 | 2 | 2 | GẦN |
| L19 | 76dd738213b6f8ff | 11,3 / 17,72 | 1 2 2 2 2 1 2 | 12 | 2 | 2 | ĐỦ |
| L20 | 64b4f5badd8741c5 | 11,6 / 18,43 | 0 2 2 2 2 1 1 | 10 | 2 | 2 | GẦN |
| L21 | eb8f0d56a3c4d20c | 11,1 / 15,25 | 1 2 2 2 2 2 2 | 13 | 2 | 2 | ĐỦ |
| L22 | 80a5e8f581ea1152 | 11,6 / 17,05 | 1 2 2 2 2 2 2 | 13 | 2 | 2 | ĐỦ |
| L23 | d40f5fa0d2aefed1 | 11,75 / 20,6 | 1 1 2 2 2 2 2 | 12 | 2 | 2 | ĐỦ |

## 0.3 Các điểm được hỏi riêng
- "Chạy thật" (L13): chỉ `docker build --check` đo thật; Dockerfile, `.gitlab-ci.yml`, Deployment chưa dựng/áp dụng (parse YAML đúng cú pháp). "Kết quả chạy thật: 24 3 5 True" là mô hình Python của tác giả (SHOULD: nhãn nên ghi mô hình). Cảnh `quymo`/`practice` đã ghi "mô phỏng".
- L16: "Kết quả chạy thật" có dòng `số lượt: 3` là phép tính hằng, không phải đo (SHOULD). Lab đếm, không phụ thuộc đồng hồ; chạy 3–5 lần ổn định.
- L17: mã Spring chỉ hiện từng đoạn; ghép nguyên văn không biên dịch được (CauHinh 18 lỗi, ChayThu 15 lỗi: thiếu import, hàm `ky()` ký JWT, trường, main, danh sách jar). Bổ sung đủ thì chạy thật trên Spring Security 7.1.2 và ra đúng mọi dòng. Người học KHÔNG gõ lại được từ màn hình (SHOULD). Phần Spring Cloud (Gateway, Consul, Config, LoadBalancer): chỉ đọc. ChiaTai ghi "MÔ PHỎNG".
- L20: bảng đo ghi "Số đo trên máy này (Go 1.25.5, Windows)… đổi theo phiên bản"; lab không có phép đo, xác định. L16/L20 ổn.
- L22: ghi rõ mô phỏng Python, không phải AEM thật (hook, tiêu đề bước, recap). Dispatcher cache và AEMaaCS vs 6.5 không được dạy.
- Pháp lý: L12 YAML hiện tại đạt (NĐ52 CHUA_KIEM có cảnh báo, không nêu số điều; Luật 108/2025 ghi "nguồn tổng hợp, cần kiểm lại"); bản video cũ chưa đạt. L21: TT 31/2024 khớp Điều 10 qua bản dịch, nhưng có TT 37/2025/TT-NHNN (31/10/2025) sửa đổi, registry chưa ghi (SHOULD).
- E51: `covers` đúng cả 12 bài. Mục tiêu chỉ "xem, không tự làm/đo": L13 (viết Dockerfile; gắn ảnh–commit), L14 (1,3,4), L15 (3,4), L16 (3), L17 (2), L18 (1,2 không dùng JUnit/Mockito trong lab), L20 (1,4).

## 0.4 Bảng MUST/SHOULD tổng hợp (chi tiết từng dòng ở phần của mỗi nhóm bên dưới)
| Bài | MUST | SHOULD |
|---|---|---|
| L12 | video cũ thiếu quymo/practice; lời cũ khẳng định NĐ52 không cảnh báo (YAML mới đã sửa) | bất biến "cuối ngày" vs TT40 Điều 27 khoản 1 "cùng một thời điểm"; mũi tên SVG1 không nhãn |
| L13 | 25% vs 75% (quymo bước 4); "mỗi đợt thay một phần tư"; video cũ thiếu 2 cảnh | "luôn 2 đợt" sai khi D≡3 mod 4; "Kết quả chạy thật" là mô hình; "hơn 1 giờ 40" = đúng 100 phút |
| L14 | video cũ thiếu quymo/practice | 180 ngày bỏ vế "trừ khi thoả thuận"; "01/3/2025 mở cho bên thứ ba" thiếu lộ trình chuyển tiếp (Điều 15) và giới hạn đối tượng (Điều 5); "cụm thực thể" vs "aggregate" |
| L15 | video cũ có "như bài 1 đã dạy" | de.md làm tròn 41,6 vs 41,7; practice thiếu 4 chặng; đếm Oracle luôn 40 ms |
| L16 | video cũ 17,9 phút | "Kết quả chạy thật" là phép tính; orTimeout không có minh chứng; công thức ④⑤ chạm viền |
| L17 | video cũ 19,9 phút | mã không gõ lại được; nhãn "dài 32 byte" thực 36; khoá chung vs khoá công khai không nối; 35 s/10 s không nói mặc định; vòng chia bắt đầu ngẫu nhiên (chưa kiểm) |
| L18 | không | mục tiêu 1–2 chỉ xem (lab không JUnit/Mockito); thiếu cách sinh ca từ bảng; bản cũ 16,78 phút tổng |
| L19 | video cũ 17,72 phút | hook gom Cluster vào "chặn trùng"; "giây không" nghe ngược nghĩa |
| L20 | video cũ 18,43 phút | "hai chỗ lược kiểm lỗi" thực 3 chỗ; mục tiêu 1, 4 chỉ xem; quiz câu 3 khẳng định tập quán không nguồn; Fiber chưa kiểm |
| L21 | video cũ thiếu practice | TT 37/2025 chưa ghi; openssl verify thêm 2 dòng error stderr |
| L22 | video cũ 17,05 phút, thiếu practice | "5 nút" thực 6 theo hàm `duyet` của bài; "Thiếu dòng cuối thì không đăng ký" tuyệt đối (Sling-Model-Classes) |
| L23 | video cũ 20,6 phút, thiếu practice | quy tắc `int(p(n−1))+1` sai khi điểm trùng (1010 vs 1005); hai thước "độ sâu" 15,8 vs 11,88 chưa nối; phiên bản skl2onnx/lệnh cài không có trên màn hình |

## 0.5 Nhận xét chung
- Chặn lớn nhất là trạng thái dựng: 12/12 video lệch YAML; phải dựng lại rồi đọc/nghe lại trước khi chốt.
- Kiến thức nền chuẩn: không có số sai trong hàng trăm giá trị tính lại (trừ L13 hai chỗ lời và hai điểm quy ước L22/L23); mọi mã chạy được đều ra đúng kết quả màn hình.
- P1 là điểm yếu hệ thống: thuật ngữ dùng không giảng (OFS/T24, DS, numpy, `defer`/`:=`, ENV/WORKDIR, SAGA/Outbox, bộ đệm, giờ Unix).
- Lab (P8) mạnh nhưng nhiều bài chỉ kiểm mô hình thuần; mục tiêu "viết/dùng công cụ thật" (Dockerfile, JUnit/Mockito, HTTP/Fiber, cấu hình Spring) người học chỉ xem.
- Chưa nghe âm thanh (không có TTS bản mới); phút của YAML mới là ước lượng ±1.
- Nguồn pháp lý đối chiếu qua bản dịch/hợp nhất thứ cấp (TT40 VBHN, TT64 bản EN, TT31): chưa mở văn bản gốc.

---
# Chi tiết từng nhóm (báo cáo của tác tử, giữ nguyên)

## NHOM A (L12-L14)
# Phần A — BNX L12, L13, L14: đã đọc 3/3 bài (YAML trọn, curriculum, SRT, 18 khung hình, lab chạy)

**Phát hiện trạng thái kho (ảnh hưởng mọi mục dưới):** `out/BNX/L12|L13|L14` đang LỆCH `lessons/bnx`. `build_report.json` ghi spec_sha256 lúc dựng khác YAML hiện tại; YAML sửa 2026-11-14 07:19–07:43, mp4/srt/chapters dựng 11-10 → 11-13. Hậu quả: mp4/srt/chapters.txt KHÔNG có cảnh `quymo` (mục tiêu 5, L14 là 6) và `practice` (mục tiêu cuối); `chapters.txt` chỉ 10 mục, `grep -c "bảng tra|nano|bình phương" L12.srt` = 0. Thư mục `frames/` thì đã render lại 2026-11-14 theo YAML mới (100/104/105 ảnh) nhưng `_frames.txt` vẫn cũ (140/130/139). Vậy: **mọi đánh giá lời/hình dưới đây là theo YAML hiện tại + khung hình mới; mp4/srt hiện có là bản cũ, cần dựng lại.** Phút lời đọc của YAML mới là ước tính (từ số từ × tốc độ bản cũ + pause).

## 1) Bảng chuẩn xác

| Bài | Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng đã chạy | Đề xuất | Tin cậy |
|---|---|---|---|---|---|---|
| L12 | MUST | `out/BNX/L12` (mp4/srt/chapters) | chapters.txt: 10 mục, hết ở "Chuỗi logic & tư duy cần mang theo"; srt cuối 13:08 | `build_report.json` spec_sha256 `76ad27d2…` ≠ sha YAML hiện tại `6abee821…`; video thiếu cảnh `quymo` (mục tiêu 5: đếm phép so sánh 100/10 000/1 000 000) và `practice` (mục tiêu 6, lab); giáo án hứa mà video chưa dạy | Dựng lại video từ YAML hiện tại | CONFIRMED |
| L12 | MUST | srt cũ dòng 28–35 (cảnh `sym`) | "Nghị định năm mươi hai năm hai nghìn không trăm hai mươi tư nói tổng số dư tài khoản đảm bảo không thấp hơn tổng số dư các ví." (không kèm cần kiểm lại) | registry: 52/2024/NĐ-CP = CHUA_KIEM. `grep "kiểm lại" srt` chỉ 1 dòng (Lỗi 3, 10:13). Lời đọc bản cũ khẳng định như chắc chắn. YAML hiện tại đã sửa (màn hình "cần kiểm lại văn bản hiện hành") nhưng lời đọc YAML mới chỉ nói "nhưng cần kiểm lại" 1 lần cho NĐ52 | Dựng lại (bản mới đã có cảnh báo) | CONFIRMED (bản cũ) |
| L12 | SHOULD | `hook` bước 2, `intuition` SVG1, `recap`, `sym` bước 2 | "Cuối ngày tài khoản đảm bảo không thấp hơn tổng số dư các ví"; bảng sym gán điều này cho "Nghị định 52/2024" | Bản hợp nhất 76/VBHN-NHNN (tôi tải và đọc, `curl` chinhphu.vn) Điều 27 khoản 1: "duy trì tổng số dư trên **tất cả các tài khoản đảm bảo** … **không thấp hơn** tổng số dư tất cả các ví … **tại cùng một thời điểm**". Luật đòi mọi thời điểm, "cuối ngày" chỉ là lúc đối soát; điều khoản kiểm được nằm ở TT40, không phải NĐ52 (CHUA_KIEM) | Dẫn TT40 Điều 27 khoản 1 cho bất biến; nói "mọi lúc, kiểm cuối ngày" | CONFIRMED |
| L12 | SHOULD | `intuition` SVG1 (khung 00030) | mũi tên tím đứt nét từ "tài khoản đảm bảo" sang "ví A: 0 → 2 000 000", không nhãn | Đọc như dòng tiền, trong khi lời đọc nói đây là hai cuốn sổ đối ứng; ví B không có trong hình dù bước sau dùng B | Gắn nhãn "ghi sổ tương ứng" hoặc bỏ mũi tên | PLAUSIBLE |
| L13 | MUST | `quymo` bước 4 (bảng thứ hai, khung 00072) | màn hình: "tụt tới 25% sức chứa; cần chỗ cho 100 Pod thêm"; lời đọc: "sức chứa tụt tới bảy mươi lăm phần trăm" | Màn hình nói khác lời ở một điểm kiến thức. 300/400 = 0,75 (`python`: 300/400 → 0.75): còn 75%, mất 25%; "tụt tới 25%" nghĩa là chỉ còn 25% | Sửa màn hình: "tụt 25% (còn 75%)". Curriculum fix cũng ghi "tụt tới 25% sức chứa" | CONFIRMED |
| L13 | MUST | `quymo` bước 3 (bảng thứ nhất) | lời đọc: "mặc định hai mươi lăm phần trăm luôn hai đợt, vì mỗi đợt thay một phần tư số bản" | Mỗi đợt thay mu+ms = D/4 + D/4 = D/2 (de.md lab: "thay tối đa mu + ms"). Chạy `so_dot(40,10,10)` = 2 (mỗi đợt 20 = một nửa). Nếu mỗi đợt một phần tư thì phải 4 đợt | "vì mỗi đợt thay một nửa số bản (một phần tư thiếu cộng một phần tư thừa)" | CONFIRMED |
| L13 | SHOULD | `quymo` bước 3 + curriculum fix + recap | "mặc định 25% luôn 2 đợt" | Sai khi D ≡ 3 (mod 4) và D=1: `so_dot(D, D//4, -(-D//4))` ra 3 đợt ở D=3,7,11,15,…,39 (chạy D=1..40) | "gần như luôn 2 đợt với D lớn" hoặc ghi điều kiện | CONFIRMED |
| L13 | SHOULD | `check` bước 1 ("Kết quả chạy thật: 24 3 5 True"), `example` | "Kết quả chạy thật" | Đó là chạy mô hình Python do tác giả tự viết từ cùng quy tắc, KHÔNG phải Kubernetes: `source` ghi rõ "KHÔNG chạy trên cụm Kubernetes thật"; Dockerfile, `.gitlab-ci.yml`, Deployment chưa từng được dựng/áp dụng (chỉ `docker build --check` OBSERVED). Chỉ cảnh `quymo` và `practice` ghi "mô phỏng" trên màn hình. Tôi chạy lại: `24 3 5 True` khớp, nhưng nó chỉ chứng minh mô hình khớp chính nó | Ghi "(mô hình Python, chưa chạy trên cụm thật)" ở `check`, `example` | CONFIRMED |
| L13 | SHOULD | `quymo` bước 3 (bảng) | "100 phút, hơn 1 giờ 40" | 200 đợt × 30 s = 6000 s = đúng 100 phút = 1 giờ 40, không "hơn" | bỏ "hơn" | CONFIRMED |
| L13 | MUST | `out/BNX/L13` | chapters.txt: 10 mục, không có "Khi số bản lớn dần", "Tự làm" | spec_sha256 lúc dựng `5e0b3e41…` ≠ YAML `5014e685…`; srt (11-10) không có "bốn trăm bản", không có lab | Dựng lại | CONFIRMED |
| L14 | MUST | `out/BNX/L14` | chapters.txt: 10 mục, hết 14:33; srt cuối: "Bài đó có ước lượng tải và ngân sách thời gian…" | spec_sha256 `12dbc724…` ≠ YAML `fd52c3f3…`; thiếu cảnh `quymo` (mục tiêu 6: 1/100/10 000 bên) và `practice` | Dựng lại | CONFIRMED |
| L14 | SHOULD | `intuition` bước 4 (bảng Điều 11), say tương ứng | "thời hạn truy vấn sau khi khách đồng ý không quá 180 ngày" | TT 64/2024/TT-NHNN Điều 11 khoản 6 (bản dịch EN luatvietnam, đã tải đọc): "not exceeding 180 days … **unless otherwise agreed upon between the customer and the Bank**". Bài bỏ vế "trừ khi khách và ngân hàng thỏa thuận khác" | Thêm điều kiện | CONFIRMED |
| L14 | SHOULD | `hook` bước 1; `sym` bước 2 | "Từ 01/3/2025, ngân hàng mở API … cho bên thứ ba (tổ chức khác ngoài ngân hàng và khách)" | Điều 15: ngân hàng đã kết nối trực tiếp trước đó phải tuân thủ trước 01/3/2027 (lập danh mục trước 01/7/2025); Điều 5 khoản 3: API khởi tạo thanh toán/nạp-rút ví chỉ cấp cho bên thứ ba là ngân hàng hoặc tổ chức trung gian thanh toán. "Mở cho mọi tổ chức" quá rộng | Thêm "có lộ trình chuyển tiếp"; hạn chế đối tượng | CONFIRMED |
| L14 | SHOULD | `sym` bước 1 (màn hình) vs lời đọc | màn hình: "aggregate, gốc (root) — cụm đối tượng được coi là một khối"; lời đọc: "Cụm thực thể là nhóm đối tượng coi như một khối" | Thuật ngữ "cụm thực thể" không xuất hiện trên màn hình, người học không nối được với chữ "aggregate" | Thống nhất một tên | CONFIRMED |

Không phát hiện sai số học nào khác ở cả ba bài (xem mục 5).

## 2) Độ sâu

| Bài | sha16 | Phút | P1 P2 P3 P4 P5 P6 P7 | P8 | P9 | Tổng(P1–P7) | Mất gốc | Cần biết trước | Chỗ thiếu chính |
|---|---|---|---|---|---|---|---|---|---|
| L12 | 6abee8211726b579 | srt cũ 13,1; YAML mới ước ≈14,0 (≤16 ✓) | 2 1 2 2 2 2 2 | 2 | 2 | 13 | ĐỦ | Python `def/return/range/set/break/.items()` dùng ở `quymo` mà không giảng; đơn vị ns/µs/ms; tên "độ phức tạp bình phương" | P2=1: `quymo` bước 3 "tinh = n * (n + 1) // 2" không suy ra vì sao quét = 1+2+…+n; video chưa dựng đủ cảnh |
| L13 | 5014e6856c92e711 | srt cũ 12,8; YAML mới ước ≈14,6 (≤16 ✓) | 1 2 2 2 2 2 1 | 2 | 2 | 12 | ĐỦ | `ENV`, `WORKDIR`, `EXPOSE` (formula bước 1, pitfalls), "Secret của Kubernetes", digest, runner, `docker build --check`; Python tuple/set/`todo.pop()` ở `check` | P1=1: ENV/WORKDIR/Secret không giảng tại chỗ; P7=1: mục tiêu "Viết Dockerfile" và "Gắn ảnh với mã commit" không có việc làm/quiz đo; người học không dựng Docker/K8s thật |
| L14 | fd52c3f3c26fc9be | srt cũ 14,6; YAML mới ước ≈14,5 (≤16 ✓) | 1 2 2 2 2 2 1 | 2 | 2 | 12 | ĐỦ | OpenAPI/HTTP/OAuth scope chỉ gói trong 1 dòng; `Fraction`; SAGA, Outbox chỉ chú thích 1 vế (quiz câu 3); Oracle | P1=1: SAGA/Outbox; P7=1: mục tiêu 1 (chia ngữ cảnh), 3 (liệt kê việc cổng), 4 (mô tả Open API) không có câu hỏi/bài tập đo; DDD chỉ có SVG, không làm tay |

Ghi chú điểm 1: P1 chấm đã coi PYT/JVA là biết (người học đã qua); điểm 0 không có.

## 3) Lab (chạy như người học: đọc de.md, tự viết `mau.py` trong scratchpad, `cham.sh`, rồi mới so loi_giai)

| Bài | Tự làm được | Thời gian | Kẹt ở đâu | mong_doi khớp màn hình |
|---|---|---|---|---|
| L12 | Có | viết ≈5–8 phút (ước); chấm 0,8 s; "ĐÚNG" lần đầu | Không kẹt: đề cho dữ liệu, định dạng `print("vi", *vi.values())`, quy tắc từ chối đều rõ; so sánh `loi_giai.py` chỉ khác cấu trúc if | Khớp từng dòng (so tự động với `show` bước kết quả mong đợi: True) |
| L13 | Có (mô phỏng, không cần Docker/K8s) | ≈8–10 phút (ước); chấm 0,9 s; "ĐÚNG" lần đầu | Không kẹt; "làm tròn xuống thiếu, lên thừa" đã ghi. Lưu ý: không có việc nào chạy Docker/GitLab/K8s thật (kể cả tùy chọn `docker build`, `kind`/`minikube`) | Khớp |
| L14 | Có | ≈8 phút (ước); chấm 0,7 s; "ĐÚNG" lần đầu | Không kẹt; đề nêu rõ công thức cận trên và phép chia `/` | Khớp |

## 4) Người học kẹt ở đâu

- L12: `quymo` bước 3 "tinh = n * (n + 1) // 2 … cách 1 chỉ tính bằng công thức n(n+1)/2" — chưa được cho biết vì sao số phép so sánh là 1+2+…+n (người học không tự kiểm được 5 050).
- L13: `formula` bước 1 Dockerfile: "WORKDIR /src … RUN mvn -q dependency:go-offline" — WORKDIR/ENV/EXPOSE chưa giảng; kẹt nặng hơn ở `check` bước 1 (mã `c, r, k = s = todo.pop()` với bộ ba trạng thái dày đặc).
- L14: `quiz` câu 3 đáp án "giao dịch vượt hai dịch vụ phải dùng SAGA (chuỗi bước bù trừ), Outbox (ghi tin cần gửi cùng giao dịch)" — hai khái niệm chỉ chú thích một vế, người học không hiểu cơ chế.

## 5) Số đã tính lại / mã đã chạy

- L12: 3 đoạn mã trên màn hình (hạn mức 100 triệu, đối soát R1–R3, chạy lại nhật ký) + mã `quymo` (quet_danh_sach/tra_bang ở 100 và 10 000; n(n+1)/2 ở 1 000 000) + ~30 số tính tay/đọc ra (95, 105, 102, 8, 3 000 000, 2 500 000, 300 000, 1 500 000, 9 901,98 lần, 0,2525 ms, 2,50025 s, 25 000,025 s = 6,94 giờ, 0,05 s…): **khớp tất cả**. Lab: ĐÚNG. Không chạy: các `checks:` gọi `alg.*` (module `alg` không nạp), chỉ đọc.
- L13: Dockerfile (30/120/27/108/114 giây), 4 Pod (3, 5, 750, 1 000), 24 trạng thái (`24 3 5 True`), bảng `hang()` 7 dòng, thời gian đợt (1/10/100/5 phút), quiz (4, 7; 4 đợt vs 2 đợt), parse bằng `yaml.safe_load` Deployment (replicas 4, maxUnavailable 1, maxSurge 1, selector/labels khớp, readinessProbe) và `.gitlab-ci.yml` (4 stage, biến, script) — **khớp, cú pháp hợp lệ**; 2 chỗ lời nói sai (mục 1). Chỉ đọc, không chạy: `docker build --check` (không chạy docker; theo hiểu biết, `SecretsUsedInArgOrEnv` có thật, không có quy tắc báo `latest`, khớp lời bài), build Dockerfile, `kubectl`, GitLab runner.
- L14: hàm cổng (10, 14), bảng 1/100/10 000 bên (10/1 000/100 000; 14/1 400/140 000; từ chối 20/2 000/200 000; 0,005/0,5/50 s), thời điểm nhận `[0..10,12,18,24]`, 5/3, 89/6 ≈ 14,83, quiz (10/30; 5, cận 5,5), lab (6/14; 13, cận 13; 300/700; 2,5 s), 60 ngày (31/12/2024 → 01/3/2025), bước debit (300 000 → 100 000), 80+30 = 110: **khớp tất cả**. Lab: ĐÚNG.
- Ba lab: `mau12/13/14.py` tự viết, `cham.sh` in ĐÚNG cả ba.

## 6) Khung hình đã xem (frames/ mới, 14/11) và lỗi hiển thị

L12: 00000 (mở đầu), 00024 (bảng văn bản pháp lý), 00030 (SVG1 hai cuốn sổ), 00033 (SVG2 luồng thuế), 00036, 00046 (mã hạn mức), 00066 (quymo), 00081 (quiz), 00096 (tổng kết) + contact sheet 34 khung. Lỗi: không tràn/đè/cắt; chỉ mũi tên SVG1 không nhãn.
L13: 00029 (SVG pipeline), 00030 (SVG lớp đệm), 00048 (bước Pod), 00057 (bảng đợt), 00072 (quymo, lỗi nội dung 25%), 00096 (kết quả lab) + sheet 35 khung. Không lỗi hiển thị.
L14: 00000 (ngày "01/3/2025" hiện bằng font toán KaTeX, khác chữ xung quanh — nhỏ), 00024 (3 ngữ cảnh), 00027 (cổng), 00030 (Open API), 00069 (bảng N bên), 00093 (đề lab) + sheet 35 khung. Không tràn/đè.

## 7) E51 (giáo án ↔ video) và phút

- L12: `covers` đúng (1,2,3→formula; 4→intuition; 5→quymo; 6→practice); cả 6 mục tiêu có cảnh dạy + đo được trong YAML (quiz/lab); **video dựng cũ thiếu mục tiêu 5, 6** (MUST ở bảng 1). Phút: srt cũ 13,1; YAML mới ≈14,0.
- L13: `covers` đúng cảnh; mục tiêu 1 "Viết Dockerfile" thực tế chỉ đọc Dockerfile (lab dùng danh sách lớp, không viết Dockerfile) — lệch nhẹ; mục tiêu 4 "Gắn ảnh với mã commit" có dạy (formula bước 2 biến IMG) nhưng không đo; mục tiêu 5, 6 ok; **video cũ thiếu 5, 6**. Phút: 12,8 cũ; ≈14,6 mới.
- L14: `covers` đúng (1,3,4→intuition; 2→formula; 5→example; 6→quymo; 7→practice); mục tiêu 1, 3, 4 có dạy nhưng không có bài tập/quiz đo; **video cũ thiếu 6, 7**. Phút: 14,6 cũ; ≈14,5 mới.

## 8) Pháp lý (L12; kèm L14)

| Văn bản | Registry | Bài (YAML hiện tại) | Đối chiếu của tôi |
|---|---|---|---|
| NĐ 52/2024/NĐ-CP | CHUA_KIEM (có thể thay bởi NĐ 320/2025) | Màn hình "cần kiểm lại văn bản hiện hành"; lời đọc "nhưng cần kiểm lại"; không nêu số điều; không nhắc khả năng thay thế | Tồn tại, ngày 15/5/2024, "thanh toán không dùng tiền mặt": xác nhận qua phần căn cứ của TT 64. Nội dung bài gán (bất biến, chỉ ví liên kết tài khoản chính khách) chưa kiểm được ở NĐ52; bất biến thấy ở TT40 Điều 27 khoản 1 |
| TT 40/2024 (76/VBHN) | HIEU_LUC, ORIGINAL | "100 triệu/tháng, tính chuyển tiền và thanh toán, không tính rút về tài khoản liên kết"; ghi "kiểm lại trước khi áp dụng" | Khớp Điều 26 khoản 1 + Điều 25 khoản 2 (rút = điểm a, bị loại). Bài bỏ ngoại lệ ví của đơn vị chấp nhận thanh toán (không sai) |
| TT 41/2025 | HIEU_LUC | "thêm hạn mức riêng ≤ 300 triệu cho một số khoản thiết yếu; hiệu lực 05/11/2025" | Khớp Điều 26 khoản 3 (VBHN) và hiệu lực 05/11/2025; "ngoài hạn mức khoản 1", tổ chức ví "được quy định thêm" (không tự động) |
| TT 19/2021/TT-BTC | SUA_DOI (46/2024; TT 89/2026 chưa rõ) | "đã sửa đổi, cần kiểm lại"; chỉ nói cơ chế số tham chiếu | Không mở được nguồn; bài đúng yêu cầu registry |
| Luật 108/2025/QH15 Điều 14 khoản 5 | HIEU_LUC, SECONDARY | "thay luật cũ từ 01/7/2026; nguồn tổng hợp, cần kiểm lại" | Chưa kiểm được bản gốc; bài ghi rõ |
| TT 64/2024/TT-NHNN (L14) | HIEU_LUC, ORIGINAL | Điều 8, Điều 11, Phụ lục 01, ban hành 31/12/2024, hiệu lực 01/3/2025; lời đọc nói "theo hai bài báo… đọc nguyên văn" | Khớp Điều 8 (hợp đồng, cam kết dùng đúng phạm vi), Điều 11 khoản 5 (tra cứu/rút lại), khoản 6 (180 ngày — thiếu vế "trừ khi thỏa thuận"), ngày; Phụ lục 01 = đặc tả danh mục (Điều 6 khoản 2). Nguồn: bản dịch EN luatvietnam, chưa mở bản Công báo VN |

Kết luận pháp lý: YAML hiện tại làm đúng yêu cầu CHUA_KIEM (có cảnh báo trên màn hình và trong lời đọc, không nêu số điều của NĐ52/TT40/TT41); **video đang có (bản cũ) chưa làm đúng** (lời đọc khẳng định NĐ52 không cảnh báo).

## NHOM B (L15-L17)
# Phần B (agentB): đã đọc 3/3 bài — BNX L15, L16, L17

Ghi chú nền: YAML là bản đọc ở sha16 dưới đây (kiểm lại lúc kết thúc, không đổi). `out/BNX/Lxx/Lxx.mp4/.srt/chapters.txt` dựng ngày 2026-11-12; YAML sửa 2026-11-14 (L15 07:54, L17 08:07, L16 09:04) và thư mục `frames/` được chụp lại sau đó từ YAML mới. Vì vậy: khung hình = YAML hiện tại; `.srt`/`.mp4` = bản cũ (xem lỗi V1). Các thang P1–P9 chấm theo YAML hiện tại + khung hình hiện tại.

## 1. Bảng chuẩn xác

| Bài | Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng đã chạy | Đề xuất | Tin cậy |
|---|---|---|---|---|---|---|
| L15 | MUST (V1) | toàn bài (`out/BNX/L15/L15.srt`, `.mp4`) | SRT: "Ở bài 3 và bài 5, mã truy cập tự mang thông tin cho biết người gọi là ai…"; "viết bằng OpenAPI trước khi viết mã, như bài 1 đã dạy."; cũng có "ở bài 6", "ở bài 13", "ở bài 14" | Video/SRT dựng 2026-11-12 09:01, YAML sửa 2026-11-14 07:54. So `say` (YAML) với SRT bằng difflib: tỉ lệ khớp 0,76 (2236 vs 2311 từ); SRT còn câu nhắc bài khác, mà YAML hiện tại không có. Người học xem mp4 hiện có thì gặp lỗi "như đã học ở bài khác". | Dựng lại video từ YAML hiện tại trước khi chốt | CONFIRMED (trạng thái tệp) |
| L16 | MUST (V1) | toàn bài (`L16.srt`, `.mp4`) | SRT 176 cue, kết thúc 00:19:02; tổng lời đọc 17,9 phút | Bản dựng cũ dài hơn trần 16 phút. Tỉ lệ khớp say↔SRT chỉ 0,60 (YAML 2299 từ vs SRT 3564 từ). YAML hiện tại ước ≈ 12,0 phút (2299 từ ÷ 192 từ/phút = SRT cũ 3564 từ/17,9 phút) nên sau khi dựng lại sẽ dưới trần. | Dựng lại | CONFIRMED |
| L17 | MUST (V1) | toàn bài (`L17.srt`, `.mp4`) | SRT 187 cue, kết thúc 00:21:02; tổng lời đọc 19,9 phút | Vượt trần 16 phút; tỉ lệ khớp say↔SRT 0,53 (YAML 2076 từ vs SRT 4034 từ). YAML hiện tại ≈ 10,8 phút. | Dựng lại | CONFIRMED |
| L15 | SHOULD | practice, step 1–2 + `labs/BNX/L15/de.md` | de.md: "`cung luc o Oracle <số>` — … tải cao điểm × thời gian mỗi lệnh, tính bằng giây … một chữ số thập phân" | Nếu người học làm tròn cao điểm trước rồi nhân: 347 × 0,120 = 41,64 → in 41,6, không phải 41,7 (mong_doi), chấm ra sai dòng 4 dù đúng ý. Bài có dạy dùng số chưa làm tròn (example ②) nhưng de.md không nhắc. Chạy: `python -c "print(347*0.12, 5e6/86400*6*0.12)"` → 41.64 / 41.666. | Thêm vào de.md: "dùng số chưa làm tròn" | CONFIRMED |
| L15 | SHOULD | practice step 1 (màn hình + lời) | "bộ số liệu trong de.md (5 000 000 giao dịch/ngày, cao điểm gấp 6, ngân sách 400 ms, Oracle 120 ms, bể 30 kết nối)" rồi "con du 234 ms" | Màn hình và lời không nêu bốn chặng còn lại (cổng 12, xác thực 6, dịch vụ 25, Redis 3 — chỉ có trong de.md), nên "dư 234" không tính được chỉ từ video. | Nêu 4 chặng trên màn hình | CONFIRMED |
| L15 | SHOULD | quymo, step 2–3 | "lệnh cùng lúc ở Oracle (đếm thật) … 463 … 46 297" | Đếm giả định mỗi lệnh luôn ở Oracle 40 ms; ở 463 hay 46 297 lệnh cùng lúc thực tế Oracle chậm lại (hàng đợi trong chính cơ sở dữ liệu), nên con số chỉ là cận dưới theo mô hình. Bài không nêu điều kiện này. | Thêm một câu điều kiện | PLAUSIBLE |
| L16 | SHOULD | example, BeLuong.java (3/3) | "**Kết quả chạy thật** … số lượt: 3" | Dòng này in `(10 + 4 - 1) / 4`, một phép tính hằng, không đo gì; thời gian "≈ 300 ms" không chương trình nào đo. Chạy BeLuong: in "số luồng đã dùng: 4 / tổng 10 kết quả: 385 / số lượt: 3" đúng, nhưng "số lượt" không phải kết quả quan sát. Tương tự GhepLoiGoi chỉ in `chờ dưới 900 ms: true` (đo thực: 401, 413, 405 ms ở 3 lần chạy, không hiện trên màn hình). | Ghi nhãn "tính từ công thức" hoặc in thời gian đo thật (có ghi chú đổi theo máy) | CONFIRMED |
| L16 | SHOULD | pitfalls, Lỗi 3 (màn hình) | "`orTimeout` chỉ báo lỗi quá hạn cho bên gọi; việc đang chạy không bị huỷ và luồng của bể vẫn bận (chạy thật ở bộ kiểm)." | Khẳng định đúng (chạy thử: `supplyAsync(...).orTimeout(200ms)` ném `CompletionException` ← `TimeoutException` sau 212 ms), nhưng người học không thấy chương trình nào chứng minh ("bộ kiểm" không có trong video/labs); màn hình nói nhiều hơn lời đọc (lời không nhắc orTimeout và điều kiện 1 nhân). | Bỏ hoặc thêm đoạn mã ngắn | PLAUSIBLE |
| L16 | SHOULD | khung hình 00061–00063 (example, ChiaDoi 3/3) | công thức ④⑤ dưới ô "Kết quả chạy thật" | Tử số "1 000 000" và "1 000 000 · 1 000 001" chạm viền cam của ô nổi bật (đã cắt ảnh phóng to kiểm). Vẫn đọc được. | Thêm khoảng cách | CONFIRMED |
| L17 | SHOULD | example, CauHinh/ChayThu (6 màn hình mã) + lệnh `javac … -cp "lib/*"` | "CauHinh.java (trích)"; "ChayThu.java (trích)"; "Biên dịch và chạy (thư viện Spring nằm trong thư mục lib)" | Không gõ lại được thành chương trình chạy. Ghép đúng nguyên văn các đoạn + `}` đóng lớp rồi `javac` với 21 jar ở deps/l17: CauHinh 18 lỗi, ChayThu 15 lỗi. Thiếu: toàn bộ `import` (13+ lớp), hàm `ky(...)` (ký JWT HS256 — cốt lõi của "ta tự ký bốn mã") không hiện ở đâu, trường `static Filter chuoi`, khai lớp/`main` của ChayThu, dấu đóng lớp; không nói lấy jar nào, phiên bản nào, tải ở đâu. Bổ sung đủ các phần đó thì chạy được và ra đúng mọi dòng trên màn hình (xem mục 5). | Hiện `ky()`, danh sách import, danh sách jar+phiên bản (hoặc nói rõ đây là minh hoạ chỉ xem) | CONFIRMED |
| L17 | SHOULD | example, CauHinh.java (1/3) | `KHOA = "khoa-bi-mat-chi-de-hoc-dai-32-byte!!"` và `"khoa-cua-ke-gian-cung-dai-32-byte!!!"` | Chuỗi tự gắn nhãn "dài 32 byte" nhưng đo: `len(...encode())` = 36 byte cả hai. (HS256 cần ≥ 32 byte nên vẫn chạy.) | Sửa nhãn | CONFIRMED |
| L17 | SHOULD | formula step 3 vs example CauHinh | step 3: "dịch vụ tự lấy khoá công khai ở đó" (`issuer-uri`); example: `NimbusJwtDecoder.withSecretKey(khoa)` HmacSHA256, lời: "khoá bí mật" | Hai cách kiểm chữ ký khác loại (khoá công khai bất đối xứng vs khoá chung đối xứng) xuất hiện liền nhau mà không nói vì sao demo đổi sang khoá chung; người học dễ hiểu nhầm cấu hình YAML là cái đang chạy. | Một câu giải thích | CONFIRMED (văn bản) |
| L17 | SHOULD | quymo + quiz câu 3 | "bộ đệm 35 giây", "sổ kiểm mỗi 10 giây" | Hai số này (35 s: thời gian sống bộ đệm danh sách bản của Spring Cloud LoadBalancer; 10 s: chu kỳ kiểm sức khoẻ Consul) trông như số mặc định thật nhưng không được nói là mặc định, cũng không nói bộ đệm giữ cái gì ở đâu (ở cổng). Spring Cloud không có jar → chưa kiểm được nguồn; `source:` của YAML liệt kê Gateway/Commons/Consul 5.0.4 nhưng tôi không mở được `sources_l17`. | Nói "mặc định" + giải thích bộ đệm, hoặc ghi "số minh hoạ" | PLAUSIBLE |
| L17 | SHOULD | example, ChiaTai.java + lời | "chia xoay vòng giao yêu cầu thứ i cho bản thứ i chia lấy dư" | Đúng với mô phỏng (đã chạy: `{bản 1=34, bản 2=33, bản 3=33}`, `{bản 1=50, bản 3=50}`) và bài ghi rõ "MÔ PHỎNG". Nhưng bộ chia thật của Spring Cloud LoadBalancer bắt đầu từ vị trí ngẫu nhiên nên bản nhận dư không cố định là "bản 1". Chưa kiểm vì không có jar. | Thêm "vị trí đầu ngẫu nhiên" | PLAUSIBLE |
| L15, L16, L17 | — | — | — | Không phát hiện lỗi kiến thức/số liệu nào khác (mọi số tính lại khớp; mọi mã chạy ra đúng như màn hình — mục 5). Khẳng định về Spring Security 7 (`authorizeHttpRequests`, `requestMatchers`, `oauth2ResourceServer(m -> m.jwt(...))`, `JwtDecoder`, 14 bộ lọc theo thứ tự trên màn hình, 401 từ trạm 8/13, 403 từ trạm 13, POST không mã → 403 từ CsrfFilter trạm 5) đã chạy thật trên 7.1.2: khớp. YAML Gateway `spring.cloud.gateway.server.webflux.routes` và `{cipher}` của Config: chỉ đọc, chưa chạy (không có jar), khớp cách viết của tài liệu 5.x theo hiểu biết của tôi. | | |

## 2. Độ sâu

Phút = lời đọc. "YAML" = ước lượng từ số từ ÷ 192 từ/phút (hệ số đo từ SRT cũ); "SRT cũ" = đo trực tiếp bản dựng 11-12. Thời gian dừng thêm: L15 25+120 s, L16 25+180 s, L17 25+180 s.

| Bài | sha16 | Phút | P1 P2 P3 P4 P5 P6 P7 | P8 | P9 | Tổng(P1–P7) | Mất gốc | Cần biết trước | Chỗ thiếu chính |
|---|---|---|---|---|---|---|---|---|---|
| L15 | 158019698ce11e00 | YAML ≈ 11,6; SRT cũ 12,0 (hết 12,9) | 1 2 2 2 2 1 1 | 2 | 2 | 11 | GẦN | Swagger = OpenAPI, "lược đồ" (400 sai lược đồ), Couchbase/gRPC/Elasticsearch, cách đo p99 (công cụ tải) | P1: "sai lược đồ" và 3 tên công nghệ ở Lỗi 2 chưa giải (lời nói thay bằng "công cụ tìm kiếm/lời gọi nhị phân"). P6: không dạy CÁCH đo p99 dù lặp "đo trước khi tối ưu"; mô hình Oracle luôn 40 ms. P7: mục tiêu 3 "thành phần nào trả lời yêu cầu nào của JD" không có bảng JD→thành phần, chỉ khẳng định; mục tiêu 4 "trình bày bằng số đo thật" không có bài tập đo/trình bày để kiểm. |
| L16 | 904c311bd58f9103 | YAML ≈ 12,0; SRT cũ 17,9 (hết 19,0) | 1 2 1 2 2 2 1 | 2 | 2 | 11 | GẦN | AtomicInteger, CopyOnWriteArrayList, ConcurrentLinkedQueue, `ConcurrentHashMap.newKeySet`, `Runnable`/`execute` vs `submit`, `static import` (mã dùng, lời chỉ gọi tên theo chức năng); an toàn luồng (có ở BNK:L01) | P1: các lớp tập hợp an toàn luồng không giải vì sao dùng. P3: công thức ④⑤ chạm viền (00061–00063); hình lấy việc của nhau chỉ có một mũi tên, không cho thấy hàng đôi của mỗi luồng. P7: mục tiêu 3 "giải thích cơ chế lấy việc của nhau" chỉ có một câu định nghĩa + hình minh hoạ, bài tự nói "không đo được". |
| L17 | a359137c59a1f8ef | YAML ≈ 10,8; SRT cũ 19,9 (hết 21,0) | 0 2 1 2 2 2 1 | 2 | 2 | 10 | GẦN | "bộ đệm 35 giây" (bộ đệm của cái gì), `exp` = giờ Unix (4102444800 = 2100-01-01; 1700000000 = 2023-11-14), khoá chung vs khoá công khai, CSRF là gì (chỉ gọi "chống giả mạo yêu cầu"), `@Configuration/@EnableWebSecurity`, `->` lambda, JWT cấu trúc 3 phần | P1=0: ≥ 3 mục then chốt chưa giảng (bộ đệm ở quymo/quiz; `exp`/giờ Unix; hai loại khoá). P3: hình 14 trạm chỉ cho thứ tự; 9/14 ô không có tên; cơ chế "trạm 14 ném lỗi, trạm 13 bọc ngoài bắt" chỉ bằng chữ, không có mũi tên. P7: mục tiêu 2 "cấu hình máy chủ tài nguyên" chỉ xem YAML + mã trích, lab không đụng cấu hình, mã không gõ lại được (xem lỗi L17 SHOULD). P8=2 theo lab (Python), nhưng phần Spring không thể tự làm. |

## 3. Lab

| Bài | tự làm được | thời gian | kẹt ở đâu | mong_doi khớp màn hình |
|---|---|---|---|---|
| L15 | có (lần đầu `ĐÚNG`) | ≈ 3 phút | không kẹt; cần đọc `de.md` để lấy 4 chặng còn lại; bẫy làm tròn 41,6 vs 41,7 nếu làm tròn sớm | khớp (5 dòng giống màn hình) |
| L16 | có (3 lần chạy `cham.sh` đều `ĐÚNG`) | ≈ 5 phút | không kẹt (cần biết `ThreadPoolExecutor` 5 tham số — bài có giải thích tham số 4,4,0,SECONDS,ArrayBlockingQueue(2)); kết quả đếm, không phụ thuộc đồng hồ nên ổn định | khớp (5 dòng) |
| L17 | có (`ĐÚNG`); lab Python, mirror hàm `kiem` trên màn hình "tự kiểm" | ≈ 3 phút | không kẹt ở lab; phần Spring của bài không có lab và không gõ lại được | khớp (7 dòng) |

## 4. Người học kẹt ở đâu

- L15: practice step 1 — "ngân sách 400 ms, Oracle 120 ms…" rồi "con du 234 ms": không đủ dữ kiện trên màn hình/lời, phải mở de.md (video có nói "bộ số liệu trong de.md"). Nếu chỉ xem video: pitfalls Lỗi 3 "đo phân vị 99 của từng chặng trước" — không biết đo bằng gì.
- L16: không kẹt ở lab. Chỗ đầu tiên mờ: example, BeLuong 1/3 "`ConcurrentHashMap.newKeySet()`" và `Set<String> luong` — không giải lớp này làm gì và vì sao không dùng HashSet (lời: "tập hợp ghi tên luồng đã làm").
- L17: sym/formula step 3 — "`issuer-uri: https://idp.example.com/issuer`" rồi example "`NimbusJwtDecoder.withSecretKey(khoa)`" và `ky(...)` (không hiện): không biết mã được tạo thế nào, không gõ lại được chương trình; quymo step 1 "danh sách cũ bốn mươi lăm giây, là mười giây chờ lần kiểm kế cộng ba mươi lăm giây bộ đệm" — bộ đệm chưa được giải.

## 5. Số đã tính lại / mã đã chạy

- L15: ≈ 30 số/phép tính, 30 khớp: 86 400; 1 000 000/86 400 = 11,574 (11,6); ×10 = 115,74 (116); 75; 225; 116×0,04 = 4,64; 1e6/24 = 41 667 → 11,574; hình tỉ lệ [47,23,93,187,1050]; Q1 23,148/185,19; Q2 77/173; ×100 = 11 574, ×10 000 = 1 157 407; bể 50/0,04 = 1 250; 11 574−1 250 = 10 324; 1 157 407−1 250 = 1 156 157; hàm `cung_luc` chạy lại: 5 / 463 / 46 297 khớp; đoạn Python trên màn hình in đúng 5 dòng; lab 57,9/347/234/41,7/42. OpenAPI 3.0.3 khớp (chỉ đọc cú pháp). 0 sai.
- L16: 7/7 chương trình Java (BeLuong, HangDoi, GhepLoiGoi, ChiaDoi, KiemLai, HangQuyMo, DungChung) ghép từ màn hình, biên dịch JDK 21.0.13 không sửa, chạy ra đúng mọi dòng trên màn hình; GhepLoiGoi/DungChung/HangDoi chạy lại 5 lần: không đổi (thứ tự xong luôn [số dư, hạn mức, điểm]); đo thời gian GhepLoiGoi 401/413/405 ms; số lá 128 (64 lá 7 812 + 64 lá 7 813) bằng mô phỏng Python; tổng 500 000 500 000; `la(100000)` ngưỡng 5000 = 32; (14+3−1)/3 = 5; quymo 6/996/99 996 và 4/994/99 994; 249 lượt ≈ 25 s, 24 999 lượt = 2 499 900 ms ≈ 42 phút; Q3: 40 việc/s, 600 chờ, 15 s, 0,5 s. Kiểm thêm: `commonPool` song song 11 trên máy này; đặt `-D…common.parallelism=1` thì `supplyAsync` chạy trên `Thread-0` (luồng mới) — khớp câu "bể chung không cho nổi hai luồng thì mỗi việc chạy trên một luồng mới". 0 sai.
- L17: ghép + bổ sung import/`ky()`/trường/main với 21 jar deps/l17 (Spring Security 7.1.2, Framework 7.0.10): in đúng 14 bộ lọc (1 DisableEncodeUrlFilter … 5 CsrfFilter, 8 BearerTokenAuthenticationFilter, 9 TramQuanSat, 12 AnonymousAuthenticationFilter, 13 ExceptionTranslationFilter, 14 AuthorizationFilter); A 401 (có "qua trạm quan sát", `Bearer resource_metadata=…`), B 401 (không có "qua trạm quan sát", `Invalid signature`), C 403 `insufficient_scope`, D 200, E 401 (hết hạn), F POST không mã 403 không qua trạm quan sát, G 200: khớp toàn bộ. ChiaTai (34/33/33; 50/50) và CuaSoLoi (1500; 150 000; 15 000 000) khớp. Python bảng quyết định `[401,401,403,200,401]`, `50 [34,33,33]` khớp. 100×45/3 = 1500; 100×37/3 = 1233,3 → 1234; 90/3 = 30; 90/2 = 45; 10/2 = 5; 250 → [84,83,83]. Lab ĐÚNG. Chỉ đọc, không chạy: Spring Cloud Gateway/Consul/Config/LoadBalancer (không có jar), YAML `application.yml` (3 khối). 1 nhãn sai (36 byte, không 32).

## 6. Khung hình đã xem

Dùng tờ tổng hợp (contact sheet) tất cả khung (4 khung/hàng, đọc được chữ chính) + mở riêng cỡ đầy đủ:
- L15 (96 khung): 00000–00095 qua 4 tờ tổng hợp (mở đầu, bảng prereq, hình kiến trúc, hình ngân sách, hợp đồng API, ví dụ, quymo, pitfalls, quiz, practice, recap); đầy đủ: 00026 (kiến trúc), 00062 (bảng quymo). Không lỗi hiển thị; mỗi khung chỉ chiếm nửa trên, nửa dưới trống (cỡ chữ bảng đọc được).
- L16 (119 khung): 00000–00118 qua 5 tờ; đầy đủ: 00050 (HangDoi 3/3), 00063 (ChiaDoi 3/3), thêm cắt phóng 00063. Lỗi: công thức ④⑤ chạm viền ô nổi bật (00061–00063). Khung mã chữ nhỏ nhưng đọc được; mỗi chương trình tách 3–4 màn hình, người học phải ghép.
- L17 (103 khung): 00000–00102 qua 5 tờ; đầy đủ: 00017 (hình 14 trạm). Không đè/cắt chữ; hình 14 trạm nhãn cỡ nhỏ, 9 ô không nhãn; Lỗi 2 (00069/00070) khung đỏ dày chữ nhỏ, màn hình dài hơn lời đọc.
- Lưu ý: `_frames.txt` (123/177/188 mục) là của bản dựng cũ, không khớp thư mục `frames/` hiện tại (96/119/103 tệp); nên tôi không dùng nó để suy thời điểm.

## 7. E51 (giáo án ↔ video) và phút lời đọc

- Phút lời đọc: xem bảng mục 2. Bản dựng hiện có (SRT cũ): L15 12,0 / L16 17,9 / L17 19,9 phút lời (hết 12,9 / 19,0 / 21,0) → L16, L17 vượt trần 16 phút ở bản đã dựng; YAML hiện tại ước ≈ 11,6 / 12,0 / 10,8 phút (+ dừng 2,4 / 3,4 / 3,4 phút), nằm dưới trần nếu dựng lại.
- `curriculum/bnx.yaml`: objectives của L15, L16, L17 trùng chữ với YAML; `example` khớp mọi số trên màn hình (L15 5/463/46 297 và 1 250; L16 128 lá, 500 000 500 000; L17 50/50 và 401/403/200); `fix` của cả ba bài đều có cảnh dạy (L15 Lỗi 1–3 + quymo; L16 Lỗi 1–3; L17 Lỗi 1–4 + quymo).
- `covers`: L15 đúng (1,2→formula; 3→intuition; 4→check; 5→quymo; 6→practice). L16 đúng (1→practice; 2,3→example; 4→formula). L17 đúng (1→example; 2,3→formula; 4→practice).
- Mục tiêu đo được: L15 mục tiêu 1,2,5,6 đo được (quiz + lab); mục tiêu 3 chỉ dạy một nửa (không có ánh xạ JD→thành phần); mục tiêu 4 không có bài kiểm. L16: 1 (lab), 2 (quiz câu 2), 4 (quiz câu 3 + bảng công cụ) đo được; 3 "giải thích cơ chế lấy việc" chỉ có hình/định nghĩa. L17: 1 (quiz câu 1 + lab), 4 (quiz câu 2–3 + lab phần 2) đo được; 2 "cấu hình máy chủ tài nguyên" không có bài kiểm/ lab; 3 (vai trò cổng/Consul/Config) có bảng ở step 5 và recap nhưng không có câu kiểm riêng.
- Điều kiện chặn: không bị giới hạn quota trong lần chạy này; phần chưa làm: Spring Cloud (không có jar), `sources_l16/l17` (cấm mở), nghe tai.

## NHOM C (L18-L20)
# Phần C (BNX L18, L19, L20): đã đọc 3/3 bài

Ghi chú nền (áp dụng cả ba bài):
- YAML đọc trọn; sha16 lúc đọc: L18 `98b729a0f8ee781e`, L19 `76dd738213b6f8ff`, L20 `64b4f5badd8741c5`.
- **Video đã dựng KHÔNG khớp YAML hiện tại.** `build_report.json` ghi spec_sha256 L18 `47f5273d…`, L19 `65c78e1b…`, L20 `b72b30cf…`, khác sha256 của YAML hiện tại (L18 `98b729a0…`, L19 `76dd7382…`, L20 `64b4f5ba…`). mp4/srt dựng 2026-11-12, YAML sửa 2026-11-14 (08:12–09:07). Thư mục `frames/` đã dựng lại từ YAML mới (117/112/107 png, phụ đề trên khung = `say` mới), nhưng `_frames.txt` (155/169/186 mục), `.srt`, `.mp4`, `chapters.txt` vẫn là bản cũ. SRT dài hơn YAML: 3214/3617/3590 từ so với 2295/2296/2253 từ trong `say`.
- Vì vậy mọi thời điểm khung hình tôi chọn theo thứ tự tệp png (bản mới), không cộng dồn `_frames.txt` (đã cũ). Lời đọc cũ có nội dung YAML mới đã bỏ: @ParameterizedTest, spy, ArgumentCaptor, @Mock + extension (L18); mã hàng rào, bộ nhớ đầy/chính sách đẩy khoá, bản sao chép bất đồng bộ, mô phỏng Python đồng hồ giả (L19); lệnh `defer` (L20). Tôi đánh giá YAML hiện tại, và chỉ dùng SRT để đo độ dài bản dựng.
- Docker/Redis không chạy theo yêu cầu. Mã Java (JDK 21.0.x, JUnit Platform 1.14.4, Mockito 5.24.0 từ `audit/bnx/deps/l18`), Python, Go 1.25.5 (có gcc w64devkit cho `-race`) đều chạy thật, tệp tạm ở scratchpad/agentC.

---
## L18 — JUnit 5 + Mockito

### (1) Chuẩn xác
| Bài | Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng đã chạy | Đề xuất | Tin cậy |
|---|---|---|---|---|---|---|
| L18 | SHOULD | `covers`/`practice` ↔ `curriculum/bnx.yaml` L18 mục tiêu 1–3 | mục tiêu 1 “Viết ca kiểm JUnit 5 cho từng nhánh của một hàm…”, 2 “Thay phần phụ thuộc bên ngoài bằng đối tượng giả của Mockito”, 3 “Kiểm một lời gọi…”; `covers: objective 1 → scene practice`; `de.md`: “Lab chạy được chỉ với JDK, không cần JUnit hay Mockito” | Lab tự làm chỉ viết hàm `ca()` thủ công và cổng giả bằng lambda, không có `@Test`, `assertEquals`, `mock`, `verify`. Mục tiêu đo bằng việc “viết ca kiểm JUnit 5 / dùng Mockito” nên người học không bao giờ tự làm chính điều mục tiêu nêu (chỉ xem). Đã chạy `cham.sh BNX L18` bằng lời giải tự viết: ĐÚNG, không dùng thư viện nào. | Thêm bước tuỳ chọn của lab có jar (hoặc sửa mục tiêu thành “đọc/chạy”) | CONFIRMED |
| L18 | SHOULD | quymo, bảng cuối (“cách / được / mất”) | “2k + 1 ca phải viết; nên sinh từ bảng” | Khuyên sinh ca từ bảng nhưng không chỉ cách (JUnit 5 có @ParameterizedTest + nguồn đối số; lời đọc cũ có nhắc, YAML mới đã bỏ). Không sai, nhưng là lời khuyên không kèm cách làm. | Thêm 1 cảnh ngắn @ParameterizedTest hoặc bỏ câu | PLAUSIBLE |
| L18 | SHOULD | build `out/BNX/L18` | `chapters.txt`: tổng 16:47 (srt kết thúc 16:46,78; lời đọc 15,74 phút) | Bản dựng cũ không phải bản của YAML hiện tại (xem ghi chú nền); tổng thời lượng bản cũ 16,78 phút vượt trần 16. Ước lượng bản mới: 2295 từ ÷ 3,40 từ/giây = 11,2 phút lời + 265 s dừng = 15,7 phút. | Dựng lại video từ YAML mới | CONFIRMED (bản cũ), PLAUSIBLE (ước lượng mới) |

Đã kiểm, không lỗi: mọi khẳng định Mockito/JUnit trong YAML (mock trả mặc định false/0/null khi chưa dặn; `verify(times(1))`; `assertThrows`; JUnit tạo bản thể lớp kiểm mới mỗi ca; Java 21 in cảnh báo agent động khi Mockito tự gắn; thứ tự chạy phiCao, phiVua, bien, mienPhi) đều khớp khi chạy thật.

### (2) Độ sâu
| Bài | sha16 | Phút | P1 P2 P3 P4 P5 P6 P7 | P8 | P9 | Tổng | Mất gốc | Cần biết trước | Chỗ thiếu chính |
|---|---|---|---|---|---|---|---|---|---|
| L18 | 98b729a0f8ee781e | YAML ước 15,7 (lời 11,2 + dừng 4,4); bản dựng cũ 15,74 lời / 16,78 tổng | 1 2 2 2 2 1 1 | 2 | 2 | 11 | GẦN | classpath/jar và `-cp "lib/*"`, `sed -i`, lambda, `static`, `java.time` (Instant, ZoneOffset), `Arrays.binarySearch`, hàm tạo | P1: classpath/`lib/` và `sed -i` dùng không giảng, không nói lấy jar ở đâu (example, bước biên dịch). P6: không có @ParameterizedTest, @BeforeEach/lifecycle, spy, ArgumentCaptor, strict stubs (YAML mới bỏ; lời đọc cũ có). P7: lab không dùng JUnit/Mockito (xem bảng 1). |

Điểm 2 có ghi chú: P2 `BoCa` dùng `binarySearch` với `-i - 1` không giảng nhưng kết quả kiểm lại được; P5 dừng 25 giây cho ba câu (câu 3 là quyết định) hơi ngắn.

### (3) Lab
| Bài | tự làm được | thời gian | kẹt ở đâu | mong_doi khớp màn hình |
|---|---|---|---|---|
| L18 | có | khoảng 3 phút viết + 1,8 s chạy; `cham.sh` in ĐÚNG ở lần đầu; `loi_giai.java` cũng ĐÚNG | không kẹt (`de.md` chép sẵn `tinh/chuyen/kip`, chỉ cần viết `ca`, lambda, `Clock.fixed`); người chưa từng dùng `Instant.parse("…+07:00")` phải chép từ video | khớp: 9 dòng trên màn hình `mong_doi` trùng `mong_doi.txt` từng dòng |

### (4) Người học kẹt ở đâu
example, bước “Biên dịch rồi chạy bằng JUnit Platform (thư viện nằm trong thư mục lib)”: `javac -encoding UTF-8 -cp "lib/*" -d out Phi.java PhiTest.java` — không nói tải `junit-platform-console-standalone-1.14.4.jar` từ đâu, `-cp` là gì; kẹt khi muốn tự chạy lại ví dụ (lab thì không kẹt).

### (5) Số tính lại / mã đã chạy
- Java chạy thật: Phi.java (lỗi `<=`) + PhiTest → 3 đạt/1 trượt, `expected: <5500> but was: <5000>`, `PhiTest.bien(PhiTest.java:8)`, thứ tự ca đúng như màn hình; sau sửa `sed` → 4/4 đạt; ChuyenTienTest + TuChoiTest (Mockito 5.24.0) → 2/2 đạt, có cảnh báo agent động trên stderr như lời đọc; Main đối tượng giả viết tay → `5000 1 2005000`; Main đồng hồ → `true`/`false`; BoCa → ba dòng `3/2, 5/0; 201/200, 401/0; 2001/2000, 4001/0` khớp đúng chữ.
- Số: 5500−5000=500; 20000×500=10 000 000; 2 000 000+5000=2 005 000; 20 000 000+5500=20 005 500; quiz 499999/500000/9999999 → 0/5000/5000 (mã lỗi cũng cho cùng ba giá trị); 90×10+10×2000=20 900 ms; 100×2000/(100×10)=200; 4001×10 ms=40,01 s; 4001×2000 ms=8 002 000 ms=2,22 giờ; k=2/200/2000 → 3/201/2001 và 5/401/4001. Tổng khoảng 36 giá trị/mã, 36 khớp. Lab tự viết + lời giải: khớp.

### (6) Khung hình đã xem
00000, 00022, 00036, 00050, 00070, 00092, 00104, 00116 (.png trong `out/BNX/L18/frames/`). Không thấy chữ tràn/đè/cắt; hình SVG nằm nửa trên, khoảng trống phía dưới lớn (thẩm mỹ, không ảnh hưởng đọc). Cột “chạy 10 ms mỗi ca” trong bảng quy mô không ghi rõ tính cho bộ nào (đúng là bộ “sát mốc”), lời đọc làm rõ.

### (7) E51 + phút
- Mục tiêu 1 (ca JUnit từng nhánh, đọc bản báo): dạy ở formula bước 2–3 + example, đo ở quiz câu 1; `covers` ghi `practice` nhưng lab không dùng JUnit (SHOULD ở bảng 1). Mục tiêu 2 (Mockito): example (ChuyenTienTest), `covers: example` đúng; lab không đo. Mục tiêu 3 (verify 1 lần đúng tham số): example + quiz câu 2, đúng. Mục tiêu 4 (đồng hồ/mạng/thứ tự): pitfalls lỗi 3 + chạy Clock, `covers: pitfalls` đúng; không có lab đo riêng (lab phần 3 có `Clock.fixed`, đo được). Curriculum `example`/`fix` khớp bài.
- Phút lời đọc: bản dựng hiện có 15,74 (lời) / 16,78 (tổng có dừng) — vượt trần ở tổng; ước lượng YAML hiện tại 11,2 lời, 15,7 tổng.

---
## L19 — Redis nâng cao

### (1) Chuẩn xác
| Bài | Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng đã chạy | Đề xuất | Tin cậy |
|---|---|---|---|---|---|---|
| L19 | MUST | build `out/BNX/L19` | `.srt` kết thúc 18:48; lời đọc 17,72 phút (168 cue, tính từ srt) | Vượt trần 16 phút của bản dựng hiện có (bản cũ, không phải YAML hiện tại). Ước lượng YAML mới: 2296 từ ÷ 3,40 = 11,25 phút lời + 205 s dừng = 14,7 phút. | Dựng lại từ YAML mới và đo lại | CONFIRMED (bản cũ) |
| L19 | SHOULD | hook, step 1 (màn hình + lời đọc) | “Trên CV có bốn dòng về Redis để chặn chuyện này: Redis Cluster, khoá SET … NX EX 300, khử trùng …”; lời: “Bốn kỹ thuật Redis chặn chuyện này là cụm nhiều nút, khoá có hạn, khử trùng và danh sách đen” | “Chuyện này” là bấm giải ngân hai lần. Redis Cluster chia khoá theo khe để mở rộng bộ nhớ/tải, không chặn yêu cầu trùng; chính bài (recap) coi lớp chặn là khoá + ràng buộc duy nhất ở CSDL. Gom Cluster vào “kỹ thuật chặn” gây hiểu sai vai trò. | Đổi thành “bốn dòng CV về Redis; ba dòng chặn trùng/thu hồi, Cluster lo mở rộng” | CONFIRMED (văn bản) |
| L19 | SHOULD | intuition, step 2 (hình hạn 60 giây), lời đọc | “Giây không đặt được nên được xử lý, giây ba mươi gặp mục còn sống nên bị từ chối” (phụ đề khung 00021) | “Giây không” (giây 0) viết không dấu phẩy dễ đọc thành “giây không đặt được” = đặt không được, ngược nghĩa “đặt được → xử lý”. Người nghe chỉ có tiếng, không thấy chữ. | Viết “Ở giây 0, đặt được nên được xử lý” (bản dựng cũ dùng “Ở giây không, yêu cầu tới lần đầu, đặt được mục”) | CONFIRMED (văn bản) |

Đã kiểm, không lỗi: CRC16("foo")=44950, khe 12182 nút 3 (khớp ví dụ chuẩn của đặc tả Redis); `CRC16("123456789")=0x31c3`; dải 0–5460/5461–10922/10923–16383 (nút giữa 5462 khe); `DELEX … IFEQ` có từ 8.4.0, trả 0/1 (đã đối chiếu trang lệnh DELEX trên redis.io); TTL −2/−1; hash tag và `{}` rỗng; `SET NX EX` + mã chủ khoá; CROSSSLOT khi khác khe.
Chưa kiểm được: các đầu ra Docker/Redis thật (không chạy Docker), “Redis 8.10.3” (README ghi ảnh `redis:8.10.3`, chưa tự kiểm). Bài ghi rõ phần đo bằng Python (quymo: “Hai cỡ đầu đo thật bằng Python (cỡ 3 000 khoá cũng đã đối chiếu với Redis thật)… dòng cuối là mô hình, chưa đo”) và lab “không cần Redis”.

### (2) Độ sâu
| Bài | sha16 | Phút | P1 P2 P3 P4 P5 P6 P7 | P8 | P9 | Tổng | Mất gốc | Cần biết trước | Chỗ thiếu chính |
|---|---|---|---|---|---|---|---|---|---|
| L19 | 76dd738213b6f8ff | YAML ước 14,7 (lời 11,3 + dừng 3,4); bản dựng cũ 17,72 lời / 18,80 tổng | 1 2 2 2 2 1 2 | 2 | 2 | 12 | ĐỦ | Docker (`docker run/exec`, heredoc `<<'EOF'`, hàm shell `r()`), nút chính/nút bản sao (primary/replica), thu gom rác, ràng buộc duy nhất của CSDL, chuỗi byte/hệ 16 | P1: “nút chính hỏng trước khi nút bản sao nhận khoá” (pitfalls lỗi 3, bảng quiz câu 3) dùng khái niệm bản sao chưa giảng; Docker không giảng. P6: không có Redlock và tranh cãi, mã hàng rào (fencing token) chỉ còn ở lời đọc cũ, không có chính sách đẩy khoá khi đầy bộ nhớ, resharding/ASK, SET … PX; vì vậy “khoá phân tán” chỉ nói tới “không tuyệt đối”. |

### (3) Lab
| Bài | tự làm được | thời gian | kẹt ở đâu | mong_doi khớp màn hình |
|---|---|---|---|---|
| L19 | có | khoảng 4 phút viết; `cham.sh` 4,1 s ĐÚNG; `loi_giai.py` ĐÚNG | không kẹt; luật thẻ băm viết sẵn trong `de.md` nhưng thuật toán “`{` đầu và `}` đầu sau nó, không rỗng” phải suy từ ví dụ video (đã có ở cảnh quymo PhanBo.py) | khớp: 9 dòng trùng `mong_doi.txt` |

### (4) Người học kẹt ở đâu
example, bước “Dựng cụm ba nút thật (… trong một container Docker)”: `docker run -d --name bnx-l19-redis redis:8.10.3 …`, `D="docker exec -i bnx-l19-redis"`, `r() { $D redis-cli … }` — Docker và hàm shell không giảng; không tự chạy lại được ví dụ Redis thật (lab Python thì làm được).

### (5) Số tính lại / mã đã chạy
Python (crc16 tự viết + `binascii.crc_hqx`): `0x31c3 44950 12182`; ba dải khớp; khe `acc:1`=16276 (nút 3), `acc:2`=4087 (nút 1), `{acc}:1/2`=12007 (nút 3), `dedup:TX1001`=9306 (nút 2), `bl:jti-0000`=1074 (nút 1), `loan:disb:{A1001}`=1830 vs `loan:disb:A1001`=5075, `hello`=866 (50018−49152=866, nút 1), `dedup:TX9`=11819, `loan:disb:B7`=13590 (nút 4 trong cụm 4 nút), `{acc}:5/6`=12007; mô phỏng PhanBo.py: 3000 khoá → [994, 994, 1012] và [0,0,3000]; 300000 → [100008, 99949, 100043] và [0,0,300000], lệch lớn nhất 1,2% (“chưa tới hai phần trăm” đúng). Số học: 44950−2×16384=12182; 16384−3×5461=1; 300−120=180; 320−300=20; 300−60=240; 900−250=650; 100×60=6000, 10 000×60=600 000, 1 000 000×60=60 000 000. Khoảng 34 giá trị, 34 khớp. Chỉ đọc, không chạy: các khối `docker`/`redis-cli` (không chạy Docker); các số MOVED/Redirected/slot (9306 cổng 7001, 1074 cổng 7000, 12007 cổng 7002) khớp phép tính nút ↔ cổng nhưng đầu ra Redis thật chưa tự kiểm.

### (6) Khung hình đã xem
00000, 00021, 00040, 00050, 00072, 00088, 00111. Không có chữ tràn/đè/cắt. Bảng quy mô trộn hai thang (số khoá 3 000/300 000/30 000 000 và tốc độ 100/10 000/1 000 000 yêu cầu/giây) trong cùng hàng, đã có ghi chú “mô hình”.

### (7) E51 + phút
- Mục tiêu 1 (tính khe, nút trong cụm 3 nút): example + quiz câu 1 + lab; `covers: example` đúng, đo được. Mục tiêu 2 (SET NX EX, vì sao cần mã chủ khoá): formula bước 4 + pitfalls lỗi 1; `covers: formula` đúng, đo ở quiz câu 3 (một phần). Mục tiêu 3 (khử trùng hạn 60 giây): example, quiz câu 2, lab hạn 90; `covers: practice` đúng. Mục tiêu 4 (danh sách đen): formula bước 5 + example + quiz câu 2 + lab; `covers: example` đúng. Curriculum `example` (12182, ba dải, hạn 60/giây 30/giây 61, 240 giây) và `fix` (3 ý) đều có trong bài.
- Phút lời đọc: bản dựng hiện có 17,72 lời / 18,80 tổng (vượt 16); ước lượng YAML hiện tại 11,3 lời / 14,7 tổng.

---
## L20 — Go goroutine, kênh, HTTP

### (1) Chuẩn xác
| Bài | Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng đã chạy | Đề xuất | Tin cậy |
|---|---|---|---|---|---|---|
| L20 | MUST | build `out/BNX/L20` | `.srt` kết thúc 19:34; lời đọc 18,43 phút (185 cue) | Vượt trần 16 phút ở bản dựng hiện có (bản cũ). Ước lượng YAML mới: 2253 từ ÷ 3,25 = 11,6 phút lời + 145 s dừng = 14,0 phút. | Dựng lại từ YAML mới và đo lại | CONFIRMED (bản cũ) |
| L20 | SHOULD | example, “main.go (hết): gọi ba yêu cầu, hai chỗ lược kiểm lỗi cho vừa khung” | tiêu đề cảnh “hai chỗ lược kiểm lỗi”; lời đọc “lược kiểm lỗi ở hai chỗ” | Mã trên màn hình bỏ lỗi ở ba chỗ: `ln, _ := net.Listen(…)` (cảnh trước), `req, _ := http.NewRequest(…)`, `than, _ := io.ReadAll(…)`. Lời nói hai nhưng có ba; bài lại dạy “bỏ qua lỗi thì chương trình chạy tiếp với giá trị không”. | Sửa thành “vài chỗ” hoặc kiểm đủ | CONFIRMED |
| L20 | SHOULD | `curriculum` mục tiêu 4 ↔ bài | “Viết một dịch vụ HTTP nhỏ và nói bộ khung Fiber thêm gì lên trên”; `covers: objective 4 → example`; lab chỉ có bộ đếm và kênh | Người học chỉ xem mã HTTP/Fiber, không có bước tự viết; mục tiêu 1 (“đọc và chạy chương trình Go có hàm, cấu trúc, xử lý lỗi”) cũng chỉ có phần đọc, lab không đụng struct/error. Mục tiêu “viết” không đo được. | Thêm phần 3 cho lab (viết /suc-khoe) hoặc đổi chữ mục tiêu | CONFIRMED |
| L20 | SHOULD | quiz câu 3, lời giải | “Giao dịch ngân hàng thường chọn giới hạn rồi từ chối sớm, vì khách không chờ lâu được.” | Khẳng định tập quán nghề không kèm nguồn (phần tính 2×1000/50=40 việc/giây, dư 10, 600 việc sau 60 s, 20/40=0,5 s đúng). | Nói “nên cân nhắc” hoặc dẫn nguồn | PLAUSIBLE |

Đã kiểm, không lỗi: mọi mã Go trên màn hình chạy ra đúng kết quả đã ghi (bảng (5)); xác nhận `-race` in `WARNING: DATA RACE` và `exit status 66` (có gcc); 405 khi sai phương thức, 404, mẫu `GET /suc-khoe` cần Go ≥ 1.22 (chạy Go 1.25.5); kênh đệm 3 gửi 4 giá trị; bộ đếm không khoá nằm giữa 1 và số luồng. Chưa kiểm được nguồn: “Fiber … ở bản v2: không còn được bảo trì tích cực” (không mở được README ở nhánh v2; bài chạy Fiber v2.52.16 từ `audit/bnx/deps/l20/fiber`, tôi không chạy lại Fiber vì cần mạng/vendor).
Phép đo phụ thuộc máy: bảng quymo ghi rõ “Số đo trên máy này (Go 1.25.5, Windows), làm tròn xuống nghìn byte; đổi theo phiên bản Go và hệ điều hành” (đạt). Cảnh “Lỗi 3” dùng `time.Sleep(200ms)` rồi `NumGoroutine`, kết quả ổn định ở 3 lần chạy của tôi (1 và 1001), không nói phụ thuộc thời gian.

### (2) Độ sâu
| Bài | sha16 | Phút | P1 P2 P3 P4 P5 P6 P7 | P8 | P9 | Tổng | Mất gốc | Cần biết trước | Chỗ thiếu chính |
|---|---|---|---|---|---|---|---|---|---|
| L20 | 64b4f5badd8741c5 | YAML ước 14,0 (lời 11,6 + dừng 2,4); bản dựng cũ 18,43 lời / 19,58 tổng | 0 2 2 2 2 1 1 | 2 | 2 | 10 | GẦN | cú pháp Go: `defer`, `:=`, `func(){…}()` (hàm vô danh), `struct`, `for … range`, `_`, con trỏ `&`; cài Go; `grep`/pipe (`2>&1 | grep | uniq`) | P1: khối mã Go dùng `defer nhom.Done()`, `:=`, hàm vô danh, `range` mà YAML không có giải thích nào (bảng sym chỉ giải mã `go f()`, WaitGroup, Mutex, chan, select, error, -race, Fiber; lời đọc cũ mới có câu về `defer`), dù mục tiêu 1 là “đọc và chạy một chương trình Go”. P6: không nói bộ lập lịch (G, M, P), deadlock (“all goroutines are asleep”), `context`, vòng lặp Go 1.22 (biến lặp theo từng vòng), kênh không đệm đồng bộ; chỉ có rò rỉ, nguyên tử, -race. P7: mục tiêu 1 và 4 không có bước tự làm (bảng 1). |

### (3) Lab
| Bài | tự làm được | thời gian | kẹt ở đâu | mong_doi khớp màn hình |
|---|---|---|---|---|
| L20 | có | khoảng 5 phút viết; lần chạy đầu 19,8 s (nạp bộ nhớ đệm Go), các lần sau nhanh; chạy 4 lần liên tiếp đều ĐÚNG; `loi_giai.sh` ĐÚNG | không kẹt về logic (không có số đo, đầu ra xác định, ổn định). Người mới phải tự biết cú pháp `defer`/`select` (có gợi ý “Nếu kẹt”); cài Go chỉ có đường dẫn trong `de.md`, video chỉ nói “cần cài Go” | khớp: 6 dòng trùng `mong_doi.txt` |

### (4) Người học kẹt ở đâu
example, cảnh đầu “main.go (trích): cấu trúc tài khoản và hàm trả lỗi”: `type TaiKhoan struct{ So string; SoDu int }`, `func rut(tk TaiKhoan, tien int) (TaiKhoan, error)`, và cảnh 4 `defer nhom.Done()` — cú pháp Go chưa từng được giảng; người mới theo được ý nghĩa nhưng không đọc được mã.

### (5) Số tính lại / mã đã chạy
Go 1.25.5 chạy thật 8 chương trình trên màn hình + lab: rút 200/400 → “rut 200 xong, con 300 / rut 400 loi: khong du so du - so du van 300”; bộ đếm có khoá → 1000; bỏ khoá (100 lần chạy) → 99 lần <1000, 1 lần =1000, nhỏ nhất 964 (đúng ý “có lần thấp hơn 1000”); `-race` → “WARNING: DATA RACE / exit status 66”; select kênh đệm 3 → 7 dòng khớp từng chữ; HTTP chuẩn → 200/405/404 đúng chữ; nguyên tử + kênh → “atomic: 1000 - qua kenh: 1000”; đo ngăn xếp → “8 / 7 / 7 nghin byte” ở cả 6 lần chạy (1 lần + 5 lần) khớp bảng; rò rỉ → “1” và “1001” khớp. Không chạy: Fiber (cần mô-đun/mạng). Số học: 3−2=1; 500−200=300; 1000×1=1000; 5+1=6; 2×1000/50=40; 50−40=10, ×60=600; 20/40=0,5; 1000×8=8, 10 000×7=70, 100 000×7=700 (triệu byte). Khoảng 22 giá trị, 22 khớp (Fiber không tính).

### (6) Khung hình đã xem
00000, 00018, 00060, 00068, 00080, 00106. Không có chữ tràn/đè/cắt; mã Go bị chia nhiều cảnh (“trích” / “hết”) nên có cảnh dừng giữa hàm (vd. kết thúc ở `go func() {`), đọc được nhưng mã hiện nửa chừng.

### (7) E51 + phút
- Mục tiêu 1 (đọc/chạy chương trình Go có hàm, cấu trúc, lỗi): example đúng, nhưng chỉ đọc (SHOULD). 2 (WaitGroup): example đúng. 3 (kênh có/không đệm, lúc nào bị chặn): intuition + example + quiz câu 1, đúng, đo được. 4 (viết dịch vụ HTTP + Fiber): chỉ xem, không đo (SHOULD). 5 (ngăn xếp ở 1 000/10 000/100 000): quymo, đúng, có số đo. 6 (viết chương trình có khoá + kênh đệm 2): practice, đúng, đo được bằng `cham.sh`. Curriculum `example` (1000 goroutine khoá/bỏ khoá + -race; kênh đệm 3; /suc-khoe 200) và `fix` (3 ý) có trong bài.
- Phút lời đọc: bản dựng hiện có 18,43 lời / 19,58 tổng (vượt 16); ước lượng YAML hiện tại 11,6 lời / 14,0 tổng.

---
## Tổng kết ngắn cho người điều phối
- MUST: 2 (L19 và L20 bản dựng cũ vượt trần 16 phút; cả hai bản dựng cũ không khớp YAML mới). Không có MUST về kiến thức.
- SHOULD: 8 (L18: 3, L19: 2, L20: 3, gồm 1 PLAUSIBLE ở L20, 1 ở L18).
- Khuyến nghị: dựng lại ba video từ YAML hiện tại rồi đo lại thời lượng và so SRT ↔ `say`; trước khi phát hành, kiểm tra `_frames.txt`/`chapters.txt` mới.

## NHOM D (L21-L23)
# Phần D — BNX L21, L22, L23: đã đọc 3/3 bài (đọc trọn YAML, mục curriculum, SRT, ≥6 khung hình/bài, chạy lab và mã)

Ghi chú chung (ảnh hưởng cả ba bài):
- sha16 lúc đọc: L21 `eb8f0d56a3c4d20c`, L22 `80a5e8f581ea1152`, L23 `d40f5fa0d2aefed1` (kiểm lại lúc kết thúc, không đổi).
- **Video đã dựng KHÁC YAML hiện tại.** YAML sửa 2026-11-14 (L21 07:20, L22 08:52, L23 07:48); `L2x.mp4`, `L2x.srt`, `chapters.txt`, `_frames.txt` dựng 2026-11-12 (L21 15:13, L22 16:13, L23 16:40; `build_report.json` ghi `spec_sha256` L21 = d93350ea…, khác sha hiện tại). Thư mục `frames/*.png` (106/103/103 tệp) được chụp lại 2026-11-14 từ YAML mới, nên khung hình khớp YAML mới nhưng `.srt`/`.mp4` thì không. Tôi chấm nội dung theo YAML hiện tại + khung hình mới; `.srt` chỉ dùng để đo thời lượng của bản đã dựng.
- Ước lượng phút lời đọc của YAML hiện tại: số từ `say` × tốc độ thật của SRT cũ (≈194 từ/phút) + `pause` (25 s + 120 s). Sai số ±1 phút (chưa có TTS thật).

## Bài L21 — Hệ thống cho vay số (LOS/LMS, DTI, thẻ điểm, ký số, dấu vân tay thiết bị, OFS)
Lưu ý phạm vi: bài KHÔNG có lãi, kỳ trả hay bảng khấu hao (khác mô tả giao việc). Số tiền duy nhất là DTI, thẻ điểm, mã băm, nhóm nợ theo số ngày.

### (1) Chuẩn xác
| Bài | Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng đã chạy | Đề xuất | Tin cậy |
|---|---|---|---|---|---|---|
| L21 | MUST (quy trình) | cả video; chapters.txt | chapters.txt kết thúc `14:50 Chuỗi logic, góc phỏng vấn…`, không có cảnh "Tự làm" | mp4/srt dựng 11-12 từ spec cũ (spec_sha d93350ea…, 164 cue, 2952 từ); YAML nay 2157 từ, có cảnh `practice` (mục tiêu 7, `covers`). Người học xem mp4 hiện có không được dạy việc tự làm mà `de.md` cần; quiz/tổng kết cũng khác chữ. Lệnh: so mtime, `build_report.json`, `chapters.txt`, đếm từ bằng Python | Dựng lại mp4/srt/chapters từ YAML hiện tại | CONFIRMED |
| L21 | SHOULD | scene `sym` step 2 (hàm `nhom_no`, chú thích) + source | `Thông tư 31/2024/TT-NHNN, Điều 10` | Đối chiếu ngoài: Điều 10 khoản 1 điểm a(ii) "quá hạn dưới 10 ngày", b(i) "đến 90 ngày", c(i) "91–180", d(i) "181–360", đ(i) ">360" khớp mã (kết quả đọc từ english.luatvietnam.vn, bản dịch). NHƯNG tìm web cho thấy TT 37/2025/TT-NHNN (31-10-2025) sửa đổi, bổ sung một số điều của TT 31/2024; `audit/legal/registry.yaml` ghi TT 31 `HIEU_LUC` không nhắc sửa đổi. Chưa kiểm được Điều 10 có bị đổi không. Bài đã nhắc "đọc nguyên văn" nên chỉ thiếu ghi bản sửa đổi | Thêm TT 37/2025 vào registry và dòng chú thích, hoặc ghi "chưa đối chiếu bản hợp nhất" | PLAUSIBLE |
| L21 | SHOULD | step 6 (openssl) "Kết quả chạy thật" | `Verified OK / Verification failure / Verified OK` | Chạy thật openssl 3.5.5: lệnh verify thất bại in thêm 2 dòng lỗi stderr (`error:02000068:rsa routines:ossl_rsa_verify:bad signature`, `error:1C880004:Provider routines…`) trước chữ "Verification failure". Màn hình lược bỏ, người học gõ lại sẽ thấy khác | Ghi chú "kèm vài dòng error trên stderr" hoặc thêm `2>/dev/null` | CONFIRMED |
| L21 | — | khác | — | Không phát hiện lỗi kiến thức ở bảng nhóm nợ (9→1, 10→2, 90→2, 91→3, 180→3, 181→4, 360→4, 361→5), DTI, thẻ điểm, băm, vân tay, OFS, quy mô, đáp án quiz | | |

### (2) Độ sâu
| Bài | sha16 | Phút | P1 P2 P3 P4 P5 P6 P7 | P8 | P9 | Tổng | Mất gốc | Cần biết trước | Chỗ thiếu chính |
|---|---|---|---|---|---|---|---|---|---|
| L21 | eb8f0d56a3c4d20c | YAML ≈ 11,1 nói + 2,4 dừng ≈ 13,6; mp4 cũ 16,3 (nói 15,25) | P1=1 (OFS, T24 dùng mà không giải nghĩa; `genrsa 2048`, `.pem`, `2>/dev/null` không giảng) P2=2 P3=2 P4=2 (ví dụ 9/20, 80 điểm, mã băm) P5=2 (dừng 25 s, 3 câu có lời giải) P6=2 (lỗi người mới/người đi làm, biên 50,95%) P7=2 | 2 (`labs/BNX/L21`, kết quả 5 dòng) | 2 (5/500/50 000 hồ sơ: 0/500/50 000 cờ, 0/13/1 250 người; 4 cách chữa có được/mất) | 13 | ĐỦ | cờ lệnh shell của openssl; tên OFS/T24; "giải ngân" (không giảng, dùng ngay từ hook) | OFS/T24 không được giải nghĩa; cờ openssl chỉ nói gộp |

### (3) Lab
| Bài | Tự làm được | Thời gian | Kẹt ở đâu | mong_doi khớp |
|---|---|---|---|---|
| L21 | có (chấm "ĐÚNG" ngay lần chạy đầu) | ≈ 3 phút viết | không kẹt; `de.md` đã cho công thức điểm, nhân chéo, `hashlib…hexdigest()`; chỉ cần biết `f"{x:.1f}"` (PYT) | khớp màn hình cảnh practice (DTI 42.9, 65, TU_CHOI, ab9bd3255a16, 60) và `mong_doi.txt`; `loi_giai.py` cùng kết quả |

### (4) Người học kẹt ở đâu
L21: scene `formula` Bước 6 "openssl genrsa -out rieng.pem 2048 2>/dev/null … sed 's/50000000/60000000/' hd.txt" (cờ lệnh không giảng); nếu qua được thì Bước 8 "bản tin OFS … T24" (OFS chưa được giải nghĩa).

### (5) Số đã tính lại
≈ 46 mục chạy/tính bằng Python (nhóm nợ 9 giá trị; máy trạng thái 2 đầu ra; `tham_dinh` 3 hồ sơ; băm 16 ký tự đầu và 60 vị trí; dấu vân tay `f7286011deef`/`3b0dc756fcb5`; OFS 3 dòng; quy mô 5/500/50 000 → 5/24/24 mã, 0/500/50 000 cờ; người xét 0/13/1 250; DTI 50,95 và 1 019 000 000 > 1 000 000 000; quiz 53,3%, 9 triệu, nhóm 3, 55 điểm; tối đa 6 triệu; lab 5 dòng) và openssl 3 lần ký/kiểm: 46/46 khớp màn hình (openssl khớp kết quả cuối, chỉ thêm stderr như dòng 3 ở bảng 1).

### (6) Khung hình đã xem
`frames/00000, 00014, 00017, 00020, 00024, 00034, 00040, 00072, 00080, 00083, 00092, 00096, 00105` (mở đầu, bảng nhóm nợ, 2 hình cơ chế, máy trạng thái, bộ quyết định, openssl, 4 cách chữa quy mô, lỗi 3, quiz, đề tự làm, kết quả mong đợi, tổng kết). Lỗi hiển thị: không có chữ tràn/đè. "CHAM_DIEM" trong hộp SVG hơi sát mép (vẫn nằm trong khung).

### (7) E51 và phút
Giáo án ↔ video: 7/7 mục tiêu có cảnh dạy và đo được (1 intuition, 2 example, 3–5 formula, 6 quymo, 7 practice); `covers` đúng; example/fix của curriculum khớp bài. Phút: YAML ≈ 13,6 (≤ 16 đạt); mp4 đã dựng 16,3 phút tổng, 15,25 phút lời (chưa vượt trần theo lời đọc nhưng tổng 16,3 > 16 và không có cảnh Tự làm).

---

## Bài L22 — AEM: JCR, Sling phân giải đường dẫn, HTL, OSGi (mô phỏng Python, bài ghi rõ không có máy chủ AEM)
Bài ghi "mô phỏng, không phải máy chủ AEM" ở hook, mọi tiêu đề bước, recap. Phần có thật theo đặc tả: tách URL (Sling URL decomposition), chọn tệp dựng theo `sling:resourceType` + selector, /apps trước /libs, ngữ cảnh HTL, vòng đời OSGi, log Oak "Traversed … nodes". Bài nói rõ HTL, Sling Model, MANIFEST chỉ "đọc đối chiếu". Dispatcher cache và AEMaaCS vs 6.5: bài không dạy (không phải lỗi; ghi nhận là chưa phủ).

### (1) Chuẩn xác
| Bài | Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng đã chạy | Đề xuất | Tin cậy |
|---|---|---|---|---|---|---|
| L22 | MUST (quy trình) | cả video | chapters/srt dựng 11-12 16:13 | SRT cũ 183 cue, 3352 từ, lời đọc 17,05 phút, tổng 18,2 phút (> trần 16). YAML nay 2276 từ ≈ 11,6 + 2,4 = 14,0 phút nên đạt, nhưng mp4 hiện có không phải bản này và thiếu cảnh `practice` | Dựng lại | CONFIRMED |
| L22 | SHOULD | pitfalls Lỗi 3 | `phải đọc cả 5 nút để ra 2 nút khớp` | Hàm `duyet` đã hiện trên màn hình ở cảnh quymo đếm cả nút gốc (10 trang → 14 nút = 10 + gốc + content + site + vi). Áp đúng hàm đó lên kho mẫu: `duyet(KHO)` = (6, 2), không phải (5, 2). Hai chỗ đếm khác quy ước (`bnx_l22_scan_cost` không đếm gốc) | Sửa 5 → 6 hoặc nói rõ "không tính nút gốc" ở cả hai nơi | CONFIRMED |
| L22 | SHOULD | formula step "Tệp khai báo của gói (MANIFEST.MF)" | `Thiếu dòng cuối thì lớp mô hình không được đăng ký.` | Khẳng định tuyệt đối. Tài liệu Apache Sling Models: có thể đăng ký bằng `Sling-Model-Classes`, plugin bnd mặc định sinh `Sling-Model-Classes` (chỉ sinh `Sling-Model-Packages` khi `generatePackagesHeader=true`). Đúng riêng cho bản kê khai trên màn hình | Thêm điều kiện "trong khai báo này" hoặc nhắc `Sling-Model-Classes` | CONFIRMED |
| L22 | — | còn lại | — | Không phát hiện lỗi: tách URL (4 ca + bảng 14 hàng của Sling kiểm trong mã bài), chọn tệp /apps trước /libs, thứ tự selector (khớp "Servlets and Scripts": `print/a4`, `print` rồi tên nhãn), 5 ngữ cảnh HTL, 6 trạng thái OSGi + dịch vụ gỡ khi dừng, khẳng định `import`/`start` kẹt INSTALLED, log "Traversed N nodes", /libs đổi khi nâng cấp | | |

### (2) Độ sâu
| Bài | sha16 | Phút | P1 P2 P3 P4 P5 P6 P7 | P8 | P9 | Tổng | Mất gốc | Cần biết trước | Chỗ thiếu chính |
|---|---|---|---|---|---|---|---|---|---|
| L22 | 80a5e8f581ea1152 | YAML ≈ 11,6 + 2,4 = 14,0; mp4 cũ 18,2 (nói 17,05) | P1=1 (thành phần DS, "Oak", `BundleException`, `Import-Package` chỉ giảng bằng một câu) P2=2 P3=2 P4=2 (5 phép tính cho `/home.html`) P5=2 P6=2 (mô phỏng so với thật, lỗi theo giai đoạn, /libs) P7=2 | 2 (`labs/BNX/L22`, 5 dòng mong đợi) | 2 (10/1 000/100 000 trang: 14/1 004/100 004 nút duyệt vs 1/10/1 000 qua chỉ mục, 3 lựa chọn đánh đổi) | 13 | ĐỦ | Declarative Services (DS, chỉ xuất hiện trên chữ: "thành phần khai báo kiểu DS"); regex `re.sub`; khái niệm XSS (chỉ tả, không gọi tên); author/publish | DS không giảng; Dispatcher/AEMaaCS không có |

### (3) Lab
| Bài | Tự làm được | Thời gian | Kẹt ở đâu | mong_doi khớp |
|---|---|---|---|---|
| L22 | có (ĐÚNG ngay lần đầu) | ≈ 5 phút | không kẹt; `de.md` chứa `KHO`, `TEP` và 3 bước; cảnh practice chỉ ghi "Kho… nằm ở de.md" nên người học phải mở `de.md` (nhắc rõ trong màn hình và lời đọc) | khớp (5 dòng); `loi_giai.py` dùng `chon` một bộ chọn, tương đương |

### (4) Người học kẹt ở đâu
L22: scene `pitfalls` Lỗi 2 "thành phần khai báo kiểu DS còn thiếu tham chiếu thì chưa đăng ký dịch vụ (OSGi Compendium §112.3)" (DS chưa được giảng; chỉ ở màn hình, không có trong lời đọc nên không ảnh hưởng đáp án).

### (5) Số đã tính lại
≈ 31 mục: nút con/thuộc tính/None, 4 kết quả `tach`, 3 kết quả `chon_tep` + kiểu, hai dòng HTML thoát, 34/46 ký tự (và 4 ký tự đặc biệt), vết gói 3 dòng, `chon_tep` sau khi gỡ 3 dòng, quymo 3 dòng 14/1 004/100 004 và 1/10/1 000, quiz `vay.in.a4.html` → `/apps/…/in.html`, lab 5 dòng, `duyet(KHO)`. 30/31 khớp; 1 lệch quy ước (6 so với "5 nút", xem bảng 1).

### (6) Khung hình đã xem
`frames/00000, 00016, 00020, 00023, 00036, 00040, 00045, 00048, 00064, 00080, 00094, 00102` (hook, bảng trạng thái gói, 2 hình cơ chế, HTL, 5 ngữ cảnh, MANIFEST, vòng đời gói chạy thật, quymo, quiz, gợi ý tự làm, tổng kết). Lỗi hiển thị: không. Ký hiệu `${…}` hiển thị đúng. Nhãn ③ trong SVG chữ nhỏ (17 px) nhưng đọc được.

### (7) E51 và phút
Giáo án ↔ video: 6/6 mục tiêu có cảnh dạy và đo được (1,3,4 formula; 2 example; 5 quymo; 6 practice); `covers` đúng; curriculum example (`/content/site/vi/home.html` → page.html; INSTALLED→RESOLVED→ACTIVE) khớp. Phút: YAML ≈ 14,0 (đạt); mp4 cũ 18,2 (vượt 16).

---

## Bài L23 — scikit-learn, ONNX Runtime, rừng cô lập
Chạy bằng thư viện thật: `audit/bnx/deps/l23/venv` (Python 3.13.5, scikit-learn 1.9.1, skl2onnx 1.20.0, onnxruntime 1.31.1, numpy 2.5.4, onnx 1.23.2). Chạy thêm bằng Python hệ thống với scikit-learn 1.8.0 + numpy 2.4.2 (bước huấn luyện và quy mô): kết quả y hệt.

### (1) Chuẩn xác
| Bài | Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng đã chạy | Đề xuất | Tin cậy |
|---|---|---|---|---|---|---|
| L23 | MUST (quy trình) | cả video | chapters/srt dựng 11-12 16:40 | SRT cũ 221 cue, 3989 từ, lời đọc 20,6 phút, tổng 21,9 phút (> trần 16). YAML nay 2273 từ ≈ 11,75 + 2,4 = 14,2 phút đạt, nhưng mp4 không phải bản này, thiếu cảnh `practice` | Dựng lại | CONFIRMED |
| L23 | SHOULD | prereq ③, formula Bước 5, quiz câu 2, practice "Nếu kẹt" | `số giá trị dưới ngưỡng: phần nguyên của p × (n−1), cộng một` | Chỉ đúng khi mọi điểm có điểm số khác nhau. Chính bảng quymo của bài phản ví dụ: N = 101 000, p = 0,01 → quy tắc cho `int(0,01·100 999)+1 = 1010`, nhưng chạy thật ra 1005 (dòng "1 005"). Nguyên nhân: điểm trùng nhau ở phân vị: chỉ 3 613 giá trị khác nhau trên 101 000 điểm; `(s < offset_)` = 1005, `(s <= offset_)` = 1011, 6 điểm nằm đúng ở ngưỡng −0,7232. Bài không giải thích chênh lệch 1010 vs 1005 | Thêm điều kiện "khi điểm không trùng nhau" và một câu giải thích dòng 1005 | CONFIRMED |
| L23 | SHOULD | intuition SVG 2 + formula Bước 2 so với Bước 5 | `điểm thường: 15,8 lần cắt` / `thường -0.4475 độ sâu quy đổi 11.88` | Cùng gọi "độ sâu/số lần cắt" cho nhóm thường mà hai số khác nhau (15,775 chạy tự cắt trên cả 1010 điểm không giới hạn độ sâu, cho riêng điểm 515; 11,88 quy đổi từ điểm trung bình của thư viện, cây học ≤ 256 điểm, độ sâu cắt cụt + hiệu chỉnh c). Bài không nói vì sao khác, người học có thể tưởng một trong hai sai. Đã chạy: 15.775 và 11.88 đều tái hiện | Thêm một câu: hai thước đo khác nhau (điểm đơn, không giới hạn, cỡ mẫu 1010 so với trung bình nhóm, cỡ mẫu 256, cắt cụt) | CONFIRMED |
| L23 | SHOULD | pitfalls Lỗi 2 | `RuntimeError: The model is using version 4 of domain 'ai.onnx.ml'…` | Tái hiện đúng với skl2onnx 1.20.0 + onnx 1.23.2 (`…not supported yet by this library. You need to specify target_opset={'ai.onnx.ml': 3}`), nhưng đây là hành vi theo phiên bản; màn hình không ghi phiên bản (chỉ có ở trường `source`); bài không hướng dẫn cài `scikit-learn skl2onnx onnxruntime`. Người học cài bản mới có thể không gặp lỗi hoặc gặp lỗi khác | Ghi phiên bản trên màn hình ("với skl2onnx 1.20.0") và lệnh `pip install` | PLAUSIBLE |
| L23 | — | còn lại | — | Không phát hiện lỗi: c(256) = 10,2448; −0,5; −0,7071; −0,9346; offset_ −0,7353; 10/10 và 11/1010; 1,8e-07; `decision_function = score_samples − offset_`; 5 hạt giống 10/11; contamination 0,001/0,01/0,05/auto → 2/11/51/137; 520 → 1, 50 000 → −1; 977/1000; 3 dòng quy mô; ONNX khai `target_opset={"":17,"ai.onnx.ml":3}` chạy được, đầu ra `label`, `scores` = decision_function, 1010/1010 cùng nhãn; ghi `auto` → offset_ = −0,5 đúng | | |

### (2) Độ sâu
| Bài | sha16 | Phút | P1 P2 P3 P4 P5 P6 P7 | P8 | P9 | Tổng | Mất gốc | Cần biết trước | Chỗ thiếu chính |
|---|---|---|---|---|---|---|---|---|---|
| L23 | d40f5fa0d2aefed1 | YAML ≈ 11,75 + 2,4 = 14,2; mp4 cũ 21,9 (nói 20,6) | P1=1 (numpy `default_rng/normal/concatenate/reshape(-1,1)/ravel`, `tree_.node_count`, `float32`, opset, `InferenceSession`, log₂ không giảng) P2=1 (Bước 2 → Bước 5: 15,8 so với 11,88 không được nối) P3=2 P4=2 (c(256) và 2^(−1/2) tính tay) P5=2 P6=2 (lỗi theo giai đoạn: tỉ lệ nhiễm, ONNX opset, trôi dữ liệu 977/1000, độ trễ p95/p99) P7=2 | 2 (lab Python thuần có mong đợi; code sklearn/ONNX trên màn hình chạy được với phiên bản nêu ở `source`) | 2 (1 010/10 100/101 000: 11/101/1 005 nhãn, nút ≈ 11 400 không đổi, 1/3/26 người xét; 3 đánh đổi) | 12 | ĐỦ (sát ngưỡng, không điểm 0) | numpy (mảng, `reshape`), log₂, cài thư viện bằng pip, đọc mảng bool/`sum`; cây quyết định (bài tả là "cây cắt ngẫu nhiên") | không có hướng dẫn cài thư viện học máy; hai thước "độ sâu" |

### (3) Lab
| Bài | Tự làm được | Thời gian | Kẹt ở đâu | mong_doi khớp |
|---|---|---|---|---|
| L23 | có (ĐÚNG ngay lần đầu) | ≈ 3 phút | không kẹt; `de.md` ghi sẵn công thức c(n), quy tắc `int(p·(N−1))+1` (không gọi ra điều kiện điểm trùng nhau, không ảnh hưởng ca này vì chỉ tính công thức) | khớp (4 dòng: c(128)=8.8584; A −0.8551/−0.2551/−1; B −0.4945/0.1055/1; 90/65); lab không dùng scikit-learn/ONNX nên 3 lần chạy giống hệt tự nhiên |

Ổn định thực nghiệm (chạy lại): bước huấn luyện 5 hạt giống (0–4) đều 10/11; 3 lần `IsolationForest` không đặt `random_state` đều bắt 10/10 và gắn 11 (offset_ dao động −0,7169, −0,7338, −0,7279); scikit-learn 1.8.0 và 1.9.1 cho cùng 11/101/1 005 nhãn, 11 384/11 802/11 436 nút, 977/1000.

### (4) Người học kẹt ở đâu
L23: scene `formula` Bước 4 "from sklearn.ensemble import IsolationForest" (bài không nói cài thư viện, số nút/lỗi phụ thuộc phiên bản); rồi Bước 5 "độ sâu quy đổi 11.88" đứng sau "15,775" ở Bước 2 mà không nối. Lab thì không kẹt.

### (5) Số đã tính lại
≈ 52 mục chạy bằng thư viện thật (dữ liệu 4 dòng; 94%; 2 trung bình 200 lần cắt; c/điểm 4 dòng; bước 4 bốn dòng; 2 độ sâu quy đổi; ONNX 2 dòng; kiểm 1; 5 hạt giống; 4 giá trị contamination; 2 dự đoán; lỗi ONNX; 977; 3 dòng quy mô × 4 giá trị; lab 4 dòng; ví dụ 4 phép tính tay; quiz 3 câu). 51/52 khớp; 1 lệch có điều kiện (quy tắc đếm 1010 so với 1005 ở N = 101 000, xem bảng 1).

### (6) Khung hình đã xem
`frames/00000, 00018, 00022, 00040, 00060, 00072, 00084, 00102` (hook, hình cắt ngẫu nhiên, Bước 1, Bước 5, bảng quy mô, lỗi ONNX, đáp án quiz, tổng kết). Lỗi hiển thị: không. Công thức KaTeX hiển thị đúng (khung 00040).

### (7) E51 và phút
Giáo án ↔ video: 6/6 mục tiêu có cảnh dạy và đo được (1 intuition + example, 2–3 formula, 4 pitfalls, 5 quymo, 6 practice; `covers` ghi `example` cho mục tiêu 1 là ổn vì ví dụ tính độ sâu 2,49 và 11,88; hình cơ chế ở intuition). Curriculum example (1000+10, 100 cây, 1%, 11 nhãn âm một, ONNX 1010/1010) khớp. Phút: YAML ≈ 14,2 (đạt); mp4 cũ 21,9 (vượt 16 → cần dựng lại).

---

## Nhận xét chung (≤ 8 gạch)
- Điều kiện chốt ngưỡng kế hoạch: MUST còn lại ở cả ba bài chỉ là việc quy trình (mp4/srt chưa dựng lại sau khi sửa YAML 2026-11-14; L22/L23 bản cũ vượt trần 16 phút). Kiến thức: không phát hiện MUST.
- Không có số sai; mọi số trên màn hình và trong lab tính lại khớp (trừ hai điểm quy ước ở L22 "5 nút" và quy tắc đếm L23).
- P1 = 1 ở cả ba bài (thuật ngữ dùng không giảng: OFS/T24/cờ openssl; DS/Oak; numpy/opset) nên P1 = 2 chưa đạt.
- P8 = 2 và P9 = 2 ở cả ba bài; lab chạy ĐÚNG ngay lần đầu, ổn định giữa 2 phiên bản scikit-learn và 5 hạt giống.
- Việc nên làm sau khi dựng lại: ghi bản thư viện và lệnh cài ở L23; nối hai thước "độ sâu" (L23); sửa "5 nút" (L22); thêm điều kiện cho quy tắc đếm (L23) và `Sling-Model-Packages` (L22); thêm TT 37/2025 vào registry (L21).
- Hạn chế của tôi: thời lượng YAML là ước lượng từ số từ, chưa đo bằng TTS; chưa nghe âm thanh; TT 31/2024 chỉ đối chiếu qua bản dịch/web, không mở văn bản gốc; không chạy AEM thật.
