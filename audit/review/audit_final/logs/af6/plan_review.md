# Phản biện độc lập `plan_AF6_20261127T1608Z.md`

- Người phản biện: tác tử `af6-planreview` · Ngày: 2026-11-27 · Mốc git: `a3039c1f`
- Phạm vi: chỉ đọc kho; tệp duy nhất được ghi là tệp này. Không chạy build/tts/render, không lệnh git làm đổi kho, không đụng `nghe_thu_ket_qua.json` (chỉ đọc). Mọi tập lệnh đo nằm ngoài kho, trong thư mục tạm của phiên (`C:\Users\AI_WOR~1\AppData\Local\Temp\claude\740fb36319f596fa\7f7b6502-2016-4cc6-a561-b1aadf44e550\scratchpad\a1.py` … `a7.py`); bản lời đọc mốc `5d7f329` lấy bằng `git archive 5d7f329 lessons | tar -x` vào cùng thư mục tạm.
- Nhãn: OBSERVED = tôi chạy lệnh hoặc đọc dòng mã trong lượt này; INFERRED = suy luận từ thứ đã đọc; CHƯA KIỂM = không kiểm được.

## Bảng tổng

| Mức | Số phát hiện | Mã |
|---|---:|---|
| CAO | 10 | PR-01 … PR-10 |
| VỪA | 8 | PR-11 … PR-18 |
| THẤP | 4 | PR-19 … PR-22 |
| **Tổng** | **22** | |

Kết luận ngắn: phần chẩn đoán của kế hoạch (mục 1) đứng được và các con số chính khớp tệp `.out`. Phần chữa (mục 3, 5, 7, 9) còn mười chỗ nếu đem thực thi nguyên văn sẽ hoặc làm hỏng bài đang đúng, hoặc tạo ra cổng không đạt được, hoặc tạo ra cổng lách được theo đúng kiểu mà kế hoạch đang phê phán.

---

## Mức CAO

### PR-01 · "Mặc định xoá" theo từng câu sẽ làm hỏng bài: bước bị câm, câu gốc bị xoá thay vì khôi phục, `focus` lệch

**Trích.** D-2: "Câu thêm sau mốc `5d7f329` ở cảnh không phải Tự làm: **mặc định xoá**, chỉ giữ khi người đọc xác nhận…" · WP-2: "(a) lập bảng câu thêm; (b) mặc định xoá" · lý do: "xoá rẻ và an toàn hơn sửa từng câu".

**Bằng chứng (OBSERVED).** Tôi dựng lại đúng phép đo `p8` (ra đúng 7 934 câu) rồi phân loại từng câu theo bước cũ cùng `(scene id, chỉ số step)`:

| Loại câu "thêm" | Lớp A | Lớp B | Lớp C |
|---|---:|---:|---:|
| Nối thêm, các câu cũ của bước còn nguyên | 4 | 871 | 4 187 |
| Thêm trong lúc câu cũ của bước cũng đổi | 14 | 661 | 652 |
| Là **bản sửa** của một câu cũ (độ giống ≥ 0,75 với câu cũ đã mất) | 75 | 54 | 265 |
| Là bản viết lại của câu cũ (độ giống 0,5–0,75) | 34 | 74 | 53 |
| Nằm trong **bước mới** (bước không có ở `5d7f329`) | 38 | 170 | 782 |
| Tổng | 165 | 1 830 | 5 939 |

- `p8_tail_sentences.py` định nghĩa "câu thêm" là câu ở HEAD không trùng **nguyên văn** câu nào của bài cũ. Câu cũ bị sửa một chữ cũng thành "câu thêm". 555 câu (265 + 53 + 54 + 74 + 75 + 34) là bản sửa hoặc viết lại của câu gốc: xoá chúng là xoá luôn nội dung gốc, không phải trả bài về trạng thái đã rà.
- 591 bước (C 380, B 164, A 47) có **mọi** câu đều là "câu thêm". Xoá mặc định thì bước còn `show` mà không còn `say`. `tools/lv.py:1055` dựng một khung hình cho mỗi câu của `say`; bước không câu thì không có khung nào, khối `show` của nó không bao giờ là khối đang giảng.
- 4 971 trong 7 934 câu thêm (C 3 551, B 1 313, A 107) nằm trong bước có mảng `focus`. `tools/lv.py:871` (E31) báo **lỗi** khi số mục `focus` khác số câu. Xoá câu mà không xoá đúng mục `focus` cùng vị trí thì lint gãy; xoá lệch vị trí thì khung sáng lệch hàng (đúng loại lỗi mà `G-SHOW` muốn chặn).
- Mẫu 20 câu tôi đọc trong ngữ cảnh (hạt giống 20261127; 10 câu rút từ `p8_tail_candidates.tsv`, 10 câu thêm không phải ứng viên, lớp B và C):

| Nhóm | Nên xoá | Nên giữ | Ghi chú |
|---|---:|---:|---|
| 10 ứng viên `p8` | 8 | 2 | `CPR L05 example[1]`: câu "Ép sang con trỏ ký tự một bai khi đo…" giải thích đúng phép ép kiểu `(const char *)` đang hiện trên màn hình; bị gắn "lệch màn hình" chỉ vì lời tiếng Việt không chung từ ≥ 4 chữ với mã. `CPR L08 pitfalls[1]`: bước có `show` rỗng, cả lời là hai câu thêm, nội dung đúng và có ích (mở tệp chế độ `b`, dịch bit trên kiểu không dấu); xoá thì bước câm |
| 10 câu không phải ứng viên | 7 | 3 | `DVO L01 check[2]`: bước **mới hoàn toàn** có bảng trên màn hình, cả ba câu đọc đúng bảng. `MLP L11 formula[0]`: câu duy nhất nêu quy tắc đếm tham số cho công thức 2 trên màn hình. `CSA L15 pitfalls[2]`: đúng và bám màn hình, giữ được |

  Bảy câu "nên xoá" của nhóm không ứng viên đều là câu nhắc lại hoặc câu nói sang lỗi khác (`CLD L01`, `CSA L14`, `AIF L11`, `TOC L09`, `DBS L14`, `BCH L00`, `PRJ L04`). Tức là mặc định xoá đúng với khoảng 3/4 số câu và sai với khoảng 1/4 (n = 20, khoảng tin cậy rộng).

**Vì sao là lỗi.** Quy tắc được viết ở mức câu trong khi dữ liệu có ba dạng khác nhau (nối đuôi, sửa câu cũ, bước mới). Với 7 934 phán quyết, người duyệt gần như chắc chắn sẽ chấp nhận mặc định, nên mặc định sai ở đâu thì bài hỏng ở đó.

**Đề xuất sửa.** (1) Ba phán quyết thay cho hai: `giu` · `xoa` · `khoi_phuc` (trả nguyên văn câu của `5d7f329`). (2) Mặc định theo loại: nối đuôi khi câu cũ còn nguyên → `xoa`; bản sửa của câu cũ → `khoi_phuc`, trừ khi bản sửa đang chữa lỗi cổng (`check_xref`, E55, `arith_scan`) thì `giu`; bước mới → quyết định ở mức **bước** (giữ cả bước hoặc xoá cả `show` lẫn `say`), không ở mức câu. (3) `tail_review.py` phải có lệnh áp phán quyết tự động: xoá câu cùng mục `focus` cùng vị trí, chạy `lv.py lint` ngay, từ chối tạo bước không còn câu. (4) Trước khi áp cho cả chặng, chạy thử trên 10 bài rồi cho người đọc khác so từng bài trước/sau.

---

### PR-02 · Tiền đề "thân bài trước khi độn đã được kiểm đúng" không đúng; nội dung thêm trên màn hình (`show`) không có quy tắc nào xử lý

**Trích.** D-2: "Thân bài trước khi độn đã được kiểm đúng" · bảng 1.1 dòng lớp C: "16/16 bài mẫu: số liệu và mã trên màn hình đúng khi tính/chạy lại; lỗi nằm ở câu nối thêm và ở lab" · `G-TAIL` chỉ nói "mọi câu lời đọc".

**Bằng chứng (OBSERVED).** Tôi lấy từng dòng MUST của `sample_k/K1..K3.md` (31 dòng, các bài có ở mốc cũ), trích các câu trong ngoặc kép rồi dò trong tệp bài ở HEAD và ở `5d7f329`:

| Nhóm | Số dòng MUST |
|---|---:|
| Mọi câu trích đều **đã có ở `5d7f329`** | 3 (`CVI L03` "độ lệch tăng theo bình phương…" — có 3 lần ở bản cũ, gồm chú thích SVG trên màn hình; `CS115 L24` "bài toán lồi… điều kiện đủ"; `CPR L06` pitfalls) |
| Vừa có câu cũ vừa có câu thêm | 6 (`AIF L13`, `HCI L11`, `CPR L04`, `LNX L03`, `MLP L00` ×2) |
| Chỉ gồm câu thêm, có ít nhất một câu nằm trong `p8_tail_candidates.tsv` | 6 |
| Chỉ gồm câu thêm, **không** câu nào là ứng viên `p8` | 9 |
| Nằm ở cảnh Tự làm, màn hình, hoặc lab (không dò được bằng câu trích) | 7 |

- 9/31 dòng MUST có câu đã tồn tại ở mốc "đã rà". `CVI L03` là lỗi kiến thức hiện ngay trên màn hình, trái với câu "16/16… số liệu trên màn hình đúng". Chính `K2.md` mục nhận xét 5 ghi "Lỗi kiến thức thật sự chỉ có 2 (CVI…; CS115 KKT…)".
- Đợt AF5 không chỉ thêm lời. So `show` theo `(scene id, chỉ số step)`: 1 522/12 866 bước lớp C, 210/813 bước lớp B, 99/7 022 bước lớp A có `show` khác bản cũ. Chuỗi "So sánh hai quy mô" có trong `show` của 382 bài ở HEAD so với 18 bài ở `5d7f329`. `K2.md` mục 4 ghi đoạn này "là nguồn số không căn cứ ở 6 bài".
- Đo độ bắt cho BN6-14 (việc kế hoạch để tới WP-1.5, tôi làm luôn): trong 21 dòng MUST có dính câu thêm, danh sách 1 490 ứng viên `p8` chỉ chạm 7 dòng (33%). Danh sách 7 934 câu chạm cả 21.

**Vì sao là lỗi.** (1) Sau khi xoá hết câu thêm, bài vẫn còn lỗi cũ và còn nội dung màn hình mới chưa ai rà; câu "xoá rẻ và an toàn" làm người thực thi tin rằng xoá xong là sạch. (2) Xoá lời mà để lại ghi chú "So sánh hai quy mô" trên màn hình sẽ tạo ra chữ trên màn hình không ai đọc (xem `TOC L09 quiz[2]`, `BCH L00 recap[0]` trong mẫu 20 câu: các câu thêm đứng trước chính là lời đọc ghi chú đó). (3) Con số 1 490 dễ bị đọc thành khối lượng việc; nó chỉ bắt một phần ba.

