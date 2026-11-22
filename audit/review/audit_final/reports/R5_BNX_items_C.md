# R5 BNX L26–L38 (kiểm tra độc lập từng mục sau fix6_BNX_C, chỉ đọc)

Người kiểm tra: verifier độc lập (chỉ đọc; KHÔNG chạy Docker, `dbrun.py`, dịch vụ ngoài hay sửa tệp).
Phạm vi: `lessons/bnx/L26_*.yaml`..`L38_*.yaml`, `out/BNX/L26..L38/{build_report.json,LNN.srt,asr_report.md,frames/*.png}`, đối chiếu toàn bộ mục trong `audit/review/audit_final/reports/R4_BNX_C.md` và `audit/review/audit_final/reports/fix6_BNX_C.md` (+ `p1..p4`).

---

## 1. Tóm tắt kiểm tra dựng lại, độ tươi & đối chiếu lời

| Bài | `spec_sha256` khớp | `tts_sha256` khớp | `say` == `.srt` (ký tự) | Khung (`frames` = `srt`) | `lint` (fail/warn) | `asr_report.md` (`chưa_xem`) | Ghi chú dựng |
|---|---|---|---|---|---|---|---|
| L26 | ĐÚNG | ĐÚNG | ĐÚNG (10 094) | 124 = 124 | 0 / 0 | 0 (cờ 4/124) | `built_at` 2026-11-16T09:16:19Z; `edge`: 124 |
| L27 | ĐÚNG | ĐÚNG | ĐÚNG (9 990) | 117 = 117 | 0 / 0 | 0 (cờ 15/117) | `built_at` 2026-11-16T09:31:34Z; `edge`: 117 |
| L28 | ĐÚNG | ĐÚNG | ĐÚNG (10 080) | 124 = 124 | 0 / 0 | 0 (cờ 8/124) | `built_at` 2026-11-16T09:56:57Z; `edge`: 124 |
| L29 | ĐÚNG | ĐÚNG | ĐÚNG (9 895) | 117 = 117 | 0 / 0 | 0 (cờ 4/117) | `built_at` 2026-11-16T10:14:04Z; `edge`: 117 |
| L30 | ĐÚNG | ĐÚNG | ĐÚNG (10 128) | 133 = 133 | 0 / 0 | 0 (cờ 13/133) | `built_at` 2026-11-16T10:47:43Z; `edge`: 133 |
| L31 | ĐÚNG | ĐÚNG | ĐÚNG (10 080) | 132 = 132 | 0 / 0 | 0 (cờ 6/132) | `built_at` 2026-11-16T11:10:33Z; `edge`: 132 |
| L32 | ĐÚNG | ĐÚNG | ĐÚNG (9 946) | 132 = 132 | 0 / 0 | 0 (cờ 4/132) | `built_at` 2026-11-16T11:19:40Z; `edge`: 132 |
| L33 | ĐÚNG | ĐÚNG | ĐÚNG (10 225) | 132 = 132 | 0 / 0 | 0 (cờ 20/132) | `built_at` 2026-11-16T11:55:34Z; `edge`: 132 |
| L34 | ĐÚNG | ĐÚNG | ĐÚNG (10 004) | 130 = 130 | 0 / 0 | 0 (cờ 6/130) | `built_at` 2026-11-16T12:03:23Z; `edge`: 130 |
| L35 | ĐÚNG | ĐÚNG | ĐÚNG (10 177) | 112 = 112 | 0 / 0 | 0 (cờ 2/112) | `built_at` 2026-11-16T12:34:18Z; `edge`: 112 |
| L36 | ĐÚNG | ĐÚNG | ĐÚNG (10 141) | 128 = 128 | 0 / 0 | 0 (cờ 3/128) | `built_at` 2026-11-16T12:34:24Z; `edge`: 128 |
| L37 | ĐÚNG | ĐÚNG | ĐÚNG (10 204) | 128 = 128 | 0 / 0 | 0 (cờ 6/128) | `built_at` 2026-11-16T17:54:58Z; `edge`: 127, `edge?`: 1 (cache cũ, `tts_sha256` khớp) |
| L38 | ĐÚNG | ĐÚNG | ĐÚNG (10 221) | 115 = 115 | 0 / 0 | 0 (cờ 8/115) | `built_at` 2026-11-16T17:48:19Z; `edge`: 115 |

Lưu ý: Không có tệp `build_report.md` trong `out/BNX/L26..L38/`; chỉ có `build_report.json`. Mọi `spec_sha256` (tính qua `lv.spec_digest`, bỏ qua `asr_reviewed`) và `tts_sha256` khớp 13/13; giọng đồng nhất `vi-VN-NamMinhNeural`. Mọi câu gắn cờ trong `asr_report.md` đều có `chưa xem xét: 0` (đã đối chiếu máy; vẫn ghi nhận `NOT_VERIFIED bằng tai người` theo quy ước).

---

## 2. Kết luận tổng hợp từng loại mục R4

