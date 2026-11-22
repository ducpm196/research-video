"""Trình dựng bài chuẩn AF2 riêng cho khoá PRJ · Dự án tổng hợp cuối mỗi chặng."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "audit" / "review"))
import af2_kit as ak  # noqa: E402

COURSE = "PRJ"
SERIES = "PRJ · Dự án tổng hợp cuối mỗi chặng"

COURSE_MAP_ROWS = [
    ["L00 (Chặng 1)", "Sổ giao dịch đa công cụ: lọc CSV và đối chiếu SQLite"],
    ["L01 (Chặng 2)", "Lõi chuyển khoản bút toán kép và khoá tránh bế tắc"],
    ["L02–L03 (Chặng 3–4)", "Cổng lũy đẳng bảo mật, đối soát ba bên và bảo vệ kiến trúc"],
    ["L04 (Chặng 5)", "Tìm đường chi phí thấp nhất trên đồ thị và hồi quy tối ưu"],
]


def make_prj_lesson(cfg, ledger_meta):
    lid = cfg["id"]
    n_idx = int(lid[1:])
    slug = cfg["slug"]
    title = f"Bài {n_idx} — {cfg['title']}"
    src = (
        f"curriculum/prj.yaml {lid}; labs/PRJ/SPEC.md (thang chấm 100 điểm); "
        f"audit/prj/verify_prj.py {lid} (chạy thật bằng Python 3.12 và chấm qua cham.sh)"
    )

    prog_outs = {}
    for pid, pinfo in cfg["progs"].items():
        out = ak.run_py(pinfo["code"], files=pinfo.get("files"))
        if "expect" in pinfo and out != pinfo["expect"].strip("\n"):
            raise AssertionError(f"{lid} {pid}: đầu ra thật {out!r} != mong đợi {pinfo['expect']!r}")
        prog_outs[pid] = out

    lab_out = ak.write_and_grade_lab(COURSE, lid, cfg["lab_de"], "py", cfg["lab_sol"])
    lab_lines = lab_out.splitlines()

    scenes = []

    # 1. HOOK
    hook_steps = [ak.st_auto(ak.box(cfg["hook_html"], "key"), cfg["hook_say"])]
    if lid == "L00":
        hm = ak.table(["dự án", "trọng tâm thực hành theo chặng"], COURSE_MAP_ROWS)
        hs = (
            "Khoá dự án nối thẳng năm chặng kiến thức nền thành sản phẩm chạy thật. "
            "Bài 0 làm chủ chuẩn hoá dữ liệu CSV và đối chiếu cơ sở dữ liệu nhẹ. "
            "Bài 1 xây lõi chuyển khoản bút toán kép sạch lỗi đồng thời. "
            "Bài 2 và bài 3 giải bài toán cổng bảo mật và đối soát ba bên, rồi bài 4 chốt bằng đồ thị và hồi quy."
        )
        hook_steps.append(ak.st_auto(hm, hs, clear=True, forward_ref=True))
    scenes.append(ak.sc("hook", "hook", cfg["hook_title"], hook_steps, checks=cfg.get("hook_checks")))

    # 2. PREREQ
    prereq_steps = [
        ak.st_auto(s["show"], s["say"], clear=True, introduces=s.get("introduces"))
        for s in cfg["prereq_steps"]
    ]
    scenes.append(ak.sc("prereq", "prereq", "Ghép các mảnh kiến thức trong chặng", prereq_steps, checks=cfg.get("prereq_checks")))

    # 3. SYMBOL / SPEC
    sym_steps = [
        ak.st_auto(s["show"], s["say"], clear=True, introduces=s.get("introduces"))
        for s in cfg["sym_steps"]
    ]
    scenes.append(ak.sc("sym", "symbol", "Quy chuẩn kỹ thuật và bất biến cần bảo đảm", sym_steps, checks=cfg.get("sym_checks")))

    # 4. INTUITION
    intuition_steps = [
        ak.st_auto(s["show"], s["say"], clear=True, introduces=s.get("introduces"))
        for s in cfg["intuition_steps"]
    ]
    scenes.append(ak.sc("intuition", "intuition", cfg["intuition_title"], intuition_steps, checks=cfg.get("intuition_checks")))

    # 5. FORMULA / RUBRIC INVARIANT
    formula_steps = [
        ak.st_auto(s["show"], s["say"], clear=True, introduces=s.get("introduces"))
        for s in cfg["formula_steps"]
    ]
    scenes.append(ak.sc("formula", "formula", cfg["formula_title"], formula_steps, checks=cfg.get("formula_checks")))

    # 6. EXAMPLE
    ex_steps = []
    for item in cfg["example_items"]:
        if item["type"] == "r3":
            tbl = ak.table(["ký hiệu / kỹ thuật", "vai trò trong dự án"], item["rows"])
            ex_steps.append(ak.st_auto(tbl, item["say"], clear=True, introduces=item.get("introduces")))
        elif item["type"] == "code":
            pid = item["pid"]
            pinfo = cfg["progs"][pid]
            ex_steps.append(ak.st_auto(ak.code_block(pinfo["code"], item.get("title")), item["say"], clear=True))
            ex_steps.append(ak.st_auto(ak.out_block(prog_outs[pid], item.get("out_title", "Kết quả chạy thật (Python)")), item["out_say"], clear=True))
    scenes.append(ak.sc("example", "example", cfg["example_title"], ex_steps, checks=cfg.get("example_checks")))

    # 7. CHECK
    chk_steps = []
    for item in cfg["check_items"]:
        if item["type"] == "code":
            pid = item["pid"]
            pinfo = cfg["progs"][pid]
            chk_steps.append(ak.st_auto(ak.code_block(pinfo["code"], item.get("title")), item["say"], clear=True))
            chk_steps.append(ak.st_auto(ak.out_block(prog_outs[pid], "Đầu ra kiểm chứng độc lập"), item["out_say"], clear=True))
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
            sh = ak.table(["lỗi mất điểm phổ biến khi nộp dự án"], [[sh]])
        pit_steps.append(ak.st_auto(sh, stp["say"], clear=True))
    scenes.append(ak.sc("pitfalls", "pitfall", "Ba lỗi làm mất điểm nặng ở đồ án thực tế", pit_steps, checks=cfg.get("pitfall_checks")))

    # 10. QUIZ
    quiz_steps = []
    for qi, qst in enumerate(cfg["quiz_steps"]):
        sh = qst["show"]
        if qi > 0 and "<table" not in sh and "$$" not in sh:
            sh = ak.table([f"đáp án câu {qi}"], [[sh]])
        quiz_steps.append(ak.st(sh, qst["say"], pause=qst.get("pause"), clear=qst.get("clear")))
    scenes.append(ak.sc("quiz", "quiz", "Kiểm tra nhanh tiêu chí nghiệm thu", quiz_steps, checks=cfg.get("quiz_checks")))

    # 11. PRACTICE (kèm rubric 100 điểm trong labs/PRJ/Lxx/de.md)
    lab_cmd = f"bash labs/cham.sh PRJ {lid} duong_dan/bai_cua_ban.py"
    prac_steps = [
        ak.st_auto(
            ak.box(
                f"<p><b>Dự án {lid} (thang 100 điểm theo <code>labs/PRJ/SPEC.md</code>):</b> mở đề tại <code>labs/PRJ/{lid}/de.md</code>, "
                f"cài đặt đầy đủ bất biến, xử lý biên và chấm tự động bằng lệnh:</p>"
                f"<p><code>{ak.esc(lab_cmd)}</code></p>",
                "key",
            ),
            "Bây giờ đến phần bạn tự hoàn thiện mã dự án để chấm điểm tự động theo thang một trăm điểm chuẩn. Bạn mở tệp đề bài, đọc kỹ dữ liệu mẫu và chạy trình chấm để đối chiếu từng dòng kết quả. Hãy bấm tạm dừng và tự triển khai trước.",
            pause=30,
            clear=True,
        ),
        ak.st_auto(
            ak.out_block("\n".join(lab_lines), f"Kết quả mong đợi cần khớp 100% ({len(lab_lines)} dòng)"),
            "Màn hình hiện đầy đủ các dòng kết quả đầu ra mà dự án của bạn phải xuất ra khớp từng ký tự.",
            clear=True,
        ),
    ]
    scenes.append(ak.sc("practice", "practice", "Tự cài đặt dự án và chấm tự động 100 điểm", prac_steps, lab=f"labs/PRJ/{lid}"))

    # 12. RECAP
    recap_steps = list(cfg["recap_steps"])
    if cfg.get("next_title"):
        next_num = n_idx + 1
        recap_steps.append(
            ak.st(
                ak.box(f"<b>Bài sau (bài {next_num}):</b> {ak.esc(cfg['next_title'])}", "ok"),
                f"Dự án tiếp theo ở bài {next_num} tổng hợp trọn vẹn chặng học kế tiếp. Hẹn gặp bạn ở bài sau.",
                forward_ref=True,
                clear=True,
            )
        )
    else:
        recap_steps.append(
            ak.st(
                ak.box("<b>Hoàn thành 5 dự án Chặng 1–5:</b> bạn đã nối thông từ CLI tới thuật toán đồ thị và hồi quy.", "ok"),
                "Chúc mừng bạn đã hoàn thành trọn vẹn năm dự án tổng hợp cho năm chặng học đầu tiên. Toàn bộ nền tảng này sẽ dẫn thẳng vào các chặng hệ thống và trí tuệ nhân tạo sắp tới.",
                clear=True,
            )
        )
    scenes.append(ak.sc("recap", "recap", "Tổng kết kiến trúc và bất biến dự án", recap_steps, checks=cfg.get("recap_checks")))

    spec = ak.build_spec(COURSE, SERIES, lid, title, src, cfg["objectives"], scenes, cfg["covers"], assumes=cfg.get("assumes"))
    out_path = ak.write_lesson(spec, slug)

    _, blocks = ak.sc_mod.blocks_of(out_path)
    last_run_key = None
    for sid, ti, bi, txt in blocks:
        k = f"{COURSE} {lid} {sid} {ti} {bi}"
        if sid == "practice":
            ledger_meta[k] = {
                "kind": "other",
                "lang": "text",
                "reason": f"Đầu ra mong đợi chính xác của dự án labs/PRJ/{lid} (được verify_prj và lab_gate chấm qua cham.sh).",
                "read_check": f"Khớp từng dòng mong_doi.txt từ labs/PRJ/{lid}/loi_giai.py.",
            }
        elif sid in ("example", "check") and last_run_key is None and not txt.startswith("bash "):
            ledger_meta[k] = {
                "kind": "run",
                "lang": "python",
                "no_claim_reason": "Đoạn mã Python chạy sạch trên môi trường chuẩn và kiểm đầu ra ở khối liền sau.",
            }
            last_run_key = k
        elif sid in ("example", "check") and last_run_key is not None:
            ledger_meta[k] = {
                "kind": "output",
                "of": last_run_key,
                "reason": f"Đầu ra thực tế khi chạy khối Python {last_run_key}.",
            }
            last_run_key = None
        else:
            ledger_meta[k] = {
                "kind": "other",
                "lang": "text",
                "reason": "Khối minh hoạ lệnh.",
                "read_check": "Kiểm trực tiếp theo nội dung bài.",
            }
    return out_path, prog_outs, lab_out
