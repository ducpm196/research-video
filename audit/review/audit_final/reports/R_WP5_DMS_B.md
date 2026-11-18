# WP5 DMS-B (L11–L20): đã đọc 10/10 bài

Người đọc độc lập, 2026-11-14. Tiêu chí: BRIEF mẫu F + ADDENDUM + P8/P9; người học mất gốc toán, chỉ có Python cơ bản.
Chỉ đọc YAML (`lessons/dms/Lxx_*.yaml`), `curriculum/dms.yaml`, `labs/DMS/Lxx`, `audit/dms/sources_L20.md`, `out/DMS/Lxx/frames`. Không sửa tệp nào ngoài báo cáo này.

## 0. Cổng quy trình (không phải lỗi nội dung YAML)

- **VIDEO CHƯA DỰNG LẠI.** `out/DMS/L11..L20/*.mp4, *.srt, chapters.txt, _frames.txt` có mtime 2026-11-09..11-11; YAML được sửa 2026-11-14 16:42–17:50 (thêm cảnh `quymo` + `practice`). `chapters.txt` hiện có 10–14 mục và KHÔNG có cảnh quymo/practice (L11: 11 mục, kết thúc ở "Chuỗi logic"). Chỉ `frames/*.png` được vẽ lại lúc 18:00–18:05 (khớp YAML mới). Hệ quả: lời đọc mới (kể cả số có dấu cách, mục S1) chưa có tệp tiếng/SRT để nghe. Phải dựng lại mp4/tts/asr trước khi coi video "đủ chuẩn".
- Không có tệp ngoài `frames/` thay đổi sau 11-11; không thấy phiên nào khác ghi vào `lessons/`.

- **Cập nhật 18:26 (giữa lúc đọc):** toàn bộ 10 YAML bị ghi lại lúc 18:26. Quét lại: L11, L12, L14, L16, L17, L19 đổi sha16 vì bỏ dấu cách trong số ở `say` ("5 151"→"5151", "1 000"→"1000", "14 833", "4 096", "1 001", "16 807", "1 178", "77 164"); `dump` trước/sau chỉ khác đúng các câu đó. L13, L15, L18 giữ nguyên sha; L20 không đổi (mtime 17:50). Bảng độ sâu ghi sha16 LÚC ĐỌC; sha16 hiện tại ở mục 2b. Các dòng S1 dưới đây đã được sửa, nhưng frames/mp4 chưa dựng lại.

## 1. Bảng chuẩn xác (chỉ lỗi có bằng chứng)

MUST nội dung: **0**. Số tính lại và mã chạy: mọi số khớp (mục 5).

