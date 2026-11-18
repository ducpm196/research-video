# R3 INT + ACB: đã đọc 18/18 bài (INT L00–L08, ACB L00–L08), vòng 3 trên bản đã sửa và dựng lại

Người điều phối: R3_INT_ACB; ba tác tử con đọc song song (A = INT L00–L05; B = INT L06–L08 + ACB L00–L02; C = ACB L03–L08). Mọi bảng dưới là tổng hợp của người điều phối; phụ lục cuối tệp là nguyên văn tệp từng bài (8 mục theo BRIEF: Phần A, điểm, cảnh Tự làm/quy mô, lab, người học kẹt, số tính lại và khung hình, bảng sự kiện cần nhất quán).
Chuẩn P1: chuẩn CHÍNH THỨC chặt (mục chưa giảng = lệnh/ký hiệu/đối số/cú pháp/thuật ngữ trên màn hình đường chính, không suy ra từ tên, chưa giảng ở lần xuất hiện đầu; 0 mục = 2, 1–2 = 1, >=3 = 0).

## 1. Kết luận theo ngưỡng chốt

| Ngưỡng | Kết quả | Đạt? |
|---|---|---|
| MUST = 0 | 0 MUST ở 18 bài (63 SHOULD) | ĐẠT |
| P1 = 2 ở >= 90% bài | 0/18 bài (0%): P1=1 ở 10 bài, P1=0 ở 8 bài | KHÔNG ĐẠT |
| P8 = 2 ở 100% bài | 18/18 | ĐẠT |
| spec_sha256 build_report = lv.spec_digest (bỏ asr_reviewed) | 18/18 khớp, không có "video cũ" | ĐẠT |
| SRT khớp say | 18/18 (ghép toàn bộ câu say sau khi chuẩn hoá khoảng trắng = ghép toàn bộ khối SRT, từng ký tự) | ĐẠT |
| Mỗi bài có cảnh "Tự làm" (P8) và cảnh quy mô (P9) | 18/18 có `practice` (tiêu đề bắt đầu "Tự làm") và `quymo`; kết quả mong đợi trên màn hình khớp mong_doi.txt 18/18; số quy mô tính lại đúng 18/18; P9 = 2 ở 18/18 | ĐẠT |

Nhận xét P1: các mục chưa giảng chủ yếu là cú pháp mã (Python, Java, PL/SQL, Go, ksqlDB, SQL tham số), không phải khái niệm nghiệp vụ. Hai tác tử (B, C) ghi một số mục là "biên" (đếm gộp hay tách) nên P1 của INT L07, ACB L01, ACB L02 và một vài bài khác có thể lệch 1 điểm tuỳ cách đếm; dù lệch thế nào, tỉ lệ P1=2 vẫn xa mức 90%.

## 2. spec_sha256 và SRT (người điều phối tự chạy, không tin tác tử)

Cách làm: nạp tools/lv.py (load_yaml), băm sha256 của JSON(sort_keys, ensure_ascii=False) của YAML đã bỏ khoá asr_reviewed, so với out/<KHOÁ>/<Lxx>/build_report.json. Cùng lúc ghi sha16 tệp YAML (byte thô) lúc đọc và phút từ timeline_seconds. Toàn bộ tts_sources = edge, giọng duy nhất vi-VN-NamMinhNeural (không trộn giọng).

| Bài | sha16 YAML | spec_digest 12 ký tự đầu | Khớp build_report | Phút | Khung | SRT = say |
|---|---|---|---|---|---|---|
| INT L00 | 6001ff309b4f2c5b | d23e5548775a | OK | 15,4 | 105 | EQ |
| INT L01 | 6f96414358fde365 | 8ff8ff8b60b2 | OK | 14,3 | 96 | EQ |
| INT L02 | 6094c2508ee95b93 | 4d407a215304 | OK | 14,4 | 92 | EQ |
| INT L03 | 6947e1676429c89c | 6a38f95c3e23 | OK | 14,1 | 89 | EQ |
| INT L04 | 5ad87d0202323101 | e34867b2887f | OK | 15,7 | 90 | EQ |
| INT L05 | afdf15ec95deba41 | 0f1109fcdb49 | OK | 14,4 | 97 | EQ |
| INT L06 | 18a7bd8058c7daf2 | 5f817f51024e | OK | 13,3 | 89 | EQ |
| INT L07 | eed205398e71dfb3 | a544268c6b35 | OK | 13,2 | 89 | EQ |
| INT L08 | ad4c7eae500e0d55 | 2cfb6419a8f5 | OK | 16,7 | 97 | EQ |
| ACB L00 | a581eda427709609 | a444952b8195 | OK | 14,9 | 113 | EQ |
| ACB L01 | 12470f9d53589388 | a417ca958d6d | OK | 13,3 | 97 | EQ |
| ACB L02 | df13a47a911e359c | 7b21609e7b3a | OK | 15,6 | 111 | EQ |
| ACB L03 | b920c4706498ffa8 | ecf5d64c3f86 | OK | 14,5 | 100 | EQ |
| ACB L04 | d18a7fccc0e66c74 | 8fc3c0de24e9 | OK | 14,2 | 98 | EQ |
| ACB L05 | cd4c22eed138d94e | b24e6ef4011f | OK | 16,7 | 117 | EQ |
| ACB L06 | d16ab77fd3ee0222 | 24c8cc977738 | OK | 15,8 | 111 | EQ |
| ACB L07 | 4bf6f78d6e3ff3ba | 2edd5fbfc712 | OK | 16,6 | 120 | EQ |
| ACB L08 | 8ff9af055621b299 | a13b04ef8402 | OK | 16,4 | 106 | EQ |

Ba tác tử báo sha16 YAML của cả 18 bài khớp giá trị giao việc.

## 3. Phần A: chuẩn xác (tổng hợp; chi tiết trong phụ lục)

MUST: 0. SHOULD: 63 (A = 20, B = 23, C = 20). Không SHOULD nào là sai kiến thức hẳn; phần lớn là thiếu điều kiện, nhãn "minh hoạ/chưa kiểm", hoặc lệch nhỏ giữa các cảnh. Mục đáng ưu tiên sửa (chọn lọc, có bằng chứng ở phụ lục):

| Mức | Bài:cảnh | Trích / vấn đề | Tin cậy |
|---|---|---|---|
| SHOULD | ACB L00:example s2, code, practice s2 | "120 + 35 = 155 ms ... đạt mục tiêu P99 200 ms", mã `if tong < 200: print("dat P99")`: P99 không cộng được theo thành phần, trong khi prereq đã định nghĩa P99 | CONFIRMED |
| SHOULD | ACB L00:quiz s3 so với INT L08:hook s1 | ACB L00 ghi "3 năm tại OCB là Chuyên viên chính trong Squad Lending"; INT L08 nói Squad Lending chỉ là tên nhóm lấy từ một tin tuyển dụng đã lưu, chưa kiểm. Hai khoá không nhất quán (người điều phối xác nhận bằng grep: ACB L00 dòng 597 và INT L08 dòng 9 YAML) | CONFIRMED |
| SHOULD | ACB L02:concept so với recap | concept: Core giữ tiền (bước 2) trước khi khử trùng (bước 3); recap: khử trùng trước rồi mới giữ tiền. Thứ tự ngược nhau | CONFIRMED |
| SHOULD | INT L08:pitfall s2 so với mục tiêu và recap | lời đọc "ba lớp"; mục tiêu và recap "hai lớp chặn" | CONFIRMED |
| SHOULD | INT L04:quymo (dòng x10) | "khoá sống lâu hơn 17 phút" mâu thuẫn "khoá sống 300 giây" nêu đầu cảnh | CONFIRMED |
| SHOULD | ACB L04:example step3 | "25 ms" gán nhãn "toàn bộ quy trình"; trên màn hình 125-100 là khoảng từ lần ghi cũ, quy trình thật 5 ms | CONFIRMED |
| SHOULD | ACB L05:hook/pitfall so với quymo | nói "mất hàng giờ" nhưng bảng của bài cho 10 000 lệnh tuần tự 50 s (hàng giờ chỉ ở 1 triệu lệnh); hàng x10 000 "100 đoạn -> 10 s" trái với chia theo ngày tối đa 30 đoạn (~33,3 s) | CONFIRMED |
| SHOULD | ACB L03:quymo cỡ x100 | "2 tiến trình" theo tải trung bình 833/s, bỏ qua đỉnh 1500/s bài tự nêu (cần 3) | CONFIRMED |
| SHOULD | ACB L07:quymo so với example | 0,065 s và 180 s cho cùng 3 triệu dòng mà không giải thích; hook "trăm nghìn đơn mỗi ngày" lệch 10 lần so với "3 triệu dòng mỗi nguồn" | CONFIRMED |
| SHOULD | ACB L08:example/symbol | luồng khoá sổ -> ký số -> mở hạn mức chỉ xử lý lỗi ở bước mở hạn mức; ký lỗi hoặc bỏ dở sau khoá sổ thì sổ vẫn bị phong toả. Mục tiêu 4 hứa luồng LOS/Cloud CA/CIC qua mTLS nhưng không cảnh nào chạy từng bước | CONFIRMED |
| SHOULD | INT L00:concept | lời đọc "Tầng hai là dịch vụ nhỏ và cơ sở dữ liệu" khác màn hình ghi "REDIS" | CONFIRMED |
| SHOULD | INT L01:concept | bảng GC: Full GC "Dừng toàn bộ hệ thống, nguyên nhân gây quá hạn API" là khẳng định tuyệt đối (G1/ZGC giảm mạnh) | CONFIRMED |
| SHOULD | INT L06:prereq s1, pitfall | "OCB" dùng không giải thích trong bài phỏng vấn ACB | CONFIRMED |
| SHOULD | INT L07:example s2 | tên công ty, mốc năm thật của một cá nhân (Sutrix, Grooo, Mirae Asset Finance, OCB) không nguồn, không nhãn minh hoạ (L06 có nhãn); freelance 2022 chồng Grooo 2022-2023 | PLAUSIBLE |
| SHOULD | INT L04 (mã phản hồi 68), ACB L00/L02 (0400 chỉ khi biết chắc thất bại) | theo NAPAS chưa kiểm nguồn; bài đã gắn nhãn "cần kiểm" | PLAUSIBLE |
| SHOULD | INT L05:pháp lý, INT L06:check s1, ACB L06 (tiêu đề, mục tiêu 1, recap) | ngưỡng 10 triệu/lần hoặc 20 triệu/ngày gắn với "TT 50/2024 (sửa đổi bởi TT 77/2025)": xem mục 4 | PLAUSIBLE |
| SHOULD | ACB L06:code, ACB L07:code | so sánh chữ ký bằng `!=`/`==` thay vì `hmac.compare_digest` | PLAUSIBLE |
| SHOULD | ACB L07:pitfall | `LIKE '8888%'` chỉ dùng chỉ mục B-Tree trên PostgreSQL non-C khi có `text_pattern_ops` (chưa kiểm) | PLAUSIBLE |

Các SHOULD còn lại (nhãn "chưa kiểm" thiếu trên màn hình, mốc "dự kiến tốt nghiệp 11/2026" trùng tháng hiện tại 2026-11 nên video sẽ lỗi thời, "TTL Redis 60 s ở INT L00 so với 120 s ở INT L02 và ACB L07", "L02 REQUIRES_NEW chưa nêu rủi ro cạn bể", ...) nằm trong phụ lục theo từng bài.

## 4. Số liệu pháp lý, lương, tên người thật; nhất quán INT với ACB

Nguồn đối chiếu: WebSearch/WebFetch của các tác tử (chỉ nguồn thứ cấp, báo chí/ngân hàng; không đọc được toàn văn văn bản gốc) cộng sources trong YAML.

| Mục | Trạng thái trong bài | Đối chiếu | Kết luận |
|---|---|---|---|
| QĐ 2345/QĐ-NHNN | INT L05/L06: "chưa đọc nguyên văn, chưa rõ còn áp dụng, không nêu số điều"; ACB L06: "ngày 18/12/2023, hiệu lực 01/07/2024 theo tài liệu phỏng vấn đã lưu" | ngày/hiệu lực khớp nguồn thứ cấp | Nhất quán, cả hai đều hedge; ACB chi tiết hơn INT, không mâu thuẫn |
| TT 50/2024/TT-NHNN | cả INT và ACB nêu; ACB nói "sửa đổi bởi TT 77/2025" | ký 31/10/2024, hiệu lực 01/01/2025 (bài không nêu hai mốc); bài hedge điều kiện đi kèm | OK, chưa kiểm văn bản gốc |
| TT 77/2025/TT-NHNN | ACB L06 nêu hiệu lực 01/03/2026 và "bản hợp nhất 25/VBHN-NHNN"; INT L05/L06 chỉ nêu "sửa đổi bởi TT 77/2025" | ban hành 31/12/2025, hiệu lực 01/03/2026, đúng theo nguồn thứ cấp; "25/VBHN-NHNN", "Công báo 1279+1280" chưa kiểm được | Số hiệu/hiệu lực đúng; VBHN và Công báo ghi "chưa kiểm" |
| Ngưỡng sinh trắc học "trên 10 triệu/lần hoặc tổng ngày trên 20 triệu" | INT L05 (concept/ranh giới, dòng YAML 317, 325), INT L06 (dòng 261), ACB L06 (lệnh `>` 10 triệu, tổng ngày > 20 triệu) | các báo không thống nhất "trên" hay "từ"; không nguồn nào nói TT 77 đổi ngưỡng cá nhân; ngưỡng doanh nghiệp/hộ kinh doanh từ 01/07/2026 khác; ACB L06 đã nói bài chỉ nói cá nhân | Nhất quán giữa INT và ACB; biên "trên/từ" và ngưỡng đi kèm chưa kiểm (đã hedge ở ACB, hedge nhẹ hơn ở INT L05/L06: SHOULD) |
| Luật 91/2025/QH15 (Bảo vệ dữ liệu cá nhân) | ACB L06 nêu như khuyến nghị thiết kế, "CHƯA kiểm số điều" | thông qua 26/06/2025, hiệu lực 01/01/2026: đúng | OK |
| TT 31/2024/TT-NHNN (nhóm nợ), TT 37/2025 | INT L08 prereq s2 và ACB L08: "nhóm 2 quá hạn 10-90 ngày", "cần đối chiếu bản hợp nhất" | TT 31/2024 hiệu lực 01/07/2024, TT 37/2025 ký 31/10/2025: có thật; chưa xác nhận TT 37 có đổi Điều 10 không; "Công báo 825+826" chưa kiểm | OK, đã hedge |
| Lương ACB | INT L07 và ACB L00: "Thương lượng", tháng 13 cố định, thưởng 1-4 tháng (tin ACB đọc 2026-11); ACB L05 recap: JD lương thương lượng | công thức T = L x (13+k) + 12P nhất quán INT L07 / ACB L00 (L=40 cho 560-680) | Nhất quán; nên ghi ngày đọc tin và "kiểm lại tin hiện hành" |
| Hồ sơ cá nhân (OCB 10/2023-nay, UIT dự kiến 11/2026) | INT L00/L01/L04/L05/L07, ACB L00 | khớp nhau | Nhất quán; mốc 11/2026 trùng tháng hiện tại, sẽ lỗi thời |
| Squad Lending | INT L08: tên nhóm trong tin tuyển dụng chưa kiểm; ACB L00 quiz: "3 năm tại OCB là Chuyên viên chính trong Squad Lending" | | MÂU THUẪN (SHOULD, mục 3) |
| Core T24 | ACB L04/L07/L08: "kiến trúc tham chiếu OCB, ACB không nói dùng core nào" | INT L04/L05 có câu CV "OCB/T24/đội Switch" không nguồn trong bài | Giọng điệu hơi khác (ACB hedge, INT L04/L05 nói như CV) |
| Khoá khử trùng/TTL | INT L00 60 s; INT L02 120 s; ACB L03 24 h; ACB L07 120 s giao dịch và 24 h mã sự kiện; ACB L06 vé 180 s | các số theo từng ví dụ minh hoạ | Không mâu thuẫn trực tiếp; nên ghi "ví dụ" |

Quy tắc "sau khi quét mặt, tổng cộng dồn về 0" ở ACB L06 là giả định của mô phỏng, không phải luật; INT chưa nêu như luật (nhất quán).

## 5. Bảng độ sâu

Cột: Bài | Phút | P1 | P2 | P3 | P4 | P5 | P6 | P7 | Tổng(P1-P7) | Mất gốc | P8 | P9 | Số mục P1 chưa giảng | Chỗ thiếu chính (danh sách mục P1 chi tiết ở phụ lục và mục 6)

