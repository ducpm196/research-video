import re, sys, collections
sys.stdout.reconfigure(encoding="utf-8")
rows = []
for p in range(1, 5):
    for line in open(rf"D:/research-video/audit/review/sample_e/part_{p}.md", encoding="utf-8"):
        c = [x.strip() for x in line.strip().strip("|").split("|")]
        if len(c) >= 12 and re.match(r"^[A-Z]+[0-9]* L\d+$", c[0]) and re.match(r"^[0-2]$", c[2] or "x"):
            rows.append(c)
print(len(rows), "bài")
names = ["P1", "P2", "P3", "P4", "P5", "P6", "P7"]
for i, n in enumerate(names):
    v = [int(r[2 + i]) for r in rows]
    cnt = collections.Counter(v)
    print(f"{n}: TB {sum(v)/len(v):.2f}  =2:{cnt[2]} =1:{cnt[1]} =0:{cnt[0]}")
print("Mất gốc:", collections.Counter(r[10] for r in rows))
mins = []
for r in rows:
    m = re.search(r"[\d,\.]+", r[1])
    if m:
        mins.append(float(m.group().replace(",", ".")))
mins.sort()
print("phút trung vị", mins[len(mins)//2], "min", mins[0], "max", mins[-1])
for r in rows:
    if r[10] != "ĐỦ":
        print(" ", r[0], r[9], r[10], "|", r[11][:150])
