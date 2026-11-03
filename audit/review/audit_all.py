"""Rà soát toàn kho, trong một tiến trình (nhanh hơn audit_built.py, và xét video lỗi thời bằng DẤU BĂM như `verify`, không bằng
giờ sửa file — sửa asr_reviewed làm đổi giờ sửa nhưng không làm video lỗi thời). Với mỗi bài: lint theo bộ luật hiện hành;
nếu đã dựng: spec_sha256 / tts_sha256 trong build_report có khớp đặc tả hiện tại không (STALE), giọng (đúng một giọng),
câu ASR gắn cờ chưa xem xét (tính lại từ asr_report.md và asr_reviewed hiện tại), asr_report có lỗi thời so với lời đọc không.
Chạy: .venv/Scripts/python audit/review/audit_all.py [khoá …] → audit/review/audit_all.tsv"""
import io
import json
import re
import sys
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import lv  # noqa: E402

courses = [c.lower() for c in sys.argv[1:]] or sorted(p.name for p in (ROOT / "lessons").iterdir() if p.is_dir())
rows, bad = [], 0
for c in courses:
    for f in sorted((ROOT / "lessons" / c).glob("L*_*.yaml")):
        lid = f.name.split("_")[0]
        spec = lv.load_spec(f)
        with redirect_stdout(io.StringIO()):
            r = lv.lint(spec, quiet=True)
        probs = [f"FAIL {e}" for e in r.errors] + [f"WARN {w}" for w in r.warnings]
        od = ROOT / "out" / c.upper() / lid
        rep = od / "build_report.json"
        state = "chưa dựng"
        if rep.exists():
            b = json.loads(rep.read_text(encoding="utf-8"))
            state = "đã dựng"
            v = b.get("voices") or []
            if b.get("spec_sha256") != lv.spec_digest(spec):
                probs.append("STALE đặc tả đổi sau lần dựng")
            else:
                with redirect_stdout(io.StringIO()):
                    frames = lv.build_frames(spec)
                if b.get("tts_sha256") != lv.tts_digest(frames):
                    probs.append("STALE lời đọc/lexicon đổi sau lần dựng")
                elif not v:
                    # bản dựng trước khi build_report ghi `voices`: tts_sha256 băm cả giọng của TỪNG câu, nên khớp dấu băm
                    # nghĩa là audio đã dựng đúng bằng các giọng trong khung hiện tại
                    v = sorted({fr["voice"] for fr in frames})
            if len(v) != 1:
                probs.append(f"giọng: {v}")
            # âm thanh cụt đuôi trong cache của bài (lỗi thật AIF L08, CSA L11, DBS L15 — 2026-10-30; ngưỡng ở lv.tts_truncated)
            with redirect_stdout(io.StringIO()):
                cut = [i for i, fr in enumerate(lv.build_frames(spec)) if lv.tts_key(fr).exists() and lv.tts_truncated(fr, lv.tts_key(fr))]
            if cut:
                probs.append(f"âm thanh cụt ở khung {cut[:5]} — dựng lại (build đọc lại câu cụt)")
            md = od / "asr_report.md"
            if not md.exists():
                probs.append("chưa có asr_report")
            else:
                said = {s.strip() for sc in spec["scenes"] for st in sc["steps"] for s in lv.sentences(st.get("say", ""))}
                done = {str(x["sentence"]).strip() for x in spec.get("asr_reviewed") or []}
                heard, unrev = set(), []
                for line in md.read_text(encoding="utf-8").split("## Tham khảo")[0].splitlines():
                    cells = [x.strip() for x in line.strip().strip("|").split("|")]
                    if len(cells) == 8 and cells[0].isdigit():
                        heard.add(cells[2])
                        if cells[2] in said and cells[2] not in done:
                            unrev.append(cells[2])
                gone = [s for s in heard if s not in said]
                if unrev:
                    probs.append(f"ASR chưa xem xét {len(unrev)}: {unrev[0][:60]}")
                if gone and not any(p.startswith("STALE") for p in probs):
                    probs.append(f"asr_report lỗi thời ({len(gone)} câu không còn trong bài) — chạy lại asr")
                # báo cáo ghi “chưa xem xét” khác số tính lại (đã thêm asr_reviewed sau lần chạy asr) → tài liệu nói sai hiện trạng
                m = re.search(r"chưa xem xét: (\d+)", md.read_text(encoding="utf-8"))
                if m and int(m.group(1)) != len(unrev) and not unrev:
                    probs.append(f"asr_report ghi chưa xem xét {m.group(1)} nhưng đặc tả đã xem xét đủ — chạy lại asr để báo cáo khớp")
        bad += bool(probs)
        rows.append((c.upper(), lid, state, " | ".join(probs)))
        if probs:
            print(c.upper(), lid, state, "→", " | ".join(probs)[:300], flush=True)
# mẫu sinh bài (audit/<khoá>/src/*.tpl.yaml) phải khớp bài, nếu không lần chạy fill_all sau ghi đè bài (lỗi thật 2026-10-31, đợt đào sâu)
import subprocess  # noqa: E402
tp = subprocess.run([sys.executable, str(ROOT / "audit/review/sync_tpl_from_lesson.py"), *courses], capture_output=True, text=True,
                    encoding="utf-8", cwd=ROOT)
for line in tp.stdout.splitlines():
    if "LỆCH" in line or "thiếu hình" in line:
        c, lid = line.split()[0], line.split()[1].split("_")[0]
        bad += 1
        rows.append((c.upper(), lid, "mẫu", line))
        print(c.upper(), lid, "mẫu →", line, flush=True)
(ROOT / "audit" / "review" / "audit_all.tsv").write_text(
    "course\tid\tstate\tproblems\n" + "\n".join("\t".join(r) for r in rows), encoding="utf-8")
built = sum(r[2] == "đã dựng" for r in rows)
print(f"\naudit_all: {len(rows)} bài, {built} đã dựng, {bad} bài có vấn đề")