| Bài | Phút | P1 | P2 | P3 | P4 | P5 | P6 | P7 | Tổng | Mất gốc | P8 | P9 | Mục P1 | Chỗ thiếu chính |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| INT L00 | 15,4 | 1 | 2 | 1 | 2 | 2 | 2 | 2 | 12 | ĐỦ (sát ngưỡng) | 2 | 2 | 2 | lỗi hiển thị kim tự tháp (chữ tràn), recap dàn ngang |
| INT L01 | 14,3 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | 2 | 2 | 2 | khối mã chưa dẫn từng dòng; thiếu lệnh javac/java |
| INT L02 | 14,4 | 0 | 2 | 2 | 2 | 2 | 2 | 2 | 12 | GẦN | 2 | 2 | 5 | Singleton, trạng thái khả biến, PostConstruct, failover, đổi ngữ cảnh |
| INT L03 | 14,1 | 0 | 2 | 1 | 2 | 2 | 2 | 2 | 11 | GẦN | 2 | 2 | 5 | FK, WAL/redo log, sendfile, page cache; sơ đồ SAGA không mũi tên |
| INT L04 | 15,7 | 0 | 2 | 2 | 2 | 2 | 2 | 2 | 12 | GẦN | 2 | 2 | 4 | mã `<<`, `[-13:-1]`, `:016X`, XOR 16 cặp hex |
| INT L05 | 14,4 | 0 | 2 | 2 | 2 | 2 | 2 | 2 | 12 | GẦN | 2 | 2 | 5 | mạng nơ-ron sâu, mô hình đồ thị, mã Java ONNX |
| INT L06 | 13,3 | 0 | 1 | 2 | 2 | 1 | 1 | 2 | 9 | GẦN | 2 | 2 | 8 | TLS/mTLS, IBM MQ, TCP Socket, NAPAS, Spring, ORDER BY...FOR UPDATE, OCB, "yêu cầu dở", TPS x độ trễ |
| INT L07 | 13,2 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | 2 | 2 | 2 | cú pháp Python for/range/+=/*= |
| INT L08 | 16,7 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | GẦN | 2 | 2 | 4 (có thể gộp 1) | tài sản bảo đảm/cầm cố, tín chấp, `&&`, `.size()` |
| ACB L00 | 14,9 | 0 | 2 | 2 | 2 | 2 | 2 | 2 | 12 | GẦN | 2 | 2 | 4 | "0200/0210" trước khi giải thích, "247", "TTL" (đáp án lab), OCB, Squad Lending |
| ACB L01 | 13,3 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | 2 | 2 | 2 (+2 biên) | MV:SV trong OFS, biểu thức sinh `for k, v in truong.items()` |
| ACB L02 | 15,6 | 0 | 2 | 2 | 2 | 2 | 2 | 2 | 12 | GẦN | 2 | 2 | 3 (biên) | `format(bits,"016X")`, `[n for n in range(1,65) if ...]`, "băm" |
| ACB L03 | 14,5 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | 2 | 2 | 2 | bí danh `e`/`p`, `e.account_no`; OTP chưa nối với "mật mã dùng một lần" |
| ACB L04 | 14,2 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | 2 | 2 | 2 | `:cif :id ...` và `?` trong SQL; cột khoá; trạng thái REVERT |
| ACB L05 | 16,7 | 1 | 2 | 2 | 2 | 2 | 2 | 1 | 12 | ĐỦ | 2 | 2 | 2 | `khoa.get(tk, ai) != ai`, `INTO v_bal`, `r.acc`; tiêu đề hứa BULK COLLECT mà không có trên màn hình |
| ACB L06 | 15,8 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | 2 | 2 | 2 | VNeID, `expires_at` số giây Unix |
| ACB L07 | 16,6 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | 2 | 2 | 2 | "EOD", "Webhook Idempotent" chỉ mô tả hành vi |
| ACB L08 | 16,4 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | 2 | 2 | 2 | tham số `ctx` trong mã Go, "lũy đẳng" |

Tổng quát: ĐỦ 9 bài (INT L00, L01, L07; ACB L01, L03-L08), GẦN 9 bài (INT L02-L06, L08; ACB L00, L02; trong đó INT L06 chỉ 9 điểm). Không bài nào CHƯA. Điểm thấp ngoài P1: INT L00 P3=1 (lỗi hiển thị), INT L03 P3=1 (sơ đồ SAGA thiếu mũi tên), INT L06 P2/P5/P6 = 1 (bài ngân hàng câu hỏi, lời giải ngắn), INT L08 và ACB L05 P7=1.

## 6. Danh sách mục P1 chưa giảng (mọi bài P1 < 2)

Danh sách đầy đủ, kèm trích chữ và cảnh, nằm ở mục "Điểm" của từng tệp bài trong phụ lục. Tóm tắt:
- INT L00 (2): quymo step 1, cú pháp Python `for tps in (...)`, `print`, `10 ** -chin`, `round(..., 2)`; và `525600` (phút một năm) dùng trong mã trước khi được giải thích (chỉ giải ở practice "Nếu kẹt").
- INT L01 (2): example step 4, mã Java LuongAo (`public static void main`, `try (var ex = ...)`, lambda `() -> {...}`, `ex.submit`) dù lời đọc bảo "gõ lại"; quymo step 1, Python `while suc < n: suc *= m; cao += 1`, `10**4`, `cao, suc = 0, 1`.
- INT L02 (5): Singleton / "trạng thái khả biến", PostConstruct, failover, "đổi ngữ cảnh", cú pháp Java.
- INT L03 (5): FK (dùng ở example, định nghĩa ở pitfall), WAL/redo log, sendfile và page cache, mã PL/SQL.
- INT L04 (4): `<<`, `[-13:-1]`, `:016X`, XOR 16 cặp hex.
- INT L05 (5): "mạng nơ-ron sâu", "mô hình đồ thị", mã Java ONNX, cú pháp.
- INT L06 (8): TLS (trong mTLS), IBM MQ, TCP Socket, NAPAS, Spring, ORDER BY ... FOR UPDATE, OCB, "yêu cầu dở", công thức TPS x độ trễ.
- INT L07 (2 nhóm): `for/range/in`, `+=`, `*=` (đếm riêng từng cú pháp có thể thành 0).
- INT L08 (4): "tài sản bảo đảm/cầm cố", "tín chấp", `&&` và `.size()` trong mã giả, cú pháp Python.
- ACB L00 (4): "0200/0210" dùng trước khi giải thích, "247", "TTL", OCB và Squad Lending.
- ACB L01 (2 + 2 biên): MV:SV trong khung OFS, biểu thức sinh `for k, v in truong.items()`; (biên) "mã FT", "COMPANY/VN0010001".
- ACB L02 (3, biên): `format(bits,"016X")`, `[n for n in range(1,65) if ...]`, "băm".
- ACB L03 (2): bí danh `e`/`p` và `e.account_no` (ksqlDB, symbol); chữ OTP trong sơ đồ chưa nối với "mật mã dùng một lần" (concept).
- ACB L04 (2): `:cif :id :ch :dt :old_ts` và `?` trong SQL, ba cột khoá `channel`/`order_date` (symbol, code); trạng thái `REVERT` (code, practice).
- ACB L05 (2): `khoa.get(tk, ai) != ai` (code step1); `INTO v_bal`, `r.acc` (symbol, ranh giới).
- ACB L06 (2): VNeID (hook); `"expires_at": 1730948400` số giây Unix (symbol step2).
- ACB L07 (2): "EOD" (hook, concept); "Webhook Idempotent" chỉ mô tả hành vi (hook, check).
- ACB L08 (2): tham số `ctx` trong mã Go (symbol step2); "lũy đẳng" (code, pitfall).

## 7. Lab

INT: cả 9 lab là giấy-bút `.md` (cham.sh không chấm `.md`); tác tử tự tính bằng Python/tay trước khi mở loi_giai.md rồi so mong_doi.txt: 9/9 khớp; số trên màn hình cảnh Tự làm khớp mong_doi.txt 9/9. ACB: 9 lab chạy được; tác tử viết lời giải riêng cho L00-L02 và L03-L08, `bash labs/cham.sh ACB Lxx <tệp>` in ĐÚNG; chạy cham.sh với chính loi_giai.py cũng ĐÚNG (9/9).
Ghi chú quy trình: ở INT L00 tác tử A lỡ thấy 5 dòng đầu loi_giai/mong_doi trong cùng lệnh với de.md trước khi tự tính; kết quả tự tính vẫn độc lập và trùng.

| Bài | tự làm được | thời gian | kẹt ở đâu | mong_doi khớp màn hình |
|---|---|---|---|---|
| INT L00-L08 | có (giấy bút) | vài phút mỗi bài (INT L07 ~3 phút) | không kẹt; đề cho sẵn công thức và số | 9/9 khớp |
| ACB L00-L08 | có; cham.sh ĐÚNG với lời giải tự viết và với loi_giai.py | theo từng tệp bài | không kẹt ở đề; kẹt thuật ngữ chỉ ở cú pháp mã (mục 6) và đáp án lab ACB L00 dùng "TTL" chưa giảng | 9/9 khớp |

Chi tiết từng bài (thời gian, kẹt) nằm ở mục "Lab" của tệp bài trong phụ lục.

## 8. Người học kẹt ở đâu (một dòng mỗi bài; chi tiết trích chữ ở phụ lục)

- INT L00, L01: chỉ ở khối mã (không kẹt hẳn).
- INT L02: "Singleton ... trạng thái khả biến".
- INT L03: "FK" và mã PL/SQL.
- INT L04: mã `<<`, `[-13:-1]`, `:016X`, XOR 16 cặp hex.
- INT L05: "mạng nơ-ron sâu" và mã Java ONNX.
- INT L06: TLS/mTLS, IBM MQ, TCP Socket, NAPAS ở prereq (nhiều từ liên tiếp).
- INT L07: quymo s1, khối Python (`for nam in range(1, 6)`, `tong += ...`) nhưng vẫn theo được ý qua lời đọc và bảng.
- INT L08: "tài sản bảo đảm/cầm cố", "tín chấp", mã giả `&&`.
- ACB L00: "0200/0210" dùng trước khi giải thích; "TTL" ở đáp án lab.
- ACB L01: khung OFS MV:SV, biểu thức sinh.
- ACB L02: `format(bits,"016X")`, "băm".
- ACB L03: bí danh `e`/`p` trong câu ksqlDB.
- ACB L04: `:cif :id ...` và `?` trong SQL.
- ACB L05: `khoa.get(tk, ai) != ai` (code step1).
- ACB L06: VNeID (hook), `expires_at` số giây Unix.
- ACB L07: "EOD" (hook).
- ACB L08: `ctx` trong mã Go, "lũy đẳng".

## 9. Số đã tính lại / mã đã chạy

- A (INT L00-L05): Java 21 chạy được ở INT L01 (LuongAo, BigDecimal) và INT L02 (TuGoi): khớp màn hình; Python ở quymo/chaythat của INT L00-L05: khớp từng dòng; PL/SQL INT L03 và Java ONNX INT L05 chỉ đọc, không chạy.
- B: khoảng 210 số tính lại, khớp hết (INT L07 riêng 34/34); cham.sh ACB L00-L02 ĐÚNG.
- C: khoảng 100 phép, khớp hết; toàn bộ đoạn Python/sqlite trên màn hình khớp; Go/ksqlDB/PL/SQL chỉ đọc; 6 lab ĐÚNG.
- Người điều phối: 18/18 spec_sha256 khớp; 18/18 SRT = say (mục 2).

## 10. Khung hình đã xem

A: 6-8 ảnh mỗi bài; B: 5-7 ảnh mỗi bài; C: 5 ảnh mỗi bài (tổng 30), chưa xem riêng khung cảnh Tự làm của ACB L07 và L08 và khung bảng quymo của ACB L04 và L08 (đã đối chiếu qua YAML). Tên png và thời điểm từng bài ở phụ lục.
Lỗi hiển thị:
- INT L00: chữ "TẦNG 4: T24, NAPAS, TÍN DỤNG" tràn khỏi kim tự tháp.
- INT L00 và INT L03: chuỗi recap bị dàn ngang (khung 00104).
- INT L03: sơ đồ SAGA không có mũi tên.
- Các bài còn lại: không thấy lỗi hiển thị.

## 11. Nhận xét chung

- Gate cứng đạt: 0 MUST, 18/18 video không cũ so với đặc tả, 18/18 SRT = say, P8 = 2 ở 18/18, P9 = 2 ở 18/18, cả 18 lab làm được và khớp mong_doi.
- Gate mềm KHÔNG đạt: P1 = 2 ở 0/18 theo chuẩn chặt (ngưỡng 90%). Cách sửa tập trung: giảng tại chỗ (một câu lời thường hoặc một dòng chú thích trên màn hình) mọi cú pháp mã/đối số trước khi đưa vào khối mã, hoặc thay khối mã khó bằng bảng từng bước.
- Bài đáng ưu tiên nhất: INT L06 (P1=0 với 8 mục, tổng 9, P2/P5/P6 = 1), rồi INT L02, L03, L05, ACB L00, L02.
- Pháp lý: số hiệu và ngày hiệu lực (QĐ 2345, TT 50/2024, TT 77/2025, Luật 91/2025/QH15) khớp nguồn thứ cấp; INT và ACB nhất quán; việc chưa làm được là đối chiếu văn bản gốc và điều kiện đi kèm ngưỡng 10/20 triệu; đề xuất ghi trên màn hình "chưa kiểm văn bản gốc" ở INT L05/L06 như ACB L06 đã làm.
- Mâu thuẫn nội dung xuyên khoá duy nhất cần sửa: Squad Lending (ACB L00 quiz so với INT L08 hook); nên dùng cùng nhãn "tên nhóm lấy từ tin tuyển dụng, chưa kiểm".
- Mâu thuẫn nội bộ có thật cần sửa: ACB L02 (thứ tự khử trùng/giữ tiền, concept so với recap), INT L08 (ba lớp so với hai lớp), INT L04 (17 phút so với 300 giây), ACB L04 (25 ms), ACB L05 ("hàng giờ" so với 50 s; 10 s so với 33,3 s).
- Rủi ro lỗi thời: mốc "dự kiến tốt nghiệp 11/2026" trùng tháng hiện tại (INT L00/L01/L04/L05/L07, ACB L00); tin ACB "đọc 2026-11" cần ngày đọc.
- Không bài nào kẹt ở đề lab; chỗ kẹt của người mất gốc là thuật ngữ và cú pháp mã, không phải suy luận.
- Hạn chế của vòng đọc: đối chiếu pháp lý chỉ qua nguồn thứ cấp; một số khung cảnh Tự làm/quymo của ACB L04, L07, L08 chưa xem trực tiếp; mã Go/ksqlDB/PL/SQL/Java ONNX chỉ đọc, không chạy; tai người chưa nghe (chỉ so SRT với say).

---

# PHỤ LỤC: nguyên văn tệp từng bài của ba tác tử


## INT L00
sha16 YAML = 6001ff309b4f2c5b (khớp giao). 11 cảnh, 28 step; 15,38 phút (922,8 s / 60).

## Phần A — chuẩn xác
| Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng | Đề xuất | Tin cậy |
|---|---|---|---|---|---|
| SHOULD | concept step 1 (frame 00019, 2:03) | say: "Tầng hai là dịch vụ nhỏ và cơ sở dữ liệu." / show SVG: "TẦNG 2: MICROSERVICES, SPRING BOOT, REDIS" | Lời đọc nói "cơ sở dữ liệu", màn hình ghi Redis (kho dữ liệu trong RAM, bài tự giải thích ở step sau là "kho dữ liệu nằm trong RAM"), không phải CSDL quan hệ; lệch chi tiết lời đọc/màn hình. Tầng 3 trong khóa (L03) mới có Oracle. | Đổi lời đọc thành "dịch vụ nhỏ, Spring Boot và kho dữ liệu Redis" | CONFIRMED |
| SHOULD | quymo step 2 (bảng ×100) | "bể kết nối cỡ vài chục không đủ cho 500 yêu cầu dở" | 500 yêu cầu dở là số yêu cầu trong cả hệ thống, không phải số kết nối CSDL đang giữ; chỉ đúng nếu mỗi yêu cầu giữ một kết nối suốt 10 ms. Thiếu điều kiện áp dụng (L02 mới dạy "thời gian giữ kết nối"). | Thêm "nếu mỗi yêu cầu giữ một kết nối trong suốt thời gian ở lại" | PLAUSIBLE |
| SHOULD | symbol step 1 | "Tin tuyển dụng ACB ... ghi lương tháng 13 cố định và thưởng cuối năm 1–4 tháng lương tuỳ xếp loại, còn mức lương ghi 'Thương lượng'" | Số liệu tin tuyển dụng thật nhưng nguồn là "tin đã lưu"; trong YAML không có URL/ngày; bài có ghi "đối chiếu lại trước khi nộp" nên đã tự gắn nhãn chưa kiểm. Không sai, ghi "chưa kiểm được nguồn". | Giữ nhãn; thêm ngày lưu tin vào sources | PLAUSIBLE |
Không có MUST. Không có số sai: mọi phép tính khớp (xem mục 7).

## Điểm
P1=1 P2=2 P3=1 P4=2 P5=2 P6=2 P7=2 Tổng(P1–P7)=12 P8=2 P9=2 — Mất gốc: ĐỦ (sát ngưỡng 12).
Cần biết trước: cú pháp Python (for…in, print, `**`, round) ở quymo; "UIT" (viết tắt trường, không bung); khoá Redis `lock:transfer:TXN_998822 1` (khoá/giá trị đặt tên thế nào); "mili giây" bài tự giải thích mili = 1/1000 ở prereq? (có ghi "10 mili giây = 0,01 giây", đủ).
Chỗ thiếu chính: khối mã Python trong quymo cho người chưa từng lập trình.
P1<2 — DANH SÁCH mục chưa giảng:
1. quymo step 1: `for tps in (...)`, `print(...)`, `10 ** -chin`, `round(..., 2)` — lời đọc chỉ tả ý ("ba mức tải", "đổi số chín ra phút"), không giải thích cú pháp `**` (luỹ thừa) hay vòng lặp for. (1 mục, gộp cú pháp Python)
2. quymo step 1: `525600` (số phút một năm) xuất hiện trong mã khi chưa ai giải thích 365×24×60; chỉ được giải thích về sau ở cảnh practice "Nếu kẹt". Ở prereq con số 52,56 phút cũng chưa nêu cách ra.
(Biên giới, không tính: "UIT" ở pitfall chưa bung chữ.)

## Cảnh Tự làm / quy mô
- practice (10:57, tiêu đề "Tự làm: trả lời một câu phỏng vấn có số..."): giấy bút, 8 000 TPS × 25 ms, 99,95%, tin JBoss/JSP/MS SQL; pause 180 s; step sau hiện "Đáp án để đối chiếu": `dang xu ly do: 200 / ngung toi da 99.95%: 262.8 phut/nam / nhom tin tuyen dung: B`. CÓ kết quả mong đợi trên màn hình; KHỚP mong_doi.txt từng dòng.
- quymo (6:57): 500 / 50 000 / 5 000 000 TPS × 0,010 s → 5 / 500 / 50 000 yêu cầu dở; 2/3/4 số chín → 5256 / 525,6 / 52,56 phút/năm; bảng "điều gì gãy" + đánh đổi ("thêm số chín hay thêm máy đều tốn tiền"). Tính lại ĐÚNG (Python chạy ra đúng các dòng "Kết quả chạy thật").

## Lab (labs/INT/L00, giấy-bút .md)
Có làm được; ~3 phút. Đề đủ, định dạng 3 dòng rõ. Thiếu kiến thức: không (công thức Little và 525 600 có trong "Nếu kẹt"). mong_doi khớp màn hình cảnh Tự làm: CÓ. Tự tính bằng Python: 200 / 262.8 / B = đúng mong_doi. Lưu ý quy trình: tôi đã vô tình thấy 5 dòng đầu loi_giai.md/mong_doi.txt trong cùng lệnh với de.md trước khi tự tính (kết quả tự tính độc lập vẫn trùng) — người học thật không bị ảnh hưởng. cham.sh không chấm .md nên không chạy.

## Người học kẹt ở đâu
quymo step 1 — khối mã "for tps in (500, 50000, 5000000): print(tps, ..., tps * w, ...)" và "10 ** -chin": người chưa từng lập trình không đọc được; tuy nhiên có kết quả + lời đọc nên vẫn theo được ý chính (kẹt nhẹ, không kẹt hẳn).

## Số tính lại / mã chạy / khung hình
- Tính lại 14 số (5; 500; 50 000; 5256; 525,6; 52,56; 200; 262,8; 480; 520; 560; 680; 560/680 từ T=L(13+k); 52,56 prereq) = 14/14 khớp. Chạy đoạn Python trên màn hình: 6 dòng in ra KHỚP chữ-theo-chữ. Các `checks:` YAML tự nhất quán.
- Khung hình đã xem: 00000 (0:00), 00019 (2:03, kim tự tháp), 00050 (5:18, bài toán), 00063 (6:12, bước 3), 00066 (7:14, mã Python), 00096 (11:20, Tự làm), 00098 (14:34, "Nếu kẹt"), 00104 (15:14, tổng kết).
- Lỗi hiển thị: (a) 00019 chữ "TẦNG 4: T24, NAPAS, TÍN DỤNG" tràn ra ngoài hai cạnh kim tự tháp, bị đường viền cắt qua "T" và "G"; chữ "TẦNG 5: AI" cỡ 10 rất nhỏ. (b) 00104 sơ đồ chuỗi "node/arrow" bị dàn ngang: "1. … ↓ 2. … ↓" nối liền trên cùng dòng, không còn là chuỗi dọc. Cả hai nhẹ, vẫn đọc được.

## Bảng sự kiện cần nhất quán
| Sự kiện | Giá trị | bài:cảnh |
|---|---|---|
| Lương minh hoạ L | 40 triệu/tháng; T = L×(13+k), k 1–4 → 560–680 triệu | L00:symbol, L00:quiz |
| Tin tuyển dụng ACB (đã lưu, chưa kiểm) | tháng 13 cố định; thưởng 1–4 tháng; lương "Thương lượng" | L00:symbol, L00:quiz |
| Hai nhóm vai trò | A: Spring Boot/Kafka/Redis/Saga/Outbox; B: JBoss/JSP/Oracle/MS SQL, sở hữu mảng nghiệp vụ; mức 3 và bản thiết kế ở cả hai | L00:concept step 4, L00:practice |
| Chương trình Cử nhân AI UIT | dự kiến tốt nghiệp 11/2026 | L00:pitfall, L00:recap |
| Sẵn sàng 99,99% | 52,56 phút/năm (năm 365 ngày = 525 600 phút) | L00:prereq, quymo |
| 99,95% | 262,8 phút/năm | L00:practice |
| Little | 50 000 TPS × 10 ms = 500 | L00:prereq step 2 |
| Khoá Redis chống trùng | SET ... NX EX 60 (hết hạn 60 s); bấm hai lần cách 500 ms; chuyển 20 triệu | L00:example |
| Chống trừ tiền kép | 4 bước: mã yêu cầu, khoá Redis, UNIQUE, hàng đợi IBM MQ | L00:example |
| Hệ thống tên | T24 (Temenos), NAPAS, IBM MQ | L00:concept, example |
| Không có số pháp lý nào trong bài | — | — |


## INT L01
sha16 YAML = 6f96414358fde365 (khớp). 11 cảnh, 27 step; 14,31 phút (858,77 s / 60).

## Phần A — chuẩn xác
| Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng | Đề xuất | Tin cậy |
|---|---|---|---|---|---|
| SHOULD | concept step 3 (bảng GC) | show: "Thu gom rác toàn phần (Full GC) ... Dừng toàn bộ hệ thống, nguyên nhân gây quá hạn API" | Khẳng định chung cho mọi bộ thu gom rác. Java 21 mặc định dùng G1; ZGC/Shenandoah dừng dưới mili giây và Full GC của G1 hiếm. Lời đọc đã nhẹ hơn ("một nguyên nhân thường gặp", "vùng nhớ lớn có thể kéo dài tới hàng giây") nhưng chữ trên màn hình tuyệt đối. Thiếu điều kiện (bộ thu gom nào, kích cỡ heap). "Major GC" cũng không phải thuật ngữ chính thức trong JVM (chỉ minh hoạ). | Sửa chữ show: "có thể dừng hàng giây với heap lớn; G1/ZGC giảm mạnh" | PLAUSIBLE |
| SHOULD | example step 4 (mã Java), say | "bạn gõ lại từ trên xuống rồi chạy được" | Mã chạy đúng (JDK 21.0.13: in "xong 10000 tac vu", 1,3 s) nhưng bài không nói cách biên dịch/chạy (javac LuongAo.java; java LuongAo) và lab không có tệp này; người mất gốc không chạy được theo lời đọc. Kết quả in cũng không chứng minh gì về 10 000 luồng (không đo thời gian/không so với bể luồng). | Thêm 2 lệnh chạy và in thời gian (vd System.nanoTime) để thấy ≈ 50 ms thay vì 10 000×50 ms | CONFIRMED (chạy thử) |
| SHOULD | prereq step 1 | "Thanh ghi CPU 0.5 nano giây ... L1 1 nano giây ... RAM 100 nano giây" | Số xấp xỉ, đã ghi "số liệu xấp xỉ, minh họa; tuỳ đời CPU" — chấp nhận được; nhưng "nano giây" chưa giảng (1 phần tỉ giây). Dùng dấu chấm thập phân kiểu Anh (0.5) trong bài tiếng Việt, lẫn với "0,01" ở L00. | Giải "nano = một phần tỉ" | CONFIRMED (nhỏ) |
Không có MUST. Mọi phép tính ĐÚNG; mã Java và Python chạy khớp màn hình.

## Điểm
P1=1 P2=2 P3=2 P4=2 P5=2 P6=2 P7=2 Tổng(P1–P7)=13 P8=2 P9=2 — Mất gốc: ĐỦ.
Cần biết trước: cú pháp Java (class/main/try-with-resources/var/lambda `() -> {}`/submit/`10_000`), cú pháp Python (`while`, `*=`, `**`, gán đa biến `cao, suc = 0, 1`), "nano giây", "lôgarit" (chỉ giải bằng trực giác O(log N)), IEEE 754 (nêu tên, không giảng).
P1<2 — DANH SÁCH mục chưa giảng:
1. example step 4: toàn bộ mã Java LuongAo (khai báo `public static void main`, `try (var ex = …)`, lambda `() -> { Thread.sleep(50); return 1; }`, `ex.submit`) — lời đọc chỉ tả hiệu ứng ("tạo mười nghìn luồng ảo, mỗi luồng ngủ 50 mili giây", "khối bao ngoài tự đợi") chứ không giải cú pháp; lời bảo "gõ lại" làm người học cần đọc được. (1 mục, gộp)
2. quymo step 1: mã Python `while suc < n: suc *= m; cao += 1`, `10**4`, `cao, suc = 0, 1` — chỉ tả ý "đếm số tầng". (1 mục, gộp)
(Biên giới, không tính: "nano giây" chưa giảng; tên "IEEE 754", "JEP 444" nêu tên không giảng.)

## Cảnh Tự làm / quy mô
- practice (10:25, "Tự làm: trả lời một câu phỏng vấn có số về chỉ mục và bộ nhớ luồng"): giấy bút; 80 000 000 dòng, 500 nhánh, 2 000 tác vụ, 1 MB, 2 000 byte; pause 180 s; step sau hiện đáp án "chieu cao cay: 3 / so lan doc mot dong: 4 / ngan xep luong he dieu hanh: 2000 MB / ngan xep luong ao: 4000000 byte". CÓ kết quả trên màn hình; KHỚP mong_doi.txt.
- quymo (6:49): bảng 10 nghìn / 10 triệu / 10 tỉ dòng → cây cao 2/3/4 → đọc 3/4/5 lần; quét toàn bảng 10^4/10^7/10^10 dòng; đánh đổi (chỉ mục tốn đĩa, chậm ghi). Tính lại ĐÚNG (Python while-loop và log_1000). Ngoài ra example nêu 10 000 luồng: 10 GB dự trữ vs 20 MB.

## Lab (labs/INT/L01, giấy-bút .md)
Làm được, ~3 phút; đề đủ, định dạng rõ, công thức nằm ngay trong đề ("500^h ≥ 80 000 000"). Tự tính trước khi mở loi_giai: 3 / 4 / 2000 MB / 4 000 000 byte = ĐÚNG mong_doi.txt (đã so sau). Không kẹt. mong_doi khớp màn hình cảnh Tự làm: CÓ. cham.sh không chấm .md.

## Người học kẹt ở đâu
example step 4 (mã Java): "import java.util.concurrent.*; public class LuongAo { ... ex.submit(() -> { Thread.sleep(50); return 1; }); ..." — người chưa học Java không đọc được và không biết chạy ra sao; vẫn theo được ý chính nhờ lời đọc + kết quả.

## Số tính lại / mã chạy / khung hình
- Tính lại: 64/8=8; 0,1+0,2 → 0.30000000000000004 (17 chữ số sau dấu phẩy, khớp "thứ mười bảy"); log_1000(10^7)=2,333 → H=3; 4 lần đọc; 10 000×1 MB≈10 GB; 10 000×2 000 B=20 MB; Python quymo 3 dòng; 50 triệu dòng → H=3 (log=2,57) → 4 lần (phù hợp "3 đến 4"); lab 4 số; 500^3≥8·10^7>500^2 = 17/17 khớp. Mã chạy: Java LuongAo (JDK 21.0.13) KHỚP; Java BigDecimal/double (0.30000000000000004 / 0.3) KHỚP; Python quymo KHỚP.
- Khung hình đã xem: 00012 (1:18, chia sẻ giả), 00024 (2:45, sơ đồ JVM), 00048 (5:29, luồng ảo), 00054 (mã Java), 00061 (6:57, mã Python), 00088 (10:25, Tự làm), 00095 (14:09, tổng kết).
- Lỗi hiển thị: không có lỗi đáng kể (sơ đồ JVM vừa khung; chữ SVG nhỏ nhưng đọc được; "-XX:-RestrictContended" bị ngắt dòng ở dấu "-" nhưng đọc được).

## Bảng sự kiện cần nhất quán
| Sự kiện | Giá trị | bài:cảnh |
|---|---|---|
| Khối đệm CPU | 64 byte (trên hầu hết CPU máy chủ); long = 8 byte → 8 biến/khối | L01:prereq step 2 |
| Độ trễ (minh hoạ) | thanh ghi 0,5 ns; L1 1 ns; L2 3–10; L3 20–40; RAM 100 ns | L01:prereq step 1 |
| double | 0.1+0.2 = 0.30000000000000004 → dùng BigDecimal | L01:prereq step 3 |
| Ngăn xếp luồng OS | mặc định thường 1 MB/luồng | L01:concept, symbol |
| Luồng ảo Java 21 | JEP 444; ~2 000 byte (minh hoạ, vài trăm B đến vài KB); pinning với synchronized; JEP 491 (Java 24) gỡ | L01:symbol, example |
| Spring Boot 3.2+ | spring.threads.virtual.enabled=true; HikariCP là giới hạn đồng thời | L01:example step 5 |
| B-Tree | m=1000: 10^7 dòng → 3 tầng → 4 lần đọc; 10^4 → 2/3; 10^10 → 4/5 | L01:symbol, quymo |
| Lab | 80 triệu dòng, m=500 → 3 tầng, 4 lần; 2 000 luồng → 2 000 MB vs 4 000 000 B | L01:practice |
| Cổng thanh toán minh hoạ | 10 000 kết nối đồng thời; 50 ms chờ core; 16 GB, 8 nhân | L01:example |
| ISO 8583, OFS (Temenos T24) | nêu tên và giải nghĩa ngắn | L01:quiz |
| Không có số pháp lý/lương | — | — |


## INT L02
sha16 YAML = 6094c2508ee95b93 (khớp). 12 cảnh (hook, prereq, concept, chaythat, symbol, example, quymo, check, pitfall, quiz, practice, recap), 30 step; 14,40 phút (863,77 s / 60).

## Phần A — chuẩn xác
| Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng | Đề xuất | Tin cậy |
|---|---|---|---|---|---|
| SHOULD | symbol step 2 vs example step 2 | symbol: `SET dedup:transfer:{requestId} "PROCESSING" NX EX 120` ; example: `redis.setIfAbsent("trans:" + reqId, "PROCESSING", 120, ...)` | Hai cảnh trong cùng bài dùng hai tên khoá khác nhau (dedup:transfer:… vs trans:…) cho cùng một cơ chế; L00:example dùng `lock:transfer:TXN_998822 … EX 60` (60 s). Chỉ là minh hoạ nhưng người học dễ hỏi "khoá nào đúng". Cũng `{requestId}` (chỗ giữ chỗ) không được giải. | Thống nhất một tên khoá và nói rõ TTL chọn theo thời gian xử lý tối đa | CONFIRMED |
| SHOULD | quymo step 2 (bảng ×10) | "rút ngắn thời gian giữ: không gọi mạng khi đang giữ kết nối" / phía trước: "mỗi giao dịch giữ một kết nối hai mươi mili giây" | Trần 850/s = 17 / 0,020 đúng, nhưng chỉ khi MỌI giao dịch giữ kết nối 20 ms liên tục; bài không nêu điều kiện này như giả định (đã ghi "số minh hoạ"). Chấp nhận. Chỉ lưu ý quymo bỏ qua điều kiện "pool 17 tính cho DB 8 nhân, tổng mọi instance" (có ở symbol). | Thêm 1 câu điều kiện | PLAUSIBLE (nhẹ) |
| SHOULD | prereq step 3 + practice | "Cách làm thường gặp: ghi nhật ký kiểm toán bằng REQUIRES_NEW ... cần thêm một kết nối từ bể" | Video dừng ở "cần thêm một kết nối"; KHÔNG nêu rủi ro bế tắc cạn bể (mọi giao dịch chính giữ 1 kết nối và chờ kết nối thứ hai). Rủi ro này CÓ trong labs/INT/L02/loi_giai.md (ghi chú) nhưng không có trên video. Kiến thức senior bị hụt ở video. | Thêm một câu/ô trong quymo hoặc pitfall: giới hạn số giao dịch chính < kích thước bể | CONFIRMED (đối chiếu lab) |
Không có MUST. Kiểm tra: quy tắc rollback (RuntimeException/Error; checked không rollback) ĐÚNG; mức REQUIRED/REQUIRES_NEW ĐÚNG; RFC 9457 (2023, thay RFC 7807) ĐÚNG; công thức nhân×2+đĩa (PostgreSQL wiki, HikariCP dẫn lại) ĐÚNG và có ghi "không phải định lý"; 202/409/422 ĐÚNG; Bloom (không âm tính giả, có dương tính giả) ĐÚNG; Filter trước DispatcherServlet, Interceptor trong DispatcherServlet ĐÚNG; Java mô phỏng proxy chạy đúng.

## Điểm
P1=0 P2=2 P3=2 P4=2 P5=2 P6=2 P7=2 Tổng(P1–P7)=12 P8=2 P9=2 — Mất gốc: GẦN (≥12 nhưng có một mục 0).
Cần biết trước: Singleton/"trạng thái khả biến", PostConstruct, failover, "luân chuyển/đổi ngữ cảnh" (context switch), cú pháp Java của mã Spring (try/catch, `Boolean.TRUE.equals`, `ResponseEntity`, `TimeUnit`), `Class<?>[]`/`Proxy.newProxyInstance`, `{requestId}`, cú pháp Python (`for`, `if … else` nội tuyến, `round`).
P1<2 — DANH SÁCH mục chưa giảng:
1. prereq step 2 (bảng vòng đời bean): "Singleton dùng chung giữa các luồng: không giữ trạng thái khả biến" — Singleton, "trạng thái khả biến" không có định nghĩa; và "Thực thi các hàm đánh dấu PostConstruct".
2. example step 4 (bảng hành vi): "Redis mất khoá khi failover" — failover (chuyển sang máy dự phòng) không được giải.
3. pitfall: "Hệ thống bị treo cứng do luân chuyển ngữ cảnh" / lời đọc "liên tục đổi ngữ cảnh" — đổi ngữ cảnh (context switch) chưa được giải (L01 chỉ nhắc "chi phí chuyển đổi ngữ cảnh luồng", cũng không giải).
4. example step 2–3: mã Java của cổng (`Boolean.TRUE.equals(locked)`, `catch (ValidationException ex)`, `ResponseEntity.accepted().build()`, `TimeUnit.SECONDS`) — lời đọc tả ý nghiệp vụ, không giải cú pháp; chaythat chỉ giải interface/implements/static class/lambda/invoke, KHÔNG giải `Class<?>[] gt = { Dv.class }`, `Proxy.newProxyInstance`, `moGD++`.
5. quymo: mã Python (`for … in`, `x if … else y`, `round`) — không giải cú pháp.
(Mục 1–3 là khái niệm; 4–5 là cú pháp mã.)

## Cảnh Tự làm / quy mô
- practice (10:30, "Tự làm: trả lời một câu phỏng vấn có số về bể kết nối và nhật ký giao dịch độc lập"): giấy bút; 16 nhân, 2 đĩa, 20 ms, +5 ms REQUIRES_NEW; pause 180 s; step sau: "be ket noi: 34 / toi da khong nhat ky: 1700 giao dich/giay / toi da co nhat ky REQUIRES_NEW: 1360 giao dich/giay". CÓ kết quả trên màn hình; KHỚP mong_doi.txt.
- quymo (6:40): 500/5 000/50 000 TPS × 0,020 s → cần 10/100/1 000 kết nối, bể 17 → đủ/thiếu/thiếu, trần 850 TPS; bảng "điều gì gãy" + đánh đổi (cache/queue làm dữ liệu trễ; REQUIRES_NEW giữ thêm kết nối). Tính lại ĐÚNG (Python chạy ra y chữ trên màn hình).

## Lab (labs/INT/L02, giấy-bút .md)
Làm được, ~3 phút. Đề đủ (công thức nằm sẵn trong đề ở từng dòng). Tự tính trước khi mở loi_giai: 34 / 1700 / 1360 = ĐÚNG mong_doi.txt. mong_doi khớp màn hình: CÓ. Điểm cộng: loi_giai.md có ghi chú bế tắc cạn bể mà video không nêu. cham.sh không chấm .md.

## Người học kẹt ở đâu
prereq step 2 — "Singleton dùng chung giữa các luồng: không giữ trạng thái khả biến" (và "Thực thi các hàm đánh dấu PostConstruct"): người mất gốc chưa biết singleton/khả biến; còn lại đa số theo được vì từ vựng được giảng ở prereq step 1 và chaythat.

## Số tính lại / mã chạy / khung hình
- Tính lại: 8×2+1=17; 10/100/1 000 kết nối; 17/0,020=850; 16×2+2=34; 34/0,020=1 700; 34/0,025=1 360 = 8/8 khớp. Mã chạy: Java TuGoi (JDK 21) in đúng 6 dòng như màn hình (số giao dịch 1 rồi 2) KHỚP; Python quymo 4 dòng KHỚP.
- Khung hình đã xem: 00021 (2:23, sơ đồ vỏ proxy), 00029 (3:15, mã TuGoi), 00034 (3:50, gọi hai hàm), 00055 (6:40, mã Python quymo), 00084 (10:30, Tự làm), 00091 (14:14, tổng kết). Không thấy lỗi hiển thị (mã Java dài vẫn vừa khung, sơ đồ SVG đọc được, recap chuỗi bị dàn thành đoạn văn nhưng đọc được).

## Bảng sự kiện cần nhất quán
| Sự kiện | Giá trị | bài:cảnh |
|---|---|---|
| Rollback mặc định Spring | chỉ RuntimeException và Error; checked exception vẫn commit; rollbackFor = Exception.class | L02:concept step 2 |
| REQUIRED / REQUIRES_NEW | REQUIRES_NEW cần gọi qua proxy (bean khác) + thêm 1 kết nối | L02:prereq step 3 |
| Mã HTTP | 200 xong, 202 đã nhận chưa xong, 409 xung đột, 422 không xử lý được | L02:prereq, symbol, example |
| RFC 9457 | IETF 2023, thay RFC 7807; trường type/title/status/detail | L02:symbol step 3 |
| Công thức bể kết nối | nhân×2 + số đĩa (PostgreSQL wiki, HikariCP dẫn), DB 8 nhân 1 đĩa → 17; điểm khởi đầu, không phải định lý | L02:symbol step 1 |
| Khoá chống trùng Redis | SET … NX EX 120 (symbol, example) vs L00 NX EX 60; kết quả lưu 86 400 s; PENDING khi core quá hạn | L02:symbol/example; L00:example |
| Trần bể 17 kết nối | 17/0,020 = 850 TPS; ×10 → 100 kết nối; ×100 → 1 000 | L02:quymo |
| Lab | 16 nhân, 2 đĩa → 34; 1 700; 1 360 TPS | L02:practice |
| Bộ lọc Bloom | không âm tính giả (nếu nạp đủ), có dương tính giả | L02:check |
| mTLS | Servlet Filter (A) | L02:quiz |
| Không có số pháp lý/lương | — | — |


## INT L03
sha16 YAML = 6947e1676429c89c (khớp). 11 cảnh, 30 step; 14,14 phút (848,6 s / 60).

## Phần A — chuẩn xác
| Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng | Đề xuất | Tin cậy |
|---|---|---|---|---|---|
| SHOULD | quymo step 1–2 | code: `giu = 2 * rtt # 2PC: khoa giu qua hai vong hoi dap` ; `s = 0.004 # SAGA: chi giu khoa trong giao dich cuc bo 4 ms` | So sánh không đối xứng, giả định không nói ra: thời gian giữ khoá của 2PC chỉ tính 2×RTT, không cộng 4 ms giao dịch cục bộ (thực tế ≥ 4 ms + 2×RTT); SAGA không tính khoá của bước bồi hoàn khi đối tác lỗi. Kết luận định tính (2PC gãy khi đối tác chậm) vẫn đúng; phép tính 400/4 000/40 000 s và 40 s đã tính lại ĐÚNG theo mô hình đó. | Thêm "mô hình rút gọn: chưa tính 4 ms cục bộ của 2PC, chưa tính bước bồi hoàn" | PLAUSIBLE |
| SHOULD | example step 4 (hộp "Không dựa vào ORDER BY … FOR UPDATE") | "FK thiếu index" | Thuật ngữ FK (khoá ngoại) xuất hiện ở đây trước khi được định nghĩa ở cảnh pitfall (3 cảnh sau): người mất gốc không biết FK. Không phải sai kiến thức. | Bung "khoá ngoại (FK)" tại chỗ | CONFIRMED |
| SHOULD | example step 3 (PL/SQL BULK COLLECT) | "OPEN cur_payroll; LOOP FETCH ... BULK COLLECT INTO l_accounts LIMIT 1000; ... FORALL i IN 1..l_accounts.COUNT UPDATE ..." | Đoạn trích khai báo kiểu `l_accounts` và `cur_payroll` không có; chỉ đọc, KHÔNG chạy được (không có Oracle ở môi trường kiểm). Theo hiểu biết Oracle ≥ 11g cú pháp hợp lệ (FORALL tham chiếu trường bản ghi được từ 11g). Ghi "chỉ đọc, không chạy". | Ghi chú rõ "trích, thiếu DECLARE" (đã có chữ "trích thân thủ tục") | PLAUSIBLE (không chạy) |
Không có MUST. Đã kiểm: CAP (A = "mọi yêu cầu nhận phản hồi không lỗi, không phải tỉ lệ uptime") ĐÚNG và tách rõ khỏi availability 99,99% ở L00; ACID ví dụ 5/2 → 4/3 ĐÚNG; Kafka acks=all + min.insync.replicas=2 + RF=3 (hỏng 1 broker vẫn ghi, hỏng 2 từ chối) ĐÚNG; producer idempotent chỉ khử trùng do producer tự retry (ĐÚNG, có nêu giới hạn); TLS làm mất zero-copy (ĐÚNG); Oracle FK không index → khoá bảng con khi xoá/sửa khoá cha (ĐÚNG, ghi "trong lúc câu lệnh chạy"); deadlock graph trong trace file ORA-00060 (ĐÚNG); lời nhắc "ORDER BY … FOR UPDATE không bảo đảm thứ tự khoá" thận trọng, chấp nhận.

## Điểm
P1=0 P2=2 P3=1 P4=2 P5=2 P6=2 P7=2 Tổng(P1–P7)=11 P8=2 P9=2 — Mất gốc: GẦN.
Cần biết trước: FK/khoá ngoại (dùng trước khi giảng), WAL / redo log, OS Page Cache + `sendfile(socket_fd, file_fd, offset, count)`, cú pháp PL/SQL (`:=`, `SELECT … INTO`, `OPEN/LOOP/FETCH … BULK COLLECT … LIMIT`, `FORALL`, `EXIT WHEN`), cú pháp Python (for + gán bộ, list of tuple, `round`), "ORDER BY".
P1<2 — DANH SÁCH mục chưa giảng:
1. example step 4: "ORA-00060 vẫn có thể đến từ luồng khác hoặc FK thiếu index" — FK/khoá ngoại dùng trước khi định nghĩa (định nghĩa ở pitfall).
2. concept step 3: "đọc nhật ký giao dịch của cơ sở dữ liệu (WAL / redo log)" — WAL, redo log không giải; "nhật ký giao dịch" chỉ gọi tên.
3. symbol step 3: "sendfile(socket_fd, file_fd, offset, count); … OS Page Cache -> Network Socket Buffer" — page cache, socket buffer, đối số không giải (lời đọc chỉ nói "lệnh truyền trực tiếp").
4. example step 3: mã PL/SQL `OPEN … LOOP FETCH … BULK COLLECT INTO … LIMIT 1000; EXIT WHEN …; FORALL i IN 1..l_accounts.COUNT` và step 2 `v_first := LEAST(...)`, `SELECT … INTO` — lời đọc tả ý ("lấy theo từng lô một nghìn dòng"), không giải cú pháp; có giải SELECT/FOR UPDATE/UPDATE/con trỏ/BULK COLLECT/FORALL ở mức khái niệm.
5. quymo step 1: mã Python (`for ten, rtt in doi_tac`, `toc, xong = …`, list of tuple).
(Mục 1–3 là khái niệm; 4–5 là cú pháp mã.)

## Cảnh Tự làm / quy mô
- practice (10:15, "Tự làm: trả lời một câu phỏng vấn có số về xử lý lô lương và thời gian giữ khoá"): giấy bút; 24 000 dòng, lô 2 000, 2 lần đổi ngữ cảnh, đối tác 15 ms, SAGA 3 ms; pause 180 s; step sau "so lo: 12 / doi ngu canh tung dong: 48000 / doi ngu canh theo lo: 24 / giu khoa 2PC: 30 ms / toi da 2PC …: 33 / toi da SAGA …: 333". CÓ kết quả trên màn hình; KHỚP mong_doi.txt. Ghi chú: thuật ngữ "dòng nóng" được định nghĩa trong de.md (và lời đọc quymo), không có trên màn hình cảnh Tự làm.
- quymo (6:15): đối tác 20/200/2 000 ms → 2PC giữ 40/400/4 000 ms, 25/2,5/0,25 lệnh/s, 400/4 000/40 000 s (>11 giờ); SAGA 4 ms → 250 lệnh/s, 40 s; đánh đổi (nhất quán sau một lúc, bước bù trừ lũy đẳng). Tính lại ĐÚNG; xem SHOULD đầu về giả định ẩn.
- Cũng example step 5: 10 000 dòng × 2 = 20 000 lần đổi ngữ cảnh vs 10 lô × 2 = 20 (có nêu "mô hình đơn giản hoá").

## Lab (labs/INT/L03, giấy-bút .md)
Làm được, ~4 phút; đề đủ (de.md nêu công thức từng dòng, có định nghĩa "dòng nóng"). Tự tính trước khi mở loi_giai: 12 / 48000 / 24 / 30 ms / 33 / 333 = ĐÚNG mong_doi.txt. mong_doi khớp màn hình: CÓ. cham.sh không chấm .md.

## Người học kẹt ở đâu
example step 4 — "ORA-00060 vẫn có thể đến từ luồng khác hoặc FK thiếu index" (FK chưa định nghĩa); và nặng hơn ở example step 3 — mã PL/SQL "FETCH cur_payroll BULK COLLECT INTO l_accounts LIMIT 1000 … FORALL i IN 1..l_accounts.COUNT" (người chưa biết PL/SQL không đọc được cú pháp, chỉ theo được lời đọc).

## Số tính lại / mã chạy / khung hình
- Tính lại: 7=5+2; 3−2=1; 20 000/20; 25,0/2,5/0,25; 400/4 000/40 000; 40 000 s = 11,1 giờ ("hơn 11 giờ" đúng); 4 000 s = 1,11 giờ ("hơn 1 giờ" đúng); 250/40; lab 6 số; 150 tỉ/10 000 = 15 triệu/người (YAML check) = 15/15 khớp. Python quymo 4 dòng KHỚP. PL/SQL: chỉ đọc, không chạy (không có Oracle).
- Khung hình đã xem: 00024 (2:38, sơ đồ SAGA), 00039 (4:35, dữ liệu bài toán ORA-00060), 00043 (5:13, khoá có thứ tự), 00052 (6:15, mã Python), 00066 (8:08, bẫy phân vùng/FK), 00083 (13:20, đáp án Tự làm).
- Lỗi hiển thị: sơ đồ SAGA (00024) không có mũi tên, ba đường nối kiểu hình sao, không thể hiện thứ tự bước và luồng bồi hoàn (chỉ ghi chữ "Bồi hoàn: Hoàn tiền CASA") — hình minh hoạ chứ chưa cho thấy cơ chế (P3=1). Không có hình cho chu trình bế tắc A→X→Y (chỉ chữ). Phần còn lại vừa khung.

## Bảng sự kiện cần nhất quán
| Sự kiện | Giá trị | bài:cảnh |
|---|---|---|
| CAP | khi phân vùng mạng chọn C hay A; số dư chọn nhất quán; "availability" CAP ≠ uptime | L03:prereq step 1 (khác nghĩa với L00:prereq: Availability = tỉ lệ thời gian phục vụ) |
| ACID ví dụ | A 5 triệu, B 2 triệu, chuyển 1 triệu → 4 và 3, tổng 7 | L03:prereq step 2 |
| Kafka | acks=all, min.insync.replicas=2, replication.factor=3, enable.idempotence=true; hỏng 1 broker vẫn ghi, hỏng 2 từ chối | L03:symbol, recap |
| Outbox | ghi chung transaction; CDC (Debezium) đọc redo log/WAL; giao nhận at-least-once → consumer idempotent | L03:concept step 3 |
| SAGA | điều phối tập trung; hết giờ chờ ≠ từ chối, hỏi lại trạng thái trước khi bồi hoàn | L03:concept step 2 (khớp L00:check IN_DOUBT, L02 PENDING) |
| 2PC vs SAGA (minh hoạ) | đối tác 20/200/2 000 ms; 2PC giữ 2×RTT; SAGA giữ 4 ms; 10 000 lệnh → 400/4 000/40 000 s vs 40 s | L03:quymo |
| Lô lương minh hoạ | 10 000 nhân viên, 150 tỉ đồng; lô 1 000 dòng → 10 lô; đổi ngữ cảnh 20 000 vs 20 | L03:example |
| Lab | 24 000 dòng, lô 2 000 → 12 lô; 48 000/24; 2PC 30 ms → 33/s; SAGA 3 ms → 333/s | L03:practice |
| Oracle | ORA-00060 = phát hiện bế tắc; tệp .trc trong ADR; khoá hàng nhỏ trước lớn sau; FK không index khoá bảng con | L03:example, pitfall, quiz |
| Phiên bản | Oracle Database 19c | L03:title |
| Không có số pháp lý/lương | — | — |


## INT L04
sha16 YAML = 5ad87d0202323101 (khớp). 11 cảnh, 24 step; 15,70 phút (941,87 s / 60).

## Phần A — chuẩn xác
| Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng | Đề xuất | Tin cậy |
|---|---|---|---|---|---|
| SHOULD | quymo step 2 (bảng, hàng ×10) | show: "khoá sống lâu hơn 17 phút và chỉ có STAN sẽ chặn nhầm một giao dịch mới trùng số" ; lời đọc: "STAN quay lại sau khoảng mười bảy phút, nên khoá sống lâu hơn thế" | Đầu cảnh đã đặt "khoá khử trùng sống 300 giây". Ở 1 000 gd/s STAN quay sau 1 000 s > 300 s nên khoá 300 s KHÔNG chặn nhầm; câu chỉ đúng nếu khoá sống > 17 phút (giả định khác, không nêu rõ là "nếu"). Người học dễ hiểu mâu thuẫn với 300 s. Phép tính 1 000 s (16,67 phút) đúng. | Viết "nếu khoá sống lâu hơn 17 phút (vd. giữ 24 giờ)" hoặc bỏ hàng này | CONFIRMED (mơ hồ) |
| SHOULD | symbol step 2 vs pitfall/quiz/practice | show bản tin 0200 minh hoạ có trường 0, 3, 4, 11, 37, 52 | Các cảnh sau lấy khoá khử trùng theo "trường 7 (thời điểm gửi gốc)" và "mã thiết bị" (trường 41) và lab dùng bitmap 3, 7, 11, 41; bản tin minh hoạ ở symbol lại KHÔNG có trường 7 và 41. Mâu thuẫn nhẹ giữa các ví dụ. | Thêm trường 7 và 41 vào bản tin mẫu | CONFIRMED |
| SHOULD | check step 1–2; pitfall | "mã phản hồi 68 (theo cách gọi phổ biến: giao dịch nghi vấn do ngân hàng thụ hưởng chưa trả lời kịp; đặc tả NAPAS cần kiểm)" ; "Mã 68 trong chuẩn ISO 8583 gốc nghĩa là phản hồi về quá muộn" | Chưa kiểm được nguồn: đặc tả NAPAS 247 không có công khai để đối chiếu. Phần ISO 8583:1987 "68 = response received too late" đúng theo hiểu biết của tôi. Bài đã gắn nhãn "cần kiểm" 6 lần nên không phải sai; nhưng đáp án quiz (C) dựa trên cách gán nghĩa chưa kiểm. | Giữ nhãn; thêm ghi chú "đặc tả ngân hàng thật mới là nguồn" vào sources | PLAUSIBLE (chưa kiểm được nguồn) |
Không có MUST. Đã kiểm đúng: MTI 0200/0210/0400/0420 và các chữ số; bit 1 = còn bitmap thứ hai; MAC ở trường 64/128; trường 4 (12 chữ số, VND 0 số lẻ theo ISO 4217), 7, 11 (6 chữ số), 37 (12 ký tự), 41; XOR ISO 9564 format 0 (04122D789ABCDEF6 và lab 045802BA9876FEDC chạy lại khớp); lệnh payShield CA (TPK→ZPK), CC (ZPK→ZPK), JE/JC (→LMK) và ZMK chỉ bọc khoá — đúng theo hiểu biết, chưa mở tài liệu Thales; OFS cú pháp `APP,VERSION/OP/PROCESS//n,USER/PASS,,FIELD=VALUE` — đúng theo hiểu biết, bài tự ghi "chưa kiểm được phiên bản".
Quan sát cá nhân/CV: hook step 1 có chữ "ứng viên đã tích hợp với T24 ở OCB" (chỉ trên màn hình, lời đọc bỏ qua) — khẳng định về CV người thật, chưa kiểm được nguồn trong bài; xem bảng sự kiện.

## Điểm
P1=0 P2=2 P3=2 P4=2 P5=2 P6=2 P7=2 Tổng(P1–P7)=12 P8=2 P9=2 — Mất gốc: GẦN (12 nhưng có một mục 0).
Cần biết trước: cú pháp Python `1 << (64 - b)`, `sum(... for b in bit)`, `[-13:-1]` (cắt chuỗi), `f"{x:016X}"`, `int("…", 16)`, `^`; tên lệnh HSM CA/CC/JE/JC và khoá TPK/ZPK/LMK/ZMK (có giải một dòng, rất nặng); "payShield", "ISO 9564", "ISO 4217" (nêu tên); "bể luồng chặn" (có giải).
P1<2 — DANH SÁCH mục chưa giảng (cú pháp mã, đường chính của mục tiêu 2 "bằng mã Python chạy thật"):
1. chaythat step 1: `sum(1 << (64 - b) for b in bit)` — toán tử dịch bit `<<`, biểu thức sinh trong sum; lời đọc chỉ tả "mỗi trường bật một bit đếm từ bên trái".
2. chaythat step 1: `"4321987654321098"[-13:-1]` — cắt chuỗi lấy 12 ký tự trước ký tự cuối; chỉ có giải bằng lời ở prereq (không gắn với cú pháp).
3. chaythat step 1: `f"{bm:016X}"` — định dạng in hệ 16, 16 chữ số, chữ hoa; `int("…", 16)`; `pin ^ pan`.
4. quymo step 1: `for tps in (...)`, `10**6 / tps`.
5. concept/prereq: hầu hết thuật ngữ khác đã giảng (OFS, ISO 8583, MTI, bitmap, hex, XOR, PIN block, HSM, MQ, STAN, RRN, MAC, TCP, khoá phân tán/nguyên tử/Redis). Riêng "đối soát" và "In-doubt" dùng trong bài này dựa vào L00 (chấp nhận trong cùng khoá).

## Cảnh Tự làm / quy mô
- practice (10:16, "Tự làm: câu phỏng vấn có số về bản đồ bit, khối PIN, vòng quay STAN"): giấy bút; trường 3, 7, 11, 41; PIN 5821 + thẻ 5412345678901234; 4 000 gd/s, khoá 300 s; chờ 1,5 s; pause 240 s; step sau: `bitmap: 2220000000800000 / khoi PIN: 045802BA9876FEDC / STAN quay vong sau: 250 giay / chan nham: co / tin dang cho: 6000`. CÓ kết quả trên màn hình; KHỚP mong_doi.txt. Tự tính độc lập (Python) ra đúng các giá trị.
- quymo (5:43): 100/1 000/10 000 gd/s → STAN quay lại sau 10 000/1 000/100 s; tin chờ 200/2 000/20 000 (0,2/2/20 GB nếu mỗi tin giữ luồng 1 MB); điều gì gãy + cách xử lý (khoá thêm RRN/thiết bị/thời điểm; bỏ chặn luồng, bảng tin chờ theo mã tương quan); đánh đổi (bộ nhớ khoá, bảng tin chờ). Tính lại ĐÚNG. (Xem SHOULD đầu về câu "khoá sống lâu hơn 17 phút".)

## Lab (labs/INT/L04, giấy-bút .md)
Làm được; ~12 phút (XOR 16 cặp hex bằng tay là phần mất thời gian). Đề đủ: de.md nêu rõ quy tắc bitmap, định dạng khối PIN, cách lấy 12 chữ số thẻ, dòng định dạng; không thiếu kiến thức vì prereq giảng XOR hex bằng 2 cặp ví dụ. Tự tính (Python) trước khi mở loi_giai: 2220000000800000 / 045802BA9876FEDC / 250 / co / 6000 = ĐÚNG mong_doi.txt. Hexa XOR từng cặp (kiểm bằng zip): khớp. mong_doi khớp màn hình: CÓ. cham.sh không chấm .md.

## Người học kẹt ở đâu
chaythat step 1 — mã "bm = sum(1 << (64 - b) for b in bit)" và "pan = int("0000" + "4321987654321098"[-13:-1], 16)": không đọc được cú pháp (nhưng nhờ phần tính tay ở prereq vẫn hiểu kết quả); phần khó hơn là prereq step 3 — XOR 16 cặp hex, chỉ làm mẫu 1 cặp "34 và 19 cho 2D" rồi nhảy tới đáp số.

## Số tính lại / mã chạy / khung hình
- Tính lại: bitmap 3020000008001000; khối PIN 04122D789ABCDEF6 (+ XOR từng cặp bằng zip khớp); 12 chữ số thẻ "198765432109"; 000050000000; STAN 10 000/1 000/100 s (2,78 giờ; 16,67 phút); tin chờ 200/2 000/20 000; 20 GB; lab 5 dòng (bitmap, PIN 045802BA9876FEDC, 250 s, co, 6000) = 12/12 khớp. Python chaythat và quymo chạy KHỚP từng dòng. Java/MQ/HSM: không chạy được (chỉ đọc).
- Khung hình đã xem: 00013 (1:27, bảng khái niệm), 00029 (3:42, sơ đồ hàng đợi), 00042 (5:11, mã Python), 00046 (5:43, mã Python quymo), 00079 (10:16, đề Tự làm), 00089 (15:31, tổng kết).
- Lỗi hiển thị: không có (sơ đồ SVG có mũi tên rõ, chữ đủ lớn; mã Python không tràn). Recap: chuỗi mũi tên dàn thành đoạn văn (nhẹ).

## Bảng sự kiện cần nhất quán
| Sự kiện | Giá trị | bài:cảnh |
|---|---|---|
| Hệ lõi minh hoạ | Temenos T24 (OFS qua IBM MQ); "tin tuyển dụng ACB không nói ACB dùng hệ lõi nào, đừng khẳng định" | L04:hook (show + say) |
| CV người thật | "ứng viên đã tích hợp với T24 ở OCB" (chỉ chữ trên màn hình, chưa kiểm được nguồn) | L04:hook step 1 |
| NAPAS 247 | đặc tả riêng "thường mô tả có gốc ISO 8583" qua TCP; "cần kiểm đặc tả hiện hành" | L04:hook, prereq, symbol |
| MTI | 0200 yêu cầu tài chính; 0210 phản hồi; 0400 yêu cầu đảo; 0420 thông báo đảo (ISO 8583:1987) | L04:prereq step 2, check |
| Mã phản hồi 68 | theo cách gọi phổ biến: nghi vấn/chưa trả lời kịp; ISO gốc: phản hồi quá muộn; xử lý: giữ in-doubt, tra soát, KHÔNG tự hoàn/trừ lại; cần kiểm đặc tả NAPAS | L04:check |
| Trường ISO | 3 processing code (40xxxx chuyển khoản), 4 amount 12 chữ số, 7 thời điểm gốc, 11 STAN 6 chữ số, 37 RRN 12 ký tự, 41 mã thiết bị, 52 PIN block, 64/128 MAC | L04:symbol, pitfall |
| Khối PIN | ISO 9564 định dạng 0; PIN 1234 + thẻ 4321987654321098 → 04122D789ABCDEF6 | L04:prereq step 3 |
| HSM (Thales payShield) | CA TPK→ZPK; CC ZPK→ZPK; JE/JC → LMK; ZMK chỉ bọc khoá | L04:prereq step 3 |
| STAN | 6 chữ số = 1 000 000 giá trị; 100/1 000/10 000 gd/s → 10 000/1 000/100 s; khoá 300 s | L04:quymo, quiz |
| Khoá khử trùng | STAN + RRN + mã thiết bị + trường 7 (giữ nguyên khi gửi lại), kho chung (Redis), lớp cuối UNIQUE | L04:pitfall, quiz |
| Số tiền minh hoạ | chuyển 50 triệu đồng; 000050000000 | L04:symbol, check |
| Lab | trường 3,7,11,41 → 2220000000800000; PIN 5821 + 5412345678901234 → 045802BA9876FEDC; 4 000 gd/s → 250 s, chặn nhầm; 1,5 s → 6 000 | L04:practice |
| Tham chiếu chéo | tín dụng bán lẻ và đối soát cuối ngày ở chuyên đề 8 (INT:L08) | L04:hook, recap |
| Không có số pháp lý/lương | — | — |


## INT L05
sha16 YAML = afdf15ec95deba41 (khớp). 12 cảnh, 29 step; 14,45 phút (866,93 s / 60).

## Phần A — chuẩn xác
| Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng | Đề xuất | Tin cậy |
|---|---|---|---|---|---|
| SHOULD | example step 4 (pháp lý) | "theo Thông tư 50/2024/TT-NHNN (sửa đổi bởi Thông tư 77/2025/TT-NHNN), chuyển tiền trực tuyến trên 10 triệu đồng một lần hoặc tổng trong ngày trên 20 triệu đồng phải xác thực sinh trắc học" | Không sai theo nguồn thứ cấp: TT 50/2024 yêu cầu ngưỡng này cho khách hàng cá nhân; TT 77/2025 (ban hành 31/12/2025, hiệu lực 1/3/2026 theo các báo) sửa TT 50 và đặt lộ trình theo nhóm khách (doanh nghiệp/hộ KD từ 1/7/2026; ngưỡng 10 triệu/lần, 20 triệu/ngày dẫn lại cho hộ KD siêu nhỏ). Tôi KHÔNG đọc được toàn văn (WebSearch chỉ ra tin báo, nguồn không thống nhất ngưỡng/ngày áp dụng giữa các báo). Bài nói như sự thật không kèm đối tượng áp dụng (cá nhân) và ngày hiệu lực; nhưng đã ghi "chưa đọc nguyên văn, cần đối chiếu bản hợp nhất" ở sources và "khi làm thật hãy mở văn bản hiện hành" trên màn hình. | Thêm "đối với khách cá nhân" và ngày áp dụng; đối chiếu toàn văn bản hợp nhất | PLAUSIBLE (chưa kiểm được toàn văn) |
| SHOULD | example step 4 | "Quyết định 2345/QĐ-NHNN cũng hay được nhắc nhưng chưa đọc nguyên văn, chưa rõ còn áp dụng" | Số hiệu 2345/QĐ-NHNN là văn bản có thật (2023) theo hiểu biết của tôi; bài tự gắn nhãn chưa kiểm — đúng quy tắc, không phải lỗi. Ghi lại để đối chiếu với ACB. | — | PLAUSIBLE |
| SHOULD | quymo step 1–2 | "mô hình nhẹ cần một nhân ... 100 nhân" ; "nặng cần khoảng 50 máy 8 nhân" | Công thức số nhân = TPS × thời gian là mức tối thiểu lý thuyết khi dùng nhân 100%; thực tế phải dự phòng (thường vận hành ≤ 60–70% tải) nên số nhân thật lớn hơn. Bài có nói "một nhân xử lý một giao dịch tại một thời điểm", chưa nêu hệ số dự phòng. Phép tính 1/10/100 nhân và 40/400/4 000 nhân, 13 và 500 máy đã tính lại ĐÚNG (100/8=12,5→13). | Thêm "chưa kể dự phòng" | PLAUSIBLE |
| SHOULD | hook / check / recap | "dự kiến tốt nghiệp 11/2026" | Hôm nay là 2026-11-15, tức chính tháng dự kiến; thông tin có thể cũ ngay sau khi tốt nghiệp/hoãn; không có nguồn kiểm được trong bài (chương trình đào tạo UIT, bảng điểm "đối chiếu khi nói"). Nhất quán với L00. Chưa kiểm được nguồn. | Ghi "cập nhật theo thực tế" | PLAUSIBLE |
| SHOULD | prereq step 2 | "kinh nghiệm tích hợp Core T24 và phối hợp luồng NAPAS 247 với đội Switch ở OCB" | Khẳng định CV người thật, không có nguồn trong bài; nhất quán với L04:hook ("tích hợp với T24 ở OCB"). Chưa kiểm được nguồn. | Giữ, ghi "đối chiếu CV thật" | PLAUSIBLE |
Không có MUST. Đã kiểm đúng: 4 400 km/h (1 100/0,25), gần 5 lần 900; Z=(30−2)/1,5=18,67; UCB1 công thức Auer et al. 2002 (c=√2, phần thưởng trong [0,1]); 1,21 và 1,77; cosine 0,992; ln 110 ≈ 4,70; 384 chiều (đúng với mô hình MiniLM thông dụng, bài không nêu tên mô hình); "p99 = 99% yêu cầu nhanh hơn" đúng; hạn chế Isolation Forest (chỉ biết hiếm, không biết gian lận) đúng; thiết kế dual-path hợp lý. Hàm Java ONNX Runtime chỉ đọc, không chạy (không có mô hình/onnxruntime).

## Điểm
P1=0 P2=2 P3=2 P4=2 P5=2 P6=2 P7=2 Tổng(P1–P7)=12 P8=2 P9=2 — Mất gốc: GẦN (12 nhưng có một mục 0).
Cần biết trước: mạng nơ-ron sâu / học sâu / "mô hình đồ thị sâu"; tên học phần (Machine Learning, Deep Learning, Computer Vision, Giải tích…); JSON ("gói tin JSON" ở hook); p95; "tensor" và cú pháp Java ONNX; cú pháp Python (`def`, `for ten, ms in ((…),(…))`, `math.sqrt/log`); "danh sách đen"; ký hiệu LaTeX (có giải).
P1<2 — DANH SÁCH mục chưa giảng:
1. pitfall step 1 + concept step 1: "Nhúng mạng nơ-ron sâu vào luồng đồng bộ"; "mô hình đồ thị sâu phân tích quan hệ ngầm"; "Phân tích Đồ thị AI" — mạng nơ-ron sâu và mô hình đồ thị không được giải ở đâu trong bài.
2. example step 3: mã Java ONNX (`OnnxTensor.createTensor(env, FloatBuffer.wrap(features), shape)`, `session.run(Collections.singletonMap("input", inputTensor))`, `((float[][]) result.get("scores").get().getValue())[0][0]`) và step 2 `float[] features = new float[]{ … }` — lời đọc chỉ tả ý "đưa đặc trưng vào mô hình".
3. chaythat step 1 + quymo step 1: mã Python (`def ucb(mu, nk, n): return …`, `math.sqrt`, `math.log`, vòng for lồng nhau với bộ).
4. prereq step 1: tên học phần "Machine Learning, Deep Learning, Computer Vision" và "Phân tích thuật toán, Cấu trúc dữ liệu nâng cao" chỉ nêu tên (lời đọc: "đối chiếu với bảng điểm") — chấp nhận vì là danh sách tên môn, không dùng để tính.
5. hook step 1: "JSON" dùng khi chưa giải (JSON được giải ở L02:symbol step 3 — trong cùng khoá, chấp nhận).

## Cảnh Tự làm / quy mô
- practice (10:10, "Tự làm: trả lời một câu phỏng vấn có số về số nhân xử lý, điểm Z, UCB1 và cosine"): giấy bút; 12 000 gd/s, 3 ms/40 ms; Z với 45/5/4 triệu; UCB1 hai kênh 180/200 và 9/10, N=210; cosine (2,1) và (1,3); pause 180 s; step sau: `so nhan mo hinh nhe 3 ms: 36 / … nang 40 ms: 480 / diem Z: 10 / diem A: 1.13 / diem B: 1.93 / chon kenh: B / cosine: 0.707`. CÓ kết quả trên màn hình; KHỚP mong_doi.txt (tự tính độc lập bằng Python ra y hệt). Cần máy tính cho √ và ln (de.md cho phép).
- quymo (7:09): 500/5 000/50 000 gd/s × 2 ms và 80 ms → 1/10/100 nhân và 40/400/4 000 nhân; 50 máy/500 máy (8 nhân) vs 13 máy; điều gì gãy + đánh đổi (mô hình nặng sang bất đồng bộ thì chậm vài giây). Tính lại ĐÚNG. (Lab dùng 3/40 ms, 12 000 gd/s — số khác ví dụ, đúng tinh thần.)

## Lab (labs/INT/L05, giấy-bút .md)
Làm được, ~8 phút (cần √ và ln). Đề đủ: de.md cho sẵn công thức điểm UCB1 và định dạng 7 dòng; thiếu kiến thức: không. Tự tính trước khi mở loi_giai: 36 / 480 / 10 / 1.13 / 1.93 / B / 0.707 = ĐÚNG mong_doi.txt. mong_doi khớp màn hình: CÓ. cham.sh không chấm .md.

## Người học kẹt ở đâu
pitfall step 1 / concept step 1 — "Nhúng mạng nơ-ron sâu vào luồng đồng bộ", "mô hình đồ thị sâu" (không giải); và example step 3 — mã Java "OnnxTensor.createTensor(env, FloatBuffer.wrap(features), shape)" (không giải); các phép tính Z/UCB1/cosine thì theo được nhờ giải bằng lời + ví dụ số.

## Số tính lại / mã chạy / khung hình
- Tính lại: 4 400; 4,9 lần máy bay; 18,67; 1,21; 1,77; 0,992; 1/10/100 và 40/400/4 000 nhân; 12,5→13; 50; 500; lab 7 dòng (36, 480, 10, 1,13, 1,93, B, 0,707) = 20/20 khớp. Python chaythat (3 dòng) và quymo (6 dòng) chạy KHỚP. Java ONNX: chỉ đọc, không chạy.
- Khung hình đã xem: 00004 (0:30, bảng hook), 00015 (1:38, sơ đồ dual-path), 00028 (3:19, công thức UCB1/cosine), 00056 (6:43, bước 3 pháp lý), 00086 (10:10, đề Tự làm), 00096 (14:18, tổng kết).
- Lỗi hiển thị: không có lỗi đáng kể; công thức LaTeX hiển thị đúng; sơ đồ dual-path có mũi tên rõ. Hình cho Isolation Forest/UCB1 là bảng chữ, không có hình cây hay đồ thị (P3 vẫn 2 vì sơ đồ cơ chế chính, dual-path, đạt).

## Bảng sự kiện cần nhất quán
| Sự kiện | Giá trị | bài:cảnh |
|---|---|---|
| Thông tư 50/2024/TT-NHNN | sửa đổi bởi Thông tư 77/2025/TT-NHNN; "nguồn thứ cấp theo bài phỏng vấn đã lưu, chưa đọc nguyên văn" | L05:YAML source; example step 4 |
| Ngưỡng sinh trắc học | chuyển tiền trực tuyến TRÊN 10 triệu đồng/lần hoặc TỔNG TRÊN 20 triệu đồng/ngày phải xác thực sinh trắc học (khác ngưỡng điểm rủi ro mô hình) | L05:example step 4 |
| Quyết định 2345/QĐ-NHNN | chưa đọc nguyên văn, chưa rõ còn áp dụng, không nêu số điều | L05:example step 4 |
| UIT Cử nhân AI | dự kiến tốt nghiệp 11/2026; dự án AI = nguyên mẫu học thuật, không phải hệ thống đã vận hành; tên học phần "đối chiếu bảng điểm" | L05:check, quiz step 4, recap; L00:pitfall |
| CV | tích hợp Core T24, phối hợp NAPAS 247 với đội Switch ở OCB (check: "đã làm về tích hợp hệ thống ngân hàng tại OCB") | L05:prereq step 2, check; L04:hook |
| Địa lý | HCM–Singapore ≈ 1 100 km, 15 phút → 4 400 km/h vs máy bay 900 km/h | L05:example step 1 |
| Z-score | (30−2)/1,5 = 18,67; lab (45−5)/4 = 10 | L05:example, practice |
| UCB1 | Auer–Cesa-Bianchi–Fischer 2002; c=√2; N=110: A 1,21, B 1,77; lab N=210: A 1,13, B 1,93 → chọn B | L05:symbol, practice |
| Cosine | (1,2)·(2,3)=8 → 0,992; lab (2,1),(1,3) → 0,707; 384 chiều; ngưỡng 0,88 minh hoạ | L05:symbol, practice |
| Số nhân | nhẹ 2 ms, nặng 80 ms; 500/5 000/50 000 gd/s; lab 12 000 gd/s: 36 và 480 | L05:quymo, practice |
| Isolation Forest | 45 triệu tách sau ~2 lần chia vs ~6 (minh hoạ); ONNX Runtime trong RAM, mục tiêu vài ms (phải đo, JMH, p95/p99) | L05:concept |


## INT L06
sha16 YAML = 18a7bd8058c7daf2 (khớp). 11 cảnh / 25 step; 13,26 phút (795,4 s).

## Phần A
| Mức | Cảnh/step | Trích | Vì sao / bằng chứng | Đề xuất | Tin cậy |
|---|---|---|---|---|---|
| SHOULD | prereq s1 (hàng "Tầng 4"), pitfall s1 | "Nêu bối cảnh, hành động và kết quả tại OCB"; "Luôn gắn với dự án thực tế đã làm tại OCB" | Bài dành cho phỏng vấn ACB nhưng hai bảng bảo người học nói về "dự án đã làm tại OCB"; OCB không được giải thích (ngân hàng nào, vì sao). Người học khác (không từng làm ở OCB) đọc như bắt buộc có kinh nghiệm OCB; sai chủ thể. | Đổi thành "tại nơi bạn từng làm" | CONFIRMED |
| SHOULD | example s3 | "khoá từng dòng tài khoản bằng câu lệnh riêng theo thứ tự mã tăng dần (không dựa vào ORDER BY ... FOR UPDATE)" | Khẳng định hành vi của Oracle (ORDER BY ... FOR UPDATE không bảo đảm thứ tự khoá) không có nguồn trong bài; không giải thích vì sao. Tôi không kiểm được từ tài liệu Oracle: chưa kiểm được nguồn. | Thêm nguồn hoặc bỏ ngoặc | PLAUSIBLE |
| SHOULD | check s1 | "theo Thông tư 50/2024/TT-NHNN (sửa đổi bởi Thông tư 77/2025/TT-NHNN), phải xác thực khuôn mặt khi một lần chuyển trên 10 triệu đồng hoặc khi tổng chuyển trong ngày vượt 20 triệu đồng" | WebSearch: TT 77/2025/TT-NHNN có thật, ban hành 31/12/2025, hiệu lực 1/3/2026 (một số điều lộ trình tháng 7 và 10/2026). Báo chí nêu ngưỡng 10 triệu/lần, 20 triệu/ngày cho nhóm doanh nghiệp/hộ KD; ngưỡng áp cho cá nhân đúng theo kiến thức của tôi (TT 50 điều về xác thực sinh trắc học, hiệu lực 1/7/2025) nhưng chưa đọc văn bản gốc; báo chí dùng lẫn "trên" và "từ...trở lên". Bài đã ghi rõ "nguồn thứ cấp, chưa đọc nguyên văn" trong YAML source nhưng MÀN HÌNH/lời đọc không nói chưa kiểm, không nêu ngày hiệu lực. Quiz coi như chắc chắn. | Thêm "(đối chiếu văn bản hiện hành, hiệu lực/lộ trình theo văn bản)" trên màn hình | PLAUSIBLE |
| SHOULD | quymo s1 | "do = tps * 0.120 ... yeu cau do cung luc" / lời đọc "120 yêu cầu dở" | Phép tính đúng (Little: L = lambda x W) nhưng "yêu cầu dở" và lý do nhân TPS với độ trễ không được giảng bằng lời thường ở đâu trong video (xem P1). | Thêm 1 câu giải thích | CONFIRMED |

Không phát hiện MUST. Số: 10000x0.12=1200; ceil(1200/500)=3; ceil(12000/500)=24; 0.9999^4=0.99960006 -> 99.96%, 210.2 phút (=4,0x của 52,56: "gấp bốn lần" đúng); 525600x0,0001=52,56; SRE "bốn tín hiệu vàng" = độ trễ, lưu lượng, lỗi, độ bão hoà (đúng). ORA-00060, .trc, 504 đúng.

## Điểm
P1=0 P2=1 P3=2 P4=2 P5=1 P6=1 P7=2 Tổng(P1–P7)=9 P8=2 P9=2. Mất gốc: GẦN (9, có mục 0 ở P1).
Cần biết trước: Little (yêu cầu dở = TPS x độ trễ), TLS, IBM MQ, TCP Socket, NAPAS, Spring, Oracle/UPDATE (SQL), B-Tree, Kafka (được nhắc là hàng đợi sự kiện), OCB.
Chỗ thiếu chính: dồn nhiều từ khoá (mTLS/CDC/IBM MQ/TCP Socket) vào một sơ đồ; 100 câu hỏi không được trình bày (chỉ 5 tình huống); quiz đáp án B rõ ràng dài nhất, kiểm nhớ chứ không kiểm hiểu.
P1 < 2, danh sách mục chưa giảng (trong video, theo chuẩn chặt):
1. "TLS" trong "mTLS = TLS hai chiều" (concept s1) — TLS không giải thích.
2. "IBM MQ" (concept s1, svg tầng 4) — không giải thích.
3. "TCP Socket" (concept s1, svg tầng 4) — không giải thích.
4. "NAPAS" (hook s2 bảng, concept svg) — không giải thích trong video này.
5. "Spring" ("Quản lý giao dịch Spring", hook s2) — không giải thích.
6. "ORDER BY ... FOR UPDATE" (example s3) — cú pháp không giảng.
7. "OCB" (prereq s1, pitfall) — không giải thích.
8. "yêu cầu dở" + công thức TPS x độ trễ (quymo s1; practice "Nếu kẹt") — không có câu giải thích bằng lời thường (chỉ nhân số).
(Một phần các mục này nằm ở khoá/bài trước theo `assumes`, nhưng chuẩn chặt: phải giảng trong chính video hoặc cảnh prereq.)

## Cảnh Tự làm
id practice: đề giấy bút 6 dòng số mới (2000 TPS, 200 ms, 150 y/c, 99,95%, 3 tầng, 12 triệu, 8+7 triệu), pause 180 s. Có đáp án để đối chiếu trên màn hình (step 2): CÓ. Khớp labs/INT/L06/mong_doi.txt: KHỚP 6/6 dòng (400; 4; 262.8; 99.85%/788.0; can; chua can). Cảnh quy mô id quymo: ×1/×10/×100: 120/1200/12000 yêu cầu dở; 1+1/3+1/24+1 máy; chuỗi 4 tầng 99,99% -> 99,96% & 210,2 phút/năm; đánh đổi nêu. Tính lại: ĐÚNG hết.

## Lab (giấy bút, de.md đọc rồi tự tính bằng Python trước khi đọc loi_giai.md)
Tự làm được: CÓ (~5 phút). Kẹt: không đáng kể; công thức "yêu cầu dở = giao dịch/giây x số giây ở lại" cho sẵn trong de.md ("số giây ở lại" mơ hồ nhưng ghi "độ trễ"). Kết quả của tôi: 400; 4 (ceil 2,667=3 +1); 262,8; 0,9995^3=0,998500749875 -> 99,85%, 787,98 -> 788,0; can; chua can. Khớp mong_doi.txt và loi_giai.md. cham.sh không chấm .md (không chạy). Lưu ý: ngưỡng "mỗi lần ≤ 10 triệu, tổng ≤ 20 triệu" -> ranh giới đúng "trên".

## Người học kẹt ở đâu
concept s1: sơ đồ 4 tầng "mTLS ... CDC ... IBM MQ ... TCP Socket" — nhiều từ khoá, chỉ vài từ được giải thích; kế đó quymo s1 "120 yêu cầu dở" không giảng "dở".

## Đã tính lại / chạy
Tính lại 22 số (TPS tầng, máy, chuỗi, 52,56, 262,8, 788,0, ...): 22/22 khớp. Mã chạy: Python quymo s1 (3 dòng) và s2 chạy lại bằng công thức: khớp. SQL deadlock đọc, không chạy (Oracle).
Khung hình: 00022 (≈150 s concept SVG), 00030 (≈200 s SLA), 00060 (≈420 s quymo chuỗi), 00075 (≈520 s quiz bước 2), 00081 (practice ≈600 s). Không lỗi hiển thị; chữ SVG nhỏ (12px trong viewBox) nhưng đọc được.

## Bảng sự kiện cần nhất quán
| Sự kiện | Giá trị | bài:cảnh |
|---|---|---|
| Ngưỡng sinh trắc học | một lần > 10 triệu; tổng trong ngày > 20 triệu | INT L06:check s1,s2; practice; lab de.md |
| Văn bản | Thông tư 50/2024/TT-NHNN, sửa đổi TT 77/2025/TT-NHNN; QĐ 2345/QĐ-NHNN "chưa đọc nguyên văn, chưa rõ còn áp dụng" | INT L06:check s1 |
| SLA đề giả định | 10 000 TPS; 120 ms; 99,99% = 52,56 phút/năm; lỗi < 0,001% | INT L06:symbol |
| Sức chứa/máy | 500 yêu cầu (minh hoạ); practice 150 | quymo; practice |
| Timeout phân tầng | nội bộ < 3 s; đối tác ngoài < 8 s + gọi lại bất đồng bộ (minh hoạ) | INT L06:concept s2 |
| Nội dung "bốn tín hiệu vàng" SRE | độ trễ, lưu lượng, lỗi, độ bão hoà (Google 2016) | INT L06:symbol |
| Ngân hàng | ACB là nơi phỏng vấn; OCB là nơi ứng viên từng làm | INT L06:prereq, pitfall |
| Kế hoạch 90 ngày | 30/60/90 | INT L06:quiz |


## INT L07
sha16 YAML = eed205398e71dfb3 (khớp). 11 cảnh / 26 step; 13,22 phút (793,0 s).

## Phần A
| Mức | Cảnh/step | Trích | Vì sao / bằng chứng | Đề xuất | Tin cậy |
|---|---|---|---|---|---|
| SHOULD | example s2 | "Dạ em đi làm phần mềm từ 01/2019: Sutrix (2019–2021), freelance (2022), Grooo làm dự án cho Mirae Asset Finance (2022–2023) và OCB (10/2023 – nay)" | Tên công ty/ngày tháng thật của một cá nhân cụ thể, không có nguồn trong bài và không gắn nhãn "câu mẫu, thay bằng của bạn" (khác L06 có ghi). Học viên khác đọc như lời đáp để nói. freelance 2022 và Grooo 2022–2023 chồng năm. Chưa kiểm được nguồn. | Gắn nhãn minh hoạ, thay bằng "[kinh nghiệm thật của bạn]" | PLAUSIBLE |
| SHOULD | prereq s1, symbol s2 | "Tháng 13 cố định ... thưởng 1–4 tháng lương tuỳ xếp loại (tin ACB ghi ...)" | Nguồn là tin tuyển dụng ACB "đọc 2026-11" (YAML source); trong video có ghi "tin ACB ghi", nhưng không có ngày đọc hoặc cảnh báo tin có thể đổi. Chưa kiểm được nguồn. Nội dung nhạy thời gian. | Thêm "đọc 11/2026, kiểm lại tin hiện hành" | PLAUSIBLE |
| SHOULD | concept s3 | "luật lao động giới hạn thời gian thử việc: cần kiểm lại văn bản hiện hành" | Đã gắn nhãn cần kiểm; không nêu số điều/thời hạn (tối đa 180 ngày theo Bộ luật Lao động 2019 cho quản lý doanh nghiệp, 60 ngày trình độ cao đẳng trở lên là kiến thức của tôi, chưa kiểm). Không sai. | không bắt buộc | PLAUSIBLE |
| SHOULD | example s2 | "Bằng Cử nhân AI tại UIT ... dự kiến tốt nghiệp 11/2026" | Mốc 11/2026 trùng tháng hiện tại (2026-11); video sẽ lỗi thời nếu không cập nhật; nhất quán với INT L00/L01 (dự kiến 11/2026). | Cập nhật khi đã tốt nghiệp | PLAUSIBLE |

Không phát hiện MUST. Tính lại: 36x14..17 = 504/540/576/612; 40x14..17 = 560/600/640/680; chênh 56/60/64/68; 36x(13+k)=600 -> k=3,667; k=5 -> 648; quymo 60 / 194,78 -> 194,8 / 351,996 -> 352,0; quiz 384, 416, 448–544, +24 -> 472–568; practice 570/534/36/5. Tất cả đúng. Công thức T = L(13+k)+12P nhất quán xuyên bài. "Lương gross" định nghĩa đúng.

## Điểm
P1=1 P2=2 P3=2 P4=2 P5=2 P6=2 P7=2 Tổng(P1–P7)=13 P8=2 P9=2. Mất gốc: ĐỦ.
Cần biết trước: cú pháp Python (for/range, +=, *=, if ... in (...), round); BHXH được viết tắt nhưng chỉ nêu tên (không giải thích ngoài "bảo hiểm xã hội"); "Offer".
P1 < 2, danh sách mục chưa giảng:
1. Python `for nam in range(1, 6):` + `if nam in (1, 3, 5):` (quymo s1) — không giảng, nhưng lời đọc giải thích ý nghĩa vòng 5 năm.
2. Toán tử `tong += chenh * tang`, `tang *= 1.08` (quymo s1) — chỉ chú thích "moi nam tang 8%" cho tang; `+=` không giảng.
(Nếu đếm riêng từng cú pháp: for/range, +=, *=, in-tuple, round => >=3, P1 có thể 0; tôi đếm gộp 2 nhóm => 1.)
Chỗ thiếu chính: mã Python quymo không dẫn từng dòng; không có biểu đồ đường cho đà phình chênh lệch (chỉ bảng 3 mốc).

## Cảnh Tự làm
id practice: so Offer A (38, không phụ cấp) và B (34 + phụ cấp 2) bằng T, k=2; pause 180 s. Có đáp án trên màn hình step 2 (570/534/36/5): CÓ; khớp mong_doi.txt 4/4. Cảnh quy mô id quymo: mức 1/3/5 năm: 60 / 194,8 / 352,0 triệu; đánh đổi nêu ("đòi quá cao có thể mất lời mời"). Tính lại ĐÚNG (giả định tăng 8%/năm trên lương hiện tại là minh hoạ, ghi rõ).

## Lab
Giấy bút; tự tính bằng Python trước khi mở loi_giai.md: 570; 534; 36; 5 -> khớp mong_doi.txt và loi_giai.md. Tự làm được: CÓ (~3 phút). Đề đủ (công thức cho sẵn, giả định phụ cấp không tính thưởng). Kẹt: không. cham.sh không chấm .md.

## Người học kẹt ở đâu
quymo s1: khối Python (`for nam in range(1, 6)`, `tong += ...`) — người chưa lập trình không đọc được mã, nhưng vẫn theo được ý qua lời đọc và bảng bước 2.

## Đã tính lại / chạy
~34 số: 34/34 khớp. Python quymo chạy lại bằng công thức tương đương: khớp. Khung hình: 00025 (≈160 s, câu hỏi cho HR), 00041 (≈260 s, bảng đòn 3), 00050 (≈330 s, quymo code), 00059 (≈400 s, quiz tình huống), 00077 (≈600 s, practice). Không lỗi hiển thị.

## Bảng sự kiện cần nhất quán
| Sự kiện | Giá trị | bài:cảnh |
|---|---|---|
| Tháng 13 + thưởng ACB | tháng 13 cố định; thưởng 1–4 tháng lương theo xếp loại (tin ACB, đọc 2026-11) | INT L07:prereq s1; symbol s2; quiz |
| Lương ACB | "Thương lượng" (không nêu số) | INT L07:hook; example s4 |
| Một tin khác (không xác nhận) | tăng lương 2 lần/năm | YAML source (không trên màn hình) |
| Công thức | T = L x (13+k) + 12 x P (số minh hoạ L=34,k=2,P=2 -> 534) | symbol s1 |
| Kinh nghiệm cá nhân | đi làm từ 01/2019: Sutrix 2019–2021, freelance 2022, Grooo (dự án Mirae Asset Finance) 2022–2023, OCB 10/2023–nay | INT L07:example s2 |
| Bằng cấp | Cử nhân AI UIT dự kiến 11/2026 | INT L07:example s2; recap s2 |
| Tăng lương minh hoạ | 8%/năm | quymo |
| Số minh hoạ khác | 36 vs 40 triệu; 32 triệu + 2 PC; 38 vs 34+2 | example; quiz; practice |


## INT L08
sha16 YAML = ad4c7eae500e0d55 (khớp). 11 cảnh / 33 step; 16,67 phút (1000,3 s).

## Phần A
| Mức | Cảnh/step | Trích | Vì sao / bằng chứng | Đề xuất | Tin cậy |
|---|---|---|---|---|---|
| SHOULD | quiz s2 (bảng bước 1), s1 đáp án B | "Pha 1: Phong tỏa ... Giữa hai pha: Ký hợp đồng ... Pha 2: Cấp vốn"; "Phong tỏa số dư sổ tiết kiệm ... trước, sau khi thành công mới cấp hạn mức" | Bảng đặt phong tỏa trước khi ký hợp đồng, nhưng cột lý do nói ký hợp đồng để "có căn cứ pháp lý trước khi cấp vốn". Thực tế cầm cố sổ tiết kiệm thường có hợp đồng cầm cố/thoả thuận phong toả trước hoặc cùng lúc phong toả; phong toả khi chưa ký là điểm tranh luận. Đáp án D ("Chờ khách ký giấy tờ ... mới thực hiện thao tác") không hẳn sai thứ tự. Không kiểm được quy trình ngân hàng cụ thể: chưa kiểm được nguồn. | Ghi rõ "thứ tự minh hoạ, quy trình thật theo hợp đồng cầm cố của ngân hàng" hoặc đổi phương án D | PLAUSIBLE |
| SHOULD | example s4 (mã giả) | "if (core[i].rrn == napas[j].rrn) matchOrFlagAmount(core[i++], napas[j++]);" | Thuật toán hai con trỏ giả định mã đối soát (RRN) duy nhất trong mỗi danh sách; RRN trùng hoặc thứ tự khác (chuỗi so với số) làm sai kết quả. Bài không nêu điều kiện này. | Thêm "giả định mã duy nhất và cùng kiểu sắp xếp" | PLAUSIBLE |
| SHOULD | pitfall s2 vs objectives/recap | "Cách chữa gồm ba lớp ..." (lời đọc/bảng 3 hàng) so với mục tiêu "hai lớp chặn cần có" và recap "chống giải ngân trùng bằng hai lớp chặn" | Mâu thuẫn số lớp (ba hay hai); bảng liệt kê 3 (khoá sớm, ràng buộc duy nhất, đối soát), nhưng đối soát là lớp phát hiện. | Thống nhất "hai lớp chặn + một lớp phát hiện" | CONFIRMED |
| SHOULD | quymo s1 | "sắp xếp cộng hai con trỏ cho cả ba danh sách chỉ khoảng 0 phẩy 21 giây" (giả định 10^9 phép so sánh/giây) | Số là minh hoạ (có ghi), nhưng thực tế sắp xếp 3 triệu bản ghi bằng Python mất cỡ giây, không phải 0,21 s; bài có ghi "thời gian đọc ghi tệp thường vượt thời gian so sánh nên phải đo thật". Chấp nhận được. | không bắt buộc | PLAUSIBLE |
| SHOULD | prereq s2 | "quá hạn 10–90 ngày là nhóm 2 ... nhóm 3–5 là nợ xấu ... TT 31/2024/TT-NHNN ... TT 37/2025/TT-NHNN" | WebSearch: TT 31/2024/TT-NHNN có thật (phân loại tài sản có, hiệu lực 1/7/2024); TT 37/2025/TT-NHNN ký 31/10/2025 sửa đổi (hiệu lực khoảng 15/12/2025), có bản hợp nhất 27/2025/VBHN-NHNN. Ngưỡng "10 ngày" của nhóm 2 tôi chưa xác minh được từ kết quả tìm kiếm (nguồn chỉ nói "đến 90 ngày"); bài đã ghi "nguồn thứ cấp, định nghĩa rút gọn, cần đối chiếu bản hợp nhất" trên màn hình. Nhóm 3 = 91–180 ngày đúng theo kiến thức (YAML source). | chưa kiểm được nguồn mốc 10 ngày | PLAUSIBLE |

Không phát hiện MUST. Tính lại: 100x0,85=85; 12/30=40%; 150x0,8=120; (6+4,5)/25=42%; 4,5-2,7=1,8; 3e6^2=9e12 -> 9000 s=2,5 h; ceil(log2 3e6)=22, 3e6: 0,21 s; 3e7: ceil(24,84)=25 -> 2,37 s, 250 h; 3e8: ceil(28,16)=29 -> 27,3 s, 25000 h; 0,3/3,0/30,0 GB; bảng 9 GB ở x10; vết hai con trỏ 5 bước đúng; Redis giây 0/300/350/400 nhất quán; 2x120=240. Tất cả đúng.

## Điểm
P1=0 P2=2 P3=2 P4=2 P5=2 P6=2 P7=1 Tổng(P1–P7)=11 P8=2 P9=2. Mất gốc: GẦN (11).
Cần biết trước: "tài sản bảo đảm"/"cầm cố"/"tín chấp" (thuật ngữ cho vay), cú pháp Python (for, import, math.ceil/log2, 1e9, round), cú pháp mã giả (&&, .size(), core[i].rrn, lệnh gọi hàm), "RRN", "ràng buộc duy nhất".
P1 < 2, danh sách mục chưa giảng (theo chuẩn chặt):
1. "tài sản bảo đảm" / "cầm cố" (prereq s1 LTV; quiz: "Thấu chi Cầm cố"; hook) — dùng nhiều lần, không có câu giải nghĩa bằng lời thường.
2. "tín chấp" ("Thấu chi Lương tín chấp", concept s1 svg) — không giải thích.
3. Mã giả `while (i < core.size() && j < napas.size())`, `core[i].rrn` (example s4): `&&`, `.size()`, `.rrn` không giảng (chỉ giảng while và i++).
4. Python `for n in (...)`, `math.ceil(math.log2(n))`, `1e9`, `round` (quymo s1) — chỉ giảng bằng lời đọc số, không giảng cú pháp.
(Mục 3 và 4 có thể coi cùng nhóm "cú pháp lập trình"; nếu gộp, còn 3 nhóm => vẫn >=3, nhưng mục 1–2 là ranh giới "suy được từ ngữ cảnh". Người điều phối cân nhắc: P1 có thể là 1.)
Chỗ thiếu chính: sáu mảng tín dụng (concept s1) chỉ nêu tên trên sơ đồ, không giảng từng mảng (đặc biệt vay trên hạn mức thẻ, thấu chi lương); video 16,7 phút dài.

## Cảnh Tự làm
id practice: 4 ý (240 triệu LTV 70%; 9/36 DTI; 12 vs 7,5; đối soát 3 x 2 triệu), pause 240 s. Đáp án trên màn hình (step 2): CÓ; khớp mong_doi.txt 5/5 (168; 25%; 7.5/4.5; 1.1 giờ; 0.13 giây). Công thức sắp xếp cho sẵn trên đề. Cảnh quy mô id quymo: x1/x10/x100 (3/30/300 triệu): lồng nhau 2,5 / 250 / 25000 giờ; sắp xếp 0,21 / 2,37 / 27,3 giây; 0,3/3/30 GB mỗi danh sách; điều gì gãy (bộ nhớ ở x100, sắp xếp ngoài bộ nhớ hay chia theo dải) và đánh đổi nêu. Tính lại ĐÚNG hết.

## Lab (giấy bút; tự tính bằng Python trước)
168; 0,25 -> 25%; 7,5 và 4,5; 4e12/1e9/3600=1,111 -> 1,1; 3x2e6x21 + 2x4e6 = 134e6 -> 0,134 -> 0,13. Khớp mong_doi.txt và loi_giai.md. Tự làm được: CÓ (~6 phút). Đề đủ: cho sẵn công thức sắp xếp và ⌈log2 N⌉ (mẹo kiểm 2^20, 2^21 có trong "Nếu kẹt"). Thiếu: người mất gốc cần biết log2 và làm tròn lên (giả định khoá "log" trước đã dạy). cham.sh không chấm .md.

## Người học kẹt ở đâu
concept s1 / quiz: "thấu chi cầm cố ... tài sản bảo đảm" (không giải nghĩa) và example s4 mã giả `core.size() && ...`.

## Đã tính lại / chạy
~45 số: 45/45 khớp. Mã Python quymo chạy lại: ra đúng 3 dòng như màn hình. Khung hình: 00014 (≈100 s, prereq s2), 00019 (≈130 s, sáu mảng SVG), 00048 (≈420 s, hai con trỏ khái niệm), 00059 (≈500 s, quymo code), 00068 (≈560 s, bẫy Redis), 00079 (≈640 s, quiz), 00089 (≈760 s, practice). Không lỗi hiển thị.

## Bảng sự kiện cần nhất quán
| Sự kiện | Giá trị | bài:cảnh |
|---|---|---|
| Phân loại nợ | TT 31/2024/TT-NHNN (hiệu lực 1/7/2024), sửa đổi bởi TT 37/2025/TT-NHNN (ký 31/10/2025); nhóm 2 quá hạn 10–90 ngày; nhóm 3 = 91–180; nhóm 3–5 nợ xấu; 5 nhóm | INT L08:prereq s2; YAML source |
| CIC | Trung tâm Thông tin Tín dụng Quốc gia (thuộc NHNN), B2B | INT L08:prereq s2 |
| LTV / DTI minh hoạ | LTV 85% (100 triệu -> 85); LTV 80%; DTI chặn khi > 50% (chính sách ví dụ) | prereq; check; quiz |
| Khoá Redis | 300 giây (minh hoạ); khoá >= 2x thời gian chờ tối đa (120 s -> 240 s) | prereq s2; pitfall |
| Squad Lending | tên nhóm trong tin tuyển dụng đã lưu, chưa kiểm | INT L08:hook s1 |
| Core banking | T24 của Temenos; AZ = tiền gửi kỳ hạn; CASA = thanh toán | hook; prereq s1 |
| Thứ tự hai pha | phong tỏa -> ký -> cấp vốn | quiz s2 |
| Quy mô đối soát | 3 triệu GD/ngày giữa lõi, NAPAS, đối tác; mục tiêu 5 phút; 10^9 phép/s; 100 byte/bản ghi | example s1; quymo |


## ACB L00
sha16 YAML = a581eda427709609 (khớp). 13 cảnh / 33 step; 14,94 phút (896,5 s).

## Phần A
| Mức | Cảnh/step | Trích | Vì sao / bằng chứng | Đề xuất | Tin cậy |
|---|---|---|---|---|---|
| SHOULD | example s2; code; practice s2 | "Toàn trình 120 + 35 = 155 ms | đạt mục tiêu P99 200 ms"; mã "if tong < 200: print("dat P99")"; "toan trinh: 130 ms, dat P99" | P99 là phân vị thứ 99 của phân bố độ trễ; không cộng được các thành phần: tổng 120 + 35 là độ trễ điển hình/ước lượng một lần, chứ không phải P99; "đạt P99" cần P99 đo của từng đoạn (P99 không cộng tuyến tính). Bài định nghĩa P99 đúng ở prereq nhưng rồi dùng sai ở ví dụ và lab. Người học mang câu "tổng độ trễ < 200 nên đạt P99" vào phỏng vấn. | Đổi "đạt P99" thành "tổng thời gian ước lượng thấp hơn ngưỡng 200 ms"; thêm câu P99 không cộng | CONFIRMED |
| SHOULD | quiz s3 (đáp án câu 2) YAML vs INT L08 hook | "3 năm tại OCB là Chuyên viên chính trong Squad Lending, trực tiếp làm các luồng tích hợp tín dụng" (show); INT L08: "Squad Lending là tên một nhóm cho vay số trong một tin tuyển dụng đã lưu, chưa kiểm lại" | Mâu thuẫn giữa hai khoá: ACB L00 nêu Squad Lending là nhóm của ứng viên tại OCB (chữ trên màn hình), còn INT L08 nói tên đó chỉ lấy từ một tin tuyển dụng và "chưa kiểm". Lời đọc chỉ nói "nhóm tín dụng tại OCB". Chức danh "Chuyên viên chính" và chi tiết kinh nghiệm không có nguồn trong bài (chưa kiểm được nguồn). | Thống nhất một cách nói; ghi rõ là hồ sơ minh hoạ | CONFIRMED |
| SHOULD | quiz s2 (đáp án câu 1) | "Không hoàn tiền ngay ... Chỉ khi biết chắc giao dịch đã thất bại mới gửi yêu cầu đảo (MTI 0400; 0420 là thông báo đảo ...)" | Trong ISO 8583 (mạng thẻ), 0400 thường được gửi chính vì kết quả chưa biết (đảo do hết giờ), phía nhận so khớp giao dịch gốc và bỏ qua nếu chưa có. Bài nói ngược chiều ("chỉ khi biết chắc thất bại") và có cảnh báo "đặc tả NAPAS cần kiểm". Không kiểm được đặc tả NAPAS: chưa kiểm được nguồn; xem so ACB L02 (tôi sẽ ghi nếu mâu thuẫn). | Ghi "tuỳ đặc tả của mạng; thẻ thường đảo ngay khi hết giờ" | PLAUSIBLE |
| SHOULD | vaitro s1 | "Nhóm thứ nhất ... Spring Boot, Kafka, Redis" / "hỗ trợ sự cố mức 3 theo SLA" | Dựa trên tin tuyển dụng "bản đã lưu, chưa kiểm lại" (đã ghi trên màn hình và lời đọc); chấp nhận. | — | PLAUSIBLE |

Không phát hiện MUST. Số tính lại: 10000x60=600000; x60=36000000; 120+35=155; 60 s=60000 ms; quymo: 100/360 000/15,5/6000; 10 000/36 triệu/1550/600 000; 1 triệu/3,6 tỷ/155 000/60 triệu; 1 000 000 ghi khoá/giây là giả định; practice 240 000 / 14 400 000 / 130 / 90 s = 90 000 ms / 3 000 000. Quiz 40x13=520; 40x14..17 = 560..680 (khớp INT L07 công thức T=L(13+k)+12P với P=0). Tất cả đúng. MTI 0200/0210/0400/0420 đúng chuẩn ISO 8583:1987. Spring self-invocation bỏ qua proxy: đúng. FK không chỉ mục khoá bảng con (Oracle): khớp mô tả thường gặp.

## Điểm
P1=0 P2=2 P3=2 P4=2 P5=2 P6=2 P7=2 Tổng(P1–P7)=12 P8=2 P9=2. Mất gốc: GẦN (tổng 12 nhưng có mục 0 ở P1).
Cần biết trước: "247" (NAPAS 247 = chuyển nhanh 24/7), mã bản tin "0200/0210", "TTL" (dùng trong đáp án lab), OCB và "Squad Lending", "OFS" (có tên đầy đủ, nhưng "Open Financial Service" không giải thích bằng lời thường ngoài "chuỗi văn bản").
P1 < 2, danh sách mục chưa giảng:
1. "0200/0210" (concept s1 SVG "Bản tin ISO 8583 0200/0210"; quiz s1 "bản tin 0200") — chỉ giảng "mã loại bản tin 4 chữ số" ở đáp án, sau khi đã dùng; không nói 0200 là yêu cầu, 0210 là phản hồi.
2. "247" trong "NAPAS 247" (tiêu đề concept, hook, mục tiêu) — không giải thích (24/7).
3. "TTL" (practice s2: "ttl: 90 giay = 90000 ms") — chỉ xuất hiện ở đáp án; đề dùng "thời gian sống".
4. "OCB" / "Squad Lending" (concept SVG tiêu đề, quiz s3) — không giải thích OCB là gì, Squad Lending không giải thích.
(Mục 1–3 rõ ràng; mục 4 là tên riêng.)
Chỗ thiếu chính: tối ưu đoạn hơn 15 phút, bài nhồi nhiều chủ đề (kiến trúc, tải, SAGA, vai trò JD, lương); quiz hai câu chỉ có đáp án đọc, không có chấm điểm; P99 bị dùng sai (xem Phần A).

## Cảnh Tự làm
id practice: viết mau.py in 5 dòng với số mới (4000 TPS; 90+40 ms; 45 s gấp đôi; 3 000 000 trừ 1 200 000 bồi hoàn); pause 150 s. Kết quả mong đợi trên màn hình step 2: CÓ; khớp mong_doi.txt 5/5. Cảnh quy mô id quymo: x1 / x100 / x10 000: 100 / 10 000 / 1 triệu TPS; 15,5 / 1550 / 155 000 việc cùng lúc; 6000 / 600 000 / 60 triệu khoá; giải pháp đổi (một máy -> hàng đợi nhiều máy Redis chung -> chia theo tài khoản, nhiều cụm Redis, SAGA); đánh đổi (SAGA là cái giá). Tính lại: ĐÚNG hết.

## Lab
Tự làm được: CÓ (~4 phút). Tự viết acb_l00_mau.py trước khi mở loi_giai.py; `bash labs/cham.sh ACB L00 <tệp>` -> ĐÚNG. cham.sh với loi_giai.py -> ĐÚNG. Kẹt: không; de.md có mẫu năm dòng. Thiếu: người học cần biết print/if (video có dạy ở cảnh code). Điều kiện: máy phải có Python 3 (requires_ext PYT:L00,L01). mong_doi khớp màn hình.

## Người học kẹt ở đâu
concept s1: SVG "Bản tin ISO 8583 0200/0210 ... Socket TCP nhị phân ... Oracle 19c PL-SQL" (không giải thích 0200/0210 và 19c); và quiz s1 "bản tin 0200".

## Đã tính lại / chạy
~38 số: 38/38 khớp. Mã chạy: acb_l00_mau.py bằng cham.sh (ĐÚNG), loi_giai.py (ĐÚNG), mã trong cảnh code chạy cho ra 600000 36000000 / 155 ms / dat P99 (khớp). Khung hình: 00019 (≈130 s thuật ngữ), 00029 (≈200 s SVG bốn tầng), 00046 (≈300 s code), 00076 (≈500 s quymo), 00099 (≈700 s quiz/practice). Không lỗi hiển thị (SVG 4 tầng chiếm 3/4 chiều ngang, chữ đọc được).

## Bảng sự kiện cần nhất quán
| Sự kiện | Giá trị | bài:cảnh |
|---|---|---|
| Vai trò ứng viên | "3 năm tại OCB, Chuyên viên chính trong Squad Lending" (show); "nhóm tín dụng tại OCB" (say); từng làm mảng cho vay tại Mirae Asset; đang học Cử nhân AI UIT, dự kiến 11/2026 | ACB L00:quiz s3 (mâu thuẫn INT L08:hook về Squad Lending) |
| Kinh nghiệm theo INT | OCB 10/2023–nay; Grooo dự án Mirae Asset Finance 2022–2023 | INT L07:example s2 |
| Lương ACB | "Thương lượng"; tháng 13 cố định; thưởng cuối năm 1–4 tháng | ACB L00:quiz s3; source |
| Số lương minh hoạ | L=40 triệu -> 520; 560–680 | ACB L00:quiz |
| Hệ core | T24 (Temenos), kiến trúc tham chiếu từ OCB; ACB không nói rõ core | ACB L00:hook |
| MTI | 0200/0210 yêu cầu/phản hồi; 0400 yêu cầu đảo; 0420 thông báo đảo | ACB L00:concept, quiz s2 |
| Độ trễ minh hoạ | NAPAS 120 ms + core 35 ms = 155 ms; ngưỡng chờ 1500 ms; P99 200 ms | ACB L00:example s2 |
| Khoá khử trùng lặp | 60 giây (TTL) | ACB L00:prereq; example s3 |
| Timeout xử lý | nghi vấn -> truy vấn sau 3 giây -> bồi hoàn SAGA | ACB L00:check |
| Tải minh hoạ | 10 000 TPS (x100 của 100 TPS) | ACB L00:prereq; quymo |


## ACB L01
sha16 YAML = 12470f9d53589388 (khớp). 12 cảnh / 31 step; 13,34 phút (800,3 s).

## Phần A
| Mức | Cảnh/step | Trích | Vì sao / bằng chứng | Đề xuất | Tin cậy |
|---|---|---|---|---|---|
| SHOULD | symbol s1, s2 | "APPLICATION,VERSION/FUNCTION/PROCESS,USER/PASSWORD/COMPANY,TRANSACTION.ID,FIELD:MV:SV=VALUE,..."; "FUNDS.TRANSFER,ACTR/I/PROCESS,INPUTTER/******/VN0010001,,DEBIT.ACCT.NO=..." | YAML source ghi rõ "tài liệu Temenos về OFS không công khai (cú pháp ... chưa kiểm được với nguồn có thẩm quyền)", nhưng màn hình/lời đọc chỉ ghi "ví dụ minh hoạ", không báo cú pháp chưa kiểm; còn lời đọc nói "Bản tin OFS tuân theo cấu trúc phân cách nghiêm ngặt ... thiếu một dấu phẩy ... T24 sẽ từ chối". Theo kiến thức của tôi, phần tuỳ chọn thật còn có thêm thành phần (VALIDATE, GTSMODE, NO.OF.AUTH...), và "ACTR" là version không chắc có sẵn. Không kiểm được nguồn thẩm quyền. | Thêm "cú pháp rút gọn, kiểm lại với tài liệu Temenos của ngân hàng" | PLAUSIBLE |
| SHOULD | quiz s3 / concept | "Hàng đợi riêng ... hàng triệu hàng đợi riêng sẽ làm quá tải"; đáp án A | Hợp lý nhưng tuyệt đối: thực tế IBM MQ vẫn dùng hàng đợi trả lời động theo phiên; so sánh "một hàng đợi mỗi khách hàng" là kịch bản cực đoan. Đáp án A vẫn là lựa chọn tốt nhất trong 4. | không bắt buộc | PLAUSIBLE |

