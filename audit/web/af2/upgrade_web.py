"""Nâng trọn bộ 16 bài WEB (L00–L15) lên chuẩn AF2 theo bảng quyết định BN-08.

Toàn bộ 16 bài chạy THẬT trên Node.js v25.8.0 (`*.js` qua `labs/cham.sh`):
tính RTT web, phân tích cây HTML, CSS box-model, vòng lặp sự kiện microtask/macrotask thật,
Promise.all song song, thuật toán LIS cập nhật danh sách, chuẩn RFC 9110, phân trang,
HTTP cache freshness, PKCE SHA-256 Base64URL thật bằng module `crypto`, độ tương phản WCAG,
ngân sách khung hình 60/120Hz, hợp nhất ngoại tuyến, và suy giảm phiên bản cũ.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "audit" / "review"))
import af2_kit as ak  # noqa: E402
import af2_upgrader as up  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")

LESSONS = [
    (
        "L00", "js", "Mỗi vòng bắt tay TCP + TLS + HTTP tốn thêm 1 RTT (vòng đi về) trước byte đầu tiên (TTFB)",
        "# Lab WEB L00 — Node.js thật: tính TTFB (thời gian trước byte đầu tiên) qua TCP + TLS + HTTP với RTT\n\n"
        "Viết tập lệnh Node.js (`*.js`) tính thời gian trước byte đầu tiên TTFB qua 3 chặng (TCP, TLS, HTTP GET) "
        "ở `RTT = 50 ms` so với người dùng ở xa `RTT = 200 ms` cộng `4` lượt gọi API tuần tự, in đúng 3 dòng:\n"
        "1. `ttfb_50ms=150`\n2. `remote_200ms_4api=1400`\n3. `roundtrips_handshake=3`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh WEB L00 duong_dan/bai_cua_ban.js\n```",
        "const stages = ['TCP', 'TLS', 'HTTP'], ttfb = rtt => stages.length * rtt;\n"
        "console.log(`ttfb_50ms=${ttfb(50)}`);\n"
        "console.log(`remote_200ms_4api=${ttfb(200) + 4 * 200}`);\n"
        "console.log(`roundtrips_handshake=${stages.length}`);\n",
    ),
    (
        "L01", "js", "Cây HTML tạo các nút lồng nhau, đo bằng tổng số thẻ và độ sâu tối đa",
        "# Lab WEB L01 — Node.js thật: phân tích cây DOM từ chuỗi thẻ HTML\n\n"
        "Viết tập lệnh Node.js dùng stack đọc các thẻ mở/đóng của `<ul><li>A</li><li>B<b>!</b></li></ul>` "
        "để đếm tổng số phần tử và độ sâu lớn nhất của cây DOM, in đúng 3 dòng:\n"
        "1. `nodes=4`\n2. `max_depth=3`\n3. `valid_balanced=1`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh WEB L01 duong_dan/bai_cua_ban.js\n```",
        "const html = '<ul><li>A</li><li>B<b>!</b></li></ul>';\n"
        "let nodes = 0, d = 0, mx = 0;\n"
        "for (const [, close, tag] of html.matchAll(/<(\\/?)([a-z]+)>/g)) {\n"
        "  if (!close) { nodes++; d++; mx = Math.max(mx, d); } else d--;\n"
        "}\n"
        "console.log(`nodes=${nodes}`); console.log(`max_depth=${mx}`);\n"
        "console.log(`valid_balanced=${Number(d === 0)}`);\n",
    ),
    (
        "L02", "js", "box-sizing: content-box cộng thêm padding + border vào width; border-box giữ nguyên",
        "# Lab WEB L02 — Node.js thật: CSS Box Model và điểm ưu tiên bộ chọn (ID, Class, Tag)\n\n"
        "Viết tập lệnh Node.js tính tổng bề rộng `width=200, padding=20, border=5` theo `content-box` và `border-box`, "
        "đồng thời so sánh độ ưu tiên `(id, class, tag)` giữa `#nav a` và `.menu .item a`, in đúng 3 dòng:\n"
        "1. `content_box_w=250`\n2. `border_box_w=200`\n3. `id_beats_2class=1`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh WEB L02 duong_dan/bai_cua_ban.js\n```",
        "const w = 200, pad = 20, bd = 5;\n"
        "const cb = w + 2 * (pad + bd), bb = w;\n"
        "const specA = [1, 0, 1], specB = [0, 2, 1];\n"
        "console.log(`content_box_w=${cb}`); console.log(`border_box_w=${bb}`);\n"
        "console.log(`id_beats_2class=${Number(specA[0] > specB[0])}`);\n",
    ),
    (
        "L03", "js", "Event Loop V8 chạy mã đồng bộ -> toàn bộ microtask Promise -> macrotask setTimeout",
        "# Lab WEB L03 — Node.js thật: kiểm chứng thứ tự 1, 4, 3, 2 trên V8 Event Loop\n\n"
        "Viết tập lệnh Node.js thực thi đồng bộ (`1`, `4`), `Promise.resolve().then(...)` (`3`) và `setTimeout(..., 0)` (`2`) "
        "vào mảng `order` để chứng minh microtask luôn chạy trước macrotask, in đúng 3 dòng:\n"
        "1. `sync_done=1`\n2. `event_loop_order=1,4,3,2`\n3. `micro_before_macro=1`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh WEB L03 duong_dan/bai_cua_ban.js\n```",
        "const out = [1]; let syncDone = 0;\n"
        "setTimeout(() => { out.push(2);\n"
        "  console.log(`sync_done=${syncDone}`);\n"
        "  console.log('event_loop_order=' + out.join(','));\n"
        "  console.log(`micro_before_macro=${Number(out.indexOf(3) < out.indexOf(2))}`);\n"
        "}, 0);\n"
        "Promise.resolve().then(() => out.push(3));\n"
        "out.push(4); syncDone = Number(out.length === 2);\n",
    ),
    (
        "L04", "js", "Chạy bất đồng bộ song song tốn max(ti), tuần tự tốn sum(ti)",
        "# Lab WEB L04 — Node.js thật: đo thời gian chờ tuần tự vs Promise.all\n\n"
        "Viết hàm `async` mô phỏng 3 tác vụ `100, 200, 300 ms`: tính tổng thời gian lý thuyết khi `await` tuần tự (`600`) "
        "vs chạy đồng thời `Promise.all` (`300`) và mức tăng tốc, in đúng 3 dòng:\n"
        "1. `seq_ms=600`\n2. `parallel_ms=300`\n3. `speedup=2.0x`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh WEB L04 duong_dan/bai_cua_ban.js\n```",
        "const t = [100, 200, 300];\n"
        "const seq = t.reduce((a, b) => a + b, 0), par = Math.max(...t);\n"
        "console.log(`seq_ms=${seq}`); console.log(`parallel_ms=${par}`);\n"
        "console.log(`speedup=${(seq / par).toFixed(1)}x`);\n",
    ),
    (
        "L05", "js", "Khớp danh sách theo key chỉ giữ lại dãy con tăng dài nhất (LIS), dời tối thiểu phần tử còn lại",
        "# Lab WEB L05 — Node.js thật: tính LIS để tối thiểu thao tác DOM khi cập nhật danh sách\n\n"
        "Viết tập lệnh Node.js tìm độ dài dãy con tăng dài nhất (LIS) của `[A, B, C, D, E]` biến thành `[C, A, B, D, E]` "
        "(chỉ số `[2, 0, 1, 3, 4]` -> LIS = `[0, 1, 3, 4]` giữ `4` nút, chỉ dời `1` nút), in đúng 3 dòng:\n"
        "1. `kept_in_place=4`\n2. `min_moves=1`\n3. `total_items=5`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh WEB L05 duong_dan/bai_cua_ban.js\n```",
        "const a = [2, 0, 1, 3, 4], dp = a.map(() => 1);\n"
        "for (let i = 0; i < a.length; i++)\n"
        "  for (let j = 0; j < i; j++) if (a[j] < a[i]) dp[i] = Math.max(dp[i], dp[j] + 1);\n"
        "const lis = Math.max(...dp);\n"
        "console.log(`kept_in_place=${lis}`); console.log(`min_moves=${a.length - lis}`);\n"
        "console.log(`total_items=${a.length}`);\n",
    ),
    (
        "L06", "js", "GET an toàn & lũy đẳng; PUT/DELETE lũy đẳng; POST không an toàn không lũy đẳng",
        "# Lab WEB L06 — Node.js thật: kiểm chuẩn RFC 9110 phương thức HTTP và lũy đẳng\n\n"
        "Viết bảng kiểm chuẩn các phương thức `GET, PUT, DELETE, POST` và mô phỏng Idempotency-Key chống trừ tiền 2 lần khi gửi lại `POST /pay`, in đúng 3 dòng:\n"
        "1. `get_safe_idem=1,1`\n2. `put_safe_idem=0,1`\n3. `post_with_idem_key_bal=150`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh WEB L06 duong_dan/bai_cua_ban.js\n```",
        "const RFC = { GET:[1,1], PUT:[0,1], DELETE:[0,1], POST:[0,0] };\n"
        "let bal = 250; const seen = new Set();\n"
        "const pay = (k, v) => { if (!seen.has(k)) { seen.add(k); bal -= v; } };\n"
        "pay('k1', 100); pay('k1', 100);\n"
        "console.log('get_safe_idem=' + RFC.GET.join(','));\n"
        "console.log('put_safe_idem=' + RFC.PUT.join(','));\n"
        "console.log(`post_with_idem_key_bal=${bal}`);\n",
    ),
    (
        "L07", "js", "OFFSET 19 980 dòng quét bỏ vô ích; Cursor (keyset) nhảy thẳng qua chỉ mục",
        "# Lab WEB L07 — Node.js thật: so sánh chi phí phân trang OFFSET vs Cursor\n\n"
        "Viết tập lệnh Node.js tính số dòng cần đọc và bỏ qua khi lấy trang `1 000` (mỗi trang `20` dòng) "
        "bằng `OFFSET` (`19 980` dòng bị bỏ) so với Cursor (`0` dòng bỏ), in đúng 3 dòng:\n"
        "1. `offset_skipped=19980`\n2. `offset_scanned=20000`\n3. `cursor_scanned=20`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh WEB L07 duong_dan/bai_cua_ban.js\n```",
        "const page = 1000, size = 20, off = (page - 1) * size;\n"
        "console.log(`offset_skipped=${off}`);\n"
        "console.log(`offset_scanned=${off + size}`);\n"
        "console.log(`cursor_scanned=${size}`);\n",
    ),
    (
        "L08", "js", "Hết hạn max-age gửi kèm If-None-Match ETag: khớp trả 304 nhẹ hơn nhiều 200",
        "# Lab WEB L08 — Node.js thật: kiểm độ tươi Cache-Control & phản hồi ETag 304\n\n"
        "Viết hàm Node.js đánh giá yêu cầu cache: `max-age=600`, tuổi bản lưu `700 s`, gửi `If-None-Match='\"v42\"'` "
        "so với ETag máy chủ `'\"v42\"'`, trả mã HTTP `304`, in đúng 3 dòng:\n"
        "1. `is_stale=1`\n2. `status_code=304`\n3. `body_resent=0`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh WEB L08 duong_dan/bai_cua_ban.js\n```",
        "const stale = 700 > 600, etagClient = '\"v42\"', etagSrv = '\"v42\"';\n"
        "const code = stale ? (etagClient === etagSrv ? 304 : 200) : 200;\n"
        "console.log(`is_stale=${Number(stale)}`);\n"
        "console.log(`status_code=${code}`);\n"
        "console.log(`body_resent=${Number(code === 200)}`);\n",
    ),
    (
        "L09", "js", "PKCE dùng mã hoá Base64URL(SHA256(verifier)) bảo vệ luồng OAuth không cần khoá bí mật",
        "# Lab WEB L09 — Node.js thật: tính chuỗi thử thách PKCE từ chuẩn RFC 7636 bằng module crypto\n\n"
        "Viết tập lệnh Node.js dùng module `crypto` tính `code_challenge = BASE64URL(SHA256(verifier))` (mã hoá Base64 an toàn cho URL) cho vector chuẩn RFC 7636 "
        "`'dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk'`, in đúng 3 dòng:\n"
        "1. `challenge=E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM`\n2. `len=43`\n3. `no_padding=1`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh WEB L09 duong_dan/bai_cua_ban.js\n```",
        "const crypto = require('crypto');\n"
        "const v = 'dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk';\n"
        "const ch = crypto.createHash('sha256').update(v).digest('base64url');\n"
        "console.log(`challenge=${ch}`);\n"
        "console.log(`len=${ch.length}`);\n"
        "console.log(`no_padding=${Number(!ch.includes('='))}`);\n",
    ),
    (
        "L10", "js", "Giảm kích thước tải JS từ 2 MB xuống 500 KB hạ thời gian tải 4 lần (10s -> 2.5s)",
        "# Lab WEB L10 — Node.js thật: đo thời gian tải gói theo kích thước & băng thông\n\n"
        "Viết tập lệnh Node.js tính thời gian tải gói `2 000 KB` vs `500 KB` trên đường truyền `200 KB/s`, in đúng 3 dòng:\n"
        "1. `time_2mb_s=10.0`\n2. `time_500kb_s=2.5`\n3. `faster_by=4.0x`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh WEB L10 duong_dan/bai_cua_ban.js\n```",
        "const t1 = 2000 / 200, t2 = 500 / 200;\n"
        "console.log(`time_2mb_s=${t1.toFixed(1)}`);\n"
        "console.log(`time_500kb_s=${t2.toFixed(1)}`);\n"
        "console.log(`faster_by=${(t1 / t2).toFixed(1)}x`);\n",
    ),
    (
        "L11", "js", "Chuẩn tương phản WCAG AA cho chữ thường yêu cầu tỉ số >= 4.5:1 (#777 trượt, #767676 đạt)",
        "# Lab WEB L11 — Node.js thật: tính độ tương phản màu WCAG 2.1 (#777777 vs #767676)\n\n"
        "Viết hàm Node.js tính độ chói tương đối `L` và tỉ số `(L1 + 0.05)/(L2 + 0.05)` so với nền trắng `#FFFFFF` "
        "cho hai màu `#777777` và `#767676`, in đúng 3 dòng:\n"
        "1. `ratio_777=4.48`\n2. `ratio_767676=4.54`\n3. `aa_pass_pair=0,1`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh WEB L11 duong_dan/bai_cua_ban.js\n```",
        "const lin = c => (c <= 0.04045 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4));\n"
        "const lum = hex => 0.2126*lin(parseInt(hex.slice(1,3),16)/255)+0.7152*lin(parseInt(hex.slice(3,5),16)/255)+0.0722*lin(parseInt(hex.slice(5,7),16)/255);\n"
        "const cr = (h1, h2) => { const [a, b] = [lum(h1), lum(h2)].sort((x,y)=>y-x); return (a+0.05)/(b+0.05); };\n"
        "const r1 = cr('#777777', '#ffffff'), r2 = cr('#767676', '#ffffff');\n"
        "console.log(`ratio_777=${r1.toFixed(2)}`); console.log(`ratio_767676=${r2.toFixed(2)}`);\n"
        "console.log(`aa_pass_pair=${Number(r1 >= 4.5)},${Number(r2 >= 4.5)}`);\n",
    ),
    (
        "L12", "js", "Màn 60 Hz cho tối đa 16.7 ms/khung, 120 Hz chỉ còn 8.3 ms/khung",
        "# Lab WEB L12 — Node.js thật: ngân sách thời gian khung hình giao diện 60Hz và 120Hz\n\n"
        "Viết tập lệnh Node.js tính ngân sách mỗi khung hình (`1000 / Hz`) cho `60 Hz` và `120 Hz`, "
        "và kiểm tra một tác vụ chạy trên luồng giao diện mất `12 ms` có làm rớt khung ở từng tần số không, in đúng 3 dòng:\n"
        "1. `budget_60hz_ms=16.7`\n2. `budget_120hz_ms=8.3`\n3. `task12ms_jank_at_60_120=0,1`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh WEB L12 duong_dan/bai_cua_ban.js\n```",
        "const b60 = 1000 / 60, b120 = 1000 / 120;\n"
        "console.log(`budget_60hz_ms=${b60.toFixed(1)}`);\n"
        "console.log(`budget_120hz_ms=${b120.toFixed(1)}`);\n"
        "console.log(`task12ms_jank_at_60_120=${Number(12 > b60)},${Number(12 > b120)}`);\n",
    ),
    (
        "L13", "js", "Hợp nhất tập hợp cộng (G-Set) đạt giao hoán, kết hợp nên đồng bộ không mất",
        "# Lab WEB L13 — Node.js thật: kiểm chứng hợp nhất không mất dữ liệu ở chế độ ngoại tuyến\n\n"
        "Viết tập lệnh Node.js mô phỏng hai máy ngoại tuyến cùng thêm `'mua sua'` và `'goi me'` vào tập hợp gốc `{'lam bai'}`: "
        "kiểm tra hợp nhất hai chiều `merge(A, B)` và `merge(B, A)` đều cho kết quả y hệt (`3` mục), in đúng 3 dòng:\n"
        "1. `merged_len=3`\n2. `commutative=1`\n3. `idempotent=1`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh WEB L13 duong_dan/bai_cua_ban.js\n```",
        "const merge = (a, b) => [...new Set([...a, ...b])].sort();\n"
        "const a = ['lam bai', 'mua sua'], b = ['lam bai', 'goi me'];\n"
        "const ab = merge(a, b), ba = merge(b, a);\n"
        "console.log(`merged_len=${ab.length}`);\n"
        "console.log(`commutative=${Number(JSON.stringify(ab) === JSON.stringify(ba))}`);\n"
        "console.log(`idempotent=${Number(JSON.stringify(merge(ab, ab)) === JSON.stringify(ab))}`);\n",
    ),
    (
        "L14", "js", "Mỗi tuần 30% người cũ nâng cấp thì sau 4 tuần vẫn còn 0.7^4 = 24.0% dùng bản cũ",
        "# Lab WEB L14 — Node.js thật: tính phần trăm người dùng kẹt ở bản API cũ theo tuần\n\n"
        "Viết tập lệnh Node.js tính tỉ lệ còn lại ở bản cũ sau `4` và `8` tuần nếu mỗi tuần có `30%` số người còn lại nâng cấp (`0.7^k`), in đúng 3 dòng:\n"
        "1. `week4_old_pct=24.0%`\n2. `week8_old_pct=5.8%`\n3. `weeks_under_10pct=7`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh WEB L14 duong_dan/bai_cua_ban.js\n```",
        "let k = 0; while (Math.pow(0.7, k) >= 0.10) k++;\n"
        "console.log(`week4_old_pct=${(100 * Math.pow(0.7, 4)).toFixed(1)}%`);\n"
        "console.log(`week8_old_pct=${(100 * Math.pow(0.7, 8)).toFixed(1)}%`);\n"
        "console.log(`weeks_under_10pct=${k}`);\n",
    ),
    (
        "L15", "js", "HTTP/1.0 mở kết nối mới mất 22 RTT (1100 ms); ghép kênh HTTP/2 giảm mạnh còn 3 RTT",
        "# Lab WEB L15 — Node.js thật: so sánh độ trễ RTT từ HTTP/1.0 tới HTTP/2 và HTTP/3\n\n"
        "Viết tập lệnh Node.js tính độ trễ tải `1 HTML + 10 ảnh` ở `RTT = 50 ms` bằng HTTP/1.0 (`22` RTT), HTTP/1.1 keep-alive 1 kết nối tuần tự (`12` RTT), và HTTP/2 ghép kênh (`3` RTT), in đúng 3 dòng:\n"
        "1. `http10_ms=1100`\n2. `http11_ms=600`\n3. `http2_ms=150`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh WEB L15 duong_dan/bai_cua_ban.js\n```",
        "const rtt = 50;\n"
        "console.log(`http10_ms=${22 * rtt}`);\n"
        "console.log(`http11_ms=${12 * rtt}`);\n"
        "console.log(`http2_ms=${3 * rtt}`);\n",
    ),
]

for lid, ext, hint, de_md, sol in LESSONS:
    cov = [(1, "stage1" if lid == "L15" else "example"), (2, "check"), (3, "practice")]
    fp, lo = up.apply_upgrade("WEB", lid, de_md=de_md, ext=ext, sol_code=sol, de_hint=hint, covers=cov)
    print(f"OK WEB {lid}: {fp.name} ({len(lo.splitlines())} dòng)")

led_p, nblk = up.sync_course_ledger("WEB", default_lang="javascript")
print(f"Synced {led_p.relative_to(ROOT)}: {nblk} blocks")
tpl = subprocess.run([ak.VENV_PY, "-B", "audit/review/sync_tpl_from_lesson.py", "web", "--write"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
print("sync_tpl WEB:", tpl.stdout.strip() or tpl.stderr.strip())
