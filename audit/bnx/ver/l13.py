"""Kiểm độc lập BNX L13: phân tích YAML THẬT (pyyaml) của bài, mô phỏng bằng cách KHÁC checklib rồi đối chiếu alg.bnx_*.
- Cập nhật cuốn chiếu: checklib mô phỏng bộ điều khiển theo đợt; ở đây (a) bộ điều khiển viết lại với từng Pod có tên và đồng hồ,
  (b) mọi thứ tự hành động ngẫu nhiên hợp lệ (bao cận ≥ 3 / ≤ 5), (c) liệt kê trạng thái (chạy nguyên văn khối PY_ROLL).
- Đường ống: đọc stages/job từ YAML, mô phỏng bằng hàng đợi giai đoạn riêng.
- Bộ nhớ đệm Dockerfile: chuỗi khoá đệm băm nối tiếp (key_i = sha256(key_{i-1} + lệnh + băm tệp đầu vào)), đếm lớp đổi khoá.
- Dockerfile thật: docker build --check (cần Docker; không có → SKIP)."""
import hashlib
import io
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile
from contextlib import redirect_stdout
from fractions import Fraction
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "audit" / "bnx" / "src"))
sys.path.insert(0, str(ROOT / "audit" / "bnx"))
sys.path.insert(0, str(ROOT / "tools"))
import checklib as alg  # noqa: E402
import l13  # noqa: E402


def pods_sim(D, mu, ms, seed):
    """Từng Pod có tên; mỗi bước chọn ngẫu nhiên một hành động hợp lệ: tạo mới / xoá cũ / một Pod mới khởi động xong."""
    rnd = random.Random(seed)
    pods = [{"v": "cu", "ready": True} for _ in range(D)]
    lo_seen, hi_seen, steps = D, D, 0
    while not (len(pods) == D and all(p["v"] == "moi" and p["ready"] for p in pods)):
        ready = sum(p["ready"] for p in pods)
        acts = []
        if len(pods) < D + ms and sum(p["v"] == "moi" for p in pods) < D:
            acts.append("tao")
        olds = [i for i, p in enumerate(pods) if p["v"] == "cu"]
        if olds and ready - 1 >= D - mu:
            acts.append("xoa")
        starting = [i for i, p in enumerate(pods) if not p["ready"]]
        if starting:
            acts.append("san")
        a = rnd.choice(acts)
        if a == "tao":
            pods.append({"v": "moi", "ready": False})
        elif a == "xoa":
            pods.pop(rnd.choice(olds))
        else:
            pods[rnd.choice(starting)]["ready"] = True
        lo_seen = min(lo_seen, sum(p["ready"] for p in pods))
        hi_seen = max(hi_seen, len(pods))
        steps += 1
        if steps > 1000:
            raise RuntimeError("kẹt")
    return lo_seen, hi_seen


def controller_sim(D, mu, ms, T=10):
    """Bộ điều khiển Deployment theo mã nguồn Kubernetes, viết lại kiểu khác checklib: danh sách Pod có tên và giờ sẵn sàng,
    đồng hồ thời gian; mỗi lần đồng bộ tăng RS mới trước (có tăng thì dừng lần đó), không thì giảm RS cũ theo maxScaledDown;
    hết việc thì tua đồng hồ tới giờ sẵn sàng kế tiếp. Trả (số lần phải chờ, sẵn sàng thấp nhất, Pod cao nhất, thứ tự hành động)."""
    mu = pct(mu, D, False)
    ms = pct(ms, D, True)
    t, waits, log = 0, 0, []
    old = [{"ten": f"cu{i}", "ready_at": -1} for i in range(D)]
    new = []
    lo, hi = D, D

    def avail(lst):
        return sum(1 for p_ in lst if p_["ready_at"] <= t)
    while True:
        changed = True
        while changed:
            changed = False
            total = len(old) + len(new)
            up = min(D + ms - total, D - len(new))
            if up > 0:
                for _ in range(up):
                    new.append({"ten": f"moi{len(new)}", "ready_at": t + T})
                log.append(f"tao{up}")
                changed = True
            else:
                min_av = D - mu
                new_unav = len(new) - avail(new)
                if total - min_av - new_unav > 0 and old:
                    k = min(avail(old) + avail(new) - min_av, len(old))
                    if k > 0:
                        del old[:k]
                        log.append(f"xoa{k}")
                        changed = True
            lo = min(lo, avail(old) + avail(new))
            hi = max(hi, len(old) + len(new))
        pending = [p_["ready_at"] for p_ in new if p_["ready_at"] > t]
        if not pending:
            return waits, lo, hi, log
        t = min(pending)
        waits += 1


