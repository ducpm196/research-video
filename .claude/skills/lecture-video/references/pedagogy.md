# Khung sư phạm cho người mới / mất gốc (dùng khi viết `lessons/*.yaml`)

Quay lại: SKILL.md, Bước 3.

## 1. Thứ tự phân cảnh chuẩn (10 nhịp)

| # | kind | Mục đích | Câu hỏi người học đang nghĩ |
|---|---|---|---|
| 1 | `hook` | Vấn đề thật, vì sao cần học; nêu 2–3 câu hỏi bài sẽ trả lời | “Học cái này để làm gì?” |
| 2 | `prereq` | Ôn đúng các phép tính sẽ dùng (bình phương, căn, phân số, số âm…) bằng ví dụ số | “Mình có đủ nền không?” |
| 3 | `symbol` | Giải mã **từng** ký hiệu: hình dạng → cách đọc → nghĩa → ví dụ số | “Cái ký hiệu lạ này là gì?” |
| 4 | `concept` | Khái niệm bằng lời thường trước, công thức sau | “Nó nghĩa là gì?” |
| 5 | `intuition` | Hình ảnh/ẩn dụ đời thường (cái bóng, máy cộng dồn, mũi tên) + hình SVG | “Hình dung nó thế nào?” |
| 6 | `formula` | **Suy ra** công thức từ một điều kiện, không đưa công thức từ trên trời | “Công thức từ đâu ra?” |
| 7 | `example` | Ví dụ số, **mỗi phép tính một step**, tô màu cùng màu với công thức | “Áp dụng thế nào?” |
| 8 | `check` | Cách tự kiểm tra kết quả (ít nhất 1 phép thử độc lập) | “Sao biết mình đúng?” |
| 9 | `pitfall` | 3–4 lỗi thật hay gặp, mỗi lỗi chỉ ra **phép thử nào bắt được nó** | “Mình hay sai ở đâu?” |
| 10 | `quiz` → `recap` | Bài tự làm (`pause`) + đáp án từng bước; chuỗi logic + tư duy + nối sang bài sau | “Mình đã hiểu chưa? Tiếp theo là gì?” |

## 2. Luật viết cho người toán yếu
1. **Một step = một ý.** Nếu cần chữ “và” để mô tả step thì tách đôi.
2. **Lời trước, ký hiệu sau.** Nói ý bằng lời thường, rồi mới hiện ký hiệu, rồi đọc ký hiệu thành lời.
3. **Ký hiệu nào cũng phải được đọc to** ít nhất một lần (“hai vạch đứng kép là độ dài”).
4. **Con số nhỏ, chẵn.** Ví dụ chọn sao cho kết quả là số nguyên (10/5 = 2), trừ khi đang minh hoạ lỗi.
5. **Dùng lại số.** Con số tính ở phần trước (vd 56) được dùng lại ở phần sau để người học thấy các phần nối nhau.
6. **Màu có nghĩa cố định trong bài:** xanh = tử số/đầu vào, đỏ = mẫu số/cảnh báo, cam = ẩn số đang tìm, lục = kết quả.
7. **Tư duy suy ra thay vì học thuộc:** mỗi bài chốt “một điều kiện cần nhớ” mà từ đó suy ra công thức.
8. **Nối bức tranh lớn:** hook và recap đều nói bài này đứng ở đâu trong chuỗi Biểu diễn → Dự đoán → Sai số → Tối ưu.
9. **Không lặp lại lỗi của nguồn:** đọc `fix` trong curriculum và `audit/AUDIT_*.md` trước khi viết.
10. **Nhịp:** 130–160 từ/phút; bài 10–15 phút; mỗi 2–3 phút có một ví dụ số hoặc câu hỏi.

