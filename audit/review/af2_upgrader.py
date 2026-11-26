"""Bộ nâng cấp chuẩn AF2 dùng chung cho các khoá LF2 hiện có (WP-AF4-3 / WP-AF4-4).

Cơ chế tái lập hoàn toàn (idempotent) học từ audit/dms/af2/af2lib.py:
- Lần đầu chạy trên một bài: sao lưu nguyên bản LF2 vào audit/<khoá>/af2/base/<Lxx>.yaml.
- Mọi lần chạy sau luôn đọc từ bản gốc `base/` nên chạy lại bao nhiêu lần vẫn cho kết quả y hệt.
- Chạy thật lời giải (Python / C gcc / SQLite / Bash / Java / Node), chấm qua `labs/cham.sh`,
  cài cảnh `practice` (+ `quymo` + bảng giải mã nếu thiếu), gắn `af2: true` & `covers`,
  chạy `lv.lint` (0 error, 0 warn) và đồng bộ `audit/review/screen_code/<KHOÁ>.yaml`.
"""
import sys as _sys; from pathlib import Path as _P; _sys.path.insert(0, str(_P(__file__).resolve().parents[1])); import _frozen  # noqa: E402,F401
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
import af2_kit as ak  # noqa: E402


class _Dumper(yaml.SafeDumper):
    pass


def _str_representer(dumper, data):
    if "\n" in data and not any(line != line.rstrip() for line in data.split("\n")):
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


_Dumper.add_representer(str, _str_representer)


def dump_yaml(obj):
    return yaml.dump(obj, Dumper=_Dumper, allow_unicode=True, sort_keys=False, width=10**6, default_flow_style=False)


def run_sql(sql_text):
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as d:
        p = Path(d) / "q.sql"
        p.write_text(sql_text.strip("\n") + "\n", encoding="utf-8", newline="\n")
        cmd = [shutil.which("sqlite3", path=ak._tool_env()["PATH"]) or "sqlite3", ":memory:"]
        r = subprocess.run(cmd, input=p.read_text(encoding="utf-8"), env=ak._tool_env(),
                           capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=30)
        if r.returncode != 0:
            raise RuntimeError(f"sqlite3 lỗi rc={r.returncode}: {r.stderr}")
        return "\n".join(l.rstrip() for l in r.stdout.replace("\r\n", "\n").splitlines()).strip("\n")


def run_java(java_code, class_name=None):
    if not class_name:
        m = re.search(r"public\s+class\s+([A-Za-z0-9_]+)", java_code)
        class_name = m.group(1) if m else "Main"
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as d:
        dp = Path(d)
        src = dp / f"{class_name}.java"
        src.write_text(java_code.strip("\n") + "\n", encoding="utf-8", newline="\n")
        c = subprocess.run(["javac", "-encoding", "UTF-8", src.name], cwd=d, env=ak._tool_env(),
                           capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60)
        if c.returncode != 0:
            raise RuntimeError(f"javac lỗi:\n{c.stderr}")
        r = subprocess.run(["java", "-Dfile.encoding=UTF-8", class_name], cwd=d, env=ak._tool_env(),
                           capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=30)
        if r.returncode != 0:
            raise RuntimeError(f"java lỗi rc={r.returncode}:\n{r.stderr}")
        return "\n".join(l.rstrip() for l in r.stdout.replace("\r\n", "\n").splitlines()).strip("\n")


def run_node(js_code):
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as d:
        p = Path(d) / "app.js"
        p.write_text(js_code.strip("\n") + "\n", encoding="utf-8", newline="\n")
        r = subprocess.run(["node", p.name], cwd=d, env=ak._tool_env(),
                           capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=30)
        if r.returncode != 0:
            raise RuntimeError(f"node lỗi rc={r.returncode}:\n{r.stderr}")
        return "\n".join(l.rstrip() for l in r.stdout.replace("\r\n", "\n").splitlines()).strip("\n")


