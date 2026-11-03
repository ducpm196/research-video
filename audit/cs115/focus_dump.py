"""In mọi step cần `focus` mà chưa có (tiêu chí như focus_gap.py), kèm nội dung từng phần của khối (chữ, công thức,
từng dòng bảng/mục danh sách) và từng câu đánh số, để đặt focus đúng chỗ câu đang nói. Chạy: focus_dump.py Lxx [--all]"""
import html as H
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import lv  # noqa: E402

COURSE = __import__("os").environ.get("LV_COURSE", "cs115")  # khoá: LV_COURSE=cs112


def units(src):
    src = lv.MATH_RE.sub(lambda m: "<m>" + H.escape(m.group(0)) + "</m>", src)
    root = {"tag": "root", "kids": [], "text": []}
    stack = [root]

    class P(HTMLParser):
        def handle_starttag(self, tag, attrs):
            node = {"tag": tag, "kids": [], "text": []}
            if tag != "br":
                stack[-1]["kids"].append(node)
            if tag not in lv.VOID_TAGS:
                stack.append(node)

        def handle_endtag(self, tag):
            for k in range(len(stack) - 1, 0, -1):
                if stack[k]["tag"] == tag:
                    del stack[k:]
                    break

        def handle_data(self, d):
            for n in stack[1:]:
                n["text"].append(d)
    P(convert_charrefs=True).feed(src)

    def rows(n):
        if n["tag"] == "table":
            return [r for k in n["kids"] for r in (k["kids"] if k["tag"] in ("tbody", "thead") else [k]) if r["tag"] == "tr"]
        return n["kids"]
    for n in root["kids"]:
        n["kids"] = rows(n)
    return root["kids"]


def txt(n, w):
    t = re.sub(r"\s+", " ", "".join(n["text"])).strip()
    return t[:w] + ("…" if len(t) > w else "")


def show_block(us, pre):
    for i, u in enumerate(us, 1):
        print(f"{pre}{i} <{u['tag']}> {txt(u, 120)}")
        if len(u["kids"]) >= 2:
            for j, k in enumerate(u["kids"], 1):
                print(f"{pre}   {i}.{j} <{k['tag']}> {txt(k, 100)}")


def main():
    lid, show_all = sys.argv[1], "--all" in sys.argv
    p = next((ROOT / "lessons" / COURSE).glob(lid + "_*.yaml"))
    sp = lv.load_spec(p)
    for sc in sp["scenes"]:
        blocks = []
        for ki, st in enumerate(sc["steps"]):
            if st.get("clear"):
                blocks = []
            if st.get("show"):
                blocks.append(units(str(st["show"])))
            sents = lv.sentences(st["say"])
            n_units = len(blocks[-1]) if st.get("show") else 0
            need = len(sents) >= 2 and (n_units >= 2 or (not st.get("show") and len(blocks) >= 2))
            if not (show_all or (need and st.get("focus") is None)):
                continue
            print(f"\n=== {sc['id']}.{ki} [{sc['kind']}] {len(sents)} câu, focus={st.get('focus')}")
            if st.get("show"):
                for b in range(len(blocks) - 1):
                    print(f"  (B{b + 1} trên bảng: {' | '.join(txt(u, 40) for u in blocks[b])[:150]})")
                show_block(blocks[-1], "  ")
            else:
                for b, us in enumerate(blocks, 1):
                    print(f"  -- B{b}:")
                    show_block(us, f"    B{b}:")
            for j, s in enumerate(sents, 1):
                print(f"  {j}. {s}")


if __name__ == "__main__":
    main()
