# WP5 — nâng khoá DMS (Toán rời rạc) lên chuẩn AF2 — báo cáo

## Tiến độ
- Phiên 1 (2026-11-14): L00–L11. Phiên 2 (cùng ngày): L12–L20. **Cả 21/21 bài** đã `af2: true` + `covers` + cảnh `practice` + lab `labs/DMS/L00..L20` + (L00–L19) cảnh `quymo` quy mô/thời gian; L20 là bài hành trình, đã có sẵn trục thời gian năm chặng.
- Lời đọc: mọi bài ≤ 2 300 từ (bộ kiểm kiểm). L20 cắt từ 3 192 xuống 2 261 từ.

## Cổng cuối phần cho cả 21 bài (chạy thật, `bash audit/dms/af2/final_gates.sh`)
| Cổng | Kết quả (2026-11-14) |
|---|---|
| `tools/lv.py lint` L00–L20 | 21/21 bài: 0 FAIL, 0 WARN (30–43 PASS mỗi bài) |
| `tools/lv.py render` L00–L20 | 0 vấn đề mỗi bài (mỗi bài render lại sau lần sửa cuối; L00, L01, L03, L04 render lại sau khi sửa đoạn "bài sau" ở recap) |
| `audit/dms/verify_dms.py` | 323 PASS, 0 FAIL (21 lab tính lại độc lập, 22 cặp mã–kết quả chạy thật, con số quy mô, hợp đồng AF2) |
| `audit/review/lab_gate.py DMS` | 21 PASS, 0 FAIL |
| `tools/lv.py curriculum curriculum/dms.yaml` | 21 bài, 21 có đặc tả, 0 lỗi |
| `audit/check_curricula_graph.py` | không chu trình, tham chiếu hỏng 0; mục 2 chỉ báo WEB:L04 FAIL (khoá khác, ngoài phạm vi); không có lỗi DMS |
| `tests/test_e52.py` | 0 FAIL |
| `audit/review/screen_code.py check --course DMS` | 72 khối bài, PASS 95 (gồm nguồn), 0 FAIL/STALE/MISSING/ORPHAN |
| `audit/review/arith_scan.py` | 243 phép tính, 0 FAIL |

## Việc đã làm với mỗi bài
1. **Cảnh `quymo` (P9)**: mã Python ≤ 12 dòng chạy thật ở ≥ 2 cỡ n + kết quả thật hiện kèm, rồi bảng ×100/×10 000 và đánh đổi. Số suy ra từ "một tỉ phép mỗi giây" đều ghi "số minh hoạ". Chủ đề: L00 bảng chân trị 2ⁿ; L01 thử ngẫu nhiên bỏ sót lỗi biên; L02 hai lượng từ lồng nhau n²; L03 thử từng cặp vs chứng minh; L04 n phép cộng vs công thức đã chứng minh; L05 duyệt từng số vs bao hàm–loại trừ; L06 va chạm bảng băm vs cận chuồng bồ câu; L07 kiểm bắc cầu n³ vs gom lớp; L08 thử mọi hàng n! vs chọn từng phần tử; L09 PIN và mật khẩu 62ⁿ; L10 so mọi cặp n²; L11 chia kẹo, số hộp tăng; L12 liệt kê hoán vị n! vs bao hàm–loại trừ; L13 thử từng ước vs Euclid (cặp liên tiếp của dãy chậm nhất: 88 bước vs 1,8×10¹⁸ phép); L14 nhân từng lần vs bình phương liên tiếp; L15 chia thử phân tích n (√n); L16 kiểm Euler bằng bậc vs thử mọi thứ tự đỉnh (n−1)!/2; L17 thử từng tập cạnh vs công thức Cayley; L18 tô màu tham lam phí gấp n/2 lần ở thứ tự xấu; L19 số khoá để va chạm ≈ 1,18√m; L20 hành trình (trục thời gian 2004→2030).
2. **Cảnh `practice` + lab** (`de.md`, `mong_doi.txt`, `loi_giai.py`): số liệu khác ví dụ; `mong_doi.txt` = đầu ra thật của lời giải; mọi dòng hiện trên màn hình; step 1 có `pause`; chấm bằng `labs/cham.sh`.
3. **Mục tiêu + `covers` (E51)** + `curriculum/dms.yaml` đồng bộ (và `requires_ext: [PYT:L00..L03]`, L19 còn `CS115:L13`). Mục tiêu động từ LÀM mà bài không dạy bằng cảnh ví dụ được viết lại đúng điều video dạy: L00 ("Nêu vì sao"), L03, L08, L10, L12, L15, L17 ("Nêu cách/vì sao …").
4. **P1/E52**: 13 mục `term:` trong `tools/registry/symbols.DMS.yaml` (mệnh đề, bảng chân trị, tương đương, De Morgan, phản đảo, phản ví dụ, vị từ, lượng từ, định lý, giả thiết, quy nạp, giả thiết quy nạp, tập hợp); giảng tại chỗ thêm: phản ví dụ (L01), định lý/giả thiết/kết luận (L03), "n giai thừa" (L08 và L16, nơi cảnh quy mô dùng n! trước khi L09 dạy), bội (L05); đoạn "bài sau" ở recap L00/L01/L04 viết lại để không dùng thuật ngữ chưa giảng.
5. Lỗi thật do bộ kiểm độc lập bắt được trong lúc làm (không lọt vào bài): L14 lab `6^100 mod 19` lệch hai cách tính (sửa), số ngày dò mật khẩu 12 ký tự (L09), số năm và số chữ số của 100!/2 (L16) đoán sai (`checks` của lint bắt).