**Đề xuất sửa.** Sửa câu chữ D-2 và bảng 1.1 (ghi rõ `CVI L03`, `CS115 L24` là lỗi có từ trước). Mở rộng `tail_review.py` sang `show`: mọi khối `show` khác `5d7f329` cũng phải có phán quyết, và phán quyết của `say` với `show` cùng bước phải nhất quán (xoá ghi chú thì xoá lời đọc nó). Ghi vào BN6-14: độ bắt của `p8` = 7/21, dùng danh sách đầy đủ làm đầu vào, `p8` chỉ để xếp ưu tiên.

---

### PR-03 · `G-REPEAT` viết như hiện tại sẽ đánh trượt 122 bài lớp A, cho qua toàn bộ bài đúc khuôn theo khoá, và số nghiệm thu không khớp ngưỡng

**Trích.** 5.3: "Tỉ lệ từ của cảnh Tự làm nằm trong câu lặp ở ≥ 20 bài phải ≤ 20%; ngoài cảnh Tự làm ≤ 5%" · WP-1 nghiệm thu: "`G-REPEAT` trượt ≥ 378 bài" · bẫy 10: "Không sửa lớp A theo kiểu hàng loạt; 120 bài không đổi là tài sản đã kiểm".

**Bằng chứng (OBSERVED, tính từ `p2_repeat_per_lesson.tsv`).**

| Lớp | Bài có cảnh Tự làm > 20% từ nằm trong câu lặp | Bài có phần ngoài Tự làm > 5% |
|---|---:|---:|
| A (196) | **122** | 0 |
| B (45) | 20 | 0 |
| C (536) | 501 | 0 |
| Khoá mới (29) | **0** | 0 |
| Tổng | 643 | 0 |

- Ngưỡng 20% cho ra 643 bài trượt, không phải 378 (378 là số bài ≥ 50%).
- Vế "ngoài cảnh Tự làm ≤ 5%" hiện không bài nào trượt: vế này không chặn được gì trong 7 934 câu độn.
- Bài mới `BEP`/`AIP` qua cổng 29/29 dù `K4.md` ghi "mười một tiêu đề cảnh giống hệt nhau… năm đến sáu câu độn dùng lại nguyên văn". Lý do: khuôn theo khoá chỉ lặp 6–18 bài, dưới ngưỡng 20. `p2_repeat_sentences.out`: 133 câu lặp ở ≥ 10 bài nhưng chỉ 66 câu ở ≥ 20 bài; `p4_before_after.out` liệt kê 14 khung câu lặp đúng 14 bài (toàn bộ `MLP`), và dòng trung vị theo khoá ghi `MLP:0 AIP:0 BEP:0 PRJ:0`.
- 122 bài lớp A trượt vì cảnh Tự làm soạn tay ngắn và dùng vài câu quen ("Đây là kết quả mong đợi." 142 bài; "Bạn chạy chương trình của mình rồi so từng dòng." 85 bài).

**Vì sao là lỗi.** Cổng vừa ép sửa hàng loạt lớp A (trái bẫy 10, kéo theo dựng lại 122 video lớp A và làm lệch các phán quyết nghe của người dùng ở những bài đó, xem PR-13), vừa bỏ lọt đúng loại khuôn mà RC-2 mô tả. Cách lách đã có sẵn trong kho: chia khuôn theo khoá, hoặc chèn tên khoá vào câu.

**Đề xuất sửa.** (1) Đo lặp theo hai mức: giữa các khoá (≥ 3 khoá) và **trong một khoá** (≥ 30% số bài của khoá). (2) Chuẩn hoá trước khi so: bỏ số, mã bài, tên khoá, tên tệp. (3) Có danh sách câu quy ước được phép, ngắn và do người duyệt (lời chào cuối bài, "Dừng video và làm ra giấy."); đo phần còn lại. (4) Ghi phạm vi: lớp A chỉ báo cáo, không chặn. (5) Sửa nghiệm thu WP-1 thành con số tính từ đúng ngưỡng, kèm đối chứng dương "`BEP`, `AIP`, `MLP` phải trượt".

---

### PR-04 · Điều kiện "khoá đạt" ở 5.1 không thể đạt với khối lượng WP-5; điểm dừng E5 và E7–E8 hứa nhãn mà không có việc tạo ra nhãn

**Trích.** 5.1: "Khoá chỉ được ghi 'đạt' khi 100% bài `G2`, mọi bài ≥ `T1`, có ≥ 3 lab `T3` (hoặc `T2` với khoá thuần lý thuyết: `DMS`, `TOC`, `CS112`, `CS115`, `CLC` phần toán)…" · WP-5: "10–11 | các khoá chuyên ngành | Mỗi khoá 2 lab `T2`/`T3`" · D-3: "3–5 lab mỗi khoá" · E5: "rà 76 bài lớp A có đổi + WP-6.1; thêm ca ẩn cho lab lớp A nào in cứng vẫn đạt" → "196 bài đạt `G2` · `T1+` · `A1`" · E7–E8: "Chặng 1–5 trọn vẹn đạt nhãn".

**Bằng chứng (OBSERVED, đếm trên chính bảng WP-5 và `p3_labs.out`).**

| Dòng WP-5 | Số khoá | Số lab nghề liệt kê | Lab mỗi khoá |
|---|---:|---:|---:|
| `CPR` | 1 | 3 | 3 |
| `LNX` | 1 | 4 | 4 |
| `CSA` `OSY` `NET` | 3 | 6 | 2 |
| `DBS` | 1 | 3 | 3 |
| `SWF` `SDP` | 2 | 2 | 1 |
| `WEB` `SEC` | 2 | 3 | 1,5 |
| `DSY` `EVT` `DEN` | 3 | 3 | 1 |
| `CLD` `CLC` `DVO` `SAR` | 4 | 4 | 1 |
| `DAN` `DSC` | 2 | 3 | 1,5 |
| `MLP` `MLO` `AIP` | 3 | 4 | 1,3 |
| `CS115 L22–43` `CVI` `LLM` `AGT` `IRS` `RLN` | 6 | 6 | 1 |
| Chặng 10–11 (11 khoá) | 11 | 22 | 2 |
| Chặng 1–5 (`FND` `JVA` `JV2` `PYT` `BNK` `BNX` `INT` `ACB` `SPB` `BEP`) | 10 | **0** | 0 |

- Chỉ `CPR`, `LNX`, `DBS` đủ 3 lab. Ngoại lệ lý thuyết chỉ gồm 5 khoá (trong đó `TOC` thuộc Chặng 10, chỉ được 2 lab). Theo 5.1 thì ít nhất 45/53 khoá không bao giờ "đạt".
- E5: `G2` cần "báo cáo của người đọc đã qua hiệu chuẩn, khớp mã băm tệp bài". Chỉ rà 76 bài thì 120 bài còn lại không có báo cáo như vậy; nhãn `G2` cho 196 bài là không có chứng cứ theo chính 5.1.
- E5: `T1` = "đủ đề + ca kiểm tốt" (`G-DE`, `G-CASE`). `p3_labs.out`: 196 lab không có `ca_an/` lẫn `kiem/`; `labs/CONTRACT.yaml` ghi `ca_them: 'mien: lop_A_da_dat'`. Để 196 lab lên `T1` phải viết đề 5 mục, ≥ 3 ca và ≥ 2 biến thể sai cho từng lab. 10 lab là tệp `.md` (9 `INT`, `BNX L35`), không có đầu ra để đặt ca ẩn.
- `A1` = "đã sửa theo từ điển và **nghe mẫu**": cần tai người, E5 không ghi.

**Vì sao là lỗi.** Kế hoạch tự dựng lại tình huống nó phê phán: nhãn được hứa ở điểm dừng mà không có đường hợp lệ để có nhãn. Người thực thi sẽ hoặc hạ chuẩn ngầm, hoặc ghi nhãn không chứng cứ.

**Đề xuất sửa.** Chọn một trong hai và ghi rõ: (a) hạ điều kiện khoá xuống "≥ 1 lab `T3` hoặc dự án chặng `T4` phủ khoá đó", hoặc (b) giữ ≥ 3 và bổ sung bảng WP-5 cho đủ, kể cả Chặng 1–5. Thêm dòng WP-5 cho Chặng 1–5 (xem PR-17: đây là phần JD đòi nhiều nhất). Sửa điểm dừng E5 thành thứ đạt được: "76 bài đã đọc có hiệu chuẩn; 120 bài giữ `G1` kèm mẫu ngẫu nhiên n ≥ 12 đọc có hiệu chuẩn"; tách việc nâng 196 lab lớp A thành phiên riêng và định nghĩa `T` cho lab giấy.

---

### PR-05 · Cổng mới mâu thuẫn với cổng AF5 đang giữ; việc "bỏ ba cổng" làm gãy bộ thử hiện có

**Trích.** BN6-03: "`G-DE`: 5 mục bắt buộc có mặt; ví dụ tính tay khớp `mong_doi.txt`" · 5.3 `G-TASKCARD`: "Thẻ Tự làm sinh tất định từ `de.md` (nhiệm vụ, dữ liệu mẫu, đầu ra mong đợi)… Thay cho `G-PRACTICE`" · WP-1.2: "Bỏ `G-LEN`, `G-PAD`, `G-BOILER` khỏi `content_gates.py` và `final_gates`" · D-3: "video chỉ giữ một thẻ giao việc ngắn".