11. **Phép toán nền trước suy luận.** Bất kỳ bước nào dùng một phép toán (cộng/trừ vector, nhân với số, chuyển vế, phá ngoặc) thì phép toán đó phải được dạy kèm ví dụ số ở phần trước. (Lỗi thật ở L01 v1: viết `z = y − c·u` khi chưa dạy trừ vector.)
12. **Mỗi bước biến đổi có lý do + làm thử bằng số.** Mẫu: “Bước 2. *Vì* y = bóng + z (hình nối đuôi), *chuyển vế* được z = y − c·u” rồi đến “Làm thử ngay: z = (6 − c, 2 − 2c, 4)ᵀ, zᵀu = 10 − 5c = 0 ⇒ c = 2”. Cho hai cách (thay số trực tiếp, dùng công thức) khớp nhau.
13. **Mọi dấu phụ của ký hiệu phải được đọc tên:** chỉ số dưới (‖x‖**₂** = chuẩn L2), số mũ (‖u‖**²** = bình phương), chữ nhỏ dưới chân (proj**ᵤ** = chiếu lên u), dấu chấm giữa (· = nhân), hai chữ viết sát nhau (u₁v₁ = nhân). Người mất gốc sẽ thấy “dư số 2” nếu không ai nói số 2 đó là gì.
14. **Quy ước ký hiệu của bài** ghi ở đầu file đặc tả (độ dài, chuyển vị, dấu nhân, cách viết vector ngang có ᵀ) và giữ nguyên trong cả bài. Muốn nhắc tới kiểu viết của sách khác thì làm trong một step `notation_note: true`.
15. **Phát biểu chính xác, không nói gần đúng:** ví dụ “tích vô hướng dương ⇔ góc nhọn” (không viết “gần cùng hướng”), kèm điều kiện (hai vector khác vector không). Có `checks` cho phát biểu đó khi kiểm được bằng máy.

16. **Bảng phải tự đủ sau mỗi `clear`.** Khối nào nói “ở trên”, “lúc nãy” hoặc dùng số của một ma trận/vector thì đối tượng đó phải đang hiện trên bảng (nhắc lại dạng nhỏ nếu cần). Khi cùng một chữ được dùng cho cả dạng tổng quát (a, b, c, d) và dạng số, ghi rõ dạng số bên cạnh. (Lỗi thật L02 v1: “x₁₂ = 2 với X ở trên” khi X đã bị xoá; X lại có hai số 2.)

17. **Trích dẫn bài khác phải tự hiểu được** (lint E22–E24; người dùng yêu cầu 2026-10-24). Số “bài N” = thứ tự học trong `curriculum/*.yaml` (L00, L01, … tịnh tiến; `lv.py curriculum` chặn nhảy cóc).
    - **Bài trước:** nói lại kiến thức đó là gì, không nói tắt. Sai: “Bài 5 đã có gradient.” Đúng: “Ở bài 5, ta đã tính gradient của hàm này, gồm hai thành phần 2x − y + 1 và 2y − x − 1.” Sai: “tính theo công thức của bài 1”. Đúng: “theo công thức cái bóng của bài 1, tích vô hướng chia cho độ dài bình phương”.
    - **Bài sau:** người học CHƯA học. Chỉ nhắc ở `hook` (vì sao cần), `in_ai` và `recap` (gặp lại ở đâu, bài sau học gì). Mỗi lần nhắc phải giải thích bằng lời thường, không dùng thuật ngữ chưa dạy. Sai: “Cực trị (bài 7) xét dấu trị riêng của ma trận đạo hàm cấp 2”, nói trong bài 4 khi người học chưa biết đạo hàm. Đúng: “Ở bài 7, muốn biết một điểm là đáy hay đỉnh, ta xét dấu các trị riêng của một ma trận mô tả độ cong.” Step đó đánh dấu `forward_ref: true`.
    - **Không nhắc bài sau giữa phần giảng.** Trong `symbol`, `formula`, `example`… phải nói trọn ý tại chỗ. Sai: “đó là điểm dừng (bài 7)”. Đúng: “chỗ bằng phẳng theo mọi hướng như vậy gọi là điểm dừng”.
    - **Tên thuật toán của bài sau** (PCA, hồi quy tuyến tính, lan truyền ngược…) không đứng trống: kèm một cụm giải thích, ví dụ “PCA, một cách nén dữ liệu”, “hồi quy tuyến tính, cách dự đoán giá nhà từ dữ liệu”.
    - Khi đánh số lại lộ trình, sửa mọi “bài N” trong các bài đã làm rồi dựng lại video. Lint chặn số không có trong lộ trình nhưng không chặn số sai chủ đề, nên phải đọc lại từng chỗ.

18. **Người học CHỈ có video** (người dùng yêu cầu 2026-10-27, lint E29). Không nhắc thứ họ không có: “tài liệu gốc viết…”, “tài liệu dòng 266”, “slide môn học”, “bài báo gốc”. Sai: “Tài liệu gốc viết giảm dần về 0, cách viết đó chưa chính xác.” Đúng: “Bạn có thể nghe cách nói sai số giảm dần về 0. Nói vậy chưa chính xác, vì ở đây sai số tổng nhỏ nhất vẫn còn khoảng 0,066.” Khác biệt ký hiệu: “Nhiều sách viết …”. Cần nguồn thì gọi tên đủ để tra được: “bài báo năm 2015 của hai tác giả đề xuất Adam” (màn hình ghi Kingma & Ba, 2015). Số dòng nguồn chỉ để ở `source:`/`fix`.

