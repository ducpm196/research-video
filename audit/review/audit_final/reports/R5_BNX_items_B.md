# R5 — Xác minh độc lập từng mục BNX L13–L25 (Batch B sau `fix6_BNX_B`)

> Vai trò: đọc-duy-nhất (không chạy Docker/dbrun, không sửa file). Đã đối chiếu trực tiếp `lessons/bnx/L13_*.yaml`..`L25_*.yaml`, `out/BNX/L13..L25/*.srt`, `out/BNX/L13..L25/build_report.json` (BNX không có `build_report.md`), các khung hình PNG đã dựng (`out/BNX/L13..L25/frames/*.png`), `labs/BNX/L24/java/*`, `labs/BNX/L25/ma_day_du/*`, và hồ sơ nguồn `audit/bnx/sources*.md`.

## 1. Tóm tắt kết quả

- **Freshness & SRT (`L13–L25`)**: **13/13 ĐẠT**. Tất cả 13 bài có `spec_sha256` khớp `lv.spec_digest(spec)`, `tts_sha256` khớp `lv.tts_digest(frames)`, số khung hình khớp `build_report.json['frames']`, `SRT == say` khớp 100%, và số từ phần `say` đều `≤ 2300` (riêng `L21` đếm theo token khoảng trắng là `2294`, lệch nhẹ so với `2290` ghi trong `fix6_BNX_B.md`). *(Ghi chú: file YAML có `mtime` mới hơn `build_report.json` do thêm `asr_reviewed`, nhưng `lv.spec_digest` bỏ qua trường `asr_reviewed` nên `spec_sha256` và bản dựng video/SRT vẫn khớp hoàn toàn.)*
- **Mục R4 & `fix6_BNX_B`**:
  - Phần lớn các mục MUST, P1 (`chắc`/`vừa`/`yếu`) và SHOULD đã **ĐÃ** được xử lý đúng trước chỗ dùng đầu tiên và giữ nguyên nhãn pháp lý/nguồn (`L14`, `L19`, `L21`, `L23`, `L25`).
  - **Còn tồn đọng 1 `CHƯA` và 3 `MỘT PHẦN` từ các hạng mục R4/`fix6`**:
    1. **L15 `(×N)` nowrap (`quymo[4]`) — `CHƯA`**: dòng `×10 000` không bọc `white-space:nowrap`; PNG `out/BNX/L15/frames/00076.png` vẫn bị ngắt dòng thành `×10` / `000`.
    2. **L18 `(×N)` nowrap (`quymo[6]`) — `MỘT PHẦN`**: `fix6` chỉ bọc `nowrap` cho hàng 1 (`2 (×1)`), bỏ sót hàng 2–3 (`200 (×100)`, `2 000 (×1000)`); PNG `out/BNX/L18/frames/00086.png` vẫn ngắt `2 000` / `(×1000)` (và cột 3 ngắt `2 000 trên 2` / `000`).
    3. **L16 `for (int i = 1; i <= 10; i++) {` — `MỘT PHẦN`**: đã giảng ở `example[3]` trước `BeLuong.java (2/3)` (`example[4]`), nhưng dòng `for (int i = 1; i <= 10; i++) {` đã xuất hiện ở cuối `BeLuong.java (1/3)` tại `example[2]` (lệch 1 bước).
    4. **L24 `s.find(TaiKhoan.class, 11L)` / `11L` — `MỘT PHẦN`**: đã giảng ở `example[9]` trước `DemBan.java` ở `example[10]`, nhưng `TaiKhoan a = s.find(TaiKhoan.class, 11L);` vẫn xuất hiện sớm hơn tại `formula[3]` (`DemBan.java (trích)`).
