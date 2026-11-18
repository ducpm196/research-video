# BRIEF_FIX_PYT — sửa khoá PYT theo người đọc độc lập — 2026-11-14

Báo cáo gốc: `audit/review/audit_final/reports/S01_PYT.md` (ĐỌC TOÀN BỘ: 15 MUST, SHOULD, bảng độ sâu, cột "Cần biết trước", "Người học kẹt ở đâu"). Chuẩn bài: `audit/review/audit_final/BRIEF_AF2.md`, `.claude/skills/lecture-video/SKILL.md`, `audit/review/audit_final/BRIEF_FIX_S01.md` (mục "Việc phải làm", "Quy trình", "Cổng mới"; bỏ phần FND). Bộ sinh/kiểm của khoá: `audit/pyt/` (`lib.py`, `gen.py`, `src/lNN.py`, `verify_pyt.py`, `gates.sh Lxx`, `gates_all.sh`, `measured.json`).
Ngưỡng cần đạt: **MUST 0; P1 = 2 ở ≥ 90% bài (hiện 2/14); P8 = 2 100% (đang đạt)**.

## Gốc chung phải xử lý (mọi bài của phần bạn)
1. **Mã cụt / kết quả dán nhầm khung / REPL dùng biến chưa gán**: mọi khối `>>>` và khối mã trên màn hình phải CHẠY ĐƯỢC khi gõ lại từ trên xuống (mỗi khối tự đứng: có gán biến, `import`, thân vòng lặp, `print` nếu kết quả hiện ra). Kết quả hiện ra phải đúng là kết quả của mã hiện ra. Thêm vào `verify_pyt.py` kiểm ghép nguyên văn khối trên màn hình rồi chạy thật cho từng chỗ bạn sửa.
2. **Cách viết số trong `say`**: "190 B", "140 B"… bị TTS đọc thành "N chục byte". Trong MỌI lời đọc viết "byte" đầy đủ và số bằng chữ đúng ("một trăm chín mươi byte"); quét `lessons/pyt/*.yaml` và `audit/pyt/src` tìm mẫu số + " B" trong `say`/`srt` và sửa hết (cả hai nửa khoá, người sửa nửa nào thì sửa nửa đó).
3. **P1 thấp**: giảng TẠI CHỖ bằng một câu lời thường + ví dụ nhỏ ở lần đầu xuất hiện trong bài (hoặc bỏ nếu không cần) mọi mục "Cần biết trước" của từng bài trong báo cáo (ví dụ `in`/tập hợp, phương thức dấu chấm, `is`, `isinstance`, `pass`, `.loc`, "biên dịch", "ngoại suy", `datetime64`, `idxmax`, "trung vị", `tempfile`, pip/site-packages/`cut`); đặt `introduces`/`assumes` E52 + mục `term:` trong `tools/registry/symbols.PYT.yaml` (thêm bằng Edit nhỏ, đừng ghi đè tệp; có tác tử khác sửa nửa kia của khoá).
4. **Mục tiêu giáo án ↔ video (E51)**: mục tiêu nào không được dạy thì thêm cảnh/step dạy hoặc xoá mục tiêu khỏi bài + `curriculum/pyt.yaml` (Edit nhỏ) và `covers`. Đặc biệt: L03 mục tiêu 1 "sửa danh sách bằng chỉ số" (cả bài không có `x[0] = …`); L13 mục tiêu 1 "đo thời gian và bộ nhớ" (L00–L13 không dạy cách đo: dạy `time.perf_counter` ở L02 và `sys.getsizeof`/`tracemalloc` ở L06 — người sửa L00–L06 làm; L07–L13 chỉ nhắc lại ngắn khi dùng).
5. **Python 3.13**: ghi chú ở L04 "chạy tệp .py thì giống video" SAI (tệp cũng in dòng mã và `~^^^` trên 3.13); sửa đúng: nội dung lỗi giống nhau, dạng hiển thị khác nhau giữa 3.11 và 3.13 ở cả cửa sổ `>>>` lẫn tệp; `breakpoint()` ở L07 khác dòng dừng giữa 3.11 và 3.13 — nói rõ.
6. Mọi SHOULD trong báo cáo cho bài của bạn: sửa; mục nào không sửa phải ghi lý do cụ thể.

## Quy tắc
- Sửa NGUỒN `audit/pyt/src/lNN.py` → `gen.py Lxx` (không sửa YAML sinh ra bằng tay; không đụng `lessons/pyt/` bằng Edit).
- Mỗi câu `say` mới/đổi là câu TTS mới: ≥ 8 từ, ≥ 4 và ≤ 38 từ; không từ khoá lập trình tiếng Anh trong lời đọc (gen từ chối; numpy/pandas/matplotlib/pytest đọc bằng tiếng Việt theo `lexicon_vi.PYT.yaml`).
- **Độ dài lời đọc: mỗi bài ≤ 16 phút ước (≤ 2 300 từ); hiện 12–15,9 phút: thêm câu giảng thì cắt chỗ khác, không bỏ mục tiêu `covers`; không vừa thì ghi đề xuất tách vào báo cáo.**
- Quy trình mỗi bài: `bash audit/pyt/gates.sh Lxx` (verify → gen → lint 0/0 → render 0 → lab_gate). Lab: sửa `de.md` khi đề thiếu (L10 thiếu `int()`, L13 chuỗi `\n` hàm chấm chỉ in "CHUA (0/2)" → chấm in rõ lý do) và giữ `mong_doi.txt`/`loi_giai.py` khớp.
- Cuối phần của bạn: `python -B audit/pyt/verify_pyt.py <các bài của bạn>`; `python -B tools/lv.py curriculum curriculum/pyt.yaml`; `python tests/test_e52.py`. KHÔNG chạy `gen-pyt`/`screen_code check --course PYT` (người điều phối chạy một lần sau khi cả hai nửa xong — nó tái sinh cả sổ, chạy song song sẽ giẫm nhau).
- KHÔNG chạy build/tts/asr/audit_all/git/docker. Chuỗi có `\` dùng Edit/Write, không heredoc.
- Báo cáo `reports/fix_S01_PYT_<A|B>.md`; tin nhắn cuối ≤ 25 dòng: bài đã đổi, MUST/SHOULD đã sửa (số), P1 dự kiến, số cổng thật, mục không sửa + lý do.
