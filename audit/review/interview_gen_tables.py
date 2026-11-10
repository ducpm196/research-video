"""(Chuyển từ scratchpad phiên 7f725234 vào kho 2026-11-10; chạy SAU interview_sync_video.py: .venv/Scripts/python audit/review/interview_gen_tables.py)
Fill the <!-- BEGIN:X --> ... <!-- END:X --> blocks of MASTER_CURRICULUM_INDEX.md with video tables measured now
(ffprobe duration, sha256 prefix, voice and digest-fresh state from build_report + lv.spec_digest)."""
import hashlib, json, re, subprocess, sys
from pathlib import Path
ROOT = Path("D:/research-video")
sys.path.insert(0, str(ROOT / "tools"))
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    import lv
INT = ["00_overview_roadmap", "01_foundation_cs_java", "02_backend_microservices", "03_distributed_systems_senior",
       "04_banking_domain_t24_napas", "05_uit_ai_banking_multiplier", "06_interview_qa_bank_100", "07_salary_negotiation_50m_gross"]
F = "file:///D:/research-video/"
def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                                capture_output=True, text=True).stdout)
def info(course, L):
    o = ROOT / "out" / course / L
    spec = next((ROOT / "lessons" / course.lower()).glob(f"{L}_*.yaml"))
    br = json.loads((o / "build_report.json").read_text(encoding="utf-8"))
    fresh = br.get("spec_sha256") == lv.spec_digest(lv.load_spec(spec))
    t = dur(o / f"{L}.mp4")
    title = lv.load_spec(spec)["title"]
    title = re.sub(r"^(Bài \d+|Chuyên đề \d+)\s*[—-]\s*", "", title)
    voice = ",".join(v.replace("vi-VN-", "").replace("Neural", "") for v in br.get("voices", []))
    h = hashlib.sha256((o / f"{L}.mp4").read_bytes()).hexdigest()[:12]
    return spec, t, title, voice, h, fresh, br.get("built_at", "?")
def mmss(t): return f"{int(t // 60)}:{int(round(t % 60)):02d}"
blocks, totals = {}, {}
rows = ["| Mã bài | Giáo án | Đặc tả (YAML) | Video | Phụ đề | Chapters | Thời lượng | Giọng | Đặc tả khớp video | sha256 (12) |",
        "|:---:|:---|:---|:---|:---|:---|:---:|:---:|:---:|:---|"]
tot = 0
for i, n in enumerate(INT):
    L = f"L{i:02d}"; spec, t, title, voice, h, fresh, _ = info("INT", L); tot += t
    rows.append(f"| **`INT:{L}`** | [`{n}.md`]({F}interview/{n}.md) | [`{spec.name}`]({F}lessons/int/{spec.name}) | "
                f"[`{n}.mp4`]({F}interview/video/{n}.mp4) | [`.srt`]({F}interview/video/{n}.srt) | [`chapters`]({F}interview/video/{n}_chapters.txt) | "
                f"{mmss(t)} | {voice} | {'có' if fresh else 'KHÔNG'} | `{h}` |")
blocks["INT"] = rows; totals["INT"] = tot
rows = ["| Mã bài | Chuyên đề | Đặc tả (YAML) | Video | Phụ đề | Chapters | Thời lượng | Giọng | Đặc tả khớp video | sha256 (12) |",
        "|:---:|:---|:---|:---|:---|:---|:---:|:---:|:---:|:---|"]
tot = 0
for i in range(9):
    L = f"L{i:02d}"; spec, t, title, voice, h, fresh, _ = info("ACB", L); tot += t
    ch = "chapters.txt" if i == 0 else f"chapters_{L}.txt"
    rows.append(f"| **`ACB:{L}`** | {title} | [`{spec.name}`]({F}lessons/acb/{spec.name}) | [`{L}.mp4`]({F}interview/video/{L}.mp4) | "
                f"[`.srt`]({F}interview/video/{L}.srt) | [`chapters`]({F}interview/video/{ch}) | {mmss(t)} | {voice} | {'có' if fresh else 'KHÔNG'} | `{h}` |")
blocks["ACB"] = rows; totals["ACB"] = tot
rows = ["| Mã bài | Bài học | Đặc tả (YAML) | Video | Phụ đề | Chapters | Thời lượng | Giọng | Đặc tả khớp video | sha256 (12) |",
        "|:---:|:---|:---|:---|:---|:---|:---:|:---:|:---:|:---|"]
tot = 0
for i in range(15):
    L = f"L{i:02d}"; spec, t, title, voice, h, fresh, _ = info("BNK", L); tot += t
    rows.append(f"| **`BNK:{L}`** | {title} | [`{spec.name}`]({F}lessons/bnk/{spec.name}) | [`{L}.mp4`]({F}out/BNK/{L}/{L}.mp4) | "
                f"[`.srt`]({F}out/BNK/{L}/{L}.srt) | [`chapters`]({F}out/BNK/{L}/chapters.txt) | {mmss(t)} | {voice} | {'có' if fresh else 'KHÔNG'} | `{h}` |")
blocks["BNK"] = rows; totals["BNK"] = tot
rows = ["| Mã bài | Bài học | Đặc tả (YAML) | Video | Phụ đề | Chapters | Thời lượng | Giọng | Đặc tả khớp video | sha256 (12) |",
        "|:---:|:---|:---|:---|:---|:---|:---:|:---:|:---:|:---|"]
tot = 0
for i in range(13):
    L = f"L{i:02d}"; spec, t, title, voice, h, fresh, _ = info("JVA", L); tot += t
    rows.append(f"| **`JVA:{L}`** | {title} | [`{spec.name}`]({F}lessons/jva/{spec.name}) | [`{L}.mp4`]({F}out/JVA/{L}/{L}.mp4) | "
                f"[`.srt`]({F}out/JVA/{L}/{L}.srt) | [`chapters`]({F}out/JVA/{L}/chapters.txt) | {mmss(t)} | {voice} | {'có' if fresh else 'KHÔNG'} | `{h}` |")
blocks["JVA"] = rows; totals["JVA"] = tot
p = ROOT / "interview/MASTER_CURRICULUM_INDEX.md"
s = p.read_text(encoding="utf-8")
for k, r in blocks.items():
    body = "\n".join(r) + f"\n\n*Tổng {k}: **{totals[k] / 60:.2f} phút** ({len(r) - 2} video, ffprobe).*"
    s, n = re.subn(rf"(<!-- BEGIN:{k} -->).*?(<!-- END:{k} -->)", lambda m: m.group(1) + "\n" + body + "\n" + m.group(2), s, flags=re.S)
    assert n == 1, k
p.write_text(s, encoding="utf-8")
print({k: round(v / 60, 2) for k, v in totals.items()}, "sum", round(sum(totals.values()) / 60, 2))