- **Lỗi mới phát hiện khi soi PNG / rà chéo**:
  1. **[HIGH - Lỗi hiển thị KaTeX] `L19` `example[7]` (`out/BNX/L19/frames/00049.png`)**: hai ký tự `$D` thô trong 2 ô `<td>` liền kề (`<code>D="docker exec -i …"</code>, rồi <code>$D …</code>` ở cột 1 và `<code>$D</code>` ở cột 2) ghép thành cặp `$...$`, làm hỏng chữ Việt ở cột 2 thành `đ{\char"1EB7}t cả m{\char"1ED9}t l{\char"1EC7}nh vào bi{\char"1EBF}n D; $D`. (`example[8]` bên dưới đã thoát bằng `<span>&#36;</span>`, nhưng `example[7]` bị sót.)
  2. **Các vết M (chưa giảng trước lần xuất hiện đầu) nhẹ mới thấy thêm**:
     - `L17` `example[22]` (`ChiaTai.java (1/2)`) dùng `for (int i = 0; i < n; i++)` trước `quymo[0]` (nơi mới giảng `for`).
     - `L20` `quymo[1]` dùng `runtime.NumGoroutine()` trước `pitfalls[2]`.
     - `L21` `sym[1]` chứa đoạn mã Python (`def nhom_no`, `for`, `return`, list comprehension, `print`) trước cảnh `formula`.

---

## 2. Kiểm tra Freshness, SHA & SRT (`L13–L25`)

| Bài | `spec_sha256` | `tts_sha256` | Frames (khớp `build_report.json`) | `built_at` (UTC) | `asr_reviewed` | `words` (`say`) | `SRT == say` |
|---|---|---|---|---|---|---|---|
| L13 | Khớp | Khớp | 107 / 107 | `2026-11-16T16:31:53Z` | 4 | 2294 | Khớp |
| L14 | Khớp | Khớp | 107 / 107 | `2026-11-16T16:30:30Z` | 3 | 2300 | Khớp |
| L15 | Khớp | Khớp | 108 / 108 | `2026-11-16T16:45:19Z` | 18 | 2298 | Khớp |
| L16 | Khớp | Khớp | 130 / 130 | `2026-11-16T16:52:47Z` | 6 | 2299 | Khớp |
| L17 | Khớp | Khớp | 119 / 119 | `2026-11-16T16:58:49Z` | 4 | 2288 | Khớp |
| L18 | Khớp | Khớp | 130 / 130 | `2026-11-16T17:04:03Z` | 2 | 2287 | Khớp |
| L19 | Khớp | Khớp | 120 / 120 | `2026-11-16T17:09:34Z` | 26 | 2292 | Khớp |
| L20 | Khớp | Khớp | 119 / 119 | `2026-11-16T17:20:34Z` | 5 | 2288 | Khớp |
| L21 | Khớp | Khớp | 116 / 116 | `2026-11-16T18:30:05Z` | 5 | 2294 | Khớp |
| L22 | Khớp | Khớp | 116 / 116 | `2026-11-16T17:38:51Z` | 6 | 2292 | Khớp |
| L23 | Khớp | Khớp | 109 / 109 | `2026-11-16T17:28:55Z` | 9 | 2296 | Khớp |
| L24 | Khớp | Khớp | 115 / 115 | `2026-11-16T08:43:04Z` | 12 | 2260 | Khớp |
| L25 | Khớp | Khớp | 114 / 114 | `2026-11-16T08:59:09Z` | 9 | 2300 | Khớp |

---

## 3. Xác minh chi tiết từng mục theo bài (`L13–L25`)

### L13 (`lessons/bnx/L13_docker_gitlab_ci_kubernetes.yaml`)
- **P1 `chắc` — `quymo[0]`: `def so_dot`, `while`, `min`, `+=`, `for D in (4, 40, 400): hang(D, 1, 1)`, `print`**: **ĐÃ** — `quymo[0]` (dòng 602–624) là bảng `jstep` giải thích đầy đủ trước `quymo[1..2]`.
- **P1 `vừa` — `formula[6-7]` YAML (`matchLabels: {app: chuyen-tien}`, `ports: [{containerPort: 8080}]`, `- name: app`)**: **ĐÃ** — `formula[2]` (dòng 343–356) giải thích `{app: x}, [a, b], - name: n` + `$VAR`, và `formula[7]` (dòng 404–420) giải thích chi tiết đúng các dòng `matchLabels`, `ports`, `- name` ngay trước `formula[8..9]`.
- **P1 `yếu` — `formula[0]` `RUN mvn -q dependency:go-offline`**: **ĐÃ** — giải thích ở `sym[0]` (dòng 133–136) và `sym[1]` (dòng 144–145) trước `formula[0]`.
- **P1 `yếu` — `formula[2-3]` `echo "$CI_REGISTRY_PASSWORD" | docker login ...`**: **ĐÃ** — `formula[4]` (dòng 368–385) giải thích trước `formula[5]` (chứa lệnh `docker login`); PNG `out/BNX/L13/frames/00037.png` hiển thị `$` sạch không lỗi KaTeX.
- **P1 `yếu` — `check[1]` `(0, D, 0) in seen`, `max`, `print`**: **ĐÃ** — `check[0]` (dòng 535–550) giải thích trước `check[1]`.
- **SHOULD / `fix6` — Bọc `(×N)` không ngắt dòng (`quymo[3]`)**: **ĐÃ** — `quymo[3]` (dòng 646–650) bọc `nowrap` cho cả 3 dòng `4 (×1)`, `40 (×10)`, `400 (×100)`. PNG `out/BNX/L13/frames/00078.png` hiển thị 1 dòng gọn.