**Bằng chứng (OBSERVED, đọc mã).**
1. `audit/review/content_gates.py:181-188` (`check_g_leak_de`): FAIL khi **mọi** dòng của `mong_doi.txt` xuất hiện trong `de.md`. `G-DE` đòi ví dụ khớp `mong_doi.txt` và `G-TASKCARD` đòi lấy "đầu ra mong đợi" từ `de.md`, trong khi `tools/lv.py:751-755` (E53) đòi mọi dòng `mong_doi.txt` hiện trên màn hình cảnh Tự làm. Ba đòi hỏi cùng lúc buộc `de.md` chứa đủ `mong_doi.txt` → `G-LEAK-DE` trượt ở mọi lab → `content_gates --ratchet` báo `NEW_REGRESSION`.
2. `content_gates.py:147-157` (`check_g_practice`): FAIL khi cảnh Tự làm có < 3 bước hoặc không có bước `pause`. 5.3 nói `G-TASKCARD` thay `G-PRACTICE`, nhưng WP-1.2 không liệt kê `G-PRACTICE` trong danh sách bỏ. Thẻ "ngắn" dưới 3 bước sẽ là hồi quy.
3. `tests/test_content_gates.py:12-24`: bảng `EXPECTED` có dòng cho `G-LEN`, `G-PAD`, `G-BOILER` và truy cập `grid[(c, l)][gate]`. Bỏ ba khoá đó khỏi `res` thì bộ thử ném `KeyError`; nó nằm trong cổng `[11]` của `final_gates_af5.sh` (chế độ `nhanh`). `final_gates_af5.sh` không có dòng riêng nào cho ba cổng này để "bỏ".
4. `content_gates.py:270,290`: `check_g_covers` nhận kết quả `G-PRACTICE` và `G-BOILER` làm tham số; bỏ `G-BOILER` phải sửa cả hàm này.
5. `content_gates.py:572-580`: chế độ ratchet lấy danh sách khoá khoá-cứng từ `label == "ĐÃ CHỐT"`. Sau WP-0.4 danh sách rỗng, dòng "0 lỗi khoá ĐÃ CHỐT" đúng một cách trống rỗng.
6. `covers` trỏ vào cảnh Tự làm: 170 bài lớp A có mục tiêu trỏ tới cảnh `practice`, **168 bài lớp A có ít nhất một mục tiêu chỉ được phủ bởi cảnh Tự làm** (lớp C: 7, lớp B: 1). Nếu D-3 áp cho lớp A thì 168 bài mất cảnh dạy của một mục tiêu (E51 ở `lv.py:726-731` và `G-COVERS`).

**Vì sao là lỗi.** Điểm dừng E1 ghi "cổng bản 2 có phép thử" và mọi phiên phải kết thúc với "cổng nhanh đạt"; với các điểm 1–3 thì ngay sau WP-1 cổng nhanh sẽ đỏ, hoặc người thực thi phải sửa cổng AF5 ngoài kế hoạch.

**Đề xuất sửa.** Thêm vào WP-1 một bảng "cổng cũ bị ảnh hưởng": `G-LEAK-DE` (đổi thành "ví dụ tính tay dùng **dữ liệu khác** dữ liệu mẫu công khai", hoặc bỏ hẳn vì chống in cứng đã do ca ẩn đảm nhận, ghi rõ chọn cách nào); `G-PRACTICE` (bỏ, thay bằng `G-TASKCARD`, giữ điều kiện `pause` vì E53 còn đòi); `test_content_gates.py` và thư mục `tests/fixtures/content_gates/` (sửa cùng lượt); tệp nền ratchet (sinh lại với bộ cột mới). Ghi phạm vi D-3 và `G-TASKCARD`: **không áp cho lớp A**, hoặc nếu áp thì phải chuyển 168 mục `covers` sang cảnh khác trước.

---

### PR-06 · Hiệu chuẩn và mẫu đối chứng (5.2) lách được và tự mâu thuẫn

**Trích.** 5.2.1: "bộ 6 bài có cài 20 lỗi đã biết (lấy từ lỗi thật của Mẫu K và Mẫu H, cài vào bản sao trong `tests/fixtures/calib/`). Người đọc (tác tử hay người) phải bắt ≥ 16/20 và không báo quá 4 lỗi giả mới được chấm `G2`" · 5.2.4: "tìm ra ≥ 1 lỗi bắt buộc sửa thì cả khoá quay lại sửa và đọc, tối đa 2 vòng rồi báo `PARTIAL`" · mục 11: "41/48 lỗi bắt buộc sửa của Mẫu K | CITED từ báo cáo tác tử, chưa tự kiểm lại".

**Bằng chứng.**
- Đáp án nằm trong kho: bài hiệu chuẩn ở `tests/fixtures/calib/`, lỗi gốc mô tả đầy đủ trong `logs/af6/sample_k/K1..K4.md`. Một tác tử đọc có quyền đọc kho chỉ cần `diff` bản cài lỗi với `lessons/` hoặc mở `sample_k/` (INFERRED từ đường dẫn kế hoạch nêu; `BRIEF_K.md` luật 4 cấm đọc `sample_*` nhưng không có gì cưỡng chế).
- Người đọc là tác tử không có trí nhớ giữa các lần gọi. "Đã qua hiệu chuẩn" gắn với một lần chạy, trong khi lần chạy đọc bài thật là một ngữ cảnh khác. Kế hoạch không nói hiệu chuẩn gắn vào cái gì (mô hình + bản `BRIEF_AF6.md`?) và khi nào hết hiệu lực.
- Dung sai trái nhau: hiệu chuẩn cho phép 4 lỗi giả trên 6 bài (0,67 lỗi giả mỗi bài). Mẫu đối chứng ≥ 3 bài với dung sai 0: một người đọc vừa đủ chuẩn sẽ báo trung bình 2 lỗi giả trên 3 bài, tức khoá sạch vẫn gần như chắc chắn bị trả về. Không có bước phân xử lỗi do mẫu đối chứng báo.
- 20 lỗi cài lấy từ Mẫu K, nhưng mới 7/48 lỗi được người điều phối kiểm lại; `K1.md` tự ghi 2 dòng là "MUST (nhẹ)". Dùng lỗi chưa kiểm làm đáp án là dạy người đọc theo một chuẩn chưa xác nhận. WP-2(c) cũng ra lệnh sửa "các lỗi bắt buộc sửa đã nêu trong `sample_k/`" mà không có bước kiểm 41 lỗi còn lại.

**Vì sao là lỗi.** Đây là cơ chế thay cho "đọc độc lập 100%" đã thất bại (RC-4). Nếu bài thi có đáp án mở và kết quả đối chứng không phân xử, nó sẽ hoặc bị qua bằng mẹo, hoặc kẹt ở `PARTIAL` cho mọi khoá.

**Đề xuất sửa.** (1) Thay bài thi một lần bằng **mục vàng cài mù**: mỗi lô 8 bài giao cho người đọc có 1–2 bài bị cài lỗi mới, người đọc không biết bài nào; lô nào bắt < 80% lỗi cài thì cả lô bị loại. (2) Bản cài lỗi và đáp án sinh lúc giao việc vào thư mục tạm ngoài kho; trong kho chỉ lưu hạt giống và mã băm. (3) Lỗi do mẫu đối chứng báo phải qua phân xử bằng lệnh chạy lại (đúng cách kế hoạch đã làm với 7 lỗi) trước khi tính. (4) Thêm việc WP-1.0: kiểm lại 41 lỗi Mẫu K còn lại, chỉ lỗi đã xác nhận mới được dùng làm lỗi cài và làm danh sách sửa.

---

### PR-07 · Lab nghề: nhiều công cụ kế hoạch coi là "đã có trên máy này" thực tế không có; `lab_gate`, `CONTRACT.yaml`, `cham.sh` chưa có việc sửa để nhận lab nghề

**Trích.** WP-5: "Chạy trên máy người học với công cụ đã có trên máy này (OBSERVED: Java 21, gcc 16.2, Docker 28.3, Node 25…)" · "Danh sách liên kết không rò (gcc + AddressSanitizer)… gỡ lỗi bằng gdb" · "viết dịch vụ nhỏ + `cron`" · "bắt và đọc gói bằng `tcpdump`" · "Kubernetes cục bộ (kind) nếu máy đủ" · BN6-05: "bằng công cụ (valgrind/`docker inspect`/`EXPLAIN`)" · "thư mục `labs/<KHOÁ>/N<k>/` gồm `de.md`, mã khởi đầu, `kiem/`, `kiem/ne/`, `loi_giai/`".

**Bằng chứng (OBSERVED).**
- `command -v` trong Git Bash: `valgrind`, `tcpdump`, `cron`, `crontab`, `kind`, `psql`, `mvn`, `clang` → không có. Có: `java` 21.0.13, `gcc` 16.2.0 (`x86_64-w64-mingw32`, w64devkit), `gdb`, `docker` 28.3.2 (máy chủ Linux), `node` v25.8.0, `kubectl`.
- Thử trong thư mục tạm: `gcc -fsanitize=address -g a.c` → `ld.exe: cannot find -lasan: No such file or directory`. AddressSanitizer không dùng được với gcc này.
- `audit/review/lab_gate.py:139-141` duyệt **mọi** thư mục con của `labs/<KHOÁ>/`; dòng 164 báo "thiếu mục trong labs/CONTRACT.yaml"; dòng 182 và 203 báo "mồ côi: không bài nào có cảnh practice trỏ tới" (cả lab dự án lẫn lab tệp). Lab `N<k>` tách khỏi video (D-3) sẽ trượt cả hai.
- `labs/cham.sh:85`: `cp -R "$KIEM"/. "$TMP/proj/"` chép cả `kiem/` vào dự án của người học; `kiem/ne/` (bài làm né kỹ năng) sẽ bị chép theo vào bản dựng Maven.
- 5.1 nhắc "`labs/CONTRACT.yaml` bản 3" nhưng không gói việc nào tạo nó; tệp hiện là `version: 2`.

**Vì sao là lỗi.** Lab nghề đầu tiên theo lộ trình (`CPR`, Chặng 6, E9) không chạy được trên chính máy soạn bài. Nhãn OBSERVED trong kế hoạch chỉ đúng với năm công cụ đã kể, không đúng với các công cụ mà bảng lab dùng.

**Đề xuất sửa.** (1) Ghi quyết định: lab cần công cụ Linux (ASan, valgrind, tcpdump, cron) chạy **trong container** với ảnh ghim digest; `kiem/chay_kiem.sh` gọi `docker run`; nêu tiên quyết "Docker đang chạy" trên trang lab. (2) Thêm bước "kiểm công cụ" vào nghiệm thu từng lab (lệnh thật, phiên bản thật) trước khi viết đề. (3) Thêm việc WP-1: `CONTRACT.yaml` bản 3 (trường `tang`, `cong_cu`, `ne`), sửa `lab_gate.py` (nhận `N<k>`, bỏ luật mồ côi cho lab nghề nhưng đòi `catalog.json` trỏ tới), đặt bài làm né ở `ne/` ngang hàng `kiem/` thay vì bên trong.

---

### PR-08 · Người học đang ở Chặng 1 sẽ không dùng được phần lớn thang phần thưởng trong 11 tới 21 phiên; thứ tự ở mục 7 trái mục 9