- **MUST / P2 / P3 (R4)**:
  - L30 P2=1 (thiếu bước tính tay `3 + 9 = 12` cho "có cầu dao: 12"): **ĐÃ** (`quymo#3`, `frames/00087.png`).
  - L35 P3=1 (dòng `print` cuối `example#3` nhô mép khung mã): **ĐÃ** (`example#4`, `frames/00053.png`).
- **SHOULD (10 mục trong R4)**: **9 ĐÃ, 1 MỘT PHẦN** (`L28` `example#11` hết dấu `'` thừa, nhưng dòng `var rut = ... modifiedCount;` ở `frames/00073.png` dấu `;` cuối vẫn chạm/lấn mép phải khung `.code`).
- **P1 `chắc` (toàn bộ 11 mục ở L26–L33)**: **11/11 ĐÃ**.
- **P1 `vừa` (toàn bộ 77 mục ở L26–L38)**: **77/77 ĐÃ**.
- **P1 `yếu` (toàn bộ mục nêu ở R4 L26–L38)**: **ĐÃ** hầu hết; còn vài mục nền nhỏ nằm trong khối lệnh shell/JDBC hoặc hàm tách ngoài (`L30` `for c in ...; do ... done` ở `example#1` đã học ở L26 `sym#3`; `L37` `CallableStatement`/`PreparedStatement`/`try (Connection c = ...)` giảng bằng lời ở `check#3,4,6`, không có bảng riêng).
- **Khác (R4) & Nhãn pháp lý/nguồn**:
  - `L33` `sed` xám nhạt / tràn khung: **ĐÃ** (`formula#9`, `frames/00039.png`).
  - `L29` chữ `.note` xám nhạt: giữ nguyên CSS `.note` toàn cục (`frames/00076.png`), vẫn đọc được.
  - Nhãn nguồn, `MÔ PHỎNG`, `số minh hoạ`, `NOT_VERIFIED` (W3C L27), trích NIST (L34), Lưu ý pháp lý (L34), 10 câu tiếng Anh nguyên văn (L36), mọi số đã kiểm L30/L37/L38: **ĐÃ bảo toàn nguyên vẹn 13/13**.

---

## 3. Chi tiết đối chiếu từng bài (L26–L38)

*(Quy ước đánh số `scene#N`: `N` tính theo thứ tự bước 1-based trong `steps` của scene tương ứng trong `lessons/bnx/LNN_*.yaml`.)*

### L26 — `lessons/bnx/L26_maven_gradle_jenkins.yaml`
- **SHOULD `example#4` (`dung()`, `$M` không hiện)**: **ĐÃ** — `example#4` (bảng 4 hàng `M=…/bin/mvn`, `test -x $M`, `mkdir -p`, `$M -B -q -f $1 clean package`, `sha256sum`; `frames/00049.png`), `example#5` (hiện đủ `M=...`, `test -x`, `mkdir`, `dung()`; `frames/00053.png`), `example#6` (hiện `so()` và hai lời gọi), kết hợp `sym#2` (`$2`, `sleep 2`, `[ x = y ] && A || B`). Không tràn khung.
- **P1 Chắc (3/3)**:
  1. `(cd $d && $M -B -q dependency:list …)` (`quymo#1`): **ĐÃ** — `quymo#1` hàng 2, đặt ngay trước `quymo#2`.
  2. `grep -c ':jar:'` (`quymo#1`): **ĐÃ** — `quymo#1` hàng 3, đặt ngay trước `quymo#2`.
  3. `for … else:` (`example#7`): **ĐÃ** — `example#9` hàng 4, đặt ngay trước `example#10` (`PY_PIPE`).
- **P1 Vừa (4/4)**:
  1. `mkdir -p $d && cp pom-$d.xml $d/pom.xml`: **ĐÃ** — `quymo#1` hàng 1.
  2. `hang.pop(0)`: **ĐÃ** — `check#1` hàng 4 (`frames/00068.png`).
  3. `[(k, v, sau + 1) for k, v in …]`: **ĐÃ** — `check#1` hàng 2 (`[(k, v, 1) for ...]`) và `check#2` hàng 4 (`hang += [(k, v, sau + 1) ...]`).
  4. `f"bo {ten} …"`: **ĐÃ** — `check#2` hàng 2.
- **P1 Yếu (7/7)**: **ĐÃ** — `while hang:` (`check#1` hàng 3), `da, hang = {}, […]` (`check#1` hàng 2), `continue` (`check#2` hàng 1), `CAY.get(…, [])` (`check#2` hàng 4), `def chay(cac_buoc, hong=None)` (`example#9` hàng 1), `ket.append` (`example#9` hàng 2), `break` (`example#9` hàng 3).
- **Hiển thị & nhãn**: **ĐÃ** — `quymo#3` bọc `white-space:nowrap` (`frames/00086.png`), không gãy dòng `×10 000`. Nhãn `MÔ PHỎNG` / `không chạy Jenkins/Gradle` (`intuition#2`, `example#8`, `example#10`, `check#4`, `practice#1`) nguyên vẹn.

