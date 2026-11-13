"""Bộ dụng cụ lab dùng chung cho mọi bộ sinh bài (audit/<khoá>/src, gen.py): ghi thư mục labs/<KHOÁ>/<Lxx>/ và sinh các step của
cảnh `practice` (Tự làm). Hợp đồng ở labs/ENV.md; cổng: tools/lv.py lint (E51/E53) + audit/review/lab_gate.py.

    from labkit import write_lab, practice_steps
    write_lab("JVA", "L04", de_md, "java", solution_code, expected_text)
    steps = practice_steps(st, "JVA", "L04", task_html, task_say, expected_text, "TinhLai.java", hint_html, hint_say, pause=60)
    sc("practice", "practice", "Tự làm: …", steps)  → thêm lab="labs/JVA/L04" vào scene bằng practice_scene()

Luật: expected là ĐẦU RA THẬT của lời giải (lab_gate chạy lời giải qua labs/cham.sh và so); số liệu lab KHÁC số của ví dụ trong bài."""
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def write_lab(course, lid, de_md, ext, solution, expected):
    d = ROOT / "labs" / course.upper() / lid.upper()
    d.mkdir(parents=True, exist_ok=True)
    for old in d.glob("loi_giai.*"):
        old.unlink()
    (d / "de.md").write_text(de_md.strip("\n") + "\n", encoding="utf-8", newline="\n")
    (d / "mong_doi.txt").write_text(expected.strip("\n") + "\n", encoding="utf-8", newline="\n")
    (d / f"loi_giai.{ext}").write_text(solution.strip("\n") + "\n", encoding="utf-8", newline="\n")
    return d


def out_html(expected, title="Kết quả mong đợi"):
    lines = "".join(f"<div>{html.escape(x)}</div>" for x in expected.strip("\n").splitlines())
    return f"<p><b>{title}</b></p><div class=\"code\">{lines}</div>"


def practice_steps(st, course, lid, task_html, task_say, expected, filename, hint_html="", hint_say="", pause=60):
    """3 step: (1) đề + dừng để làm; (2) kết quả mong đợi + lệnh chấm; (3) gợi ý nếu kẹt (bỏ nếu không truyền)."""
    cmd = f"bash labs/cham.sh {course.upper()} {lid.upper()} {filename}"
    s1 = st(task_html, task_say, pause=pause)
    s2 = st(out_html(expected) + f"<p class=\"note\">Chấm bằng Git Bash: <code>{html.escape(cmd)}</code> — in <b>ĐÚNG</b> khi trùng.</p>",
            "Đây là kết quả mong đợi. Bạn chạy chương trình của mình rồi so từng dòng. Nếu muốn chấm bằng máy, dùng lệnh ở dưới màn hình; "
            "lệnh in chữ ĐÚNG khi đầu ra trùng, hoặc chỉ ra dòng nào khác.", clear=True)
    steps = [s1, s2]
    if hint_html:
        steps.append(st(hint_html, hint_say))
    return steps


def practice_scene(sc, title, steps, course, lid):
    """sc = hàm sc của bộ sinh; gắn lab vào cảnh."""
    s = sc("practice", "practice", title, steps)
    s["lab"] = f"labs/{course.upper()}/{lid.upper()}"
    return s
