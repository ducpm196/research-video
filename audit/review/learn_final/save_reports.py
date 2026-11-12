# Trích báo cáo cuối của từng người đọc từ nhật ký tác vụ (JSONL) và lưu vào audit/review/learn_final/reports/Bxx.md.
# Người đọc phụ không ghi được tệp, nên người điều phối trích từ nhật ký. Không in nội dung ra màn hình.
# Chạy: PYTHONIOENCODING=utf-8 .venv/Scripts/python -B audit/review/learn_final/save_reports.py <thư mục tasks> Bxx=<agentId> ...
import sys, os, json, re
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "reports")
os.makedirs(OUT, exist_ok=True)


def strings(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for v in o.values():
            yield from strings(v)
    elif isinstance(o, list):
        for v in o:
            yield from strings(v)


tasks = sys.argv[1]
for pair in sys.argv[2:]:
    bid, aid = pair.split("=")
    p = os.path.join(tasks, aid + ".output")
    best = ""
    with open(p, encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                o = json.loads(line)
            except Exception:
                continue
            if o.get("type") != "assistant":
                continue
            for s in strings(o.get("message", o)):
                if re.search(r"ĐÃ ĐỌC \d+/\d+ bài", s) and "| Bài |" in s and len(s) > len(best):
                    best = s
    if not best:
        print(bid, "KHÔNG TÌM THẤY báo cáo trong", p)
        continue
    m = re.search(r"ĐÃ ĐỌC (\d+)/(\d+) bài", best)
    must = len(re.findall(r"^\s*\|[^|\n]*\|\s*MUST", best, re.M))
    block = len(re.findall(r"^\s*\|[^|\n]*\|\s*BLOCK", best, re.M))
    should = len(re.findall(r"^\s*\|[^|\n]*\|\s*SHOULD", best, re.M))
    open(os.path.join(OUT, bid + ".md"), "w", encoding="utf-8").write(
        f"<!-- lô {bid}; trích từ nhật ký tác vụ {aid}; nguyên văn báo cáo của người đọc độc lập -->\n" + best.strip() + "\n")
    print(f"{bid}: ĐÃ ĐỌC {m.group(1)}/{m.group(2)} · MUST {must} · BLOCK {block} · SHOULD {should} · {len(best)} ký tự → reports/{bid}.md")