Không phát hiện MUST. Tính lại: 5000x60=300000; 1000//35=28 (28,57); L=5000x0,035=175; 5000/28=178,57 -> 179; 2x3=6; 5000x2=10000; quymo 50 -> 1,75/2; 5000 -> 175/179; 500000 -> 17500/17857,1 -> 17858; tồn đọng 1000/s, 60 s -> 60000, chờ 60000/4000 = 15 s; 10 s -> 10000, 2,5 s; practice 2000x45//1000=90, 1000//45=22, ceil(2000/22)=91. Tất cả đúng. BOTHRESH/BOQNAME/Message Expiry/JMSCorrelationID đúng thuật ngữ IBM MQ. Nhất quán với ACB L00 (timeout: nghi vấn, truy vấn sau 3 giây, không hoàn tiền vội).

## Điểm
P1=1 P2=2 P3=2 P4=2 P5=2 P6=2 P7=2 Tổng(P1–P7)=13 P8=2 P9=2. Mất gốc: ĐỦ (13, không mục 0).
Cần biết trước: MV/SV (đa trị/phụ trị) trong khung OFS; biểu thức sinh trong Python `for k, v in truong.items()`; "mã FT"; "COMPANY"/mã công ty.
P1 < 2, danh sách mục chưa giảng:
1. "FIELD:MV:SV=VALUE" (symbol s1, chuỗi khung OFS) — MV, SV không giải thích.
2. `",".join(k + "=" + v for k, v in truong.items())` (code s1) — biểu thức sinh và `.items()` không giảng (lời đọc chỉ nói "nối các cặp").
(Mục "mã FT" và "COMPANY/VN0010001" cũng không giải thích tại chỗ; nếu tính thì thành 4 mục, P1=0. Tôi tính 2 mục rõ ràng.)
Chỗ thiếu chính: mã Python s1 khá dày với người mất gốc; JMS/Java nhắc không giảng nền Java.