### L27 — `lessons/bnx/L27_soap_wsdl_sftp.yaml`
- **SHOULD `example#2, intuition#1` (so 246 thụt dòng vs 20 viết liền)**: **ĐÃ** — `intuition#1` (`frames/00023.png`) ghi rõ `phong bì mẫu viết liền: 203 byte` so với `20 byte`, `trả lời mẫu viết liền: 211 byte` so với `16 byte`, `đo thật, viết liền`; `example#2` (`frames/00053.png`) giữ nguyên stdout `246` kèm chú thích `246 là tệp thụt dòng; viết liền ... còn 203` và công thức `203 : 20 ≈ 10,2 lần`; `recap#3` ghi `≈10 lần ... cùng cách viết liền`.
- **P1 Chắc (1/1)**:
  1. `_, so, ma = dong[-1].split("|")`: **ĐÃ** — `check#1` hàng 2, đặt ngay trước `check#3` (`KiemLo.py`).
- **P1 Vừa (5/5)**:
  1. `var f = DocumentBuilderFactory.newInstance(); f.setNamespaceAware(true); if (chan) f.setFeature(…, true);`: **ĐÃ** — `formula#4` (bảng 3 hàng, nêu rõ `chan` là tham số hàm), trước `formula#5`.
  2. `tempfile.TemporaryDirectory() as nhan`, `sorted(f for f in os.listdir(nhan) if not f.endswith(".part"))`: **ĐÃ** — `example#5` (bảng 3 hàng), trước `example#6` (tiêu đề nêu rõ `tao_lo(n)` định nghĩa ở đầu tệp).
  3. `.rstrip("\n")`, `"\n".join`, `.encode()`, `.hexdigest()`: **ĐÃ** — `check#1` hàng 1, 3 và `check#2` hàng 1 (cộng `check#4` cho `[:900] + [-2:]`, `.replace`), trước `check#3`, `check#5`.
  4. `for n in (1000, 1000000)`, `h, byte, khoi = hashlib.sha256(), 0, 0`, `h.update`: **ĐÃ** — `quymo#1` hàng 1, 2, 4, trước `quymo#2`.
  5. `def gui`, `os.path.join`, `with open`, `os.rename`: **ĐÃ** — `formula#6` (bảng 4 hàng), trước `formula#7`.
- **P1 Yếu (3/3)**: **ĐÃ** — mã HTTP `200/400/500` (`hook#1` hộp & `say`), `OWASP` (`formula#5` "tổ chức về an toàn ứng dụng web"), `range(1, n+1)` (`quymo#1` hàng 3).
- **Nhãn nguồn / hedged claims**: **ĐÃ** — `formula#3` (`chưa kiểm được (NOT_VERIFIED: máy chủ w3.org chặn tải)`), `intuition#2` (`MÔ PHỎNG`), `pitfalls#1` + `recap#2` (giới hạn chữ ký) nguyên vẹn.

### L28 — `lessons/bnx/L28_co_so_du_lieu_so_sanh.yaml`
- **SHOULD `formula#1, example#9` (dấu `'` thừa cuối khối mongosh; dòng 1 `example#9` chạm mép phải)**: **MỘT PHẦN** —
  - Dấu `'` thừa: **ĐÃ** sửa ở `formula#2` (`frames/00029.png`) và `example#11` (`frames/00073.png`), nay đều có dòng mở `js '` khớp với `'` đóng.
  - Chạm mép phải: **CHƯA hết** — kiểm tra trực quan `out/BNX/L28/frames/00073.png` (`example#11`) cho thấy dòng 2 `var rut = () => db.tk.updateOne({_id: "001", so_du: {$gte: 600}}, {$inc: {so_du: -600}}).modifiedCount;` dấu `;` cuối dòng vẫn **chạm/nhô nhẹ qua đường viền phải** của khung `.code` (tác giả nhánh C1 có ghi nhận trong `fix6_BNX_C_p1.md` nhưng giữ nguyên để không đổi sha khối Docker).
- **P1 Chắc (2/2)**:
  1. `until docker exec $C test -f /tmp/a.ok; do sleep 0.5; done` (`test -f`): **ĐÃ** — `example#3` hàng 2, trước `example#4`.
  2. `2>&1 | head -1`, `>/dev/null 2>&1`: **ĐÃ** — `example#3` hàng 3, 4, trước `example#4`, `example#8`.