**Trích.** 1.1: "Bắt đầu học Chặng 1 ngay hôm nay là an toàn" · D-9: "mỗi chặng sửa trọn (lời đọc, thẻ giao việc, lab, phát âm) rồi mới sang chặng sau" · E4: "Bản đồ + phần thưởng đủ cấp; người dùng dùng thử" · E15: "WP-4 W4 (chấm lab từ web…)" · E25–E26: "WP-7, WP-4 W5–W6" · 6.4: "③ Luyện nhanh | `POST /api/cham` trả về đạt | ★★★" · 6.5: "Đủ sao của bài… Khoá: Xong mọi bài… Chặng: Qua cổng chặng (dự án)" · mục 7: "WP-0 → WP-1 → (WP-4 W1–W3 song song với WP-2/WP-3 của Chặng 6)".

**Bằng chứng (đối chiếu các mục của kế hoạch).**
- Sao thứ ba cần `/api/cham`, có từ W4 = E15. Từ E4 tới E15 không bài nào đủ sao, nên cấp "Bài" (đủ sao) và cấp "Chặng" (cổng chặng là dự án `PRJ`, cũng chấm qua `/api/cham`) của bảng 6.5 không đạt được. Cấp "Lab nghề" không tồn tại cho Chặng 1–5 vì WP-5 không có lab nào ở đó (PR-04). Cấp "Khoá" đạt được nếu "xong" nghĩa là một sao; kế hoạch chưa định nghĩa chữ "xong" ở dòng này.
- Bước ② có máy chấm từ W5 = E25–E26; "bài kiểm 20 câu" của cổng chặng thuộc WP-7 = E25.
- `/api/cham` không phụ thuộc việc sửa lab: `cham.sh` đã chấm được 806 lab hiện có (`lab_gate` 806/806 theo bản bàn giao AF5; `p5_mutation.out` 179/179).
- Mục 7 xếp W1–W3 song song Chặng 6 và không nhắc Chặng 1–5; mục 9 xếp W1–W3 ở E2–E4, rồi Chặng 1–5 ở E5–E8, Chặng 6 ở E9.

**Vì sao là lỗi.** Yêu cầu của người dùng là "tích từng bước, phần thưởng từ mục nhỏ tới mục lớn". Theo lộ trình này, đúng người học duy nhất đang học (ở Chặng 1–5, lớp A, phần kho tốt nhất) nhận một bản đồ mà ba trong chín cấp thưởng (Bài, Lab nghề, Chặng) bị khoá bởi thứ tự việc, không bởi nội dung.

**Đề xuất sửa.** Chuyển phần "chấm lab từ web" của W4 lên ngay sau W2 (trước E4), vì nó không chờ gì. Cho Chặng 1–5: cổng chặng dùng dự án hiện có + tự chấm theo bảng kiểm cho tới khi WP-7 xong, ghi rõ trên giao diện là "tạm". Sửa dòng thứ tự ở mục 7 cho khớp bảng mục 9.

---

### PR-09 · "Đã phát ≥ 90% thời lượng, tua không tính" sai với video có đoạn lặng chờ làm bài

**Trích.** 6.4: "① Xem video | Đã phát ≥ 90% thời lượng (tính theo các đoạn đã phát, tua không tính) | ★".

**Bằng chứng (OBSERVED).** Tổng `pause` (giây) của từng bài chia cho `timeline_seconds` trong `out/<KHOÁ>/<Lxx>/build_report.json`, 806 bài: trung vị 6,9%; p90 28%; lớn nhất 50,8%; **193 bài > 10%, 138 bài > 20%**. `tools/lv.py:1069` cộng `pause` vào độ dài khung cuối của bước, tức là hình đứng yên và im lặng trong video. Lời bài bảo "Dừng video và làm ra giấy" (478 bài, `p2_repeat_sentences.out`).

**Vì sao là lỗi.** Người học làm đúng lời dặn (dừng, làm bài, rồi tua qua đoạn chờ) sẽ không bao giờ đạt 90% ở 193 bài. Người để video chạy im lặng trong lúc đi pha cà phê thì đạt. Điều kiện thưởng phạt ngược hành vi mong muốn.

Các lỗ hổng khác của cùng điều kiện (INFERRED từ cách trình duyệt hoạt động, chưa có mã để thử): `video.played` mất khi tải lại trang nên xem hai buổi không cộng được; tốc độ phát không bị giới hạn; thẻ nền không tiếng vẫn tính.

**Đề xuất sửa.** Mẫu số = thời lượng trừ các đoạn `pause` (đã có trong dữ liệu dựng: mỗi khung có `pause`, `t0`); coi đoạn `pause` là đã xem. Tích luỹ khoảng đã phát trên máy chủ theo sự kiện (hợp các khoảng `[t0, t1]`, chỉ nhận bước tiến ≤ 2 giây × tốc độ, tốc độ ≤ 2), nên không mất khi tải lại. Thêm ba phép thử vào `G-WEB`: tua qua đoạn chờ vẫn đạt; tua thẳng tới cuối không đạt; xem hai buổi cộng lại đạt.

---

### PR-10 · An toàn của máy chủ cục bộ chưa đủ đặc tả và nghiệm thu chỉ thử một trong các đường tấn công

**Trích.** 6.2: "Mã phiên ngẫu nhiên trong địa chỉ; API chấm chỉ nhận tệp nằm trong thư mục làm bài người học chọn; gọi `cham.sh` bằng danh sách tham số, có giới hạn thời gian" · "phục vụ tệp tĩnh, video (hỗ trợ tua), và 5 đường API" · W4 nghiệm thu: "đường dẫn ngoài thư mục làm bài bị từ chối".

