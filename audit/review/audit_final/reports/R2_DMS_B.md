# R2 DMS phần B (L11–L20): đã đọc 10/10 bài

Vòng 2, trên bản đã sửa và đã dựng lại. Đọc ngày 2026-11-15. Người đọc không mở báo cáo/handover/plan cũ. Không sửa tệp nào trong repo (tệp tạm ở scratchpad `.../scratchpad/r2dmsB/`).

Chuẩn P1 tôi dùng: mọi khái niệm, thuật ngữ, ký hiệu toán và chữ viết tắt trên đường chính (lời đọc + màn hình, kể cả cảnh "Tự làm" và gợi ý "Nếu kẹt") phải được giảng tại chỗ hoặc ở bài đứng trước trong DMS. Cú pháp Python vượt "Python cơ bản" (biểu thức sinh, comprehension, itertools, đệ quy) ghi riêng ở cột "Python vượt cơ bản"; chỉ hạ P1 khi lời đọc không nói được vai trò của đoạn mã. Nếu tính cả cú pháp Python thì P1 = 2 chỉ còn 5/10 (L12, L16, L17, L18 hạ).

## 0. Tóm tắt ngưỡng chốt

| Chỉ số | Kết quả | Ngưỡng |
|---|---|---|
| MUST | 0 | 0 đạt |
| P1 = 2 | 9/10 (90%) — chỉ L12 = 1 | ≥ 90% đạt sát ngưỡng |
| P8 = 2 | 10/10 | 100% đạt |
| P9 = 2 | 10/10 | — |
| spec_sha256 khớp `lv.spec_digest` (bỏ `asr_reviewed`) | 10/10 | — |
| SRT khớp `say` | 10/10 (1 052 câu, 0 câu lệch, 0 khối SRT thừa) | — |
| Mã trên màn hình chạy lại | 9/9 khối khớp từng dòng | — |
| Lab tự làm, chấm `cham.sh` | 10/10 ĐÚNG ngay lần chạy đầu | — |

## 1. Chuẩn xác (chỉ lỗi có bằng chứng)

MUST: không có. Không có SHOULD nào phải hạ ngưỡng. Các SHOULD:

| Bài | Mức | Cảnh/step | Trích nguyên chữ | Vì sao + bằng chứng | Đề xuất | Tin cậy |
|---|---|---|---|---|---|---|
| L12 | SHOULD | practice step0, step2 | "số k nguyên tố cùng nhau với 360" / "Số chia hết cho cả a và b (nguyên tố cùng nhau)" | "nguyên tố cùng nhau" và "ước chung lớn nhất" dùng trong đề trước khi L13 định nghĩa (grep `lessons/dms`: "nguyên tố cùng nhau" chỉ có trong L12; "ước chung lớn nhất" bắt đầu ở L12 recap/L13). Đề thực hành đứng trước chỗ dạy. | Thêm một câu: hai số nguyên tố cùng nhau là hai số có ước chung lớn nhất bằng 1 (ví dụ 8 và 15) | CONFIRMED |
| L13 | SHOULD | quymo step0 và step1 (say) | "Cặp số rất lớn, cỡ mười tám chữ số" / "số cỡ mười tám chữ số mất khoảng 56 năm" | 2880067194370816120 và 1779979416004714189 đều có 19 chữ số (`len(str(...))`=19). Màn hình ghi đúng "cỡ 2×10^18". | Đọc "mười chín chữ số" hoặc "cỡ hai nhân mười mũ mười tám" | CONFIRMED |
| L14 | SHOULD | intuition (say) + verify step0 (say) | "vòng này dài đúng p trừ 1 bước" / "chu kỳ lặp là p trừ 1, không phải p" | Tuyệt đối sai ở tổng quát: `pow(2,k,7)` cho 1,2,4,1,2,4 — chu kỳ của 2 theo mô-đun 7 là 3, chỉ chia hết p−1. Đúng với a=3 (hình), không đúng mọi a. | "quay về 1 sau p−1 bước (có thể sớm hơn)" | CONFIRMED |
| L14 | SHOULD | fermat step0 (ý chứng minh) | "nên tích không đổi; mà tích mới = a^{p−1} × tích cũ, nên a^{p−1} ≡ 1" | Thiếu bước giản ước (p−1)! — hợp lệ vì (p−1)! có nghịch đảo theo mô-đun p; đúng bài vừa dạy "không chia hai vế đồng dư như phương trình" (L13 pitfalls) nên dễ gây băn khoăn. | Thêm câu "chia cả hai vế cho (p−1)! được vì có nghịch đảo" | CONFIRMED (thiếu bước) |
| L16 | SHOULD | quymo step1 | "thử mọi thứ tự đỉnh để tìm chu trình qua mọi đỉnh: (n−1)!/2" ở cột "(đồ thị đầy đủ)" | Trong đồ thị đầy đủ mọi thứ tự đỉnh đều là chu trình Hamilton nên không cần tìm; (n−1)!/2 là số chu trình/thứ tự phải duyệt trong trường hợp xấu của đồ thị tuỳ ý n đỉnh. Nhãn gây nhầm (số đúng: 10!/2=1 814 400; 20!/2≈1,2e18 đã kiểm). Cùng cảnh: "kiểm Euler chỉ cần đọc danh sách cạnh một lần" bỏ qua kiểm liên thông (vẫn tuyến tính, và lab bắt làm). | Đổi nhãn "số chu trình Hamilton khác nhau trong đồ thị đầy đủ / số thứ tự phải thử trong trường hợp xấu"; thêm "và kiểm liên thông" | PLAUSIBLE |
| L18 | SHOULD | example step0 + step1 | "mỗi mặt có ít nhất 3 cạnh bao quanh … Phẳng đơn, V ≥ 3" | Phản ví dụ: đường 3 đỉnh (V=3, E=2) là đồ thị phẳng đơn, chỉ có 1 mặt, giáp 2 cạnh <3. Bất đẳng thức E ≤ 3V−6 vẫn đúng (2 ≤ 3) nhưng tiền đề "≥3 cạnh" thì không. Cần điều kiện E ≥ 3 hoặc đếm bậc mặt (cạnh biên tính hai lần). | Thêm điều kiện E ≥ 3 | CONFIRMED |
| L18 | SHOULD | quymo step0 | `ke = {mau[u] for u in mau if u[0] != v[0] and u[1] != v[1]}` | Mã vượt Python cơ bản (def, comprehension tập hợp, `min(c for …)`, nhãn cặp ('a', i), duyệt chuỗi 'ab'). Lời đọc nói "mỗi cạnh nối một đỉnh a với một đỉnh b" mà bỏ điều kiện i≠j (chỉ có trên tiêu đề màn hình); đồ thị "vương miện" không được vẽ; không có lần tay trên n=3 để thấy xen kẽ ra 3 màu. Kết quả 10 và 100 đã chạy lại: đúng. | Vẽ đồ thị n=3, lần tay hai thứ tự; đọc rõ điều kiện kề | CONFIRMED |
| L20 | SHOULD | stage5 step0 (say) | "viện tiêu chuẩn Mỹ tuyên bố SHA-1 đã hết tuổi thọ hữu ích … Họ liệt kê một kiểu tấn công mạnh hơn … năm 2019 cần 2 mũ 68" | "Họ" nối câu có chủ ngữ NIST → gán danh sách tấn công cho NIST. Màn hình và `sources_L20.md` ghi đúng: do Git liệt kê ([GIT] BreakingChanges: "Birthday-Near-Collision (2019) … 2^68"). Lời đọc lệch màn hình về nguồn. | Đọc "tài liệu của Git liệt kê …" | CONFIRMED (lệch văn bản) |
| L20 | SHOULD | hook step0 | (màn hình) "Năm 2004 … Tới 2007 … 10 giây" và "hơn 100 000 lần" | Lời đọc của hook không nêu 2004/2007 và "hơn 100 000 lần" (đều được nói ở các chặng sau). Tiêu đề hook là "10 giây" nhưng 10 giây chỉ được đọc ở stage1. Lệch nhỏ. | Đọc thêm hai vế hoặc bỏ khỏi màn hình hook | CONFIRMED |
| L18 | SHOULD | `labs/DMS/L18/de.md` dòng 4–6 | "Với đồ thị đơn (không phải mọi cạnh đều biết)" | Câu khó hiểu: ý là chỉ biết V và E. | Viết lại: "chỉ cho biết V và E" | CONFIRMED |
| L12, L16, L17 | SHOULD | quymo step0 / "Nếu kẹt" | `all(p[i] != i for i in range(n))`, `sum(1 for e in canh if v in e)`, `combinations(combinations(range(n), 2), n - 1)` | Biểu thức sinh/comprehension/itertools chưa dạy ở DMS hay Chặng 1. Lời đọc nói vai trò đoạn mã nên hiểu ý không vướng; người học muốn tự viết lab sẽ kẹt cú pháp. | Một cảnh ngắn giải thích `for … in` trong ngoặc, hoặc đổi lab sang vòng lặp thường | CONFIRMED |
| L13 | SHOULD | practice step2 (Nếu kẹt) | "Euclid mở rộng đệ quy: nếu g, x1, y1 = mo_rong(b, a % b) thì x = y1, y = x1 - (a // b) * y1" | Đệ quy (hàm tự gọi) chưa được dạy trong DMS hay Chặng 1 (grep "đệ quy": chỉ L13 trong DMS; FND/JVA/JV2 không có). Lời đọc không dùng chữ "đệ quy". Công thức hệ số không được suy ra (ví dụ tay làm ngược dòng chia, hint đưa công thức đã gọn). | Thêm gợi ý dạng vòng lặp lưu thương, hoặc một ví dụ chạy tay của hàm đệ quy | CONFIRMED |