- **P1 Vừa (9/9)**: **ĐÃ** — `psql -U postgres -q -o /dev/null -f /a.sql` (`example#3` hàng 1), `-tA` (`sym#2` hàng 3), `'K'||g` (`formula#3` hàng 3), `mysql -uroot -pbnx_pass bnx < /mysqla.sql` và `sh -c "…"` (`example#7` hàng 1), `"gd.loai"` + `insertMany/findOne/countDocuments/JSON.stringify` (`formula#1` hàng 2–4), `begin; … commit;` (`formula#5` hàng 1), `for n in 1000 100000 1000000; do … done` (`formula#3` hàng 1), khoá chính / khoá ngoại / `JOIN` (`prereq#1` hàng 1; `frames/00004.png`).
- **P1 Yếu (6/6)**: **ĐÃ** — `docker rm -f` (`example#3` hàng 4), `SELECT … INTO x` (`sym#4` hàng 1), `args=(x,)` (`sym#4` hàng 2; ghi chú nhỏ: `"""…"""` trong `example#5` không có mục riêng), `doc_a = doc_b = 1000` (`check#1` hàng 3), `wait_lock`/`q` (`example#7` hàng 2–3), `() =>` (`example#10` hàng 1).
- **Nhãn nguồn / mô phỏng**: **ĐÃ** — `check#2-3` (`MÔ PHỎNG bằng Python`), `quymo#1` (`suy ra: n − 1 (công thức), không chạy ở bài`), `hook#1` (`MongoDB cũng có giao dịch nhiều bản ghi`) nguyên vẹn.

### L29 — `lessons/bnx/L29_cqrs_event_sourcing.yaml`
- **SHOULD `quymo#2` (nhãn "chạy thật" cho 2 dòng tính từ `n mod k`)**: **ĐÃ** — `quymo#3` (`frames/00076.png`) tách tiêu đề riêng `<p><b>TÍNH TỪ CÔNG THỨC n mod k (không đo kho thật): ...</b></p>` và `say` nói rõ "Hai dòng sau không đo kho thật mà tính từ công thức chia lấy dư".
- **P1 Chắc (1/1)**:
  1. `sum(1 for _ in SU_KIEN)`: **ĐÃ** — `example#5` hàng 4, trước `example#6`.
- **P1 Vừa (5/5)**: **ĐÃ** — `db.executescript("""…""")` + `INTEGER PRIMARY KEY AUTOINCREMENT` + `INSERT OR REPLACE`/`DROP TRIGGER`/chuỗi băm (`formula#1` hàng 1–3, trước `formula#2`); SQL cơ bản (`INSERT INTO ... VALUES`, `UPDATE ... SET ... WHERE`, `DELETE FROM ... WHERE`, `SELECT COUNT(*)`) (`example#1`, `example#2`, `check#1`, trước `example#3`, `check#2`); `db.executemany(…, ((i % 2, i % 97 + 1) for i in range(1000000)))` (`quymo#1` hàng 1, trước `quymo#2`).
- **P1 Yếu (5/5)**: **ĐÃ** — `sqlite3.connect(":memory:")` (`formula#1` hàng 1), `loai, tien = su_kien` + `so_du + tien if loai == "NAP" else so_du - tien` (`example#5` hàng 1), `kho.append` (`example#8` hàng 2), `for loai, tien in db.execute(…)` (`quymo#1` hàng 2).
- **Khác & Nhãn**: `frames/00076.png` hiển thị rõ; chữ `.note` vẫn dùng màu xám nhạt CSS chuẩn (đọc được). `source` và `pitfalls#1` bảo toàn nguyên vẹn.

### L30 — `lessons/bnx/L30_chiu_loi_cau_dao_can_bang_tai.yaml`
- **P2=1 ("có cầu dao: 12" thiếu bước tính tay 3 + 9)**: **ĐÃ** — `quymo#3` (`frames/00087.png`) có đoạn `Tính tay trước khi chạy`: 3 cuộc hỏng đầu (0, 100, 200 ms) mở cầu dao lúc 200 ms, rồi mỗi 1 000 ms thử 1 cuộc (1 200..9 200 ms = 9 cuộc) → `3 + 9 = 12 cuộc gọi thật`, và nêu cả trường hợp `n = 10 000` (`2 ms`, thử ở `1 002..9 002 ms`), đặt ngay trước kết quả chạy thật `quymo#4`.
- **SHOULD `formula#8, pitfalls#1` (`CanBang`/`QuyMo` cắt giữa khối)**: **ĐÃ** — `formula#12` + `formula#14` (`frames/00054.png`) hiện đủ toàn bộ hàm `chay` của `CanBang.java`, `example#6` hiện `main` và kết quả; `quymo#2` + `quymo#3` hiện đủ 16 dòng `QuyMo.java`; `formula#3` hiện đủ 11 dòng `ThuLai.chay`; `pitfalls#1` (`frames/00095.png`) thay khối 3 dòng bằng bảng đối chiếu `100 → 400 / 12`, `10 000 → 40 000 / 12`.
- **P1 Chắc (1/1)**:
  1. `int s = it ? (dang[1] < dang[0] ? 1 : 0) : i % 2;` (ternary lồng): **ĐÃ** — `formula#13` hàng 2, trước `formula#14`.