**Bằng chứng.** Chưa có mã; đây là rà thiết kế, đối chiếu với mã sẽ được gọi.
- `/api/cham` chạy mã của người học không cô lập: `labs/cham.sh:91` có `eval "$CHAY_CMD"`, dòng 93 chạy `./mvnw` lấy từ thư mục bài nộp. Ai gọi được API với một đường dẫn hợp lệ là chạy được mã với quyền người dùng. Hàng rào duy nhất là mã phiên.
- Mã phiên đặt trong địa chỉ sẽ nằm trong lịch sử trình duyệt và trong tiêu đề `Referer` khi trang bài học mở liên kết ngoài.
- Không có yêu cầu kiểm tiêu đề `Host` (chống DNS rebinding) và `Origin` (chống trang lạ gửi POST). Không nói cổng cố định hay ngẫu nhiên; "một nguồn gốc ổn định" cần cổng cố định, mà cổng cố định thì trang lạ đoán được.
- "Thư mục làm bài người học chọn": không nói chọn ở đâu. Nếu chọn qua API thì kẻ có mã phiên đổi được nó.
- Đường dẫn trên Windows: `..\`, chữ ổ đĩa khác, đường dẫn UNC `\\máy\chia_sẻ` (làm lộ băm NTLM khi mở), tên thiết bị (`CON`, `NUL`), luồng dữ liệu phụ (`tệp::$DATA`), tên ngắn 8.3, liên kết tượng trưng và junction. Nghiệm thu chỉ ghi một ca "đường dẫn ngoài thư mục".
- "Phục vụ tệp tĩnh" không nói gốc phục vụ. Nếu gốc là gốc kho thì `.git/`, `labs/*/ca_an/`, `labs/*/loi_giai*`, `nghe_thu_ket_qua.json` đều tải được qua HTTP.
- `cham.sh` không có giới hạn thời gian của riêng nó (chỉ `labs/kiem_ham.py:177` có `timeout=60`). Giới hạn phải do `hoc.py` đặt và phải diệt cả cây tiến trình; trên Windows, diệt tiến trình cha để lại `bash`/`java` mồ côi (đã ghi trong sổ nhớ dự án: "TaskStop leaves orphans… `taskkill /T`"). Lab `SPB` chạy 17,9–40,1 giây và khởi động container (`K4.md`).
- `http.server` của thư viện chuẩn không hỗ trợ `Range` và `HTTPServer` xử lý từng yêu cầu một. Video tổng 18,5 GiB, tệp lớn nhất 51,9 MB (OBSERVED): phải tự viết trả lời 206 và dùng `ThreadingHTTPServer`, nếu không một lần xem video sẽ chặn mọi lời gọi API. Kế hoạch có ghi "hỗ trợ tua" nhưng `G-WEB` không có phép thử `Range`.

**Vì sao là lỗi.** Đường xấu nhất là trang web lạ khiến máy người học chạy mã. Kế hoạch có nêu mã phiên và danh sách tham số, nhưng nghiệm thu W4 không thử các đường còn lại, nên bản đầu có thể qua nghiệm thu mà vẫn hở.

**Đề xuất sửa.** Ghi thành yêu cầu và phép thử trong `G-WEB`:
1. Từ chối mọi yêu cầu có `Host` khác `127.0.0.1:<cổng>` và `localhost:<cổng>`.
2. Mọi `POST` phải có `Origin` đúng nguồn gốc, `Content-Type: application/json`, và mã phiên trong **tiêu đề** (không trong địa chỉ). Không phát tiêu đề CORS. Thêm `Referrer-Policy: no-referrer`.
3. Thư mục làm bài đặt lúc khởi động (tham số dòng lệnh hoặc tệp cấu hình trong `~/.hoc_tap/`), API không đổi được.
4. Chuẩn hoá đường dẫn bằng `os.path.realpath` rồi so tiền tố; từ chối UNC, dấu `:` ngoài chữ ổ đĩa, tên thiết bị; có phép thử cho từng loại.
5. Gốc tĩnh là danh sách cho phép: `web/`, `out/<KHOÁ>/<Lxx>/{*.mp4,*.srt,frames/,chapters.txt}`, `labs/<KHOÁ>/<Lxx>/de.md` và mã khởi đầu.
6. Chấm chạy dạng việc nền (gửi → nhận mã việc → hỏi trạng thái), một việc mỗi lúc, giới hạn thời gian theo lab, diệt bằng `taskkill /T /F`.
7. Phép thử: `Range` trả 206 đúng byte; phát video trong lúc gọi `/api/state` không treo.

---

## Mức VỪA

### PR-11 · `G-TAIL`: phạm vi chưa rõ, tiêu chí "giữ" vừa loại nhầm câu đúng vừa lách được

**Trích.** 5.3: "Mọi câu lời đọc có mặt ở HEAD mà không có ở `5d7f329` phải có phán quyết `giu`/`xoa`…; câu `giu` phải chung ≥ 1 từ nội dung với màn hình của đoạn và không chứa từ tuyệt đối ngoài danh sách cho phép" · RC-1: "153 câu trong đó dùng từ tuyệt đối ('hoàn toàn', 'luôn', 'dứt điểm')".

**Bằng chứng (OBSERVED).**
- Phạm vi. 29 bài `SPB`/`BEP`/`AIP` không có ở `5d7f329` (`p4_before_after.out`: `only new 29`). Theo câu chữ, mọi câu của chúng cần phán quyết; riêng `SPB` là 944 câu ngoài cảnh Tự làm. Mọi câu viết mới về sau (sửa lỗi ở WP-2(c), lời thẻ ở WP-3, khoá mới ở WP-8) cũng vậy. `p8` thì bỏ cảnh Tự làm và bỏ bài mới; cổng và phép đo không cùng phạm vi.
- Loại nhầm. Áp đúng tiêu chí "chung ≥ 1 từ nội dung với `show` của bước" (cùng hàm `words` của `p8`) lên 10 khoá soạn tay lớp A: 2 193/19 421 câu (11,3%) không chung từ nào với màn hình của bước. Bài tốt nhất của kho trượt tiêu chí ở một câu trên chín. Nguyên nhân: câu chuyển ý, câu giải thích mã bằng tiếng Việt, và bảng của cảnh cộng dồn qua các bước (`lv.py:1044`) nên nội dung đang nói có thể nằm ở `show` của bước trước. 147 bước có `show` rỗng không bao giờ thoả.
- Lách. Chèn một danh từ của màn hình vào câu độn là qua. Thay "hoàn toàn" bằng "triệt tiêu", "trọn", "100%" là qua. Người ghi `tail_review.tsv` cũng là người thực thi.
- Từ tuyệt đối. Biểu thức `ABS` trong `p8_tail_sentences.py` không có "luôn" đứng một mình (chỉ có "luôn luôn") và không có "mọi"; kế hoạch lại trích "luôn" làm ví dụ. Các lỗi MUST của Mẫu K dùng đúng "luôn" ("luôn kết hợp tìm kiếm", "luôn giằng co"). Con số 153 vì thế đếm thiếu. Ngược lại, đưa "luôn"/"mọi" vào danh sách cấm thì 5,6% câu lớp A soạn tay dính (1 095/19 421).

**Vì sao là lỗi.** Cổng thay cho `G-LEN`/`G-PAD` phải không lách được bằng thêm chữ; tiêu chí chung-một-từ là tiêu chí đạt được bằng thêm chữ.

**Đề xuất sửa.** Tách hai việc. Phần máy của `G-TAIL` chỉ kiểm **độ phủ phán quyết** (0 câu khác mốc mà chưa có phán quyết; mỗi phán quyết có mã người đọc và mã băm câu). Phần "đúng, bám màn hình, không tuyệt đối hoá" do người đọc quyết và được kiểm bằng mẫu đối chứng trên các câu `giu` (rút 5% câu `giu` của mỗi chặng cho người đọc khác). Từ tuyệt đối chỉ dùng để **xếp hàng ưu tiên đọc**. Ghi rõ phạm vi: bài mới và bài viết lại không qua `G-TAIL` mà qua đọc `G2` toàn bài; đổi mốc so sánh sang thẻ git của lần chốt gần nhất sau mỗi chặng để cổng không phình mãi.

---

### PR-12 · Các cổng còn lại ở 5.3: cách lách từng cổng, chỗ không kiểm được bằng máy, và sàn số lượng quay lại dưới tên khác

**Trích.** 5.3 (bảng cổng) · "Không cổng nào đặt sàn số lượng chữ, số câu hay số phút" · bẫy 1: "Không đặt lại bất kỳ sàn số lượng nào (từ, phút, số câu)" · 5.1: "`T2` tự cài cơ chế (≥ 20 dòng lôgic…)" · BN6-04: "≥ 3 ca… ≥ 2 biến thể sai" · WP-7: "Mỗi bài ≥ 3 câu".

**Bằng chứng (phân tích theo câu chữ của kế hoạch; số liệu OBSERVED ghi kèm).**

| Cổng | Cách lách rẻ nhất | Kiểm được bằng máy? | Sửa |
|---|---|---|---|
| `G-DE` | Thêm 5 tiêu đề, mỗi mục một dòng | "Có mặt": có. "Ví dụ tính tay khớp": không, và trái `G-LEAK-DE` (PR-05) | Ví dụ tính tay khai báo dạng dữ liệu (`vi_du: {vao, ra}`); máy chạy lời giải mẫu trên `vao` và so với `ra` |
| `G-CASE` "≥ 3 ca" | Thêm một ca chép từ ca có sẵn, đổi một số | Có | Đòi các ca cho đầu ra khác nhau ở mọi dòng không phải hằng. Hiện 594 lab có đúng 2 ca, 3 lab có 3 ca (đếm từ `p3_labs.tsv`) |
| `G-CASE` "không ca nào cách điểm giữa < 1e-9" | — | **Không**: cổng chỉ thấy đầu ra đã làm tròn, không thấy giá trị trước khi làm tròn | Thay bằng phép thử hành vi: 3 cách cài đúng (float, `Decimal` nửa-lên, đổi thứ tự phép tính) phải cho cùng đầu ra ở mọi ca; đây đúng là phép thử đã bắt `BCH L08` trong `K2.md` |
| `G-CASE` "≥ 2 biến thể sai có tên đều bị trượt" | Viết biến thể sai hiển nhiên (in thiếu một dòng) | Có | Đòi mỗi biến thể **đạt ca công khai và trượt ít nhất một ca ẩn**; biến thể trượt ngay ca công khai không được tính |
| `G-SKILL` | Không tạo `kiem/ne/` thì cổng đúng một cách trống rỗng; hoặc đặt vào đó một tệp không biên dịch được | Có | Lab `T3`/`T4` bắt buộc ≥ 1 bài né; bài né phải biên dịch/chạy được, cho đúng đầu ra chức năng, và chỉ trượt ở phép kiểm kỹ năng |
| `G-SHOW` vế 2 "khung sáng trỏ đúng hàng đang đọc" | — | **Không** theo câu chữ (cần hiểu nghĩa) | Xấp xỉ bằng máy: hàng được `focus` phải chung ≥ 1 số hoặc từ khoá với câu; phần còn lại giao người đọc. Vế 1 (`show` rỗng) kiểm được: hiện 147 bước ở 99 bài (C 88, B 46, mới 13; lớp A 0) |
| `G-LABEL` | Sinh 806 tệp chứng cứ theo khuôn, mỗi tệp chèn mã bài | Có nhưng vô nghĩa | Chứng cứ = mã băm tệp bài + mã lô đọc + kết quả mục vàng của lô (PR-06); cổng tính lại mã băm |
| `quiz_verify.py` | Sinh câu hỏi từ `checks` tầm thường (`K3.md` nêu `80 + 443 == 523`, `len('lnx_srv8') == 8`) | Có | Loại biểu thức không chứa đại lượng của bài; mẫu đối chứng 10% đã có trong WP-7, giữ |

Sàn số lượng: "≥ 20 dòng lôgic" (`T2`), "≥ 3 ca", "≥ 2 biến thể", "≥ 3 câu mỗi bài", "≥ 3 lab `T3`" đều là sàn đếm, đạt được bằng thêm dòng. Riêng "≥ 3 câu mỗi bài" trái nguyên văn bẫy 1 ("số câu"). `lv.py:788` (E39) cũng còn một sàn đếm đang là **lỗi** lint ("cần ≥ 4 step làm mẫu") mà kế hoạch không nhắc.

**Vì sao là lỗi.** Bài học thiết kế ở cuối mục 1.2 nói mọi cổng đạt được bằng thêm chữ sẽ bị đáp ứng theo cách đó; bảng trên cho thấy phần lớn cổng mới (`G-DE`, `G-CASE`, `G-SKILL`, `G-LABEL`, cùng `G-TAIL` ở PR-11 và `G-REPEAT` ở PR-03) còn ở dạng đó.

**Đề xuất sửa.** Đưa cột "cách lách đã thử" vào bảng 5.3 và đòi mỗi cổng có một phép thử âm là chính cách lách đó (`tests/test_gates_v2.py`). Đổi các sàn đếm thành điều kiện hành vi như cột "Sửa"; với `T2`, bỏ "≥ 20 dòng", giữ "biến thể sai đạt ca công khai bị ca ẩn bắt".

---

### PR-13 · Điểm dừng "cổng nhanh đạt" trái với D-10; các sổ phụ gắn theo số thứ tự bước/khung sẽ lệch khi xoá câu

**Trích.** Mục 9: "Mỗi phiên kết thúc ở một điểm dừng an toàn: cổng nhanh đạt, không có bài nào dựng dở" · WP-2(e): "không dựng video ở bước này (chờ WP-3, `D-10`)" · 5.1: trục Âm thanh "Từ `nghe_thu_ket_qua.json` và hàng nghe".

**Bằng chứng (OBSERVED, đọc mã và dữ liệu).**
- `audit/review/find_stale_all.py:14-24` so `spec_sha256` và `tts_sha256` của bài với `build_report.json`. Sửa `say` mà chưa dựng lại là `STALE`; đây là cổng `[16]` của chế độ `nhanh`. Một chặng trải 3–5 phiên (E9–E11, E16–E19, E20–E24), nên mọi phiên giữa chừng sẽ kết thúc với cổng nhanh đỏ.
- `audit/review/sync_tpl_from_lesson.py` (cổng `[13]`): bài sửa tay phải chạy lại với `--write` để ghi mẫu, nếu không "LỆCH". WP-2/WP-3 không nhắc.
- `audit/review/screen_code.py`: khoá sổ là `"<KHOÁ> <Lxx> <scene_id> <step> <khối>"`. Xoá một bước (PR-01) làm lệch chỉ số bước của các khối mã phía sau.
- `nghe_thu_ket_qua.json` (chỉ đọc): 191 mục, khoá dạng `FND:L09:26` = khoá:bài:**số khung**. `lv.py:1059-1061` tạo một khung cho mỗi câu, nên xoá hoặc thêm một câu làm lệch mọi số khung phía sau. Phán quyết của người dùng sẽ trỏ sang câu khác sau khi dựng lại; `POST /api/nghe` "theo đúng lược đồ" kế thừa đúng điểm yếu này.
- `asr_reviewed`: gắn theo nguyên văn câu, xoá câu chỉ sinh cảnh báo E30 (`lv.py:683-685`), không gãy.

**Vì sao là lỗi.** Quy tắc điểm dừng không thực hiện được cùng D-10; người thực thi sẽ phải chọn bỏ một trong hai mà không có hướng dẫn. Trục `A2` tính từ khoá số khung sẽ gán "đã nghe" cho câu chưa ai nghe.

**Đề xuất sửa.** (1) Sửa lời đọc trên nhánh hoặc worktree riêng cho từng chặng, chỉ nhập về khi WP-2 + WP-3 + dựng lại xong; hoặc định nghĩa lại điểm dừng: "cổng nhanh đạt, trừ `find_stale_all` với danh sách bài chờ dựng ghi trong `STATE`". (2) Thêm vào WP-2/WP-3 danh sách việc đồng bộ sau mỗi bài: `sync_tpl_from_lesson --write`, cập nhật sổ `screen_code`, `prune_stale_asr`. (3) Trước khi dựng lại bài nào có phán quyết nghe, chuyển khoá phán quyết sang mã băm câu (hoặc tên tệp wav trong `out/_cache/tts/`); lược đồ `nghe.jsonl` của web dùng luôn khoá mới. Việc chuyển đọc tệp của người dùng và ghi ra tệp khác, không ghi đè (D-11).

---

### PR-14 · Phát âm: số liệu lệch nhau, 4/10 mục `fix` không phải lỗi từ điển, 7 mục `warn` bị bỏ, cổng `asr_flags` không bao giờ trượt, 5 359 mục tự động chưa có quyết định

**Trích.** Bảng mục 1: "người dùng nghe 15 câu ngày 27/11, 5 câu phải sửa" · WP-6.1: "Đưa 10 mục `fix` hiện có của người dùng vào từ điển đọc, mỗi mục một phép thử" · mục 11: "191 phán quyết tính tới 22:53 +07" · BN6-08: "`lexicon_regress.py`: mỗi mục `fix`… có một dòng trong từ điển và một phép thử" · BN6-07 phép đóng: "được người nghe hoặc được sửa từ điển rồi dựng lại" · WP-9: "cổng AF5 còn giữ".

**Bằng chứng (OBSERVED).**
- `nghe_thu_ket_qua.json` lúc tôi đọc: 191 mục = 174 `ok` + 10 `fix` + 7 `warn`. Con số "15 câu, 5 phải sửa" không khớp với hai chỗ khác của chính kế hoạch.
- Nội dung 10 mục `fix`: 3 mục về `ORA` (`BNK:L05:4`, `BNX:L28:66`, `ACB:L05:12`), 1 về `PostgreSQL` (`SPB:L04:30`), 2 về tên cờ lệnh (`FND:L07:24`, `:27`) là loại sửa được bằng từ điển. Bốn mục còn lại thì không: `DEN:L02:94` "thiếu phát âm từ đĩa" (âm thanh mất từ, phải tổng hợp lại câu); `RLN:L10:20` "trừ r B bị phát âm thành EB" (đọc ký hiệu); `HCI:L08:33` và `:41` "A-B-C thì đọc là A B C" (quy tắc đọc chuỗi chữ cái có gạch nối). Đòi "mỗi mục `fix` có một dòng trong từ điển" chắc chắn không đạt được với `DEN:L02:94`.
- 7 mục `warn` có ghi chú thật: "Oracle - o rơ cồ" (2 mục), "SQL - ét kiu eo", "vẽ đang đọc là về" (đọc sai từ thuần Việt, `ACB:L02:35`), `ksqlDB`. WP-6 và BN6-08 chỉ nói `fix`.
- `audit/review/asr_flags.py` dài 28 dòng, không có lệnh thoát mã khác 0: nó chỉ in danh sách. Cổng `[19]` của `final_gates_af5.sh` chỉ trượt khi tập lệnh sập. "0 câu ASR chưa xem xét" chưa từng là điều kiện cổng.
- 5 706 mục `asr_reviewed` (đếm lại: khớp), 5 359 có lý do sinh sẵn. Kế hoạch nói chúng không có giá trị chứng cứ nhưng không nói xoá, giữ, hay đánh dấu lại.
- `p7_asr_whitelist.out`: biểu đồ độ giống cộng lại 1 642 + 2 154 + 1 271 + 161 = 5 228, không bằng 5 359 lẫn 5 706; không có `p7*.py` để biết 131 mục còn lại là gì.
- BN6-07 cho đóng bằng "sửa từ điển rồi dựng lại" mà không nghe lại: đó là đóng bằng máy, đúng kiểu RC-5.

**Đề xuất sửa.** Thống nhất một con số có mốc giờ. Phân loại phán quyết nghe thành bốn loại xử lý: từ điển · quy tắc đọc (chữ cái, gạch nối) · tổng hợp lại câu · viết lại câu; `lexicon_regress.py` chỉ áp cho hai loại đầu, hai loại sau có phép thử riêng (tệp wav mới có độ dài ≥ ngưỡng theo số từ). Xử lý cả `warn`. Quyết định cho 5 359 mục: đổi nhãn thành `auto` và tách khỏi "đã xem"; sửa `asr_flags.py` trả mã 1 khi còn câu chưa xử lý, hoặc gỡ nó khỏi danh sách cổng và ghi rõ nó là báo cáo. BN6-07 chỉ đóng khi câu đã sửa được **nghe lại** (đưa câu sửa vào đầu hàng nghe).

---

### PR-15 · Chuyển dữ liệu `hoc_tap_v2`: mục 6.1 ghi sai hiện trạng; phép thử bỏ sót ghi chú và chuỗi ngày; nhật ký sự kiện thiếu quy tắc bền dữ liệu

**Trích.** 6.1: "Chưa có: bản đồ, các bước trong một bài, phần thưởng, huy hiệu, chấm lab từ web, **xuất/nhập tiến độ**" · BN6-09: "trạng thái mẫu `hoc_tap_v2` → nhật ký sự kiện, số bài đã học và lịch ôn giữ nguyên" · 6.2: "Nhật ký sự kiện chỉ ghi thêm `~/.hoc_tap/events.jsonl`".

**Bằng chứng (OBSERVED, `audit/review/learn_start/pack.py`).**
- Dòng 1065: `S = { v: 2, L: {}, N: {}, A: {}, cfg: { min: 60 } }`. `L[uid] = {t, b, due, r, f, last}` (ngày học, hộp ôn 1–7, hạn ôn, số lần ôn, số lần quên, lần ôn cuối); `N[uid]` = **ghi chú tự giảng của người học** (dòng 1180-1181); `A[ngày] = 1` = ngày có học, nguồn của chuỗi ngày (dòng 1077, 1100); `cfg.min` = mục tiêu phút mỗi ngày. Còn hai khoá khác: `hoc_tap_theme`, `hoc_tap_done_v1`.
- Dòng 1242-1257: trang hiện có **đã có** nút "Xuất tệp sao lưu" (`hoc_tap_tien_do_<ngày>.json`) và nhập tệp (kiểm `v === 2`, thay toàn bộ). `HOC_TAP.html` hiện tại chứa cả hai (`id="b-exp"`, `id="f-imp"`).
- Phép thử BN6-09 chỉ nêu "số bài đã học và lịch ôn". Không nêu `N` (thứ duy nhất người học tự viết, không tái tạo được), `A` (chuỗi ngày, liên quan trực tiếp tới phần thưởng "Ngày" và cột mốc 7/30/100 ngày), `cfg.min`, `r`, `f`.
- Thiết kế web mới (6.6) không có chỗ cho ghi chú theo bài.
- `localStorage` của trang cũ thuộc nguồn gốc `file://`; trang mới ở `http://127.0.0.1:<cổng>` không đọc được. Đường chuyển duy nhất là tệp xuất của trang cũ. Kế hoạch không ghi bước này (và ghi nhầm là chưa có).
- Nhật ký sự kiện: chưa nói về hai thẻ cùng ghi, dòng ghi dở khi máy tắt, đồng hồ máy bị chỉnh lùi (ảnh hưởng chuỗi ngày và lịch ôn), tần suất sự kiện khi xem video, nghĩa của "nhập" (gộp hay thay), khử trùng khi nhập hai lần.