### L14 (`lessons/bnx/L14_ddd_cong_api_open_api.yaml`)
- **P1 `chắc` — `example[5-6]` `from fractions import Fraction as F`, `[F(0)] * 30`, `print`, `#`**: **ĐÃ** — `example[5..6]` (dòng 496–530) giảng đầy đủ trước `example[7]`.
- **P1 `vừa` — `quymo[0]` `print(n, a, b, 30 * n - a)`**: **ĐÃ** — `print` đã giảng ở `example[6]`, ý nghĩa `a, b, 30*n - a` nêu rõ trong `quymo[1]` (dòng 627–630).
- **SHOULD — `quymo` `(×N)` nowrap**: **ĐÃ** — `quymo[2]` (dòng 643–648) bọc `nowrap` cho `1 (×1)`, `100 (×100)`, `10 000 (×10 000)`; PNG `out/BNX/L14/frames/00072.png` sạch.
- **SHOULD — `intuition[3]` giữ nhãn pháp lý**: **ĐÃ** — `intuition[3]` (dòng 319–323) giữ nguyên `Điều 5, Điều 15 (theo bản dịch tiếng Anh, cần kiểm lại)`, mốc `01/3/2027`, và phần `say` nhắc kiểm tra bản gốc tiếng Việt.

### L15 (`lessons/bnx/L15_tinh_huong_du_an_mau.yaml`)
- **P1 `chắc` — `quymo[2]` `while vao[j] + w <= t: j += 1`, `vao = [i * 1_000_000 // tps for i in range(tps // 5)]`, `for tps in ... print(...)`**: **ĐÃ** — `quymo[0..1]` (dòng 615–652) giải thích đầy đủ trước `quymo[2..3]`.
- **P1 `vừa` — `intuition[3]` YAML `- {name: Idempotency-Key, ...}`, `"201": {description: ...}`**: **ĐÃ** — `intuition[3]` (dòng 363–376) giảng trước `intuition[4]`.
- **P1 `yếu` — `example[5]` `1_000_000`, `# giây`**: **ĐÃ** — `example[5]` (dòng 526–538) giảng trước `example[6]`. PNG `out/BNX/L15/frames/00066.png` hiển thị bảng `quymo` bình thường.
- **SHOULD — `quymo` `(×N)` nowrap**: **CHƯA** — `quymo[4]` (dòng 683–686) dùng dạng `×1`, `×100`, `×10 000` (không có ngoặc) và không bọc `white-space:nowrap`. Kiểm tra trực tiếp PNG `out/BNX/L15/frames/00076.png`: ô `×10 000` vẫn bị ngắt làm 2 dòng (`×10` / `000`).