- **P1 Vừa (6/6)**: **ĐÃ** — `static String chay(...)`, `for (int lan = 1; ...)`, `"..." + lan + "..."` (`formula#2` hàng 1, 2, 4); `t == T.MO`/`T.NUA_MO`, `++hong >= NGUONG` (`formula#6` hàng 1, 4); `long[][] ketThuc = new long[2][8]` (`formula#11` hàng 2); `throw new IllegalStateException("hong")` (`check#4` hàng 3).
- **P1 Yếu (7 mục)**: **ĐÃ 6/7** (`10L` ở `formula#11` hàng 3; `Thread.sleep(1100)` ở `check#6` hàng 1; `else if` ở `formula#6` hàng 4; `main ... throws Exception` ở `check#1` hàng 3; `import io.github...*` ở `check#1` hàng 1; `onStateTransition(e -> ...)` ở `check#4` hàng 1). Còn `for c in ...; do java ... $c; done` (`example#1`): vòng `for d in ...; do ... done` đã giảng ở L26 `sym#3` (loại B yếu), L30 không lặp lại bảng riêng.
- **Số liệu & nhãn**: Mọi số đã kiểm (`400`, `40 000`, `12`, `7 gọi thật + 2 chặn = 9`, quiz `750/1550/4/2/5000/1750/≤25/95%`) và ghi chú `lược các dòng t = 3 500, 4 000` (`example#3`), `MÔ PHỎNG` vs `THẬT` (`example#1`), `chưa chứng minh với mọi cấu hình` (`check#8`) giữ nguyên.

### L31 — `lessons/bnx/L31_quan_sat_nhat_ky_chi_so_canh_bao.yaml`
- **P1 Chắc (1/1)**:
  1. `values: '0+995x12'`: **ĐÃ** — `example#8` hàng 3 (`frames/00064.png`), trước `example#9`.
- **P1 Vừa (8/8)**: **ĐÃ** —
  1. `formula#4`: `[(DV[i % 5], ...)]`, `enumerate(dong)`, `setdefault`, `set(...)`, `[i for i in a if i in b]` (4 hàng trước `formula#5`, khối `ChiMuc.py` hiện từ dòng 1).
  2. `example#2`: `json.dumps(d, separators=(",", ":"))` (trước `example#3`).
  3. `example#4`: `" > ".join(...)` (trước `example#5`).
  4. `formula#6,8`: `Integer.parseInt(a[0])`, `String[] duong`, `int[][] so`, `StringBuilder`/`append`, `\"`, `if (nguoi == 0) ... else for ...` (trước `formula#7,9`).
  5. `example#6,8,10,12`: `cat > rules.yml <<'EOF'`, `groups/rules/alert/expr/for/labels`, `input_series`, `eval_time`, `exp_samples`, `exp_alerts` (trước mỗi khối YAML).
  6. `check#3`: `sed 's/.*"value":\[[0-9.]*,"\([^"]*\)"\].*/\1/'` (`frames/00083.png`, trước `check#5`).
  7. `check#4`: `L='...'`, `$(q "$L")`, `"$L/sum(...)"` (trước `check#5`).
  8. `quymo#2`: `java XuatChiSo.java $n > m$n`, `grep -vc '^#'`, `wc -c < m$n` (trước `quymo#3`).
- **P1 Yếu (6/6)**: **ĐÃ** — `fallback_scrape_protocol`, `static_configs`, `targets` (`check#1`), `[ ... ] && break` (`check#3` hàng 4), `container` (`example#15` hàng 3, `frames/00074.png`), bỏ `ArgoCD` khỏi `recap#2` (nay chỉ còn `ELK, Grafana`).
- **Hiển thị & nhãn**: `frames/00074.png` (`IMG=prom/prometheus@sha256:...`) nằm gọn trong khung. Nhãn `MÔ PHỎNG` (`intuition#1`, `quymo#1`, `recap#3`) và `Grafana: chỉ giảng` (`intuition#2`) nguyên vẹn.

### L32 — `lessons/bnx/L32_gitops_bi_mat_aws_toi_thieu.yaml`
- **SHOULD `check#1` (`git log --name-status` vs `--reverse --name-status --format=%s`)**: **ĐÃ** — `check#1` (bảng giải mã), `check#2` (`frames/00086.png` hiện đủ 3 dòng vòng `for dong in git("log", "--reverse", "--name-status", "--format=%s")...`), `check#3` (`frames/00087.png` đầu ra).
- **SHOULD `formula#10, example#5` (thiếu lệnh ghi và `sleep 6`)**: **ĐÃ** — `formula#14` (`frames/00048.png`) hiện đủ `ghi() { ... }`, `echo "the doc luc 0 giay..."`, `echo "the ghi luc 0 giay: $(ghi)"`, `sleep 6`, `echo "the doc sau 6 giay..."`.
- **P1 Chắc (1/1)**:
  1. `vault policy write chi-doc - >/dev/null <<'P' … P` (`-` và here-doc): **ĐÃ** — `formula#12` hàng 1, trước `formula#13`.
