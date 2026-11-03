"""Đo mức đủ-cho-người-mới của từng bài đã có đặc tả (đọc lessons/**/*.yaml, không dựng gì).

Mỗi bài một dòng TSV (audit/review/pedagogy_scan.tsv) + tóm tắt theo khoá ra màn hình.
Chỉ số (đều tính từ đặc tả, nên là OBSERVED về đặc tả, không phải về người học):
  phút        ước lượng thời lượng = số từ lời đọc / 140
  hình        số step có <svg> (hình vẽ cơ chế) ; bảng = step có <table> ; chuỗi = step có class="chain"
  trực_quan   tỉ lệ step có hình HOẶC bảng HOẶC chuỗi HOẶC công thức hiển thị ($$) HOẶC mã (<pre>)
  chữ_liền    số step liên tiếp dài nhất chỉ có chữ (người mới mất dấu khi nhìn bảng toàn chữ)
  chữ_max     số ký tự chữ lớn nhất trên một khung (sau khi bỏ thẻ)
  vd          số step thuộc phân cảnh example/check (làm bằng số từng bước)
  thiếu       phân cảnh nên có cho người mất gốc mà bài không có: prereq, intuition, check
  quiz_dap    quiz có pause và có ≥2 step đáp án sau pause
  recap_chuoi recap có chuỗi logic (class="chain")
  hook_so     hook có con số (tình huống thật có số đo)
  lý_do       tỉ lệ câu lời đọc có từ nối lý do (vì, nên, do đó, tức là, nghĩa là, bởi)
Ngưỡng cờ (đặt theo trung vị toàn kho, xem --stats): KHÔNG_HÌNH, CHỮ_LIỀN≥5, THIẾU_TRỰC_QUAN, THIẾU_KIỂM, QUIZ_THIẾU_ĐÁP.
"""
import re, sys, glob, statistics, pathlib, yaml
from collections import defaultdict

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import lv  # noqa: E402  luật E39 dùng chung với lint
REASON = re.compile(r"(?<!\w)(vì|nên|do đó|tức là|nghĩa là|bởi|cho nên|suy ra)(?!\w)", re.I)
SENT = re.compile(r"(?<=[.!?])\s+")
TAG = re.compile(r"<[^>]+>")


def text_of(show):
    s = TAG.sub(" ", show)
    s = re.sub(r"\$\$.*?\$\$", " ", s, flags=re.S)
    return re.sub(r"\s+", " ", s).strip()


def visual(show):
    return bool(re.search(r"<svg|<table|class=\"chain\"|\$\$|<pre|class=\"code\"", show))