### L16 (`lessons/bnx/L16_be_luong_completablefuture_forkjoin.yaml`)
- **P1 `chắc` — `public class BeLuong`, `main ... throws Exception`**: **ĐÃ** — `example[0]` (dòng 440–451) + `sym[3]` giảng trước `example[2]`.
- **P1 `chắc` — `int/long/boolean/String`, `new ArrayList<>()`, `new CountDownLatch(1)`, `new int[] {300, 400}`**: **ĐÃ** — `example[1]` (dòng 452–466) giảng trước `example[2]`.
- **P1 `chắc` — `for (int i = 1; i <= 10; i++) {`**: **MỘT PHẦN** — đã thêm giải thích tại `example[3]` (dòng 481–496) trước `BeLuong.java (2/3)` (`example[4]`), nhưng bản thân dòng `for (int i = 1; i <= 10; i++) {` vẫn nằm ở dòng cuối của `BeLuong.java (1/3)` tại `example[2]` (dòng 472–473), tức xuất hiện sớm hơn 1 bước trước `example[3]`.
- **P1 `chắc` — `System.out.println(...)`, `(10 + 4 - 1) / 4`**: **ĐÃ** — `example[5]` (dòng 508–517) giảng trước `BeLuong.java (3/3)` (`example[6]`).
- **P1 `chắc` — `try ... catch (InterruptedException e) { }`**: **ĐÃ** — `example[9]` (dòng 557–566) giảng trước `HangDoi.java (2/3)` (`example[10]`).
- **P1 `chắc` — `static final int NGUONG`, `final int tu, den;`, `ChiaDoi(int tu, int den) { this.tu = tu; … }`, `protected Long compute()`**: **ĐÃ** — `example[12]` (dòng 589–602) giảng trước `GhepLoiGoi.java (1/4)`, và `example[17]` (dòng 661–671) giảng trước `ChiaDoi.java (1/3)` (`example[18]`).
- **SHOULD — `(×N)` nowrap (`quymo[4]`)**: **ĐÃ** — `quymo[4]` (dòng 806–810) bọc `nowrap` cho `10 (×1)`, `1 000 (×100)`, `100 000 (×10 000)`; PNG `out/BNX/L16/frames/00092.png` gọn 1 dòng. (PNG `00041.png` cũng sạch.)

### L17 (`lessons/bnx/L17_spring_security_spring_cloud.yaml`)
- **P1 `chắc` — `implements Filter`, `doFilter(...) throws IOException, ServletException`**: **ĐÃ** — `example[4]` giảng trước `example[5]`.
- **P1 `chắc` — `record Ban`, `Ban::khoe`, `dem.merge`, `Map<String, Integer> dem = new TreeMap<>()`**: **ĐÃ** — `example[20..21]` (dòng 651–670) giảng trước `ChiaTai.java (1/2)` (`example[22]`). *(Lưu ý nhỏ phát hiện thêm: dòng 676 trong `ChiaTai.java (1/2)` ở `example[22]` dùng `for (int i = 0; i < n; i++)` trước `quymo[0]` dòng 775, là nơi giải thích vòng lặp `for`.)*
- **P1 `chắc` — `quymo`: `for (long i = 0; ...)`, `if (i % soBan == 0) roi++;`**: **ĐÃ** — `quymo[0]` giảng trước `quymo[1]`.
- **P1 `vừa` — `formula`: `predicates: - Path=/service/**`, `lb://service`**: **ĐÃ** — `formula[3]` giảng trước `formula[4]`.
- **P1 `vừa` — `"{\"alg\":\"HS256\"}"`, `var ctx = new AnnotationConfigWebApplicationContext();`**: **ĐÃ** — `example[7]` giảng trước `example[8]`; `example[11]` giảng trước `example[12]`.
- **P1 `vừa` — `check`: `is None`, `not`, `not in`, `dict(an, ...)`, `[len(range(i, 100, 3)) ...]`**: **ĐÃ** — `check[0]` giảng trước `check[1]`; `check[2]` giảng trước `check[3]`.
- **SHOULD — Bỏ `(trích)` ở `ChiaTai.java` & đủ mã `CuaSoLoi.java`**: **ĐÃ** — `ChiaTai.java (1/2)` và `(2/2)` (`example[22..23]`) có đủ 21 dòng gồm `import java.util.*;` và dấu `}` đóng, đã bỏ chữ `(trích)`; `CuaSoLoi.java` (`quymo[1]`) đủ 14 dòng.
- **SHOULD — `(×N)` nowrap (`quymo[2]`)**: **ĐÃ** — `quymo[2]` (dòng 810–816) bọc `nowrap` cho `100 (×1)`, `10 000 (×100)`, `1 000 000 (×10 000)`; PNG `out/BNX/L17/frames/00083.png` (và `00065.png`) hiển thị sạch.