def grade_and_write_lab(course, lid, de_md, ext, sol_code):
    """Ghi labs/<C>/<Lxx>/{de.md, loi_giai.<ext>, mong_doi.txt}, chạy thật và kiểm qua cham.sh."""
    C = course.upper()
    ldir = ROOT / "labs" / C / lid
    ldir.mkdir(parents=True, exist_ok=True)
    for old in ldir.glob("loi_giai.*"):
        old.unlink()
    if ext == "c":
        out = ak.run_c(sol_code)
    elif ext == "py":
        out = ak.run_py(sol_code)
    elif ext == "sh":
        _, out = ak.run_bash(sol_code)
    elif ext == "sql":
        out = run_sql(sol_code)
    elif ext == "java":
        out = run_java(sol_code)
    elif ext == "js":
        out = run_node(sol_code)
    else:
        raise ValueError(f"chưa hỗ trợ đuôi {ext}")
    sol_path = ldir / f"loi_giai.{ext}"
    sol_path.write_text(sol_code.strip("\n") + "\n", encoding="utf-8", newline="\n")
    (ldir / "de.md").write_text(de_md.strip("\n") + "\n", encoding="utf-8", newline="\n")
    (ldir / "mong_doi.txt").write_text(out + "\n", encoding="utf-8", newline="\n")
    chk = subprocess.run([ak.BASH_EXE, str(ROOT / "labs" / "cham.sh"), C, lid, str(sol_path)],
                         cwd=ROOT, env=ak._tool_env(), capture_output=True, text=True, encoding="utf-8", errors="replace")
    if chk.returncode != 0 or chk.stdout.strip() != "ĐÚNG":
        raise RuntimeError(f"cham.sh {C} {lid} không ĐÚNG: rc={chk.returncode} out={chk.stdout!r} err={chk.stderr!r}")
    return out


_LANG_NAMES = {
    "py": "Python",
    "sql": "SQL (SQLite)",
    "sh": "Bash (Shell)",
    "c": "C (C11)",
    "java": "Java",
    "js": "Node.js",
}


def practice_scene(course, lid, ext, lab_out, de_hint=None):
    C = course.upper()
    lines = lab_out.splitlines()
    lang_name = _LANG_NAMES.get(ext.lower(), ext.upper())
    cmd = f"bash labs/cham.sh {C} {lid} duong_dan/bai_cua_ban.{ext}"
    rows = [
        ["<b>Đề bài</b>", f"Mở <code>labs/{C}/{lid}/de.md</code>, cài đặt bằng <b>{lang_name}</b>"],
        ["<b>Kiểm chứng</b>", ak.esc(de_hint) if de_hint else f"Khớp chính xác 100% ({len(lines)} dòng đầu ra)"],
        ["<b>Lệnh chấm</b>", f"<code>{ak.esc(cmd)}</code>"],
    ]
    s1 = ak.st_auto(
        ak.table([f"Thực hành {C}:{lid}", "Hướng dẫn tự làm và chấm trên máy"], rows),
        "Bây giờ đến phần bạn tự thực hành và chấm điểm trực tiếp trên máy. Bạn mở đề bài, tự viết lời giải vào tệp riêng rồi chạy lệnh chấm để đối chiếu từng dòng kết quả. Hãy bấm tạm dừng và tự làm trước.",
        pause=30,
        clear=True,
    )
    s2 = ak.st_auto(
        ak.out_block("\n".join(lines), f"Kết quả mong đợi cần khớp 100% ({len(lines)} dòng)"),
        "Màn hình hiển thị toàn bộ các dòng kết quả mong đợi mà chương trình của bạn phải in ra khớp từng ký tự.",
        clear=True,
    )
    return ak.sc("practice", "practice", "Tự làm bài thực hành và chấm thật", [s1, s2], lab=f"labs/{C}/{lid}")


def _lesson_path(course, lid):
    cdir = ROOT / "lessons" / course.lower()
    hits = sorted(cdir.glob(f"{lid}_*.yaml"))
    if len(hits) != 1:
        raise FileNotFoundError(f"không tìm thấy đúng 1 tệp bài {course} {lid} trong {cdir}: {hits}")
    return hits[0]


