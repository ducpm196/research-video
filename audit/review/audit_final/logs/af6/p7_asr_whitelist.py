# AF6 probe 7: hồ sơ các mục asr_reviewed (chỉ đọc). Chạy từ gốc kho.
import yaml, glob, re, collections
tot = tpl = 0
hist = collections.Counter(); les = set(); subs = collections.Counter()
for p in glob.glob('lessons/*/L*.yaml'):
    d = yaml.load(open(p, encoding='utf-8'), Loader=yaml.CSafeLoader)
    for e in d.get('asr_reviewed') or []:
        tot += 1
        r = str(e.get('reason') if isinstance(e, dict) else '')
        if 'NOT_VERIFIED bằng tai người' in r:
            tpl += 1; les.add(p)
            m = re.search(r'\((0\.\d+|1\.0+)\)', r)
            if m:
                v = float(m.group(1))
                hist['<0.70' if v < 0.7 else '0.70-0.79' if v < 0.8 else '0.80-0.89' if v < 0.9 else '>=0.90'] += 1
            for a, b in re.findall(r'“([^”]+)” → nghe thành “([^”]+)”', r):
                subs[(a.lower(), b.lower())] += 1
print('asr_reviewed entries', tot, 'auto-reason (NOT_VERIFIED bằng tai người)', tpl, 'lessons', len(les))
print('similarity histogram', dict(hist))
print('top heard-as pairs')
for (a, b), c in subs.most_common(40):
    print(' ', c, a, '->', b)