19. **Người xem luôn biết câu đang nói chỗ nào** (lint E31/E32). Bước có ≥3 câu nói về một khối ≥3 phần phải có `focus:` — mỗi câu một mục, trỏ đúng phần (dòng, công thức, hàng của bảng) mà câu đó đang nói; câu nói chung về cả khối ghi `0`. Phần được trỏ có viền cam, các phần khác trong khối mờ đi, nên mắt đi theo lời. Không trỏ vào một chữ in đậm giữa câu (chữ thường xen giữa không mờ được); trỏ cả dòng.
    ```yaml
    - show: |
        <p>Nhà A, giá thật $y = 20$:</p>
        <table class="t">…3 lần thử…</table>
        <div class="box key">Quy tắc tự sửa: …</div>
      focus: [2, 3, 3, 3, 0]     # câu 1 → bảng; câu 2–4 → hộp quy tắc; câu 5 nói chung
      say: "Đặt ba lần thử cạnh nhau, ta rút ra quy tắc tự sửa. Nhích w một chút rồi xem sai số. …"
    ```

20. **Kinh nghiệm chuyên gia, không chỉ định nghĩa** (người dùng yêu cầu 2026-10-30). Hook mở bằng một tình huống người làm nghề thật gặp, có con số ("8 GPU mà chỉ nhanh gấp 3", "đơn 42 đặt lúc 9 giờ mà 9 giờ 20 mới có thư"). Pitfall nêu điều chuyên gia làm khác người mới: đo trước khi sửa, hỏi "đúng vì lý do sai không?". Bài cuối mỗi khoá là bài tình huống chuyên gia; khoá CAS phân tích sự cố có thật. Xem references/case-lessons.md: chỉ khẳng định điều nguồn gốc ghi, tính lại con số của báo cáo, không đổ lỗi cá nhân.

21. **Một từ một cách viết, một khoá một kiểu** (lint E38, `check_meta.py`). Chính tả theo `SPELL_CANON`; tên chuỗi (`series`), giọng, tốc độ giống nhau trong cả khoá; bản đồ khoá ở bài 0 phải liệt kê đủ mọi bài, kể cả bài thêm sau (E37).

22. **Chuẩn độ sâu cho người mới / mất gốc** (người dùng yêu cầu 2026-10-31; lint E39 khi bài khai `depth: full`; đo toàn kho bằng
    `audit/review/pedagogy_scan.py`). Lỗi thật: 270 bài của 19 khoá dựng đợt 2026-10-28…30 chỉ có 6 phân cảnh, 1 step ví dụ, 0 hình,
    ≈ 4,5 phút: đúng, nhưng là bản tóm tắt cho người đã biết, không phải bài giảng cho người mất gốc. Một bài `depth: full` phải có:
    - `prereq`: ôn đúng kiến thức sẽ dùng, mỗi điều một ví dụ số (nhắc bài trước thì nói lại nội dung — luật 17);
    - `intuition` hoặc `concept` có **hình cơ chế** (`<svg>`): người mới phải THẤY dữ liệu đi đâu, cái gì được lưu, cái gì chờ cái gì;
    - `formula`/`concept` **suy ra từng bước**, mỗi bước một lý do và một lần “làm thử” bằng số nhỏ (luật 12);
    - ≥ 4 step làm bằng số (`example` + `check`), mỗi phép tính một step, dùng lại số của phần trước (luật 5);
    - `check`: kiểm bằng **đường khác** (nhân thẳng, đếm lại, đơn vị khác) — không phải đọc lại kết quả;
    - `pitfall` có ít nhất một lỗi của **người đã đi làm** (kiểu “gộp lô tưởng nhanh gấp 16”), không chỉ lỗi của người mới;
    - `quiz` có `pause` rồi ≥ 2 step đáp án giải từng bước; câu cuối nên là một **quyết định** (thẻ 80 GB phục vụ mấy chuỗi?);
    - `recap` có chuỗi logic; không quá 3 khung liền chỉ có chữ (xen bảng, hình, công thức); lời giảng ≥ 900 từ (≈ 6,5 phút).
    Mẫu đã dựng: `lessons/llm/L05_chi_phi_tinh_toan.yaml` (4,4 → 9,7 phút; 0 → 2 hình; 1 → 10 step số).