### L18 (`lessons/bnx/L18_junit5_mockito.yaml`)
- **P1 `chắc` — `class Phi`, `static long tinh(...)`**: **ĐÃ** — `example[0]` giảng trước `example[1]`.
- **P1 `chắc` — `import static ...assertEquals;` (type M trong R4)**: **ĐÃ** — `example[2]` (dòng 369–377) giảng trước `PhiTest.java` (`example[3]`).
- **P1 `chắc` — `private final CongThanhToan cong;`, `ChuyenTien(CongThanhToan cong)`, `throw new IllegalStateException(...)`, `new ChuyenTien(cong).chuyen(...)`**: **ĐÃ** — `example[9..10]` giảng trước `example[11]`; `example[12]` giảng trước `example[13]`.
- **P1 `chắc` — `quymo`: `import java.util.Arrays;`, `for (int loi...)`, `for (long x : ca)`, `boolean bat = false;`**: **ĐÃ** — `quymo[0]` giảng trước `quymo[1]`; `quymo[2]` giảng trước `quymo[3]`.
- **P1 `vừa` — `check`: `new long[2]`, `ghi[0]++; ghi[1] = soTien;`, `javac ... *.java`**: **ĐÃ** — `example[15]` giảng trước `example[16]`; `check[0]` giảng trước `check[1]`.
- **Hạng mục `fix6` — Lỗi KaTeX `$L` ở `example[15]`**: **ĐÃ** — đã thoát `$`; PNG `out/BNX/L18/frames/00065.png` (và `00044.png`, `00054.png`) sạch.
- **SHOULD / `fix6` — `(×N)` nowrap (`quymo[6]`)**: **MỘT PHẦN** — `quymo[6]` (dòng 703–707) chỉ bọc `<span style='white-space:nowrap'>` cho hàng 1 (`2 (×1)`), còn hàng 2–3 để `<td>200 (×100)</td>` và `<td>2 000 (×1000)</td>`. Kiểm tra PNG `out/BNX/L18/frames/00086.png`: hàng 3 vẫn bị ngắt `2 000` / `(×1000)` (và cột 3 ngắt `2 000 trên 2` / `000`).

### L19 (`lessons/bnx/L19_redis_cum_khoa_khu_trung.yaml`)
- **P1 `chắc` — `example`: phép bit, `def/return`, `for x in b`, `A if đk else B`, `b"foo"`, `print([(a, a + n - 1) ...])`**: **ĐÃ** — `example[0..2]` (dòng 475–519) giảng đầy đủ trước `example[3]`.
- **P1 `chắc` — `quymo`: `khoa.find("{")`, `khoa[a + 1:b]`, `next(...)`, `for n in (3000, 300000)`, `f"dedup:{{tx}}:{i}"`, `dem[nut(...)] += 1`**: **ĐÃ** — `quymo[0]` giảng trước `quymo[1]`; `quymo[2]` giảng trước `quymo[3]`.
- **SHOULD — `(×N)` nowrap (`quymo[5]`)**: **ĐÃ** — `quymo[5]` (dòng 803–807) bọc `nowrap` cho `3 000 (×1)`, `300 000 (×100)`, `30 000 000 (×10 000)`; PNG `out/BNX/L19/frames/00083.png` (và `00036.png`, `00066.png`) sạch.
- **SHOULD — `example[8]` ghi chú Redis `8.10.3` & `DELEX` `8.4`**: **ĐÃ** — `example[8]` (dòng 594–597) giữ nguyên nhãn `(NOT_VERIFIED)` và `cũng NOT_VERIFIED độc lập`.
- **LỖI MỚI PHÁT HIỆN tại `L19` `example[7]` (PNG `out/BNX/L19/frames/00049.png`)**: `example[7]` (dòng 574–580) dùng `$D` thô trong 2 ô cùng hàng (`<code>D="docker exec -i …"</code>, rồi <code>$D …</code>` và `<code>$D</code>`) khiến KaTeX bắt cặp `$...$`, làm hỏng văn bản cột 2 thành `đ{\char"1EB7}t cả m{\char"1ED9}t l{\char"1EC7}nh vào bi{\char"1EBF}n D; $D`.

