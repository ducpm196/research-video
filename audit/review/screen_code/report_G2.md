# SC1 nhóm 2 — SDP, WEB, SEC, DEN, CLD, CLC, SAR, DSY: 55 khối

> Người điều phối ghi tệp này, nguyên văn từ câu trả lời cuối của tác tử nhóm 2 (công cụ không cho tác tử ghi tệp báo cáo). Kết quả cổng do người điều phối chạy lại nằm ở `report_SC1.md`.

Giao 54 khối. Sau khi sửa, WEB L04 tách một khối thành hai, nên tổng là 55 khối. Có thêm 8 nguồn `sources:`. Cổng chạy bằng bản `screen_code.py` lúc 11:45Z.

## 1. Số khối theo khoá
| Khoá | khối | run | syntax | fragment | output | pseudo | other | unverified_claims |
|---|---|---|---|---|---|---|---|---|
| SDP | 38 | 35 | 2 | 1 | 0 | 0 | 0 | 4 |
| WEB | 6 | 4 | 0 | 0 | 1 | 0 | 1 | 1 |
| SEC | 3 | 1 | 0 | 0 | 0 | 2 | 0 | 0 |
| DEN | 2 | 0 | 0 | 0 | 0 | 1 | 1 | 2 |
| CLD | 2 | 0 | 0 | 0 | 0 | 0 | 2 | 2 |
| CLC | 2 | 0 | 0 | 0 | 0 | 2 | 0 | 1 |
| SAR | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 1 |
| DSY | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 1 |
| **Tổng** | **55** | **40** | **2** | **1** | **1** | **6** | **5** | **12** |

Điều bài nói về các khối pseudo/other được kiểm bằng nguồn đọc đúng văn bản đã ghim (`files:`):
- SEC L12: phân tích bộ luật tường lửa, đủ 9 yêu cầu bài nêu.
- CLC L03: phân tích hai câu chính sách, 6 yêu cầu.
- CLD L02: mô phỏng quy tắc bộ nhớ đệm của Docker Docs trên hai tệp dựng hiện trên màn hình.
- DEN L03: dùng node để eval đối tượng và kiểm cấu trúc.
- SAR L01: tính lại 16,7 và 2500 từ chính chữ trong khối.
- DSY L14: bản Python đối chiếu dùng giao dịch sqlite thật (`twin_of`).
- WEB L01: sơ đồ cây là khối output; nguồn dùng html.parser in cây ra để so.

Một số khối có ca thứ hai: SDP L01 prereq, SDP L05 example 1, SEC L06, SDP L14 quiz bản cũ. Các ca này chạy lại đúng văn bản đã ghim qua `files: {khoi.txt: <khối>}` rồi exec/eval.

## 2. Lỗi đã sửa (7 MUST, 1 SHOULD)
| Khối | Mức | Trích nguyên chữ (cũ) | Vì sao sai + bằng chứng | Sửa thành | lint/render/verify |
|---|---|---|---|---|---|
| SDP L03 example 0 0 (kéo theo prereq 1 0) | MUST | `class ChuNhat(Hinh):` / `def area(self): return self.w * self.h` … `tong = sum(h.area() for h in cac_hinh)` | Thiếu `import math`; không có `__init__`, nên `ChuNhat(3, 4)` ở cảnh prereq báo TypeError; không có lớp tam giác dù bảng dùng `self.b * self.h / 2`; `cac_hinh` chưa định nghĩa. Cổng với văn bản cũ: FAIL NameError | Thêm `import math`, `__init__` cho ChuNhat/Tron, lớp TamGiac, `cac_hinh = [ChuNhat(3, 4), Tron(1), TamGiac(6, 2)]`; `say` thêm một câu, `focus` [1,1,1,1]; bước 1 thêm `clear: true` (tràn bảng); thêm `checks` chạy mã mới | lint 0/0; render 60 khung 0 vấn đề; verify_sdp 36/0 |
| SDP L06 example 0 0 | MUST | `class ChuNhat:` / `def dat_rong(self, w): self.w = w` (không có hàm tạo) | Bảng bước 2 và quiz ghi "dat_rong(5) → rộng 5, cao 0", nhưng đọc `r.h` báo AttributeError | Thêm `def __init__(self): self.w = self.h = 0`; `say` thêm một câu, `focus` [1,1,1,1,2]; thêm `checks` | lint 0/0; render 77 khung, 0 vấn đề |
| SDP L07 hook 0 0, example 3 0 | MUST | `hom_nay = date.today()` · `loi_chao(date.today())` | chưa nhập `date`, báo NameError | thêm `from datetime import date` vào cả hai khối | lint 0/0; render 63 khung, 0 vấn đề |
| SDP L08 prereq 0 0 | MUST | `a = Dem()` / `b = Dem()` / `a.n += 1` | lớp `Dem` chỉ có trong `checks:` (cùng mẫu lỗi `nap` của L02), báo NameError | hiện thêm `class Dem:` / `def __init__(self): self.n = 0  # bộ đếm, bắt đầu từ 0`; bước 1 thêm `clear: true` | lint 0/0; render 70 khung, 0 vấn đề |
| SDP L11 prereq 1 0 | MUST | `bang = {("MỚI", "trả tiền"): "ĐÃ TRẢ", ...}` | SyntaxError `':' expected after dictionary key` | viết đủ 4 ô trên 2 dòng, khớp `alg.ORDER_FLOW`; thêm `checks` | lint 0/0; render 74 khung, 0 vấn đề |
| SDP L12 example 0 0 | MUST | `@functools.lru_cache(maxsize=None)` không có dòng nhập | NameError: functools | thêm `import functools` | lint 0/0; render 72 khung, 0 vấn đề |
| WEB L04 example 0 0 | MUST | một khối chứa cả `const u = await layNguoiDung(); …` và `const [u, d, g] = await Promise.all(…)` | khai báo `u, d, g` hai lần trong một chương trình: `SyntaxError: Identifier 'u' has already been declared` | tách hai khối (hai chương trình riêng); câu 1 của `say`: "Hai đoạn mã là hai chương trình riêng…", `focus` [[1, 2], 3]; đo thật: tuần tự ≥ 590 ms, đồng thời 295–590 ms | lint 0/0; render 69 khung 0 vấn đề; verify_web 16/16 |
| WEB L06 example 2 0 | SHOULD | `Idempotency-Key: 7f3c…` | draft-ietf-httpapi-idempotency-key-header-08: "Its value MUST be a String (Section 3.3.3 of [RFC9651])", ví dụ trong draft có nháy kép. Datatracker truy cập 2026-11-10, đọc qua công cụ tóm tắt | `Idempotency-Key: "7f3c…"` | lint 0/0; render 79 khung, 0 vấn đề |