23. **Bài hành trình theo trục thời gian** (người dùng yêu cầu 2026-10-31; lint E40 khi bài khai `case: journey`): kinh nghiệm chuyên gia
    được kể như **lịch sử có thật của một hệ thống**, từ lúc khai sinh → tăng trưởng → quy mô lớn → ổn định → tiếp tục phát triển. Mỗi chặng:
    quy mô lúc đó (có nguồn) → điểm nghẽn quy mô ấy làm lộ ra → chuyên gia xử lý thế nào → thực hành tốt rút ra, kèm điều kiện áp dụng →
    một con số tính lại bằng kiến thức đã học. Xem references/case-lessons.md mục 5; mẫu: `lessons/cld/L15_hanh_trinh_borg_kubernetes.yaml`.

24. **Đào sâu tại chỗ một bài đã dựng** (quy trình đợt A, 2026-10-31; đã làm AIF 14, LLM 14, SWF 13 bài). Giữ nguyên nội dung đã
    kiểm chứng (hook, ký hiệu, `checks` cũ, lỗi thường gặp, recap) và **thêm** cho đủ luật 22:
    1. Sao lưu bài vào thư mục nháp; viết script vá bằng Python (Write, không heredoc) với `rep(a, b)` khẳng định `a` xuất hiện đúng 1 lần.
    2. `depth: full` sau `rate:`; thêm `prereq` trước `sym` (nói lại kiến thức đã học kèm một ví dụ số; khoá khác thì nói “ở khoá …”,
       **không** viết “bài N” của khoá khác — E22 hiểu là bài của khoá này); thêm `intuition` có `<svg>` trước `example`.
    3. Tách `example` thành ≥ 4 step, mỗi phép tính một step có chữ “Bước N”; thêm `clear: true` khi bảng dài; thêm `check` kiểm bằng
       **đường khác** (dò từng ô, liệt kê, đếm thẳng, máy thử hết các ca nhỏ), mỗi con số có `checks`.
    4. Đề `quiz` dạng `<ol>` đổi thành bảng (tránh chuỗi > 3 khung chữ); đáp án tách ≥ 2 step, mỗi câu giải từng bước.
    5. Dưới 900 từ thì thêm **Lỗi 4 của người đã đi làm** (kèm bảng số và `checks`), có `clear: true` để khỏi tràn khung.
    6. Chạy `audit/review/prune_stale_asr.py`, `lv.py lint` (0 FAIL, 0 WARN), `audit/review/text_runs.py`, rồi **`lv.py render`** riêng
       (≈ 20 s, không cần TTS) tới khi báo “(0 vấn đề)” — lint KHÔNG bắt được tràn khung và chữ đè trong hình; đợt A có 14/17 bài SDP,
       8/15 CLD, 7/15 SEC, LLM bài 12, SWF bài 0–1 chỉ lộ lỗi này ở render (sửa: `clear: true` ở step đáp án đầu hay bảng dài, dời nhãn SVG).
       Xong mới dựng qua hàng đợi.
    Thêm (đợt A, các tác tử phụ): `P(...)` trong công thức kích hoạt ký hiệu xác suất `prob`; `\Rightarrow` cần `introduces: [implies]`;
    `\tfrac` không có trong sổ ký hiệu (dùng `\frac`); thay chuỗi bằng `python -c` làm `\f` của `\frac` thành ký tự form-feed — quét
    ký tự điều khiển trên mọi tệp bài sau mỗi đợt sửa.
    `checks` không được đặt **cận trên thời gian thật** (đo bằng đồng hồ: `Date.now`, `perf_counter`) — lint chạy lúc hàng đợi dựng đang tải
    nặng nên sẽ trượt ngẫu nhiên (WEB L04, 2026-10-31). Dùng cận dưới (bộ hẹn giờ bảo đảm) và so sánh tương đối (song song < tuần tự),
    hoặc mô phỏng tất định; thứ tự in của vòng lặp sự kiện thì tất định, giữ được.
    7. Bài sinh từ mẫu (`audit/<khoá>/src/*.tpl.yaml`, điền bằng `fill_all.py`): sửa bài xong phải chạy
       `audit/review/sync_tpl_from_lesson.py <khoá> --write` (chỉ ghi khi điền ngược khớp từng byte) — nếu không, lần chạy `fill_all` sau
       GHI ĐÈ mất phần đào sâu. Lỗi thật 2026-10-31: SWF L07, DBS L06/L08/L12/L16 lệch mẫu; rà thêm thấy mẫu cũ CS112 L14, CS115 L44,
       hình NET L10 (nhãn sửa trên bài, không sửa ở bộ sinh hình). `audit_all.py` nay báo mọi mẫu lệch bài.
    Bẫy đã gặp: `focus` phải đúng số câu của `say` (E31); ký hiệu mới cần `introduces` ở step đầu dùng nó, kể cả `cdot`, `geq`, `dots`,
    `implies`, `power` (id phải có trong `symbols.yaml` — không có `fact`, `leq` là `geq`); ký tự `·`, `′`, `✗` trong chữ thường hay trong
    SVG bị chặn (dùng lời hoặc `$…$`; `$` trong SVG bị E51 chặn); `e^{-1}` kích hoạt ký hiệu nghịch đảo — viết `\frac{1}{e}`; câu nói “dòng 1”
    bị E29 coi là trích dòng nguồn — nói “dòng đầu”; từ tiếng Anh chưa thử ASR (for, range) không được vào lời đọc; trong YAML chuỗi
    nháp kép không được có `\'`; **đọc lại đáp án cũ khi tách step** — SWF bài 7 đáp án cũ bỏ sót một vi phạm đống (vị trí 4), chỉ lộ ra
    khi lập bảng từng cặp; tệp lý do HAND phải là tệp **mới** (Write từ chối ghi đè tệp chưa đọc, và lệnh chèn sẽ chèn nội dung cũ).

