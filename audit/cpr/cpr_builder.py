"""Trình dựng bài chuẩn AF2 riêng cho khoá CPR (Lập trình C và bộ nhớ)."""
import sys as _sys; from pathlib import Path as _P; _sys.path.insert(0, str(_P(__file__).resolve().parents[1])); import _frozen  # noqa: E402,F401
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "audit" / "review"))
import af2_kit as ak  # noqa: E402

COURSE = "CPR"
SERIES = "CPR · Lập trình C và bộ nhớ: con trỏ, cấp phát động, tệp và gcc"

COURSE_MAP_ROWS = [
    ["Bài 0–2", "Chương trình C, đo kích thước <code>sizeof</code>, tràn số nguyên và khung ngăn xếp"],
    ["Bài 3–5", "Chuỗi ký tự kết thúc bằng byte không, địa chỉ bộ nhớ và số học dịch chuyển địa chỉ"],
    ["Bài 6–7", "Cấp phát động trên vùng nhớ mở, kiểu cấu trúc, sắp trường tối ưu và danh sách liên kết"],
    ["Bài 8–9", "Đọc ghi tệp nhị phân, phép toán bit và bài tình huống phân tích nhật ký 16 byte"],
]


def auto_focus(show_html, say_text):
    return ak.auto_focus(show_html, say_text)


def _st_auto(show, say, clear=None, pause=None, introduces=None, forward_ref=None):
    return ak.st_auto(show, say, clear=clear, pause=pause, introduces=introduces, forward_ref=forward_ref)


