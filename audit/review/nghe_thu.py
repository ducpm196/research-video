"""Sinh trang NGHE_THU.html để tai người nghe thử mẫu âm thanh TTS đại diện theo từng chặng (đóng BN-07).

Mỗi chặng lấy 15 câu mẫu (lưu ở out/_cache/tts/*.wav):
  - 5 câu có độ khớp ASR thấp nhất (ưu tiên trải đều các khoá/bài);
  - 5 câu có từ ngoại / lexicon / chữ cái (both_missed khác rỗng);
  - 5 câu có số liệu / phép tính / ký hiệu đọc thành lời.
Mọi đường dẫn .wav và xem.html được kiểm tồn tại thật trên đĩa trước khi ghi.

Dùng:
  .venv/Scripts/python -B audit/review/nghe_thu.py [--stages S01 S02 S03 S04 S05]
"""
import argparse
import datetime
import html
import io
import json
import re
import sys
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "audit" / "review" / "learn_start"))
sys.stdout.reconfigure(encoding="utf-8")

import lv  # noqa: E402
import pack  # noqa: E402

NUM_RX = re.compile(r"\d|phẩy|bình phương|lập phương|giai thừa|phần trăm|triệu|nghìn|tỉ|mũ", re.I)


def collect_stage_items(stage_key, name, items):
    candidates = []
    for C, l in items:
        lid = l["id"]
        od = ROOT / "out" / C / lid
        aj = od / "asr_report.json"
        if not aj.exists():
            continue
        sp = pack.spec_of(l)
        if not sp:
            continue
        with redirect_stdout(io.StringIO()):
            frames = lv.build_frames(sp)
        recs = json.loads(aj.read_text(encoding="utf-8"))
        by_frame = {int(r["frame"]): r for r in recs if "frame" in r}
        for idx, fr in enumerate(frames):
            wav = lv.tts_key(fr)
            if not wav.exists():
                continue
            r = by_frame.get(idx)
            if not r:
                continue
            candidates.append({
                "stage": stage_key,
                "course": C,
                "lid": lid,
                "title": l.get("title") or lid,
                "frame": idx,
                "ratio": float(r.get("ratio", 1.0)),
                "caption": str(r.get("caption") or fr.get("caption") or ""),
                "heard": str(r.get("heard") or ""),
                "both_missed": list(r.get("both_missed") or []),
                "both_missed_other": list(r.get("both_missed_other") or []),
                "reviewed": str(r.get("reviewed") or ""),
                "wav": wav.relative_to(ROOT).as_posix(),
                "xem": f"out/{C}/{lid}/xem.html",
            })
    return candidates


def pick_diverse(pool, sort_key, limit, seen):
    picked = []
    used_lessons = set()
    ordered = sorted(pool, key=sort_key)
    # Ưu tiên mỗi bài tối đa 1 câu trước để trải đều toàn chặng
    for it in ordered:
        k = (it["course"], it["lid"], it["frame"])
        lk = (it["course"], it["lid"])
        if k in seen or lk in used_lessons:
            continue
        seen.add(k)
        used_lessons.add(lk)
        picked.append(it)
        if len(picked) >= limit:
            return picked
    for it in ordered:
        k = (it["course"], it["lid"], it["frame"])
        if k in seen:
            continue
        seen.add(k)
        picked.append(it)
        if len(picked) >= limit:
            return picked
    return picked


def sample_stage(cands):
    seen = set()
    low = pick_diverse(cands, lambda x: (x["ratio"], x["course"], x["lid"], x["frame"]), 5, seen)
    for x in low:
        x["bucket"] = "Độ khớp ASR thấp nhất"
    lex_pool = [x for x in cands if x["both_missed"]]
    lex = pick_diverse(lex_pool, lambda x: (x["ratio"], -len(x["both_missed"]), x["course"], x["lid"], x["frame"]), 5, seen)
    for x in lex:
        x["bucket"] = "Tên riêng / từ ngoại / lexicon"
    num_pool = [x for x in cands if NUM_RX.search(x["caption"])]
    num = pick_diverse(num_pool, lambda x: (x["ratio"], x["course"], x["lid"], x["frame"]), 5, seen)
    for x in num:
        x["bucket"] = "Số liệu / phép tính / ký hiệu"
    extra = pick_diverse(cands, lambda x: (x["ratio"], x["course"], x["lid"], x["frame"]), max(0, 15 - (len(low) + len(lex) + len(num))), seen)
    for x in extra:
        x["bucket"] = "Mẫu bổ sung"
    return low + lex + num + extra


