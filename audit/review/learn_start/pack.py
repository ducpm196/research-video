"""Gói học cho người bắt đầu: hai lộ trình (P: phỏng vấn backend ngân hàng; N: nền tảng chung).

Dùng (từ gốc kho):
  .venv/Scripts/python -B audit/review/learn_start/pack.py list
  .venv/Scripts/python -B audit/review/learn_start/pack.py check [--decode] [--tsv out.tsv]
  .venv/Scripts/python -B audit/review/learn_start/pack.py preview      # sinh lại preview.html cho bài nào lệch
  .venv/Scripts/python -B audit/review/learn_start/pack.py page         # sinh HOC_TAP.html + HOC_TAP.md, rồi kiểm liên kết

Lộ trình:
  P = JVA → BNK → INT → ACB, mỗi khoá đủ bài theo thứ tự trong curriculum/<khoá>.yaml
      ("đường học tối thiểu cho người mất gốc", interview/MASTER_CURRICULUM_INDEX.md).
  N = mục tiêu "nen-tang" của curriculum/tracks.yaml, bao đóng tiên quyết (requires, requires_ext) rồi sắp tô pô
      như audit/review/tracks.py (phá hoà theo `prefer`, rồi số bài); kiểm lại từng cạnh.

check, cho mỗi bài:
  - mục giáo án có `spec` trỏ tới tệp có thật; tiêu đề đặc tả = tiêu đề giáo án;
  - out/<KHOÁ>/<id>/: mp4, srt, chapters.txt, build_report.json, preview.html;
  - ffprobe: h264 1920x1080 + aac; |độ dài − timeline| ≤ 0,5 s;
  - (--decode) ffmpeg giải mã trọn, không in lỗi;
  - srt: số thứ tự liên tiếp, đầu < cuối, tăng dần, cuối ≤ độ dài + 0,5 s, chữ không rỗng;
  - chapters: bắt đầu 00:00, tăng dần, < độ dài;
  - build_report.spec_sha256 = lv.spec_digest(đặc tả hiện tại);
  - preview.html trùng từng byte với bản lv.player_html sinh ra từ đặc tả hiện tại (không cũ).
"""
import argparse
import html
import io
import json
import re
import subprocess
import sys
from collections import defaultdict
from contextlib import redirect_stdout
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import lv  # noqa: E402

FFPROBE = "ffprobe"
FFMPEG = "ffmpeg"


def load_cur():
    cur = {}
    for f in sorted((ROOT / "curriculum").glob("*.yaml")):
        c = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
        if isinstance(c, dict) and c.get("course"):
            cur[str(c["course"])] = c
    return cur


def path_P(cur):
    return [(C, l) for C in ("JVA", "BNK", "INT", "ACB") for l in cur[C]["lessons"]]


def path_N(cur):
    tr = yaml.safe_load((ROOT / "curriculum" / "tracks.yaml").read_text(encoding="utf-8"))
    prefer = tr["prefer"]
    goals = next(t for t in tr["tracks"] if t["id"] == "nen-tang")["goals"]
    les = {f"{C}:{l['id']}": (C, l) for C, c in cur.items() for l in c["lessons"]}
    pre = {u: {f"{C}:{q}" for q in l.get("requires") or []} | {str(q) for q in l.get("requires_ext") or []}
           for u, (C, l) in les.items()}

    def expand(g):
        if ":" not in g:
            return [f"{g}:{l['id']}" for l in cur[g]["lessons"]]
        C, rng = g.split(":")
        m = re.fullmatch(r"L(\d+)(?:-L(\d+))?", rng)
        return [f"{C}:L{k:02d}" for k in range(int(m.group(1)), int(m.group(2) or m.group(1)) + 1)]

    need, stack = set(), [u for g in goals for u in expand(g)]
    while stack:
        u = stack.pop()
        if u in need:
            continue
        assert u in les, f"tiên quyết {u} không có"
        need.add(u)
        stack += list(pre[u])
    key = lambda u: (prefer.index(u.split(":")[0]), int(u.split(":L")[1]))
    ind = {u: len(pre[u] & need) for u in need}
    order, ready = [], sorted((u for u in need if ind[u] == 0), key=key)
    while ready:
        u = ready.pop(0)
        order.append(u)
        for v in need:
            if u in pre[v]:
                ind[v] -= 1
                if ind[v] == 0:
                    ready.append(v)
        ready.sort(key=key)
    assert len(order) == len(need), "chu trình tiên quyết"
    pos = {u: i for i, u in enumerate(order)}
    assert all(pos[a] < pos[u] for u in need for a in pre[u]), "thứ tự vi phạm tiên quyết"
    return [les[u] for u in order]