def scan(path):
    spec = yaml.safe_load(open(path, encoding="utf-8"))
    steps, kinds = [], []
    for sc in spec.get("scenes", []):
        kinds.append(sc.get("kind"))
        for st in sc.get("steps", []):
            steps.append((sc.get("kind"), str(st.get("show", "") or ""), str(st.get("say", "") or ""), st.get("pause")))
    words = sum(len(s[2].split()) for s in steps)
    vis = [visual(s[1]) for s in steps]
    run = best = 0
    for v, s in zip(vis, steps):
        run = 0 if (v or not s[1].strip()) else run + 1
        best = max(best, run)
    sents = [x for s in steps for x in SENT.split(s[2]) if x.strip()]
    qsteps = [s for s in steps if s[0] == "quiz"]
    pi = next((i for i, s in enumerate(qsteps) if s[3]), None)
    hook = " ".join(s[1] + s[2] for s in steps if s[0] == "hook")
    r = dict(
        khoa=spec.get("course") or pathlib.Path(path).parent.name.upper(), bai=spec.get("id"),
        do_sau=spec.get("depth", ""), loai=spec.get("case", ""), tieu_de=spec.get("title", "")[:60],
        phut=round(words / 140, 1), step=len(steps),
        hinh=sum("<svg" in s[1] for s in steps), bang=sum("<table" in s[1] for s in steps),
        chuoi=sum('class="chain"' in s[1] for s in steps),
        truc_quan=round(sum(vis) / max(1, len(steps)), 2), chu_lien=best,
        chu_max=max((len(text_of(s[1])) for s in steps), default=0),
        vd=sum(s[0] in ("example", "check") for s in steps),
        thieu=",".join(k for k in ("prereq", "intuition", "check") if k not in kinds),
        quiz_dap=int(pi is not None and len(qsteps) - pi - 1 >= 2),
        recap_chuoi=int(any('class="chain"' in s[1] for s in steps if s[0] == "recap")),
        hook_so=int(bool(re.search(r"\d", hook))),
        ly_do=round(sum(bool(REASON.search(x)) for x in sents) / max(1, len(sents)), 2),
        file=str(pathlib.Path(path).relative_to(ROOT)).replace("\\", "/"),
    )
    flags = []
    if r["hinh"] == 0: flags.append("KHÔNG_HÌNH")
    if r["chu_lien"] >= 5: flags.append(f"CHỮ_LIỀN{r['chu_lien']}")
    if r["truc_quan"] < 0.4: flags.append("THIẾU_TRỰC_QUAN")
    if "check" in r["thieu"] and r["vd"] < 4: flags.append("THIẾU_KIỂM")
    if not r["quiz_dap"]: flags.append("QUIZ_THIẾU_ĐÁP")
    if not r["recap_chuoi"]: flags.append("RECAP_KHÔNG_CHUỖI")
    if not r["hook_so"]: flags.append("HOOK_KHÔNG_SỐ")
    r["co"] = " ".join(flags)
    # mức theo đúng luật E39 của lint (một nguồn sự thật): chạy lint_depth như thể bài khai `depth: full`
    rep = lv.Report()
    lv.lint_depth(dict(spec, depth="full"), rep)
    miss = [e.split("E39 ", 1)[1].split(" —")[0][:40] for e in rep.errors]
    r["thieu_e39"] = "; ".join(miss)
    r["muc"] = "ĐỦ" if not miss else ("GẦN" if len(miss) <= 2 else "MỎNG")
    return r


def main():
    rows = [scan(p) for p in sorted(glob.glob(str(ROOT / "lessons" / "**" / "*.yaml"), recursive=True))]
    rows = [r for r in rows if r["bai"]]
    cols = list(rows[0])
    out = ROOT / "audit" / "review" / "pedagogy_scan.tsv"
    with open(out, "w", encoding="utf-8") as f:
        f.write("\t".join(cols) + "\n")
        for r in rows:
            f.write("\t".join(str(r[c]) for c in cols) + "\n")
    by = defaultdict(list)
    for r in rows:
        by[r["khoa"]].append(r)
    print(f"{len(rows)} bài → {out.relative_to(ROOT)}")
    print("mức theo khoá (ĐỦ/GẦN/MỎNG):", {k: "/".join(str(sum(r["muc"] == m for r in rs)) for m in ("ĐỦ", "GẦN", "MỎNG")) for k, rs in sorted(by.items())})
    print("khoá  bài  phút  hình/bài  bài_0_hình  trực_quan  chữ_liền_max  vd/bài  thiếu_prereq  thiếu_intuition  thiếu_check  lý_do")
    for k, rs in sorted(by.items()):
        n = len(rs)
        print(f"{k:5} {n:4} {statistics.median(r['phut'] for r in rs):5.1f} {sum(r['hinh'] for r in rs)/n:8.2f} {sum(r['hinh']==0 for r in rs):10} "
              f"{statistics.median(r['truc_quan'] for r in rs):10.2f} {max(r['chu_lien'] for r in rs):12} {sum(r['vd'] for r in rs)/n:7.1f} "
              f"{sum('prereq' in r['thieu'] for r in rs):12} {sum('intuition' in r['thieu'] for r in rs):16} {sum('check' in r['thieu'] for r in rs):12} "
              f"{statistics.median(r['ly_do'] for r in rs):6.2f}")
    if "--stats" in sys.argv:
        for c in ("phut", "step", "hinh", "truc_quan", "chu_lien", "chu_max", "vd", "ly_do"):
            v = sorted(r[c] for r in rows)
            print(f"{c:10} min {v[0]} p25 {v[len(v)//4]} med {v[len(v)//2]} p75 {v[3*len(v)//4]} max {v[-1]}")
        fl = defaultdict(int)
        for r in rows:
            for f in r["co"].split():
                fl[re.sub(r"\d+$", "", f)] += 1
        print("cờ:", dict(fl))


if __name__ == "__main__":
    main()