**Đề xuất sửa.** Sửa 6.1. Ghi đường chuyển: "mở trang cũ bằng đúng trình duyệt đang dùng → Xuất tệp sao lưu → trang mới nhập tệp"; trang mới nhận đúng lược đồ `v: 2`. Phép thử BN6-09 so đủ `L` (cả `b`, `due`, `r`, `f`), `N`, `A`, `cfg.min`. Thêm ghi chú theo bài vào trang Bài học. Quy tắc nhật ký: mỗi sự kiện có `id` ngẫu nhiên và số thứ tự; ghi một dòng bằng một lần `write` rồi `flush` + `fsync`; khi đọc bỏ qua dòng cuối hỏng; nhập = gộp theo `id`; chuỗi ngày tính theo ngày địa phương ghi trong sự kiện; sự kiện xem video gộp thành khoảng, tối đa một dòng mỗi 15 giây; xoay bản sao lưu `events.jsonl.1`.

---

### PR-16 · "Học ngay được" cho 196 bài dựa trên một bài mẫu không ngẫu nhiên và trên hồ sơ đọc mà chính kế hoạch không còn nhận làm chứng cứ

**Trích.** 1.1: "**Học ngay được.** | 120 bài không đổi lời đọc so với mốc đã rà `5d7f329`; 76 bài đổi nhỏ (trung vị +32 từ)… Bài đổi nhiều nhất (`JV2 L09`) được đọc lại: 0 lỗi" · "Bắt đầu học Chặng 1 ngay hôm nay là an toàn" · bẫy 4: "Không dùng báo cáo của người đọc chưa qua hiệu chuẩn làm chứng cứ".

**Bằng chứng (OBSERVED).**
- Mẫu K có đúng 1 bài lớp A, chọn có chủ đích (đổi nhiều nhất), không phải ngẫu nhiên.
- "Mốc đã rà" là các lượt đọc trước AF5, cùng loại người đọc chưa hiệu chuẩn. PR-02 cho thấy 3 lỗi MUST của lớp B, C đã tồn tại ở chính mốc đó.
- 76 bài đổi: 8 bài thêm ≥ 100 từ, 3 bài thêm ≥ 300 từ (`JV2:L09` 560, `CS112:L28` 317, `BNK:L08` 308). 165 câu "thêm" của lớp A gồm 38 câu ở bước mới.
- Người dùng tự nghe: 5/10 mục `fix` thuộc lớp A (`FND:L07` ×2, `BNK:L05`, `BNX:L28`, `ACB:L05`) và 6/7 mục `warn` thuộc lớp A (`FND:L10`, `BNX:L06`, `BNX:L15`, `ACB:L02`, `ACB:L03`, `DMS:L07`).
- Lab lớp A: 196/196 không có ca ẩn (kế hoạch có ghi).
- Theo 5.1, cả 196 bài hiện là `G1` · `T0/T1` chưa xác định · `A0`, và bản đồ sẽ vẽ chúng với viền "đang rà".

**Vì sao là lỗi.** Khuyến nghị có thể đúng, nhưng căn cứ nêu ra yếu hơn chuẩn chứng cứ mà kế hoạch đặt cho mọi thứ khác; nếu lớp A có tỉ lệ lỗi thật là 10–20% thì n = 1 không thấy được.

