# Liệt kê bài đã đổi so với ảnh chụp trước khi sửa, và đưa vào hàng dựng lại các bài thuộc lô đã áp xong.
# Chạy: PYTHONIOENCODING=utf-8 .venv/Scripts/python -B audit/review/learn_final/changed.py <thư mục snap/lessons> [--queue B01 B02 … | --queue-all]
#   không có --queue: chỉ in danh sách bài đã đổi (theo lô).
import sys, os, json, glob, filecmp
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
snap = sys.argv[1]
args = sys.argv[2:]
batches = json.load(open(os.path.join(HERE, "batches.json"), encoding="utf-8"))
where = {}
for b in batches:
    for l in b["lessons"]:
        where[os.path.normpath(l["spec"])] = (b["id"], l["course"], l["id"])
changed, new = [], []
for p in sorted(glob.glob(os.path.join(ROOT, "lessons", "*", "L*.yaml"))):
    rel = os.path.normpath(os.path.relpath(p, ROOT))
    old = os.path.join(snap, os.path.relpath(p, os.path.join(ROOT, "lessons")))
    C = os.path.basename(os.path.dirname(p)).upper()
    lid = os.path.basename(p)[:3]
    if not os.path.exists(old):
        new.append((C, lid))
    elif not filecmp.cmp(p, old, shallow=False):
        changed.append((where.get(rel, ("ngoài lô", C, lid))[0], C, lid))
by = {}
for b, C, lid in changed:
    by.setdefault(b, []).append(f"{C} {lid}")
for b in sorted(by):
    print(b, len(by[b]), "·", ", ".join(by[b]))
print("tổng bài đã đổi:", len(changed), "| bài mới (chưa có trong ảnh chụp):", len(new), " ".join(f"{C}:{l}" for C, l in new))
if args and args[0] in ("--queue", "--queue-all"):
    want = set(args[1:])
    q = os.path.join(HERE, "rebuild.queue")
    have = set(open(q, encoding="utf-8").read().split("\n")) if os.path.exists(q) else set()
    add = [f"{C} {lid}" for b, C, lid in changed if (args[0] == "--queue-all" or b in want) and f"{C} {lid}" not in have]
    with open(q, "a", encoding="utf-8", newline="\n") as f:
        for x in add:
            f.write(x + "\n")
    print("thêm vào hàng dựng:", len(add), "·", ", ".join(add))
