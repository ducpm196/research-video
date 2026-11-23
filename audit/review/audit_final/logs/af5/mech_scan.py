"""AF5 — đo cơ học (chỉ đọc) mức khuôn mẫu của đợt nâng AF2 hàng loạt.
Chạy: .venv/Scripts/python -B audit/review/audit_final/logs/af5/mech_scan.py
Ghi: logs/af5/mech_scan.tsv (một dòng/bài), logs/af5/mech_dups.tsv (câu lặp ≥ 5 bài), in tổng theo khoá.
Không sửa tệp nào ngoài hai tệp tsv của chính nó."""
import collections
import hashlib
import json
import pathlib
import re
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import lv  # noqa: E402

OUT = pathlib.Path(__file__).resolve().parent
GEN_SAY = "Bây giờ đến phần bạn tự thực hành và chấm điểm trực tiếp trên máy."
GEN_TITLE = "Tự làm bài thực hành và chấm thật"
TAG = re.compile(r"<[^>]+>")


def words(s):
    return len(re.findall(r"\w+", s or "", re.U))


rows = []
sent_lessons = collections.defaultdict(set)
lesson_sents = {}
de_hash = collections.defaultdict(list)
for p in sorted((ROOT / "lessons").glob("*/L*.yaml")):
    C = p.parent.name.upper()
    lid = p.name.split("_")[0]
    d = yaml.safe_load(p.read_text(encoding="utf-8"))
    scenes = d.get("scenes") or []
    says, shows = [], []
    prac = [s for s in scenes if s.get("kind") == "practice"]
    for s in scenes:
        for st in s.get("steps") or []:
            says.append(st.get("say") or "")
            shows.append(st.get("show") or "")
    sents = [x.strip() for t in says for x in lv.sentences(t)]
    lesson_sents[(C, lid)] = sents
    for x in set(sents):
        sent_lessons[x].add((C, lid))
    n_words = sum(words(x) for x in says)
    kinds = collections.Counter(s.get("kind") for s in scenes)
    pr = prac[0] if prac else None
    pr_steps = len(pr.get("steps") or []) if pr else 0
    pr_say = " ".join((st.get("say") or "") for st in (pr.get("steps") or [])) if pr else ""
    pr_show = " ".join((st.get("show") or "") for st in (pr.get("steps") or [])) if pr else ""
    generic = bool(pr and (GEN_SAY in pr_say or pr.get("title") == GEN_TITLE))
    lab = (pr or {}).get("lab") or ""
    ld = ROOT / lab if lab else None
    de_w = exp_lines = 0
    sol_ext = ""
    de_leak = False
    exp_in_ex = None
    if ld and ld.is_dir():
        de = (ld / "de.md").read_text(encoding="utf-8") if (ld / "de.md").exists() else ""
        exp = (ld / "mong_doi.txt").read_text(encoding="utf-8") if (ld / "mong_doi.txt").exists() else ""
        de_w = words(de)
        el = [l.strip() for l in exp.splitlines() if l.strip()]
        exp_lines = len(el)
        sols = sorted(ld.glob("loi_giai.*"))
        sol_ext = ",".join(s.suffix[1:] for s in sols)
        # đề chép nguyên mọi dòng đáp án?
        de_leak = bool(el) and all(l in de for l in el)
        de_hash[hashlib.sha1(re.sub(r"\s+", " ", de).encode()).hexdigest()].append(f"{C}:{lid}")
        # mọi dòng đáp án có sẵn nguyên văn ở các cảnh KHÁC practice (số liệu lab trùng ví dụ)?
        other = TAG.sub(" ", " ".join((st.get("show") or "") for s in scenes if s.get("kind") != "practice" for st in s.get("steps") or []))
        vals = [v for l in el for v in re.findall(r"[-+]?\d[\d.,]*", l)]
        exp_in_ex = (sum(1 for v in vals if v in other), len(vals))
    br = ROOT / "out" / C / lid / "build_report.json"
    dur = 0.0
    if br.exists():
        j = json.loads(br.read_text(encoding="utf-8"))
        dur = float(j.get("timeline_seconds") or 0)
    covers = d.get("covers") or []
    objs = d.get("objectives") or []
    cov_pr = sum(1 for c in covers if c.get("scene") == "practice")
    quiz = [s for s in scenes if s.get("kind") == "quiz"]
    n_svg = sum(x.count("<svg") for x in shows)
    n_code = sum(x.count('class="code"') + x.count("class='code'") for x in shows)
    rows.append(dict(course=C, id=lid, af2=bool(d.get("af2")), words=n_words, dur_min=round(dur / 60, 2), scenes=len(scenes),
                     objectives=len(objs), covers=len(covers), covers_practice=cov_pr, practice=len(prac), pr_steps=pr_steps,
                     pr_generic=generic, pr_pause=bool(pr and any(st.get("pause") for st in pr.get("steps") or [])),
                     pr_task_on_screen=bool(pr and not generic), lab=lab, sol=sol_ext, de_words=de_w, exp_lines=exp_lines,
                     de_leaks_answers=de_leak, exp_vals_in_lesson=f"{exp_in_ex[0]}/{exp_in_ex[1]}" if exp_in_ex else "",
                     quiz=len(quiz), svg=n_svg, code=n_code, checks=sum(len(s.get("checks") or []) for s in scenes)))

