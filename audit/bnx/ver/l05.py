"""Kiểm độc lập BNX L05 (mTLS) — CHẠY THẬT:
- sinh 2 nơi cấp + chứng chỉ máy chủ/khách bằng openssl 3.5 (chạy NGUYÊN VĂN ba khối bash của audit/bnx/src/l05.py);
- máy chủ TLS Python ssl (CERT_REQUIRED) ở 127.0.0.1 cổng ngẫu nhiên, chạy NGUYÊN VĂN các khối Python, lặp 5 lần;
- đường khác 1: openssl verify (bản OpenSSL khác bản Python dùng) + đọc issuer/notAfter bằng openssl x509, đưa vào alg.bnx_mtls_decision;
- đường khác 2: bắt tay lại với khách bị giới hạn TLS 1.2 (lỗi tới ngay trong bắt tay, không phải ở lần đọc) — máy chủ phải ghi cùng lý do;
- kiểm điều lời giảng nói: thiếu keyUsage ở nơi cấp thì Python 3.13 từ chối; Git Bash đổi “/CN=…” nếu thiếu MSYS_NO_PATHCONV."""
import datetime as dt
import shutil
import socket
import ssl
import subprocess
import sys
import tempfile
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "audit" / "bnx"))
sys.path.insert(0, str(ROOT / "audit" / "bnx" / "src"))
import checklib as alg  # noqa: E402
import l05 as src  # noqa: E402

CASES = [None, "la_mat", "het_han", "thanh_toan"]


def handshake(d, ten, max12=False, allow=None):
    """Bắt tay bằng mã RIÊNG của bộ kiểm (không dùng khối trên màn hình). Trả (lý do máy chủ, kết quả khách)."""
    mc = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    mc.load_cert_chain(str(d / "may_chu.crt"), str(d / "may_chu.key"))
    mc.load_verify_locations(str(d / "ca1.crt"))
    mc.verify_mode = ssl.CERT_REQUIRED
    ls = socket.create_server(("127.0.0.1", 0))
    res, done = {}, threading.Event()

    def srv():
        c, _ = ls.accept()
        t = mc.wrap_socket(c, server_side=True, do_handshake_on_connect=False)
        try:
            t.do_handshake()
            nm = dict(x[0] for x in t.getpeercert()["subject"])["commonName"]
            if allow is not None and nm not in allow:       # cửa ④ của bộ kiểm (mã riêng)
                res["srv"] = "tên không được phép"
                t.sendall(b"no")
            else:
                res["srv"] = "ok:" + nm
                t.sendall(b"ok")
        except ssl.SSLError as e:
            res["srv"] = getattr(e, "verify_message", None) or e.reason
        done.wait(10)
        t.close()

    th = threading.Thread(target=srv)
    th.start()
    kh = ssl.create_default_context(cafile=str(d / "ca1.crt"))
    if max12:
        kh.maximum_version = ssl.TLSVersion.TLSv1_2
    if ten:
        kh.load_cert_chain(str(d / f"{ten}.crt"), str(d / f"{ten}.key"))
    stage = "bắt tay"
    try:
        with socket.create_connection(ls.getsockname()) as s, kh.wrap_socket(s, server_hostname="localhost") as t:
            stage = "đọc"
            res["cli"] = t.recv(2).decode()
    except (ssl.SSLError, OSError) as e:
        res["cli"] = f"lỗi ở {stage}: " + (getattr(e, "reason", None) or type(e).__name__)
    done.set()
    th.join()
    ls.close()
    return res["srv"], res["cli"]


def x509(ossl, f, *what):
    r = subprocess.run([ossl, "x509", "-in", str(f), "-noout", *what], capture_output=True, text=True)
    return r.stdout


