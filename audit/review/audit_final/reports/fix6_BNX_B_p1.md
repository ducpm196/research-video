# fix6 BNX_B nhánh B1 (L16–L18) — 2026-11-16

## TIẾN ĐỘ
- [x] L16 xong - [x] L17 xong - [x] L18 xong (lint 0/0 cả ba, render 0 vấn đề, verify_bnx PASS, screen_keep + screen_fast sạch)

Khuôn dùng chung: `audit/bnx/libj.py` (không sửa), thêm trong từng bài hàm `R(khoá, lời đọc rút gọn)` / bảng `SHORT` để lấy cột "viết trong mã/đọc là" của `JROW` nhưng lời đọc ngắn hơn (giữ ≤ 2300 từ). Không sửa lib.py, lib2.py. Không chạy docker, build, tts, asr, git, merge sổ.

## Bảng tổng
| Bài | từ trước → sau | lint | render | verify_bnx | screen_fast | asr_reviewed | mục chưa giảng ước còn lại |
|---|---|---|---|---|---|---|---|
| L16 | 2290 → 2299 | 0/0 | 130 khung, 0 vấn đề | 31/31 PASS | PASS 35, 0 lỗi | 5 → 2 | 0 |
| L17 | 2298 → 2288 | 0/0 | 119 khung, 0 vấn đề | 34/34 PASS | PASS 39, 0 lỗi | 2 → 1 | 0 |
| L18 | 2299 → 2287 | 0/0 | 130 khung, 0 vấn đề | 26/26 PASS | PASS 23, 0 lỗi | 2 → 1 | 0 |
(asr_reviewed giảm vì các câu đổi chữ khi cắt lời đọc; gen.py giữ mọi câu không đổi. Các câu đã đổi cần ASR lại ở lần dựng sau.)

## L16
- example `public class BeLuong`, `main … throws Exception`, `int/long/boolean/String`, `new ArrayList<>()`/`new CountDownLatch(1)`/`new int[] {300, 400}`: hai bảng (class+main; decl+new) trước BeLuong 1/3.
- `for (int i = 1; …; i++)`, `for (Future<Integer> h : hen) tong += h.get()`, `() -> {…}`, `Thread.sleep`: bảng for/foreach/lambda trước BeLuong 2/3.
- `System.out.println("…" + …)`, `(10 + 4 - 1) / 4` chia số nguyên: bảng print/div trước 3/3.
- `try { … } catch (RejectedExecutionException e) { tuChoi++; }`, khối bắt lỗi trống: bảng trước HangDoi 2/3.
- `static int goi(String ten, int ms, int giaTri)`, `static final int K`, hàng chung: bảng sig/fld trước GhepLoiGoi 1/4; `System.nanoTime() / 1_000_000 / K`, `(ms < 900)`: bảng trước 3/4.
- `ChiaDoi(int tu, int den) { this.tu = tu; … }`, `protected Long compute()`: bảng trước ChiaDoi 1/3.
- SHOULD: ô "(×N)" bảng quy mô bọc `nowrap()`.
- Tách bảng class+main / decl+new thành hai step vì bảng 4 hàng tràn khung.