| Bài | Mức | Cảnh/step | Trích | Vì sao / bằng chứng | Đề xuất | Tin cậy |
|---|---|---|---|---|---|---|
| L11 | SHOULD | quymo@0 say | "5 151 cách", "1 000 viên" | số nhóm bằng dấu cách trong `say`; TTS có thể đọc rời "5, 151". Phụ đề đã hiện "1 000" (frame L11 quymo) | viết "5151" hoặc chữ ("năm nghìn một trăm năm mươi mốt"), như L20 đã làm | PLAUSIBLE (chưa có bản dựng để nghe) |
| L12 | SHOULD | quymo@0 say | "cùng ra 14 833" | như trên | "14833" | PLAUSIBLE |
| L14 | SHOULD | quymo@1 say | "tối đa 4 096 phép nhân" | như trên | "4096" | PLAUSIBLE |
| L16 | SHOULD | quymo@0 say | "Với 1 001 đỉnh" | như trên | "1001" | PLAUSIBLE |
| L17 | SHOULD | quymo@0 say | "Với 7 đỉnh, 16 807" | như trên | "16807" | PLAUSIBLE |
| L19 | SHOULD | quymo@0 say | "1 178 khoá", "77 164 khoá" | như trên | "1178", "77164" | PLAUSIBLE |
| L20 | SHOULD | check (scene `check`) | say: "Ta kiểm lại bốn con số" | `focus: [1,'1.2','1.3']` và lời đọc chỉ nêu 2 con số (585 năm; 122 295). Hai hàng còn lại (1796 ngày; 2,8×10^14) không được đọc/tô sáng; "1796 ngày" còn không được dẫn ra ở stage2 (bảng ngày không tính số ngày) | đọc nốt hai hàng (1796 = 2/11/2007→2/10/2012; 2^48 ≈ 2,8×10^14 vs 2,56×10^14) hoặc bỏ hàng 1796 | CONFIRMED (đọc YAML) |
| L20 | SHOULD | sym@1 | say "Câu chuyện có bốn hàm băm" | chỉ nêu MD5, SHA-1, "họ thứ hai"; hàng SHA-3 (4 mục focus) không được đọc; tên SHA-256 không nói | thêm một câu cho SHA-3 | CONFIRMED |
| L18 | SHOULD | quymo@1 say | "gấp một nửa số cặp lần mức cần thiết" | khó hiểu khi nghe; màn hình ghi "phí gấp n/2 lần" (n=10 → 5 lần; n=100 → 50 lần) | "gấp n chia 2 lần: 5 lần với 20 đỉnh, 50 lần với 200 đỉnh" | CONFIRMED |
| L15 | SHOULD | sym say; recap say | "L bằng p trừ 1 nhân q trừ 1" | đọc thành tiếng mơ hồ (p − 1×q − 1) | "tích của p trừ 1 và q trừ 1" | PLAUSIBLE |
| L15 | SHOULD | why@0 | "Xét x có ước chung 1 với n" | chứng minh chỉ cho gcd(x, n) = 1; x chia hết cho p hoặc q chỉ dựa vào "máy kiểm 0..32" mà không nói rõ là chưa chứng minh; mục tiêu 2 ("vì sao giải mã đúng") đạt một phần | thêm một câu: trường hợp x chia hết cho p hoặc q cũng đúng (CRT/lập luận theo từng mô-đun), bài này chỉ kiểm bằng máy | CONFIRMED |
| L12 | SHOULD | lab `de.md` mục 4 | "công thức: `3**5 - 3*2**5 + 3*1**5`" | đề đã ghi sẵn nguyên lời giải bài toàn ánh (người học chỉ chép) | chỉ nêu "tất cả − hàm bỏ sót ≥ 1 giá trị", không ghi biểu thức | CONFIRMED |
| L11–L19 | SHOULD | quiz (step 0) | `pause: 8`/`10` cho hai câu | hai câu, mỗi câu 3–4 bước tính; 8–10 giây dừng quá ngắn (L20 dùng 20 giây). Người học phải tự bấm dừng | 30–45 giây, hoặc nói "bấm dừng" (đã nói "Dừng video") | CONFIRMED |
| L17 | SHOULD (nhỏ) | quymo@1 (hiển thị) | "khoảng 5 phần trăm nghìn giây" | 5,4×10^-5 s; cách nói lạ | "khoảng 50 phần triệu giây" | CONFIRMED |

Ghi chú nguồn L20 (`audit/dms/sources_L20.md`): "6 500 năm CPU và 100 năm GPU" khớp ePrint 2017/190 (blog Google ghi 110 năm GPU; nguồn đã ghi lệch này); 2019: 2^68, 2020: 2^63 khớp `BreakingChanges.adoc` của Git; mọi ngày NIST/Git khớp. Không có lỗi sự kiện.

## 2. Bảng độ sâu

Quy tắc P1: thuật ngữ dùng trong `say`, không giảng trong bài và không phải ký hiệu `assumes`; khái niệm cốt lõi đã định nghĩa ở bài DMS trước nhưng không ôn ở prereq cũng tính là chưa giảng.
"Phút" = ước lượng từ tốc độ 0,35 giây/từ của bản dựng cũ (chưa có bản dựng mới); trong ngoặc là thời gian dừng 6–7 phút ở cảnh practice.