## Công cụ (để tiếp, hoặc dựng lại)
- `audit/dms/af2/af2lib.py` + `audit/dms/af2/lNN.py` (L00–L20): vá TÁI CHẠY ĐƯỢC từ bản gốc chép ở `audit/dms/af2/base/`; giữ CRLF của bài/giáo án/sổ; L08, L16, L17, L18 vá MẪU `audit/dms/src/*.tpl.yaml` rồi ghép hình bằng `fill()` (đã kiểm: ghép lại mẫu gốc cho đúng bài gốc). L20 (bài hành trình, YAML viết tay) vá bằng nạp–sửa–ghi lại cấu trúc (mất các dòng chú thích tiêu đề cảnh; giữ khối chú thích quy ước đầu tệp).
- `audit/dms/verify_dms.py` + `audit/dms/vparts/lNN.py`: (A) tính lại từng dòng `mong_doi.txt` bằng cách KHÁC lời giải (phép bit, Fraction, sympy, đệ quy, quy hoạch động, liệt kê tập…) + chạy `loi_giai.py`; (B) chạy nguyên văn từng cặp (mã, kết quả) của cảnh `quymo` và tính lại số quy mô; (C) hợp đồng AF2 (covers phủ đủ, practice trước recap, lời đọc ≤ 2 300, mục tiêu giáo án = bài, không "như đã học ở khoá").
- `audit/dms/af2/final_gates.sh`: chạy lint + render 21 bài và các cổng cấp khoá.
- Sổ `audit/review/screen_code/DMS.yaml`: thêm mục cho mọi khối mã mới (`run` + `expect_stdout`; `output of:`; khối kết quả mong đợi của practice là `output of: src:DMS:Lxx_lab`).
- Bài học kỹ thuật: heredoc của Bash làm hỏng `\\`, `\n` trong chuỗi Python (ba lần phải sửa bằng Edit); dòng mã trên màn hình dài quá ~110 ký tự bị cắt phải; khung mã cỡ 10 dòng + 3 dòng kết quả đã tràn, nên cảnh quy mô giữ mã ≤ 10 dòng và kết quả ≤ 2–3 dòng.

## Điểm cần người đọc độc lập / điều phối chú ý
- Câu `say` mới/đổi chưa qua máy nghe (ASR); chữ cái đứng riêng (p, q, n, x) và số lớn đọc bằng chữ cần nghe. Mục `asr_reviewed` đã xoá các câu không còn: L03 (một), L20 (các câu bị cắt).
- **L20 cắt**: bỏ câu (và mục `focus` tương ứng) ở hook, prereq, sym, stage1–5, check, pitfalls, quiz, recap; bỏ hẳn ba step: `prereq` step 2 (quy tắc lũy thừa của 2), `stage2` step 2 (hai con số 4 năm/1796 ngày; `checks` vẫn còn), `stage3` step 3 (bảng quy mô tính toán 6 500 năm máy). Các sự kiện/ số bị cắt khỏi lời đọc vẫn còn trên màn hình ở bảng của từng chặng. Nếu muốn khôi phục đầy đủ, nên tách bài (đề xuất: chặng 1–3 là một bài, chặng 4–5 + quyết định là bài cuối), không tự tách trong phiên này.
- Lab đều là Python; bài lý thuyết thuần (L03) dùng lab tìm phản ví dụ bằng máy; phần viết chứng minh vẫn ở cảnh quiz.
- Số trong cảnh quy mô là "số minh hoạ" (một tỉ phép mỗi giây), mã của cảnh chỉ đếm (tất định), không đo thời gian. Mệnh đề an toàn mật mã (L15: "với 2048 bit chưa ai làm nổi") ghi theo hiểu biết công khai, đã nêu giới hạn trong lời đọc.
- Đã mở PNG khung: L00, L01, L11, L14, L16, L17, L20; các bài khác chỉ qua render 0 vấn đề.
- P1/P8 dự kiến (chưa có người đọc độc lập): P1 = 2 ở phần lớn bài nhờ định nghĩa tại chỗ và lab tự đứng; rủi ro P1 còn ở cú pháp Python trong lab (giả định PYT:L00–L03, `itertools`/`lambda` chỉ giải thích ở `de.md`).

