# Cổng "mã trên màn hình" phủ FND và JV2

Ngày: 2026-11-13. Cổng: `audit/review/screen_code.py`. Sổ mới: `audit/review/screen_code/FND.yaml`, `audit/review/screen_code/JV2.yaml`.
Không sửa `lessons/`, `audit/fnd`, `audit/jv2`, `audit/jva`, `audit/bnk`.

## Kết quả (số thật)

| Phạm vi | Khối | Kết quả |
|---|---|---|
| `check --course fnd` (và phần FND của `check` toàn kho, bản cuối) | 186 | PASS 267 · FAIL 0 · STALE 0 · MISSING 0 · ORPHAN 0 · WARN 0 (267 = 186 khối + 81 nguồn) |
| `check --course jv2` (và phần JV2 của `check` toàn kho, bản cuối) | 200 | PASS 295 · FAIL 0 · STALE 0 · MISSING 0 · ORPHAN 0 · WARN 0 (295 = 200 khối + 95 nguồn) |
| `check` toàn kho (lần cuối, 23 phút) | 1419 | PASS 1881 · FAIL 3 · STALE 5 · MISSING 0 · ORPHAN 0 · WARN 0; 8 dòng lỗi đều thuộc BNX L05, xem "Cổng toàn kho" |
| `negative_controls.py` | 49 | 49/49 đúng kết luận (30 ca cũ giữ nguyên + 19 ca mới: phiên dòng lệnh, `cmds_only`, tệp dựng sẵn, `retries`, java args/stdin) |
| Cấy lỗi vào bản sao sổ thật (SC_REGDIR tạm) | 11 | 11/11 bị bắt (sửa đầu ra một bước, sửa tệp dựng sẵn, hỏng cú pháp Java trong dự án, JUnit, mong_doi lab thừa dòng, sha lệch, trỏ khối sang phiên khác, bật `cmds_only` sai) |

Mốc đầu đợt: 1089 khối PASS, MISSING 4 (chính là FND/JV2). Số khối toàn kho tăng 1089 → 1419 vì FND (186) và JV2 (200) vào sổ (và 3 khối của khoá khác đổi trong lúc chạy).

## Sổ mỗi khoá

FND, 186 khối, 81 nguồn:
- 70 nguồn là phiên Git Bash (mỗi `lib.cmd(...)` một nguồn), 11 nguồn là lời giải lab (`LAB_Lxx`, chạy thật, đòi đúng `labs/FND/Lxx/mong_doi.txt`).
- 154 khối terminal là `fragment` trong một phiên (dãy dòng liên tiếp của phiên vẽ như màn hình: `$ lệnh`, `> ` dòng nối, đầu ra); 20 khối nội dung tệp dựng sẵn (`within: src:FND:<phiên>#<tệp>`); 11 khối kết quả mong đợi của lab là `output` `of` nguồn lab; 1 khối đề lab là `fragment` trong lời giải.
- Không khối nào phải ghi tay (`hand: true`).

JV2, 200 khối, 95 nguồn:
- 71 nguồn Java (mỗi `lib.prog(...)`, có `args`, `stdin`, `javac --release 21` như `verify_jv2.py`), 14 nguồn phiên dự án nhiều tệp (`lib.project(...)`: javac, java, jar, JUnit console, jdb, sed), 10 nguồn lab.
- 120 `fragment` trong chương trình Java, 8 `fragment` nội dung tệp của dự án, 71 `output` (61 của chương trình, 10 của lab), 1 `other` (xem dưới).
- 2 khối ghi tay (`hand: true`, giữ qua các lần sinh lại):
  - `JV2 L04 hook 0 0`: đoạn minh hoạ Spring (`@Service`, `@Autowired`, `@Transactional`, `(...)` lược) → `other/java` với `read_check`; không biên dịch được (kho không có jar Spring, `chuyen(...)` là lược).
  - `JV2 L07 quiz 0 0`: dấu vết ngăn xếp minh hoạ cho bài tập (lớp Lenh/Dich/App/Kho không có chương trình thật) → `output` không `of`, kèm `unverified_claims`.