**Đề xuất sửa.** Đổi chữ thành "Học được, nhãn `G1`; đã biết: phát âm sai ở các từ `ORA`, cờ lệnh; lab chưa chống in cứng". Thêm vào E1 một mẫu ngẫu nhiên phân tầng lớp A (đề nghị 12 bài: 6 trong 120 bài không đổi, 6 trong 76 bài đổi) do người đọc có mục vàng chấm; kết quả mẫu quyết định giữ hay hạ khuyến nghị.

---

### PR-17 · Ma trận năng lực (mục 8): 14 khoá không gắn với năng lực nào, yêu cầu bắt buộc của JD không có lab, một mục "thiếu" thực ra kho đã có

**Trích.** Mục 8 (bảng) · WP-8: "Ưu tiên: thống kê suy diễn…; học sâu thực hành; SQL phân tích; kỹ năng nghề của senior" · BN6-11: "mỗi năng lực có ≥ 1 lab nghề hoặc dự án làm bằng chứng".

**Bằng chứng (OBSERVED).**
- Dò mã khoá trong bảng mục 8: 14/53 khoá không xuất hiện: `ACB`, `AIF`, `BCH`, `CVI`, `ESY`, `GFX`, `HCI`, `INT`, `PRJ`, `RBM`, `RLN`, `ROB`, `SDP`, `SWF`. Trong đó `SWF` (đặc tả, kiểm thử, độ phủ, đồng thời) và `SDP` (mẫu thiết kế) là lõi kỹ nghệ phần mềm; `AIF` (tìm kiếm, suy luận, mạng Bayes) là nền AI cổ điển; `CVI`, `RLN` là hai nhánh AI lớn.
- Bảng WP-5 không có 24 khoá, gồm toàn bộ lõi Java/Spring/Oracle của JD: `JVA`, `JV2`, `BNK`, `BNX`, `SPB`, `BEP`.
- `resources/job/JD.md` (tin Software Engineer): "Bắt buộc… Ít nhất 3 năm làm việc với Stored Procedure (Oracle, MS SQL). Ít nhất 2 năm Java/SpringBoot…"; kiến thức: Swagger, Kafka/RabbitMQ, Redis, gRPC, TLS, Elasticsearch/Couchbase. `pack.py:130-152` đã có bảng `JD_MAP` nối 22 yêu cầu JD với bài cụ thể (thủ tục lưu trữ: `BNK:L05`, `BNX:L06`, `BNX:L37`; "đọc tài liệu tiếng Anh" đang được gán cho `DVO:L00`, `DVO:L09`, `SEP:L00`, là các bài không dạy việc đó). Ma trận mục 8 không dùng bảng này; dòng "Cơ sở dữ liệu và SQL" chỉ nêu PostgreSQL. `K4.md` ghi máy đang có sẵn hai container `mssql` và `oracle-free`.
- "**thiếu SQL phân tích**": `lessons/dan/L03_ham_cua_so.yaml` dạy `SUM(...) OVER`, `LAG`, `RANK` có `checks` chạy trên sqlite; `DAN L01–L05` là gộp nhóm, nối bảng nhân dòng, hàm cửa sổ, nhóm theo kỳ, phễu. Thứ thiếu là **thực hành** (13 lab `DAN` đều là `.py`, trung vị 6 dòng), không phải bài giảng.
- "Thiếu khoá thống kê suy diễn": bài rải ở `CS115 L13–15, L17, L44`, `DSC L06–L09, L12`, `DAN L10`, `SWF L10`. Nhận định "rải rác" hợp lý; tôi CHƯA KIỂM nội dung từng bài nên không khẳng định có đủ kiểm định giả thuyết hay không.
- Năng lực nền của kỹ sư senior chưa có dòng nào: đọc tài liệu kỹ thuật tiếng Anh (JD ghi rõ); kiểm thử và thiết kế mã (có khoá, không có dòng); lập trình đồng thời thực hành (`JV2`, `PAR`, `SWF L09`); đo và tối ưu hiệu năng (`SWF L10`); gỡ lỗi hệ thống đang chạy và quan sát (`CAS`, `CLD L11`, `DVO L10–L11`); làm việc nhóm qua Git (nhánh, yêu cầu hợp nhất, rà soát).

**Đề xuất sửa.** Dựng ma trận từ hai nguồn có sẵn thay vì từ tên bài: `JD_MAP` của `pack.py` và 16 lộ trình của `tracks.yaml`; mỗi khoá phải thuộc ít nhất một dòng, hoặc được ghi rõ là "tuỳ chọn, không tính vào đích" (Chặng 11 đã tự ghi "tuỳ chọn"). Thêm dòng: kỹ nghệ phần mềm (`SWF`, `SDP`), AI cổ điển (`AIF`), thị giác và học tăng cường (`CVI`, `RLN`), thủ tục lưu trữ Oracle/SQL Server, hàng đợi và bộ đệm thực hành, đọc tài liệu tiếng Anh. Đổi "thiếu SQL phân tích" thành lab nghề `DAN` (đã có trong WP-5 dòng `DAN` `DSC`) và bỏ khỏi danh sách khoá mới của WP-8. Thêm dòng WP-5 cho Chặng 1–5 (ví dụ: thủ tục lưu trữ trên `oracle-free`/`mssql` trong Docker; `SPB` với PostgreSQL/Redis/Kafka thật như WP-2 đã nêu).

---

### PR-18 · Việc được hứa mà không gói việc nào làm; khối lượng lớn không được ước lượng

**Trích.** 5.3 `G-SHOW` · 5.1 "`labs/CONTRACT.yaml` bản 3" · 6.2 "`POST /api/nghe`… vào tệp riêng `~/.hoc_tap/nghe.jsonl`" · WP-6, WP-7 nghiệm thu: "`lexicon_regress.py` đạt", "`quiz_verify.py` 100%" · WP-0.4 · mục 9: "thứ tự, không phải cam kết thời gian".

**Bằng chứng (đối chiếu các mục; số liệu OBSERVED).**

| Lời hứa | Thiếu gì |
|---|---|
| `G-SHOW` (147 bước `show` rỗng ở 99 bài; 5 bài lệch khung sáng trong mẫu) | Không gói việc nào sửa; nghiệm thu WP-2, WP-3 không liệt kê `G-SHOW` |
| `CONTRACT.yaml` bản 3, `cham.sh`/`lab_gate.py` nhận lab nghề | Không bước nào (PR-07) |
| `nghe.jsonl` từ nút báo lỗi phát âm | Không bước nào đưa nó vào `lexicon_regress.py` hay hàng nghe; BN6-08 chỉ đọc `nghe_thu_ket_qua.json` |
| `lexicon_regress.py`, `quiz_verify.py` | Chỉ xuất hiện ở nghiệm thu, không có bước "viết" và không có phép thử cho chính chúng |
| Nhãn ba trục theo bài trong `quality.yaml` bản 2 | `pack.py:107-128` đọc lược đồ theo khoá (`label`, `segments`); `HOC_TAP.html` còn là trang dự phòng tới W3 nên `pack.py` phải đọc được lược đồ mới. Không bước nào sửa `pack.py` |
| Kiểm lại 41 lỗi Mẫu K chưa kiểm | Không bước nào (PR-06) |
| "Ghi lại 8 phép đo `af6/p1…p8` làm mốc" (WP-0.2) | `p6` và `p7` chỉ có tệp `.out`, không có tập lệnh; không chạy lại được |

Khối lượng không có trong kế hoạch (tôi tính từ số đo của kế hoạch):
- Đọc có hiệu chuẩn: 806 bài + mẫu đối chứng khoảng 20% mỗi khoá, tối thiểu 3 (≈ 180 bài) + ≥ 60 bài ở WP-9 + các vòng đọc lại. Mẫu K: 4 tác tử đọc 32 bài trong khoảng 20–30 phút. Ở mức 4 tác tử cùng lúc, riêng lượt đọc đầu là khoảng 25 lượt như vậy.
- 7 934 phán quyết câu, cộng phán quyết cho `show` (PR-02).
- Lab tầng 1: 597 lab × (đề 5 mục + ≥ 1 ca mới + 2 biến thể sai) ≈ 1 200 biến thể; cộng 196 lab lớp A nếu giữ điều kiện `T1`.
- Câu hỏi: 806 × 3 = 2 418 câu, 10% do người đọc làm thử.
- Lab nghề: ≈ 41 lab trong bảng + 22 lab Chặng 10–11 + 11 dự án `PRJ`, mỗi lab cần một người đọc làm thử từ đề.
- Dựng lại: 777 bài trở lên. Theo số kế hoạch trích (526 bài trong 56 840 giây = 108 giây/bài) là 23–24 giờ máy chưa kể ASR; lời mới (thẻ, câu sửa) phải gọi dịch vụ đọc, có hạn mức (sổ nhớ dự án: "on quota/rate-limit blocks, re-check every 1 h").
- Nghe bằng tai: nhóm 1 của WP-6.2 chưa có con số.

**Đề xuất sửa.** Thêm bảng "lời hứa → gói việc → nghiệm thu" và lấp các dòng trống ở trên. Thêm cột ước lượng khối lượng (số bài, số lab, số lượt đọc, giờ máy) cho từng phiên E; đo kích thước nhóm 1 của hàng nghe trước khi hứa "100% nhóm 1".

---

## Mức THẤP

### PR-19 · Số liệu lệch nhỏ

**Trích và bằng chứng (OBSERVED).**

| Kế hoạch ghi | Kho/tệp `.out` cho thấy |
|---|---|
| 1.1: "Chặng 6–11 lớp C (**34 khoá** + `CS115 L22–L43`)" | 53 khoá − 10 khoá lớp A − `CS115` − 4 khoá lớp B − 3 khoá mới = **35 khoá**; cộng số bài của 35 khoá trong `p3_labs.out` ra 514, thêm 22 bài `CS115` = 536 (số bài đúng, số khoá sai) |
| RC-6: "**53 dòng** `quality.yaml` cùng một câu chứng cứ" | 54 dòng (52 khoá + 2 đoạn của `CS115`); `grep -c` = 54 như kế hoạch ghi ở cột bên |
| RC-4: "422/806 báo cáo chấm điểm tối đa" | `p1_read_reports.out` có thêm 11 dòng cùng điểm tối đa viết dạng "Tổng=14/14": 433 |
| WP-2: "vì 11/17 lỗi của khoá mới là mục tiêu ghi 'Đo/Cài/…'" dùng làm lý do viết lại `BEP`, `AIP` | `BEP` + `AIP` chỉ có 10 lỗi MUST (2 + 2 + 4 + 2); 11 lỗi loại đó tính trên cả 7 bài, gồm `SPB` |
| BN6-01: "Mọi bài lớp B, C… 7 934 câu"; WP-2: "614 bài có câu thêm" | 7 934 = 165 (lớp A, 58 bài) + 1 830 (lớp B, 45 bài) + 5 939 (lớp C, 511 bài). Lớp A không thuộc diện xoá mặc định |
| BN6-07: "Âm thanh 738 bài" | 748 bài có `asr_reviewed` (đếm lại); 738 có lẽ là số bài có mục tự động, tệp `.out` không ghi rõ |
| D-10: "khoảng 16–24 giờ máy" | 108 giây/bài × 806 = 24,2 giờ; cận dưới 16 giờ không có căn cứ trong nguồn trích |
| Dòng đầu: "mọi con số dưới đây có lệnh và đầu ra trong `af6/`" | `p6_lab_by_stage.out`, `p7_asr_whitelist.out` không có tập lệnh. `AGENTS.md` ghi "`p1`…`p9`", thư mục chỉ có tới `p8` |