**Không sửa** ba khối SDP (L08 example 1 0, L14 example 1 0, L14 example 2 0). Chúng gọi lớp hoặc hàm mà bài không hiện thân (`YeuCau.builder()`, thân `tinh_thue`). Tác tử ghi syntax/fragment kèm `unverified_claims`, không tự viết lớp để che. Đề xuất: hiện một lớp xây tối thiểu ở L08.

## 3. unverified_claims (12)
- **SDP**:
  - L08 ex 1 0: không có lớp YeuCau, nên không kiểm được build() chạy cuối.
  - L13 ex 0 0: "bản tách trùng bản cũ trên 10 000 cặp". Hàm dài ban đầu không hiện thành mã, chỉ `checks` (alg.fee_old) kiểm; số 817 thì cổng có kiểm.
  - L14 ex 1 0: "tinh_thue(100) vẫn chạy", nhưng thân hàm không hiện.
  - L14 ex 2 0: "→ KeyError", nhưng hàm bản mới không hiện.
- **WEB**: L06: hành vi máy chủ khi gặp lại khoá (không có máy chủ); 10 233 / 10 000 chỉ do `checks` kiểm.
- **DEN**:
  - L03: tiêu chí nhúng hay tham chiếu là quy tắc thiết kế.
  - L05: phân vùng và sắp xếp của Cassandra (không có Cassandra; chưa đối chiếu tài liệu chính thức).
- **CLD** L02 (×2): chưa chạy `docker build` thật vì dịch vụ Docker không chạy. Kết luận dựa trên mô phỏng quy tắc "Build cache invalidation" của Docker Docs (truy cập 2026-11-10, no revision given), độ trung thực INFERRED. Chưa kiểm ảnh python:3.12.4 có trên Docker Hub.
- **CLC** L03: chưa đối chiếu tài liệu nhà cung cấp đám mây cho quy tắc "từ chối tường minh thắng, mặc định từ chối".
- **SAR** L01: 5000 ghi/s và kết quả thử cơ sở dữ liệu phân tán là số minh hoạ.
- **DSY** L14: kiểm bằng bản Python đối chiếu, độ trung thực INFERRED.

Phép thử âm 21/21 FAIL như mong đợi. Gồm đột biến khẳng định ở 5 khối SDP và 7 nguồn/khối khoá khác, văn bản cũ của 7 khối đã sửa, và một dòng sai độ sâu trong cây WEB L01. Tệp: scratchpad `sc/g2/neg.py`, `neg2.py`, `neg2.out`.

## 4. Kết quả cuối (tác tử chạy)
- SDP: 38 khối, PASS 39 · FAIL 0 · STALE 0 · MISSING 0 · ORPHAN 0 · WARN 0
- WEB: 6 khối, PASS 7, các cột lỗi đều 0
- SEC: 3 khối, PASS 4, các cột lỗi đều 0
- DEN: 2 khối, PASS 3, các cột lỗi đều 0
- CLD: 2 khối, PASS 3, các cột lỗi đều 0
- CLC: 2 khối, PASS 3, các cột lỗi đều 0
- SAR: 1 khối, PASS 2, các cột lỗi đều 0
- DSY: 1 khối, PASS 2, các cột lỗi đều 0

Bộ kiểm khác:
- verify_sdp 36/0; verify_web 16/16
- scan_ctrl 8 (JVA cố ý)
- check_xref SDP/WEB 0
- lv.py curriculum: sdp 0 lỗi, web 0 lỗi

Bài cần dựng lại:
- SDP: L03, L06, L07, L08, L11, L12
- WEB: L04, L06

Có 3 bài đổi `say`: SDP L03, SDP L06, WEB L04.

Đề xuất cho cổng: cho khối pseudo/other khai `files` hoặc nguồn kiểm ngay trong mục của khối.
