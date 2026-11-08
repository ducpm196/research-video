# Khoá JVA · Lập trình Java từ con số 0 — bản giao việc soạn bài (2026-11-08)

Người học: **mất gốc, chưa từng lập trình**, mục tiêu cuối là backend ngân hàng (sau JVA học tiếp BNK, rồi INT/ACB). Bài phải tự đủ: chỉ dùng khái niệm đã dạy ở bài trước hoặc ngay trong bài.

## Cách làm (bắt buộc)
- Nguồn bài là Python: `audit/jva/src/lNN.py`, hàm `build()` trả `lesson(...)`. **Bài mẫu: `audit/jva/src/l00.py`** — đọc kỹ trước khi viết, giữ đúng cấu trúc 10 cảnh: hook, prereq, symbol (sym), intuition, formula ("Suy ra từng bước"), example ("Ví dụ … từng phép tính", 5 phép tính đánh số ①–⑤), check ("Tự kiểm bằng đường khác"), pitfall (3 lỗi; ít nhất 1 lỗi "người đã đi làm"), quiz ("Bây giờ tới phần bạn tự làm", có `pause=20`, đáp án từng bước), recap (chuỗi logic + "Tư duy").
- **Mọi chương trình Java trên màn hình phải khai bằng `prog(name, code, out=..., expect=..., err=...)`** rồi hiện bằng `code_block(p, lines=(a, b))` / `out_block(p)`. Không gõ mã hay kết quả trực tiếp vào chuỗi show. `name` = tên lớp public = tên tệp; mỗi `prog` là một chương trình đầy đủ có `main`. Dùng `expect="compile_error:<chuỗi con của thông báo javac>"` cho lỗi biên dịch, `expect="runtime_error:<TenNgoaiLe>"` kèm `err='<dòng đầu stderr nguyên văn>'` cho lỗi khi chạy.
- Chuỗi in ra trong chương trình viết **không dấu, ASCII** (bảng điều khiển Windows của người học có thể hiện sai dấu). Chú thích `//` trong mã được viết tiếng Việt có dấu.
- Khối mã hiện trên một khung: **tối đa ~12 dòng**; dài hơn thì hiện từng đoạn bằng `lines=(a, b)` qua nhiều step, mỗi step `clear` (code_block tự `clear`).
- Tên lớp nên đọc được như tiếng Việt một âm tiết (Chao, Tong, Loi, Phi, Lai, Mang…) hoặc **không đọc tên lớp** trong lời. Lời đọc (`say`) không chứa từ khoá tiếng Anh của Java — `gen.py` từ chối (danh sách `SAY_FORBIDDEN` trong `audit/jva/lib.py`): nói "lệnh rẽ nhánh nếu", "vòng lặp đếm", "kiểu số nguyên", "chuỗi", "hàm chính", "giá trị rỗng", "danh sách", "bản đồ khoá–giá trị", "khối thử và bắt lỗi"… Từ "Java", "JVM" viết nguyên (lexicon tự đọc). Không dùng thêm từ tiếng Anh mới trong lời (chưa dò phát âm).
- Lời đọc đọc số bằng chữ ("hai nghìn không trăm…", "không phẩy một"), câu ≥ 4 từ, bước suy luận nói lý do ("vì", "nên", "nghĩa là"). Màn hình và lời đọc phải nói cùng một điều.
- Ví dụ tài chính dùng **số minh hoạ** (ghi "(số minh hoạ)" nếu là phí, lãi suất…), không khẳng định biểu phí thật của ngân hàng nào. Tiền dùng `long` theo đơn vị đồng; `BigDecimal` chỉ giới thiệu ở L01/L02 như cách khác đúng cho tiền.
- `checks:` của cảnh: biểu thức Python đúng (đặc biệt cẩn thận: `/` và `%` của Java với số âm khác Python — Java `-7 / 2 == -3`, `-7 % 2 == -1`; trong checks dùng `int(-7 / 2)` và `math.fmod`, hoặc chỉ ghi số dương). Bộ kiểm thật là chạy Java.
- `source` của bài: "curriculum/jva.yaml Lxx; audit/jva/verify_jva.py Lxx (javac/java chạy thật); The Java Language Specification, Java SE 21; dev.java/learn" (+ mục JLS cụ thể nếu dẫn, ví dụ JLS §15.17.2 chia số nguyên).

