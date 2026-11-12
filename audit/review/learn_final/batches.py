# Chia 537 bài của chặng 6–11 (chưa được đọc độc lập ở LS1/LF1) thành lô đọc, theo đúng thứ tự học.
# Chạy: PYTHONIOENCODING=utf-8 .venv/Scripts/python -B audit/review/learn_final/batches.py [cỡ lô]
# Ghi: audit/review/learn_final/batches.json  (danh sách lô; mỗi lô = chặng, các bài, các khoá đứng trước)
import sys, os, json
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(ROOT, "audit", "review", "learn_start"))
import pack

SIZE = int(sys.argv[1]) if len(sys.argv) > 1 else 13
cur = pack.load_cur()
st = pack.stages(cur)
batches, seen_courses, total = [], [], 0
for k, name, level, intro, items in st:
    if k < "S06":
        for C, l in items:
            if C not in seen_courses:
                seen_courses.append(C)
        continue
    # gom tham lam theo đúng thứ tự học trong chặng: mỗi lô không quá SIZE bài và không quá CAP KB đặc tả
    CAP = 400 * 1024
    part, size = [], 0
    def flush():
        global total
        if part:
            batches.append({
                "id": f"B{len(batches) + 1:02d}", "stage": k, "stage_name": name,
                "course": " ".join(dict.fromkeys(C for C, _ in part)),
                "before": list(seen_courses),
                "lessons": [{"course": C, "id": l["id"], "title": l["title"], "spec": l["spec"]} for C, l in part],
            })
            total += len(part)
            for C, _ in part:
                if C not in seen_courses:
                    seen_courses.append(C)
    for C, l in items:
        sz = os.path.getsize(os.path.join(ROOT, l["spec"]))
        if part and (len(part) >= SIZE or size + sz > CAP):
            flush(); part, size = [], 0
        part.append((C, l)); size += sz
    flush()
json.dump(batches, open(os.path.join(HERE, "batches.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for b in batches:
    kb = sum(os.path.getsize(os.path.join(ROOT, l["spec"])) for l in b["lessons"]) // 1024
    print(b["id"], b["stage"], b["course"], len(b["lessons"]), "bài", f"{kb} KB", " ".join(l["course"]+":"+l["id"] for l in b["lessons"]))
print("tổng", total, "bài,", len(batches), "lô")