### L20 (`lessons/bnx/L20_go_goroutine_kenh_http.yaml`)
- **P1 `chắc` — `func rut(...)`, `tk := TaiKhoan{...}`, `tk.SoDu -= tien`, `dem++`**: **ĐÃ** — `example[0]` (dòng 472–486) giảng trước `example[1]`.
- **P1 `chắc` — `for i := 0; i < 1000; i++ {`**: **ĐÃ** — `example[4]` (dòng 509–515) giảng trước `example[5]`.
- **P1 `chắc` — ``fmt.Fprint(w, `{"trang_thai":"ok"}`)``**: **ĐÃ** — `example[12]` (dòng 580–591) giảng trước `example[13]`.
- **P1 `vừa` — `close(ch)`, `for v := range ch`, `time.Sleep(200 * time.Millisecond)`**: **ĐÃ** — `check[0]` giảng trước `check[2]`; `pitfalls[2]` giảng trước `pitfalls[3]`. *(Lưu ý nhỏ phát hiện thêm: `runtime.NumGoroutine()` có xuất hiện ở `quymo[1]` dòng 730 trước khi giải thích ở `pitfalls[2]`.)*
- **SHOULD — `(×N)` nowrap (`quymo[3]`)**: **ĐÃ** — `quymo[3]` (dòng 746–749) bọc `nowrap` cho `1 000 (×1)`, `10 000 (×10)`, `100 000 (×100)`; PNG `out/BNX/L20/frames/00080.png` (và `00040.png`) sạch.

### L21 (`lessons/bnx/L21_he_thong_cho_vay_so.yaml`)
- **P1 `chắc` — `(35 if thu_nhap >= 15_000_000 else 20)`, `15_000_000`**: **ĐÃ** — `formula[5]` giảng trước `formula[6]`. *(Lưu ý nhỏ phát hiện thêm: `sym[1]` dòng 168–173 có đoạn Python `def nhom_no`, `for`, `return`, list comprehension và `print` trước cảnh `formula`.)*
- **P1 `vừa` — `hexdigest()[:16]`, `hexdigest()[:12]`, `for ma, giay_to, may in ho_so:`, `ofs.split(",")[4:]`, `len({mv for mv, sv in ...})`**: **ĐÃ** — `formula[7]` trước `[8]`; `[12]` trước `[13]`; `[16]` trước `[17]`.
- **P1 `yếu` — `quymo`: `int(hashlib.sha256(...).hexdigest(), 16)`, `h // 4 % 6`**: **ĐÃ** — `quymo[0]` giảng trước `quymo[1]`.
- **SHOULD — `(×N)` nowrap (`quymo[3]`)**: **ĐÃ** — bọc `nowrap` đầy đủ; PNG `out/BNX/L21/frames/00080.png` (và `00059.png`) sạch.
- **Nhãn pháp lý (`sym[1]`, dòng 173–177)**: **ĐÃ** — giữ nguyên cảnh báo quy định TT 31/2024 + TT 37/2025 NHNN.

### L22 (`lessons/bnx/L22_aem_jcr_sling_htl_osgi.yaml`)
- **P1 `chắc`/`vừa` — `formula`: cắt lát `url[:i]`/`phan[:-1]`, `[i for i, c in enumerate(url)...]`, `i = max(co) if co else cat[0]`, Java `package/private/getTieuDe`, Python `self.ten, ...`, `self.vet += [...]`**: **ĐÃ** — `formula[3]` trước `[4]`; `formula[12]` trước `[13]`; `formula[16]` trước `[17]`.
- **SHOULD — `(×N)` nowrap (`quymo[3]`)**: **ĐÃ** — bọc `nowrap` đầy đủ; PNG `out/BNX/L22/frames/00079.png` (và `00047.png`) sạch.

### L23 (`lessons/bnx/L23_scikit_learn_onnx_rung_co_lap.yaml`)
- **P1 `chắc`/`vừa` — `(nhan[1000:] == -1).sum()`, `for`/`[so_lan_cat(...) for _ in range(200)]`, `-2 ** (-h / c)`, `import onnxruntime as rt`, `f"...{lech:.1e}"`**: **ĐÃ** — `formula[4]` trước `[5]`; `[7]` trước `[8]`; `[10]` trước `[11]`; `[16]` trước `[17]`.
- **SHOULD — `(×N)` nowrap (`quymo[2]`)**: **ĐÃ** — bọc `nowrap` đầy đủ; PNG `out/BNX/L23/frames/00073.png` (và `00053.png`) sạch.
- **SHOULD / Nguồn — Ghi chú phụ thuộc phiên bản (`scikit-learn 1.9.1, skl2onnx 1.20.0, onnxruntime 1.31.1`)**: **ĐÃ** — giữ nguyên ở `formula[11]` (dòng 468–472) và `pitfalls[2]` (dòng 795–798), không có nhận định độ trễ ngân hàng hay Python-only.

