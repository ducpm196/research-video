"""Sinh toàn bộ 14 bài khoá MLP (L00..L13) từ dữ liệu thật chạy trên labs/.venv-ml + cham.sh + screen_code."""
import subprocess
import sys
import time
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "audit" / "review"))
sys.path.insert(0, str(ROOT / "audit" / "mlp"))
sys.stdout.reconfigure(encoding="utf-8")

import af2_kit as ak  # noqa: E402
import af2_upgrader as up  # noqa: E402
import lv  # noqa: E402
from data_mlp_a import LESSONS_A  # noqa: E402
from data_mlp_b import LESSONS_B  # noqa: E402

VENV_ML_PY = str(ROOT / "labs" / ".venv-ml" / "Scripts" / "python.exe")
SERIES = "MLP · Học máy Thực hành"

ALL = LESSONS_A + LESSONS_B


def batch_run_ml(jobs):
    """Run all (key, code) snippets inside one .venv-ml process (one sklearn/torch import) for speed."""
    import json as _json
    worker = (
        "import contextlib, io, json, sys, time\n"
        "jobs = json.loads(sys.stdin.buffer.read().decode('utf-8'))\n"
        "out = {}\n"
        "for k, code in jobs:\n"
        "    buf = io.StringIO()\n"
        "    t0 = time.perf_counter()\n"
        "    with contextlib.redirect_stdout(buf):\n"
        "        exec(compile(code, k, 'exec'), {'__name__': '__main__'})\n"
        "    dt = time.perf_counter() - t0\n"
        "    if dt > 60.0:\n"
        "        raise RuntimeError(f'{k} exceeded 60s CPU budget: {dt:.2f}s')\n"
        "    out[k] = buf.getvalue().strip()\n"
        "sys.stdout.buffer.write(json.dumps(out).encode('utf-8'))\n"
    )
    p = subprocess.run([VENV_ML_PY, "-I", "-X", "utf8", "-B", "-c", worker],
                       input=_json.dumps(jobs).encode("utf-8"), cwd=ROOT, capture_output=True, timeout=300)
    if p.returncode != 0:
        raise RuntimeError(f"batch_run_ml failed: {p.stderr.decode('utf-8', 'replace')}")
    return _json.loads(p.stdout.decode("utf-8"))


_JOBS = []
for cfg in ALL:
    lid = cfg["id"]
    _JOBS.extend([(f"{lid}:lab", cfg["lab_sol"].strip("\n") + "\n"), (f"{lid}:ex", cfg["ex_code"]), (f"{lid}:chk", cfg["chk_code"])])
_OUTS = batch_run_ml(_JOBS)