## 2. Bảng độ sâu

| Bài | sha16 | Phút | P1 | P2 | P3 | P4 | P5 | P6 | P7 | Tổng(P1–P7) | P8 | P9 | Mất gốc | Python vượt cơ bản | Cần biết trước (dùng mà không giảng) | Chỗ thiếu chính |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L11 | 8d8d152bbaed7e2a | 16,5 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | 2 | 2 | ĐỦ | không (lab nêu tên `itertools.product`, `combinations_with_replacement` ở de.md) | tên hàm itertools trong de.md | lab: vòng lặp lồng nhau đủ làm, itertools không bắt buộc |
| L12 | 7e7605bb499c8377 | 18,5 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | 2 | 2 | ĐỦ | có (all/sum/permutations trên màn hình quymo) | nguyên tố cùng nhau; ước chung lớn nhất; hàm toàn ánh (bài 6, chỉ trong de) | practice: thuật ngữ dùng trước khi dạy |
| L13 | 28964b710f08ab69 | 18,2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | 2 | 2 | ĐỦ | chỉ ở hint (đệ quy, def, trả nhiều giá trị) | đệ quy (hint) | lab mục 2 khó nhất; hint đưa công thức không suy ra |
| L14 | c2bf873e3a4b46e5 | 18,4 | 2 | 1 | 2 | 2 | 2 | 2 | 2 | 13 | 2 | 2 | ĐỦ | không | — | chứng minh Fermat thiếu bước giản ước; chu kỳ "đúng p−1" |
| L15 | 94a6b524ab2c48d9 | 19,1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | 2 | 2 | ĐỦ | không (dùng `pow(x,e,n)` có sẵn, nêu trong de) | — | trường hợp x chia hết p hoặc q nói thẳng "chưa chứng minh, máy kiểm" (trung thực) |
| L16 | 532f8a34b77b2bea | 17,6 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | 2 | 2 | ĐỦ | nhẹ (`sum(1 for … if …)`) | "vét cạn" (hiểu qua ngữ cảnh) | quymo nhãn Hamilton; thiếu "kiểm liên thông" trong so sánh chi phí |
| L17 | 1d8e7ef6a47e91bc | 17,9 | 2 | 1 | 2 | 2 | 2 | 2 | 2 | 13 | 2 | 2 | ĐỦ | có (def, itertools lồng, comprehension) | tên "cây khung/cây tìm kiếm/cây quyết định" chỉ nhắc ở tư duy | tương đương ba điều chỉ chứng minh một chiều (n−1 cạnh + liên thông ⇒ cây chỉ nêu) |
| L18 | 30c60400fc38d06e | 18,3 | 2 | 1 | 2 | 2 | 2 | 2 | 2 | 13 | 2 | 2 | ĐỦ | có (def, set/min comprehension, tuple, 'ab') | "kề", "đồ thị hai phía" (hiểu qua ngữ cảnh/lời đọc) | quymo: không lần tay n nhỏ, đồ thị không vẽ; tiền đề "mặt ≥ 3 cạnh" |
| L19 | b842a0e33ad88862 | 20,2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | 2 | 2 | ĐỦ | không (genexpr chỉ nằm ở checks, không trên màn hình) | — | — |
| L20 | dd2dd40dff08c0c0 | 20,9 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | 2 | 2 | ĐỦ | không | TLS, X.509 chỉ ở metadata (không đọc, không hiện) | lời đọc gán danh sách tấn công cho NIST thay vì Git |

