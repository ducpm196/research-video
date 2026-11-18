"""Ca thử cổng E52 (thuật ngữ chữ giảng tại chỗ). Chạy: .venv/Scripts/python tests/test_e52.py
Đối chứng dương: thuật ngữ dùng trước khi giảng trong bài `af2: true` phải bị bắt; âm: có `introduces` thì sạch; bài không `af2` không bị đòi."""
import copy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import lv  # noqa: E402

TERM = {"id": "t_dau_ong", "name": "dấu ống", "term": "(?i)dấu ống"}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    fails = 0
    real = lv.registry
    base = lv.load_spec(ROOT / "lessons" / "fnd" / "L03_doc_va_loc_van_ban.yaml")

    def reg_with(course=lv.DEFAULT_COURSE):
        reg = real(course)
        reg = copy.deepcopy(reg)
        reg["symbols"] = list(reg["symbols"]) + [dict(TERM, pattern="(?!)")]
        return reg

    def run(spec):
        lv.registry = lambda course=lv.DEFAULT_COURSE: reg_with(course)
        try:
            return lv.lint(spec, quiet=True).errors
        finally:
            lv.registry = real

    # đầu tiên: tìm step đầu tiên có chữ “dấu ống” (trong show đã bỏ thẻ hoặc say)
    import re
    first = None
    for si, sc, ki, st in lv.iter_steps(base):
        if re.search(TERM["term"], re.sub(r"<[^>]+>", " ", str(st.get("show", ""))) + " " + str(st.get("say", ""))):
            first = (si, ki)
            break
    cases = []
    s = copy.deepcopy(base)
    errs = run(s)
    cases.append(("E52 thuật ngữ dùng trước khi giảng (bài af2) bị bắt", first is not None and any("E52" in e and "t_dau_ong" in e for e in errs)))
    s = copy.deepcopy(base)
    if first:
        sc = s["scenes"][first[0]]
        sc["steps"][first[1] - 0 if isinstance(first[1], int) else 0]
        for i2, (si2, sc2, ki2, st2) in enumerate(lv.iter_steps(s)):
            if (si2, ki2) == first:
                st2["introduces"] = list(st2.get("introduces") or []) + ["t_dau_ong"]
                break
    errs = run(s)
    cases.append(("E52 có `introduces` ở step đầu tiên thì sạch", first is not None and not any("E52" in e for e in errs)))
    s = copy.deepcopy(base)
    s["assumes"] = list(s.get("assumes") or []) + ["t_dau_ong"]
    errs = run(s)
    cases.append(("E52 có `assumes` (bài đứng trước đã giảng) thì sạch", not any("E52" in e for e in errs)))
    s = copy.deepcopy(base)
    s.pop("af2", None)
    errs = run(s)
    cases.append(("E52 bài chưa khai `af2` không bị đòi", not any("E52" in e for e in errs)))
    # E55: dạng không chuẩn bị bắt ở bài af2, không bị bắt ở bài chưa af2; dạng chuẩn sạch
    s = copy.deepcopy(base); s["scenes"][0]["steps"][0]["say"] += " Mở tập tin ra xem."
    cases.append(("E55 “tập tin” (dạng không chuẩn) bị bắt ở bài af2", any("E55" in e for e in run(s))))
    s = copy.deepcopy(base); s["scenes"][0]["steps"][0]["say"] += " Mở tệp ra xem."
    cases.append(("E55 “tệp” (dạng chuẩn) sạch", not any("E55" in e for e in run(s))))
    s = copy.deepcopy(base); s.pop("af2", None); s["scenes"][0]["steps"][0]["say"] += " Mở tập tin ra xem."
    cases.append(("E55 bài chưa khai af2 không bị đòi", not any("E55" in e for e in run(s))))
    for name, ok in cases:
        fails += not ok
        print(f"{'PASS' if ok else 'FAIL'} | {name}")
    print(f"tests E52/E55: {fails} FAIL")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