## Mở rộng cổng (screen_code.py)

1. Lệnh mới `gen-fnd`, `gen-jv2`, `gen-prog --course JVA|FND|JV2`. `cmd_gen_jva` được tách thành hàm dùng chung (`_java_sources`, `_java_fragment`, `_java_output`, `_write_ledger`); kết quả `gen-jva` KHÔNG đổi một byte: chạy bản cũ và bản mới vào hai thư mục sổ tạm (SC_REGDIR), `cmp` ra IDENTICAL. Tệp `audit/review/screen_code/JVA.yaml` trong kho không bị chạm.
2. Nguồn `session: [{cmd, out}]` (+ `fs`, `profile: fnd|jv2`, `env`, `deps`): chạy MỘT phiên Git Bash thật, so từng bước. Profile `fnd` dùng `audit/fnd/runner.run_session` (thư mục tạm là C:/Users/ban, cấu hình Git riêng, ngày cố định); profile `jv2` dựng thư mục tạm, chép jar `audit/jv2/deps` vào `lib/`, thay `{DEPS}`, đổi gạch ngược thành gạch xuôi như `verify_jv2.py`. Thiếu jar → NOT_VERIFIED (FAIL), không PASS lặng lẽ.
3. Văn bản nguồn phiên = phiên vẽ như màn hình, nên khối terminal dùng `fragment`/`within` sẵn có. Thêm `cmds_only: true` (khối chỉ hiện dòng lệnh, đầu ra ẩn: so với riêng các dòng lệnh), và `within: "src:<KHOÁ>:<tên>#<đường dẫn>"` (khối là đoạn một tệp dựng sẵn của phiên, đúng tệp phiên đã chạy).
4. Java: `args`, `stdin`, `java_release` cho nguồn chạy chương trình.
5. Nguồn lab: `labs/<KHOÁ>/Lxx/loi_giai.*` chạy thật (bash, java, sqlite) và đòi đúng `mong_doi.txt`; khối cảnh `practice` (đề hoặc kết quả mong đợi) là fragment/output của nguồn này. Bash lab có sqlite3 dùng `shim_sqlite3` (PATH thêm `audit/fnd/shim` khi máy chưa cài sqlite3).
6. `tempfile.TemporaryDirectory(ignore_cleanup_errors=True)`: lời giải lab FND L07 chạy máy chủ nền rồi `kill`, tiến trình con còn giữ thư mục tạm trên Windows (lỗi dọn thư mục, không phải lỗi khối).

## unverified_claims (NOT_VERIFIED bằng máy)

FND: 20 (18 ở nguồn phiên, 2 ở nguồn lab). Gồm: đầu ra `sqlite3` kiểm bằng lớp giả lập `audit/fnd/shim` vì máy chưa cài sqlite3 CLI thật (mọi phiên và lab gọi lệnh sqlite3); bố cục cột của `ls` là giả lập cửa sổ 80 cột (alias của runner); thời gian ("cùng nhanh" ở L05, truy vấn/chỉ mục ở L08, `--max-time` một giây ở L07); mạng thật ở L07 (máy chủ thử cục bộ).
JV2: 4. Gồm: `L05_ThoiGian` (máy chỉ kiểm cờ `do gan dung`, không kiểm số mili giây); `L09_SoCai` bước 9 không tất định (xem mục dưới); hai khối ghi tay nói trên.
Danh sách đầy đủ: `screen_code.py check --course fnd|jv2 -v`.

## Chưa làm được / giới hạn