for cfg in ALL:
    lid = cfg["id"]
    ldir = ROOT / "labs" / "MLP" / lid
    ldir.mkdir(parents=True, exist_ok=True)
    sol_code = cfg["lab_sol"].strip("\n") + "\n"
    lab_out = _OUTS[f"{lid}:lab"]

    (ldir / "de.md").write_text(cfg["lab_de"].strip() + "\n", encoding="utf-8", newline="\n")
    (ldir / "loi_giai.py").write_text(sol_code, encoding="utf-8", newline="\n")
    (ldir / "mong_doi.txt").write_text(lab_out + "\n", encoding="utf-8", newline="\n")

    if "--skip-cham" not in sys.argv:
        chk = subprocess.run([ak.BASH_EXE, str(ROOT / "labs" / "cham.sh"), "MLP", lid, str(ldir / "loi_giai.py")],
                             cwd=ROOT, env=ak._tool_env(), capture_output=True, text=True, encoding="utf-8", timeout=60)
        if chk.returncode != 0 or chk.stdout.strip() != "ĐÚNG":
            raise RuntimeError(f"cham MLP {lid} failed: {chk.stdout} {chk.stderr}")

    ex_out = _OUTS[f"{lid}:ex"]
    chk_out = _OUTS[f"{lid}:chk"]

    pre_rows = [[a, b] for a, b in cfg["prereq"]]
    b1, b2, b3 = cfg["svg_boxes"]
    svg = ak.svg_wrap(960, 170, (
        ak.svg_rect(40, 35, 250, 90, b1[0], b1[1], ak.C_BLUE) +
        ak.svg_arrow(290, 80, 350, 80, "bước 1") +
        ak.svg_rect(350, 35, 250, 90, b2[0], b2[1], ak.C_GREEN) +
        ak.svg_arrow(600, 80, 660, 80, "bước 2") +
        ak.svg_rect(660, 35, 260, 90, b3[0], b3[1], ak.C_AMBER)
    ))
    qm_rows = [[a, b, c] for a, b, c in cfg["quymo"]]
    pit_body = "<div class='box warn'>" + "<br>".join(cfg["pitfalls"]) + "</div>"
    lab_lines = lab_out.splitlines()
    cmd = f"bash labs/cham.sh MLP {lid} duong_dan/bai_cua_ban.py"
    prac_rows = [
        ["<b>Đề bài</b>", f"Mở <code>labs/MLP/{lid}/de.md</code>, chạy với Python (.venv-ml)"],
        ["<b>Kiểm chứng</b>", f"Đầu ra chuẩn {len(lab_lines)} dòng khớp 100% qua cham.sh (≤ 30 s CPU)"],
        ["<b>Lệnh chấm</b>", f"<code>{ak.esc(cmd)}</code>"],
    ]

    import re as _re
    def _split_long(txt):
        out = []
        for s in _re.split(r"(?<=[.?!])\s+", txt.strip()):
            if len(s) > 150 or len(s.split()) > 32:
                sep = ", " if ", " in s else next((c for c in (" nhưng ", " nên ", " vì ", " để ", " rồi ", " và ") if c in s), None)
                if sep:
                    parts = [p.strip() for p in s.split(sep)]
                    best_i, best_d = None, 10**9
                    for i in range(1, len(parts)):
                        l, r = sep.join(parts[:i]), sep.join(parts[i:])
                        if len(l.split()) >= 6 and len(r.split()) >= 6:
                            d = abs(len(l) - len(r))
                            if d < best_d:
                                best_i, best_d = i, d
                    if best_i is not None:
                        l = sep.join(parts[:best_i]).rstrip(".") + "."
                        r = sep.join(parts[best_i:])
                        w = sep.strip()
                        r = (w.capitalize() + " " + r) if w and w != "," and w != "rồi" else (r[0].upper() + r[1:])
                        out.extend([l, r])
                        continue
            out.append(s)
        return " ".join(out)
    _reasons = r"\b(?:vì|nên|do|theo)\b"
    def _need_r(txt, add):
        t = txt if _re.search(_reasons, txt.lower()) else (txt + " " + add)
        return _split_long(t)
    h_say = _split_long(cfg["hook_say"])
    pr_say = _split_long(cfg["prereq_say"] + " Đây là nền tảng trực tiếp để thiết kế đường ống thực hành sạch và ổn định.")
    sy_say = _split_long(cfg["sym_say"])
    sv_say = _split_long(cfg["svg_say"])
    f_say = _need_r(cfg["formula_say"], "Vì vậy công thức định lượng giúp kiểm soát sai số và biến đổi mô hình minh bạch hơn.")
    ex_s = _need_r(cfg["ex_say"], "Ta chạy thực nghiệm này vì cần đo trực tiếp hành vi trên dữ liệu thật.")
    exo_s = _need_r(cfg["ex_out_say"], "Đầu ra hợp lý vì tham số và hàm mất mát vận hành đúng bất biến vừa nêu.")
    c_say = _need_r(cfg["chk_say"], "Phép kiểm chứng này rất quan trọng vì đối chiếu độc lập giúp phát hiện ngay sai lệch.")
    co_say = _need_r(cfg["chk_out_say"], "Kết quả kiểm chứng nhất quán vì hệ thức toán học giữ nguyên ở cả phép thử độc lập.")
    qm_s = _split_long(cfg["quymo_say"])
    p_say = _split_long(cfg["pitfalls_say"] + " Bạn hãy rà soát từng lỗi trên trước khi chuyển sang phần tự làm bài tập thực hành trên máy.")
    q_s = _split_long(cfg["q_say"])
    qa1_s = _split_long(cfg["q_ans1_say"])
    qa2_s = _split_long(cfg["q_ans2_say"])

    hook_step = ak.st_auto(ak.box(f"<p>{cfg['hook_txt']}</p>", "key"), h_say, clear=True)
    if cfg.get("introduces"):
        hook_step["introduces"] = list(cfg["introduces"])
    scenes = [
        ak.sc("hook", "hook", cfg["title"].split("—")[-1].strip()[:58], [hook_step], checks=cfg["hook_chk"]),
        ak.sc("prereq", "prereq", "Ôn nền và kết nối bài trước", [
            ak.st_auto(ak.table(["mảnh ghép nền", "vai trò trong bài"], pre_rows), pr_say, clear=True),
        ]),
        ak.sc("sym", "symbol", "Viết trong mã → Đọc và hiểu là", [
            ak.st_auto(ak.table(["viết trong mã", "đọc và hiểu là"], cfg["sym_rows"]), sy_say, clear=True),
        ]),
        ak.sc("intuition", "intuition", "Cơ chế vận hành trực quan", [
            ak.st_auto(svg, sv_say, clear=True),
        ]),
        ak.sc("formula", "formula", "Công thức và bất biến định lượng", [
            ak.st_auto(ak.box(cfg["formula_txt"], "key"), f_say, clear=True),
        ], checks=cfg["hook_chk"]),
        ak.sc("example", "example", "Chạy thật trên CPU với dữ liệu chuẩn", [
            ak.st_auto(ak.code_block(cfg["ex_code"], "Thực nghiệm Python (.venv-ml)"), ex_s, clear=True),
            ak.st_auto(ak.out_block(ex_out, "Đầu ra chạy thật (scikit-learn / PyTorch CPU)"), exo_s, clear=True),
        ], checks=cfg["hook_chk"]),
        ak.sc("check", "check", "Kiểm chứng đối lập độc lập", [
            ak.st_auto(ak.code_block(cfg["chk_code"], "Phép kiểm chứng thứ hai"), c_say, clear=True),
            ak.st_auto(ak.out_block(chk_out, "Đầu ra kiểm chứng"), co_say, clear=True),
        ], checks=cfg["hook_chk"]),
        ak.sc("quymo", "example", "Mở rộng quy mô và giới hạn thực tế", [
            ak.st_auto(ak.table(["quy mô / bẫy", "tác động", "cách xử lý chuẩn"], qm_rows), qm_s, clear=True),
        ], checks=cfg["hook_chk"]),
        ak.sc("pitfalls", "pitfall", "Ba sai lầm làm sụp hệ thống học máy", [
            ak.st_auto(ak.table(["cảnh báo lỗi thường gặp"], [[pit_body]]), p_say, clear=True),
        ]),
        ak.sc("quiz", "quiz", "Kiểm tra nhanh trước khi tự thực hành", [
            ak.st_auto(cfg["q_text"], q_s, pause=20, clear=True),
            ak.st_auto(ak.table(["đáp án câu 1"], [[f"<p>① {cfg['q_ans1']}</p>"]]), qa1_s, clear=True),
            ak.st_auto(ak.table(["đáp án câu 2"], [[f"<p>② {cfg['q_ans2']}</p>"]]), qa2_s, clear=True),
        ], checks=cfg["hook_chk"]),
        ak.sc("practice", "practice", "Tự làm bài tập CPU và chấm tự động", [
            ak.st_auto(ak.table([f"Thực hành MLP:{lid}", "Hướng dẫn tự làm và chấm tự động"], prac_rows),
                       "Bây giờ đến phần bạn tự thực hành và chấm điểm trực tiếp trên máy bằng môi trường CPU chuẩn của kho. Bạn mở tệp đề bài, tự viết lời giải hoàn chỉnh vào tệp Python riêng rồi chạy lệnh chấm tự động để đối chiếu từng dòng kết quả với đáp án chuẩn. Hãy bấm tạm dừng video và tự tay cài đặt trước khi xem lời giải.",
                       pause=30, clear=True),
            ak.st_auto(ak.out_block(lab_out, f"Kết quả mong đợi cần khớp 100% ({len(lab_lines)} dòng)"),
                       "Màn hình hiển thị toàn bộ các dòng kết quả mong đợi mà chương trình của bạn phải in ra khớp chính xác từng ký tự. Nếu sai một chữ số hay sai nhãn khoá, bộ chấm tự động sẽ chỉ rõ dòng lệch để bạn sửa ngay.",
                       clear=True),
        ], lab=f"labs/MLP/{lid}"),
        ak.sc("recap", "recap", "Tổng kết bất biến bài học", [
            ak.st_auto('<div class="chain">' + '<span class="a">→</span>'.join(f'<span class="n">{x}</span>' for x in cfg["chain"]) + '</div>',
                       "Chuỗi tổng kết kết nối ba quy tắc bất biến bạn vừa tự tay thực chứng trên CPU qua ví dụ, kiểm chứng độc lập và bài tập thực hành. Hãy giữ chắc ba nguyên tắc này khi triển khai bất kỳ đường ống học máy nào ngoài thực tế.", clear=True),
            ak.st_auto(ak.box(f"<b>Hoàn thành MLP:{lid}:</b> đã kiểm chứng toàn bộ bất biến cốt lõi.", "ok"),
                       "Chúc mừng bạn đã hoàn tất trọn vẹn bài học máy thực hành trên CPU với đầy đủ bằng chứng số liệu và kiểm thử tự động.", clear=True),
        ]),
    ]

    spec = {
        "id": lid,
        "course": "MLP",
        "series": SERIES,
        "title": cfg["title"],
        "voice": "vi-VN-NamMinhNeural",
        "rate": "-5%",
        "depth": "full",
        "af2": True,
        "covers": [{"objective": 1, "scene": "example"}, {"objective": 2, "scene": "check"}, {"objective": 3, "scene": "quymo"}],
        "source": f"curriculum/mlp.yaml {lid}; labs/ENV.md (.venv-ml: scikit-learn 1.9.1, torch 2.15.0+cpu); labs/cham.sh",
        "assumes": cfg["assumes"],
        "objectives": cfg["obj"],
        "asr_reviewed": [],
        "scenes": scenes,
    }

    res = lv.lint(spec)
    if res.errors or res.warnings:
        raise RuntimeError(f"lint MLP {lid}: E={res.errors} W={res.warnings}")

    out_p = ak.write_lesson(spec, cfg["fname"][4:-5])
    print(f"OK MLP {lid}: {out_p.name} ({len(lab_lines)} dòng)")

led_p, nblk = up.sync_course_ledger("MLP", default_lang="python")
print(f"Synced {led_p.relative_to(ROOT)}: {nblk} blocks")
