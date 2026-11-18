# fix6 BNX_C nhánh C4 (L35–L38), 2026-11-16

## TIẾN ĐỘ
- [x] L35 xong (lint 0/0, 2290 từ, verify 28/28, screen_fast PASS 24, render 112 khung 0 vấn đề)
- [x] L36 xong (lint 0/0, 2299 từ, verify 29/29, screen_fast PASS 24, render 128 khung 0 vấn đề)
- [x] L37 xong (lint 0/0, 2295 từ; verify KHÔNG chạy: `ver/l37.py` gọi `dbrun`/Docker; sổ mã chỉ kiểm sha 28/28; render 128 khung 0 vấn đề)
- [x] L38 xong (lint 0/0, 2298 từ; verify KHÔNG chạy: `ver/l38.py` gọi `dbrun`/Docker; sổ mã chỉ kiểm sha 18/18; render 115 khung 0 vấn đề)

Nguồn sửa: `audit/bnx/src/l35.py … l38.py`, sinh bằng `gen.py`. Không sửa `libj.py`, `lib2.py`, `lib.py`, `screen_code/BNX.yaml`, curriculum, registry. Không docker, dbrun, build, tts, asr, git, `screen_try --merge`. Bảng mới dùng `libj.jstep` (L35, L36, L37) hoặc hàm cục bộ `jt()` trong `l38.py` (một câu lời đọc tóm tắt, chi tiết trên màn hình). Cả bốn bài đổi `from l16 import _spoken` thành `from spoken_b import _spoken` (cùng hàm, tách khỏi bài L16).

## L35
- Mục chưa giảng → bảng ĐỨNG TRƯỚC khối mã (step sau bảng `clear: true`): chuỗi f `{ns.normalize():f}`, `:.4f`, `D("0.9995") * D("0.999")`, `for … in (…)`, `print`, `#` (trước Bước 2; mã NganSach hiện đủ dòng `import`); `sum(p for p, _ in su_co)`, `" + ".join(str(p) …)`, `"vuot…" if tong > … else "con…"`, `abs(…)` (trước ví dụ 3, mã hiện từ dòng 1); `from fractions import Fraction as F`, `**`, `float(…):.6f`, `sum(1 for _ in range(thang))` (trước check); `getcontext().prec = 50`, `** n` (trước quy mô; mã QuyMoChuoi hiện đủ 8 dòng, tách step mã / step kết quả); `TOT = """# ADR 7 …"""`, `SMS`, cổng SMS (trước Bước 6); `def kiem(vb) … return loi`, `muc not in vb`/`loi.append`/`muc[3:]`, `"dat" if not loi else …` (trước ví dụ 4).
- SHOULD: dòng `print` cuối ví dụ 3 nhô khỏi khung: tách `cac = " + ".join(…)` và `kq = … if … else …` ra dòng riêng, khung nay 11 dòng, không dòng nào dài quá khung (xem khung 53).
- Lời đọc 2292 → 2290 (cắt ở hook, prereq, sym, intuition, formula, ví dụ, quy mô, pitfalls, quiz, practice, recap). asr_reviewed 4 → 2.
- Mục chưa giảng ước còn lại: 0.

## L36
- Bảng mới: `KHACH, GD_KHACH, DINH = 100_000, 2, 10`, `import math`/`math.ceil`/`10**9`, `for he_so in (…)`, `{tb:.1f}`/`{dinh:.0f}` (trước Bước 2a; mã hằng số hiện từ dòng 1 gồm `import math`); `with db:`, `SELECT … WHERE khoa = ?` + `fetchone()`, `INSERT … VALUES (?, …)`/`UPDATE … SET … WHERE` (trước Bước 4); `re.search`, `\b`, `(?! NOT)`, `(Consider|should)` (bảng 1); khung mã mới hiện `MUC` và `TU` (SHOULD); bảng 2: `for tu, y in MUC:`, `r"\b" + tu + r"\b" + (r"(?! NOT)" if tu != "MAY" else "")`, `return muc or ["mo ta"]`, `t in cau.lower()`; khung `def doc` giữ nguyên.
- IETF chú thích ngay trong bảng giao diện; nhãn nguồn thành "Stripe (công ty thanh toán), API v1" và "SRE (sách vận hành của Google)"; câu 10 giải nghĩa PUT (ghi đè), DELETE (xoá), phương thức an toàn (chỉ đọc, như GET); lời đọc câu 10 nói tương ứng. Nguyên văn 10 câu tiếng Anh và nhãn nguồn: không đổi, vẫn "chưa kiểm độc lập" theo `sources_l36.md`.
- Lời đọc 2299 → 2299. asr_reviewed 3 → 1.
- Mục chưa giảng ước còn lại: 2 (mã DoiSoat ở cảnh quy mô: `ghi_no, ghi_co = {}, {}`, `[i for i in ghi_no if i not in ghi_co]`; `tao_hub`/`executescript` ở KhoaLuyDang; reader R4 không liệt kê hai nhóm này, không còn dư địa lời đọc để thêm bảng).

