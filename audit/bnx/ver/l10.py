"""Kiểm độc lập BNX L10 bằng đường KHÁC checklib: (1) chạy nguyên văn các khối Python trên màn hình; (2) nén bằng cách nhóm theo khoá
rồi lấy offset lớn nhất, khớp mẫu sàn bằng biểu thức chính quy dịch từ mẫu, kiểm lược đồ bằng mô phỏng phân giải bản ghi Avro;
(3) CHẠY KAFKA THẬT (Docker, apache/kafka:3.9.0, container bnx-kafka): chủ đề cleanup.policy=compact — đọc ngay sau khi ghi thấy
đủ 9 bản ghi (đoạn đang ghi không nén), sau khi cuộn đoạn và bộ dọn chạy thì còn đúng KAFKA_OUT. Container do tệp này tạo thì tự dừng."""
import json
import re
import shlex
import shutil
import subprocess
import sys
import time
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "audit" / "bnx" / "src"))
sys.path.insert(0, str(ROOT / "audit" / "bnx"))
sys.path.insert(0, str(ROOT / "tools"))
import checklib as alg  # noqa: E402
import l10  # noqa: E402

NAME, IMAGE, K = "bnx-kafka", "apache/kafka:3.9.0", "/opt/kafka/bin/"
BS = ["--bootstrap-server", "localhost:9092"]


def cmd_tokens(text, script):
    """Tách lệnh HIỂN THỊ trên màn hình (hằng KAFKA_*_CMD của bài): trả (đối số trước script, đối số sau script) của dòng có `script`."""
    joined = text.replace("\\\n", " ")
    line = next(l for l in joined.split("\n") if script in l)
    toks = shlex.split(line)
    i = next(k for k, t in enumerate(toks) if t.endswith(script))
    return toks[:i], toks[i + 1:]


def with_topic(args, topic):
    """Thay tên chủ đề sau --topic bằng tên chủ đề duy nhất của lần kiểm."""
    out = list(args)
    out[out.index("--topic") + 1] = topic
    return out


def run_py(code):
    p = subprocess.run([sys.executable, "-X", "utf8", "-I", "-c", code], capture_output=True, text=True, encoding="utf-8")
    return p.returncode, p.stdout


def dk(*args, inp=None, timeout=120):
    p = subprocess.run(["docker", "exec", "-i", NAME, *args], input=inp, capture_output=True, text=True, encoding="utf-8",
                       errors="replace", timeout=timeout)
    return p.returncode, p.stdout, p.stderr


def compact_group(log, keep_tombstone):
    groups = {}
    for off, (k, v) in enumerate(log):
        groups.setdefault(k, []).append(off)
    out = []
    for k, offs in groups.items():
        off = max(offs)
        if log[off][1] is not None or keep_tombstone:
            out.append((off, k, log[off][1]))
    return sorted(out)


def topic_regex(pattern):
    rx = ""
    for w in pattern.split("."):
        rx += {"*": r"\.[^.]+", "#": r"(?:\.[^.]+)*"}.get(w, r"\." + re.escape(w))
    return re.compile(rx)


def rmatch(pattern, key):
    return topic_regex(pattern).fullmatch("." + key) is not None


def avro_read(reader_fields, old_record):
    """Mô phỏng phân giải: mỗi trường của lược đồ bên đọc lấy từ bản ghi cũ, không có thì dùng mặc định, không mặc định thì lỗi."""
    out = {}
    for f in reader_fields:
        if f["name"] in old_record:
            out[f["name"]] = old_record[f["name"]]
        elif "default" in f:
            out[f["name"]] = f["default"]
        else:
            raise ValueError("thiếu trường " + f["name"])
    return out


def kafka_lines(topic):
    _, cargs = cmd_tokens(l10.KAFKA_CONSUME_CMD, "kafka-console-consumer.sh")   # lệnh hiển thị trên màn hình
    rc, so, _ = dk(K + "kafka-console-consumer.sh", *with_topic(cargs, topic))
    return [l for l in so.strip().split("\n") if l.startswith("Offset:")]