## Cổng kiểm cho mỗi bài (chạy theo thứ tự, phải sạch hết)
```
cd /d/research-video
PYTHONIOENCODING=utf-8 .venv/Scripts/python -B audit/jva/verify_jva.py Lxx      # mọi prog PASS
PYTHONIOENCODING=utf-8 .venv/Scripts/python -B audit/jva/gen.py Lxx             # ghi lessons/jva/Lxx_<slug>.yaml
PYTHONIOENCODING=utf-8 .venv/Scripts/python tools/lv.py lint lessons/jva/Lxx_*.yaml    # 0 FAIL, 0 WARN
PYTHONIOENCODING=utf-8 .venv/Scripts/python tools/lv.py render lessons/jva/Lxx_*.yaml  # 0 vấn đề
```
Sửa trong `src/lNN.py` rồi chạy lại — **không sửa YAML bằng tay**. Sửa bằng công cụ Edit/Write (chuỗi có `\` đi qua bash bị hỏng). Không chạy `build`/`tts`. Mở xem 2–3 khung PNG trong `out/JVA/Lxx/frames/` (hình, khối mã, đáp án) để kiểm bằng mắt.

## Giáo án 13 bài (L00 đã xong)
| Bài | Tiêu đề | Mục tiêu chính | Ví dụ bắt buộc (chạy thật) | Lỗi người đã đi làm gợi ý |
|---|---|---|---|---|
| L00 | Chương trình đầu tiên: mã nguồn, biên dịch và máy ảo Java | gõ–biên dịch–chạy; lỗi biên dịch vs lỗi khi chạy; `+` nối chữ | xong | tin "biên dịch được là chạy đúng" |
| L01 | Biến và kiểu dữ liệu | khai báo, gán, `int`/`long`/`double`/`boolean`/`char`/`String`; phạm vi `int`; tiền bằng `long` đơn vị đồng | `Integer.MAX_VALUE + 1` ra `-2147483648`; `0.1 + 0.2` ra `0.30000000000000004`; tổng tiền bằng `long` đúng | dùng `int` cho tổng tiền rồi tràn số; dùng `double` cho tiền |
| L02 | Toán tử và biểu thức | `+ - * / %` số nguyên, ép kiểu, ưu tiên, `+=` `++`, so sánh, `&& || !` và ngắn mạch | `7 / 2` = 3, `7 % 2` = 1, `(double) 7 / 2` = 3.5, `-7 / 2` = -3, `-7 % 2` = -1; ngắn mạch tránh chia 0 | `(double)(7 / 2)` vẫn ra 3.0; chia phí theo phần trăm bằng số nguyên mất phần lẻ |
| L03 | Rẽ nhánh: nếu, nếu không, và chọn theo trường hợp | `if/else if/else`, điều kiện ghép, `switch` dạng mũi tên (Java 14+), toán tử ba ngôi | bậc phí chuyển khoản minh hoạ theo số tiền (3 bậc), thử 3 số tiền ở biên | so sánh biên `>` hay `>=` sai bậc; `if (x = 5)` lỗi biên dịch với `int`; quên ngoặc nhọn |
| L04 | Vòng lặp | `while`, `for`, `do-while`, `break`, `continue`, cộng dồn | lãi cộng dồn hằng tháng minh hoạ bằng số nguyên (12 tháng), đếm số lệnh vượt hạn mức | lệch một (`<=` vs `<`); vòng lặp không dừng vì quên tăng biến; cộng `double` trong vòng lặp lệch |
| L05 | Mảng | tạo, chỉ số 0..n−1, `length`, duyệt, tổng/lớn nhất, `Arrays.toString`, `Arrays.sort`; mảng là tham chiếu | số dư 5 tài khoản: tổng, lớn nhất, vị trí; truy cập `a[5]` → `ArrayIndexOutOfBoundsException` | gán `b = a` rồi sửa `b` làm đổi `a`; vòng lặp tới `<= length` |
| L06 | Phương thức (hàm) | khai báo `static`, tham số, `return`, gọi lồng; truyền theo giá trị; nạp chồng; phạm vi biến | tách hàm `tinhPhi`; hàm nhận `int` không đổi được biến gốc, nhận mảng thì đổi được phần tử | tưởng hàm đổi được biến số nguyên của người gọi; hàm quá dài làm nhiều việc |
| L07 | Lớp và đối tượng | `class`, trường `private`, hàm tạo, phương thức, `this`, `toString`; bất biến "số dư không âm" | lớp tài khoản có nạp/rút, rút quá số dư bị từ chối (in thông báo, chưa dùng ngoại lệ); hai đối tượng độc lập | để trường `public` cho sửa tuỳ ý phá bất biến; nhầm `static` với trường riêng mỗi đối tượng |
| L08 | Chuỗi | `String` bất biến, `equals` vs `==`, `length/charAt/substring/indexOf/split/trim`, `String.format("%,d")`, `StringBuilder` | so `==` của hai chuỗi tạo riêng ra `false`, `equals` ra `true`; định dạng `1,234,567`; tách "STK;SoTien" | nối chuỗi trong vòng lặp lớn; `x.equals("abc")` khi x rỗng → `NullPointerException` (viết `"abc".equals(x)`) |
| L09 | Danh sách và bản đồ | `ArrayList`, `HashMap`, kiểu tổng quát `<…>`, duyệt, `getOrDefault`, đếm tần suất; hộp hoá số | danh sách giao dịch: tổng; bản đồ tài khoản → số dư; đếm giao dịch theo loại | `Integer` so bằng `==`: 127 ra `true`, 128 ra `false`; xoá phần tử trong vòng duyệt → `ConcurrentModificationException` |
| L10 | Ngoại lệ | `try/catch/finally`, thứ tự in, ném `throw`, ngoại lệ tự định nghĩa (số dư không đủ), có kiểm tra vs không kiểm tra, `try`-với-tài-nguyên, đọc dấu vết ngăn xếp | rút quá số dư ném ngoại lệ tự định nghĩa, `finally` luôn chạy; dấu vết chỉ đúng dòng | `catch` rỗng nuốt lỗi; bắt `Exception` quá rộng |
| L11 | Kế thừa, giao diện và đa hình; bản ghi và kiểu liệt kê | `interface`, `implements`, `@Override`, đa hình qua danh sách; `record`; `enum` với `switch` | hai cách tính phí cài cùng một giao diện, chạy qua một vòng lặp; `record` so `equals` theo giá trị; trạng thái giao dịch `enum` | kế thừa sâu thay vì giao diện; quên `@Override` nên viết sai tên hàm mà không báo |
| L12 | Tình huống chuyên gia: viết sổ chuyển khoản nhỏ từ đầu đến cuối | ghép mọi thứ: lớp, bản đồ, ngoại lệ, kiểm tra bất biến tổng tiền; đọc dấu vết lỗi và sửa | chuyển tiền giữa 3 tài khoản, tổng tiền trước = sau; chuyển quá số dư bị từ chối và tổng không đổi; một lỗi cố ý rồi sửa | sửa lỗi bằng cách nuốt ngoại lệ; không kiểm bất biến sau mỗi thao tác |

Bài 0 (L00) đã có bản đồ khoá? — **chưa**; người soạn L12 viết câu ở recap: "Bài tiếp theo của chương trình là khoá BNK, bắt đầu từ bộ nhớ và bộ thu gom rác." Không nhắc số bài của khoá khác.