## Cảnh Tự làm
id practice: viết mau.py ráp OFS với số mới, ghép 3 trả lời sai thứ tự, tính đang chờ/số kết nối; pause 180 s. Có kết quả mong đợi trên màn hình (step 2, 9 dòng): CÓ; khớp mong_doi.txt 9/9 dòng. Cảnh quy mô id quymo: x1/x100/x10 000: 50/5000/500 000 lệnh mỗi giây; đang chờ 1,75/175/17 500; kết nối tuần tự 2/179/17 858; chọn gì (một kết nối -> nhóm kết nối ghép mã -> nhiều bộ quản lý hàng đợi, chia dải tài khoản; Core là nút cổ chai); thêm thời gian: tồn đọng 1000 bản tin/s (60 s -> 60 000; chờ 15 s; hạn sống 10 s -> hết hạn). Tính lại ĐÚNG.

## Lab
Tự làm được: CÓ (~8 phút; nhiều dòng hơn L00). Tự viết acb_l01_mau.py trước khi mở loi_giai.py; `bash labs/cham.sh ACB L01 <tệp>` -> ĐÚNG; cham.sh với loi_giai.py -> ĐÚNG. Đề đủ, có khung từng dòng; kẹt nhỏ: "phần đầu = mọi thứ tới và gồm hai dấu phẩy" (đã giải thích trong de.md); chia nguyên//, làm tròn lên cần mẹo -(-a//b) (có "Nếu kẹt"). mong_doi khớp màn hình.