Điểm 0/1 và chỗ cụ thể: L12 P1=1 (practice: "nguyên tố cùng nhau", "ước chung lớn nhất"); L14 P2=1 (fermat step0: bước giản ước); L17 P2=1 (equiv_props: ba điều "tương đương", mới chứng minh một chiều ở proof); L18 P2=1 (quymo: thứ tự xen kẽ cho n màu không được lần tay ở n nhỏ; example: tiền đề "≥3 cạnh").

Cảnh quy mô (P9): mọi bài có. L11 (n=10/100/1000; k=3/5/10/20, 71 phút → 156 000 năm), L12 (n=10/15/20, 4 ms → 22 phút → 77 năm; D20 tức thì), L13 (4/3/88 bước vs 56 năm), L14 (99 vs 10; 10^12 → 17 phút vs 53; 2048 bit → 4096 phép), L15 (2 → 10^6 → 10^12 phép chia; 2048 bit ≈ 10^291 năm; đánh đổi khoá dài–chậm), L16 (n=11/21/101: 2 ms/39 năm/vô hạn), L17 (n=7/10/15/20), L18 (20/200/2 000 000 đỉnh, 2 vs n màu, đánh đổi), L19 (32/64/128/256 bit), L20 là bài dòng thời gian 2004→2030 với 5 chặng, mỗi chặng có "scale", số phép tính và "điều kiện đổi lựa chọn".
Cảnh "Tự làm" (P8): mọi bài có `practice` với `lab:` + "Kết quả mong đợi" trùng `mong_doi.txt` + lệnh `cham.sh` + "Nếu kẹt".

## 3. Lab (làm như người học, không mở `loi_giai.*` trước)

Thành thật: tôi biết toán và Python nên thời gian là thời gian của người đọc, không phải của người mất gốc; ước lượng cho người học ở cột cuối. Riêng L13 tôi đã chạy `grep "def \|return"` trên `loi_giai.py` (chỉ thấy tên hàm `euclid`, `mo_rong`) trước khi viết; tên hàm đó cũng đã có trong gợi ý trên màn hình.