def render_html(sections, now):
    esc = html.escape
    cards = []
    tot_clips = sum(len(s["samples"]) for s in sections)
    for sec in sections:
        rows = []
        for i, it in enumerate(sec["samples"], 1):
            uid = f"{it['course']}:{it['lid']}:{it['frame']}"
            missed = ", ".join(it["both_missed"] or it["both_missed_other"] or ["—"])
            rows.append(
                f'<tr data-id="{esc(uid)}">'
                f'<td class="num">{i}</td>'
                f'<td><span class="badge">{esc(it["course"])} {esc(it["lid"])}</span> #{it["frame"]}<br>'
                f'<small class="mute">{esc(it["bucket"])}</small><br>'
                f'<a href="{esc(it["xem"])}" target="_blank">Mở xem.html</a></td>'
                f'<td><audio controls preload="none" src="{esc(it["wav"])}"></audio>'
                f'<div class="ratio">ASR khớp: <b>{it["ratio"]:.3f}</b> · Từ lệch: <code>{esc(missed)}</code></div></td>'
                f'<td><div><b>Đọc chuẩn:</b> {esc(it["caption"])}</div>'
                f'<div class="heard"><b>ASR nghe:</b> {esc(it["heard"])}</div></td>'
                f'<td><select class="verdict" data-id="{esc(uid)}">'
                f'<option value="">Chưa nghe</option>'
                f'<option value="ok">Đạt — nghe rõ</option>'
                f'<option value="warn">Tạm — hơi gượng</option>'
                f'<option value="fix">Lỗi — cần sửa phát âm</option>'
                f'</select><input class="note" type="text" placeholder="Ghi chú tai nghe..." data-id="{esc(uid)}"></td>'
                f'</tr>'
            )
        cards.append(
            f'<section id="{esc(sec["key"])}"><h2>{esc(sec["name"])} '
            f'<small>({sec["n_lessons"]} bài đã dựng, {sec["n_clips"]} câu · lấy {len(sec["samples"])} mẫu)</small></h2>'
            f'<table><thead><tr><th>#</th><th>Bài / Khung</th><th>Âm thanh &amp; Độ khớp ASR</th><th>Câu gốc vs ASR nghe được</th><th>Kết luận tai người</th></tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table></section>'
        )

    return f"""<!doctype html>
<html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Nghe thử âm thanh TTS theo chặng (BN-07)</title>
<style>
  body{{font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;margin:0;padding:24px;background:#f8fafc;color:#0f172a;line-height:1.5}}
  header{{max-width:1280px;margin:0 auto 20px;background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:18px 22px}}
  h1{{margin:0 0 6px;font-size:1.35rem}} h2{{font-size:1.12rem;margin:24px 0 10px}}
  section{{max-width:1280px;margin:0 auto 28px;background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:16px 20px}}
  table{{width:100%;border-collapse:collapse;font-size:.92rem}} th,td{{border-top:1px solid #e2e8f0;padding:10px 8px;vertical-align:top;text-align:left}}
  th{{background:#f1f5f9;font-size:.82rem;text-transform:uppercase;letter-spacing:.03em;color:#475569}}
  audio{{width:250px;height:34px}} .mute{{color:#64748b;font-size:.8rem}} .heard{{color:#475569;margin-top:4px;font-size:.86rem}}
  .badge{{display:inline-block;background:#e0f2fe;color:#0369a1;font-weight:700;padding:1px 7px;border-radius:6px;font-size:.8rem}}
  .ratio{{font-size:.82rem;margin-top:4px;color:#334155}} select,input.note{{width:100%;box-sizing:border-box;padding:5px 7px;border:1px solid #cbd5e1;border-radius:6px;margin-bottom:5px;font-size:.85rem}}
  .bar{{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin-top:10px}} button{{background:#0f172a;color:#fff;border:0;border-radius:8px;padding:7px 14px;cursor:pointer;font-weight:600}}
</style></head><body>
<header>
  <h1>🎧 Bảng nghe thử âm thanh TTS bằng tai người (BN-07)</h1>
  <div>Sinh tự động từ <code>out/_cache/tts/*.wav</code> và <code>asr_report.json</code> lúc <code>{esc(now)}</code> · Tổng <b>{len(sections)}</b> chặng, <b>{tot_clips}</b> câu mẫu.</div>
  <div class="bar"><span id="stats">Đang tải trạng thái nghe...</span><button id="exp">Xuất JSON kết quả nghe</button></div>
</header>
{"".join(cards)}
<script>
const K="nghe_thu_v1";
const load=()=>{{try{{return JSON.parse(localStorage.getItem(K)||"{{}}");}}catch(e){{return {{}};}}}};
const save=d=>localStorage.setItem(K,JSON.stringify(d));
function upd(){{
  const d=load(), vs=document.querySelectorAll("select.verdict");
  let ok=0,warn=0,fix=0;
  vs.forEach(s=>{{const v=(d[s.dataset.id]||{{}}).v||""; if(v==="ok")ok++; else if(v==="warn")warn++; else if(v==="fix")fix++;}});
  document.getElementById("stats").textContent=`Đã nghe: ${{ok+warn+fix}}/${{vs.length}} · Đạt: ${{ok}} · Tạm: ${{warn}} · Cần sửa: ${{fix}}`;
}}
const st=load();
document.querySelectorAll("select.verdict").forEach(s=>{{
  if(st[s.dataset.id]) s.value=st[s.dataset.id].v||"";
  s.addEventListener("change",()=>{{const d=load(); d[s.dataset.id]=Object.assign(d[s.dataset.id]||{{}},{{v:s.value}}); save(d); upd();}});
}});
document.querySelectorAll("input.note").forEach(i=>{{
  if(st[i.dataset.id]) i.value=st[i.dataset.id].n||"";
  i.addEventListener("input",()=>{{const d=load(); d[i.dataset.id]=Object.assign(d[i.dataset.id]||{{}},{{n:i.value}}); save(d);}});
}});
document.getElementById("exp").addEventListener("click",()=>{{
  const b=new Blob([JSON.stringify(load(),null,2)],{{type:"application/json"}});
  const a=document.createElement("a"); a.href=URL.createObjectURL(b); a.download="nghe_thu_ket_qua.json"; a.click();
}});
upd();
</script></body></html>"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stages", nargs="*", default=["S01", "S02", "S03", "S04", "S05"])
    args = ap.parse_args()
    want = set(args.stages)
    cur = pack.load_cur()
    sections, dead = [], 0
    for k, name, _, _, items in pack.stages(cur):
        if k not in want:
            continue
        cands = collect_stage_items(k, name, items)
        if not cands:
            continue
        samples = sample_stage(cands)
        for it in samples:
            if not (ROOT / it["wav"]).is_file() or not (ROOT / it["xem"]).is_file():
                dead += 1
        sections.append({"key": k, "name": name, "n_lessons": len({(x["course"], x["lid"]) for x in cands}),
                         "n_clips": len(cands), "samples": samples})
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    out = ROOT / "NGHE_THU.html"
    out.write_text(render_html(sections, now), encoding="utf-8", newline="\n")
    tot = sum(len(s["samples"]) for s in sections)
    print(f"NGHE_THU.html: {len(sections)} chặng, {tot} câu mẫu, liên kết chết: {dead}")
    sys.exit(1 if dead else 0)


if __name__ == "__main__":
    main()