## Người học kẹt ở đâu
symbol s1: "FIELD:MV:SV=VALUE" (MV, SV); code s1: biểu thức sinh `for k, v in truong.items()` trong hàm ofs.

## Đã tính lại / chạy
~30 số: 30/30 khớp. Mã chạy: acb_l01_mau.py (ĐÚNG), loi_giai.py (ĐÚNG); các đoạn mã trong cảnh code mô phỏng chạy đúng kết quả hiển thị (c2/c1/con cho: 0; tin OFS; DEBIT.AMOUNT=5000000). Khung hình: 00035 (≈230 s Little), 00052 (≈330 s code ghép), 00067 (≈420 s quymo), 00081 (≈520 s quiz bước 1), 00088 (≈650 s practice). Không lỗi hiển thị.

## Bảng sự kiện cần nhất quán
| Sự kiện | Giá trị | bài:cảnh |
|---|---|---|
| Hệ core | T24 (Temenos) là kiến trúc tham chiếu từ OCB; ACB không nêu core | ACB L01:hook s1 |
| Timeout T24 | 3 giây -> IN_DOUBT -> Worker truy vấn theo mã tham chiếu -> chỉ hoàn tiền khi có kết quả chắc chắn (khớp ACB L00:check) | ACB L01:check s1,s2 |
| Hàng đợi | T24.OFS.REQUEST / T24.OFS.REPLY; dung lượng 10 000 (=2x lưu lượng 5000/s, minh hoạ) | ACB L01:example s3 |
| Hạn sống bản tin | 60 giây (minh hoạ); BOTHRESH = 3 | ACB L01:pitfall |
| Độ trễ / tải minh hoạ | 35 ms; 5000 lệnh/s; một kết nối tuần tự 28 lệnh/s | ACB L01:example; quymo |
| Mã tham chiếu | JMSCorrelationID (khác khoá lũy đẳng) | ACB L01:quiz s3 |
| Khoá chống lặp | tên chuyên môn: khoá lũy đẳng (idempotency key) | ACB L01:quiz s3 |
| Mã công ty/OFS | VN0010001 (ví dụ), VN0010002 (lab) | ACB L01:symbol; practice |