def make_c_lesson(cfg, ledger_meta):
    lid = cfg["id"]
    n_idx = int(lid[1:])
    slug = cfg["slug"]
    title = f"Bài {n_idx} — {cfg['title']}"
    src = (
        f"curriculum/cpr.yaml {lid}; audit/cpr/verify_cpr.py {lid} (biên dịch và chạy thật bằng GCC 16.2.0 "
        f"với cờ -std=c11 -Wall -Wextra -Werror); chuẩn ngôn ngữ ISO/IEC 9899:2011 (C11, CITED theo mã chuẩn)"
    )

    # Biên dịch và chạy thật toàn bộ mã C trên màn hình trước khi dựng bước
    prog_outs = {}
    for pid, pinfo in cfg["progs"].items():
        out = ak.run_c(pinfo["code"], args=pinfo.get("args", ""), stdin=pinfo.get("stdin"))
        if "expect" in pinfo and out != pinfo["expect"].strip("\n"):
            raise AssertionError(f"{lid} {pid}: đầu ra thật {out!r} != mong đợi {pinfo['expect']!r}")
        prog_outs[pid] = out

    # Sinh và chấm thật lab qua labs/cham.sh
    lab_out = ak.write_and_grade_lab(COURSE, lid, cfg["lab_de"], "c", cfg["lab_sol"])
    lab_lines = lab_out.splitlines()

    scenes = []

    # 1. HOOK (+ bản đồ khoá học ở L00)
    hook_steps = [
        _st_auto(ak.box(cfg["hook_html"], "key"), cfg["hook_say"])
    ]
    if lid == "L00":
        hm = ak.table(["phần", "nội dung mười bài từ bài 0 tới bài 9"], COURSE_MAP_ROWS)
        hs = (
            "Khoá này gồm mười bài liên tục từ bài 0 đến bài 9. Bài 0 đến bài 2 mở đầu bằng trình biên dịch, kích thước dữ liệu, tràn số và ngăn xếp. "
            "Bài 3 đến bài 5 học chuỗi ký tự, địa chỉ bộ nhớ và số học dịch chuyển địa chỉ. Bài 6 đến bài 7 học vùng nhớ mở, kiểu cấu trúc và danh sách liên kết. "
            "Bài 8 và bài 9 đóng gói tệp nhị phân rồi giải bài toán phân tích nhật ký."
        )
        hook_steps.append(_st_auto(hm, hs, clear=True, forward_ref=True))
    scenes.append(ak.sc("hook", "hook", cfg["hook_title"], hook_steps, checks=cfg.get("hook_checks")))

    # 2. PREREQ
    prereq_steps = [_st_auto(s["show"], s["say"], clear=True, introduces=s.get("introduces")) for s in cfg["prereq_steps"]]
    scenes.append(ak.sc("prereq", "prereq", "Ôn nhanh kiến thức nền sẽ dùng", prereq_steps, checks=cfg.get("prereq_checks")))

    # 3. SYMBOL / SYNTAX DECODING
    sym_steps = [_st_auto(s["show"], s["say"], clear=True, introduces=s.get("introduces")) for s in cfg["sym_steps"]]
    scenes.append(ak.sc("sym", "symbol", "Giải mã ký hiệu và quy ước mới", sym_steps, checks=cfg.get("sym_checks")))

    # 4. INTUITION (SVG mechanism diagram)
    scenes.append(ak.sc("intuition", "intuition", cfg["intuition_title"], cfg["intuition_steps"], checks=cfg.get("intuition_checks")))

    # 5. FORMULA / MECHANISM DERIVATION
    formula_steps = [_st_auto(s["show"], s["say"], clear=True, introduces=s.get("introduces")) for s in cfg["formula_steps"]]
    scenes.append(ak.sc("formula", "formula", cfg["formula_title"], formula_steps, checks=cfg.get("formula_checks")))

    # 6. EXAMPLE (chạy thật GCC + bảng giải mã R3 đứng trước mỗi khối mã)
    ex_steps = []
    for item in cfg["example_items"]:
        if item["type"] == "r3":
            tbl = ak.table(["viết trong mã C", "nghĩa dễ hiểu"], item["rows"])
            ex_steps.append(_st_auto(tbl, item["say"], clear=True, introduces=item.get("introduces")))
        elif item["type"] == "code":
            pid = item["pid"]
            pinfo = cfg["progs"][pid]
            ex_steps.append(_st_auto(ak.code_block(pinfo["code"], item.get("title")), item["say"], clear=True))
            ex_steps.append(_st_auto(ak.out_block(prog_outs[pid], item.get("out_title", "Kết quả chạy thật (GCC)")),
                                     item["out_say"], clear=True))
        elif item["type"] == "math":
            ex_steps.append(_st_auto(item["show"], item["say"], clear=True))
    scenes.append(ak.sc("example", "example", cfg["example_title"], ex_steps, checks=cfg.get("example_checks")))

    # 7. CHECK (đường khác: mô hình toán / chạy thật khối phụ)
    chk_steps = []
    for item in cfg["check_items"]:
        if item["type"] == "code":
            pid = item["pid"]
            pinfo = cfg["progs"][pid]
            chk_steps.append(_st_auto(ak.code_block(pinfo["code"], item.get("title")), item["say"], clear=True))
            chk_steps.append(_st_auto(ak.out_block(prog_outs[pid], "Đầu ra đối chứng thật"), item["out_say"], clear=True))
        else:
            chk_steps.append(_st_auto(item["show"], item["say"], clear=True))
    scenes.append(ak.sc("check", "check", cfg["check_title"], chk_steps, checks=cfg.get("check_checks")))

    # 8. QUYMO (bảng quy mô 3 mức)
    quymo_steps = [_st_auto(s["show"], s["say"], clear=True) for s in cfg["quymo_steps"]]
    scenes.append(ak.sc("quymo", "example", cfg["quymo_title"], quymo_steps, checks=cfg.get("quymo_checks")))

    # 9. PITFALLS (bọc bảng để cắt dãy khung chỉ có chữ ở cuối bài — E39)
    pit_steps = []
    for stp in cfg["pitfall_steps"]:
        sh = stp["show"]
        if "<table" in sh:
            pit_steps.append(stp)
        else:
            pit_steps.append(ak.st(ak.table(["bẫy thường gặp và cách phòng tránh"], [[sh]]), stp["say"], clear=True))
    scenes.append(ak.sc("pitfalls", "pitfall", "Ba lỗi thường gặp, kể cả người đã đi làm", pit_steps, checks=cfg.get("pitfall_checks")))

    # 10. QUIZ (bọc bảng đáp án để giữ nhịp trực quan ≤ 1 khung chữ liền — E39)
    quiz_steps = []
    for qi, qst in enumerate(cfg["quiz_steps"]):
        sh = qst["show"]
        if qi > 0 and "<table" not in sh and "$$" not in sh:
            sh = ak.table([f"đáp án câu {qi}"], [[sh]])
        quiz_steps.append(ak.st(sh, qst["say"], pause=qst.get("pause"), clear=qst.get("clear")))
    scenes.append(ak.sc("quiz", "quiz", "Đến lượt bạn tự kiểm", quiz_steps, checks=cfg.get("quiz_checks")))

    # 11. PRACTICE (kèm mong_doi.txt + Git Bash + gcc)
    lab_cmd = f"bash labs/cham.sh CPR {lid} duong_dan/bai_cua_ban.c"
    prac_steps = [
        ak.st(
            ak.box(
                f"<p><b>Bài thực hành {lid}:</b> mở đề tại <code>labs/CPR/{lid}/de.md</code>, viết mã C chuẩn C11 "
                f"vào một tệp tạm rồi mở <b>Git Bash</b> (cài ở <code>Start → Git → Git Bash</code> hoặc chuột phải thư mục "
                f"chọn <b>Open Git Bash here</b>) và chạy lệnh chấm thật bằng trình biên dịch G C C:</p>"
                f"<p><code>{ak.esc(lab_cmd)}</code></p>",
                "key",
            ),
            "Bây giờ đến phần bạn tự viết mã C và chấm thật trên máy. Bạn mở đề thực hành, viết lời giải vào tệp riêng, "
            "rồi mở cửa sổ dòng lệnh để chạy trình chấm biên dịch và đối chiếu kết quả. Hãy bấm tạm dừng và tự làm trước.",
            pause=30,
            clear=True,
        ),
        ak.st(
            ak.out_block("\n".join(lab_lines), f"Kết quả mong đợi cần khớp 100% ({len(lab_lines)} dòng)"),
            "Màn hình hiện toàn bộ các dòng kết quả mong đợi mà chương trình của bạn phải in ra khớp từng ký tự.",
            clear=True,
        ),
    ]
    scenes.append(ak.sc("practice", "practice", "Tự làm bài thực hành C và chấm thật", prac_steps, lab=f"labs/CPR/{lid}"))

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
                ak.box("<b>Hoàn thành trọn bộ 10 bài CPR:</b> bạn đã nắm chắc bộ nhớ, con trỏ, Heap, cấu trúc và tệp nhị phân C.", "ok"),
                "Chúc mừng bạn đã hoàn thành trọn vẹn mười bài lập trình C và quản lý bộ nhớ. Kiến thức này là nền trực tiếp cho kiến trúc máy tính và hệ điều hành.",
                clear=True,
            )
        )
    scenes.append(ak.sc("recap", "recap", "Chuỗi logic và tư duy cần mang theo", recap_steps, checks=cfg.get("recap_checks")))

    spec = ak.build_spec(
        COURSE, SERIES, lid, title, src, cfg["objectives"], scenes, cfg["covers"], assumes=cfg.get("assumes")
    )
    out_path = ak.write_lesson(spec, slug)

    # Đăng ký sổ screen_code cho mọi khối mã và khối kết quả của bài này
    _, blocks = ak.sc_mod.blocks_of(out_path)
    # Gắn quy ước cho từng block của bài: mã C → run/c; kết quả chạy thật → output/- của khối ngay trước hoặc khối gần nhất
    last_run_key = None
    for sid, ti, bi, txt in blocks:
        k = f"{COURSE} {lid} {sid} {ti} {bi}"
        if sid == "practice":
            # Khối mong_doi.txt là output của lời giải lab
            ledger_meta[k] = {
                "kind": "other",
                "lang": "text",
                "reason": f"Đầu ra mong đợi chính xác của bài thực hành labs/CPR/{lid} (được verify_cpr và lab_gate chạy thật qua cham.sh).",
                "read_check": f"Khớp từng dòng mong_doi.txt từ labs/CPR/{lid}/loi_giai.c biên dịch bằng GCC.",
            }
        elif txt.startswith("#include") or "int main(" in txt or "struct " in txt or "typedef " in txt or txt.startswith("//"):
            ledger_meta[k] = {
                "kind": "run",
                "lang": "c",
                "no_claim_reason": "Đoạn mã C biên dịch sạch với -std=c11 -Wall -Wextra -Werror và kiểm đầu ra ở khối liền sau.",
            }
            last_run_key = k
        else:
            if last_run_key and (sid in ("example", "check")):
                ledger_meta[k] = {
                    "kind": "output",
                    "of": last_run_key,
                    "reason": f"Đầu ra thực tế khi biên dịch và chạy khối C {last_run_key} bằng GCC.",
                }
            else:
                ledger_meta[k] = {
                    "kind": "other",
                    "lang": "text",
                    "reason": "Khối minh hoạ lệnh hoặc văn bản.",
                    "read_check": "Kiểm trực tiếp theo nội dung bài.",
                }
    return out_path, prog_outs, lab_out