# câu lặp nhiều bài
dup = {s: v for s, v in sent_lessons.items() if len(v) >= 5 and words(s) >= 4}
for r in rows:
    ss = lesson_sents[(r["course"], r["id"])]
    tot = sum(words(x) for x in ss) or 1
    r["dup_words_pct"] = round(100 * sum(words(x) for x in ss if x in dup) / tot, 1)
    r["dup_sents"] = sum(1 for x in ss if x in dup)

keys = list(rows[0].keys())
(OUT / "mech_scan.tsv").write_text("\t".join(keys) + "\n" + "\n".join("\t".join(str(r[k]) for k in keys) for r in rows), encoding="utf-8")
(OUT / "mech_dups.tsv").write_text("n_lessons\tn_courses\twords\tsentence\n" + "\n".join(
    f"{len(v)}\t{len({c for c, _ in v})}\t{words(s)}\t{s}" for s, v in sorted(dup.items(), key=lambda kv: -len(kv[1]))), encoding="utf-8")

by = collections.defaultdict(list)
for r in rows:
    by[r["course"]].append(r)
print(f"{'khoá':<6}{'bài':>4}{'af2':>4}{'prGEN':>6}{'pr≥3b':>6}{'leak':>5}{'md':>4}{'<9p':>4}{'>16p':>5}{'dup%':>6}{'từ tb':>7}{'đề tb':>6}")
T = collections.Counter()
for c, rs in sorted(by.items()):
    n = len(rs)
    g = sum(r["pr_generic"] for r in rs)
    s3 = sum(r["pr_steps"] >= 3 for r in rs)
    lk = sum(r["de_leaks_answers"] for r in rs)
    md = sum(r["sol"] == "md" for r in rs)
    sh = sum(0 < r["dur_min"] < 9 for r in rs)
    lg = sum(r["dur_min"] > 16 for r in rs)
    print(f"{c:<6}{n:>4}{sum(r['af2'] for r in rs):>4}{g:>6}{s3:>6}{lk:>5}{md:>4}{sh:>4}{lg:>5}{sum(r['dup_words_pct'] for r in rs)/n:>6.1f}{sum(r['words'] for r in rs)//n:>7}{sum(r['de_words'] for r in rs)//n:>6}")
    T.update(n=n, af2=sum(r["af2"] for r in rs), gen=g, s3=s3, leak=lk, md=md, short=sh, long=lg, nodur=sum(r["dur_min"] == 0 for r in rs),
             noprac=sum(r["practice"] == 0 for r in rs), noquiz=sum(r["quiz"] == 0 for r in rs))
print("TỔNG", dict(T))
print("câu lặp ≥5 bài:", len(dup), "| đề lab trùng nhau (nhóm ≥2):", sum(1 for v in de_hash.values() if len(v) > 1))
print("tổng phút:", round(sum(r["dur_min"] for r in rows), 1))