## ACB L02
sha16 YAML = df13a47a911e359c (khớp). 12 cảnh / 35 step; 15,59 phút (935,2 s).

## Phần A
| Mức | Cảnh/step | Trích | Vì sao / bằng chứng | Đề xuất | Tin cậy |
|---|---|---|---|---|---|
| SHOULD | concept s1 so với recap s1 | concept (lời đọc): "Bước hai, Core Banking giữ trước số tiền ... Bước ba, Cổng thanh toán kiểm tra khoá khử trùng lặp"; recap (chữ + lời đọc): "Khoá Redis khử trùng lặp → Giữ tiền trên Core Banking → ..." | Thứ tự khử trùng lặp và giữ tiền ngược nhau giữa hai cảnh. Về kỹ thuật nên khử trùng lặp trước khi giữ tiền (nếu giữ tiền trước, bản tin gửi lại có thể giữ tiền hai lần). Người học nhớ hai thứ tự khác nhau. | Thống nhất: khử trùng lặp trước, rồi giữ tiền; sửa sơ đồ concept | CONFIRMED |
| SHOULD | quymo s1 | cột "đỉnh (× 1,5)" với giá trị 120 / 12 000 / 1 200 000 | Giá trị là TPS đỉnh (80x1,5, 8000x1,5, 800 000x1,5) nhưng cột đứng ngay sau "đang chờ" (9,6 / 960 / 96 000) nên dễ đọc thành "đang chờ lúc đỉnh" (14,4 / 1440 / 144 000). Nhãn cột thiếu đơn vị. | Đổi nhãn "lệnh mỗi giây lúc đỉnh (x1,5)" | CONFIRMED |
| SHOULD | check s2 | "Chỉ hoàn tiền 10 triệu đồng khi đã xác nhận giao dịch thất bại qua tra soát hoặc đối soát; khi đó mới gửi yêu cầu đảo (MTI 0400; 0420 là thông báo đảo)" | Cùng điểm với ACB L00:quiz s2: trong ISO 8583 mạng thẻ, 0400 thường được gửi ngay khi hết giờ vì chưa biết kết quả (bên nhận so khớp, bỏ qua nếu chưa có giao dịch gốc). Bài nêu thứ tự "tra soát rồi mới 0400" và đã kèm "đặc tả NAPAS cần kiểm". Nhất quán với L00/L01. Chưa kiểm được đặc tả NAPAS. | Ghi "tuỳ đặc tả; thẻ thường đảo ngay" | PLAUSIBLE |
| SHOULD | hook s1 | "xử lý bản tin theo đặc tả kết nối gốc ISO 8583 qua đường truyền Socket TCP" | Đặc tả NAPAS 247 thật chưa kiểm (đã ghi "cần kiểm với đặc tả kết nối của NAPAS"); NAPAS có thể dùng định dạng khác (ví dụ ISO 20022) cho một số dịch vụ. Không kiểm được: chưa kiểm được nguồn. | không bắt buộc | PLAUSIBLE |

Không phát hiện MUST. Tính lại và đã chạy: bitmap {3,4,11,37} = 3020000008000000; {2,3,4,7} = 7200000000000000; 0x72 = 0111 0010 -> bit 2,3,4,7; 0xF2 -> bit 1 + 2,3,4,7; 8000x60 = 480 000; 1500-120 = 1380; L = 8000x0,12 = 960; 8000x1,5 = 12 000; quymo 9,6 / 960 / 96 000; 4800 / 480 000 / 48 triệu khoá; dedup t=0 True, t=20 False, t=61 True; practice bitmap A 3020000008800000; B B020000008000000 + 0000000000000001; giải mã 5030000000000000 = [2, 4, 11, 12]; TTL 80; t=0 True, 30 False, 95 True; 2400x150//1000 = 360. Tất cả đúng. Trường ISO 8583 đúng chuẩn (3 mã xử lý, 4 số tiền, 11 STAN 6 số, 37 RRN 12 ký tự, 52 PIN 8 byte, 64/128 MAC; bit 1 = bitmap thứ hai); VND 0 chữ số lẻ theo ISO 4217 đúng. NAPAS = Công ty Cổ phần Thanh toán Quốc gia Việt Nam: đúng theo kiến thức của tôi. Redis SET NX EX nguyên tử đúng.

## Điểm
P1=0 P2=2 P3=2 P4=2 P5=2 P6=2 P7=2 Tổng(P1–P7)=12 P8=2 P9=2. Mất gốc: GẦN (tổng 12 nhưng P1 = 0).
Cần biết trước: cú pháp Python `format(bits, "016X")`, biểu thức liệt kê `[n for n in range(1, 65) if ...]`, "băm" (hash); "kênh truyền nhị phân"; phép tính nhị phân/hệ 16 (được giảng).
P1 < 2, danh sách mục chưa giảng:
1. `format(bits, "016X")` (code s1) — định dạng 16 chữ số hệ 16 in hoa không được giảng.
2. `[n for n in range(1, 65) if (bits >> (64 - n)) & 1]` (code s3) — biểu thức liệt kê/`range` không giảng; chỉ giảng `>>`, `& 1`, `int(..., 16)`.
3. "chia khoá theo băm sang nhiều cụm Redis" (quymo s1) — "băm" (hash) không giải thích.
(Ba mục đều có thể bị coi là biên: lời đọc giải thích ý nghĩa hàm; nếu bỏ mục 3, P1=1.)
Chỗ thiếu chính: bài dày (15,6 phút, nhiều chủ đề: bitmap, HSM, MAC, dedup, đảo); phép toán bit khó với người mất gốc nhưng có giảng từng bước và có bảng 4 bit-> hex.

## Cảnh Tự làm
id practice: viết mau.py: bitmap A (3,4,11,37,41), bitmap B (có trường 128, cần bitmap thứ hai), giải mã 5030000000000000, khoá dedup tại giây 0/30/95 (gửi lại tối đa 40 s, TTL gấp đôi), đang chờ (2400 TPS, 150 ms); pause 210 s. Kết quả mong đợi trên màn hình step 2 (7 dòng): CÓ; khớp mong_doi.txt 7/7. Lưu ý: định dạng bitmap B ("chính phụ" cách bằng dấu cách) chỉ có trong de.md, màn hình nói "Định dạng ... trong de.md". Cảnh quy mô id quymo: x1/x100/x10 000: 80 / 8000 / 800 000 TPS; đang chờ 9,6 / 960 / 96 000; đỉnh x1,5 = 120 / 12 000 / 1,2 triệu; khoá cùng tồn tại 4800 / 480 000 / 48 triệu; chọn gì (một kết nối, một Redis -> vài kết nối bền, Redis chung -> nhiều kết nối, chia khoá theo băm, nhiều cụm Redis, thêm HSM phần cứng); theo thời gian: TTL 60 s đủ khi gửi lại sau 30 s, hết hạn khi 90 s -> chốt cuối UNIQUE. Tính lại ĐÚNG.

## Lab
Tự làm được: CÓ (~10 phút; khó nhất trong ba bài ACB vì bit). Tự viết acb_l02_mau.py trước khi mở loi_giai.py; `bash labs/cham.sh ACB L02 <tệp>` -> ĐÚNG; cham.sh với loi_giai.py -> ĐÚNG. Đề đủ: de.md cho công thức 1<<(64-n), giải thích trường 128 là vị trí 64 của bitmap thứ hai, nói rõ "chính phải có thêm trường 1". Thiếu: người học cần nhớ cách giải mã (đã có trong video, scene code s3). mong_doi khớp màn hình.

## Người học kẹt ở đâu
code s1: `format(bits, "016X")`; code s3: biểu thức liệt kê `[n for n in range(1, 65) if (bits >> (64 - n)) & 1]`; practice: bitmap B (trường 1 và bitmap phụ) cần đọc de.md.

## Đã tính lại / chạy
~40 số: 40/40 khớp. Mã chạy: acb_l02_mau.py (ĐÚNG), loi_giai.py (ĐÚNG); các hàm bando, giaima, dat trong bài chạy cho đúng kết quả hiển thị. Khung hình: 00030 (≈190 s bảng trường), 00037 (≈240 s bitmap), 00057 (≈380 s code bando), 00081 (≈530 s pitfall), 00102 (≈720 s practice). Không lỗi hiển thị.

## Bảng sự kiện cần nhất quán
| Sự kiện | Giá trị | bài:cảnh |
|---|---|---|
| NAPAS | Công ty Cổ phần Thanh toán Quốc gia Việt Nam; 247 = 24/7 | ACB L02:hook s1 |
| Bản tin | MTI 0200 yêu cầu, 0210 phản hồi, 0400 yêu cầu đảo, 0420 thông báo đảo (ISO 8583:1987; đặc tả NAPAS cần kiểm) | ACB L02:prereq, check s2; ACB L00:quiz |
| Trường ISO 8583 | 3 mã xử lý; 4 số tiền (VND không số lẻ, ISO 4217); 11 STAN 6 số; 37 RRN 12 ký tự; 52 PIN block 8 byte; 64/128 MAC; bit 1 = bitmap thứ hai | ACB L02:symbol |
| Ngưỡng chờ | 1500 ms (ví dụ), phản hồi 120 ms; gửi lại tối đa 30 giây (ví dụ); TTL khoá 60 s | ACB L02:prereq; example s2 |
| Khoá khử trùng lặp | napas:dedup:{stan}:{rrn}; SET NX EX 60; chốt cuối UNIQUE | ACB L02:example s2 |
| Tải minh hoạ | 8000 TPS, hệ số đỉnh 1,5 -> 12 000 | ACB L02:example s3 |
| Timeout | IN_DOUBT -> tra soát -> chỉ hoàn khi xác nhận thất bại -> 0400; EOD đối soát (nhất quán ACB L00/L01) | ACB L02:check |
| Thứ tự luồng | concept: Core giữ tiền (bước 2) rồi dedup (bước 3); recap: dedup rồi giữ tiền (không nhất quán) | ACB L02:concept; recap |
| Tiêu chuẩn PIN | PCI DSS; PCI PIN Security; PIN chỉ dịch trong HSM | ACB L02:pitfall; quiz |


## ACB L03
sha16 YAML = b920c4706498ffa8 (khớp). 12 cảnh (hook, prereq, concept, symbol, example, code, check, pitfall, quymo, quiz, practice, recap); 100 khung/câu; 867,6 s = 14,46 phút.

## Phần A
| Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng | Đề xuất | Tin cậy |
|---|---|---|---|---|---|
| SHOULD | quymo step1 (+ example step1) | "cần hai tiến trình chạy song song. Vì vậy Kafka phải chia chủ đề thành ít nhất hai phân vùng" (hàng ×100 = "2") | Bài tự nêu ở example step1 "mức đỉnh giả định 1500 lệnh mỗi giây". 1500/500 = 3,0 tiến trình ở đỉnh, 833/500 = 1,67 -> 2 chỉ đúng với tải TRUNG BÌNH. Bảng quy mô chọn theo trung bình, bỏ qua đỉnh bài đã nêu -> mâu thuẫn nhẹ giữa hai cảnh, và dạy sai thói quen sizing. Tính lại bằng Python: 1500/500=3.0. | Thêm một dòng "ở đỉnh 1500/giây cần 3 tiến trình" hoặc ghi rõ "theo tải trung bình" | CONFIRMED (suy luận từ số trong bài) |
| SHOULD | hook step2 | "Kafka: hệ thống lưu các sự kiện theo đúng thứ tự trong từng chủ đề (topic)" | Kafka chỉ đảm bảo thứ tự TRONG TỪNG PHÂN VÙNG, không phải cả chủ đề; chính cảnh quymo nói đúng ("thứ tự chỉ được giữ trong từng phân vùng"). Hai câu lệch nhau; ở hook người mất gốc nhớ sai. | Sửa "theo đúng thứ tự trong từng phân vùng của chủ đề" hoặc thêm "khi chủ đề có 1 phân vùng" | CONFIRMED (hành vi Kafka) |
Không có MUST. Phần còn lại đã kiểm: cú pháp CREATE STREAM ... AS SELECT ... LEFT JOIN ... EMIT CHANGES hợp lệ ksqlDB; CASE với NULL rơi xuống WHEN sau đúng (None -> SMS ở 80000, đã chạy lại); "SET key 1 EX 86400 NX" nguyên tử đúng; xô thẻ ví dụ nhỏ đúng; quiz A đúng, B/C/D sai đúng lý (ksqlDB có stream-stream join với WITHIN).

## Điểm
P1=1 P2=2 P3=2 P4=2 P5=2 P6=2 P7=2 Tổng(P1-P7)=13 P8=2 P9=2. Mất gốc: ĐỦ.
Cần biết trước: Redis/SET, Core Banking, Python (while, tuple) lấy từ khoá PYT/ACB trước; HTTP 503 có chú thích.
Chỗ thiếu chính: bí danh bảng `e`/`p` trong câu ksqlDB.
P1 = 1 (2 mục, đều ở mức ranh giới):
1. symbol step1: `FROM s_balance_events e LEFT JOIN t_customer_preferences p`, `e.account_no`, `p.email` — bí danh `e`, `p` và cách viết `bí_danh.cột` không được nói ra ở đâu (nói "ghép hai bên theo số tài khoản chung" nhưng không giải thích e/p).
2. concept step1: chữ "OTP" trong sơ đồ ("Hàng đợi ưu tiên OTP") và code "ma OTP": say chỉ nói "mật mã dùng một lần" và không bao giờ gắn với chữ OTP trên màn hình trong bài này (chỉ phụ thuộc bài cũ). (Nếu coi câu say là giải thích thì còn 1 mục.)

## Cảnh Tự làm
id `practice` (tiêu đề "Tự làm: chọn kênh, hàng đợi ưu tiên và xô thẻ"), pause 240 s; đề số khác ví dụ, step 2 hiện "Kết quả mong đợi" 4 dòng, step 3 gợi ý khi kẹt + lệnh cham.sh. Có kết quả mong đợi trên màn hình: CÓ. Khớp mong_doi.txt: KHỚP từng dòng (đã đối chiếu).
## Cảnh quy mô
id `quymo`: 3 mức ×1/×100/×10 000 (500, 50 000, 5 000 000 tin/phút; 8,3 / 833 / 83 333 tin/s; 1 / 2 / 167 tiến trình; 720 000 / 72 triệu / 7,2 tỉ khoá) + đánh đổi TTL 24h vs 1h (7,2 tỉ vs 300 triệu khoá; tin gửi lại sau 1 giờ lọt) và so sánh thông báo vs lệnh chuyển tiền. Tính lại: 500/60=8,33; 50000/60=833,3; 5e6/60=83333,3; /500 = 166,67 -> 167; khoá 720000 / 72 000 000 / 7 200 000 000; 5e6*60=300 000 000. ĐÚNG (trừ SHOULD về đỉnh).

## Lab
Tự làm được: CÓ (không kẹt); ~8-10 phút. Đề đủ: đủ (luật kênh, hàng ưu tiên, xô thẻ có số giây, cước), cần biết heapq hoặc sắp xếp danh sách (đề nói "số nhỏ ra trước" nên sorted() cũng được). Điểm có thể kẹt: xô thẻ "cộng thêm số giây đã trôi" — bài đã giảng bằng bảng. mong_doi khớp màn hình: KHỚP. cham.sh với lời giải tự viết: ĐÚNG; cham.sh với loi_giai.py: ĐÚNG.

## Người học kẹt ở đâu
symbol step1: `FROM s_balance_events e LEFT JOIN ... p ON e.account_no = p.account_no` (bí danh e/p chưa giảng); ngoài ra không kẹt.

## Số tính lại / mã đã chạy / khung hình
Số tính lại: 17 phép (833; 3 triệu/giờ; 72 triệu/ngày; 35 000/15 000; 86 400 s=24h; 8,3/833/83 333; 2/167; 3 hàng khoá; 300 triệu; 1500/500=3; lab 58 500/31 500) — 17/17 khớp. Mã chạy: lab (2 lần cham.sh ĐÚNG), kenh() và heapq trên màn hình (kết quả khớp màn hình: True 20000 OTT_PUSH ... / (1,'ma OTP')...). ksqlDB/Redis chỉ đọc, không chạy.
Khung hình đã xem: 00020.png (117 s, sơ đồ concept), 00027.png (166 s, câu ksqlDB), 00052.png (327 s, heapq), 00073.png (447 s, bảng quymo), 00091.png (575 s, cảnh Tự làm). Không lỗi hiển thị (chữ không tràn/đè, đọc được).