- Không có khối FND hay JV2 nào dùng `hide_out` thật, nên nhánh `cmds_only` chỉ được thử bằng ca cấy trong bộ nhớ (3 ca), chưa có khối thật.
- Gate FND dùng chung `audit/fnd/runner.py` (ổn định hoá đường dẫn, alias `ls`, đổi "run.sh: line N:" thành "bash:") nên không độc lập hoàn toàn với bộ kiểm của khoá; điều đối chiếu độc lập là văn bản trên màn hình (phân tích từ HTML bài) so với đầu ra chạy thật.
- Khối khớp theo văn bản (tìm dãy dòng liên tiếp trong phiên cùng bài, lấy phiên đầu tiên khớp): khối ngắn có thể gắn vào phiên khác của cùng bài; vẫn đúng ý (văn bản là dãy dòng đã chạy thật), nhưng không chứng minh khối đó được tạo từ đúng `term_block` nào.
- Thời gian chạy: FND khoảng 2 đến 4 phút, JV2 khoảng 5 phút (mỗi phiên khởi động Git Bash), cổng toàn kho khoảng 19 phút khi máy đang tải. Trong lần chạy toàn kho đầu, `BNX L23 formula 11 0` ra "quá thời gian" (ngưỡng 180 giây, máy đang tải do các phiên khác); chạy riêng khối đó mất 32 giây và PASS. Không liên quan thay đổi này.
- Lời giải lab FND L10 tự dựng đường tới `labs/sqlrun.py` bằng `dirname "$0"` (chỉ dùng khi máy chưa cài sqlite3); chạy ngoài thư mục lab thì hỏng. Cổng tránh bằng `shim_sqlite3`. Không ảnh hưởng người học đã cài sqlite3.

## Khối trên màn hình KHÔNG khớp đầu ra thật

Không có khối nào sai chữ: 186 khối FND và 200 khối JV2 khớp (đầu ra từng bước của 70 phiên FND, 14 phiên dự án JV2, 71 chương trình Java, 21 lời giải lab).

MỘT phát hiện về tính ổn định (không sửa bài, theo yêu cầu): `JV2 L09`, phiên `L09_SoCai` bước 9,
`java -Xmx64m -cp out soc.AppSong lon.csv 2>&1 | head -1 | grep -o OutOfMemoryError` (màn hình: `OutOfMemoryError`).
`AppSong` chạy nhiều luồng ForkJoin; khi cả luồng chính và các luồng phụ cùng ném lỗi hết bộ nhớ thì stderr xen kẽ, dòng đầu có lần
không chứa `OutOfMemoryError` (ví dụ `Exception in thread "ForkJoinPool.commonPool-worker-1" Exception in thread "ForkJoinPool…-worker-6" …`)
và lệnh in rỗng. Bằng chứng: lần chạy toàn kho thứ hai của đợt này FAIL đúng bước đó (máy chạy `''`, 11 mục FAIL do cùng một phiên), hai lần
chạy trước và lần sau cùng PASS; lấy mẫu riêng sáu lần chạy bước đó cho một lần dòng đầu bị xen. `audit/jv2/verify_jv2.py` cũng chạy đúng
lệnh này nên có cùng rủi ro. Xử lý trong cổng: nguồn có `retries: 4` (thử lại, PASS khi một lần khớp trọn; vẫn lệch cả bốn lần thì FAIL) và
ghi `unverified_claims`. Đề xuất sửa bài (người chủ khoá làm): thay `head -1 | grep -o OutOfMemoryError` bằng `grep -m1 -o OutOfMemoryError`
hoặc `grep -c OutOfMemoryError` rồi sinh lại bài và sổ.

## Cổng toàn kho

Lần chạy cuối (`check -v`, 23 phút, máy tải nặng do các phiên khác): 1419 khối — PASS 1881 · FAIL 3 · STALE 5 · MISSING 0 · ORPHAN 0 · WARN 0.
Cả 8 dòng lỗi là `BNX L05` (5 STALE ở `example 1, 3, 4, 6, 7` và 3 FAIL phụ thuộc): `lessons/bnx/L05_mtls_chung_chi_hai_chieu.yaml` bị một phiên khác
sửa lúc 05:51, giữa lúc cổng chạy (sổ BNX chưa cập nhật). Không liên quan FND/JV2; không sửa.
Lần toàn kho thứ nhất ra FAIL 3 ở `BNX L23 formula 11 0` ("quá thời gian", máy tải), chạy riêng 32 giây PASS. Mốc MISSING 4 đầu đợt đã về 0.
