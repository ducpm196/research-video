"""Đồng bộ ngược: dựng lại tệp mẫu audit/<khoá>/src/<bài>.tpl.yaml từ bài đã sửa tay trong lessons/<khoá>/ (mỗi hình máy sinh → {{TÊN}}).
Lý do: bài đào sâu tại chỗ (pedagogy.md luật 24) sửa thẳng tệp bài; nếu mẫu không theo, lần chạy audit/<khoá>/fill_all.py sau sẽ GHI ĐÈ mất
phần đào sâu (lỗi thật 2026-10-31: SWF L07, DBS L06/L08/L12/L16, DSC L05/L06). Bảng JOBS đọc từ audit/<khoá>/fill_all.py.
Chỉ ghi khi điền ngược mẫu mới cho ra đúng từng byte bài hiện tại (bỏ qua khác biệt CRLF); mẫu cũ được sao lưu vào out/_tpl_backup/<khoá>/ (ngoài git).
Chạy: .venv/Scripts/python audit/review/sync_tpl_from_lesson.py <khoá> [--write]      (không --write: chỉ báo khớp / lệch)
      .venv/Scripts/python audit/review/sync_tpl_from_lesson.py --all                   (báo mọi khoá có mẫu)"""
import ast
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]


def jobs_of(course):
    src = (ROOT / "audit" / course / "fill_all.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    F, JOBS = f"audit/{course}/fig/", None
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            if node.targets[0].id == "JOBS":
                JOBS = ast.literal_eval(node.value)
            elif node.targets[0].id == "F":
                F = ast.literal_eval(node.value)
    return F, JOBS or {}


def fill(tpl, figs):
    for k, svg in figs.items():
        tpl = tpl.replace("{{" + k + "}}", svg)
    return tpl


def norm(s):
    return s.replace("\r\n", "\n")


def run(course, write):
    if not (ROOT / "audit" / course / "fill_all.py").exists():
        # không có bảng JOBS: chỉ so phần chữ — mỗi {{TÊN}} khớp “một dòng hình bất kỳ”; lệch thì phải sửa tay
        import re
        bad = 0
        for tp in sorted((ROOT / "audit" / course / "src").glob("*.tpl.yaml")):
            lp = ROOT / "lessons" / course / tp.name.replace(".tpl.yaml", ".yaml")
            if not lp.exists():
                # tên mẫu có thể ngắn hơn tên bài (CS112: L05_cay.tpl.yaml ↔ L05_cay_nhi_phan_avl.yaml) → tìm theo mã bài
                hits = sorted((ROOT / "lessons" / course).glob(tp.name.split("_")[0] + "_*.yaml"))
                if len(hits) != 1:
                    print(f"{course} {tp.name}: không tìm được đúng một bài cho mẫu này — kiểm tay")
                    bad += 1
                    continue
                lp = hits[0]
            parts = re.split(r"\{\{[A-Z0-9_]+\}\}", norm(tp.read_text(encoding="utf-8")))
            pat = "[^\n]*".join(re.escape(x) for x in parts)
            les = norm(lp.read_text(encoding="utf-8"))
            ok = re.fullmatch(pat, les, re.S) is not None
            if ok:
                print(f"{course} {lp.stem}: khớp (phần chữ)")
                continue
            bad += 1
            # dựng lại mẫu: lấy bài, đặt lại {{TÊN}} vào đúng dòng hình mà mẫu cũ giữ chỗ (ghép dòng bằng difflib)
            import difflib
            old_b = tp.read_bytes()
            t, l = norm(old_b.decode("utf-8")).split("\n"), les.split("\n")
            new, subs = list(l), 0
            for op, i1, i2, j1, j2 in difflib.SequenceMatcher(a=t, b=l, autojunk=False).get_opcodes():
                if op != "replace":
                    continue
                for k in range(i1, i2):
                    if "{{" not in t[k]:
                        continue
                    # dòng mẫu có chỗ hình (đứng riêng hay nhúng giữa dòng) → mẫu khớp: chữ giữ nguyên, {{TÊN}} = một đoạn bất kỳ
                    rx = "".join(".+?" if re.fullmatch(r"\{\{[A-Z0-9_]+\}\}", x) else re.escape(x)
                                 for x in re.split(r"(\{\{[A-Z0-9_]+\}\})", t[k]))
                    cand = [j for j in range(j1, j2) if re.fullmatch(rx, l[j])]
                    if len(cand) == 1:
                        new[cand[0]] = t[k]
                        subs += t[k].count("{{")
            out = "\n".join(new)
            parts2 = re.split(r"\{\{[A-Z0-9_]+\}\}", out)
            good = subs == sum(x.count("{{") for x in t) and re.fullmatch("[^\n]*".join(re.escape(x) for x in parts2), les, re.S)
            if not good:
                print(f"{course} {lp.stem}: LỆCH phần chữ — không tự dựng lại được (đặt {subs} chỗ hình), sửa tay")
            elif write:
                bk = ROOT / "out" / "_tpl_backup" / course
                bk.mkdir(parents=True, exist_ok=True)
                (bk / f"{tp.name}.bak").write_bytes(old_b)
                tp.write_bytes((out.replace("\n", "\r\n") if b"\r\n" in old_b else out).encode("utf-8"))
                print(f"{course} {lp.stem}: LỆCH phần chữ → đã ghi mẫu mới (mẫu cũ: out/_tpl_backup/{course}/{tp.name}.bak)")
            else:
                print(f"{course} {lp.stem}: LỆCH phần chữ (chạy lại với --write để ghi mẫu mới)")
        return bad
    F, JOBS = jobs_of(course)
    bad = 0
    for stem, m in JOBS.items():
        tp = ROOT / "audit" / course / "src" / f"{stem}.tpl.yaml"
        lp = ROOT / "lessons" / course / f"{stem}.yaml"
        if not tp.exists() or not lp.exists():
            continue
        paths = {k: ROOT / F / (v if Path(v).suffix else f"{v}.svg") for k, v in m.items()}
        missing = [str(p.relative_to(ROOT)) for p in paths.values() if not p.exists()]
        if missing:
            print(f"{course} {stem}: thiếu hình {missing} — chạy audit/{course}/figs.py trước")
            continue
        figs = {k: p.read_text(encoding="utf-8").strip() for k, p in paths.items()}
        old_b = tp.read_bytes()
        old, les = old_b.decode("utf-8"), lp.read_bytes().decode("utf-8")
        if norm(fill(old, figs)) == norm(les):
            print(f"{course} {stem}: khớp")
            continue
        bad += 1
        new = norm(les)
        for k, svg in figs.items():
            n = new.count(svg)
            # hình dùng lại nhiều lần (NET L08: DV_CUT hai lần) → hợp lệ khi mẫu cũ cũng giữ chỗ đúng bấy nhiêu lần
            if n != 1 and not (n > 1 and n == old.count("{{" + k + "}}")):
                print(f"{course} {stem}: LỆCH, nhưng hình {k} xuất hiện {n} lần trong bài (mẫu cũ {old.count('{{' + k + '}}')} chỗ) — sửa tay")
                break
            new = new.replace(svg, "{{" + k + "}}")
        else:
            if norm(fill(new, figs)) != norm(les):
                print(f"{course} {stem}: LỆCH, dựng ngược không khớp — sửa tay")
                continue
            if b"\r\n" in old_b:
                new = new.replace("\n", "\r\n")
            if write:
                bk = ROOT / "out" / "_tpl_backup" / course
                bk.mkdir(parents=True, exist_ok=True)
                (bk / f"{tp.name}.bak").write_bytes(old_b)
                tp.write_bytes(new.encode("utf-8"))
                print(f"{course} {stem}: LỆCH → đã ghi mẫu mới (mẫu cũ: out/_tpl_backup/{course}/{tp.name}.bak)")
            else:
                print(f"{course} {stem}: LỆCH (chạy lại với --write để ghi mẫu mới)")
    return bad


if __name__ == "__main__":
    a = sys.argv[1:]
    courses = sorted(p.parent.parent.name for p in (ROOT / "audit").glob("*/src/*.tpl.yaml")) if "--all" in a else [x.lower() for x in a if not x.startswith("--")]
    courses = [c for c in courses if (ROOT / "audit" / c / "src").is_dir()]
    total = sum(run(c, "--write" in a) for c in dict.fromkeys(courses))
    print(f"tổng: {total} mẫu lệch bài")