| Bài | sha16 | Phút | P1 | P2 | P3 | P4 | P5 | P6 | P7 | P8 | P9 | Tổng(P1–P7) | Mất gốc | Cần biết trước | Chỗ thiếu chính |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L11 | 8d2c2caef6aaf00f | 10,4 (+6) | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | `itertools`, `math.comb` (de.md nêu tên) | số có dấu cách trong say |
| L12 | ef6c706f3f2a47d1 | 11,3 (+7) | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | ∪ và \|A\| (assumes, không ôn); `permutations`, `gcd` | de.md ghi sẵn công thức toàn ánh |
| L13 | a1a51de1e44de6d4 | 10,7 (+7) | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | số nguyên tố (verify@1, ngoại biên), hàm đệ quy cho Euclid mở rộng (chỉ có ở "Nếu kẹt") | không đáng kể |
| L14 | cd43d711d120ee67 | 10,8 (+7) | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | số nguyên tố (fermat@0; L15 mới ôn), bit/"bit thấp" (quymo, lab) | thiếu định nghĩa nguyên tố và bit |
| L15 | 591684ab472d318b | 11,1 (+7) | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | bit (quymo@1 bảng; trước đó dùng "chữ số nhị phân"), "phần đệm ngẫu nhiên" (pitfall 3) | bit; chứng minh chỉ cho x nguyên tố cùng n |
| L16 | d1fbbfa1ff9b5151 | 10,8 (+7) | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | không | không đáng kể |
| L17 | 17d14f3a3be9f639 | 10,9 (+7) | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | `combinations` lồng nhau trong mã quymo | không đáng kể |
| L18 | e6f6e54a5347b4ce | 11,5 (+7) | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | tuple làm khoá, set comprehension (mã quymo, lab) | câu say n/2 khó hiểu |
| L19 | b338dc994e1309db | 12,8 (+7) | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | "bảng băm", "hàm băm", "khoá", "ô", "va chạm" (định nghĩa ở L06, không ôn ở prereq L19), `itertools.product/permutations` | khái niệm băm chưa giảng lại ở hook |
| L20 | 7c534c3434d1a736 | ≈20 (+7) | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | byte (sym@1: "20 byte, tức 160 bit"), TLS/X.509 (chỉ trên màn hình) | check: 2/4 số được đọc |

### 2b. sha16 hiện tại (sau 18:26)

L11 8a91be4c852dc385; L12 ec73f8d33e7c72ab; L13 a1a51de1e44de6d4 (không đổi); L14 308a7e92a12d749c; L15 591684ab472d318b (không đổi); L16 fe4a24da436c311c; L17 457872912b788222; L18 e6f6e54a5347b4ce (không đổi); L19 da614d19387f8621; L20 7c534c3434d1a736 (không đổi).

Điểm tổng L14, L15, L19, L20 là 13 (không có mục 0). Bài L20 là bài hành trình: P3/P9 chấm theo trục thời gian + bảng số 585 năm/10 giây/122 295 lần/2,8×10^14.

## 3. Lab (tự làm bằng `cham.sh`; không xem `loi_giai.*` trước)

Mỗi bài tôi viết lời giải từ `de.md` (Python 3.11 từ `.venv`), chấm `bash labs/cham.sh DMS Lxx <tệp>`: cả 10 bài in **ĐÚNG** ngay lần đầu (3–6 giây/lần). Sau đó chạy cả `loi_giai.py`: 10/10 ĐÚNG. `mong_doi` trên màn hình (practice@1) so từng dòng với `mong_doi.txt`: 10/10 khớp.

| Bài | tự làm được | thời gian (người học, ước lượng) | kẹt ở đâu | mong_doi khớp màn hình |
|---|---|---|---|---|
| L11 | có | 30–45 phút | bài 4 (giới hạn trên): cần ý "trừ 3 × nghiệm có biến ≥ 6"; de.md đã gợi | khớp 4/4 |
| L12 | có | 45–60 phút | D9 vét cạn 362 880 hoán vị chậm vài giây; de.md ghi sẵn công thức toàn ánh | khớp 5/5 |
| L13 | có | 60–90 phút | Euclid mở rộng cần đệ quy (chỉ gợi ở "Nếu kẹt"); tuple gán nhiều biến | khớp 7/7 |
| L14 | có | 60–90 phút | đếm "phép nhân" phải theo đúng quy ước de.md (bình phương + nhân khi bit thấp = 1) | khớp 5/5 |
| L15 | có | 45–60 phút | d phải là nghịch đảo theo L chứ không theo n (đã nhắc ở pitfall 1 và hint) | khớp 6/6 |
| L16 | có | 45–60 phút | kiểm liên thông bằng duyệt đồ thị tự viết | khớp 4/4 |
| L17 | có | 45–60 phút | phát hiện chu trình bằng "nhóm đỉnh" (hint có) | khớp 7/7 |
| L18 | có | 60–90 phút | tô tham lam với khoá tuple ('a', i); đồ thị vương miện | khớp 8/8 |
| L19 | có | 30–45 phút | không đáng kể (de.md nêu hàm cần dùng) | khớp 5/5 |
| L20 | có | 20–30 phút | định dạng `%.1e`, `round` (de.md nêu) | khớp 6/6 |