def kafka_real(rec, L):
    if not shutil.which("docker"):
        rec(L, None, "không có docker: không chạy được Kafka thật")
        return
    st = subprocess.run(["docker", "inspect", "-f", "{{.State.Running}}", NAME], capture_output=True, text=True)
    started = False
    if st.stdout.strip() != "true":
        subprocess.run(["docker", "rm", "-f", NAME], capture_output=True)
        r = subprocess.run(["docker", "run", "-d", "--name", NAME, IMAGE], capture_output=True, text=True)
        if r.returncode != 0:
            rec(L, None, "không khởi động được container Kafka: " + r.stderr.strip()[:120])
            return
        started = True
    try:
        for _ in range(60):
            if dk(K + "kafka-topics.sh", *BS, "--list", timeout=60)[0] == 0:
                break
            time.sleep(2)
        topic = f"bnx-l10-ver-{int(time.time())}"
        # lệnh HIỂN THỊ trên màn hình: tạo chủ đề, ghi bản ghi (các cờ lấy từ chính hằng KAFKA_*_CMD, chỉ đổi tên chủ đề thành tên duy nhất)
        pre, targs = cmd_tokens(l10.KAFKA_TOPIC_CMD, "kafka-topics.sh")
        rc, _, er = dk(K + "kafka-topics.sh", *with_topic(targs, topic))
        if rc != 0:
            rec(L, False, "tạo chủ đề nén thất bại: " + er.strip()[:160])
            return
        cfg = dk(K + "kafka-configs.sh", *BS, "--entity-type", "topics", "--entity-name", topic, "--describe")[1]
        ppre, pargs = cmd_tokens(l10.KAFKA_PRODUCE_CMD, "kafka-console-producer.sh")
        records = ppre[ppre.index("printf") + 2:ppre.index("|")]
        dk(K + "kafka-console-producer.sh", *with_topic(pargs, topic), inp="\n".join(records) + "\n")
        first = kafka_lines(topic)
        want_first = [f"Offset:{i}\t{k}\t{v}" for i, (k, v) in enumerate(x.split(":") for x in records)]
        want_first[-1] = "Offset:8\tC\tTOMBSTONE"
        rec(L, "cleanup.policy=compact" in cfg and first == want_first,
            f"Kafka 3.9.0 thật: chủ đề cleanup.policy=compact; đọc ngay sau khi ghi thấy đủ {len(first)}/9 bản ghi, offset 0..8 (đoạn đang ghi chưa nén)")
        time.sleep(2.5)  # > segment.ms: lần ghi sau cuộn đoạn
        dk(K + "kafka-console-producer.sh", *with_topic(pargs, topic), inp="Z:1\n")
        want = l10.KAFKA_OUT.strip().split("\n")
        seen, t0 = [], time.time()
        while time.time() - t0 < 150:
            seen = kafka_lines(topic)
            if seen == want:
                break
            time.sleep(5)
        rec(L, seen == want, f"Kafka 3.9.0 thật sau khi cuộn đoạn và bộ dọn chạy ({time.time() - t0:.0f} s): {seen} = KAFKA_OUT trên màn hình")
        rec(L, [tuple(x.split("\t")) for x in seen] == [(f"Offset:{o}", k, "TOMBSTONE" if v is None else str(v)) for o, k, v in
                alg.bnx_compact(l10_log() + [("C", None), ("Z", 1)], drop_tombstones=False)],
            "kết quả Kafka thật = alg.bnx_compact(…, giữ bia mộ) — offset 5, 7, 8, 9")
        dk(K + "kafka-topics.sh", *BS, "--delete", "--topic", topic)
    finally:
        if started:
            subprocess.run(["docker", "rm", "-f", NAME], capture_output=True)


def l10_log():
    return alg.bnx_l10_log()