PATHS = {"P": ("Lộ trình phỏng vấn backend ngân hàng", path_P), "N": ("Lộ trình nền tảng khoa học máy tính", path_N)}


def all_items(cur):
    return {k: f(cur) for k, (_, f) in PATHS.items()}


def odir(C, l):
    return ROOT / "out" / C / l["id"]


def ffprobe(mp4):
    r = subprocess.run([FFPROBE, "-v", "error", "-show_entries", "stream=codec_type,codec_name,width,height:format=duration",
                        "-of", "json", str(mp4)], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode:
        return None, r.stderr.strip()[:200]
    return json.loads(r.stdout), ""


def decode_errors(mp4):
    r = subprocess.run([FFMPEG, "-v", "error", "-xerror", "-i", str(mp4), "-f", "null", "-"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    return (r.returncode, r.stderr.strip()[:300])


TS = re.compile(r"(\d\d):(\d\d):(\d\d),(\d\d\d) --> (\d\d):(\d\d):(\d\d),(\d\d\d)$")


def srt_problems(p, dur):
    probs, blocks = [], [b for b in re.split(r"\n\s*\n", p.read_text(encoding="utf-8-sig").strip()) if b.strip()]
    prev = -1.0
    for i, b in enumerate(blocks, 1):
        ls = b.splitlines()
        if len(ls) < 3 or ls[0].strip() != str(i):
            probs.append(f"srt khối {i} sai dạng")
            break
        m = TS.match(ls[1].strip())
        if not m:
            probs.append(f"srt khối {i} mốc sai dạng")
            break
        g = [int(x) for x in m.groups()]
        a = g[0] * 3600 + g[1] * 60 + g[2] + g[3] / 1000
        e = g[4] * 3600 + g[5] * 60 + g[6] + g[7] / 1000
        if not (a < e and a >= prev):
            probs.append(f"srt khối {i} mốc không tăng")
        if not " ".join(ls[2:]).strip():
            probs.append(f"srt khối {i} rỗng")
        prev = a
        last = e
    if blocks and dur is not None and last > dur + 0.5:
        probs.append(f"srt kết thúc {last:.1f}s > video {dur:.1f}s")
    return len(blocks), probs


def chapter_problems(p, dur):
    probs, prev, n = [], -1, 0
    for ln in p.read_text(encoding="utf-8").splitlines():
        if not ln.strip():
            continue
        m = re.match(r"(\d+):(\d\d)(?::(\d\d))? (.+)$", ln)
        if not m:
            probs.append(f"chapters dòng sai dạng: {ln[:40]}")
            continue
        t = int(m.group(1)) * 60 + int(m.group(2)) if m.group(3) is None else int(m.group(1)) * 3600 + int(m.group(2)) * 60 + int(m.group(3))
        if n == 0 and t != 0:
            probs.append("chapters không bắt đầu 00:00")
        if t <= prev:
            probs.append(f"chapters không tăng ở {ln[:20]}")
        if dur is not None and t >= dur:
            probs.append(f"chapters {ln[:8]} vượt độ dài")
        prev, n = t, n + 1
    return n, probs


def norm_title(s):   # cùng quy ước với audit/review/check_meta.py: bỏ tiền tố "Bài N — " / "Chuyên đề N — "
    return re.sub(r"\s+", " ", re.sub(r"^(Bài|Chuyên đề) \d+( \([^)]*\))? — ", "", str(s))).strip()


def spec_of(l):
    return lv.load_spec(ROOT / l["spec"])


def preview_expected(spec):
    with redirect_stdout(io.StringIO()):
        frames = lv.build_frames(spec)
        total = lv.timeline(spec, frames)
    return lv.player_html(spec, frames, total, capture=False)


def check_one(C, l, decode):
    probs, info = [], {"C": C, "id": l["id"], "title": l["title"]}
    sp = ROOT / str(l.get("spec") or "")
    if not l.get("spec") or not sp.exists():
        return info | {"probs": ["giáo án không trỏ tới đặc tả có thật"]}
    spec = spec_of(l)
    if norm_title(spec.get("title")) != norm_title(l["title"]):
        probs.append(f"tiêu đề đặc tả ≠ giáo án: {spec.get('title')!r}")
    d = odir(C, l)
    mp4, srt, ch, rep, pv = d / f"{l['id']}.mp4", d / f"{l['id']}.srt", d / "chapters.txt", d / "build_report.json", d / "preview.html"
    for p in (mp4, srt, ch, rep):
        if not p.exists():
            probs.append(f"thiếu {p.name}")
    dur = None
    if mp4.exists():
        j, err = ffprobe(mp4)
        if j is None:
            probs.append(f"ffprobe lỗi: {err}")
        else:
            dur = float(j["format"]["duration"])
            st = j["streams"]
            v = [s for s in st if s.get("codec_type") == "video"]
            a = [s for s in st if s.get("codec_type") == "audio"]
            if not (v and v[0].get("codec_name") == "h264" and v[0].get("width") == 1920 and v[0].get("height") == 1080):
                probs.append("luồng hình không phải h264 1920x1080")
            if not (a and a[0].get("codec_name") == "aac"):
                probs.append("không có tiếng aac")
        if decode:
            rc, err = decode_errors(mp4)
            if rc or err:
                probs.append(f"giải mã lỗi rc={rc}: {err[:120]}")
            info["decoded"] = not (rc or err)
    info["dur"] = dur
    if rep.exists():
        b = json.loads(rep.read_text(encoding="utf-8"))
        if b.get("spec_sha256") != lv.spec_digest(spec):
            probs.append("STALE: đặc tả đổi sau lần dựng")
        tl = b.get("timeline_seconds")
        if dur is not None and tl is not None and abs(dur - tl) > 0.5:
            probs.append(f"độ dài {dur:.2f}s lệch timeline {tl:.2f}s")
    if srt.exists():
        info["cues"], ps = srt_problems(srt, dur)
        probs += ps
    if ch.exists():
        info["chapters"], ps = chapter_problems(ch, dur)
        probs += ps
    if not pv.exists():
        probs.append("thiếu preview.html")
    elif pv.read_text(encoding="utf-8") != preview_expected(spec):
        probs.append("preview.html cũ (khác bản sinh từ đặc tả hiện tại)")
    return info | {"probs": probs}


def cmd_list(cur):
    for k, items in all_items(cur).items():
        by = defaultdict(list)
        for C, l in items:
            by[C].append(l["id"])
        print(f"{k}: {len(items)} bài · " + " → ".join(f"{C} ({len(v)}: {v[0]}–{v[-1]})" for C, v in by.items()))
        print("   " + " ".join(f"{C}:{l['id']}" for C, l in items))


def cmd_check(cur, decode, tsv):
    seen, rows, bad = set(), [], 0
    for k, items in all_items(cur).items():
        for C, l in items:
            if (C, l["id"]) in seen:
                continue
            seen.add((C, l["id"]))
            r = check_one(C, l, decode)
            rows.append(r)
            if r["probs"]:
                bad += 1
                print(f"✗ {C} {l['id']}: " + " | ".join(r["probs"]))
    tot = sum(r.get("dur") or 0 for r in rows)
    print(f"# {len(rows)} bài · có vấn đề {bad} · tổng {tot / 60:.1f} phút" + (f" · giải mã trọn {sum(1 for r in rows if r.get('decoded'))}" if decode else ""))
    if tsv:
        Path(tsv).write_text("course\tlesson\tdur\tcues\tchapters\tdecoded\tproblems\n" + "".join(
            f"{r['C']}\t{r['id']}\t{r.get('dur')}\t{r.get('cues')}\t{r.get('chapters')}\t{r.get('decoded')}\t{' | '.join(r['probs'])}\n"
            for r in rows), encoding="utf-8")
    return 1 if bad else 0


def cmd_preview(cur):
    n = 0
    for k, items in all_items(cur).items():
        for C, l in items:
            spec = spec_of(l)
            pv = odir(C, l) / "preview.html"
            want = preview_expected(spec)
            if not pv.exists() or pv.read_text(encoding="utf-8") != want:
                pv.write_text(want, encoding="utf-8")
                n += 1
                print(f"↻ {C} {l['id']}")
    print(f"# sinh lại {n} preview.html")
    return 0


# ───────────────────────── trang hướng dẫn học ─────────────────────────
INTRO = {
    "P": ("Cho người chưa từng lập trình, muốn làm kỹ sư backend/tích hợp ở ngân hàng. Học Java từ con số 0 (JVA), "
          "rồi nền tảng backend ngân hàng (BNK), ôn phỏng vấn (INT), cuối cùng là các tình huống tích hợp (ACB)."),
    "N": ("Nền chung cho mọi nghề khoa học máy tính: toán rời rạc (DMS), thuật toán (CS112), rồi toán cho học máy "
          "(CS115 bài 0–21 và bài 44 thống kê, học ngay sau bài 21). Thứ tự đã được máy kiểm theo mọi tiên quyết."),
}
COURSE_NAME = {}


def mmss(s):
    s = int(round(s))
    return f"{s // 60}:{s % 60:02d}"


def rel(p):
    return p.relative_to(ROOT).as_posix()


def build_page(cur):
    data, md = [], []
    for k, items in all_items(cur).items():
        name = PATHS[k][0]
        rows = []
        for i, (C, l) in enumerate(items, 1):
            d = odir(C, l)
            mp4 = d / f"{l['id']}.mp4"
            j, _ = ffprobe(mp4)
            dur = float(j["format"]["duration"]) if j else 0.0
            chaps = (d / "chapters.txt").read_text(encoding="utf-8").splitlines() if (d / "chapters.txt").exists() else []
            rows.append({"n": i, "C": C, "id": l["id"], "title": l["title"], "dur": dur,
                         "obj": [str(o) for o in (l.get("objectives") or [])],
                         "mp4": rel(mp4), "srt": rel(d / f"{l['id']}.srt"), "pv": rel(d / "preview.html"), "xem": rel(d / "xem.html"),
                         "ch": [c for c in chaps if c.strip()],
                         "course": cur[C].get("title") or ""})
        data.append({"k": k, "name": name, "intro": INTRO[k], "rows": rows})
    return data


def page_html(data):
    esc = html.escape
    parts = []
    for p in data:
        tot = sum(r["dur"] for r in p["rows"])
        trs = []
        prevC = None
        for r in p["rows"]:
            if r["C"] != prevC:
                trs.append(f'<tr class="course"><td colspan="4">Khoá {esc(r["C"])}</td></tr>')
                prevC = r["C"]
            uid = f'{r["C"]}:{r["id"]}'
            obj = "".join(f"<li>{esc(o)}</li>" for o in r["obj"])
            ch = "".join(f"<li>{esc(c)}</li>" for c in r["ch"])
            trs.append(
                f'<tr data-uid="{esc(uid)}"><td class="n"><label><input type="checkbox" data-uid="{esc(uid)}"> {r["n"]}</label></td>'
                f'<td><div class="t"><b>{esc(r["C"])} {esc(r["id"])}</b> · {esc(r["title"])}</div>'
                f'<details><summary>Mục tiêu bài (giáo án) và mục lục video</summary><p class="h">Học xong bạn làm được:</p><ul>{obj}</ul>'
                f'<p class="h">Mục lục video (mốc phút:giây):</p><ul class="ch">{ch}</ul></details></td>'
                f'<td class="d">{mmss(r["dur"])}</td>'
                f'<td class="l"><a href="{esc(r["xem"])}">▶ xem bài</a> <a href="{esc(r["mp4"])}">tệp video</a> <a href="{esc(r["pv"])}">duyệt nhanh</a></td></tr>')
        parts.append(
            f'<section id="{p["k"]}"><h2>{esc(p["name"])}</h2><p>{esc(p["intro"])}</p>'
            f'<p class="sum">{len(p["rows"])} bài · tổng {tot / 3600:.1f} giờ video · <span class="prog" data-k="{p["k"]}"></span></p>'
            f'<table><thead><tr><th>Đã học</th><th>Bài</th><th>Thời lượng</th><th>Mở</th></tr></thead><tbody>{"".join(trs)}</tbody></table></section>')
    return f"""<!doctype html>
<html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Bắt đầu học</title>
<style>
:root {{ --bg:#fbfaf7; --fg:#1d1d1b; --mute:#5c5a55; --line:#e2dfd8; --acc:#1f5fa8; --row:#f2efe8; }}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ --bg:#16171a; --fg:#e8e6e1; --mute:#a5a29b; --line:#33353a; --acc:#7fb0ec; --row:#202227; }} }}
:root[data-theme="dark"] {{ --bg:#16171a; --fg:#e8e6e1; --mute:#a5a29b; --line:#33353a; --acc:#7fb0ec; --row:#202227; }}
body {{ background:var(--bg); color:var(--fg); font:16px/1.55 system-ui, "Segoe UI", sans-serif; margin:0; padding:0 16px 48px; }}
main {{ max-width:1000px; margin:0 auto; }}
h1 {{ font-size:1.7rem; margin:28px 0 4px; }} h2 {{ margin-top:36px; font-size:1.3rem; }}
a {{ color:var(--acc); }} .mute, .sum {{ color:var(--mute); }}
.how {{ border:1px solid var(--line); border-radius:8px; padding:12px 16px; }} .how li {{ margin:4px 0; }}
nav a {{ margin-right:16px; }}
table {{ width:100%; border-collapse:collapse; }} th, td {{ text-align:left; vertical-align:top; padding:8px 6px; border-bottom:1px solid var(--line); }}
tr.course td {{ background:var(--row); font-weight:600; }} tr.done .t {{ color:var(--mute); text-decoration:line-through; }}
td.n {{ white-space:nowrap; width:4.5em; }} td.d {{ white-space:nowrap; width:5em; font-variant-numeric:tabular-nums; }}
td.l {{ width:13em; }} td.l a {{ display:inline-block; margin:0 8px 4px 0; }}
details summary {{ cursor:pointer; color:var(--mute); font-size:.92rem; }} .h {{ margin:6px 0 0; font-weight:600; font-size:.92rem; }}
details ul {{ margin:4px 0; padding-left:20px; font-size:.92rem; }}
@media (max-width:640px) {{ thead {{ display:none; }} tr {{ display:block; }} td {{ display:block; border:0; padding:4px 0; width:auto !important; }}
  tbody tr {{ border-bottom:1px solid var(--line); padding:8px 0; }} }}
</style></head>
<body><main>
<h1>Bắt đầu học</h1>
<p class="mute">Trang này sinh tự động bằng <code>audit/review/learn_start/pack.py page</code> từ giáo án và video thật. Mở bằng trình duyệt, không cần mạng.</p>
<div class="how"><b>Cách học mỗi bài</b><ol>
<li>Đọc phần <i>Mục tiêu bài</i> trước để biết học xong phải làm được gì.</li>
<li>Bấm <i>▶ xem bài</i>: trang xem có mục lục bấm được để nhảy tới đoạn cần xem, chỉnh tốc độ, và nút sang bài sau. Phụ đề đã in sẵn trên hình.</li>
<li>Khi video đặt câu hỏi, hãy tạm dừng (phím cách), tự trả lời ra giấy rồi mới xem tiếp.</li>
<li>Làm lại bằng giấy bút ví dụ có số trong bài. Bài có mã thì gõ lại mã và chạy thử.</li>
<li>Ôn nhanh không cần nghe: mở <i>duyệt nhanh</i> và lật từng khung bằng phím ← →.</li>
<li>Tick ô "Đã học" khi tự làm lại được mọi mục tiêu bài. Dấu tick chỉ lưu trong trình duyệt này.</li></ol></div>
<nav><p><a href="#P">Lộ trình phỏng vấn backend ngân hàng</a><a href="#N">Lộ trình nền tảng khoa học máy tính</a></p></nav>
<p class="mute">Hai lộ trình độc lập; có thể học song song. Người chưa từng lập trình nên bắt đầu ở lộ trình phỏng vấn, bài JVA L00. Người muốn nền toán vững thì bắt đầu ở DMS L00.</p>
{"".join(parts)}
</main>
<script>
(function () {{
  var KEY = "hoc_tap_done_v1", done = {{}};
  try {{ done = JSON.parse(localStorage.getItem(KEY) || "{{}}") || {{}}; }} catch (e) {{ done = {{}}; }}
  function save() {{ try {{ localStorage.setItem(KEY, JSON.stringify(done)); }} catch (e) {{}} }}
  function paint() {{
    document.querySelectorAll("section").forEach(function (s) {{
      var boxes = s.querySelectorAll("input[type=checkbox]"), n = 0;
      boxes.forEach(function (b) {{ var on = !!done[b.dataset.uid]; b.checked = on; b.closest("tr").classList.toggle("done", on); if (on) n++; }});
      var p = s.querySelector(".prog"); if (p) p.textContent = "đã học " + n + "/" + boxes.length;
    }});
  }}
  document.addEventListener("change", function (e) {{
    var b = e.target; if (!b.dataset || !b.dataset.uid) return;
    if (b.checked) done[b.dataset.uid] = 1; else delete done[b.dataset.uid];
    save(); paint();
  }});
  paint();
}})();
</script>
</body></html>
"""


def page_md(data):
    md = ["# Bắt đầu học (SINH TỰ ĐỘNG bằng `audit/review/learn_start/pack.py page`, không sửa tay)", "",
          "Mở **[HOC_TAP.html](HOC_TAP.html)** trong trình duyệt để có danh sách bấm được và ô đánh dấu đã học.", ""]
    for p in data:
        tot = sum(r["dur"] for r in p["rows"])
        md += [f"## {p['name']}", "", p["intro"], "", f"{len(p['rows'])} bài · {tot / 3600:.1f} giờ video", "",
               "| # | Bài | Thời lượng | Video |", "|---:|---|---:|---|"]
        md += [f"| {r['n']} | {r['C']} {r['id']} · {r['title'].replace('|', '/')} | {mmss(r['dur'])} | [{r['mp4']}]({r['mp4']}) |" for r in p["rows"]]
        md.append("")
    return "\n".join(md)


def check_links(text, base=ROOT):
    hrefs = [h.split("#")[0] for h in re.findall(r'(?:href|src)="([^"#][^"]*)"', text)]
    dead = [h for h in hrefs if not (base / html.unescape(h)).resolve().exists()]
    return len(hrefs), dead


def watch_html(r, prev, nxt, k, pname):
    esc = html.escape
    up = "../../../"

    def link(x, label):
        if not x:
            return f'<span class="mute">{label}: không có</span>'
        return f'<a href="../../{esc(x["C"])}/{esc(x["id"])}/xem.html">{label}: {esc(x["C"])} {esc(x["id"])}</a>'
    chs = []
    for c in r["ch"]:
        m = re.match(r"(\d+):(\d\d)(?::(\d\d))? (.+)$", c)
        if not m:
            continue
        t = int(m.group(1)) * 60 + int(m.group(2)) if m.group(3) is None else int(m.group(1)) * 3600 + int(m.group(2)) * 60 + int(m.group(3))
        chs.append(f'<li><button data-t="{t}">{esc(c.split(" ", 1)[0])}</button> {esc(m.group(4))}</li>')
    obj = "".join(f"<li>{esc(o)}</li>" for o in r["obj"])
    return f"""<!doctype html>
<html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(r["C"])} {esc(r["id"])}</title>
<style>
:root {{ --bg:#fbfaf7; --fg:#1d1d1b; --mute:#5c5a55; --line:#e2dfd8; --acc:#1f5fa8; --btn:#ece8df; }}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ --bg:#16171a; --fg:#e8e6e1; --mute:#a5a29b; --line:#33353a; --acc:#7fb0ec; --btn:#2a2c31; }} }}
:root[data-theme="dark"] {{ --bg:#16171a; --fg:#e8e6e1; --mute:#a5a29b; --line:#33353a; --acc:#7fb0ec; --btn:#2a2c31; }}
body {{ background:var(--bg); color:var(--fg); font:16px/1.5 system-ui, "Segoe UI", sans-serif; margin:0; padding:0 16px 40px; }}
main {{ max-width:1100px; margin:0 auto; }} a {{ color:var(--acc); }} .mute {{ color:var(--mute); }}
h1 {{ font-size:1.3rem; margin:16px 0 8px; }} h2 {{ font-size:1.05rem; }} video {{ width:100%; background:#000; border-radius:6px; }}
.bar {{ display:flex; flex-wrap:wrap; gap:8px 16px; align-items:center; margin:8px 0; }}
button {{ background:var(--btn); color:var(--fg); border:1px solid var(--line); border-radius:6px; padding:4px 10px; font:inherit; cursor:pointer; }}
button.on {{ outline:2px solid var(--acc); }} .cols {{ display:grid; grid-template-columns:1fr 1fr; gap:24px; }}
ul {{ padding-left:20px; }} ul.ch {{ list-style:none; padding:0; }} ul.ch li {{ margin:4px 0; }} ul.ch li.cur {{ font-weight:600; }}
@media (max-width:720px) {{ .cols {{ grid-template-columns:1fr; }} }}
</style></head>
<body><main>
<p class="bar"><a href="{up}HOC_TAP.html#{k}">← {esc(pname)}</a> {link(prev, "Bài trước")} {link(nxt, "Bài sau")}</p>
<h1>{esc(r["C"])} {esc(r["id"])} · {esc(r["title"])}</h1>
<video id="v" controls preload="metadata" src="{esc(r["id"])}.mp4"></video>
<p class="bar">Tốc độ: <button data-r="0.75">0,75×</button><button data-r="1" class="on">1×</button><button data-r="1.25">1,25×</button><button data-r="1.5">1,5×</button>
<span class="mute">Phím cách: dừng/chạy · ← →: lùi/tiến 5 giây</span></p>
<div class="cols"><section><h2>Mục lục (bấm để nhảy tới)</h2><ul class="ch">{"".join(chs)}</ul></section>
<section><h2>Học xong bạn làm được</h2><ul>{obj}</ul>
<p class="mute">Thời lượng {mmss(r["dur"])} · <a href="preview.html">duyệt nhanh từng khung</a> · <a href="{esc(r["id"])}.srt">phụ đề .srt</a></p></section></div>
</main>
<script>
(function () {{
  var v = document.getElementById("v");
  document.querySelectorAll("button[data-t]").forEach(function (b) {{
    b.addEventListener("click", function () {{ v.currentTime = +b.dataset.t; v.play(); }});
  }});
  document.querySelectorAll("button[data-r]").forEach(function (b) {{
    b.addEventListener("click", function () {{
      v.playbackRate = +b.dataset.r;
      document.querySelectorAll("button[data-r]").forEach(function (x) {{ x.classList.toggle("on", x === b); }});
    }});
  }});
  var items = Array.prototype.slice.call(document.querySelectorAll("ul.ch li"));
  v.addEventListener("timeupdate", function () {{
    var cur = -1;
    items.forEach(function (li, i) {{ if (+li.querySelector("button").dataset.t <= v.currentTime + 0.25) cur = i; }});
    items.forEach(function (li, i) {{ li.classList.toggle("cur", i === cur); }});
  }});
  document.addEventListener("keydown", function (e) {{
    if (e.target.tagName === "BUTTON" || e.target === v) return;
    if (e.key === " ") {{ e.preventDefault(); v.paused ? v.play() : v.pause(); }}
    else if (e.key === "ArrowRight") v.currentTime += 5;
    else if (e.key === "ArrowLeft") v.currentTime = Math.max(0, v.currentTime - 5);
  }});
}})();
</script>
</body></html>
"""


def cmd_page(cur):
    data = build_page(cur)
    h = page_html(data)
    (ROOT / "HOC_TAP.html").write_text(h, encoding="utf-8")
    (ROOT / "HOC_TAP.md").write_text(page_md(data), encoding="utf-8")
    uids = [(r["C"], r["id"]) for p in data for r in p["rows"]]
    assert len(uids) == len(set(uids)), "một bài nằm ở hai lộ trình: nút bài trước/sau sẽ mơ hồ"
    wn, wdead, pages = 0, [], []
    for p in data:
        rows = p["rows"]
        for i, r in enumerate(rows):
            w = watch_html(r, rows[i - 1] if i else None, rows[i + 1] if i + 1 < len(rows) else None, p["k"], p["name"])
            f = ROOT / r["xem"]
            f.write_text(w, encoding="utf-8")
            pages.append((r, w, f))
    for r, w, f in pages:            # kiểm sau khi đã ghi đủ mọi trang
        c, dd = check_links(w, f.parent)
        wn += c
        wdead += [f"{r['xem']} → {x}" for x in dd]
    print(f"xem.html: {len(uids)} trang, {wn} liên kết, chết {len(wdead)}")
    n, dead = check_links(h)
    dead += wdead
    mdl = re.findall(r"\]\(([^)#]+)\)", (ROOT / "HOC_TAP.md").read_text(encoding="utf-8"))
    mdead = [x for x in mdl if not (ROOT / x).exists()]
    print(f"HOC_TAP.html: {sum(len(p['rows']) for p in data)} bài, {n} liên kết, chết {len(dead)}; HOC_TAP.md: {len(mdl)} liên kết, chết {len(mdead)}")
    for x in dead + mdead:
        print("  chết:", x)
    return 1 if dead or mdead else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["list", "check", "preview", "page"])
    ap.add_argument("--decode", action="store_true")
    ap.add_argument("--tsv")
    a = ap.parse_args()
    cur = load_cur()
    if a.cmd == "list":
        return cmd_list(cur)
    if a.cmd == "check":
        return cmd_check(cur, a.decode, a.tsv)
    if a.cmd == "preview":
        return cmd_preview(cur)
    return cmd_page(cur)


if __name__ == "__main__":
    sys.exit(main() or 0)