Đề đủ để tự làm. Kiến thức Python vượt "cơ bản": đệ quy (L13), `itertools` (L11, L12, L17 nhắc tên, L19), comprehension tập hợp (L18). Mọi lab có kết quả mong đợi để đối chiếu; không lab nào ghi đáp số trong `de.md` (L12 ghi sẵn công thức, mục 1).

## 4. Người học kẹt ở đâu (chỗ đầu tiên không theo được)

- L11: không kẹt.
- L12: không kẹt (∪ và |A| được `assumes`; "hàm toàn ánh" ở practice được định nghĩa trong de.md/hint).
- L13: không kẹt (tách "số nguyên tố" ở verify@1 là ngoại biên).
- L14: fermat@0 "Nếu p là số nguyên tố và p không chia hết a" (định nghĩa nguyên tố chỉ có ở L15 và L03); sau đó quymo@1 "số bit của số mũ".
- L15: quymo@1 bảng "n dài 2048 bit"; sym "L bằng p trừ 1 nhân q trừ 1" nghe mơ hồ.
- L16: không kẹt.
- L17: không kẹt (mã quymo `combinations(combinations(range(n), 2), n - 1)` lồng nhau khó đọc, nhưng say giải thích).
- L18: quymo@1 say "gấp một nửa số cặp lần mức cần thiết"; mã quymo@0 dùng tập hợp suy diễn với khoá tuple.
- L19: hook@1 "khi nào bảng băm bắt đầu va chạm" (bảng băm/va chạm chưa giảng); hashing@0 "hàm băm rải đều".
- L20: sym@1 "mã dài 20 byte, tức 160 bit" (byte chưa giảng).

## 5. Số đã tính lại / mã đã chạy

- `checks` trong YAML: chạy toàn bộ bằng `eval` (có `math`, `itertools`): 0 sai, 1 lỗi môi trường tự gây (`Fraction` chưa import ở L19 sym, `checks` thật do công cụ dựng nạp sẵn).
- Mã trên màn hình (cảnh `quymo`, "Chạy thật"): 9/9 khớp từng dòng với "Kết quả chạy thật" (L11–L19). L20 không có cảnh quymo.
- Bảng số quymo tính lại: L11 (k = 3, 5, 10, 20: 5151; 4 598 126; 4 263 421 511 271; 4,91×10^21; 71 phút; 155 600 năm); L12 (n!, 22 phút, 77 năm, D20 = 895 014 631 192 902 121, tỉ lệ 0,36788); L13 (88 bước, 56 năm); L14 (10/27/53 phép nhân, 17 phút, 617 chữ số); L15 (2^1023 có 308 chữ số, 2,8×10^291 năm); L16 ((n−1)!/2: 1 814 400; 1,2×10^18; 158 chữ số); L17 (54 264; 886 163 135; 9,17×10^16; 6,4×10^25; Cayley); L18 (crown graph 10/100 màu); L19 (1,18√m: 23, 1178, 77164; 5,1×10^9, 2,2×10^19, 4,0×10^38; 688 năm); L20 (585 năm; 2^16,9 = 122 295; 2^48; 0,0116; 116,4; 2,7e-08; 1796 ngày; 2^68/2^63 = 32): tất cả khớp.
- Phép tính tay trong quiz/ví dụ (D4 = 9, D5 = 44, gcd(252, 198) = 18, 3^100 mod 7 = 4, RSA 4→31→4 và 2→8→2 mod 55, K5 10 > 9, 6 mặt, 1296, 0,435, 12 = 84 − 2×36 …): khớp.
- Tổng: 10 bài × (checks + mã + lab ×2) đều đạt; 0 sai.

## 6. Khung hình đã xem (từ `out/DMS/Lxx/frames`, vẽ lại 18:00–18:05; ghép 6 khung/ảnh, đã đối chiếu SVG với số liệu)