## L37
- SHOULD hook: "Trên Oracle, … giao dịch hoàn tác (không đo ở bài này)" cả màn hình và lời đọc.
- Bảng mới: `IF DB_ID(…) IS NULL CREATE DATABASE`, `USE`, `dbo.`, `VARCHAR(10)`, `BIGINT`, `PRIMARY KEY`, `CHECK`, `INSERT … VALUES`, `DROP TABLE IF EXISTS` (trước khối dựng bảng); `CREATE OR ALTER PROCEDURE … AS BEGIN … END`, `BEGIN TRAN/COMMIT/ROLLBACK`, `SELECT SUM(so_du) AS tong` (trước Bước 1); hàng mới ở bảng cảnh quy mô: `@sql NVARCHAR(200)`, `N'…'`, `+`, `EXEC (@sql)`; ghi chú `EXEC (@sql)` nhắc lại ở lỗi 2; bảng Java trước `Goi.java`: `public class Goi`, `public static void main(String[] args) throws Exception`, `import java.sql.*;`, khai biến, `catch (SQLException e)`/`getErrorCode()`; bảng Java trước `Tim.java`: `new String[] {"A", "X' OR '1'='1"}`, `for (String ten : …)`, `rs.next()`, `rs.getInt(1)`.
- Giữ nguyên chữ mọi khối mã chạy bằng SQL Server/Oracle (sha khớp), "Dựng lại bảng" ở ví dụ 3 và 5, kết quả 1,3 triệu / 1,2 triệu / 1,8 triệu.
- KHÔNG chạy `verify_bnx L37` (cần SQL Server qua Docker): NOT_VERIFIED lần này. Các kiểm trong `ver/l37.py` đọc hằng của `src/l37.py` (không đổi) và chuỗi `flat.count("Dựng lại bảng") >= 2` (còn đúng).
- Lời đọc 2295 → 2295. asr_reviewed 8 → 3.
- Mục chưa giảng ước còn lại: 1.

## L38
- Bảng mới (hàm cục bộ `jt`, một câu lời đọc mỗi bảng): PL/SQL `eo DBMS_AQ.ENQUEUE_OPTIONS_T;`, `RAW(16)`, `bnx_l38_msg(101, 500000)`, năm đối số `ENQUEUE`, `ROLLBACK`/`COMMIT` (trước Bước 2); `dq.wait := DBMS_AQ.NO_WAIT;`, `'nhan: ' || m.ma_gd || …` (trước Bước 3); Python: `def doc_theo_hang … return tong, o`, `for`/`+=`/`len`/`hang[c]`, `sum(cot[c])`; `100_000`, `[tuple(range(i, i + COT)) for i in range(n)]`, `[[h[c] for h in bang] for c in range(COT)]`, `{t1 == t2}`; `def chay`, `hang, cho, nhan = [], [], []`, `t[0] == "gui"`/`elif`/`append`, `hang, cho = hang + cho, []`, `elif t[0] == "nhan" and hang:`/`pop(0)`/`return nhan, len(hang)`; ghi chú `("huy",)` và `CA1 + [("nhan",)]`; `[(a, b) for a in range(tk) for b in range(tk) if a != b]`, `sum(1 for a, b in cap if …)`, `{100 * x / n:.1f}`, `n, x = xuyen(60, manh)`; ghi chú `sum(1 for a in range(1000) if a % 3 != a % 4)` trước kết quả đổi mảnh.
- Giữ nguyên mọi số đã kiểm (vùng nhớ cột 0 → "chưa đo được"; 8 000 / 800 000 ô; 2 400 / 3 480 lệnh xuyên mảnh; 748/1 000) và chữ mọi khối Oracle (sha khớp).
- KHÔNG chạy `verify_bnx L38` (cần Oracle qua Docker): NOT_VERIFIED lần này; mã Python P_* không đổi.
- Lời đọc 2290 → 2298. asr_reviewed 7 → 6.
- Mục chưa giảng ước còn lại: 1.

## Cổng đã chạy (nhánh C4)
- `lv.py lint` từng bài: 0 FAIL, 0 WARN (PASS 34, 28, 36, 32).
- `lv.py render` từng bài: 0 vấn đề (đã xem khung 38/40/51/53 của L35; 46/78/86/100 của L36; 80/94/97 của L37; 60/72 của L38).
- `verify_bnx`: L35 28/28 PASS, L36 29/29 PASS; L37, L38 không chạy (Docker).
- `screen_keep.py` L35–L38: chưa khớp 0; `screen_fast.py` L35 (PASS 24), L36 (PASS 24); L37, L38 chỉ kiểm sha (MISSING 0, STALE 0, ORPHAN 0).
- Không chạy: curriculum, check_curricula_graph, test_e52, lab_gate, arith_scan, `screen_try --merge` (việc chung của người điều phối). Lab không đổi.

## Bài cần dựng lại
L35, L36, L37, L38 (lời đọc và bảng đổi ở cả bốn). Cần ASR/nghe lại các câu mới.
