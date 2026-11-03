# Mở một chuyên ngành mới (dùng khi thêm khoá cho một lĩnh vực chưa có)

Quay lại: SKILL.md, Bước 2. Áp dụng cho mọi lĩnh vực (toán, hệ thống, dữ liệu, AI, kỹ thuật, kinh tế…), không riêng tin học.
Mỗi bước có **cổng**: chưa qua cổng thì không làm bước sau.

## 1. Phạm vi và chỗ đứng (trước khi viết một dòng giáo án)
1. **Chuẩn ngoài:** chọn chuẩn chương trình của lĩnh vực (ví dụ CS2023 với 17 lĩnh vực, ACM DSTF với 11 lĩnh vực khoa học dữ liệu), một hoặc hai sách chuẩn, và bài báo gốc của mỗi kết quả sẽ nêu tên. Đọc nguyên văn, ghi ngày đọc. Trang không tải được thì ghi NOT_VERIFIED, không dựa vào trí nhớ.
2. **Lỗ hổng:** dùng `grep -il "<khái niệm>" curriculum/*.yaml` để liệt kê khoá nào đã dạy phần nào, kèm mã bài. Khoá mới chỉ dạy phần CHƯA có. Phần đã có thì trỏ tới bằng `requires_ext`, không dạy lại.
3. **Mã khoá:** 2–6 chữ in hoa, không trùng tên công cụ hay khái niệm người học dễ nhầm. Ví dụ GFX chứ không GIT, vì GIT dễ lẫn với Git của DVO; `lv.py new-course` chặn những mã như vậy.
4. **Cổng 1:** ghi đoạn “Căn cứ phạm vi” và “Vì sao cần” ở đầu `curriculum/<khoá>.yaml`, mỗi nguồn có nhãn CITED hoặc NOT_VERIFIED.

## 2. Dựng khung
```
.venv/Scripts/python tools/lv.py new-course <KHOÁ> --title "<Tên khoá>"
```
Lệnh này tạo các tệp sau và không ghi đè tệp đã có:
- `curriculum/<khoá>.yaml`
- `tools/registry/symbols.<KHOÁ>.yaml`
- `tools/registry/lexicon_vi.<KHOÁ>.yaml`
- `audit/<khoá>/verify_<khoá>.py`
- các thư mục `lessons/<khoá>/`, `audit/<khoá>/probes/`, `audit/<khoá>/logs/`

## 3. Giáo án (`status: planned`)
- **10–17 bài.** Mỗi bài có `title`, `spec_planned`, `requires`, `requires_ext`, `objectives` (động từ đo được), `example` (con số tính được, kèm `VER <KHOÁ>:Lxx`) và `fix` (phát biểu hay bị nói sai, cùng cách nói đúng).
- **`spec_planned`** là đường dẫn dự kiến. Khi tệp đặc tả đã có thì đổi thành `spec`, vì `lv.py curriculum` đòi `spec` trỏ tới tệp có thật.
- **Bài cuối là bài tình huống chuyên gia** (case-lessons.md): một quyết định hay sự cố thật của người làm nghề, giải bằng kiến thức cả khoá.
- **Mã VER:** mỗi con số trong `example` được tính lại trong `audit/verify_plan_curricula.py`, bằng mô phỏng, sympy, chạy thật hay liệt kê, không gõ sẵn kết quả. Số đặt ra để minh hoạ thì ghi “(số minh hoạ)”. Sự kiện có thật thì ghi “(CITED nguồn)”.
- **Cổng 2:** ba lệnh sau đều sạch.
  - `verify_plan_curricula.py`: 0 FAIL.
  - `check_curricula_graph.py`: không tham chiếu hỏng, không chu trình.
  - `lv.py curriculum curriculum/<khoá>.yaml`: 0 lỗi.

  Lỗi thật đã gặp: tính nhẩm sai nDCG (0,986 thay vì 0,985) và bước SGD; mô hình hoá sai thời gian đuổi kịp ở EVT L09 (bỏ quên dữ liệu mới vẫn đến). Cả ba đều do mã VER bắt được.