### L24 (`lessons/bnx/L24_jpa_hibernate_spring_data.yaml`)
- **P1 `chắc` — `formula[0]` `@Id Long id; String ten; List<TaiKhoan> tk = new ArrayList<>();`**: **ĐÃ** — `formula[0]` giảng trước `formula[1]`.
- **P1 `chắc` — `example`: `new Configuration().addAnnotatedClass(...)`, `new long[] {5, 50, 500}`, `(a == b)`, `Transaction t = ...`**: **ĐÃ** — `example[0]` trước `[1]`; `[7]` trước `[8]`; `[9]` trước `[10]`.
- **P1 `chắc` — `s.find(TaiKhoan.class, 11L)` / `11L`**: **MỘT PHẦN** — đã giảng trong `example[9]` (dòng 548–550) trước `DemBan.java` ở `example[10]` (dòng 560–561), nhưng dòng `TaiKhoan a = s.find(TaiKhoan.class, 11L);` vẫn xuất hiện sớm hơn trong `formula[3]` (`DemBan.java (trích)`, dòng 345–346).
- **P1 `vừa` — `check`: `for (i,) in ...fetchall():`, `INSERT ... (?)`, `lambda c: n.append(c)`**: **ĐÃ** — `check[0]` giảng trước `check[1]`.
- **P1 `vừa` — `pitfalls`: `catch (LazyInitializationException e)` / `getSimpleName()`**: **ĐÃ** — `pitfalls[0]` giảng trước `pitfalls[1]`.
- **SHOULD — `(×N)` nowrap (`quymo[0]`)**: **ĐÃ** — bọc `nowrap`; PNG `out/BNX/L24/frames/00071.png` (và `00055.png`) sạch.
- **SHOULD — Mã đầy đủ `Kho.java`, `DemSql.java`, `DemN1.java`, `DemBan.java`**: **ĐÃ** — `DemSql.java` đủ trong `example[3]`, `DemN1.java` đủ qua `example[5,6,8]`, và toàn bộ 9 tệp Java + `README.txt` (bao gồm `Kho.xem()`) đều có tại `labs/BNX/L24/java/`.

### L25 (`lessons/bnx/L25_giao_dich_spring_aop.yaml`)
- **P1 `chắc` — `if (rieng) ... else ... throw new IllegalStateException(...)`**: **ĐÃ** — `formula[0]` giảng trước `formula[1]`.
- **P1 `chắc` — `try { return p.proceed(); } finally { ... }`, `doThoiGian(...) throws Throwable`**: **ĐÃ** — `formula[5]` giảng trước `formula[6]`.
- **P1 `chắc` — `new DriverManagerDataSource(...)`, `nhom.submit(...)`, `try (Connection a = ...)`, `long l1 = so(a)`**: **ĐÃ** — `example[0]` trước `[1]`; `example[7]` trước `[8]`; `check[0]` trước `[1]`.
- **SHOULD — Mã đầy đủ `Cfg.java`, `DemTx.java`, `DemBe.java`**: **ĐÃ** — toàn bộ 7 tệp Java + `README.txt` có mặt tại `labs/BNX/L25/ma_day_du/`, tiêu đề trên slide ghi rõ `(trích; mã đủ ở thư mục kèm của lab)`.
- **SHOULD / Nguồn (`[SPISO]`) — Bỏ khẳng định Oracle `ORA-02179` / SQL Server**: **ĐÃ** — đã gỡ bỏ; `formula[7]` (dòng 422–423) và `check[2]` (dòng 593–605) chỉ nêu kết quả đo thật trên H2 (`bài chỉ chạy thật trên H2`).
- **SHOULD — `(×N)` nowrap (`quymo[0]`)**: **ĐÃ** — bọc `nowrap` cho `3 (×1)`, `300 (×100)`, `30 000 (×10 000)`; PNG `out/BNX/L25/frames/00075.png` (và `00039.png`) sạch.