Các số tôi đối chiếu và **khớp**: 48 lỗi ở 26/31 bài (cộng bốn bảng tổng: 7 + 6 + 18 + 17; số bài có lỗi 6 + 5 + 8 + 7); lớp C 11/16 bài, 13 lỗi; lớp B 8/8, 18; khoá mới 7/7, 17; 196 + 536 + 45 + 29 = 806; 7 934 câu / 198 664 từ / 614 bài / 343 bài ≥ 10 câu / 1 490 câu ở 336 bài / 153 (dựng lại độc lập ra đúng 7 934); 9 câu ở ≥ 100 bài, 514 bài; 378 bài ≥ 50%; 443 và 368/429; trung vị 9 dòng, 290 lab một dòng; 5 706 và 5 359; 1 432 = 1 271 + 161; 179/179; 593 lời hẹn; 56/56; 10 474,9 phút; 16 lộ trình; 10 mục `fix`; 191 phán quyết; 6/8 lab lớp B; 5 bài lệch khung sáng.

**Đề xuất sửa.** Sửa tám dòng trên; bổ sung tập lệnh cho `p6`, `p7`.

---

### PR-20 · 5.2.3 ghi "bổ sung" một loại lỗi vốn đã có trong chuẩn AF5

**Trích.** 5.2.3: "Định nghĩa lỗi bắt buộc sửa bổ sung ba loại mà đợt AF5 xếp nhẹ: câu khẳng định tuyệt đối sai điều kiện; …".

**Bằng chứng (OBSERVED).** `audit/review/audit_final/BRIEF_AF5.md:27`: "MUST… 2. Khẳng định tuyệt đối sai điều kiện hoặc bịa kết quả chưa chạy/không có nguồn." Dòng 30 cũng đã có cảnh Tự làm rỗng.

**Vì sao là lỗi.** Chuẩn đã có, người đọc không áp. Viết thành "bổ sung" làm lệch chẩn đoán: vấn đề là thi hành (RC-4), không phải định nghĩa; thêm định nghĩa sẽ không chữa được.

**Đề xuất sửa.** Viết lại: "ba loại đã có trong `BRIEF_AF5.md` nhưng không được áp; `BRIEF_AF6.md` kèm ví dụ thật từ Mẫu K cho từng loại và mục vàng cài đúng ba loại này".

---

### PR-21 · Các chi tiết web còn mơ hồ hoặc tự trái nhau

**Trích và nhận xét.**
- 6.2: "5 đường API". Thiếu ít nhất: nhập tiến độ (kế hoạch hứa "xuất/nhập"), hỏi trạng thái việc chấm (PR-10), danh sách hàng nghe (W4). Con số 5 không giữ được.
- 6.5: "'rương ngày' mở ra 10–50 điểm" so với W3: "phát lại nhật ký sự kiện cho ra đúng điểm (tất định)". Phần thưởng ngẫu nhiên phải ghi số điểm vào sự kiện hoặc sinh từ hạt giống = mã băm (ngày + mã người học).
- 6.4: "⑤ Ôn… giữ sao khỏi mờ" so với nguyên tắc "không đếm ngược gây sợ mất". Sao mờ dần là cơ chế sợ mất.
- 6.5: cột mốc "806 bài" và "Senior nền tảng" cố định trong khi WP-8 thêm khoá và người học chọn một trong 16 lộ trình; cột mốc cuối nên tính theo lộ trình đã chọn.
- W2: "6 kịch bản đầu-cuối đạt", W3: "Thêm 6 kịch bản": không liệt kê kịch bản nào, nên không kiểm được.
- W6: "tương phản ≥ 4,5:1": không nêu công cụ đo; web "không tải gì từ mạng" nên công cụ phải nằm sẵn trong kho.
- 6.2 "Dự phòng: `HOC_TAP.html`… cho tới khi web mới qua nghiệm thu W3": web mới cần `hoc.cmd` và Python; trang tĩnh mở bằng nhấp đúp. Mô-đun JavaScript không nạp được qua `file://` trên Chromium, nên `web/` không có chế độ mở trực tiếp. Nên giữ trang tĩnh vô thời hạn làm đường lui.
- `catalog.json`: `HOC_TAP.html` hiện nặng 6,26 MB cho 806 bài (không có ảnh nhúng). Chưa có ngân sách kích thước cho `catalog.json`; kích thước thật CHƯA KIỂM vì chưa có tệp.
- `G-ROOT` thêm ở WP-0.3 trước khi có `web/`, `hoc.py`, `hoc.cmd`: danh sách cho phép phải tính trước ba mục này.

**Đề xuất sửa.** Liệt kê API theo việc, không theo con số; ghi 12 kịch bản đầu-cuối thành danh sách có tên; quyết định "sao mờ" hay "nhắc ôn không phạt".

---

### PR-22 · D-10 "mỗi bài chỉ dựng lại một lần" không giữ được; `G-ROOT` được áp trước khi có phép thử

**Trích.** D-10: "Mỗi bài chỉ dựng lại video **một lần**" · WP-0.3: "Thêm `G-ROOT`" · 5.3: "Mọi cổng mới có phép thử dương và âm trong `tests/` trước khi áp vào kho" (việc viết phép thử nằm ở WP-1.1).

**Bằng chứng.** Người dùng vẫn đang nghe (191 phán quyết và tăng). Mỗi mục `fix` mới ở một bài đã dựng xong là một lần dựng nữa; sửa từ điển cho một từ dùng chung làm `tts_sha256` của mọi bài chứa từ đó đổi (`find_stale_all.py:23-24`), kể cả bài lớp A vừa dựng ở E5. Lỗi do mẫu đối chứng tìm ra (5.2.4, tối đa 2 vòng) cũng dẫn tới dựng lại.

**Đề xuất sửa.** Đổi D-10 thành "gom mọi sửa đã biết của bài trước khi dựng; sửa phát sinh về sau gom theo đợt mỗi chặng". Chuyển `G-ROOT` sang WP-1 hoặc ghi rõ nó là ngoại lệ có phép thử viết ngay tại WP-0.

---

## Những điểm kế hoạch làm đúng

- Bác tuyên bố "100%" bằng mẫu đọc lại độc lập có hạt giống và ghi rõ phần nào là CITED; bốn bảng tổng của Mẫu K cộng đúng 48 lỗi ở 26/31 bài.
- Tìm đúng nguyên nhân gốc RC-1 (sàn độ dài sinh câu độn) và tự nhận phần lỗi của kế hoạch AF5; phép đo `p8` dựng lại độc lập ra đúng 7 934 câu.
- Tách thực hành khỏi video (D-3) là hướng đúng: lab sửa bằng chữ, không phải dựng lại video.
- Giữ `nghe_thu_ket_qua.json` là tệp của người dùng (D-11); `/api/nghe` ghi sang tệp khác.
- Có mục 11 liệt kê phần chưa kiểm, và BN6-14 tự nghi ngờ phép đo của mình (tôi đã đo: độ bắt của `p8` là 7/21).
- Yêu cầu chạy thật kịch bản web bằng Playwright với Edge; `tools/lv.py:1336` đã dùng `launch(channel="msedge")`, `requirements.txt` có `playwright==1.64.0`.
- Mười hai bẫy ở mục 10 khớp với lỗi thật của các đợt trước (không quá 4 tác tử, không chạy lời giải ở gốc kho, không tin mã thoát của lệnh gộp).
- Thứ tự theo đường người học đi (D-9) và nguyên tắc "sự thật trước, gỡ nhãn" (D-1) là đúng; lỗi nằm ở chỗ các điểm dừng chưa khớp với nguyên tắc đó (PR-04, PR-08).

## Việc chưa kiểm được

| Việc | Lý do |
|---|---|
| Bộ cổng `day_du` và cả bộ `nhanh` tại `a3039c1f` | Không chạy lại (đề bài cấm build; `nhanh` tôi chỉ đọc `gates_nhanh.out`) |
| 41/48 lỗi Mẫu K | Tôi chỉ dò câu trích có trong tệp bài hay không (PR-02), không chạy lại bằng chứng của từng lỗi |
| `p6` (443, 368/429) và `p7` (5 359, biểu đồ độ giống) | Không có tập lệnh. Kiểm gián tiếp: 452 lab `.py` có lời giải ≤ 12 dòng (phù hợp với 443 sau khi trừ lab dùng thư viện ngoài); 5 706 mục `asr_reviewed` khớp |
| Mẫu 20 câu ở PR-01 | Phân loại giữ/xoá là nhận định của một người đọc, n = 20; tôi không chạy mã để kiểm tính đúng của từng câu |
| Mọi nhận định về web (PR-09 phần trình duyệt, PR-10, PR-15, PR-21) | Chưa có dòng mã nào của `hoc.py`/`web/`; đây là rà thiết kế. Riêng các số (tỉ lệ `pause`, kích thước video, cấu trúc `hoc_tap_v2`, `cham.sh`) là OBSERVED |
| Playwright khởi động Edge được trên máy này | Không chạy thử (tránh mở trình duyệt); chỉ thấy gói có trong `.venv` và mã `lv.py` dùng kênh `msedge` |
| `kiem_ham.py --py-du-an` có nhặt tệp trong `kiem/ne/` làm ca kiểm hay không | Chưa đọc `labs/kiem_ham.py` |
| Nội dung từng bài thống kê, học sâu để khẳng định "thiếu khoá" (PR-17) | Chỉ đọc tiêu đề giáo án và `DAN L03` |
| Phiên bản `SPB` (Spring Boot 4.1.3), `K8s` cục bộ, dung lượng `catalog.json` | Không kiểm |
| `nghe_thu_ket_qua.json` | Đọc lúc tệp có 191 mục; tệp đang được người dùng ghi nên số có thể đã đổi |

