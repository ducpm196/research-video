"""Nâng trọn bộ 16 bài SEC (L00–L15) lên chuẩn AF2 theo bảng quyết định BN-08.

Chạy thật PBKDF2/hashlib, HMAC-SHA256 RFC 2104, escaping chống XSS, truy vấn tham số
SQLite chống SQLi, RSA đồ chơi ký chứng chỉ, phân tích entropy Diceware, Bayes PPV,
và Heartbleed.
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
        "L00", "py", "6 mối đe doạ STRIDE ánh xạ tương ứng 1-1 tới 6 thuộc tính an toàn bị xâm phạm",
        "# Lab SEC L00 — Ánh xạ mô hình đe doạ STRIDE sang thuộc tính an toàn\n\n"
        "Viết chương trình Python cài bảng ánh xạ STRIDE và kiểm tra 6 cặp 1-1 không trùng lặp, "
        "truy vấn tính chất bị vi phạm của `Information Disclosure` (lộ thông tin → `Confidentiality` bí mật), `Tampering` (sửa lén → `Integrity` toàn vẹn) và `Spoofing` (giả mạo → `Authentication` xác thực), in đúng 3 dòng:\n"
        "1. `stride_unique_props=6`\n2. `info_disclosure=Confidentiality`\n3. `tampering=Integrity spoofing=Authentication`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh SEC L00 duong_dan/bai_cua_ban.py\n```",
        "m = {'S':'Authentication','T':'Integrity','R':'NonRepudiation','I':'Confidentiality','D':'Availability','E':'Authorization'}\n"
        "print(f'stride_unique_props={len(set(m.values()))}')\n"
        "print(f'info_disclosure={m[\"I\"]}')\n"
        "print(f'tampering={m[\"T\"]} spoofing={m[\"S\"]}')\n",
    ),
    (
        "L01", "py", "PBKDF2 chậm làm tăng thời gian vét từ vài giây lên hàng triệu lần",
        "# Lab SEC L01 — PBKDF2-HMAC-SHA256 thật + tính thời gian vét cạn\n\n"
        "Viết chương trình Python dùng `hashlib.pbkdf2_hmac` dẫn xuất khoá 32 byte dạng chuỗi hệ 16 (`hex`, 64 ký tự) từ `b'pw'` với muối ngẫu nhiên (`salt`) `b'salt1'` "
        "qua `10 000` vòng, đồng thời tính thời gian thử `26^8` mật khẩu ở tốc độ nhanh `1e10/s` vs chậm `1e4/s`, in đúng 3 dòng:\n"
        "1. `fast_crack_s=20.9`\n2. `slow_crack_days=242`\n3. `pbkdf2_hex_len=64`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh SEC L01 duong_dan/bai_cua_ban.py\n```",
        "import hashlib\ndk = hashlib.pbkdf2_hmac('sha256', b'pw', b'salt1', 10000).hex()\n"
        "fast = (26 ** 8) / 1e10; slow_d = (26 ** 8) / (1e4 * 86400)\n"
        "print(f'fast_crack_s={fast:.1f}')\nprint(f'slow_crack_days={round(slow_d)}')\nprint(f'pbkdf2_hex_len={len(dk)}')\n",
    ),
    (
        "L02", "py", "4 từ ngẫu nhiên trong 7776 từ cho 51.7 bit entropy, mạnh hơn 8 chữ thường (37.6 bit)",
        "# Lab SEC L02 — Tính entropy log2(N^L) của mật khẩu ký tự vs cụm từ Diceware\n\n"
        "Viết chương trình Python tính entropy của `8` chữ thường ngẫu nhiên (`26^8`) so với `4` từ ngẫu nhiên "
        "chọn từ từ điển `7 776` từ (cụm từ Diceware, `7776^4`), và kiểm tra 4 từ có mạnh hơn 8 chữ thường không (`1` = có, `0` = không), in đúng 3 dòng:\n"
        "1. `bits_8_lower=37.6`\n2. `bits_4_words=51.7`\n3. `words_stronger=1`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh SEC L02 duong_dan/bai_cua_ban.py\n```",
        "import math\nb1 = math.log2(26 ** 8); b2 = math.log2(7776 ** 4)\n"
        "print(f'bits_8_lower={b1:.1f}')\nprint(f'bits_4_words={b2:.1f}')\n"
        "print(f'words_stronger={int(b2 > b1)}')\n",
    ),
    (
        "L03", "py", "Khoá sau 3 lần sai giữ xác suất đoán trúng OTP (mã một lần) 6 số chỉ ở 3 / 10^6",
        "# Lab SEC L03 — Ràng buộc thử sai OTP (mã dùng một lần) 6 chữ số & tính xác suất trúng\n\n"
        "Viết chương trình Python tính xác suất trúng nếu kẻ tấn công được thử `3` lần trên `10^6` mã 6 chữ số "
        "so với thử tự do `500 000` lần khi không có giới hạn tần suất, in đúng 3 dòng:\n"
        "1. `prob_3_tries=3e-06`\n2. `prob_unbounded_500k=0.50`\n3. `rate_limit_factor=166667x`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh SEC L03 duong_dan/bai_cua_ban.py\n```",
        "p3 = 3 / 1_000_000; p500 = 500_000 / 1_000_000\n"
        "print(f'prob_3_tries={p3:.0e}')\nprint(f'prob_unbounded_500k={p500:.2f}')\n"
        "print(f'rate_limit_factor={round(p500 / p3)}x')\n",
    ),
    (
        "L04", "py", "Nguyên tắc quyền tối thiểu chỉ cấp quyền vừa đủ theo vai trò RBAC (phân quyền theo vai trò)",
        "# Lab SEC L04 — Kiểm tra chính sách phân quyền theo vai trò (RBAC) tối thiểu\n\n"
        "Viết chương trình Python cài bảng phân quyền theo vai trò `RBAC = {'accountant': {'read', 'create'}, 'auditor': {'read'}}`: "
        "kiểm tra kiểm toán viên tạo hoá đơn bị từ chối, còn kế toán viên đọc/tạo hợp lệ, in đúng 3 dòng:\n"
        "1. `accountant_create=1`\n2. `auditor_read=1`\n3. `auditor_create_denied=1`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh SEC L04 duong_dan/bai_cua_ban.py\n```",
        "RBAC = {'accountant': {'read', 'create'}, 'auditor': {'read'}}\n"
        "can = lambda role, act: int(act in RBAC.get(role, set()))\n"
        "print(f'accountant_create={can(\"accountant\", \"create\")}')\n"
        "print(f'auditor_read={can(\"auditor\", \"read\")}')\n"
        "print(f'auditor_create_denied={1 - can(\"auditor\", \"create\")}')\n",
    ),
    (
        "L05", "py", "SameSite=Strict/Lax chặn gửi kèm cookie trong POST chéo trang (giả mạo CSRF)",
        "# Lab SEC L05 — Kiểm tra chính sách cookie SameSite trước POST chéo trang\n\n"
        "Viết hàm `cookie_sent(same_site, method, cross_site)` mô phỏng quy tắc trình duyệt: "
        "`None` vẫn gửi khi `POST` chéo trang; `Lax` và `Strict` không gửi cookie khi `POST` từ trang lạ, in đúng 3 dòng:\n"
        "1. `none_cross_post=1`\n2. `lax_cross_post=0`\n3. `strict_cross_post=0`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh SEC L05 duong_dan/bai_cua_ban.py\n```",
        "def cookie_sent(ss, m, cross):\n    if not cross: return 1\n"
        "    if ss == 'None': return 1\n    if ss == 'Lax': return int(m == 'GET')\n    return 0\n"
        "print(f'none_cross_post={cookie_sent(\"None\", \"POST\", True)}')\n"
        "print(f'lax_cross_post={cookie_sent(\"Lax\", \"POST\", True)}')\n"
        "print(f'strict_cross_post={cookie_sent(\"Strict\", \"POST\", True)}')\n",
    ),
    (
        "L06", "py", "Thoát ký tự đặc biệt HTML chống chèn mã (XSS) và tham số hoá ? trên SQLite chống chèn SQL (SQLi)",
        "# Lab SEC L06 — Phòng thủ XSS (chèn mã HTML) bằng html.escape và chèn SQL (SQLi) bằng ?\n\n"
        "Viết chương trình Python thoát ký tự đặc biệt HTML của chuỗi `<script>alert(1)</script>` bằng `html.escape` "
        "và kiểm tra truy vấn SQLite tham số hoá `?` chặn chuỗi tấn công (payload) `' OR '1'='1`, in đúng 3 dòng:\n"
        "1. `raw_lt_present=0`\n2. `escaped_len=37`\n3. `sqli_rows=0`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh SEC L06 duong_dan/bai_cua_ban.py\n```",
        "import html, sqlite3\ne = html.escape('<script>alert(1)</script>')\n"
        "c = sqlite3.connect(':memory:'); c.execute('CREATE TABLE u(n TEXT)'); c.execute(\"INSERT INTO u VALUES('an')\")\n"
        "rows = c.execute('SELECT * FROM u WHERE n=?', (\"' OR '1'='1\",)).fetchall()\n"
        "print(f'raw_lt_present={int(\"<\" in e)}')\nprint(f'escaped_len={len(e)}')\n"
        "print(f'sqli_rows={len(rows)}')\n",
    ),
    (
        "L07", "py", "Chế độ ECB biến hai khối rõ giống nhau thành hai khối mã y hệt; chế độ bộ đếm CTR (kèm số dùng một lần) không bị",
        "# Lab SEC L07 — Phát hiện lộ mẫu trên chế độ ECB vs mã khối CTR (chế độ bộ đếm) dùng số dùng một lần (IV/nonce)\n\n"
        "Viết chương trình Python mô phỏng mã hoá từng khối 8 byte giả lập chế độ khối đơn ECB (cố định) so với chế độ bộ đếm CTR (XOR thêm khoá + bộ đếm/số dùng một lần IV/nonce) "
        "trên bản rõ 16 byte lặp 2 khối giống nhau `b'BLOCK_A_' * 2`, cắt `msg[:8]` và `msg[8:]` rồi kiểm tra trực tiếp hai khối mã ECB có trùng nhau làm lộ mẫu không, in đúng 3 dòng:\n"
        "1. `ecb_blocks_identical=1`\n2. `ctr_blocks_identical=0`\n3. `ecb_leaks_pattern=1`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh SEC L07 duong_dan/bai_cua_ban.py\n```",
        "import hashlib\nenc = lambda k, b: hashlib.sha256(k + b).digest()[:8]\n"
        "msg = b'BLOCK_A_' * 2; b0, b1 = msg[:8], msg[8:]; k = b'key'\n"
        "ecb0, ecb1 = enc(k, b0), enc(k, b1)\n"
        "ctr0 = bytes(x ^ y for x, y in zip(b0, enc(k, b'nonce0')))\n"
        "ctr1 = bytes(x ^ y for x, y in zip(b1, enc(k, b'nonce1')))\n"
        "same_ecb = int(ecb0 == ecb1)\n"
        "print(f'ecb_blocks_identical={same_ecb}')\n"
        "print(f'ctr_blocks_identical={int(ctr0 == ctr1)}')\n"
        "print(f'ecb_leaks_pattern={same_ecb}')\n",
    ),
    (
        "L08", "py", "HMAC-SHA256 cần khoá bí mật để ký và dùng compare_digest chống lệch thời gian",
        "# Lab SEC L08 — Tính và xác minh HMAC-SHA256 thật theo RFC 2104\n\n"
        "Viết chương trình Python dùng `hmac.new` tính thẻ xác thực của thông điệp `b'chuyen 100'` với khoá `b'secret'`, "
        "kiểm tra đổi thành `b'chuyen 900'` làm chữ ký không khớp qua `hmac.compare_digest`, in đúng 3 dòng:\n"
        "1. `mac_len_hex=64`\n2. `orig_valid=1`\n3. `tampered_valid=0`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh SEC L08 duong_dan/bai_cua_ban.py\n```",
        "import hashlib, hmac\nk = b'secret'\n"
        "tag = hmac.new(k, b'chuyen 100', hashlib.sha256).hexdigest()\n"
        "t2 = hmac.new(k, b'chuyen 900', hashlib.sha256).hexdigest()\n"
        "print(f'mac_len_hex={len(tag)}')\n"
        "print(f'orig_valid={int(hmac.compare_digest(tag, tag))}')\n"
        "print(f'tampered_valid={int(hmac.compare_digest(tag, t2))}')\n",
    ),
    (
        "L09", "py", "Chữ ký chuỗi chứng chỉ bảo mật kết nối (TLS) phát hiện ngay nếu tên miền bị sửa sau khi tổ chức cấp (CA) đã ký",
        "# Lab SEC L09 — Chuỗi tin cậy TLS: tổ chức cấp chứng chỉ (CA) ký và phát hiện sửa tên miền\n\n"
        "Viết chương trình Python băm tên miền `b'bank.vn'` và `b'evil.vn'` modulo `n = 33` (`e = 3, d = 7`), "
        "tổ chức cấp chứng chỉ (CA) ký chứng chỉ thật rồi máy khách kiểm chứng bằng khoá công khai của CA, in đúng 3 dòng:\n"
        "1. `legit_cert_valid=1`\n2. `forged_domain_valid=0`\n3. `chain_verified=1`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh SEC L09 duong_dan/bai_cua_ban.py\n```",
        "n, e, d = 33, 3, 7\n"
        "m_good = sum(b'bank.vn') % 30 + 2; m_bad = sum(b'evil.vn') % 30 + 2\n"
        "sig = pow(m_good, d, n); rec = pow(sig, e, n)\n"
        "print(f'legit_cert_valid={int(rec == m_good)}')\n"
        "print(f'forged_domain_valid={int(rec == m_bad)}')\n"
        "print(f'chain_verified={int(rec == m_good and rec != m_bad)}')\n",
    ),
    (
        "L10", "py", "Ngưỡng 50% va chạm ngày sinh của băm 64 bit là ~5.06 tỉ mục (tương đương độ an toàn 32 bit)",
        "# Lab SEC L10 — Tính ngưỡng 50% va chạm ngày sinh của hàm băm 64 bit\n\n"
        "Viết chương trình Python tính số giá trị `k ≈ sqrt(2 * 2^64 * ln(2))` cần tạo để xác suất có ít nhất 1 cặp trùng nhau đạt `50%`, "
        "tính số bit bảo mật chống va chạm (`64 / 2 = 32` bit) và kiểm chứng bậc độ lớn của `k` tương đương ngưỡng tiền ảnh của hàm băm 32 bit (`round(k / 2^32) == 1`), in đúng 3 dòng:\n"
        "1. `birthday_50pct_billions=5.06`\n2. `bit_security_collision=32`\n3. `ratio_vs_32bit_hash=1`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh SEC L10 duong_dan/bai_cua_ban.py\n```",
        "import math\nk = math.sqrt(2 * (2 ** 64) * math.log(2))\nbits_sec = 64 // 2\n"
        "print(f'birthday_50pct_billions={k / 1e9:.2f}')\n"
        "print(f'bit_security_collision={bits_sec}')\n"
        "print(f'ratio_vs_32bit_hash={round(k / (2 ** bits_sec))}')\n",
    ),
    (
        "L11", "py", "Ngẫu nhiên hoá địa chỉ (ASLR) 16 bit entropy buộc đoán trung bình 2^15 = 32 768 lần",
        "# Lab SEC L11 — Tính kỳ vọng số lần đoán khi dùng ngẫu nhiên hoá địa chỉ (ASLR) với 16 bit và 28 bit\n\n"
        "Viết chương trình Python tính số vùng địa chỉ có thể với `16` bit (`2^16 = 65 536`), với `28` bit (`2^28 = 268 435 456`) "
        "và kỳ vọng số lần đoán trung bình `(2^16)/2 = 32 768` khi chương trình khởi động lại mỗi lần đoán sai **nhưng giữ nguyên bố trí địa chỉ**, in đúng 3 dòng:\n"
        "1. `slots_16bit=65536`\n2. `expected_guesses_16=32768`\n3. `slots_28bit=268435456`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh SEC L11 duong_dan/bai_cua_ban.py\n```",
        "s16 = 2 ** 16; s28 = 2 ** 28\n"
        "print(f'slots_16bit={s16}')\nprint(f'expected_guesses_16={s16 // 2}')\n"
        "print(f'slots_28bit={s28}')\n",
    ),
    (
        "L12", "py", "Tường lửa so từ trên xuống (khớp đầu tiên first-match) kết thúc bằng luật mặc định chặn DENY",
        "# Lab SEC L12 — Mô phỏng bảng luật tường lửa khớp đầu tiên (first-match) và chặn mặc định\n\n"
        "Viết hàm `decide(src, dst, port)` xét từ trên xuống danh sách luật `[(app, db, 5432, ALLOW (cho)), (*, *, *, DENY (chặn))]` "
        "cho 3 lưu lượng `(app->db:5432)`, `(web->db:5432)`, `(app->db:22)`, in đúng 3 dòng:\n"
        "1. `app_db_5432=ALLOW`\n2. `web_db_5432=DENY`\n3. `app_db_22=DENY`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh SEC L12 duong_dan/bai_cua_ban.py\n```",
        "RULES = [('app','db',5432,'ALLOW'), ('*','*','*','DENY')]\n"
        "def decide(s, d, p):\n    for rs, rd, rp, act in RULES:\n"
        "        if (rs in ('*', s)) and (rd in ('*', d)) and (rp in ('*', p)): return act\n"
        "print(f'app_db_5432={decide(\"app\",\"db\",5432)}')\n"
        "print(f'web_db_5432={decide(\"web\",\"db\",5432)}')\n"
        "print(f'app_db_22={decide(\"app\",\"db\",22)}')\n",
    ),
    (
        "L13", "py", "Với tỉ lệ nền 1/10 000 và báo nhầm 1%, tỉ lệ cảnh báo là thật (Bayes PPV) chỉ đạt 0.98%",
        "# Lab SEC L13 — Định lý Bayes và nghịch lý tỉ lệ nền trong cảnh báo xâm nhập\n\n"
        "Viết chương trình Python tính xác suất một cảnh báo là tấn công thật `P(A | +)` khi tỉ lệ tấn công `1/10 000`, "
        "độ nhạy `99%` và báo nhầm `1%`, in đúng 3 dòng:\n"
        "1. `tp_per_1m=99`\n2. `fp_per_1m=9999`\n3. `ppv_pct=0.98%`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh SEC L13 duong_dan/bai_cua_ban.py\n```",
        "prev = 1 / 10000; tpr = 0.99; fpr = 0.01\n"
        "tp = 1_000_000 * prev * tpr; fp = 1_000_000 * (1 - prev) * fpr\n"
        "ppv = tp / (tp + fp)\n"
        "print(f'tp_per_1m={round(tp)}')\nprint(f'fp_per_1m={round(fp)}')\n"
        "print(f'ppv_pct={100 * ppv:.2f}%')\n",
    ),
    (
        "L14", "py", "Chiến lược sao lưu 3-2-1 đòi hỏi >= 3 bản, >= 2 loại phương tiện và >= 1 bản tách rời",
        "# Lab SEC L14 — Kiểm toán quy tắc sao lưu 3-2-1 tự động\n\n"
        "Viết hàm `check_321(copies, media_types, offsite)` đánh giá cấu hình `(2, 1, 0)` (cùng đĩa) so với `(3, 2, 1)` (đĩa + băng + đám mây), in đúng 3 dòng:\n"
        "1. `same_disk_210_ok=0`\n2. `full_321_ok=1`\n3. `missing_in_210=3`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh SEC L14 duong_dan/bai_cua_ban.py\n```",
        "chk = lambda c, m, o: (c >= 3, m >= 2, o >= 1)\n"
        "r_bad = chk(2, 1, 0); r_ok = chk(3, 2, 1)\n"
        "print(f'same_disk_210_ok={int(all(r_bad))}')\n"
        "print(f'full_321_ok={int(all(r_ok))}')\n"
        "print(f'missing_in_210={sum(not x for x in r_bad)}')\n",
    ),
    (
        "L15", "py", "Heartbleed đọc vượt biên 65 536 B vì máy chủ tin độ dài client gửi không kiểm biên",
        "# Lab SEC L15 — Tính biên tràn đọc Heartbleed 2 byte (64 KB) và kiểm chứng kiểm biên\n\n"
        "Viết chương trình Python mô phỏng khung Heartbeat có tải thực `5 B` nhưng trường độ dài 16 bit báo `65 535 B`: "
        "tính số byte rò rỉ bộ nhớ nếu không kiểm biên và viết hàm `safe_heartbeat(claimed, actual)` chặn lỗi này, in đúng 3 dòng:\n"
        "1. `max_u16_bytes=65536`\n2. `leaked_bytes=65530`\n3. `safe_check_rejected=1`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh SEC L15 duong_dan/bai_cua_ban.py\n```",
        "def safe_hb(claimed, actual): return claimed <= actual and claimed >= 0\n"
        "print(f'max_u16_bytes={2 ** 16}')\n"
        "print(f'leaked_bytes={65535 - 5}')\n"
        "print(f'safe_check_rejected={int(not safe_hb(65535, 5))}')\n",
    ),
]

for lid, ext, hint, de_md, sol in LESSONS:
    cov = [(1, "stage1" if lid == "L15" else "example"), (2, "check"), (3, "practice")]
    fp, lo = up.apply_upgrade("SEC", lid, de_md=de_md, ext=ext, sol_code=sol, de_hint=hint, covers=cov)
    print(f"OK SEC {lid}: {fp.name} ({len(lo.splitlines())} dòng)")

led_p, nblk = up.sync_course_ledger("SEC", default_lang="python")
print(f"Synced {led_p.relative_to(ROOT)}: {nblk} blocks")
tpl = subprocess.run([ak.VENV_PY, "-B", "audit/review/sync_tpl_from_lesson.py", "sec", "--write"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
print("sync_tpl SEC:", tpl.stdout.strip() or tpl.stderr.strip())