def run(rec):
    L = "L10"
    # (1) mã trên màn hình chạy thật
    for name in ("COMPACT", "SCHEMA", "TOPIC", "CHECK"):
        rc, so = run_py(getattr(l10, name + "_PY"))
        rec(L, rc == 0 and so.strip() == getattr(l10, name + "_OUT").strip(), f"khối {name}_PY chạy rc={rc}, đầu ra thật = hằng {name}_OUT trên màn hình")

    # (2a) nén: nhóm theo khoá, lấy offset lớn nhất
    log = l10_log()
    rec(L, len(log) == 8 and len({k for k, _ in log}) == 3 and compact_group(log, False) == alg.bnx_compact(log)
        == [(5, "A", 120), (6, "C", 75), (7, "B", 260)], "8 bản ghi 3 khoá → 3 (A@5, C@6, B@7), nhóm theo khoá = alg.bnx_compact")
    t = log + [("C", None)]
    rec(L, len(compact_group(t, True)) == 3 == len(alg.bnx_compact(t, drop_tombstones=False))
        and compact_group(t, False) == alg.bnx_compact(t) == [(5, "A", 120), (7, "B", 260)],
        "thêm bia mộ C: ngay sau nén 3 (A, B, bia mộ C); sau delete.retention.ms còn 2 (A, B)")
    q = [("X", 1), ("Y", 5), ("X", 2), ("Z", 7), ("Y", 6), ("X", 3), ("Y", None)]
    rec(L, compact_group(q, True) == alg.bnx_compact(q, drop_tombstones=False) == [(3, "Z", 7), (5, "X", 3), (6, "Y", None)]
        and len(compact_group(q, False)) == 2, "đố câu 1: 3 rồi 2")
    rec(L, 86400000 // 1000 // 3600 == 24 == alg.bnx_ms_to_hours(86400000) and 604800000 // 1000 // 86400 == 7,
        "delete.retention.ms mặc định 86 400 000 ms = 24 giờ; retention.ms 604 800 000 ms = 7 ngày (nguồn [KC2])")

    # (2b) sàn chủ đề: biểu thức chính quy dịch từ mẫu
    tut = {"quick.orange.rabbit": ["Q1", "Q2"], "lazy.orange.elephant": ["Q1", "Q2"], "quick.orange.fox": ["Q1"], "lazy.brown.fox": ["Q2"],
           "lazy.pink.rabbit": ["Q2"], "quick.brown.fox": [], "orange": [], "quick.orange.new.rabbit": [], "lazy.orange.new.rabbit": ["Q2"]}
    bind = [("Q1", "*.orange.*"), ("Q2", "*.*.rabbit"), ("Q2", "lazy.#")]
    rec(L, all(sorted({qq for qq, p in bind if rmatch(p, k)}) == w == sorted(set(alg.bnx_route(bind, k))) for k, w in tut.items()),
        "9 ví dụ RabbitMQ tutorial 5: regex và alg.bnx_route cùng cho đúng hàng đợi như hướng dẫn")
    pats = ("payment.*.napas", "payment.#", "payment.*")
    rec(L, [rmatch(p, "payment.vn.napas") for p in pats] == [True, True, False]
        == [alg.bnx_topic_match(p, "payment.vn.napas") for p in pats], "payment.vn.napas khớp payment.*.napas, payment.#, không khớp payment.*")
    qp = ("payment.*.swift", "payment.#.usd", "*.intl.#")
    rec(L, [rmatch(p, "payment.intl.swift.usd") for p in qp] == [False, True, True]
        == [alg.bnx_topic_match(p, "payment.intl.swift.usd") for p in qp] and rmatch("payment.#", "payment"),
        "đố câu 2: không, có, có; payment.# khớp cả 'payment' (# = không từ)")

    # (2c) lược đồ: phân giải bản ghi cũ bằng lược đồ mới
    s2 = json.loads(l10.SCHEMA_JSON)
    v2 = {f["name"]: "default" in f for f in s2["fields"]}
    old = {"account": "TK-1001", "amount": 500000}
    try:
        r2 = avro_read(s2["fields"], old)
        ok2 = r2["channel"] == "APP"
    except ValueError:
        ok2 = False
    s3 = [{"name": "account"}, {"name": "amount"}, {"name": "fee"}]
    try:
        avro_read(s3, old)
        ok3 = True
    except ValueError:
        ok3 = False
    rec(L, s2["type"] == "record" and v2 == {"account": False, "amount": False, "channel": True} and ok2 and not ok3
        and alg.bnx_backward_ok(v2, {"account": False, "amount": False}) == (True, [])
        and alg.bnx_backward_ok({"account": False, "amount": False, "fee": False}, {"account": False, "amount": False}) == (False, ["fee"]),
        "lược đồ Avro v2 đọc được bản ghi cũ (channel = APP mặc định); v3 thêm fee không mặc định thì không đọc được")

    # (2d) WP4: cảnh quy mô — chạy lại không đệm mọi chương trình; hàm match hiển thị đối chiếu 9 ví dụ RabbitMQ; đếm lại nén bằng đường khác
    import lib2
    lib2.verify_programs(rec, L)
    ns = {}
    exec(l10.TOPIC_PY.split("for pat in")[0], ns)
    rec(L, all(sorted({qq for qq, p in bind if ns["match"](p, k)}) == w for k, w in tut.items()),
        "hàm match HIỂN THỊ trên màn hình (TOPIC_PY) khớp đủ 9 ví dụ của RabbitMQ tutorial 5")
    for n_, line in zip((1000, 100000, 1000000), l10.P_SCALE.out.splitlines()[2:]):
        ks = {}
        for i in range(n_):
            ks["TK%d" % (i % 100)] = i
        rec(L, line.split()[-1] == str(len(ks)) == "100" == str(alg.bnx_l10_compacted(n_, 100)) and line.split()[8] == str(n_),
            f"{n_} bản ghi, 100 tài khoản: sau nén còn {len(ks)} (nhóm theo khoá), đọc lại không nén {n_}")
    rec(L, [alg.bnx_l10_read_ms(n_, 0.001) for n_ in (1000, 100000, 1000000)] == [1.0, 100.0, 1000.0] and alg.bnx_l10_read_ms(100, 0.001) == 0.1,
        "1 µs mỗi bản ghi (số minh hoạ): 1 ms, 100 ms, 1 s so với 0,1 ms")
    lab = ROOT / "labs" / "BNX" / "L10"
    p_ = subprocess.run([sys.executable, "-X", "utf8", "-I", str(lab / "loi_giai.py")], capture_output=True, text=True, encoding="utf-8")
    lg = [("M", 10), ("N", 20), ("M", 15), ("P", 5), ("N", None), ("M", 12), ("Q", 7), ("P", 9)]
    cg = compact_group(lg, True)
    fmt = lambda ds: " ".join(f"{o}:{k}:{'-' if v is None else v}" for o, k, v in ds)
    want_lab = ["con bia mo: " + fmt(cg), "het han bia mo: " + fmt(compact_group(lg, False))]
    want_lab += [f"payment.eu.sepa.eur voi {m}: " + ("co" if rmatch(m, "payment.eu.sepa.eur") else "khong") for m in ("payment.*.sepa", "payment.#.eur", "*.eu.#")]
    rec(L, p_.returncode == 0 and p_.stdout.strip().split("\n") == want_lab == (lab / "mong_doi.txt").read_text(encoding="utf-8").strip().split("\n"),
        "lab L10: loi_giai.py = mong_doi.txt = tính lại bằng nhóm theo khoá + regex dịch từ mẫu")

    # (3) Kafka thật — lệnh hiển thị trên màn hình
    cmds = (l10.KAFKA_TOPIC_CMD, l10.KAFKA_PRODUCE_CMD, l10.KAFKA_CONSUME_CMD)
    rec(L, l10.KAFKA_TOPIC_CMD.split("\n")[0].split() == ["docker", "run", "-d", "--name", NAME, IMAGE]
        and all(len(c.split("\n")) <= 12 and all(len(x) <= 70 for x in c.split("\n")) for c in cmds),
        "lệnh dựng Kafka hiển thị = ảnh/container của ver (apache/kafka:3.9.0, bnx-kafka); mỗi khối lệnh ≤ 12 dòng, dòng ≤ 70 ký tự")
    kafka_real(rec, L)

    # (4) bài sinh ra
    cur = next(x for x in yaml.safe_load((ROOT / "curriculum" / "bnx.yaml").read_text(encoding="utf-8"))["lessons"] if x["id"] == L)
    spec = yaml.safe_load(next((ROOT / "lessons" / "bnx").glob(f"{L}_*.yaml")).read_text(encoding="utf-8"))
    shows = " ".join(s_["show"] for sc_ in spec["scenes"] for s_ in sc_["steps"])
    rec(L, spec["title"].endswith(cur["title"]) and spec["objectives"] == cur["objectives"], "tiêu đề và mục tiêu chép nguyên văn giáo án")
    rec(L, all(x in shows for x in ("8 \\text{ bản ghi}, 3 \\text{ khoá}", "\\hl{3}", "\\hlg{2}", "payment.vn.napas",
                                     "payment.*.napas", "payment.\\#", "payment.*}")),
        "ví dụ giáo án trên màn hình: 8 bản ghi 3 khoá → 3; bia mộ → 2; payment.vn.napas với payment.*.napas, payment.#, payment.*")