- **P1 Vừa (5/5)**: **ĐÃ** — `apiVersion/metadata/spec/project: default` (`formula#8` hàng 1, trước `formula#9`), `fnmatch.fnmatch` (`formula#15` hàng 2), `cum.get(ten) != ch and (...)` (`formula#4` hàng 2), `sorted(set(cum) - set(mm))` (`formula#6` hàng 1), `VAULT_TOKEN=$T vault kv get` (`formula#12` hàng 3).
- **P1 Yếu (5/5)**: **ĐÃ** — `json.loads` (`formula#1` hàng 3), `("sua " if ... else "tao ") + ten` (`formula#4` hàng 3), `git revert --no-edit` (`example#1` hàng 3), `T=$(vault token create ... -field=token)` (`formula#12` hàng 2), `del cum[ten]` (`formula#6` hàng 2). (Cộng thêm `git rm -q` ở `example#5`.)
- **Nhãn nguồn / mô phỏng**: **ĐÃ** — `không chạy Argo CD hay AWS/Kubernetes` (`source`, `intuition#1-2`, `formula#9,18`, `example#8`, `recap#3`) nguyên vẹn.

### L33 — `lessons/bnx/L33_he_cu_servlet_jsp_tomcat.yaml`
- **P1 Chắc (3/3)**:
  1. `((AbstractProtocol<?>) t.getConnector().getProtocolHandler()).setMaxThreads(4)`: **ĐÃ** — `quymo#1` hàng 2, trước `quymo#2`.
  2. `new HttpServlet() { … }` (lớp ẩn danh): **ĐÃ** — `quymo#3` hàng 1 (`frames/00078.png`), trước `quymo#4`.
  3. `a[1].isEmpty() ? "" : "/" + a[1]`: **ĐÃ** — `example#1` hàng 4, trước `example#3`.
- **P1 Vừa (6/6)**: **ĐÃ** — `doGet`/`@Override`/`throws IOException`/`soYeuCau`/`setContentType`/`getWriter().print` (`formula#1` 4 hàng, trước `formula#2`); `<web-app>/<servlet>/<servlet-mapping>/<url-pattern>` (`formula#4` hàng 2–3, trước `formula#5`); `cat > … <<'EOF'` (`formula#4` hàng 1, `formula#6` hàng 4); `accumulateAndGet(dang.incrementAndGet(), Math::max)` (`quymo#3` hàng 2); `List<CompletableFuture<?>> ds`, `sendAsync`, `d.join()` (`quymo#5` hàng 2–3); `(n + 3) / 4 * 100L` (`quymo#7`, `frames/00088.png`, kèm sửa `arith_scan`: `tổng 43 chia 4 bỏ phần lẻ ra 10 lượt`).
- **P1 Yếu & Khác (R4)**: **ĐÃ** — `Files.createTempDirectory`, `Path.of` (`example#1`), `for (int i = 2; ...)` (`example#4`), `try { Thread.sleep(100); } catch ...` (`quymo#3`), `1_000_000` (`quymo#7`), `javac -d`, `2>/dev/null` (`example#6`). Giải thích `sed -i` nay chuyển thành bảng `formula#9` (`frames/00039.png`, tương phản đầy đủ, hết xám nhạt và hết tràn khung trước `Cu.java` `frames/00041.png`). Nhãn `JBoss/WildFly chỉ giảng khái niệm, không chạy` nguyên vẹn.

### L34 — `lessons/bnx/L34_he_thong_phe_duyet_tin_dung.yaml`
- **SHOULD `pitfalls#2–3` (gắn nhãn MÔ PHỎNG cho hai UPDATE nối tiếp)**: **ĐÃ** — `pitfalls#2` ghi `(bài mô phỏng bằng hai lần ghi nối tiếp)` và `pitfalls#3` (`frames/00097.png`) ghi tiêu đề `Kết quả chạy thật — MÔ PHỎNG: hai lần ghi nối tiếp trên một kết nối, không phải hai người thật` + `say` nêu rõ.
- **P1 Chắc**: 0.
- **P1 Vừa (4/4)**: **ĐÃ** — SQL cơ bản (`INSERT INTO ho_so VALUES`, `SELECT ... WHERE`, `UPDATE ho_so SET`, `COUNT(*)`/`MAX(nhom)`) ở `formula#2` (4 hàng, trước `formula#3`); `CREATE INDEX ix ON ls (khach)`, `EXPLAIN QUERY PLAN ... .fetchone()[3]`, `kh.split()[0]` ở `quymo#3` (4 hàng, trước `quymo#4`).
- **P1 Yếu (4/4)**: **ĐÃ** — `NIST` (`formula#8`: "viện tiêu chuẩn và công nghệ của Mỹ"), `tài sản bảo đảm` (`formula#7`), `kq = "cho phep" if ok else "tu choi"` (`formula#9` hàng 2), `sql += " AND tt = 'CHO_DUYET'"` (`pitfalls#2`).
- **Pháp lý / nguồn**: **ĐÃ** — `Lưu ý pháp lý` (`formula#11`), trích nguyên văn NIST (`formula#8`), `số minh hoạ` (`source`, `hook#1`, `prereq#1`, `formula#7`, `quiz#1`, `practice#1`) nguyên vẹn.

