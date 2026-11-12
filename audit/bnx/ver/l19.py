"""Kiểm độc lập BNX L19 (Redis nâng cao). Đường khác với tools/checklib_bnx/l19.py:
- CRC16 tính TỪNG BIT bằng phép chia đa thức trên số nguyên lớn (không tra bảng); thẻ băm tách bằng biểu thức chính quy;
- REDIS THẬT (Docker, ảnh chính thức redis:8.10.3, container bnx-l19-redis do tệp này dựng rồi gỡ): chạy NGUYÊN VĂN các khối bash trên
  màn hình (hằng ở audit/bnx/src/l19.py) và so đầu ra; hỏi CLUSTER KEYSLOT cho vài trăm khoá; đọc dải khe từ CLUSTER NODES;
- thời gian: giây 30 / giây 61 của hạn 60 giây KHÔNG chờ thật; kiểm bằng (a) dòng thời gian từng giây tự dựng, (b) Redis thật với hạn
  thu nhỏ 2 giây (gửi ở giây 0, 1, 3) và PTTL thật của SET … EX 60 / EX 240 / EX 300 nằm trong (hạn − 1 giây, hạn].
Thiếu Docker hoặc ảnh → SKIP (cổng FAIL, NOT_VERIFIED), không PASS lặng lẽ."""
import random
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "audit" / "bnx"))
sys.path.insert(0, str(ROOT / "audit" / "bnx" / "src"))
import checklib as alg  # noqa: E402
import l19 as src  # noqa: E402

L, NAME, IMAGE = "L19", "bnx-l19-redis", "redis:8.10.3"
DIGEST = "sha256:1f88291b4c57bdf249f02eb085a8669889b2d2954e91d4de5118a5da6b78dd53"
DEFS = 'D="docker exec -i bnx-l19-redis"\nr() { $D redis-cli --no-raw -p 7000 "$@"; }\n'
BLOCKS = ("PY_CRC", "SH_START", "SH_SLOT", "SH_LOCK", "SH_DEDUP", "PY_SIM", "SH_SHORT", "SH_MULTI")


def crc16_bits(data):
    """Chia đa thức: thông điệp (thêm 16 bit 0) chia cho x^16 + x^12 + x^5 + 1, lấy dư."""
    n = int.from_bytes(data, "big") << 16 if data else 0
    poly = 0x11021
    for i in range(n.bit_length() - 1, 15, -1):
        if n >> i & 1:
            n ^= poly << (i - 16)
    return n


def slot(key):
    m = None
    # quy tắc đặc tả: xét dấu { ĐẦU TIÊN và dấu } đầu tiên bên phải nó; giữa hai dấu phải có ≥ 1 ký tự
    if "{" in key:
        s = key.index("{")
        e = key.find("}", s + 1)
        m = key[s + 1:e] if e > s + 1 else None
    return crc16_bits((m if m else key).encode()) % 16384


def timeline(times, ttl, horizon=400):
    """Dòng thời gian từng giây: alive[t] = mục còn sống ở giây t."""
    alive, out = [False] * (horizon + ttl + 1), []
    for t in times:
        if alive[t]:
            out.append(None)
        else:
            for u in range(t, t + ttl):
                alive[u] = True
            out.append("OK")
    return out