- L11: 00000 (hook), 00024 (12 ô sao-vạch), 00032 (ví dụ kem), ~00046 (cốc kem), ~00055 (quymo mã chạy thật), ~00062 (lỗi), ~00077/00085 (practice), ~00087 (tổng kết). Hình khớp: vạch ô 4 và 10 → 3, 5, 2.
- L12: hook, Venn ba vòng (27, 14, 7, 13, 7, 3, 3 đúng vị trí; xanh/đỏ/lục khớp lời đọc), quymo bảng, ví dụ trả mũ bước 3, pitfall 3–4, practice hint.
- L13: hook, vòng tròn 7 ngày (100 bước = 14 vòng + 2), Euclid bảng, Euclid mở rộng, quymo bảng, pitfall, practice hint.
- L14: hook, vòng 6 bước của 3^k mod 7 (1,3,2,6,4,5), lũy thừa nhanh, quymo mã + kết quả, tự kiểm 3^100, practice hint.
- L15: ví dụ mã hoá 4→31, "vì sao giải mã đúng", quymo mã chia thử, pitfall 1, practice hint.
- L16: hook (hình cầu Königsberg: bậc 3, 5, 3, 3), bảng Euler, tự kiểm, quymo bảng đồ thị đầy đủ, pitfall, practice hint.
- L17: tỉa lá 5→1 đỉnh, 3 cây trên 3 đỉnh có nhãn, tự kiểm, quymo bảng, pitfall, practice hint.
- L18: K4 với 4 mặt, K5 và bất đẳng thức, tô tham lam 2 thứ tự, quymo bảng 20/200/2 000 000, pitfall, practice hint.
- L19: 4/6/8 người (6/15/28 cặp), băm căn bậc hai, quymo bảng 32–256 bit, pitfall 1–2, giải mã ký hiệu, practice hint.
- L20: hook, trục thời gian 5 chặng (chữ đọc được), stage3, pitfall, quiz câu 2, recap.

Lỗi hiển thị: không có chữ tràn/đè/cắt trong khung đã xem; nửa dưới khung để trống (bố cục chung của bộ dựng). Không có tệp tiếng/phụ đề mới để so lời đọc thật với `say` (mục 0).

## 6b. Ký tự điều khiển

Quét mọi chuỗi của 10 YAML sau khi nạp (`\x00–\x08, \x0b, \x0c, \x0e–\x1f, TAB`): 0 trường hợp. Quét `say` tìm ký hiệu toán/`$`/`\`/`^`/`_`/số thập phân dấu chấm: 0 trường hợp (số thập phân đều dùng "phẩy").

## 7. Nhận xét chung

- Nội dung chuẩn: 0 MUST, mọi số tính lại khớp; L20 khớp nguồn đã đọc ở `sources_L20.md`.
- Ngưỡng: MUST 0 → ĐẠT (nội dung; còn cổng dựng lại video, mục 0). P1 = 2 chỉ ở 6/10 bài (60%) → KHÔNG đạt ≥ 90%: thiếu L14 (số nguyên tố, bit), L15 (bit), L19 (bảng băm/hàm băm/va chạm), L20 (byte). P8 = 2 ở 10/10 → ĐẠT. P9 = 2 ở 10/10.
- Sửa rẻ để đạt P1: một câu mỗi chỗ (nguyên tố, "bit = một chữ số nhị phân 0 hoặc 1", "byte = 8 bit", định nghĩa bảng băm/hàm băm/va chạm ở hook hoặc prereq L19).
- Quymo + practice mới làm chương trình dạy khá đủ: mỗi bài có mã chạy thật 2–3 mức quy mô, bảng thời gian ("số minh hoạ" ghi rõ), đánh đổi, và lab chấm tự động.
- Việc phải làm trước khi phát hành: dựng lại 10 video (số có dấu cách trong `say` đã được sửa lúc 18:26, 8 chỗ); nâng `pause` của quiz; sửa L20 check/sym@1, L18 quymo@1, L15 why/sym.
- Rủi ro người học: lab L13 (đệ quy), L18 (tuple/set) vượt "Python cơ bản"; nên nêu rõ trong de.md hoặc thêm gợi ý mẫu.