### L35 — `lessons/bnx/L35_van_hanh_sla_tai_lieu.yaml`
- **P3=1 (dòng `print` cuối `example#3` nhô mép khung mã)**: **ĐÃ** — `example#4` (`SuCoThang.py`, `frames/00053.png`) tách `cac = ...` và `kq = ...` ra dòng riêng; kiểm tra PNG xác nhận không có dòng nào tràn hay chạm mép phải khung `.code`.
- **P1 Chắc**: 0.
- **P1 Vừa (3/3)**: **ĐÃ** — `{ns.normalize():f}` và `:.4f` (`formula#2` hàng 3, trước `formula#3,4`); `' + '.join(str(p) for p, _ in su_co)` (`example#3` hàng 2, trước `example#4`); `from fractions import Fraction as F` và `F(999, 1000) ** 2` (`check#1` hàng 1–2, trước `check#2`).
- **P1 Yếu (5/5)**: **ĐÃ** — `from decimal import Decimal as D` nay có ở `formula#2` hàng 1 VÀ hiện đủ ở dòng 1 `ChuoiPhuThuoc.py` (`formula#4`); `**` (`check#1`, `quymo#1`); `abs(...)` và `"vuot…" if ... else "con…"` (`example#3` hàng 3–4); `sum(1 for _ in range(thang))` (`check#1` hàng 4); `"""# ADR 7 …"""` và `SMS` (`formula#7`, trước `formula#8`).
- **Nhãn nguồn / giả định**: **ĐÃ** — `hook#1`, `intuition#1-2`, `example#5`, `quymo#4` giữ nguyên các điều kiện giả định/nguồn.

### L36 — `lessons/bnx/L36_phong_van_thiet_ke_he_thong.yaml`
- **SHOULD `english#7` (`MUC` và `TU` không định nghĩa trên màn hình)**: **ĐÃ** — `english#6` (`frames/00087.png`) hiện khối `DocCau.py (trích 1/2): hai danh sách` định nghĩa đầy đủ `MUC` và `TU`, đặt trước bảng `english#7` (`frames/00088.png`) và `DocCau.py (trích 2/2)` (`english#8`).
- **P1 Chắc**: 0.
- **P1 Vừa (7/7)**: **ĐÃ** — `r"\b" + tu + r"\b" + ...`, `return muc or ["mo ta"]`, `for tu, y in MUC:` (`english#7` 3 hàng, trước `english#8`); `r"\b(Consider|should)\b"` (`english#5` hàng 4); `KHACH, GD_KHACH, DINH = 100_000, 2, 10` (`formula#2` hàng 1, trước `formula#3`); `{tb:.1f}`, `{dinh:.0f}` (`formula#2` hàng 4, trước `formula#4`); `with db:` (`formula#6` hàng 1, trước `formula#7`); câu 10 `PUT`, `DELETE`, "safe request methods" (`english#4` mục 10, `frames/00083.png`).
- **P1 Yếu (3/3)**: **ĐÃ** — `import math` / `math.ceil` (`formula#2` hàng 2, `formula#3` dòng 1); `IETF` (`formula#5` "tổ chức soạn tiêu chuẩn Internet"); `Stripe`/`SRE` (`english#2` "Stripe (công ty thanh toán), API v1", `english#4` "SRE (sách vận hành của Google)").
- **Nguồn & 10 câu tiếng Anh**: **ĐÃ** bảo toàn nguyên văn 10 câu và `số minh hoạ`.
- **Mục mới / còn lại ghi nhận**:
  1. `example#2` (`KhoaLuyDang.py`): gọi `tao_hub()` và `so_du(db)` (không hiện thân hàm/`executescript` trên màn hình).
  2. `quymo#1` (`DoiSoat.py`): gọi `chay(n)` (không hiện thân hàm `ghi_no, ghi_co = {}, {}` trên màn hình).
  3. Lỗi chính tả nhỏ ở `english#4` dòng 8 (`frames/00083.png`): `(SRE (sách vận hành của Google))` dư một dấu ngoặc đóng lồng ngoài.