## 4. Phát âm (trước khi viết lời đọc)
- Liệt kê mọi tên riêng và từ ngoại sẽ nói.
- Với mỗi từ, thử 2–3 cách viết qua ASR, lưu kết quả vào `audit/<khoá>/probes/`. Ghi điểm theo dạng k/8 và luôn có đối chứng.
- Từ đạt từ 7/8 trở lên thì ghi vào `lexicon_vi.<KHOÁ>.yaml`.
- Từ không đạt thì chỉ hiện trên màn hình, còn lời đọc dùng tên tiếng Việt.
- Không bịa cách phiên âm.

## 5. Bài giảng
- Tạo bài: `lv.py new lessons/<khoá>/Lxx_<slug>.yaml --id Lxx --title "Bài N — …"`. Bài tình huống thêm `--kind case`.
- Template tự điền `course`, và lấy `series` từ bài đã có để cả khoá giữ một kiểu.
- Hàm kiểm dùng chung đặt trong `tools/checklib.py`, tên phải có tiền tố khoá. Lỗi thật: hàm `sql` của DAN che hàm `sql` của DBS và làm DBS L16 FAIL. Sau khi thêm hàm, chạy `audit/check_checklib_dupes.py`.
- Bộ kiểm độc lập `audit/<khoá>/verify_<khoá>.py` tính lại mọi khẳng định của bài bằng một cách KHÁC cách checklib dùng, rồi đối chiếu hai kết quả.
- **Cổng 3:** lint đạt 0 FAIL, 0 WARN; bộ kiểm đạt toàn PASS; `audit/layout_scan.py <KHOÁ>` báo 0 lỗi; đã tự mở xem một số khung hình.

## 6. Dựng, nghe lại, rà toàn kho
- **Dựng:** `bash audit/.build_queue_run.sh <KHOÁ> L00 L01 …`. Hàng đợi chỉ dùng một giọng; chỉ đổi giọng khi giọng gốc bị chặn, và khi đó đổi cho cả bài.
- **Câu máy nghe gắn cờ:** liệt kê bằng `audit/review/asr_flags.py <KHOÁ>` (câu ngắn ≤ 7 từ có độ khớp < 0,7 được đánh dấu ⚠ NGẮN: viết dài ra và dựng lại). Câu còn lại cần lý do dẫn từ bản chép, ghi bằng `audit/dms/asr_review_dms.py --course <KHOÁ> …` (khối HAND); bài có template `audit/<khoá>/src` thì chạy thêm `audit/review/sync_tpl_asr.py <KHOÁ> Lxx`. Sau đó chạy lại `lv.py asr` để `asr_report.md` khớp đặc tả (`audit_all.py` báo báo cáo cũ).
- **Rà toàn kho** sau mỗi đợt sửa:
  - `audit/review/audit_all.py`: lint, STALE theo dấu băm, giọng, ASR.
  - `audit/review/check_course_refs.py`: “bài N”, bản đồ khoá.
  - `audit/review/check_meta.py`: tiêu đề, chuỗi bài, tên bài so với lộ trình.
  - `audit/review/status_report.py`: sinh `curriculum/STATUS.md`.
- **Cổng 4:** STATUS ghi khoá đã hoàn thiện; ROADMAP chỉ dẫn STATUS, không chép số tay.

## 7. Lỗi thường gặp khi mở khoá mới
| Lỗi | Hậu quả | Chặn bằng |
|---|---|---|
| Template ghi cứng tên chuỗi của khoá khác | cả khoá mang sai tên chuỗi | `new` lấy khoá từ thư mục; `check_meta.py` |
| Bản đồ khoá (bài 0) liệt kê thiếu bài thêm sau | người học bỏ sót bài | lint E37 |
| Hai cách viết một từ (luỹ/lũy, logarit/lôgarit) | thiếu nhất quán trên màn hình | lint E38 (SPELL_CANON) |
| Thay chữ hàng loạt sửa luôn chữ trích nguyên văn ASR trong `reason` | lý do xem xét sai sự thật | đối chiếu `asr_report.md` sau khi thay |
| Số trong giáo án đúng nhưng mã VER vẫn kiểm số cũ | kiểm sai thứ | sửa giáo án thì sửa VER cùng lúc; `check_curricula_graph.py` |
| Hàm checklib trùng tên | phép kiểm khoá khác lặng lẽ sai | `check_checklib_dupes.py` |
| Dẫn sự kiện theo trí nhớ (“11 dòng”, “87%”) | dạy điều nguồn không ghi | chỉ dạy điều đã đọc nguyên văn |