def sh(script, timeout=240):
    bash = shutil.which("bash")
    with tempfile.TemporaryDirectory() as d:
        Path(d, "k.sh").write_text(script, encoding="utf-8", newline="\n")
        p = subprocess.run([bash, "k.sh"], cwd=d, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    return p.returncode, p.stdout.replace("\r\n", "\n"), p.stderr


def cli(lines, port=7000, cluster=True, timeout=120):
    args = ["docker", "exec", "-i", NAME, "redis-cli", "--no-raw", "-p", str(port)] + (["-c"] if cluster else [])
    p = subprocess.run(args, input="\n".join(lines) + "\n", capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    return [x for x in p.stdout.replace("\r\n", "\n").split("\n") if x and not x.startswith("-> Redirected")]


def flush():
    for p in (7000, 7001, 7002):
        cli(["FLUSHALL"], port=p, cluster=False)


def run_py(code):
    p = subprocess.run([sys.executable, "-I", "-X", "utf8", "-B", "-c", code], capture_output=True, text=True, encoding="utf-8")
    return p.returncode, p.stdout


def same(screen, actual):
    return screen.strip("\n").split("\n") == actual.strip("\n").split("\n")


def redis_real(rec):
    if not shutil.which("docker") or not shutil.which("bash"):
        rec(L, None, "thiếu docker hoặc bash: không chạy được Redis thật (NOT_VERIFIED)")
        return
    insp = subprocess.run(["docker", "image", "inspect", IMAGE, "--format", "{{json .RepoDigests}}"], capture_output=True, text=True)
    if insp.returncode != 0:
        rec(L, None, f"chưa có ảnh {IMAGE} (docker pull {IMAGE}): NOT_VERIFIED")
        return
    rec(L, DIGEST in insp.stdout, f"ảnh {IMAGE} đúng mã băm ghi ở audit/bnx/deps/l19/README.md ({DIGEST[:19]}…)")
    try:
        rc, so, se = sh(src.SH_START.strip("\n") + "\n")
        if rc != 0 or "covered" not in so:
            rec(L, None, "không dựng được cụm Redis: " + (se or so).strip()[-160:])
            return
        ver = cli(["INFO server"], cluster=False)
        rec(L, same(src.OUT_START, so) and "redis_version:8.10.3" in ver,
            "khối dựng cụm chạy nguyên văn: redis-cli thật chia 0–5460, 5461–10922, 10923–16383, đủ 16384 khe; máy chủ báo redis_version:8.10.3")
        # dải khe đọc từ CLUSTER NODES (đường khác với dòng in của công cụ tạo cụm)
        nodes = {}
        for ln in cli(["CLUSTER NODES"], cluster=False):
            f = ln.split()
            if len(f) >= 9 and "-" in f[8]:
                a, b = f[8].split("-")
                nodes[int(f[1].split(":")[1].split("@")[0])] = (int(a), int(b))
        real = [nodes.get(p) for p in (7000, 7001, 7002)]
        rec(L, real == alg.bnx_l19_ranges() == [(0, 5460), (5461, 10922), (10923, 16383)] and sum(b - a + 1 for a, b in real) == 16384,
            f"CLUSTER NODES thật: cổng 7000/7001/7002 giữ {real} = alg.bnx_l19_ranges(); cộng lại 16384 khe")
        # CLUSTER KEYSLOT thật cho nhiều khoá, có thẻ băm và ca biên của đặc tả
        rnd = random.Random(19)
        keys = ["foo", "hello", "123456789", "dedup:TX1001", "dedup:TX2002", "loan:disb:A1001", "loan:disb:{A1001}", "A1001", "bl:jti-7f3a",
                "bl:jti-0000", "acc:1", "acc:2", "{acc}:1", "{acc}:2", "acc", "{user1000}.following", "{user1000}.followers", "user1000",
                "foo{}{bar}", "foo{{bar}}zap", "foo{bar}{zap}", "{}x", "a{b", "a}b{c}"]
        abc = "abcdefghijklmnopqrstuvwxyz0123456789:-_."
        for _ in range(300):
            k = "".join(rnd.choice(abc) for _ in range(rnd.randint(1, 24)))
            if rnd.random() < 0.3:
                i = rnd.randint(0, len(k))
                k = k[:i] + "{" + "".join(rnd.choice(abc) for _ in range(rnd.randint(0, 5))) + "}" + k[i:]
            keys.append(k)
        got = [int(x.split()[-1]) for x in cli([f"CLUSTER KEYSLOT {k}" for k in keys], cluster=False)]
        mine, lib = [slot(k) for k in keys], [alg.bnx_l19_slot(k) for k in keys]
        bad = [k for k, g, m_, l_ in zip(keys, got, mine, lib) if not g == m_ == l_]
        rec(L, len(got) == len(keys) and not bad, f"CLUSTER KEYSLOT thật = CRC từng bit = alg.bnx_l19_slot cho {len(keys)} khoá (có thẻ băm, ca biên đặc tả); lệch: {bad[:3]}")
        d = dict(zip(keys, got))
        rec(L, (d["foo"], d["hello"], d["dedup:TX1001"], d["bl:jti-0000"], d["acc:1"], d["acc:2"], d["{acc}:1"], d["loan:disb:A1001"],
                d["loan:disb:{A1001}"]) == (12182, 866, 9306, 1074, 16276, 4087, 12007, 5075, 1830) and d["{acc}:1"] == d["{acc}:2"] == d["acc"]
            and d["loan:disb:{A1001}"] == d["A1001"],
            "số khe trên màn hình đúng với Redis thật: foo 12182, hello 866, dedup:TX1001 9306, bl:jti-0000 1074, acc:1 16276, acc:2 4087, "
            "{acc}:1 12007, loan:disb:A1001 5075, loan:disb:{A1001} 1830 (= khe của A1001)")
        moved = cli(["SET foo bar", "SET hello x", "SET dedup:TX1001 1"], cluster=False)
        rec(L, moved == ["(error) MOVED 12182 127.0.0.1:7002", "OK", "(error) MOVED 9306 127.0.0.1:7001"]
            and (alg.bnx_l19_node_of_key("foo"), alg.bnx_l19_node_of_key("hello"), alg.bnx_l19_node_of_key("dedup:TX1001")) == (3, 1, 2),
            "nút 7000 thật: foo → MOVED sang 7002 (nút 3), hello nhận tại chỗ (nút 1), dedup:TX1001 → MOVED sang 7001 (nút 2) = alg.bnx_l19_node_of_key")
        # các khối bash trên màn hình, nguyên văn
        for name in ("SLOT", "LOCK", "DEDUP", "SHORT", "MULTI"):
            flush()
            rc, so, se = sh(DEFS + getattr(src, "SH_" + name).strip("\n") + "\n")
            rec(L, rc == 0 and same(getattr(src, "OUT_" + name), so), f"khối SH_{name} chạy nguyên văn trên Redis thật: đầu ra = hằng OUT_{name} trên màn hình")
        # hạn thật: PTTL ngay sau SET nằm trong (hạn − 1 s, hạn]; TTL −2 / −1; hạn thu nhỏ 2 giây
        flush()
        o = cli(["SET loan:disb:A1001 may-a NX EX 300", "PTTL loan:disb:A1001", "SET dedup:TX1001 1 NX EX 60", "PTTL dedup:TX1001",
                 "SET bl:jti-7f3a 1 EX 240", "PTTL bl:jti-7f3a", "TTL khong-co", "SET vinh-vien 1", "TTL vinh-vien"])
        pt = [int(o[i].split()[-1]) for i in (1, 3, 5)]
        rec(L, all(h * 1000 - 1000 < p <= h * 1000 for p, h in zip(pt, (300, 60, 240))) and o[6] == "(integer) -2" and o[8] == "(integer) -1",
            f"PTTL thật ngay sau SET EX 300 / 60 / 240: {pt} mili giây; TTL khoá không tồn tại −2, khoá không hạn −1")
        p = subprocess.run(["docker", "exec", NAME, "sh", "-c",
                            'c="redis-cli --no-raw -c -p 7000 SET dedup:VER 1 NX EX 2"; $c; sleep 1; $c; sleep 2; $c'],
                           capture_output=True, text=True, timeout=60)
        real3 = [None if x == "(nil)" else x for x in p.stdout.split()]
        rec(L, real3 == ["OK", None, "OK"] == alg.bnx_l19_set_nx_ex([0, 1, 3], 2) == timeline([0, 1, 3], 2),
            "Redis thật, hạn thu nhỏ 2 giây, gửi ở giây 0, 1, 3: OK, (nil), OK = alg.bnx_l19_set_nx_ex = dòng thời gian tự dựng "
            "(đây là cách kiểm “giây 30 từ chối, giây 61 nhận” mà không chờ 61 giây thật)")
        # nhả khoá: DELEX IFEQ và đoạn kịch bản của tài liệu cho cùng kết quả; DEL thẳng xoá cả khoá của máy khác
        flush()
        lua = "\"if redis.call('get',KEYS[1]) == ARGV[1] then return redis.call('del',KEYS[1]) else return 0 end\""
        o = cli(["SET k1 may-b NX EX 300", f"EVAL {lua} 1 k1 may-a", "DELEX k1 IFEQ may-a", "EXISTS k1", f"EVAL {lua} 1 k1 may-b", "EXISTS k1",
                 "SET k1 may-b NX EX 300", "DEL k1", "EXISTS k1"])
        rec(L, o == ["OK", "(integer) 0", "(integer) 0", "(integer) 1", "(integer) 1", "(integer) 0", "OK", "(integer) 1", "(integer) 0"]
            and alg.bnx_l19_lock_story(300, 320) == (2, 0) and alg.bnx_l19_lock_story(300, 320, owner_check=False) == (2, 1),
            "nhả khoá trên Redis thật: sai mã chủ khoá → 0 (cả DELEX IFEQ và đoạn kịch bản so-rồi-xoá), đúng mã → 1; DEL thẳng xoá khoá của máy khác (lỗi 1)")
    finally:
        subprocess.run(["docker", "rm", "-f", NAME], capture_output=True)


def run(rec):
    # (1) CRC16 và khe: chia đa thức từng bit so với bảng tra của checklib
    rec(L, crc16_bits(b"123456789") == 0x31C3 == alg.bnx_l19_crc16("123456789"),
        "CRC16 XMODEM của \"123456789\" = 31C3 (véc-tơ thử của Redis cluster specification), chia đa thức từng bit = bảng tra")
    rnd = random.Random(1)
    blobs = [bytes(rnd.randrange(256) for _ in range(rnd.randint(0, 40))) for _ in range(500)]
    rec(L, all(crc16_bits(b) == alg.bnx_l19_crc16(b) for b in blobs), "CRC16 từng bit = alg.bnx_l19_crc16 trên 500 chuỗi byte ngẫu nhiên")
    rec(L, crc16_bits(b"foo") == 44950 == alg.bnx_l19_crc16("foo") and 44950 - 2 * 16384 == 12182 == slot("foo") == alg.bnx_l19_slot("foo")
        and crc16_bits(b"hello") == 50018 and 50018 - 3 * 16384 == 866 == slot("hello"),
        "① CRC16(foo) = 44950, mod 16384 = 12182; câu 1: CRC16(hello) = 50018, mod 16384 = 866")
    # (2) chia khe: mỗi khe đúng một nút, đếm bằng vòng lặp
    owner = [alg.bnx_l19_node(s) for s in range(16384)]
    cnt = [owner.count(i) for i in (1, 2, 3)]
    rec(L, cnt == [5461, 5462, 5461] and sum(cnt) == 16384 == 3 * 5461 + 1 and owner == sorted(owner) and owner[12182] == 3 and owner[866] == 1
        and owner[9306] == 2 and (owner[5460], owner[5461], owner[10922], owner[10923]) == (1, 2, 2, 3),
        "② đếm 16384 khe: nút 1/2/3 giữ 5461/5462/5461 khe, biên 5460|5461 và 10922|10923; khe 12182 → nút 3, 866 → nút 1, 9306 → nút 2")
    # (3) thẻ băm theo các ví dụ của đặc tả
    rec(L, slot("{user1000}.following") == slot("{user1000}.followers") == slot("user1000") and slot("foo{}{bar}") == crc16_bits(b"foo{}{bar}") % 16384
        and slot("foo{{bar}}zap") == crc16_bits(b"{bar") % 16384 and slot("foo{bar}{zap}") == slot("bar")
        and all(slot(k) == alg.bnx_l19_slot(k) for k in ("{user1000}.following", "foo{}{bar}", "foo{{bar}}zap", "foo{bar}{zap}", "{acc}:1"))
        and alg.bnx_l19_hashed_part("loan:disb:{A1001}") == "A1001",
        "thẻ băm đúng bốn ví dụ của Redis cluster specification ({user1000}…, foo{}{bar}, foo{{bar}}zap, foo{bar}{zap})")
    # (4) hạn sống: dòng thời gian từng giây so với checklib
    cases = [([0, 30, 61, 62], 60), ([0, 30], 60), ([0, 45], 60), ([0, 75], 60), ([0, 90], 60), ([0, 90], 120), ([0, 59, 60], 60), ([0, 100], 300),
             ([0, 30], 120), ([0, 1, 3], 2)]
    rec(L, all(timeline(t, h) == alg.bnx_l19_set_nx_ex(t, h) for t, h in cases)
        and timeline([0, 30, 61, 62], 60) == ["OK", None, "OK", None] and timeline([0, 45], 60)[1] is None and timeline([0, 75], 60)[1] == "OK",
        "④ hạn 60 giây: giây 30 từ chối, giây 61 nhận, giây 62 từ chối (khoảng mới); câu 2: giây 45 từ chối, giây 75 nhận — dòng thời gian = alg")
    rec(L, timeline([0, 90], 60).count("OK") == 2 == alg.bnx_l19_processed([0, 90], 60) and timeline([0, 90], 120).count("OK") == 1
        == alg.bnx_l19_processed([0, 90], 120), "lỗi 4: hạn 60 mà thử lại ở giây 90 → xử lý 2 lần; hạn 120 → 1 lần")
    rec(L, (300 - 60, 900 - 250, 300 - 120, 320 - 300) == (alg.bnx_l19_bl_ttl(300, 60), alg.bnx_l19_bl_ttl(900, 250), 180, alg.bnx_l19_overrun(300, 320))
        == (240, 650, 180, 20) and alg.bnx_l19_bl_ttl(300, 400) == 0,
        "⑤ danh sách đen: 300 − 60 = 240 giây; câu 2: 900 − 250 = 650; ③ 300 − 120 = 180; lỗi 3: 320 − 300 = 20")
    # khoá: mô phỏng sự kiện (A dừng, B xin khoá mỗi giây)
    def story(ttl, pause, owner_check):
        val, exp, work = "A", ttl, {"A"}
        for t in range(1, pause + 1):
            if t >= exp:
                val = None
            if val is None:
                val, exp = "B", t + ttl
                work.add("B")
        if owner_check:
            rel = 1 if val == "A" else 0
        else:
            rel = 1 if val else 0
        return len(work), rel
    rec(L, all(story(t, p, o) == alg.bnx_l19_lock_story(t, p, owner_check=o) for t, p, o in
               ((300, 320, True), (300, 320, False), (300, 120, True), (300, 301, True), (300, 299, False), (300, 300, True))),
        "khoá hạn 300: dừng tới giây 320 → hai máy cùng làm; có mã chủ khoá thì A không xoá được khoá của B, DEL thẳng thì xoá mất (mô phỏng từng giây = alg)")
    # (5) khối Python trên màn hình
    for name in ("CRC", "SIM"):
        rc, so = run_py(getattr(src, "PY_" + name))
        rec(L, rc == 0 and same(getattr(src, "OUT_" + name), so), f"khối PY_{name} chạy thật: đầu ra = hằng OUT_{name} trên màn hình")
    lines = [l for n in BLOCKS for l in getattr(src, n).strip("\n").split("\n")]
    rec(L, max(map(len, lines)) <= 70 and all(len(getattr(src, n).strip("\n").split("\n")) <= 12 for n in BLOCKS),
        f"khối mã ≤ 12 dòng, dòng dài nhất {max(map(len, lines))} ký tự (≤ 70)")
    # (6) Redis thật
    redis_real(rec)
    # (7) bài sinh ra khớp giáo án
    cur = next(x for x in yaml.safe_load((ROOT / "curriculum" / "bnx.yaml").read_text(encoding="utf-8"))["lessons"] if x["id"] == L)
    spec = yaml.safe_load(next((ROOT / "lessons" / "bnx").glob(f"{L}_*.yaml")).read_text(encoding="utf-8"))
    shows = " ".join(s_["show"] for sc_ in spec["scenes"] for s_ in sc_["steps"])
    rec(L, spec["title"] == "Bài 19 — " + cur["title"] and spec["objectives"] == cur["objectives"], "tiêu đề và mục tiêu chép nguyên văn giáo án")
    need = ("16384", "12182", "0–5460", "5461–10922", "10923–16383", "nút thứ ba", "giây 30", "giây 61", "hạn 60", "240")
    rec(L, all(x in shows for x in need) and "EX 60" in shows and "EX 240" in shows and "EX 300" in shows,
        "mọi con số của ví dụ giáo án có trên màn hình: 16384, 12182, ba dải khe, nút thứ ba, hạn 60 giây, giây 30, giây 61, 240 giây")
    kinds = [sc_["kind"] for sc_ in spec["scenes"]]
    rec(L, kinds == ["hook", "prereq", "symbol", "intuition", "formula", "example", "check", "pitfall", "quiz", "recap"]
        and "Nếu bị hỏi về dòng này trên CV" in shows, "đủ 10 cảnh đúng thứ tự; có bảng “Nếu bị hỏi về dòng này trên CV”")