### L37 — `lessons/bnx/L37_tsql_jdbc_xact_abort_chen_ma.yaml`
- **SHOULD `hook#1` (Oracle hoàn tác không đo ở bài)**: **ĐÃ** — `hook#1` (`frames/00001.png`) ghi `(không đo ở bài này)` trên màn hình và `say` đọc "nhưng bài này không đo điều đó".
- **P1 Chắc**: 0.
- **P1 Vừa (5/5)**: **ĐÃ** — `CREATE OR ALTER PROCEDURE ... AS BEGIN ... END` (`formula#1` hàng 1, trước `formula#2`); `EXEC (@sql)` (`quymo#1` hàng 4 và ghi chú ở `pitfalls#2`, `frames/00095.png`); `N'…'`, `NVARCHAR(200)` (`quymo#1` hàng 3, trước `quymo#2`); `new String[] {"A", "X' OR '1'='1"}` (`check#5` hàng 1, trước `check#6`); `rs.next()`, `rs.getInt(1)` (`check#5` hàng 2, trước `check#7`).
- **P1 Yếu (6/6)**: **ĐÃ** — `IF DB_ID(...)`, `dbo.`, `VARCHAR(10)` (`prereq#2` trước `prereq#3`); `BEGIN TRAN/COMMIT/ROLLBACK`, `SELECT SUM(so_du) AS tong` (`formula#1` hàng 2–3); `public static void main(String[] args) throws Exception`, `catch (SQLException e)` (`check#2` hàng 1, 3 trước `check#3`).
- **Dựng lại bảng, số liệu & mục còn lại**:
  - `example#3` ("Dựng lại bảng" trước ⑤ `XACT_ABORT OFF`), `example#5` ("Dựng lại bảng lần nữa" trước `ON`), `pitfalls#1` ("ví dụ ⑤"), các số 300k/1M/1,3M/1,2M/1,8M nguyên vẹn.
  - Còn lại (không có bảng riêng, chỉ giảng bằng lời): các API JDBC trong `check#3,4,6` (`try (Connection c = ...)`, `CallableStatement`, `PreparedStatement`, `registerOutParameter`, `Types.VARCHAR`, `execute()`, `getString(4)`, `setString(1, ten)`).
  - `build_report.json`: `tts_sources={'edge': 127, 'edge?': 1}` (cache cũ, `tts_sha256` khớp).

### L38 — `lessons/bnx/L38_oracle_hang_doi_bo_nho_cot_phan_manh.yaml`
- **P1 Chắc**: 0.
- **P1 Vừa (8/8)**: **ĐÃ** —
  1. `eo DBMS_AQ.ENQUEUE_OPTIONS_T;`, `bnx_l38_msg(101, 500000)` (`formula#2` hàng 1–2, `frames/00032.png`, trước `formula#3`).
  2. `dq.wait := DBMS_AQ.NO_WAIT;`, `'nhan: ' || m.ma_gd || …` (`formula#5` hàng 1–2, trước `formula#6`).
  3. `[tuple(range(i, i + COT)) for i in range(n)]`, `[[h[c] for h in bang] for c in range(COT)]` (`example#4` hàng 2–3, trước `example#5`).
  4. `hang, cho = hang + cho, []`, `elif t[0] == "nhan" and hang:` (`check#1` hàng 3–4, `frames/00060.png`, trước `check#2`).
  5. `[(a, b) for a in range(tk) for b in range(tk) if a != b]` (`quymo#1` hàng 1, trước `quymo#2`).
- **P1 Yếu (3/3)**: **ĐÃ** — `hang.pop(0)` (`check#1` hàng 4), `sum(1 for a, b in cap if …)` (`quymo#1` hàng 2), `{100 * x / n:.1f}` (`quymo#1` hàng 3), `100_000` (`example#4` hàng 1), cộng thêm `example#2` (`DemO.py`) và `pitfalls#3` (`sum(1 for a in range(1000) ...)`).
- **Số liệu & nhận xét**: Mọi số đã kiểm (`1`/`0` thông điệp, `INMEMORY_SIZE = 0` → chưa đo được, `8 000`/`800 000` ô, `0`/`2 400`/`3 480` lệnh xuyên mảnh, `748/1 000`) và nhãn mô hình (`check#3`, `source`) nguyên vẹn. (Ghi chú: các bảng dùng hàm cục bộ `jt()` ở L38 chỉ đọc 1 câu tóm tắt trong `say`, chi tiết từng hàng nằm trên màn hình.)

---

## 4. Lỗi mới / tồn đọng cần lưu ý

1. **L28 `example#11` (`out/BNX/L28/frames/00073.png`) — `MỘT PHẦN` từ SHOULD R4**: Dòng `var rut = () => db.tk.updateOne({_id: "001", so_du: {$gte: 600}}, {$inc: {so_du: -600}}).modifiedCount;` vẫn chạm/lấn nhẹ đường viền phải khung `.code` ở dấu `;` cuối.
2. **L36 `example#2`, `quymo#1` — 2 hàm ẩn chưa định nghĩa trên màn hình** (đã nêu ở `fix6_BNX_C.md`): `tao_hub()`/`so_du(db)` và `chay(n)` của `DoiSoat.py`.
3. **L36 `english#4` dòng 8 (`frames/00083.png`) — lỗi dấu ngoặc nhỏ**: `(SRE (sách vận hành của Google))` có 2 dấu `))` liền nhau.
4. **L37 `check#3,4,6`**: các phương thức JDBC (`CallableStatement`, `PreparedStatement`, `registerOutParameter`, `Types.VARCHAR`, `execute()`, `getString(4)`, `setString(1, ten)`) mới giải thích bằng lời `say`, chưa có hàng bảng `viết trong mã | đọc là`.
5. **L37 `build_report.json`**: `tts_sources` còn `edge?: 1` (cache cũ, `tts_sha256` khớp 100% với đặc tả).