def run(rec):
    ossl, bash = shutil.which("openssl"), shutil.which("bash")
    if not ossl or not bash:
        rec("L05", None, "thiếu openssl hoặc bash")
        return
    with tempfile.TemporaryDirectory() as td:
        d = Path(td)
        (d / "gen.sh").write_text("\n".join(x.strip("\n") for x in (src.SH_CA, src.SH_SERVER, src.SH_BAD)) + "\n", encoding="utf-8", newline="\n")
        r = subprocess.run([bash, "gen.sh"], cwd=d, capture_output=True, text=True)
        want_err = [l for l in src.OUT_VERIFY.strip().split("\n")[1:]]
        got_err = [l for l in r.stderr.split("\n") if l.startswith("error ")]
        rec("L05", r.returncode == 2 and r.stdout.strip() == "thanh_toan.crt: OK" and got_err == want_err,
            "ba khối bash chạy nguyên văn: openssl verify OK / lỗi 20 / lỗi 10 đúng như màn hình")
        # chạy NGUYÊN VĂN khối Python, 5 lần
        prog = "\n".join(x.strip("\n") for x in (src.PY_CTX, src.PY_SERVE, src.PY_CLIENT, src.PY_RUN)) + "\n"
        (d / "tls.py").write_text(prog, encoding="utf-8")
        outs = set()
        for _ in range(5):
            p = subprocess.run([sys.executable, "-I", "-X", "utf8", "-B", "tls.py"], cwd=d, capture_output=True, text=True, encoding="utf-8", timeout=60)
            outs.add((p.returncode, p.stdout.replace("\r\n", "\n").strip()))
        rec("L05", outs == {(0, src.OUT_TLS.strip())}, f"khối Python (máy chủ CERT_REQUIRED thật) chạy nguyên văn 5 lần, đầu ra = màn hình ({len(outs)} kiểu đầu ra)")
        # bộ kiểm riêng, TLS 1.3 và TLS 1.2
        r13 = [handshake(d, t) for t in CASES]
        r12 = [handshake(d, t, max12=True) for t in CASES]
        want_srv = [alg.bnx_l05_server_reason["none"], alg.bnx_l05_server_reason["ca"], alg.bnx_l05_server_reason["expired"], "ok:thanh_toan"]
        rec("L05", [a for a, _ in r13] == want_srv, f"bắt tay riêng (TLS 1.3): máy chủ ghi {[a for a, _ in r13]}")
        rec("L05", [a for a, _ in r12] == want_srv, f"đường khác TLS 1.2: máy chủ ghi cùng lý do {[a for a, _ in r12]}")
        rec("L05", all(c.startswith("lỗi ở đọc") for _, c in r13[:3]) and r13[3][1] == "ok"
            and all(c.startswith("lỗi ở bắt tay") for _, c in r12[:3]) and r12[3][1] == "ok",
            f"TLS 1.3: lỗi chứng chỉ khách tới ở lần ĐỌC; TLS 1.2: tới ngay trong bắt tay ({[c for _, c in r13]} / {[c for _, c in r12]})")
        rec("L05", [c.split(": ")[-1] for _, c in r13[:3]] == [alg.bnx_l05_client_alert[k] for k in ("none", "ca", "expired")],
            "cảnh báo phía khách: CERTIFICATE_REQUIRED / UNKNOWN_CA / CERTIFICATE_EXPIRED")
        # đường khác: đọc chứng chỉ bằng openssl x509 → alg.bnx_mtls_decision
        now = dt.datetime.now(dt.timezone.utc).replace(tzinfo=None)
        certs = [None]
        for t in CASES[1:]:
            iss = x509(ossl, d / f"{t}.crt", "-issuer").strip().split("CN=")[-1]
            nb = dt.datetime.strptime(" ".join(x509(ossl, d / f"{t}.crt", "-startdate").strip().split("=", 1)[1].split()[:4]), "%b %d %H:%M:%S %Y")
            na = dt.datetime.strptime(" ".join(x509(ossl, d / f"{t}.crt", "-enddate").strip().split("=", 1)[1].split()[:4]), "%b %d %H:%M:%S %Y")
            certs.append({"cn": t, "issuer": iss, "not_before": nb, "not_after": na})
        dec = [alg.bnx_mtls_decision(c, {"ca1"}, now) for c in certs]
        rec("L05", dec == ["none", "ca", "expired", "ok"] == alg.bnx_l05_cases(dt.datetime.now()),
            f"đọc issuer/hạn bằng openssl x509 rồi xét theo alg: {dec}")
        rec("L05", certs[2]["not_before"] == dt.datetime(2025, 1, 1) and certs[2]["not_after"] == dt.datetime(2025, 4, 1)
            and (certs[2]["not_after"] - certs[2]["not_before"]).days == 90 == alg.bnx_days_between("2025-01-01", "2025-04-01"),
            "het_han: 1/1/2025 → 1/4/2025 = 90 ngày (31 + 28 + 31)")
        rec("L05", (certs[3]["not_after"] - certs[3]["not_before"]).days == 90 and "DNS:localhost" in x509(ossl, d / "may_chu.crt", "-ext", "subjectAltName")
            and "CA:FALSE" in x509(ossl, d / "thanh_toan.crt", "-ext", "basicConstraints")
            and "Certificate Sign" in x509(ossl, d / "ca1.crt", "-ext", "keyUsage")
            and "CA:TRUE" in x509(ossl, d / "ca1.crt", "-ext", "basicConstraints"),
            "thanh_toan hạn 90 ngày, CA:FALSE; máy chủ có DNS:localhost; ca1 có keyUsage Certificate Sign và CA:TRUE (req -x509 tự thêm)")
        # cửa ④ (ca thứ năm): ke_toan do ca1 ký, còn hạn, qua ba cửa của thư viện; chỉ ứng dụng kiểm tên mới chặn được
        ke = x509(ossl, d / "ke_toan.crt", "-issuer", "-startdate", "-enddate")
        rv = subprocess.run([ossl, "verify", "-CAfile", "ca1.crt", "ke_toan.crt"], cwd=d, capture_output=True, text=True)
        rec("L05", rv.stdout.strip() == "ke_toan.crt: OK" and "CN=ca1" in ke
            and handshake(d, "ke_toan")[0] == "ok:ke_toan"
            and handshake(d, "ke_toan", allow={"thanh_toan"}) == ("tên không được phép", "no")
            and handshake(d, "thanh_toan", allow={"thanh_toan"}) == ("ok:thanh_toan", "ok"),
            "ke_toan: openssl verify OK (chuỗi + hạn đúng); không có cửa ④ thì được chào; có danh sách tên được phép thì bị từ chối, thanh_toan vẫn qua")
        rec("L05", handshake(d, "may_chu")[0] == "ok:localhost" and handshake(d, "may_chu", allow={"thanh_toan"})[0] == "tên không được phép",
            "thêm: không có cửa ④ thì chứng chỉ máy chủ do ca1 ký cũng làm khách được; có cửa ④ thì bị chặn")
        # nơi cấp thiếu keyUsage → Python 3.13 (kiểm nghiêm) từ chối
        sub = ["-subj", "/CN=ca3"]
        subprocess.run([ossl, "req", "-x509", "-newkey", "ed25519", "-noenc", *sub, "-days", "30", "-keyout", "ca3.key", "-out", "ca3.crt"], cwd=d, capture_output=True)
        subprocess.run([ossl, "req", "-x509", "-newkey", "ed25519", "-noenc", "-subj", "/CN=localhost", "-addext", "basicConstraints=CA:FALSE",
                        "-addext", "subjectAltName=DNS:localhost", "-CA", "ca3.crt", "-CAkey", "ca3.key", "-days", "30",
                        "-keyout", "mc3.key", "-out", "mc3.crt"], cwd=d, capture_output=True)
        mc = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        mc.load_cert_chain(str(d / "mc3.crt"), str(d / "mc3.key"))
        ls = socket.create_server(("127.0.0.1", 0))

        def srv3():
            c, _ = ls.accept()
            try:
                mc.wrap_socket(c, server_side=True).close()
            except (ssl.SSLError, OSError):
                pass
        th = threading.Thread(target=srv3)
        th.start()
        msg = ""
        try:
            kh = ssl.create_default_context(cafile=str(d / "ca3.crt"))
            with socket.create_connection(ls.getsockname()) as s, kh.wrap_socket(s, server_hostname="localhost"):
                pass
        except ssl.SSLCertVerificationError as e:
            msg = e.verify_message
        th.join()
        ls.close()
        rec("L05", msg == "CA cert does not include key usage extension" and sys.version_info >= (3, 13),
            f"nơi cấp thiếu keyUsage: Python {sys.version_info.major}.{sys.version_info.minor} từ chối “{msg}”")
        if sys.platform == "win32":
            r = subprocess.run([bash, "-c", "openssl req -x509 -newkey ed25519 -noenc -subj /CN=x -days 1 -keyout x.key -out x.crt"],
                               cwd=d, capture_output=True, text=True)
            rec("L05", r.returncode != 0 and "Program Files/Git/CN=x" in r.stderr, "Git Bash thiếu MSYS_NO_PATHCONV: “/CN=x” bị đổi thành đường dẫn, openssl từ chối")
    # số của bài
    rec("L05", (alg.bnx_add_days("2026-03-01", 90), alg.bnx_add_days("2026-03-01", 60), alg.bnx_rotate_day(90), 90 - alg.bnx_rotate_day(90))
        == ("2026-05-30", "2026-04-30", 60, 30) and (dt.date(2026, 3, 1) + dt.timedelta(days=90)).isoformat() == "2026-05-30" and 31 + 30 + 29 == 90,
        "hạn 90 ngày từ 1/3/2026 → 30/5/2026; xoay ở ngày 60 = 30/4/2026; dự phòng 30 ngày")
    def sim_rot(valid):   # mô phỏng: mỗi chứng chỉ được thay khi đã dùng 2/3 thời hạn; đếm số lần thay trong 365 ngày
        n, day = 0, 0
        while day + valid * 2 // 3 <= 365:
            day += valid * 2 // 3
            n += 1
        return n
    rec("L05", (alg.bnx_leak_window(365, 10), alg.bnx_leak_window(30, 10), alg.bnx_rotations_per_year(30), alg.bnx_rotations_per_year(365))
        == (355, 20, 18, 1) == (365 - 10, 30 - 10, sim_rot(30), sim_rot(365)),
        "câu 3: hở 355 / 20 ngày; xoay ở 2/3 thời hạn: 30 ngày → mỗi 20 ngày → 18 lần/năm; 365 ngày → 1 lần/năm (mô phỏng đếm)")
    blocks = (src.SH_CA, src.SH_SERVER, src.SH_BAD, src.PY_CTX, src.PY_SERVE, src.PY_CLIENT, src.PY_RUN)
    m = max(len(l) for c in blocks for l in c.strip("\n").split("\n"))
    rec("L05", m <= 70 and all(len(c.strip("\n").split("\n")) <= 15 for c in blocks) and not any("$" in c for c in blocks),
        f"khối mã ≤ 15 dòng, dòng dài nhất {m} ký tự, không có dấu $ (KaTeX)")
