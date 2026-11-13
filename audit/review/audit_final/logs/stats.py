import sys, re, pathlib, json, collections
sys.stdout.reconfigure(encoding="utf-8")
import yaml
root = pathlib.Path("D:/research-video")
PRACT = re.compile(r"(tự gõ|gõ lại|hãy chạy|chạy thử trên máy|trên máy của bạn|trên máy bạn|hãy cài|cài đặt|bài tập|tự viết|hãy viết|thực hành)", re.I)
KW = ["Python", "PyTorch", "NumPy", "numpy", "pandas", "Docker", "Linux", "terminal", "dòng lệnh", "Git", "SQL", "IDE", "debugger", "gỡ lỗi"]
tot = collections.Counter()
rows = []
kwles = collections.defaultdict(set)
for cdir in sorted((root / "lessons").iterdir()):
    if not cdir.is_dir():
        continue
    n = code = pract = quiz = 0
    mins = 0.0
    for f in sorted(cdir.glob("L*.yaml")):
        txt = f.read_text(encoding="utf-8")
        n += 1
        if 'class="code' in txt or "class='code" in txt or "<pre" in txt:
            code += 1
        d = yaml.safe_load(txt)
        say = []
        def walk(o):
            if isinstance(o, dict):
                for k, v in o.items():
                    if k == "say":
                        say.append(v if isinstance(v, str) else " ".join(map(str, v)) if isinstance(v, list) else str(v))
                    else:
                        walk(v)
            elif isinstance(o, list):
                for v in o:
                    walk(v)
        walk(d)
        s = " ".join(say)
        if PRACT.search(s):
            pract += 1
        for k in KW:
            if re.search(r"(?<![A-Za-z])" + re.escape(k) + r"(?![A-Za-z])", txt):
                kwles[k].add(cdir.name + ":" + f.name[:3])
        br = root / "out" / cdir.name.upper() / f.name[:3] / "build_report.json"
        if br.exists():
            try:
                b = json.loads(br.read_text(encoding="utf-8"))
                mins += float(b.get("duration", b.get("duration_s", 0)) or 0) / 60
            except Exception:
                pass
    rows.append((cdir.name.upper(), n, code, pract, round(mins, 1)))
    tot["n"] += n; tot["code"] += code; tot["pract"] += pract
print("khoá | bài | bài có khối mã | bài có lời mời thực hành (từ khoá trong say) | phút")
for r in rows:
    print(" | ".join(map(str, r)))
print("TỔNG", dict(tot))
for k in KW:
    cs = collections.Counter(x.split(":")[0] for x in kwles[k])
    print(k, len(kwles[k]), dict(cs.most_common(8)))
