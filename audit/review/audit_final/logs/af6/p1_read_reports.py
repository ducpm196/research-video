# AF6 probe 1: hồ sơ 806 báo cáo đọc độc lập read_af5 (chỉ đọc).
import os, re, glob, hashlib, collections, statistics, time

root = 'audit/review/read_af5'
fs = glob.glob(root + '/**/*.md', recursive=True)
print('files', len(fs))
per = [f for f in fs if re.match(r'L\d+\.md$', os.path.basename(f))]
print('per-lesson', len(per), 'other', [os.path.relpath(f, root) for f in fs if f not in per][:30])
sizes = [os.path.getsize(f) for f in per]
print('size min/med/max', min(sizes), statistics.median(sizes), max(sizes))
print('size deciles', [int(x) for x in statistics.quantiles(sizes, n=10)])
noerr = 0
must = 0
should = 0
bodyhash = collections.Counter()
pscore = collections.Counter()
mt = collections.Counter()
lines_all = collections.Counter()
chuakiem = 0
frames_named = 0
for f in per:
    t = open(f, encoding='utf-8', errors='replace').read()
    if 'Không phát hiện lỗi' in t:
        noerr += 1
    must += len(re.findall(r'^\|\s*\**MUST', t, re.M))
    should += len(re.findall(r'^\|\s*\**SHOULD', t, re.M))
    if 'CHƯA KIỂM' in t:
        chuakiem += 1
    if re.search(r'f_?\d{3,}|frame|\.png', t):
        frames_named += 1
    m = re.search(r'Điểm:.*', t)
    if m:
        pscore[re.sub(r'\s+', ' ', m.group(0))[:140]] += 1
    body = re.sub(r'^#.*\n', '', t, count=1)
    bodyhash[hashlib.md5(body.encode()).hexdigest()] += 1
    mt[time.strftime('%m-%d %H', time.gmtime(os.path.getmtime(f)))] += 1
    for ln in t.splitlines():
        ln = ln.strip()
        if len(ln) > 40:
            lines_all[ln] += 1
print('noerr', noerr, 'MUST rows', must, 'SHOULD rows', should, 'CHUA KIEM files', chuakiem, 'names a frame', frames_named)
print('distinct bodies', len(bodyhash), 'top dup', bodyhash.most_common(3))
print('distinct pscore lines', len(pscore))
for k, c in pscore.most_common(8):
    print('  ', c, k)
print('mtime hours (UTC)')
for k, c in sorted(mt.items()):
    print('  ', k, c)
print('most repeated long lines')
for k, c in lines_all.most_common(30):
    print('  ', c, k[:170])
