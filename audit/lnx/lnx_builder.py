"""Trình dựng bài chuẩn AF2 riêng cho khoá LNX · Linux và Container thực chiến."""
import sys as _sys; from pathlib import Path as _P; _sys.path.insert(0, str(_P(__file__).resolve().parents[1])); import _frozen  # noqa: E402,F401
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "audit" / "review"))
import af2_kit as ak  # noqa: E402

COURSE = "LNX"
SERIES = "LNX · Linux và Container thực chiến"

COURSE_MAP_ROWS = [
    ["Bài 0–2", "Hệ thống tệp Linux, liên kết dữ liệu, phân quyền tệp và điều khiển tiến trình"],
    ["Bài 3–6", "Luồng chuẩn lọc nhật ký, hạn mức đĩa, cổng mạng và khoá bảo mật"],
    ["Bài 7–9", "Cô lập không gian chạy, ổ gắn bền vững và cụm nhiều dịch vụ"],
]


def make_lnx_lesson(cfg, ledger_meta):
    lid = cfg["id"]
    n_idx = int(lid[1:])
    slug = cfg["slug"]
    title = f"Bài {n_idx} — {cfg['title']}"
    src = (
        f"curriculum/lnx.yaml {lid}; audit/lnx/verify_lnx.py {lid} (chạy thật trên Git Bash & Docker Engine Linux); "
        "tài liệu POSIX.1-2017 & Linux man-pages; Docker Engine Docs (bản hiện hành)"
    )

    prog_outs = {}
    for pid, pinfo in cfg["progs"].items():
        rc, out = ak.run_bash(pinfo["code"], files=pinfo.get("files"), allow_nonzero=pinfo.get("allow_nonzero", False))
        if "expect" in pinfo and out != pinfo["expect"].strip("\n"):
            raise AssertionError(f"{lid} {pid}: đầu ra thật {out!r} != mong đợi {pinfo['expect']!r}")
        if "expect_sub" in pinfo:
            for sub in pinfo["expect_sub"]:
                if sub not in out:
                    raise AssertionError(f"{lid} {pid}: thiếu {sub!r} trong {out!r}")
        prog_outs[pid] = out

    lab_out = ak.write_and_grade_lab(COURSE, lid, cfg["lab_de"], "sh", cfg["lab_sol"])
    lab_lines = lab_out.splitlines()

    scenes = []

    # 1. HOOK
    hook_steps = [ak.st_auto(ak.box(cfg["hook_html"], "key"), cfg["hook_say"])]
    if lid == "L00":
        hm = ak.table(["phần", "lộ trình mười bài từ bài 0 tới bài 9"], COURSE_MAP_ROWS)
        hs = (
            "Khoá này gồm mười bài thực chiến từ bài 0 đến bài 9. "
            "Ba bài đầu đào sâu hệ thống tệp, phân quyền bát phân và tín hiệu tiến trình. "
            "Bốn bài giữa luyện lọc nhật ký, hạn mức đĩa, cổng mạng và bảo mật bí mật. "
            "Ba bài từ bài 7 đến bài 9 làm chủ cơ chế cô lập nhân và dựng cụm dịch vụ nhiều container."
        )
        hook_steps.append(ak.st_auto(hm, hs, clear=True, forward_ref=True))
    scenes.append(ak.sc("hook", "hook", cfg["hook_title"], hook_steps, checks=cfg.get("hook_checks")))

    # 2. PREREQ
    prereq_steps = [
        ak.st_auto(s["show"], s["say"], clear=True, introduces=s.get("introduces"))
        for s in cfg["prereq_steps"]
    ]
    scenes.append(ak.sc("prereq", "prereq", "Ôn nhanh kiến thức nền sẽ dùng", prereq_steps, checks=cfg.get("prereq_checks")))

    # 3. SYMBOL
    sym_steps = [
        ak.st_auto(s["show"], s["say"], clear=True, introduces=s.get("introduces"))
        for s in cfg["sym_steps"]
    ]
    scenes.append(ak.sc("sym", "symbol", "Giải mã ký hiệu và lệnh mới", sym_steps, checks=cfg.get("sym_checks")))

    # 4. INTUITION
    intuition_steps = [
        ak.st_auto(s["show"], s["say"], clear=True, introduces=s.get("introduces"))
        for s in cfg["intuition_steps"]
    ]
    scenes.append(ak.sc("intuition", "intuition", cfg["intuition_title"], intuition_steps, checks=cfg.get("intuition_checks")))

    # 5. FORMULA / RULE
    formula_steps = [
        ak.st_auto(s["show"], s["say"], clear=True, introduces=s.get("introduces"))
        for s in cfg["formula_steps"]
    ]
    scenes.append(ak.sc("formula", "formula", cfg["formula_title"], formula_steps, checks=cfg.get("formula_checks")))

    # 6. EXAMPLE
    ex_steps = []
    for item in cfg["example_items"]:
        if item["type"] == "r3":
            tbl = ak.table(["lệnh hoặc ký hiệu", "ý nghĩa dễ hiểu"], item["rows"])
            ex_steps.append(ak.st_auto(tbl, item["say"], clear=True, introduces=item.get("introduces")))
        elif item["type"] == "code":
            pid = item["pid"]
            pinfo = cfg["progs"][pid]
            ex_steps.append(ak.st_auto(ak.code_block(pinfo["code"], item.get("title")), item["say"], clear=True))
            ex_steps.append(ak.st_auto(ak.out_block(prog_outs[pid], item.get("out_title", "Kết quả chạy thật trên môi trường Linux")), item["out_say"], clear=True))
        elif item["type"] == "math":
            ex_steps.append(ak.st_auto(item["show"], item["say"], clear=True))
    scenes.append(ak.sc("example", "example", cfg["example_title"], ex_steps, checks=cfg.get("example_checks")))

    # 7. CHECK
    chk_steps = []
    for item in cfg["check_items"]:
        if item["type"] == "code":
            pid = item["pid"]
            pinfo = cfg["progs"][pid]
            chk_steps.append(ak.st_auto(ak.code_block(pinfo["code"], item.get("title")), item["say"], clear=True))
            chk_steps.append(ak.st_auto(ak.out_block(prog_outs[pid], "Đầu ra đối chứng thật"), item["out_say"], clear=True))
        else:
            chk_steps.append(ak.st_auto(item["show"], item["say"], clear=True))
    scenes.append(ak.sc("check", "check", cfg["check_title"], chk_steps, checks=cfg.get("check_checks")))

    # 8. QUYMO
    quymo_steps = [ak.st_auto(s["show"], s["say"], clear=True) for s in cfg["quymo_steps"]]
    scenes.append(ak.sc("quymo", "example", cfg["quymo_title"], quymo_steps, checks=cfg.get("quymo_checks")))

    # 9. PITFALLS
    pit_steps = []
    for stp in cfg["pitfall_steps"]:
        sh = stp["show"]
        if "<table" not in sh:
            sh = ak.table(["bẫy thường gặp và cách phòng tránh"], [[sh]])
        pit_steps.append(ak.st_auto(sh, stp["say"], clear=True))
    scenes.append(ak.sc("pitfalls", "pitfall", "Ba lỗi thường gặp trên máy chủ thực tế", pit_steps, checks=cfg.get("pitfall_checks")))

    # 10. QUIZ
    quiz_steps = []
    for qi, qst in enumerate(cfg["quiz_steps"]):
        sh = qst["show"]
        if qi > 0 and "<table" not in sh and "$$" not in sh:
            sh = ak.table([f"đáp án câu {qi}"], [[sh]])
        quiz_steps.append(ak.st(sh, qst["say"], pause=qst.get("pause"), clear=qst.get("clear")))
    scenes.append(ak.sc("quiz", "quiz", "Đến lượt bạn tự kiểm", quiz_steps, checks=cfg.get("quiz_checks")))

    # 11. PRACTICE
    lab_cmd = f"bash labs/cham.sh LNX {lid} duong_dan/bai_cua_ban.sh"
    prac_steps = [
        ak.st_auto(
            ak.box(
                f"<p><b>Bài thực hành {lid}:</b> mở đề tại <code>labs/LNX/{lid}/de.md</code>, viết kịch bản Bash "
                f"vào một tệp tạm rồi mở <b>Git Bash</b> và chạy lệnh chấm thật:</p>"
                f"<p><code>{ak.esc(lab_cmd)}</code></p>",
                "key",
            ),
            "Bây giờ đến phần bạn tự viết kịch bản dòng lệnh và chấm thật trên máy. Bạn mở đề thực hành, viết lời giải vào tệp riêng rồi chạy lệnh kiểm định đối chiếu từng dòng. Hãy bấm tạm dừng và tự làm trước.",
            pause=30,
            clear=True,
        ),
        ak.st_auto(
            ak.out_block("\n".join(lab_lines), f"Kết quả mong đợi cần khớp 100% ({len(lab_lines)} dòng)"),
            "Màn hình hiện toàn bộ các dòng kết quả mong đợi mà kịch bản của bạn phải in ra khớp từng ký tự.",
            clear=True,
        ),
    ]
    scenes.append(ak.sc("practice", "practice", "Tự làm bài thực hành dòng lệnh và chấm thật", prac_steps, lab=f"labs/LNX/{lid}"))

    # 12. RECAP
    recap_steps = list(cfg["recap_steps"])
    if cfg.get("next_title"):
        next_num = n_idx + 1
        recap_steps.append(
            ak.st(
                ak.box(f"<b>Bài sau (bài {next_num}):</b> {ak.esc(cfg['next_title'])}", "ok"),
                f"Bài tiếp theo là bài {next_num}, tìm hiểu chủ đề tiếp nối ngay phần vừa học. Hẹn gặp bạn ở bài sau.",
                forward_ref=True,
                clear=True,
            )
        )
    else:
        recap_steps.append(
            ak.st(
                ak.box("<b>Hoàn thành trọn bộ 10 bài LNX:</b> bạn đã làm chủ hệ thống tệp, tiến trình, mạng và Docker Compose.", "ok"),
                "Chúc mừng bạn đã hoàn thành trọn vẹn mười bài thực hành hệ điều hành và container. Kiến thức này là nền trực tiếp cho mạng máy tính và vận hành hệ thống.",
                clear=True,
            )
        )
    scenes.append(ak.sc("recap", "recap", "Chuỗi logic và tư duy cần mang theo", recap_steps, checks=cfg.get("recap_checks")))

    spec = ak.build_spec(COURSE, SERIES, lid, title, src, cfg["objectives"], scenes, cfg["covers"], assumes=cfg.get("assumes"))
    out_path = ak.write_lesson(spec, slug)

    _, blocks = ak.sc_mod.blocks_of(out_path)
    last_code_key = None
    last_is_run = False
    for sid, ti, bi, txt in blocks:
        k = f"{COURSE} {lid} {sid} {ti} {bi}"
        if sid == "practice":
            ledger_meta[k] = {
                "kind": "other",
                "lang": "text",
                "reason": f"Đầu ra mong đợi chính xác của bài thực hành labs/LNX/{lid} (kiểm qua cham.sh và verify_lnx.py).",
                "read_check": f"Khớp từng dòng mong_doi.txt từ labs/LNX/{lid}/loi_giai.sh.",
            }
        elif sid in ("example", "check") and last_code_key is not None and not last_is_run:
            ledger_meta[k] = {
                "kind": "other",
                "lang": "text",
                "reason": f"Đầu ra chụp trực tiếp từ Docker Engine khi chạy khối {last_code_key} (kiểm lại trong audit/lnx/verify_lnx.py).",
                "read_check": f"Khớp stdout trong audit/lnx/verify_lnx.py cho {lid}.",
            }
            last_is_run = False
            last_code_key = None
        elif sid in ("example", "check") and last_code_key is not None and last_is_run:
            ledger_meta[k] = {
                "kind": "output",
                "of": last_code_key,
                "reason": f"Đầu ra thực tế khi chạy khối bash {last_code_key}.",
            }
            last_code_key = None
        elif "docker " in txt or "MSYS_NO_PATHCONV=1 docker" in txt:
            ledger_meta[k] = {
                "kind": "other",
                "lang": "bash",
                "reason": f"Lệnh Docker Engine chạy thật trong gen.py & verify_lnx.py (tách khỏi screen_code thuần host vì cần daemon container).",
                "read_check": f"Khớp kịch bản chạy thật trong audit/lnx/verify_lnx.py {lid}.",
            }
            last_code_key = k
            last_is_run = False
        elif sid in ("example", "check") and ("\n" in txt or txt.startswith("#") or txt.startswith("set ") or "echo " in txt or "awk " in txt or "grep " in txt or "stat " in txt or "printf " in txt):
            ledger_meta[k] = {
                "kind": "run",
                "lang": "bash",
                "no_claim_reason": "Kịch bản Bash chạy sạch trên Git Bash và đối chiếu đầu ra ở khối liền sau.",
            }
            last_code_key = k
            last_is_run = True
        else:
            ledger_meta[k] = {
                "kind": "other",
                "lang": "text",
                "reason": "Khối minh hoạ lệnh hoặc cấu hình.",
                "read_check": "Kiểm trực tiếp theo nội dung bài.",
            }
    return out_path, prog_outs, lab_out
