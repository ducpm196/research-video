"""Mẫu H — tổng hợp từ part_1..4.md: số bài có MUST, số MUST/SHOULD theo tầng, khoảng Wilson 95%.
Chạy: .venv/Scripts/python -B audit/review/sample_h/tally.py"""
import json, math, pathlib, re, sys, collections
sys.stdout.reconfigure(encoding="utf-8")
D = pathlib.Path(__file__).resolve().parent
S = {(x["course"], x["lesson"]): x for x in json.loads((D / "sample_h.json").read_text(encoding="utf-8"))}
must = collections.Counter(); should = collections.Counter(); verdict = {}
for p in sorted(D.glob("part_*.md")):
    for ln in p.read_text(encoding="utf-8").splitlines():
        m = re.match(r"\s*\|\s*([A-Z0-9]+) (L\d\d)\s*\|\s*(MUST|SHOULD)", ln)
        if m and (m.group(1), m.group(2)) in S:
            (must if m.group(3) == "MUST" else should)[(m.group(1), m.group(2))] += 1
        m = re.match(r"\s*\|\s*([A-Z0-9]+) (L\d\d)\s*\|.*\|\s*(ĐỦ|GẦN|CHƯA)\b", ln)
        if m and (m.group(1), m.group(2)) in S:
            verdict[(m.group(1), m.group(2))] = m.group(3)
def wilson(k, n, z=1.96):
    if n == 0: return (0, 0)
    p = k / n; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (round(100 * (c - h), 1), round(100 * (c + h), 1))
HAND = {"FND", "JVA", "JV2", "PYT", "BNK", "BNX", "INT", "ACB", "DMS", "CS112"}
groups = collections.defaultdict(list)
for k, x in S.items():
    groups["tầng " + x["stratum"]].append(k)
    groups["LỚP A soạn tay (chặng 1–5)" if k[0] in HAND else "LỚP B+C khoá mới + nâng hàng loạt"].append(k)
    groups["TOÀN MẪU"].append(k)
print(f"đã chấm kết luận mất gốc cho {len(verdict)}/{len(S)} bài")
for g in sorted(groups):
    ks = groups[g]; n = len(ks); k = sum(1 for x in ks if must[x])
    v = collections.Counter(verdict.get(x, "?") for x in ks)
    print(f"{g:<38} bài {n:>2} | có MUST {k:>2} ({100*k/n:.0f}%, Wilson95 {wilson(k,n)}) | MUST {sum(must[x] for x in ks):>2} SHOULD {sum(should[x] for x in ks):>3} | {dict(v)}")
print("bài có MUST:", ", ".join(f"{c} {l}×{must[(c,l)]}" for (c, l) in sorted(S) if must[(c, l)]))
print("bài không MUST:", ", ".join(f"{c} {l}" for (c, l) in sorted(S) if not must[(c, l)]))