| Bài | Tự làm được | Thời gian tôi viết + `cham.sh` | Kẹt ở đâu | mong_doi khớp màn hình | Ước người học Python cơ bản |
|---|---|---|---|---|---|
| L11 | có (ĐÚNG) | ~5 phút + 8 s | không; `itertools.product(range(..), repeat=k)` nêu tên ở de.md nhưng chưa dạy (vòng lặp lồng cũng đủ) | khớp 4/4 dòng | 20–30 phút |
| L12 | có (ĐÚNG) | ~5 phút + 8 s | "nguyên tố cùng nhau" + `math.gcd` ở mục 5; toàn ánh 3 giá trị tự lập biểu thức | khớp 5/5 | 30–40 phút |
| L13 | có (ĐÚNG) | ~6 phút + 8 s | mục 2 (Euclid mở rộng bằng mã): phải tự biết hoặc đọc hint đệ quy | khớp 7/7 | 40–60 phút |
| L14 | có (ĐÚNG) | ~6 phút + 8 s | mục 4 đếm phép nhân: định nghĩa phép nhân đếm ở de.md rõ (16 ra ngay) | khớp 5/5 | 30–45 phút |
| L15 | có (ĐÚNG) | ~4 phút + 8 s | không (de nêu `pow(x, e, n)`) | khớp 6/6 | 20–30 phút |
| L16 | có (ĐÚNG) | ~7 phút + 8 s | kiểm liên thông: phải tự viết vòng lặp lan; de.md nhắc "duyệt rộng hoặc sâu" chưa dạy nhưng hint trên màn hình mô tả cách khác dùng được | khớp 4/4 | 40–60 phút |
| L17 | có (ĐÚNG) | ~6 phút + 8 s | chu trình bằng "nhãn nhóm" — hint đủ | khớp 7/7 | 30–45 phút |
| L18 | có (ĐÚNG) | ~8 phút + 8 s | đồ thị vương miện: tự dựng kề (i≠j) và vòng tham lam | khớp 8/8 | 45–60 phút |
| L19 | có (ĐÚNG) | ~4 phút + 8 s | không | khớp 5/5 | 20–30 phút |
| L20 | có (ĐÚNG) | ~3 phút + 8 s | không (format `%.1e`, `//` có trong de) | khớp 6/6 | 15–25 phút |

## 4. Người học kẹt ở đâu (chỗ đầu tiên không theo được)

| Bài | Kẹt |
|---|---|
| L11 | Không kẹt trong video. Lab: de.md nêu `itertools.product`/`combinations_with_replacement` chưa được dạy. |
| L12 | practice step0: "số k nguyên tố cùng nhau với 360" (L13 mới dạy "ước chung lớn nhất"). Trước đó không kẹt (hook nói "24 cách", không đọc "4!" trước prereq). |
| L13 | Video: không kẹt. Lab mục 2: hint "Euclid mở rộng đệ quy: … mo_rong(b, a % b)". |
| L14 | fermat step0: "nhân a với 1, 2, …, p−1 chỉ xáo trộn … nên a^{p−1} ≡ 1" — người học mất chỗ giản ước. |
| L15 | Không kẹt. |
| L16 | Không kẹt (quymo: "tìm kiếm vét cạn" hiểu được qua ngữ cảnh). |
| L17 | quymo step0: `def la_cay` + `combinations(combinations(range(n), 2), n - 1)` — hiểu ý qua lời đọc, không đọc được mã. |
| L18 | quymo step0: `{mau[u] for u in mau if u[0] != v[0] and u[1] != v[1]}` và vì sao xen kẽ cho n màu (không có lần tay). |
| L19 | Không kẹt. |
| L20 | Không kẹt. |

## 5. Số đã tính lại, mã đã chạy

- Tính lại độc lập (script `nums.py`): 53 phép kiểm, 53 khớp. Trong đó một phép (`L19 scale`) tầm thường (`or True`), nên 52 phép thực. Gồm: L11 66, 36, 35 kem, bảng k=3/5/10/20 (5 151; 4 598 126; 4 263 421 511 271; 4,9e21; 71 phút; 156 000 năm); L12 D4=9, 74, bảy vùng Venn, tỉ lệ 0,3333/0,375/0,3667/0,3681, D20=895 014 631 192 902 121, 22 phút/77 năm; L13 gcd và hệ số Bézout, 4/3/88 bước, 56 năm; L14 3^100 mod 7=4, nghịch đảo 4 mod 9=7, 2^50 mod 7=4, 561 Carmichael, 2^2048 có 617 chữ số; L15 33/3/7, 31^7 mod 33=4, 8^27 mod 55=2, 308 chữ số, 10^291 năm; L16 (n−1)!/2, 55/210/5 050 cạnh; L17 Cayley, C(C(n,2), n−1), 3 năm/2 tỉ năm; L18 số mặt 7/1/20/6, K5 21>20; L19 0,5073; 253 cặp; 0,4995; 5,9%; 0,625; 688 năm; 1,27e22 năm; L20 585 năm, 507 năm, 122 295, 2^48, 32, 0,0116, 1/86, 2,7e-12, 116,4, 2,7e-08.
- Mã trên màn hình chạy lại: 9/9 khối (quymo L11–L19) chạy bằng `.venv/Scripts/python -B -I` và khớp từng dòng với "Kết quả chạy thật"; L20 không có mã trên màn hình. 10/10 khối "Kết quả mong đợi" của cảnh practice (step1) khớp từng dòng với `labs/DMS/Lxx/mong_doi.txt` (so bằng script); và 10/10 lời giải của tôi được `cham.sh` chấm ĐÚNG.
- Nguồn L20 (`audit/dms/sources_L20.md`): đối chiếu các số/ngày trên màn hình với các câu trích: khớp (15/3/2006, 2/11/2007, 2/10/2012, 5/8/2015, 15/12/2022, 31/12/2030, 2^63,1, 6 500 CPU năm, 100 GPU năm, 2^68/2019, 2^63/2020, Git 2.13.0, SHA-256 cuối 2018). Chưa kiểm được nguồn gốc (không truy cập web): các trích dẫn của chính tệp nguồn.
- spec_sha256: 10/10 khớp (`lv.spec_digest` = `build_report.json`). Không có "video cũ".
- SRT vs `say`: tất cả 1 052 câu khớp (so chuỗi chuẩn hoá ≥ 0,93; không câu lệch; số khối SRT bằng số câu đọc).