## L17
- `static class TramQuanSat implements Filter` + `doFilter(…) throws IOException, ServletException`: bảng trước CauHinh 4/4.
- `public class CauHinh`, hàm `chuoi(HttpSecurity http) throws Exception`: bảng trước CauHinh 2/4.
- `"{\"alg\":\"HS256\"}"` (gạch ngược trong chuỗi Java), `static String ky(…) throws Exception`, `var b = …`: bảng trước ChayThu 2/6.
- `var ctx = new AnnotationConfigWebApplicationContext();`, `for (Filter f : …)`, `(FilterChainProxy) chuoi`, `++i`: bảng trước ChayThu 4/6.
- `record Ban(String ten, boolean khoe)`, `so.stream().filter(Ban::khoe).toList()`, `Map<String, Integer> dem = new TreeMap<>()` + `dem.merge(b.ten(), 1, Integer::sum)`, `i % song.size()`: hai bảng (2 hàng mỗi bảng) trước ChiaTai.
- `for (long i = 0; i < tocDo * giay; i++)`, `if (i % soBan == 0) roi++;`, `new long[] {100, 10_000, 1_000_000}`: bảng trước CuaSoLoi.
- YAML `routes: - id: …`, `predicates: - Path=/service/**`, `lb://service`: bảng trước khối Y_GW.
- Python check: `def kiem`, `if ma is None`, `not ma["chu_ky_dung"] or …`, `x not in ma["quyen"]`: bảng trước khối bảng quyết định; `dict(an, quyen=[…])`, `gia, cu = …, …`, `[len(range(i, 100, 3)) for i in range(3)]`, `100 // 2`: bảng trước khối 2/2.
- SHOULD "mã trích": `ChiaTai.java` nay đăng đủ tệp (dòng 1–12 gồm `import java.util.*;` và dòng 13–21 gồm dấu `}` cuối), bỏ chữ "(trích)"; khai `prog("ChiaTai", J_LB, …)` (chạy thật bằng javac/java, đầu ra khớp OUT_LB) nên sổ có nguồn `L17_ChiaTai`. `CuaSoLoi.java` vốn đã hiện đủ tệp (`P_QUYMO.show` không cắt dòng), không đổi.
- SHOULD ô "(×N)" bảng quy mô bọc `nowrap()`.
- Sổ: `screen/l17.yaml` thiếu mục cho khối `E. mã thật, đã hết hạn` (sha d5f37a099d9c5846, đã có trong BNX.yaml cùng sha, `of: src:BNX:L17_spring`): thêm đúng mục đó bằng Edit (khoá `BNX L17 example 19 1`).

## L18
- `class Phi { static long tinh(long soTien) { if (…) return 0; …`, `500_000`: bảng class/sig/if-return trước Phi.
- `import static …assertEquals;` (trước đây giảng muộn, loại M): chuyển lên bảng đứng TRƯỚC PhiTest (cùng `@Test void mienPhi() { … }`), bỏ khỏi bảng lệnh phía sau.
- `interface CongThanhToan {…}`, `private final CongThanhToan cong;`, hàm tạo `this.cong = cong;`, `throw new IllegalStateException(…)`: hai bảng (2 hàng mỗi bảng) trước ChuyenTien; `new ChuyenTien(cong).chuyen(…)`: bảng `new` trước ChuyenTienTest.
- `new long[2]`, `ghi[0]++; ghi[1] = soTien;`, lambda hai tham số: bảng trước JAVA_FAKE; `javac … *.java`: thêm hàng vào bảng cờ của SH_MOCK.
- quymo: `import java.util.Arrays;`, `static int tinh(long x, int loi)`, `for (int loi = 0; loi < k; loi++)`, `for (long x : ca)`, `boolean bat = false;`: hai bảng trước BoCa 1/4 và 2/4.
- SHOULD: ô "(×N)" bọc `nowrap()`. Sửa lỗi có sẵn: bảng lệnh có `$L` làm KaTeX vẽ nhầm thành công thức (khung hiện "bi{\char"1EBF}n") — bọc `$` bằng `<span>&#36;</span>`.

## Cổng đã chạy (từng bài)
- `tools/lv.py lint`: L16 71 PASS, L17 71 PASS, L18 54 PASS; 0 FAIL, 0 WARN.
- `tools/lv.py render`: L16 130 khung, L17 119, L18 130 — 0 vấn đề (xem khung PNG: L16 00043, 00074; L17 00050, 00065; L18 00065, 00071; sau khi tách các bảng 4 hàng tràn khung).
- `audit/bnx/verify_bnx.py Lxx`: L16 31/31, L17 34/34, L18 26/26 PASS (chạy Java, Spring Security, JUnit, Mockito thật trên máy; không docker).
- `screen_keep.py Lxx` (công cụ chính thức) rồi `screen_fast.py Lxx`: L16 PASS 35, L17 PASS 39, L18 PASS 23, FAIL/STALE/MISSING/ORPHAN 0. `screen_try --merge` KHÔNG chạy (tác tử chính gộp).
- Lời đọc ≤ 2300: 2299 / 2288 / 2287.

## Bài đổi → requeue
L16, L17, L18 (lời đọc và bảng đổi ở cả ba; `audit/bnx/screen/l16.yaml`, `l17.yaml`, `l18.yaml` đã cập nhật qua screen_keep; `l17.yaml` có thêm một mục sửa bằng Edit như nêu trên).
