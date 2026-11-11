"""Sinh các khối <!-- BEGIN:LF_* --> … <!-- END:LF_* --> của interview/MASTER_CURRICULUM_INDEX.md từ giáo án + video thật (đợt LF1, 2026-11-11).
Không gõ số tay: số bài, giờ video, bài có video đều đếm/đo lúc chạy (ffprobe qua pack.py).
  LF_STAGES : bảng 11 chặng của HOC_TAP.html (pack.stages) — cùng nguồn với trang học, nên hai nơi không thể lệch nhau.
  LF_TIERS  : bảng khoá của cấp AI, cấp chuyên gia và chuyên ngành mở rộng (tên khoá lấy từ dòng đầu curriculum/<khoá>.yaml).
  LF_BNX    : bảng bài khoá BNX (đặc tả, video, thời lượng, giọng, đặc tả khớp video) — bài chưa dựng ghi "đang soạn".
Chạy: .venv/Scripts/python -B audit/review/learn_full/master_sections.py"""
import io
import json
import re
import sys
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "audit" / "review" / "learn_start"))
sys.stdout.reconfigure(encoding="utf-8")
import pack  # noqa: E402

F = "file:///D:/research-video/"
MASTER = ROOT / "interview" / "MASTER_CURRICULUM_INDEX.md"


def dur(C, l):
    if not pack.has_video(C, l):
        return None
    j, _ = pack.ffprobe(pack.odir(C, l) / f"{l['id']}.mp4")
    return float(j["format"]["duration"]) if j else None


def course_name(C):
    first = (ROOT / "curriculum" / f"{C.lower()}.yaml").read_text(encoding="utf-8").splitlines()[0]
    m = re.search(r"—\s*[A-Z0-9]+\s*·\s*(.+)$", first) or re.search(r"·\s*(.+?)(\(|$)", first)
    return (m.group(1).strip() if m else C).rstrip(" (")


def main():
    cur = pack.load_cur()
    blocks = {}
    # 11 chặng
    rows = ["| Chặng | Cấp độ (MASTER / ROADMAP) | Khoá (số bài trong chặng) | Bài có video | Giờ video |", "|:---|:---|:---|:---:|:---:|"]
    tot_n = tot_s = 0
    for k, name, level, intro, items in pack.stages(cur):
        by, ds = {}, []
        for C, l in items:
            by[C] = by.get(C, 0) + 1
            ds.append(dur(C, l))
        ready = [d for d in ds if d is not None]
        tot_n += len(ready)
        tot_s += sum(ready)
        pend = len(ds) - len(ready)
        rows.append(f"| [{name}]({F}HOC_TAP.html#{k}) | {level} | {' · '.join(f'{C} {n}' for C, n in by.items())} | "
                    f"{len(ready)}{f' (+{pend} đang soạn)' if pend else ''} | {sum(ready) / 3600:.1f} |")
    rows.append(f"| **Tổng** | | | **{tot_n}** | **{tot_s / 3600:.1f}** |")
    blocks["LF_STAGES"] = "\n".join(rows) + ("\n\n*Sinh bởi `audit/review/learn_full/master_sections.py` từ `pack.stages()` — cùng nguồn với "
                                              "`HOC_TAP.html`. Mỗi bài nằm đúng một chặng; máy kiểm mọi bài cần học trước đứng trước nó.*")
    # cấp AI, chuyên gia, mở rộng
    tiers = [("CẤP ĐỘ 5 · Trí tuệ nhân tạo và học máy (chặng 9)", ["AIF", "DAN", "DSC", "MLO", "IRS", "LLM", "AGT", "RLN", "CVI"]),
             ("CẤP ĐỘ 6 · Chuyên gia (chặng 10)", ["TOC", "PLC", "PAR", "HCI", "SEP", "CAS"]),
             ("Chuyên ngành mở rộng, tuỳ chọn (chặng 11) và đám mây", ["RBM", "ESY", "ROB", "GFX", "BCH", "CLC"])]
    rows = []
    for tname, cs in tiers:
        rows += [f"**{tname}**", "", "| Mã khoá | Tên khoá | Số bài | Có video | Giờ | Giáo án |", "|:---:|:---|:---:|:---:|:---:|:---:|"]
        for C in cs:
            ls = cur[C]["lessons"]
            ds = [d for d in (dur(C, l) for l in ls) if d is not None]
            rows.append(f"| `{C}` | {course_name(C)} | {len(ls)} | {len(ds)} | {sum(ds) / 3600:.1f} | [`{C.lower()}.yaml`]({F}curriculum/{C.lower()}.yaml) |")
        rows.append("")
    blocks["LF_TIERS"] = "\n".join(rows).rstrip()
    # BNX
    rows = ["| Mã bài | Bài học | Đặc tả (YAML) | Video | Thời lượng | Giọng | Đặc tả khớp video |", "|:---:|:---|:---|:---|:---:|:---:|:---:|"]
    tot = 0.0
    import lv
    for l in cur.get("BNX", {}).get("lessons", []):
        sp = l.get("spec") or l.get("spec_planned")
        if pack.has_video("BNX", l):
            o = pack.odir("BNX", l)
            br = json.loads((o / "build_report.json").read_text(encoding="utf-8"))
            with redirect_stdout(io.StringIO()):
                fresh = br.get("spec_sha256") == lv.spec_digest(lv.load_spec(ROOT / l["spec"]))
            d = dur("BNX", l)
            tot += d
            voice = ",".join(v.replace("vi-VN-", "").replace("Neural", "") for v in br.get("voices", []))
            rows.append(f"| **`BNX:{l['id']}`** | {l['title']} | [`{Path(sp).name}`]({F}{sp}) | [`{l['id']}.mp4`]({F}out/BNX/{l['id']}/{l['id']}.mp4) | "
                        f"{pack.mmss(d)} | {voice} | {'có' if fresh else 'KHÔNG'} |")
        else:
            rows.append(f"| **`BNX:{l['id']}`** | {l['title']} | `{Path(sp).name}` | đang soạn | — | — | — |")
    blocks["LF_BNX"] = "\n".join(rows) + f"\n\n*Tổng BNX đã dựng: **{tot / 60:.2f} phút** (ffprobe).*"
    s = MASTER.read_text(encoding="utf-8")
    for k, body in blocks.items():
        s, n = re.subn(rf"(<!-- BEGIN:{k} -->).*?(<!-- END:{k} -->)", lambda m: m.group(1) + "\n" + body + "\n" + m.group(2), s, flags=re.S)
        assert n == 1, f"thiếu khối {k} trong MASTER_CURRICULUM_INDEX.md"
    MASTER.write_text(s, encoding="utf-8")
    print(f"đã ghi {list(blocks)}; {tot_n} bài có video, {tot_s / 3600:.1f} giờ")


if __name__ == "__main__":
    main()