## Bảng sự kiện cần nhất quán
| Sự kiện | Giá trị | bài:cảnh |
|---|---|---|
| Ngưỡng tiền đi SMS (minh hoạ) | >= 50 000 đồng | L03:symbol, code, concept, practice |
| Lưu lượng ví dụ | 50 000 tin/phút; đỉnh 1500/s; 833/s | L03:prereq, example |
| Độ trễ mục tiêu | < 500 ms | L03:prereq |
| Khoá khử trùng lặp Redis | SET noti:sent:{event_id} 1 EX 86400 NX = 24h | L03:example step3 |
| Cầu dao | tỉ lệ lỗi > 10% -> nhà mạng dự phòng trong 200 ms (minh hoạ) | L03:check |
| Giao dịch minh hoạ | 50 triệu đồng cần OTP | L03:check (so với L06 ngưỡng sinh trắc 10 triệu/20 triệu) |
| Tỉ lệ cài app | 70% (bài), 65% (lab) | L03:example, practice |
| Kafka | giao ít nhất một lần (mặc định) | L03:example step3 |
| Xử lý/tiến trình | 500 tin/giây (minh hoạ) | L03:quymo |
| Văn bản pháp lý / lương / tên người thật | không có | — |


## ACB L04
sha16 YAML = d18a7fccc0e66c74 (khớp). 12 cảnh (hook, prereq, concept, symbol, example, code, check, pitfall, quymo, quiz, practice, recap); ~100 khung; 14,18 phút.

## Phần A
| Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng | Đề xuất | Tin cậy |
|---|---|---|---|---|---|
| SHOULD | example step3 | "Toàn bộ quy trình loại trừ xung đột hoàn tất trong khoảng 25 mili giây (ví dụ minh họa)"; say: "toàn bộ tiến trình xử lý chỉ tiêu tốn 25 mi li giây" | Dòng thời gian trên màn hình: 10:00:00.100 là lần ghi TRƯỚC, người mua 1 gửi .120, người mua 2 gửi .125. 125-100 = 25 là khoảng từ lần ghi cũ, không phải thời gian xử lý (từ .120 tới .125 chỉ 5 ms). Con số 25 ms gán nhầm nhãn "toàn bộ quy trình". | Đổi thành "5 ms giữa hai yêu cầu" hoặc bỏ 25 ms | CONFIRMED (số học trên màn hình) |
| SHOULD | concept step2 + quymo | "người đến sau nhận 409 ngay, không chờ"; bảng quymo coi lạc quan = 0 giây chờ | Trên PostgreSQL (READ COMMITTED) câu UPDATE thứ hai trên cùng dòng vẫn phải chờ giao dịch đầu commit rồi mới tính lại điều kiện (rồi mới 0 dòng). Chờ rất ngắn (không phải 20 ms x n) nhưng không phải "0, không chờ". Bài có nói khoá dòng giữ "trong tích tắc" nên đây là thiếu điều kiện, không sai hẳn. | Thêm "chờ rất ngắn bằng thời gian một câu UPDATE" | PLAUSIBLE (hành vi PostgreSQL, không chạy được ở đây) |
Không có MUST. Đã kiểm: 500e6 x 0,001 x 335/365 = 458 904,1 (khớp 458 904 và "459 nghìn"); 35 000 000 - 458 904 = 34 541 096 (34,5 triệu); 199 x 0,02 = 3,98; 19 999 x 0,02 = 399,98 s = 6,67 phút ("gần 7 phút"); mã Go (res.RowsAffected(), fiber.StatusConflict, fiber.Map) hợp lệ; sqlite rowcount 1/0 và ver 8 đã chạy khớp; quiz A đúng, B/C/D sai đúng lý; "CIF = Customer Information File" đúng thông lệ. Rút trước hạn hưởng lãi không kỳ hạn: bài ghi "theo thông tư NHNN về tiền gửi", không nêu số hiệu và source ghi rõ "chưa đối chiếu" -> chấp nhận (chưa kiểm được nguồn thông tư cụ thể).

## Điểm
P1=1 P2=2 P3=2 P4=2 P5=2 P6=2 P7=2 Tổng(P1-P7)=13 P8=2 P9=2. Mất gốc: ĐỦ.
Cần biết trước: Python/sqlite cơ bản (execute, tuple tham số), UPDATE...WHERE, OFS (acb_ofs L01).
Chỗ thiếu chính: cú pháp tham số `:cif :id :ch :dt :old_ts`/`?`.
P1 = 1 (2 mục chắc + 1 ranh giới):
1. symbol step1: `receive_cif = :cif`, `order_id = :id AND channel = :ch AND order_date = :dt ... = :old_ts` — ký hiệu `:tên` là chỗ giữ tham số, không giảng; cũng không nói vì sao WHERE có 3 cột `channel`, `order_date` ngoài `order_id` (khoá ghép). Sau đó code step1 `?` + `(7,)` cũng không giải thích.
2. code step2 (và practice): trạng thái `REVERT` xuất hiện trong tập CANH, không bao giờ được giảng (ý "hoàn lại") — nằm trong đề tự làm.
3. (ranh giới) code step1: `.rowcount` — say nói "số dòng tác động" nhưng chưa gắn tên thuộc tính; practice step3 mới nói "thuộc tính rowcount".

## Cảnh Tự làm
id `practice` ("Tự làm: khoá lạc quan bằng sqlite, tiền lãi mất đi và máy trạng thái"), pause 240 s; số khác ví dụ (3 người, ver 3, 300 triệu, 6,8%, ngày 200). Có kết quả mong đợi 9 dòng ở step2: CÓ; khớp mong_doi.txt từng dòng: KHỚP. Đề trên màn hình không nói "kỳ hạn 12 tháng" (de.md có) nhưng "Nếu kẹt" cho công thức gốc x 68 // 1000 nên đủ.
## Cảnh quy mô
id `quymo`: 3 mức ×1/×100/×10 000 = 2 / 200 / 20 000 người mua; lạc quan: 1 / 199 / 19 999 nhận 409; bi quan: 0,02 / 3,98 / 399,98 giây; đánh đổi (giới hạn gửi lại, báo "đã bán" sớm); thêm mục "theo thời gian": dấu thời gian thô vs số phiên bản. Tính lại ĐÚNG hết (xem trên).

## Lab
Tự làm được: CÓ, ~8 phút, không kẹt (cần sqlite3 trong Python; công thức lãi nằm ở màn hình "Nếu kẹt"). Đề (de.md) đủ. mong_doi khớp màn hình: KHỚP. cham.sh với lời giải tự viết: ĐÚNG; với loi_giai.py: ĐÚNG.

## Người học kẹt ở đâu
symbol step1: "receive_cif = :cif ... AND channel = :ch AND order_date = :dt AND last_access = :old_ts" (ký hiệu :tên và ba cột khoá chưa giảng); chỗ khác không kẹt.

## Số tính lại / mã đã chạy / khung hình
Số tính lại 14 (458 904; 34 541 096; 35 triệu; 125-120; 199/19 999 x 0,02; 399,98/60; lab 20 400 000, 164 384 (164383,56 làm tròn), 20 235 616, hạng ver 4) — 14/14 khớp. Mã chạy: sqlite + máy trạng thái trên màn hình (khớp: mua 1: 1, mua 2: 0, ver 8; cho phep/tu choi); lab 2 lần ĐÚNG. Go/PostgreSQL chỉ đọc.
Khung hình: 00023.png (137 s, sơ đồ concept + giải thích 409), 00034.png (216 s, câu UPDATE), 00048.png (297 s, mã Go), 00068.png (419 s, pitfall; không phải bảng quymo), 00089.png (558 s, cảnh Tự làm). Không lỗi hiển thị. (Chưa xem riêng bảng quymo bằng ảnh; đọc từ YAML.)

## Bảng sự kiện cần nhất quán
| Sự kiện | Giá trị | bài:cảnh |
|---|---|---|
| Ví dụ tiền gửi | 500 triệu, 12 tháng, 7% -> lãi 35 triệu | L04:prereq |
| Rút trước hạn | tháng 11 = 335 ngày, lãi không kỳ hạn giả định 0,1%/năm -> 458 904 đ; mất 34,5 triệu | L04:prereq |
| Căn cứ pháp lý rút trước hạn | "thông tư NHNN về tiền gửi" (không số hiệu; source: chưa đối chiếu) | L04:prereq, header source |
| Khoá bi quan giữ | 20 ms/người (minh hoạ) | L04:quymo |
| Thời gian ví dụ xung đột | .100 / .120 / .125; "25 ms" | L04:example |
| Mã HTTP | 200 OK, 409 Conflict | L04:concept, example |
| Mã lỗi nội bộ adapter | 04 Timeout, 05, 999 (không phải mã T24) | L04:check |
| Tỉ lệ đọc | > 99% (giả định) | L04:quiz |
| Tên bản tin OFS | ACCOUNT_T24_DEPOSIT_OFS, AZ_ACCOUNT_T24_OFS_AMD ("đã đặt lại tên") | L04:concept |
| Core | T24 là "kiến trúc tham chiếu từ OCB, ACB không nói dùng core nào" | L04:hook |
| Trạng thái | CHAO_BAN, PROCESSING, HOLD, DONE, REVERT | L04:code, practice |


## ACB L05
sha16 YAML = cd4c22eed138d94e (khớp). 13 cảnh (hook, prereq, concept, symbol, example, code, check, pitfall, quymo, quiz, practice, recap = 12 id; quymo 3 step); ~110 khung; 16,72 phút.

## Phần A
| Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng | Đề xuất | Tin cậy |
|---|---|---|---|---|---|
| SHOULD | hook step1 + pitfall step1 so với quymo step1 | hook: "Vòng lặp tuần tự gọi từng tài khoản thì quá chậm ... mục tiêu ví dụ: 3 phút"; pitfall: "mất hàng giờ để chi lương" | Bảng quymo của chính bài: 10 000 lệnh x 5 ms = 50 s tuần tự (dưới mục tiêu 3 phút), chỉ ở 1 000 000 lệnh mới 5 000 s (83 phút). Với "mười nghìn nhân viên" của hook, tuần tự KHÔNG mất hàng giờ và không vượt 3 phút -> hook/pitfall nói to hơn số liệu bài tự dựng. Tính lại bằng Python: 10000*5/1000=50,0 s. | Đổi hook thành "ở 1 triệu lệnh thì tuần tự mất 83 phút" hoặc nêu số 5 ms/lệnh ngay hook | CONFIRMED (số học trong bài) |
| SHOULD | quymo step2 (hàng ×10 000) | "100 000 000 bản ghi ... số đoạn song song 100 ... 10 giây" | Bước 4 của example chia theo ngày: 30 ngày chỉ cho tối đa 30 đoạn theo ngày (7+7+7+9 là gộp ngày). Chia theo ngày tối đa 30 đoạn thì 1e8/30/1e5 = 33,3 s, không phải 10 s; 10 s chỉ đúng nếu chia đều theo SỐ BẢN GHI (bài chỉ nói câu này cho cỡ ×100). | Ghi rõ "chia đều theo số bản ghi (offset), không theo ngày" ở hàng ×10 000, hoặc đổi số | CONFIRMED (1e8/30/1e5=33,33) |
| SHOULD | symbol (tiêu đề) + objective 4 | tiêu đề cảnh: "Cú pháp Khoá hàng có thứ tự xác định và Bulk Collect trong Oracle PL/SQL" | Mã trên màn hình chỉ có vòng FOR ... SELECT ... FOR UPDATE; KHÔNG có dòng BULK COLLECT/FORALL nào. BULK COLLECT/FORALL chỉ được nêu bằng chữ ở example step3 (không có cú pháp). Mục tiêu 4 "Tính tiết kiệm ... số lần chuyển ngữ cảnh khi cập nhật từng dòng và khi dùng FORALL" chỉ có "10 000 lần" so với "một lần" bằng lời. Bài hứa cú pháp mà không cho. | Thêm 3-4 dòng mẫu FORALL, hoặc đổi tiêu đề | CONFIRMED |
| SHOULD | check step1 (bảng) | cột "cách xử lý sơ cấp": hàng 2 "Làm nhân viên nhận lương 2 lần", hàng 3 "Gây thất thoát hàng tỉ đồng" | Hai ô này là HẬU QUẢ, không phải cách xử lý; bảng hai cột làm người học tưởng đó là các cách làm sai. | Thêm cột hậu quả như bảng cảnh khác | CONFIRMED (nhãn bảng) |
Không có MUST. Đã kiểm: 10 000 x 15 triệu = 150 tỉ; 7+7+7+9=30; 1e6 x 9/30 = 300 000 -> 3,0 s; chia đều 1e6/4/1e5 = 2,5 s; dư đầu đoạn [10,15,12,14] cuối 13; chi lương tuần tự 0,5/50/5 000 s (83,3 phút), khối 5/50 s; Kafka retention mặc định 7 ngày (168 h) đúng; ORA-00060 là mã bế tắc Oracle, Oracle huỷ CÂU LỆNH (không phải giao dịch) của một bên: đúng; quy tắc "ORDER BY + FOR UPDATE không bảo đảm thứ tự khoá" phù hợp tài liệu Oracle (chưa kiểm được nguồn chính thức bằng mạng); quiz A đúng, B/C/D sai đúng lý. Mã Python chạy khớp màn hình (cả hai lịch khoá).

## Điểm
P1=1 P2=2 P3=2 P4=2 P5=2 P6=2 P7=1 Tổng(P1-P7)=12 P8=2 P9=2. Mất gốc: ĐỦ (12, không mục nào 0).
Cần biết trước: dict.get có giá trị mặc định, sorted/append (từ khoá Python), khái niệm "tiến trình"/giao dịch cơ sở dữ liệu.
Chỗ thiếu chính: không có cú pháp BULK COLLECT/FORALL; logic `khoa.get(tk, ai) != ai`.
P1 = 1 (2 mục):
1. code step1: `if khoa.get(tk, ai) != ai:` — tham số thứ hai của .get (giá trị mặc định khi tài khoản chưa ai giữ) không được giảng; say chỉ nói "hàm xin khoá trả về được hoặc phải chờ ai".
2. symbol step1: `SELECT balance INTO v_bal FROM accounts WHERE account_no = r.acc` — `INTO v_bal` (đưa kết quả vào biến) và `r.acc` (cột của vòng lặp) không giảng (say chỉ nói "đọc số dư và khoá luôn dòng vừa đọc"). (ranh giới)

## Cảnh Tự làm
id `practice` ("Tự làm: sắp thứ tự khoá, kiểm vòng chờ và ghép số dư đầu đoạn"), pause 270 s; số khác ví dụ (khoá 7/3, 5 đoạn, 2 500 lệnh). Có kết quả mong đợi 6 dòng ở step2: CÓ, khớp mong_doi.txt từng dòng: KHỚP. Lưu ý: đề trên màn hình không nêu quy ước "tiến trình đang chờ không giữ thêm khoá" (chỉ có trong de.md) -> người học có thể ra "co" ở dòng 4 nếu cho B xin khoá hai; "Nếu kẹt" nói "A chờ B và B chờ A" nhưng không nêu quy ước này. Nhỏ.
## Cảnh quy mô
id `quymo` (3 step): ×1/×100/×10 000 = 100 / 10 000 / 1 000 000 lệnh: tuần tự 0,5 / 50 / 5 000 s, khối 1/10/100 -> 0,5/5/50 s; sao kê 1e4 / 1e6 / 1e8 bản ghi: 0,1 / 10 / 1 000 s -> 0,1 / 3 / 10 s; chỗ nghẽn còn lại: mọi lệnh trừ cùng tài khoản công ty (10 000 lần xếp hàng so với 1 nếu trừ tổng 150 tỉ). Đánh đổi có: số đoạn <= số phân vùng, ghép số dư tuần tự. Tính lại đúng (trừ SHOULD hàng ×10 000 nếu chia theo ngày).

## Lab
Tự làm được: CÓ, ~10 phút; đề đủ (de.md nêu rõ quy ước chờ); kẹt tiềm tàng: mô phỏng lịch xin khoá với "tiến trình đang chờ không giữ thêm khoá" (cần tự dựng từ điển giữ/chờ) — bài giảng code có sẵn khung. mong_doi khớp màn hình: KHỚP. cham.sh với lời giải tự viết: ĐÚNG; với loi_giai.py: ĐÚNG.

## Người học kẹt ở đâu
code step1: "if khoa.get(tk, ai) != ai:" (đối số mặc định của .get chưa giảng); ngoài ra symbol step1 nói về FOR UPDATE nhưng không kẹt vì có giải thích; không kẹt khác.

## Số tính lại / mã đã chạy / khung hình
Số tính lại 22 (150 tỉ; 7+7+7+9; 300 000 và 3,0/2,5 s; 13/24 cuối kỳ; 50 s/5 000 s/83,3 phút; 5 s/50 s; 1e8/1e5=1000; 10 s; 33,3 s; 168/24=7; lab 5 khối...) — 22/22 khớp (SHOULD hàng ×10 000 là diễn giải, không phải sai tính). Mã chạy: hai lịch khoá + ghép số dư khớp màn hình; lab 2 lần ĐÚNG. Oracle/PL/SQL chỉ đọc.
Khung hình: 00035.png (212 s, symbol PL/SQL), 00049.png (298 s, example step3 FORALL), 00073.png (450 s, mã ghép số dư), 00084.png (516 s, pitfall), 00096.png (593 s, quymo chỗ nghẽn trừ cùng tài khoản). Không lỗi hiển thị.

## Bảng sự kiện cần nhất quán
| Sự kiện | Giá trị | bài:cảnh |
|---|---|---|
| Quy mô ví dụ | 10 000 nhân viên, lương bình quân 15 triệu -> 150 tỉ/đợt; 10 khối x 1 000 | L05:prereq |
| Mục tiêu chi lương | 3 phút (ví dụ) | L05:hook |
| Mã lỗi Oracle bế tắc | ORA-00060 (Oracle huỷ câu lệnh đang chờ của một bên) | L05:hook, prereq, example |
| Bulk/Forall | 45 s -> ~1 s cho 10 000 lệnh (minh hoạ, "phải đo") | L05:example step3 |
| Kafka lưu mặc định | 7 ngày; sao kê 30 ngày cần giữ >= 30 ngày | L05:example step4, header |
| Tốc độ minh hoạ | 5 ms/lệnh mạng; 100 000 bản ghi/giây/tiến trình | L05:quymo |
| Sao kê 30 ngày | > 1 000 000 bản ghi; chia 7+7+7+9 | L05:example |
| Lương (tuyển dụng) | "Tin tuyển dụng ghi lương thương lượng" (khẳng định về tin ACB; chưa kiểm được nguồn ở bài này; nguồn ở L00/audit) | L05:recap |
| Core/NAPAS | Core Banking = hệ thống lõi giữ sổ; NAPAS = đơn vị chuyển mạch liên ngân hàng | L05:prereq |
| Debezium | CDC = đọc nhật ký thay đổi của CSDL | L05:prereq, concept |
| Văn bản pháp lý / tên người thật | không có | — |


## ACB L06 (sinh trắc học, QĐ 2345 / TT 50/2024)
sha16 YAML = d16ab77fd3ee0222 (khớp). 12 cảnh (hook, prereq, concept, symbol, example, code, check, pitfall, quymo, quiz, practice, recap); ~110 khung; 15,82 phút.

## Đối chiếu pháp lý (đã dùng WebSearch/WebFetch; nguồn đều thứ cấp/báo chí, KHÔNG phải văn bản gốc; còn lại ghi "chưa kiểm được nguồn")
- Thông tư 77/2025/TT-NHNN: ban hành 31/12/2025, hiệu lực 01/03/2026, sửa đổi bổ sung một số điều của Thông tư 50/2024 (luatvietnam.vn, tapchinganhang.gov.vn, vietnamplus) -> KHỚP bài ("hiệu lực 01/03/2026"). Nội dung sửa đổi tìm thấy: PAD chuẩn ISO 30107 cấp 2, chống root/jailbreak, thay đổi định danh, ghi nhớ mật khẩu; KHÔNG thấy nguồn nào nói Thông tư 77 đổi con số 10/20 triệu của cá nhân.
- Quyết định 2345/QĐ-NHNN: ngày 18/12/2023, hiệu lực 01/07/2024, thay QĐ 630/QĐ-NHNN (2017); giao dịch chuyển tiền trên 10 triệu/lần hoặc tổng trên 20 triệu/ngày phải xác thực sinh trắc học (nhiều báo: vnreview, luatvietnam, tapchicongthuong) -> KHỚP ngày/hiệu lực bài ghi (bài dùng "theo bài phỏng vấn đã lưu").
- Thông tư 50/2024/TT-NHNN: ký 31/10/2024, hiệu lực 01/01/2025; báo nói Phụ lục 02 quy định phương thức xác thực theo loại giao dịch và con số 10/20 triệu "bắt nguồn từ QĐ 2345"; một số báo nói chuyển khoản > 10 triệu/lần hoặc > 20 triệu/ngày của cá nhân cần HAI phương thức (sinh trắc + OTP/chữ ký/token), các nguồn không thống nhất -> bài đã ghi "nguồn thứ cấp nói còn điều kiện đi kèm, chưa kiểm". Số hiệu "bản hợp nhất 25/VBHN-NHNN" và "Công báo 1279+1280, 30-11-2024": KHÔNG tìm thấy bằng chứng web (chưa kiểm được nguồn).
- Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15: thông qua 26/6/2025, hiệu lực 01/01/2026 (nhiều nguồn) -> số hiệu bài ghi đúng; bài chỉ nêu "giảm thiểu dữ liệu" như khuyến nghị, nói rõ "chưa kiểm số điều" -> chấp nhận.
- Ngưỡng cho DOANH NGHIỆP từ 01/07/2026 (báo): ABBank/TPBank nêu 10 triệu/20 triệu cho hộ KD/DN giản đơn, 50 triệu/100 triệu cho DN mới thành lập (<12 tháng) — bài chỉ nói cá nhân, không nhắc doanh nghiệp (không sai; có thể gây nhầm nếu INT nói cùng ngưỡng cho DN).

## Phần A
| Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng | Đề xuất | Tin cậy |
|---|---|---|---|---|---|
| SHOULD | tiêu đề bài, objective 1, recap vs hook | tiêu đề: "Xác thực Sinh trắc học theo Thông tư 50/2024"; objective 1: "theo Thông tư 50/2024 đã sửa đổi"; recap: "ngưỡng sinh trắc học theo văn bản đã sửa đổi" | Chính hook nói "phụ lục chứa con số 10 và 20 triệu sau sửa đổi: chưa đối chiếu". Báo (vnreview, luatvietnam) gắn 10 triệu/20 triệu với QĐ 2345 (hiệu lực 01/07/2024); không tìm thấy nguồn nói Thông tư 50 hoặc Thông tư 77 TỰ đặt con số này. Tiêu đề/mục tiêu khẳng định mạnh hơn phần hedge. | Đổi tiêu đề/mục tiêu thành "ngưỡng 10/20 triệu (nêu trong QĐ 2345 và được dẫn trong phụ lục TT 50)" hoặc thêm "chưa đối chiếu" vào mục tiêu | PLAUSIBLE (chỉ có nguồn thứ cấp) |
| SHOULD | symbol step2; pitfall; objective 3 | "Vé có thời hạn hiệu lực tối đa 3 phút và chỉ dùng một lần"; "hết hạn sau 3 phút" | Không có nguồn pháp lý; header nói "thời gian ... là số minh hoạ" nhưng cảnh symbol/pitfall không gắn nhãn "ví dụ thiết kế" -> người học dễ tưởng là quy định. | Thêm "(ví dụ thiết kế, không phải quy định)" | CONFIRMED (thiếu nhãn) |
| SHOULD | code step3-4 + practice | `if ve["ky"] != ky(nd):` | So sánh chữ ký bằng != không hằng-thời-gian; thực tế phải dùng hmac.compare_digest (tài liệu Python hmac) để tránh tấn công đo thời gian. Chữ ký rút 8 ký tự hex (32 bit) bài nói "cho gọn" là mô phỏng; không nói rõ không dùng như vậy ngoài thực tế. | Thêm một câu "thực tế dùng compare_digest, chữ ký đủ dài" | CONFIRMED (khuyến nghị chuẩn) |
| SHOULD | hook, prereq | "...khớp dữ liệu đã đối chiếu chip căn cước (hoặc VNeID)" | Chỉ nêu một yếu tố; một số báo nói cá nhân trên ngưỡng cần thêm phương thức thứ hai (OTP/chữ ký) theo Phụ lục 02. Bài đã ghi "một nguồn thứ cấp nói còn điều kiện đi kèm ... chưa kiểm" -> đã hedge; chỉ ghi để điều phối so với INT. | giữ nguyên | PLAUSIBLE (nguồn không thống nhất) |
Không có MUST. Đã tính lại: 8+14=22, 9+8+6=23; 5/500/50 000 x 0,3 = 1,5/150/15 000; x180 = 900/90 000/9 000 000; 50 000 x 60 = 3 000 000; epoch 1730948400 = 2024-11-07 03:00 UTC (khớp thời kỳ tài liệu, không dùng tính toán); HMAC mô phỏng và 4 lần kiểm vé chạy khớp màn hình.

