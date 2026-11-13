# JVA — khoảng hở chưa nhét được vào 13 bài (đưa cho người điều phối / khoá JV2) — 2026-11-13

Đã nhét VÀO JVA (không còn là khoảng hở): nhập dữ liệu bằng chữ gõ thêm (`args`, L03–L04) và bằng đầu vào chuẩn `Scanner` (L03 `nextLong`, L04 `hasNextLong` lặp tới hết dữ liệu); ghi và đọc tệp văn bản bằng `Files.writeString/readString` + `new String[]` (L08); hàm nhỏ mũi tên (`lambda`) `forEach` và `sort` với bộ so sánh ở mức đọc hiểu (L09); khái niệm nhãn (annotation) và `@FunctionalInterface` có chạy thật (L11); luồng `Thread` hai luồng + `join` (L10, không có khoá); `jshell` (L01–L02); `cd`, `pwd`, `ls`, `mkdir -p`, lỗi biên dịch đọc dòng/cột (L00).

## Chưa nhét được (mỗi mục lý do: bài đã gần trần 15–16 phút video)
| Mục | Vì sao chưa | Gợi ý đặt ở |
|---|---|---|
| Đọc tệp **từng dòng** (`BufferedReader` trên tệp thật, `Files.lines`), tệp lớn không đủ bộ nhớ | L08 chỉ có `readString` (cả tệp); P9 của L08 đã nêu giới hạn 1,9 GB nhưng chưa có mã đọc từng dòng | JV2 bài vào/ra tệp và luồng dữ liệu |
| `synchronized`, khoá, điều kiện tranh chấp (hai luồng cùng sửa một biến), `ExecutorService` | L10 cố ý chỉ dạy `Thread` + `join` với ô ghi riêng | JV2 bài đồng thời |
| Stream API (`.stream().filter().map()`), `Optional`, `Collectors` | lambda mới ở mức đọc hiểu một dòng (L09) | JV2 |
| Generics tự viết (`class Hop<T>`), ký tự đại diện `?` | L09 chỉ giải thích `<…>` khi dùng | JV2 |
| `package`, nhiều tệp, `classpath`, `javac -d`, tệp `.jar` | mọi bài JVA dùng một tệp, thư mục phẳng | JV2 bài tổ chức dự án |
| JUnit, Maven/Gradle, IDE, trình gỡ lỗi (debugger) | chưa có bài nền cho công cụ xây dựng | JV2 / khoá công cụ |
| `equals`/`hashCode` tự viết (khoá `HashMap` là lớp của mình), `Comparator.comparing`, `Collections.sort`, `Iterator` tường minh | L09 chỉ dùng khoá chuỗi và so sánh Long | JV2 bài tập hợp |
| `BigDecimal` thực hành (làm tròn `RoundingMode`) | L01–L02 chỉ giới thiệu; L02 P9 nêu vì sao cần quy tắc làm tròn | JV2 bài tiền và số |
| Ngày giờ (`java.time`), `enum` có trường/phương thức, `switch` với mẫu (pattern) | ngoài mục tiêu BNK đầu | JV2 |
| HTTP, JSON, cơ sở dữ liệu, SQL từ Java (JDBC) | thuộc khoá FND/BNK | BNK |
| Nhập từ bàn phím tương tác (nhập → chờ → nhập) bằng `Scanner(System.in)` ngoài ống `echo … | java` | `labs/cham.sh` chấm không có bàn phím nên lab dùng giá trị mặc định/ống | — |

## Ghi chú kiểm
- `Scanner(System.in)` (L03 `RutNhap`, L04 `TongNhap`) chạy thật trong `verify_jva.py` (tham số `stdin` của `prog`) và trong sổ `screen_code` bằng lệnh `echo … | java …` (khối `run` bash). Hai chương trình đó không có trong `lib.PROGRAMS` mà ở `lib.PROGRAMS_IO`, vì `screen_code` chạy không có `stdin`.
- Lời hứa của L00 (`String[] args` → L04; `static` → L06) đã được giữ ở L04 (cảnh `nhap`) và L06 (bảng ký hiệu).