def apply_upgrade(
    course,
    lid,
    *,
    de_md,
    ext,
    sol_code,
    de_hint=None,
    covers=None,
    objectives=None,
    assumes_add=(),
    extra_scenes=(),
    repl=(),
    allow_warn=False,
):
    """Nâng một bài LF2 lên chuẩn AF2 một cách bất biến từ audit/<khoá>/af2/base/<Lxx>.yaml."""
    C = course.upper()
    fpath = _lesson_path(C, lid)
    base_dir = ROOT / "audit" / course.lower() / "af2" / "base"
    base_dir.mkdir(parents=True, exist_ok=True)
    base_file = base_dir / f"{lid}.yaml"
    if not base_file.exists():
        shutil.copy2(fpath, base_file)

    spec = yaml.safe_load(base_file.read_text(encoding="utf-8"))
    lab_out = grade_and_write_lab(C, lid, de_md, ext, sol_code)

    spec["af2"] = True
    if objectives:
        spec["objectives"] = list(objectives)
    if assumes_add:
        cur_a = list(spec.get("assumes") or [])
        for a in assumes_add:
            if a not in cur_a:
                cur_a.append(a)
        spec["assumes"] = cur_a

    # Bảo toàn asr_reviewed nếu câu vẫn còn
    old_live = yaml.safe_load(fpath.read_text(encoding="utf-8")) or {}
    old_asr = {x["sentence"]: x for x in (old_live.get("asr_reviewed") or [])}

    # Chèn các cảnh mới (extra_scenes + practice) trước recap
    scenes = list(spec.get("scenes") or [])
    recap_idx = next((i for i, s in enumerate(scenes) if s.get("id") == "recap" or s.get("kind") == "recap"), len(scenes))

    new_insert = []
    for item in extra_scenes:
        sc_obj, before_id = item if isinstance(item, tuple) else (item, None)
        if before_id is None:
            new_insert.append(sc_obj)
        else:
            pos = next((i for i, s in enumerate(scenes) if s.get("id") == before_id), recap_idx)
            scenes.insert(pos, sc_obj)
            recap_idx = next((i for i, s in enumerate(scenes) if s.get("id") == "recap" or s.get("kind") == "recap"), len(scenes))

    # Gỡ practice cũ (nếu có) rồi chèn lại bản mới trước recap
    scenes = [s for s in scenes if s.get("kind") != "practice" and s.get("id") != "practice"]
    recap_idx = next((i for i, s in enumerate(scenes) if s.get("id") == "recap" or s.get("kind") == "recap"), len(scenes))
    prac_sc = practice_scene(C, lid, ext, lab_out, de_hint=de_hint)
    scenes[recap_idx:recap_idx] = new_insert + [prac_sc]
    spec["scenes"] = scenes

    # Gắn covers hợp lý nếu chưa chỉ định
    if covers:
        spec["covers"] = [{"objective": o, "scene": s} for o, s in covers]
    elif not spec.get("covers"):
        # Chọn cảnh ví dụ / kiểm / practice / công thức theo mục tiêu hiện có
        sids = [s.get("id") for s in scenes]
        ex_s = next((x for x in ("example", "quymo", "concept", "formula") if x in sids), sids[1])
        chk_s = next((x for x in ("check", "quymo", "pitfalls", "example") if x in sids), ex_s)
        n_obj = len(spec.get("objectives") or [])
        pool = [ex_s, chk_s, "practice", "formula", "sym"]
        spec["covers"] = [{"objective": i + 1, "scene": pool[min(i, len(pool) - 1)]} for i in range(n_obj)]

    # Áp dụng thay thế chuỗi nếu có
    raw_txt = dump_yaml(spec)
    for old, new in repl:
        if old not in raw_txt:
            raise AssertionError(f"{C} {lid}: không thấy chuỗi cần thay: {old[:80]!r}")
        raw_txt = raw_txt.replace(old, new, 1)
    spec = yaml.safe_load(raw_txt)

    # Khôi phục asr_reviewed còn khớp
    all_caps = {s for sc_o in spec["scenes"] for st_o in sc_o["steps"] for s in ak.lv.sentences(st_o.get("say", ""))}
    spec["asr_reviewed"] = [x for sent, x in old_asr.items() if sent in all_caps]

    fpath.write_text(dump_yaml(spec), encoding="utf-8", newline="\n")
    res = ak.lv.lint(ak.lv.load_spec(fpath), quiet=True)
    if res.errors or (res.warnings and not allow_warn):
        raise RuntimeError(f"lint {fpath.name} thất bại:\nE={res.errors}\nW={res.warnings}")
    return fpath, lab_out