## Sửa theo reader A (L00–L10, `R_WP5_DMS_A.md`: MUST 0; P1 = 2 chỉ 5/11)
Mọi sửa đi qua tệp vá `audit/dms/af2/lNN.py` (chạy lại được); bài sinh từ mẫu (L08) sửa mẫu rồi `fill()`.
- **Số nhóm bằng dấu cách trong `say`** (L00 "1 024", L02, L03, L05, L06, L08, L10; và L11, L12, L14, L16, L17, L19 theo reader B): `af2lib.step()` nay tự nối liền ("1024", "666667") cho mọi `say` do bộ vá sinh; bảng hiện trên màn hình vẫn giữ dấu cách.
- **L01**: hook giảng tại chỗ "dấu chấm than là không, hai dấu và là và"; quymo giảng "số nguyên 32 bit là một trong hai mũ 32 giá trị"; practice bỏ vế nói trước cặp nào là luật/đảo.
- **L02**: giảng biểu thức sinh trong `all/any` ("thử lần lượt từng x/phần tử của miền") ở example, quymo, practice và gợi ý.
- **L03, L04**: đọc công thức có ngoặc ("2 nhân tổng a cộng b cộng 1, tổng này đặt trong ngoặc"; "n nhân, trong ngoặc n cộng 1, rồi chia 2" ở câu hỏi và đáp án quiz).
- **L05**: bỏ "ước chung" (nói "không có số nào lớn hơn 1 mà chia hết cho cả 2 lẫn 3"); "BCNN" viết "bội chung nhỏ nhất, tức số nhỏ nhất chia hết cho cả hai" ở đề, gợi ý, de.md; dòng mong đợi đổi thành `dem=333 congthuc=333` (lab, `mong_doi.txt`, màn hình, bộ kiểm đồng bộ).
- **L06**: "khoá" = mã định danh của dữ liệu cần cất (hook và quymo); "cận dưới" = mức thấp nhất chắc chắn có.
- **L08**: practice giảng "hoán vị = mọi cách xếp thứ tự", "tối tiểu = không ai đứng dưới", "tối đại = không ai đứng trên", `permutations` nêu ở de.md; quymo nêu điều kiện: chọn từng phần tử chỉ cỡ n + số ràng buộc khi giữ bộ đếm số việc phải xong trước của mỗi việc (không còn "tối đa n lượt … kịp cả triệu việc" vô điều kiện).
- **L10**: `C(12,5)` nêu là tổ hợp chập 5 của 12; "vét cạn" = thử hết mọi trường hợp (đề và de.md); tiêu đề lỗi 3 đổi khớp thân: "Chia thêm k! khi đã đếm theo nhóm (sai)".

## Sửa theo reader B (L11–L20, `R_WP5_DMS_B.md`: MUST 0; P1 = 2 chỉ 6/10)
- **L14**: định nghĩa số nguyên tố ngay ở định lý Fermat; "bit" = chữ số nhị phân 0 hoặc 1, "bit thấp" = chữ số nhị phân cuối (quymo).
- **L15**: "bit" = chữ số nhị phân ở bảng quymo; "phần đệm" = đoạn dữ liệu ngẫu nhiên thêm vào bản tin; "L bằng tích của p trừ 1 và q trừ 1" (sym, recap); `why`: nói rõ phạm vi, chứng minh chỉ cho x nguyên tố cùng n, trường hợp x chia hết cho p hoặc q chưa chứng minh mà chỉ kiểm bằng máy với mọi bản tin 0..32.
- **L19**: hook giảng bảng băm, hàm băm, khoá, va chạm trước khi dùng.
- **L20**: `sym` step 2 khôi phục câu hàm băm thứ ba (đủ "bốn hàm băm"), byte = 8 bit; `check` đổi thành "hai trong bốn con số", bỏ hai hàng 1796 ngày và 2,8×10¹⁴ khỏi bảng tự kiểm (số 2,8×10¹⁴ vẫn được đọc ở chặng 4; 1796 ngày không còn trên màn hình vì step tính số ngày đã bị cắt); lời đọc 2 290 từ.
- **L18**: "gấp n chia 2 lần mức cần thiết, tức 5 lần với 20 đỉnh và 50 lần với 200 đỉnh". **L17**: "khoảng 50 phần triệu giây". **L12**: `de.md` mục 4 không còn ghi sẵn biểu thức toàn ánh (chỉ nêu ý "tất cả trừ các hàm bỏ sót").
- **Quiz L11–L19**: `pause` tăng lên 30 giây (`quiz_pause=30` ở bộ vá; lint không cấm).
- Không đổi: yêu cầu dựng lại video (SRT/chapters/mp4 cũ không có quymo/practice, số đã nối liền) — việc của người điều phối khi dựng; L13/L18 vượt "Python cơ bản" (đệ quy, tuple/set): chưa thêm gợi ý mẫu.

### Cổng sau đợt sửa reader A+B (2026-11-14)
lint L00–L20: 0 FAIL 0 WARN (L07, L09 không đổi); render 0 vấn đề cho mọi bài đã đổi (L00–L06, L08, L10–L20); `verify_dms.py` 323 PASS 0 FAIL; `lab_gate.py DMS` 21 PASS; `screen_code.py check --course DMS` PASS 95, 0 STALE/MISSING/ORPHAN; `lv.py curriculum` 0 lỗi; `tests/test_e52.py` 0 FAIL; `arith_scan.py` 243/0 FAIL. Lời đọc ≤ 2 300 từ mọi bài (L20 = 2 290). Chưa dựng video/ASR.