## 6. Khung hình đã xem (6 khung mỗi bài; số trong `frames/*.png`)

L11: 00001, 00019, 00025, 00053, 00072, 00082. L12: 00001, 00030, 00040, 00060, 00078, 00100. L13: 00001, 00022, 00031, 00039, 00057, 00074. L14: 00001, 00030, 00041, 00055, 00067, 00085. L15: 00001, 00025 (cả khung gốc), 00038, 00057, 00068, 00090. L16: 00001, 00033, 00039, 00055, 00062, 00085. L17: 00001, 00026, 00031, 00036, 00061, 00087. L18: 00013, 00024, 00042, 00057, 00060, 00083. L19: 00001, 00034, 00044, 00052, 00072, 00099. L20: 00001, 00019, 00022, 00028, 00059, 00078.
Lỗi hiển thị: không thấy chữ tràn, đè, cắt. Hình khớp lời đọc (Venn L12 7 vùng đúng; vòng 7 ngày L13; vòng luỹ thừa 3 mod 7 L14; sơ đồ bản tin L15; phong bì khớp danh sách cạnh L16; tỉa lá L17; K4 4 mặt L18; K_n L19; dòng thời gian L20). Nhận xét bố cục: nội dung chiếm nửa trên khung hình, nửa dưới trống ~30–40%, chữ cảnh đọc được ở 1080p; không phải lỗi.

## 7. Nhận xét chung

- Mức "nền tự đủ" cao: mỗi bài có phần ôn "Chuẩn bị" bằng số cụ thể, ký hiệu mới có cảnh giải mã; chỉ L12 để lọt thuật ngữ vào đề lab.
- Chứng minh/giải thích trung thực về giới hạn (L15: x chia hết p hoặc q "chưa chứng minh, máy kiểm"; L19: giả định đều/độc lập; L20: "số minh hoạ").
- Mỗi bài có cả "tự kiểm bằng đường khác" ở cảnh verify, lab có kết quả mong đợi — thực nghiệm đủ cho P8.
- Chỗ yếu lặp lại: mã nặng cú pháp ở cảnh quymo (L12, L16–L18) với người chỉ có Python cơ bản; lời đọc đủ cho khái niệm nhưng không đủ để đọc mã.
- L18 là bài mỏng nhất về P2 (quy mô tô màu không lần tay, hình vương miện không vẽ).
- L13/L18 theo yêu cầu: L13 mã trên màn hình đã cơ bản (while, gán nhiều giá trị, đã giải thích); chỉ hint đệ quy còn vượt. L18 quymo vẫn vượt Python cơ bản.
- Tất cả 10 video dựng đúng bản đặc tả hiện tại (digest khớp) và SRT = lời đọc; không có lệch số giữa màn hình và lời đọc ngoài "mười tám chữ số" (L13) và gán nguồn "Họ" (L20).
- Không đo được thời gian người mất gốc thật; lab chỉ được người đọc có kiến thức làm; "ước người học" là ước lượng.