def sync_course_ledger(course, default_lang="python"):
    """Đồng bộ sổ audit/review/screen_code/<KHOÁ>.yaml: giữ khối cũ còn SHA khớp, cập nhật khối mới (practice/quymo/...)."""
    C = course.upper()
    led_p = ROOT / "audit" / "review" / "screen_code" / f"{C}.yaml"
    if led_p.exists():
        doc = yaml.safe_load(led_p.read_text(encoding="utf-8")) or {}
    else:
        doc = {"course": C, "blocks": {}}
    old_blocks = dict(doc.get("blocks") or {})
    sources = dict(doc.get("sources") or {})
    actual = ak.sc_mod.all_blocks(C)

    new_blocks = {}
    last_run_by_step = {}
    for k, txt in actual.items():
        sha = ak.sc_mod.digest(txt)
        if k in old_blocks and old_blocks[k].get("sha") == sha:
            new_blocks[k] = old_blocks[k]
            if old_blocks[k].get("kind") == "run":
                parts = k.split()
                last_run_by_step[(parts[1], parts[2], parts[3])] = k
            continue
        parts = k.split()  # C Lxx sid ti bi
        lid, sid, ti, bi = parts[1], parts[2], parts[3], parts[4]
        if sid == "practice":
            new_blocks[k] = {
                "sha": sha,
                "kind": "other",
                "lang": "text",
                "reason": f"Đầu ra mong đợi chính xác của lab labs/{C}/{lid} (kiểm qua cham.sh & lab_gate.py).",
                "read_check": f"Khớp từng dòng mong_doi.txt từ lời giải thật labs/{C}/{lid}.",
            }
        elif txt.startswith("bash labs/cham.sh"):
            new_blocks[k] = {
                "sha": sha,
                "kind": "other",
                "lang": "text",
                "reason": "Lệnh chấm bài thực hành cho người học.",
                "read_check": "Kiểm trực tiếp theo labs/cham.sh.",
            }
        elif (lid, sid, ti) in last_run_by_step:
            rk = last_run_by_step[(lid, sid, ti)]
            new_blocks[k] = {
                "sha": sha,
                "kind": "output",
                "of": rk,
                "reason": f"Đầu ra thực tế khi chạy khối {rk}.",
            }
        elif "#include" in txt and "main(" in txt:
            new_blocks[k] = {
                "sha": sha,
                "kind": "run",
                "lang": "c",
                "no_claim_reason": "Đoạn mã C biên dịch sạch với -std=c11 -Wall -Wextra -Werror và kiểm đầu ra ở khối liền sau.",
            }
            last_run_by_step[(lid, sid, ti)] = k
        elif "print(" in txt or txt.startswith("import ") or "def " in txt:
            new_blocks[k] = {
                "sha": sha,
                "kind": "run",
                "lang": default_lang,
                "no_claim_reason": "Đoạn mã kiểm chứng chạy thật và đối chiếu đầu ra ở khối liền sau.",
            }
            last_run_by_step[(lid, sid, ti)] = k
        else:
            new_blocks[k] = {
                "sha": sha,
                "kind": "other",
                "lang": "text",
                "reason": "Khối minh hoạ cấu trúc hoặc kết quả.",
                "read_check": "Kiểm trực tiếp theo nội dung bài.",
            }

    out_doc = {"course": C}
    if sources:
        out_doc["sources"] = sources
    out_doc["blocks"] = new_blocks
    led_p.write_text(dump_yaml(out_doc), encoding="utf-8", newline="\n")
    return led_p, len(new_blocks)

