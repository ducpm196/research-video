# Báo cáo JV2 — Java trung cấp (10 bài L00–L09), 2026-11-13

Cả 10 bài XONG và qua cổng. Lộ trình `curriculum/jv2.yaml` viết sau cùng (`lv.py curriculum`: 10 bài, 10 có đặc tả, 0 lỗi).

## Bộ sinh và cổng
- `audit/jv2/`: `lib.py` (mở rộng từ JVA: `project(name, files, steps, deps)` chạy dự án nhiều tệp trong một phiên Git Bash ở thư mục tạm, `term_block`, `pcode`, `tree_parts`, `pr_steps`), `gen.py`, `verify_jv2.py` (javac `--release 21` + chạy thật chương trình `prog` và dự án `project`; `deps=True` chép jar vào `lib/`, thiếu jar thì NOT_VERIFIED), `gates.sh Lxx` (verify, gen, lint, render, lab_gate), `src/l00.py … l09.py`.
- Lớp phủ: `tools/registry/lexicon_vi.JV2.yaml`, `symbols.JV2.yaml` (sao từ JVA).
- Tệp tải thêm: JUnit Platform Console Standalone 1.10.2 (sha256 `a1de557821293ce903c213c694165fff532cf92081bac4238b9e05b35f04f43f`, trùng sha1 Maven Central 552303cc…), đã ghi bảng "Tệp tải thêm" ở cuối `labs/ENV.md` (chỉ thêm); jar để ở `audit/jv2/deps/` (bị `*.jar` trong `.gitignore` che). Lab L06 chấm được không cần jar.

## Bảng kết quả (số thật, 2026-11-13, JDK 21.0.13)
| Bài | Nội dung | verify | lint | render | lời đọc ước lượng |
|---|---|---|---|---|---|
| L00 | Dự án nhiều tệp: gói, `javac -d`, `-cp`, jar, truy cập | 5/5 | 0F 0W | 0 | 13,3 phút |
| L01 | Nhập dữ liệu: args, Scanner, Files, try-với-tài-nguyên; 1 triệu dòng với 32 MB | 14/14 | 0F 0W | 0 | 13,6 |
| L02 | Generics, Comparable/Comparator; đếm so sánh n log n (đo, Random(42)) | 9/9 | 0F 0W | 0 | 12,7 |
| L03 | Lambda, Stream; đường ống lười, Files.lines với 32 MB | 12/12 | 0F 0W | 0 | 13,1 |
| L04 | Nhãn và phản chiếu, mini-DI ~50 dòng, `javap`, singleton vs mới mỗi lần (3 vs 3 000 000 đối tượng) | 8/8 | 0F 0W | 0 | 13,8 |
| L05 | Luồng: race (hàng rào ép xen kẽ), synchronized, atomic, ExecutorService, bế tắc phát hiện bằng ThreadMXBean, Little | 10/10 | 0F 0W | 0 | 13,7 |
| L06 | Kiểm thử: ca ở biên, khẳng định tự viết, đối chứng âm, JUnit 5 console (jar có sha256) | 8/8 | 0F 0W | 0 | 13,1 |
| L07 | Gỡ lỗi: dấu vết nhiều tầng, Caused by, java.util.logging, chia đôi (20 lần cho 1 triệu bước), jdb | 10/10 | 0F 0W | 0 | 13,3 |
| L08 | java.time, múi giờ/DST (ngày 23 và 25 giờ), BigDecimal, làm tròn cộng dồn (500 000 / 1 triệu giao dịch), Locale | 7/7 | 0F 0W | 0 | 13,2 |
| L09 | Dự án sổ cái 11 tệp (gói `soc`), tệp sạch và tệp lỗi, đối chiếu số dòng, 1 triệu dòng với 32 MB (App hết bộ nhớ; AppDong chạy; AppSong cần 128 MB), đột biến bỏ kiểm tra | 2/2 (dự án 12 bước) | 0F 0W | 0 | 13,7 |

`audit/review/lab_gate.py JV2`: 10 PASS, 0 FAIL (mỗi lab: lời giải chạy qua `labs/cham.sh` đúng `mong_doi.txt`, đối chứng âm bị chấm KHÁC). `arith_scan.py JV2`: 0 FAIL. `check_xref.py --course JV2`: 0 lượt. Đã mở bằng mắt các khung: L00 (cây thư mục, bảng quy mô), L01 (lỗi đường dẫn), L02, L05, L06 (đối chứng âm), L08, L09 (bảng quy mô); các khung tràn đã sửa.

## Quy ước kỹ thuật đã rút (để người sau soạn tiếp)
- Khung chứa tối đa ~10 dòng mã + đầu ra, dòng ≤ ~95 ký tự (dòng dài hơn làm tràn ngang); đầu ra lỗi dài dùng `err` với `…` ở đầu/cuối.
- Lời đọc không đọc tên định danh tiếng Anh (bank, shop, model…): tả bằng tiếng Việt, tên gốc chỉ trên màn hình.
- Các chương trình không đọc ngày giờ/số ngẫu nhiên không seed; các phép đo thời gian chỉ in "gần đúng: true" theo khoảng; số lần so sánh dùng `Random(42)`.

## Chưa nhét được / mở
1. **Chưa dò phát âm ASR** (không được chạy `asr`/`tts`): lời đọc dùng từ Việt hoá, trừ "Java"/"JVM" qua lexicon cũ và "Spring" (L04, lexicon JVA đã có "S-pring"). Cổng `asr_flags` sau khi dựng sẽ cần xem các từ ngoại còn lại: "BOM", "ATM", "UTC", "gigabyte/megabyte" (đã có trong lexicon JVA).
2. **Sổ `audit/review/screen_code/JV2.yaml` chưa tạo** (ngoài thư mục được ghi): khối mã trên màn hình của JV2 đều lấy từ `prog`/`project` đã chạy thật, nhưng cổng `screen_code.py` sẽ đòi sổ khi chạy toàn kho. Nên sinh sổ từ `audit/jv2/src/*.py` khi cho phép sửa `audit/review/`.
3. **Chưa đưa vào `pack.py STAGES`, `curriculum/tracks.yaml`, `curriculum/bnk.yaml` (`requires_ext: JV2:L09`)** theo ràng buộc phiên; `curriculum/jv2.yaml` dùng `status: active`, không có "(VER JV2:Lxx)" vì `audit/verify_plan_curricula.py` ngoài phạm vi ghi. `audit/check_curricula_graph.py` vì thế sẽ không thấy VER của JV2 (không vi phạm khi `status: active`).
4. Luồng song song (L09) chỉ có bản `groupingByConcurrent` + so với tuần tự; chưa có đo thời gian song song vs tuần tự (không đưa số không ổn định).
5. `jdb` (L07) chạy ổn định nhờ `sleep` giữa các lệnh trong `phien.sh` (3 lần thử liên tiếp đều khớp); người học gõ tay ở dấu nhắc thì không cần nghỉ.
6. Không sửa `tools/`, `pack.py`, bài của khoá khác; không chạy git, build, tts, asr, audit_all, final_gates.