## 3. Mẫu step giải mã một ký hiệu
```yaml
- show: |
    $$\sum_{i=1}^{3} i = 1 + 2 + 3 = 6$$
  introduces: [sum]
  say: "Ký hiệu chữ Sigma hoa này là một cái máy cộng dồn. Đọc là tổng, khi i chạy từ 1 đến 3, của i. Thay i bằng 1, 2, 3 rồi cộng lại, được 6."
```
Bốn phần trong `say`: hình dạng (“chữ Sigma hoa”) → ẩn dụ (“máy cộng dồn”) → cách đọc → làm thử bằng số.

## 4. Mẫu phân cảnh lỗi thường gặp
```yaml
- show: |
    <div class="box warn"><b>Lỗi 1.</b> Chia cho $\|\mathbf{u}\|$ thay vì $\|\mathbf{u}\|^2$ ✗
    <br><span class="note">Phép thử vuông góc sẽ báo sai ngay.</span></div>
  say: "Lỗi thứ nhất … May mắn là phép thử vuông góc sẽ báo sai ngay lập tức."
```
Mỗi lỗi: cái sai cụ thể (có số) → vì sao sai → phép thử nào bắt được. Thêm `checks` chứng minh cái sai đúng là sai.

## 5. Tự rà trước khi build (checklist)
- [ ] Mục `objectives` dùng động từ đo được (tính, đọc, suy ra, kiểm tra).
- [ ] Mọi ký hiệu trong `show` đã được đọc thành lời trong `say` cùng step hoặc trước đó.
- [ ] Mọi con số trên màn hình có `checks`.
- [ ] Có ít nhất 1 phép thử tự kiểm và 1 bài tự làm có đáp án từng bước.
- [ ] Recap có chuỗi logic (`.chain`) + một câu “tư duy” + nối sang bài sau.
- [ ] Không có phát biểu nằm trong mục “Sai” của audit.
- [ ] Mọi phép toán dùng trong suy luận đã được dạy trước (luật 11); mọi bước `=`/`⇒` có lý do và có bản làm thử bằng số (luật 12).
- [ ] Mọi chỉ số dưới, số mũ, chữ dưới chân ký hiệu đều đã được đọc tên (luật 13); quy ước ký hiệu ghi ở đầu file (luật 14).
- [ ] Không còn WARN phát âm nào chưa xử lý; `asr` không còn câu gắn cờ chưa xem xét.
- [ ] Sau mỗi `clear: true`, mọi đối tượng được nhắc tới đều đang hiện trên bảng (luật 16).
- [ ] Không câu nào nhắc “tài liệu”, “slide”, “dòng N”, “bài báo gốc” (luật 18); bước dày chữ có `focus` theo câu (luật 19).
- [ ] Hook mở bằng tình huống thật có con số; bài cuối khoá là tình huống chuyên gia (luật 20).
- [ ] Bài mới và bài viết lại khai `depth: full` và qua E39 (luật 22); bài hành trình khai `case: journey` và qua E40 (luật 23).
- [ ] Mọi “bài N” đúng số trong lộ trình; nhắc bài trước có nói lại nội dung; nhắc bài sau chỉ ở hook/in_ai/recap, có giải thích bằng lời thường và `forward_ref: true` (luật 17).