## Điểm
P1=1 P2=2 P3=2 P4=2 P5=2 P6=2 P7=2 Tổng(P1-P7)=13 P8=2 P9=2. Mất gốc: ĐỦ.
Cần biết trước: Unix timestamp (số giây), VNeID, HMAC/băm (có giảng ngắn).
Chỗ thiếu chính: không giải thích `expires_at: 1730948400` (giây Unix) và VNeID.
P1 = 1 (2 mục):
1. hook step1: "(hoặc VNeID)" — không giảng VNeID là gì (ứng dụng định danh điện tử).
2. symbol step2: `"expires_at": 1730948400` — số giây từ 1/1/1970 không giải thích (phần code sau lại dùng "hạn 180 giây" tương đối, người học không biết 1730948400 là gì).

## Cảnh Tự làm
id `practice` ("Tự làm: ngưỡng cộng dồn trong ngày và kiểm vé một lần"), pause 270 s; số khác ví dụ (6,7,9,15,3; vé x7/30/240; 4 lần kiểm). Có kết quả mong đợi 9 dòng step2: CÓ; khớp mong_doi.txt: KHỚP.
## Cảnh quy mô
id `quymo`: ×1 / ×100 / ×10 000 = 5 / 500 / 50 000 lượt quét mỗi giây; đang so khớp 1,5 / 150 / 15 000; vé còn hạn tối đa 900 / 90 000 / 9 000 000; chọn: 1 máy -> Redis dùng chung -> chia theo mã khách; đánh đổi hạn vé 180 s (9 triệu vé) vs 60 s (3 triệu vé, khách chậm phải quét lại). Tính lại ĐÚNG.

## Lab
Tự làm được: CÓ, ~10 phút; đề đủ (de.md nêu thứ tự cổng, cách lấy 8 ký tự hex; khoá tự chọn). Có thể kẹt nhẹ: `hmac.new(key, msg, hashlib.sha256)` — được dạy ở code step2. mong_doi khớp màn hình: KHỚP. cham.sh với lời giải tự viết: ĐÚNG; với loi_giai.py: ĐÚNG. Đề không thử mốc đúng bằng 10 hoặc đúng 20 (không kiểm điều kiện biên) — thiếu một ca biên.

## Người học kẹt ở đâu
hook step1: "(hoặc VNeID)" (VNeID chưa giảng); symbol step2: `"expires_at": 1730948400` (số giây Unix không giải thích). Còn lại không kẹt.

## Số tính lại / mã đã chạy / khung hình
Số tính lại 16 (22; 23; 1,5/150/15 000; 900/90 000/9 000 000; 3 000 000; epoch; ngưỡng 10/20; lab 5 dòng ngưỡng; 4 dòng vé) — 16/16 khớp. Mã chạy: cổng ngưỡng 4 giao dịch và vé HMAC bốn lần (khớp màn hình); lab 2 lần ĐÚNG.
Khung hình: 00004.png (25 s, slide pháp lý hook), 00009.png (66 s, bảng thách thức), 00030.png (197 s, bảng công nghệ), 00053.png (328 s, bước 4 450 ms), 00083.png (497 s, pitfall). Hook là khung rất nhiều chữ (đoạn đỏ 7 dòng) nhưng đọc được, không tràn; không lỗi hiển thị.

## Bảng sự kiện cần nhất quán (QUAN TRỌNG khi so với INT)
| Sự kiện | Giá trị trong bài | bài:cảnh | Đối chiếu |
|---|---|---|---|
| Ngưỡng sinh trắc học (cá nhân) | > 10 triệu/lần HOẶC tổng ngày > 20 triệu | L06:hook, prereq, code, practice, recap | khớp báo về QĐ 2345; bài ghi "trên 10" (báo có nơi viết "từ 10 triệu": biên chưa kiểm) |
| Văn bản gắn ngưỡng | "theo Thông tư 50/2024 đã sửa đổi"; QĐ 2345 "chưa đọc nguyên văn, chưa rõ còn áp dụng" | L06:tiêu đề, hook | báo gắn với QĐ 2345 (2024) |
| QĐ 2345/QĐ-NHNN | ngày 18/12/2023, hiệu lực 01/07/2024 | L06:hook | khớp nguồn thứ cấp |
| Thông tư 50/2024/TT-NHNN | bài KHÔNG nêu ngày ký/hiệu lực; header: Công báo 1279+1280 30-11-2024 | L06:header | web: ký 31/10/2024, hiệu lực 01/01/2025 |
| Thông tư 77/2025/TT-NHNN | hiệu lực 01/03/2026; bản hợp nhất 25/VBHN-NHNN | L06:hook, header | hiệu lực khớp (ban hành 31/12/2025); số VBHN chưa kiểm được |
| Luật BVDLCN | 91/2025/QH15 (khuyến nghị giảm thiểu dữ liệu, chưa số điều) | L06:symbol | số hiệu đúng (26/6/2025, hiệu lực 01/01/2026) |
| Quy tắc cộng dồn | sau quét mặt tổng về 0 = GIẢ ĐỊNH của mô phỏng, không phải điều khoản | L06:prereq, code, practice | giữ nhãn nhất quán; INT phải không nói như luật |
| Hạn vé / điểm khớp | 3 phút (180 s); ngưỡng khớp > 0,85; 0,965 (minh hoạ) | L06:symbol, example, pitfall | thiết kế minh hoạ |
| Giao dịch ví dụ | 50 triệu (cùng số với L03:check và INT?) | L06:example | — |
| Mã HTTP | 403 Forbidden khi thiếu vé | L06:check | — |
| Thời gian xử lý | ~450 ms phía máy chủ (minh hoạ) | L06:example | — |
| Quy mô | 5 / 500 / 50 000 lượt/giây; 0,3 s/lượt | L06:quymo | — |


## ACB L07
sha16 YAML = 4bf6f78d6e3ff3ba (khớp). 12 cảnh (hook, prereq, concept, symbol, example, code, check, pitfall, quymo, quiz, practice, recap); ~115 khung; 16,65 phút. Bài không dẫn văn bản pháp lý nào (không có QĐ 2345/TT 50/TT 77/Luật 91).

## Phần A
| Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng | Đề xuất | Tin cậy |
|---|---|---|---|---|---|
| SHOULD | quymo step1 so với example step4 | quymo: "sắp xếp + trộn ... 64 549 593 ... 0,065 giây" ; example step4: "mục tiêu ví dụ: phân loại xong sai lệch trong 180 giây" (cùng N = 3 000 000) | Hai thời gian cho cùng việc cách nhau ~3 000 lần (0,065 s so với 180 s) mà bài không giải thích. 0,065 s chỉ là số phép so/10^9, chưa gồm sắp xếp 3 nguồn x 3 triệu dòng, đọc tệp, ghi kết quả. Người học dễ hiểu "đối soát 3 triệu dòng mất 0,065 giây". Tính lại: 3e6*log2(3e6)/1e9 = 0,0645. | Ghi "chỉ tính phép so, chưa tính đọc/sắp xếp/ghi" ở hàng ×10 000 | CONFIRMED (hai số trong bài) |
| SHOULD | code step1 + practice | `print(chu_ky == ky(goi))`; lab: "True nghĩa là mã tính lại bằng mã đã đính kèm" | So sánh bằng == không hằng-thời-gian; thực tế phải dùng hmac.compare_digest (tài liệu Python hmac); mã rút 12 ký tự hex (48 bit) chỉ là mô phỏng. Cùng điểm với L06. | Thêm một câu nhắc compare_digest | CONFIRMED (khuyến nghị chuẩn) |
| SHOULD | pitfall | "So tiền tố LIKE '8888%' trên cột có chỉ mục B-Tree" | Đúng với Oracle/MySQL; trên PostgreSQL với collation không phải C cần lớp toán tử text_pattern_ops (hoặc chỉ mục varchar_pattern_ops) mới dùng được chỉ mục cho LIKE tiền tố. Bài không nêu điều kiện. | Thêm "tuỳ hệ quản trị, có thể cần kiểu chỉ mục tiền tố" | PLAUSIBLE (chưa chạy PostgreSQL) |
| SHOULD | hook step1 so với example step4 | hook: "hàng trăm nghìn đơn hàng"; example: "Core Banking Ledger 3 000 000 dòng" | Quy mô hook (trăm nghìn/ngày) và ví dụ đối soát (3 triệu dòng mỗi nguồn) lệch 10 lần mà không nói đó là tổng nhiều đối tác. | Ghi "3 triệu = tổng mọi đối tác của ngân hàng" | PLAUSIBLE |
Không có MUST. Đã kiểm: ma trận đối soát và nhãn khớp mong_doi; hai con trỏ chạy (3 chi co o B, con lai [] []) khớp màn hình; HMAC True/False khớp; N^2 = 9e4 / 9e8 / 9e12; /1e9 = 9e-5 / 0,9 / 9 000 s = 2,5 giờ; N log2 N = 2 469 / 446 180 / 64 549 593 (khớp bảng); 4+8 = 12 chữ số VA; T24 FUNDS.TRANSFER là application thật; hash join / sort-merge join mô tả đúng; quiz A đúng, B/C/D sai đúng lý.

## Điểm
P1=1 P2=2 P3=2 P4=2 P5=2 P6=2 P7=2 Tổng(P1-P7)=13 P8=2 P9=2. Mất gốc: ĐỦ.
Cần biết trước: idempotent/idempotency (khoá acb_idem), UNIQUE constraint, tập (set) Python.
Chỗ thiếu chính: thuật ngữ "EOD" và "Idempotent" xuất hiện trên màn hình mà không có câu giải nghĩa tại chỗ.
P1 = 1 (2 mục):
1. hook step2 (bảng + câu "Hôm nay, ta làm chủ: ... Webhook Idempotent, và Đối soát 3 bên EOD") và concept step3 ("3-Way EOD Reconciliation Matrix"): "EOD" không giải là End Of Day (chỉ gần chữ "cuối ngày" nhưng không nối).
2. hook step2: "Webhook Idempotent" — chỉ định nghĩa theo hành vi ở check step2 ("trả 200 OK mà không cập nhật số dư lần hai"), không bao giờ định nghĩa từ "idempotent/idempotency".

## Cảnh Tự làm
id `practice` ("Tự làm: HMAC, nhận webhook theo mã sự kiện và đối soát ba nguồn"), pause 270 s; số khác ví dụ (khoá khoa-lab-07, e1..e3, ba danh sách mã). Có kết quả mong đợi 13 dòng ở step2: CÓ; khớp mong_doi.txt từng dòng: KHỚP. Đề trên màn hình không nhắc "lấy 12 ký tự hex" (chỉ có trong de.md và code step1); nhãn phân loại nằm ở cảnh concept step4 ("cũng là nhãn của bài tự làm").
## Cảnh quy mô
id `quymo`: ×1/×100/×10 000 = N 300 / 30 000 / 3 000 000; vòng lặp lồng nhau 9e4 / 9e8 / 9e12 phép = 0,00009 s / 0,9 s / 9 000 s (2,5 giờ); sắp xếp+trộn 2 469 / 446 180 / 64 549 593 = 2,5 µs / 0,45 ms / 0,065 s; step2 theo thời gian: mã sự kiện nhớ 24 giờ, DLQ phát lại sau 3 ngày lọt -> cần ràng buộc duy nhất lâu dài; dữ liệu lớn hơn bộ nhớ -> chia khoảng. Tính lại ĐÚNG (SHOULD về nhãn 0,065 s).

## Lab
Tự làm được: CÓ, ~12 phút; đề đủ (de.md nêu cả công thức HMAC và bảng nhãn); kẹt tiềm tàng: thứ tự ưu tiên khi một mã thoả nhiều điều kiện nhãn (mã 16 chỉ ở ERP -> bat thuong; mã chỉ ở Core+ERP -> lỗi chuyển tiền) — de.md đã định nghĩa. mong_doi khớp màn hình: KHỚP. cham.sh với lời giải tự viết: ĐÚNG; với loi_giai.py: ĐÚNG.

## Người học kẹt ở đâu
hook step2: "Webhook Idempotent, và Đối soát 3 bên EOD" (hai thuật ngữ chưa giải); các cảnh sau không kẹt.

## Số tính lại / mã đã chạy / khung hình
Số tính lại 19 (12 chữ số VA; 3 tập đối soát; 9e4/9e8/9e12; 0,00009/0,9/9 000 s; 2,5 giờ; 2 469/446 180/64 549 593; 0,065; 21,5; 6,5e7...) — 19/19 khớp. Mã chạy: HMAC (True/False), hai con trỏ (3 chi co o B), webhook set; lab 2 lần ĐÚNG.
Khung hình: 00026.png (149 s, nhãn phân loại), 00033.png (193 s, gói webhook), 00055.png (336 s, ví dụ con trỏ ba nguồn), 00088.png (517 s, bảng quymo), 00099.png (591 s, quiz). Không lỗi hiển thị (bảng quymo 6 cột vẫn đọc được; chưa xem riêng khung cảnh Tự làm).

## Bảng sự kiện cần nhất quán
| Sự kiện | Giá trị | bài:cảnh |
|---|---|---|
| Số VA | 12 chữ số = tiền tố đối tác 4 (8888) + mã đơn 8; 888800123456 | L07:prereq |
| Khoá khử trùng lặp giao dịch | SET va:dedup:TXN_8888 NX EX 120 (120 s) | L07:example step1 |
| Khoá/mã sự kiện webhook | chỉ nhớ 24 giờ trong Redis; DLQ phát lại sau 3 ngày lọt | L07:quymo step2 (so L03: khoá 24h = 86 400 s; L02/L00 TTL) |
| Thử lại | Exponential Backoff 1, 2, 4 giây; sau 3 lần -> DLQ | L07:check |
| HMAC | HMAC-SHA256, header X-Signature, X-Event-ID (tên là ví dụ thiết kế); khoá chung, KHÔNG phải chữ ký số | L07:symbol |
| Thời gian ghi Có | 35 ms (mục tiêu <= 100 ms); cả bước ~80 ms | L07:example step2 |
| Đối soát EOD | 23 giờ, 3 000 000 dòng/nguồn, mục tiêu 180 s | L07:example step4 |
| VA tĩnh/động | động hết hạn 15 phút hoặc 24 giờ (ví dụ) | L07:concept |
| Core | T24 FUNDS.TRANSFER = kiến trúc tham chiếu OCB, ACB không nêu core | L07:example step2 |
| Nhãn đối soát | MATCHED / rot webhook / treo ghi co / loi chuyen tien NAPAS / bat thuong | L07:concept, practice |
| Số tiền ví dụ | 1 000 000 đ, ORD_9999 | L07:example |
| Văn bản pháp lý / lương / người thật | không có | — |


## ACB L08
sha16 YAML = 8ff9af055621b299 (khớp). 12 cảnh (hook, prereq, concept, symbol, example, code, check, pitfall, quymo, quiz, practice, recap; recap có 2 step); ~115 khung; 16,35 phút.

## Đối chiếu pháp lý (WebSearch; nguồn thứ cấp)
- Thông tư 31/2024/TT-NHNN, Điều 10 khoản 1 điểm b: nợ nhóm 2 = nợ cần chú ý, quá hạn 10-90 ngày (+ một số trường hợp điều chỉnh kỳ hạn lần đầu, khoản 2-3 Điều 10); hiệu lực 01/7/2024, thay Thông tư 11/2021 (luatvietnam, lawnet, hethongphapluat) -> KHỚP lời bài ("định nghĩa rút gọn ... còn có trường hợp điều chỉnh kỳ hạn", "5 nhóm").
- Thông tư 37/2025/TT-NHNN ngày 31/10/2025 sửa đổi bổ sung một số điều của Thông tư 31/2024 (thuvienphapluat, luatvietnam; hiệu lực 15/12/2025 theo một nguồn; có VBHN 27/2025) -> KHỚP "TT 37/2025 sửa đổi". Tôi chưa xác nhận Thông tư 37 có đổi Điều 10 (nhóm 2) hay không (chưa kiểm được) — bài đã ghi "cần đối chiếu bản hợp nhất".
- "Công báo 825+826, 21-7-2024": chưa kiểm được nguồn. CIC = Trung tâm Thông tin tín dụng Quốc gia Việt Nam thuộc NHNN: đúng.
- Chính sách "nhóm 2 trở lên không duyệt tự động": bài gắn nhãn chính sách ví dụ/giả định ở hook, prereq, quiz, mục tiêu 5 -> đúng cách.

## Phần A
| Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng | Đề xuất | Tin cậy |
|---|---|---|---|---|---|
| SHOULD | example step3 (bảng 4 bước), symbol step2, pitfall | bảng: "1. Khoá sổ -> 2. Ký số -> 3. Mở hạn mức"; objective 2: "nhả khoá nếu bước hai hỏng" | Luồng thật có 3 bước nhưng mã chỉ xử lý lỗi ở bước cấp hạn mức. Nếu khách bỏ dở hoặc ký số thất bại/hết hạn SAU khi sổ đã khoá (bước 2), sổ vẫn bị phong tỏa; bài không nói nhả khoá, hạn chờ ký, hay thứ tự nên ký trước khoá. Lỗ hổng thiết kế (khách kẹt tiền), đúng loại lỗi mà bài dạy tránh. | Thêm một dòng "ký lỗi/hết hạn -> nhả khoá sổ" | PLAUSIBLE (suy luận từ luồng bài) |
| SHOULD | concept step1 (mục tiêu 4) | mục tiêu 4: "Mô tả luồng LOS, ký số Cloud CA và tra cứu Cổng CIC qua mTLS"; covers: objective 4 -> scene concept | Chỉ có nhãn trên sơ đồ ("Tra cứu Cổng CIC B2B", "Ký số Cloud CA") và vài câu say; không có cảnh nào chạy từng bước gọi CIC hay giải thích mTLS ở đây (chỉ dựa khoá L06). Bảng 4 bước ví dụ (example step3) không có bước tra CIC dù recap đặt CIC trước phong tỏa. Giáo án hứa nhiều hơn bài dạy. | Thêm bước "0. Tra CIC" vào bảng 4 bước | CONFIRMED (đối chiếu mục tiêu và cảnh) |
| SHOULD | quymo step1 | "lượt tra CIC mỗi giây ... 278" (×10 000), "hàng trăm lượt tra CIC" | 1 000 000 hồ sơ/giờ / 3 600 = 277,8/s là trung bình đều; giờ cao điểm sẽ cao hơn nhiều (bài không nói), đúng lỗi "sizing theo trung bình" như L03. | Thêm "(trung bình, đỉnh cao hơn)" | PLAUSIBLE |
| SHOULD | quymo step1 | "thất thoát nếu không có khoá lũy đẳng ... 50 tỉ đồng" | Là giá trị kỳ vọng nếu MỌI lệnh gửi lại đều thành chi trùng; bài đã ghi "tiềm ẩn" và "(số minh hoạ)" -> chấp nhận; ghi chú để điều phối. | giữ nguyên | CONFIRMED (đã gắn nhãn) |
Không có MUST. Đã tính lại: 100 000 000 x 85% = 85 000 000; 6+2,5 = 8,5; 50e6 x 8,5% x 30/365 = 349 315,07 (làm tròn 349 315); lab 240e6 x 80% = 192 000 000, 4,8+2,7 = 7,5, 120e6 x 7,5% x 45/365 = 1 109 589,04; quymo CIC/giây 0,028 / 2,78 / 277,8; trùng 0,1 / 10 / 1 000 lệnh; thất thoát 5 triệu / 500 triệu / 50 tỉ; hai pha và sqlite PRIMARY KEY (lan 1 chi tien / lan 2 trung khoa) chạy khớp màn hình; mã Go chỉ đọc. Quiz B đúng (A/C/D sai đúng lý); khoản "bán cấn trừ" (check C) hợp lý.

## Điểm
P1=1 P2=2 P3=2 P4=2 P5=2 P6=2 P7=2 Tổng(P1-P7)=13 P8=2 P9=2. Mất gốc: ĐỦ.
(P7=2 dù SHOULD mục tiêu 4: lệch nhỏ, có thể hạ xuống 1 nếu điều phối chặt: khi đó Tổng=12 vẫn ĐỦ.)
Cần biết trước: mTLS, idempotency/"lũy đẳng" (từ khoá trước), ý niệm "context" trong Go.
Chỗ thiếu chính: `ctx` trong mã Go; thuật ngữ "lũy đẳng".
P1 = 1 (2 mục):
1. symbol step2: `t24.LockDepositAccount(ctx, depositAccNo, holdAmount)` — tham số `ctx` (Go context) không giảng; chú thích chỉ nói hàm trả hai giá trị, err != nil.
2. code step3 / pitfall / tiêu đề: "khoá lũy đẳng / giải ngân lũy đẳng" — thuật ngữ "lũy đẳng" (idempotent) chỉ được mô tả bằng hành vi (khoá chính, lần hai bị bỏ qua), không có câu định nghĩa từ.

## Cảnh Tự làm
id `practice` ("Tự làm: hạn mức, phong tỏa hai pha, nhóm nợ CIC và giải ngân lũy đẳng"), pause 300 s; số khác ví dụ (240 triệu, 80%, 4,8+2,7, 120 triệu/45 ngày, K7). Có kết quả mong đợi 8 dòng: CÓ; khớp mong_doi.txt: KHỚP. Chi tiết định dạng ("hai pha: khoa so,cap han muc loi: nha khoa so" nối bằng dấu phẩy không cách) chỉ thấy ở màn hình mong đợi và de.md.
## Cảnh quy mô
id `quymo`: ×1/×100/×10 000 = 100 / 10 000 / 1 000 000 hồ sơ mỗi giờ; tra CIC 0,03 / 2,8 / 278 lượt/giây; lệnh gửi lại 0,1 / 10 / 1 000; thất thoát tiềm ẩn 5 triệu / 500 triệu / 50 tỉ; chọn: làm tay -> hàng đợi + khoá lũy đẳng -> + UNIQUE + nhớ tạm CIC + giới hạn tốc độ; step2 theo thời gian: nhóm nợ đổi theo ngày (quá hạn 9 ngày nhóm 1, 10 ngày nhóm 2), kết quả CIC chỉ đúng lúc tra. Tính lại ĐÚNG.

## Lab
Tự làm được: CÓ, ~10 phút, không kẹt (de.md đủ; chú ý in `7.5` chứ không `7.50`: float 4.8+2.7 = 7.5 đúng). mong_doi khớp màn hình: KHỚP. cham.sh với lời giải tự viết: ĐÚNG; với loi_giai.py: ĐÚNG.

## Người học kẹt ở đâu
symbol step2: "t24.LockDepositAccount(ctx, depositAccNo, holdAmount)" (`ctx` chưa giảng); ngoài ra không kẹt.

## Số tính lại / mã đã chạy / khung hình
Số tính lại 15 (85 000 000; 8,5; 349 315; 192 000 000; 7,5; 1 109 589; 0,028/2,78/277,8; 0,1/10/1 000; 5 triệu/500 triệu/50 tỉ; 90 000 000...) — 15/15 khớp. Mã chạy: Python công thức + hai pha + sqlite PRIMARY KEY khớp màn hình; lab 2 lần ĐÚNG.
Khung hình: 00016.png (104 s, bảng 4 khái niệm), 00029.png (186 s, công thức), 00051.png (329 s, mã hai pha), 00063.png (395 s, check cấn trừ), 00082.png (516 s, quiz). Không lỗi hiển thị (chưa xem riêng khung bảng quymo và cảnh Tự làm).

## Bảng sự kiện cần nhất quán
| Sự kiện | Giá trị | bài:cảnh |
|---|---|---|
| Thông tư 31/2024/TT-NHNN | phân loại nợ 5 nhóm; Điều 10: nhóm 2 = quá hạn 10-90 ngày (rút gọn, + điều chỉnh kỳ hạn); Công báo 825+826 21-7-2024 (chưa kiểm) | L08:header, hook, quiz |
| Thông tư 37/2025/TT-NHNN | ngày 31/10/2025 sửa đổi TT 31/2024; "cần đối chiếu bản hợp nhất" | L08:header, hook, quiz |
| Chặn duyệt tự động | nhóm nợ >= 2 = CHÍNH SÁCH VÍ DỤ, không phải quy định | L08:hook, quiz, practice |
| LTV | 85% (ví dụ; quiz 90%; lab 80%) | L08:prereq, symbol, quiz, practice |
| Lãi | gửi 6% + biên độ 2,5% = 8,5%/năm; 365 ngày/năm (giả định); 50 triệu x 30 ngày = 349 315 đ | L08:symbol, example |
| Ví dụ sổ | 100 triệu, hạn mức 85 triệu, phong tỏa 100 triệu | L08:hook, example |
| Bội số lương | 2 đến 3 lần (tuỳ chính sách) | L08:concept |
| Giải ngân lệnh trùng | 0,1% gửi lại; 50 triệu/lệnh | L08:quymo |
| Core | T24 AZ/CASA = kiến trúc tham chiếu OCB; Squad Lending = nhóm ở OCB; ACB không nêu core | L08:hook, concept |
| Vai trò JD | "giữ một mảng nghiệp vụ ... hỗ trợ sự cố mức 3" (bản lưu, chưa kiểm lại) | L08:recap step2 |
| CIC | Trung tâm Thông tin tín dụng Quốc gia thuộc NHNN | L08:hook |
| Chữ ký số đám mây | "văn bản chưa đọc nguyên văn nên không nêu số hiệu" | L08:prereq |
| Lương/tên người thật | không có | — |

