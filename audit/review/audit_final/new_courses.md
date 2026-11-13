# Khoá mới của đợt AF2 (thiết kế; mỗi khoá một bộ sinh `audit/<khoá>/` theo mẫu `audit/jva/`)

Căn cứ: `sample_f/REPORT.md` mục 4–5 (khoảng hở tiên quyết đo được). Thứ tự học mới: **FND → JVA → JV2 → BNK → BNX…** và PYT đặt TRƯỚC bài đầu tiên dùng Python.
Mỗi khoá: `lv.py new-course <KHOÁ>`, lộ trình `curriculum/<khoá>.yaml`, bộ sinh bài, `verify_<khoá>.py` chạy lệnh/chương trình THẬT, sổ `screen_code`, lab, `af2: true`, thêm vào `pack.py STAGES` + `curriculum/tracks.yaml`.

## FND · Nền thực hành (11 bài; Chặng 0, đặt trước JVA)
Người học chưa từng dùng dòng lệnh. Mọi lệnh hiện trên màn hình là đầu ra THẬT từ Git Bash trong thư mục tạm (bộ kiểm chạy lại). Cửa sổ lệnh chuẩn: Git Bash (hợp đồng `labs/ENV.md`).
| Bài | Nội dung | Lab (kết quả mong đợi tự đối chiếu) |
|---|---|---|
| L00 | Máy tính chạy chương trình thế nào (CPU, bộ nhớ, tệp, hệ điều hành) · cách học bộ khoá này (tự làm trước khi xem đáp án, ôn ngắt quãng, lab) · chuẩn bị máy: Git for Windows, JDK 21, Python, sqlite (`bash labs/check_env.sh`) | chạy `check_env.sh`, đối chiếu từng dòng ✔ |
| L01 | Git Bash: dấu nhắc, `pwd ls cd`, đường dẫn tuyệt đối/tương đối, cây thư mục (hình) | `cd`/`ls` theo cây cho trước, in `pwd` cuối |
| L02 | Làm việc với tệp: `mkdir touch echo > >> cat cp mv rm`, ký tự đại diện `*`, vì sao `rm` không có thùng rác | dựng cây thư mục bằng script, in `find` |
| L03 | Đọc và lọc văn bản: `head tail grep wc sort uniq`, ống `|`, chuyển hướng | đếm lệnh theo loại trong tệp giao dịch CSV giả |
| L04 | Chương trình, `PATH`, biến môi trường, mã thoát `$?`, chạy tệp `.sh` | script in phiên bản công cụ + mã thoát |
| L05 | Trình soạn mã, mã hoá UTF-8, xuống dòng; đọc thông báo lỗi: tệp, dòng, nguyên nhân (thật: lỗi `javac`, `python`, `bash`) | sửa 3 tệp hỏng cho chạy được (đầu ra mong đợi) |
| L06 | Dữ liệu có cấu trúc: CSV, JSON, YAML — đọc, viết tay, lỗi cú pháp thường gặp | lab giấy bút: đọc giá trị trong JSON/YAML (đáp án số) |
| L07 | Máy khách–máy chủ và HTTP: yêu cầu/phản hồi, phương thức, mã trạng thái, tiêu đề; `curl` tới máy chủ cục bộ chạy ngay trong lab | `curl` ra 200 và 404 (máy chủ cục bộ trong script) |
| L08 | Bảng và SQL đầu tiên bằng sqlite: bảng/hàng/cột/khoá chính, `CREATE INSERT SELECT WHERE ORDER BY GROUP BY UPDATE DELETE`, giao dịch (ý niệm) | tệp `.sql` in số dư theo tài khoản |
| L09 | Git tối thiểu: `init add commit log diff branch`, vì sao commit nhỏ | script tạo repo, in `git log --format=%s` |
| L10 | Dự án nhỏ: sổ tay giao dịch bằng bash + sqlite + git (CSV → sqlite → truy vấn → commit) | script tổng hợp, in báo cáo |

## JV2 · Java trung cấp (≈ 10 bài; sau JVA, trước BNK) — soạn sau FND
`package`/nhiều tệp/`javac -d`/jar · nhập dữ liệu (`args`, `Scanner`) và tệp (`Files`, UTF-8) · generics, `Comparable`/`Comparator` · lambda và Stream · annotation và phản chiếu (nền cho Spring, mini-DI) · Thread, race, `synchronized`, `ExecutorService` · kiểm thử tối thiểu (khẳng định tự viết, rồi JUnit console) · gỡ lỗi (dấu vết sâu, `jdb`/IDE, nhật ký) · dự án sổ cái tệp CSV → báo cáo. Không phụ thuộc Maven/JDBC (máy kiểm chưa có `mvn`, `sqlite-jdbc`): nếu cần, thêm vào ENV.md có sha256 và hướng dẫn tải.

## PYT · Python từ con số 0 (≈ 12 bài; trước BNX và chặng dữ liệu/AI)
biến → hàm; list/dict/comprehension; chuỗi, f-string, `re`; tệp, JSON; lớp; ngoại lệ; mô-đun, `venv`, `pip`; numpy; pandas; matplotlib đọc biểu đồ; `pytest`; dự án phân tích tệp giao dịch.

## MLP · Học máy thực hành (≈ 14 bài; chặng 9, sau CS115 L22–L23)
chia tập và rò rỉ dữ liệu; scikit-learn; hồi quy/phân loại trọn quy trình; đánh giá; PyTorch tensor, autograd, vòng huấn luyện; MLP, CNN nhỏ; nhúng/attention tí hon; tinh chỉnh mô hình có sẵn; gọi API mô hình ngôn ngữ và đánh giá; tái lập; hành trình; dự án.

## Bài dự án mỗi chặng (11 bài, cuối chặng)
Đề, thang chấm, lời giải mẫu; chặng 7–8 dùng Docker khi CB-AF1-8 cho phép.