def pct(v, D, up):
    if isinstance(v, str):
        num = Fraction(int(v.rstrip("%")) * D, 100)
        return -((-num.numerator) // num.denominator) if up else num.numerator // num.denominator
    return v


def run(rec):
    # ── Deployment: đọc YAML thật ──
    dep = yaml.safe_load(l13.DEPLOY_YML)
    sp = dep["spec"]
    ru = sp["strategy"]["rollingUpdate"]
    D, mu, ms = sp["replicas"], ru["maxUnavailable"], ru["maxSurge"]
    rec("L13", dep["apiVersion"] == "apps/v1" and dep["kind"] == "Deployment" and sp["strategy"]["type"] == "RollingUpdate"
        and set(sp) == {"replicas", "strategy", "selector", "template"} and set(ru) == {"maxUnavailable", "maxSurge"}
        and sp["selector"]["matchLabels"] == sp["template"]["metadata"]["labels"],
        "Deployment YAML: apps/v1, RollingUpdate, tên trường đúng DeploymentSpec, selector khớp nhãn mẫu")
    c = sp["template"]["spec"]["containers"][0]
    rec("L13", c["readinessProbe"]["httpGet"]["port"] == c["ports"][0]["containerPort"] == 8080
        and c["image"].endswith(":" + alg.bnx_git_demo()["merge"][:8]) and c["image"].split(":")[-1] == "0eac7e6a",
        "ảnh gắn 8 ký tự đầu mã commit gộp bài 0; phép kiểm sẵn sàng đúng cổng 8080")
    lo_hi = set(pods_sim(D, mu, ms, s) for s in range(300))
    worst = (min(x for x, _ in lo_hi), max(y for _, y in lo_hi))
    rec("L13", (D, mu, ms) == (4, 1, 1) and worst == (3, 5) == alg.bnx_rolling_bounds(D, mu, ms)
        and alg.bnx_rolling_summary(D, mu, ms)[1:] == worst,
        f"300 lần mô phỏng từng Pod theo thứ tự ngẫu nhiên: sẵn sàng thấp nhất {worst[0]}, Pod cao nhất {worst[1]} = checklib")
    # liệt kê trạng thái: chạy nguyên văn khối trên màn hình, so với checklib
    buf = io.StringIO()
    with redirect_stdout(buf):
        exec(compile(l13.PY_ROLL.strip("\n"), "PY_ROLL", "exec"), {})
    rec("L13", buf.getvalue().strip() == l13.PY_ROLL_OUT.strip() == "24 3 5 True"
        and buf.getvalue().split()[1:3] == [str(x) for x in alg.bnx_rolling_bounds(4, 1, 1)],
        f"khối liệt kê trạng thái in {buf.getvalue().strip()!r}; 3 và 5 khớp checklib")
    # bộ điều khiển theo mã nguồn Kubernetes (rolling.go): mô phỏng từng Pod có đồng hồ, so với checklib theo đợt
    cs = controller_sim(D, mu, ms)
    rows, trace = alg.bnx_rolling_waves(D, mu, ms)
    rec("L13", cs[:3] == (2, 3, 5) == alg.bnx_rolling_summary(D, mu, ms) and cs[3][:3] == ["tao1", "xoa1", "tao1"]
        and rows == [(1, 3, 2, 0, 5, 3), (2, 1, 2, 2, 5, 3)],
        f"bộ điều khiển (4, 1, 1): {cs[3]} → 2 đợt chờ, sẵn sàng ≥ 3, Pod ≤ 5; khớp tài liệu “first creates a new Pod, then deletes an old Pod, and creates another new one”")
    cs01 = controller_sim(4, 0, 1)
    cs61 = controller_sim(6, 2, 1)
    cs25 = controller_sim(10, "25%", "25%")
    rec("L13", cs01[:3] == (4, 4, 5) == alg.bnx_rolling_summary(4, 0, 1) and cs61[1:3] == (4, 7) == alg.bnx_rolling_summary(6, 2, 1)[1:]
        and cs25[:3] == alg.bnx_rolling_summary(10, "25%", "25%") and cs25[1:3] == (8, 13),
        f"(0, 1): {cs01[0]} đợt chờ, luôn 4 sẵn sàng; 6 bản (2, 1): 4 và 7; 10 bản 25%: 8 và 13 — khớp checklib")
    # phần trăm mặc định 25 % và các đề quiz, bằng mô phỏng từng Pod
    q1 = set(pods_sim(6, 2, 1, s) for s in range(300))
    q3 = set(pods_sim(4, 0, 1, s) for s in range(300))
    rec("L13", (pct("25%", 4, False), pct("25%", 4, True)) == (1, 1) == (alg.bnx_k8s_abs("25%", 4, False), alg.bnx_k8s_abs("25%", 4, True))
        and (min(x for x, _ in q1), max(y for _, y in q1)) == (4, 7) == alg.bnx_rolling_bounds(6, 2, 1)
        and (min(x for x, _ in q3), max(y for _, y in q3)) == (4, 5) == alg.bnx_rolling_bounds(4, 0, 1),
        "25% của 4 = 1 (xuống/lên); câu 1: 6 bản (2, 1) → 4 và 7; (0, 1) → luôn 4 sẵn sàng, ≤ 5 Pod")
    rec("L13", (cs01[0], cs[0]) == (4, 2) and 3 * 250 < 900 <= 4 * 250 and 3 * 250 >= 600
        and Fraction(3, 4) == Fraction(75, 100),
        "câu 3: (0, 1) cần 4 đợt chờ thay vì 2; 750 < 900 ≤ 1000; ví dụ ⑤ 750 ≥ 600; 3/4 = 75%")

    # ── Đường ống: đọc YAML thật, mô phỏng bằng hàng đợi giai đoạn ──
    ci = yaml.safe_load(l13.CI_YML)
    stages = ci["stages"]
    jobs = {k: v["stage"] for k, v in ci.items() if isinstance(v, dict) and "stage" in v}

    def queue_sim(fail):
        out, q = {}, list(stages)
        while q:
            s = q.pop(0)
            js = [j for j in jobs if jobs[j] == s]
            for j in js:
                out[j] = "failed" if j in fail else "success"
            if any(out[j] == "failed" for j in js):
                for rest in q:
                    for j in jobs:
                        if jobs[j] == rest:
                            out[j] = "skipped"
                break
        return out
    ok_struct = stages == ["build", "test", "package", "deploy"] and all(s in stages for s in jobs.values()) and len(jobs) == 4
    sims = {f: queue_sim({f}) for f in jobs}
    rec("L13", ok_struct and all(sims[f] == alg.bnx_pipeline(stages, jobs, {f}) for f in jobs)
        and [k for k, v in sims["test"].items() if v == "skipped"] == ["package", "deploy"] and sims["package"]["deploy"] == "skipped",
        "YAML đường ống: 4 giai đoạn đúng thứ tự; test hỏng → package, deploy không chạy; package hỏng → deploy không chạy")
    rec("L13", ci["package"]["script"][0] == 'echo "$CI_REGISTRY_PASSWORD" | docker login $CI_REGISTRY -u $CI_REGISTRY_USER --password-stdin'
        and ci["package"]["script"][1:] == ["docker build -t $IMG .", "docker push $IMG"],
        "job package: đăng nhập kho ảnh đúng nguyên chữ ví dụ của GitLab (--password-stdin) trước khi dựng và đẩy")
    rec("L13", ci["variables"]["IMG"] == "$CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA" and all("$IMG" in " ".join(ci[j]["script"]) for j in ("package", "deploy"))
        and alg.bnx_short_sha(alg.bnx_git_demo()["merge"]) == "0eac7e6a" and len("0eac7e6a") * 4 == 32,
        "thẻ ảnh = CI_COMMIT_SHORT_SHA (8 ký tự đầu) dùng ở cả package và deploy")

    # ── Bộ nhớ đệm Dockerfile: chuỗi khoá băm nối tiếp ──
    df = [ln for ln in l13.DOCKERFILE.strip().splitlines()]
    build_stage = df[:df.index(next(ln for ln in df[1:] if ln.startswith("FROM")))]
    files_v1 = {"pom.xml": "p1", "src/Main.java": "m1"}
    files_v2 = dict(files_v1, **{"src/Main.java": "m2"})

    def inputs(line, fs):
        m = re.match(r"COPY (\S+) ", line)
        if not m:
            return ""
        src = m.group(1)
        return "".join(v for k, v in sorted(fs.items()) if src == "." or k == src or k.startswith(src.rstrip("/") + "/"))

    def keys(lines, fs):
        k, out = "", []
        for ln in lines:
            k = hashlib.sha256((k + ln + inputs(ln, fs)).encode()).hexdigest()
            out.append(k)
        return out
    good = [i + 1 for i, (a, b) in enumerate(zip(keys(build_stage, files_v1), keys(build_stage, files_v2))) if a != b]
    bad_df = ["FROM maven:3.9.9-eclipse-temurin-21", "WORKDIR /src", "COPY . .", "RUN mvn -q package"]
    bad = [i + 1 for i, (a, b) in enumerate(zip(keys(bad_df, files_v1), keys(bad_df, files_v2))) if a != b]
    rec("L13", len(build_stage) == 6 and good == [5, 6] == alg.bnx_cache_rebuilt(alg.bnx_df_good, {"src/Main.java"})
        and bad == [3, 4] == alg.bnx_cache_rebuilt(alg.bnx_df_bad, {"src/Main.java"}) and (30, 90 + 30) == (30, 120),
        f"chuỗi khoá đệm: thứ tự đúng dựng lại lớp {good}, thứ tự sai {bad}; 30 giây so với 120 giây (số minh hoạ)")
    rec("L13", "latest" not in l13.DOCKERFILE and re.search(r"FROM \S+:\d", l13.DOCKERFILE) and "USER 10001" in l13.DOCKERFILE,
        "Dockerfile: không có latest, ảnh nền ghim số phiên bản, không chạy bằng root")

    # ── Dockerfile thật: docker build --check ──
    if not shutil.which("docker"):
        rec("L13", None, "không có docker để chạy docker build --check")
        return

    def check(text):
        d = tempfile.mkdtemp(prefix="bnx_l13df_")
        Path(d, "Dockerfile").write_text(text.strip("\n") + "\n", encoding="utf-8", newline="\n")
        p = subprocess.run(["docker", "build", "--check", "."], cwd=d, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=240)
        shutil.rmtree(d, ignore_errors=True)
        return p.returncode, p.stdout + p.stderr
    try:
        rg, og = check(l13.DOCKERFILE)
        rb, ob = check(l13.BAD_DF)
    except Exception as ex:  # Docker không chạy / không có mạng tới Docker Hub
        rec("L13", None, f"docker build --check không chạy được: {type(ex).__name__}")
        return
    if "load metadata" not in og and "Check complete" not in og:
        rec("L13", None, "docker build --check không đọc được siêu dữ liệu ảnh nền (mạng?)")
        return
    rec("L13", rg == 0 and "Check complete, no warnings found." in og,
        "docker build --check trên Dockerfile của bài: không cảnh báo; hai thẻ ảnh nền ghim có thật")
    rec("L13", rb != 0 and "1 warning has been found" in ob and "SecretsUsedInArgOrEnv" in ob and 'ENV "DB_PASSWORD"' in ob,
        "docker build --check trên Dockerfile sai: đúng 1 cảnh báo mật khẩu trong ENV; thẻ latest không bị báo")
