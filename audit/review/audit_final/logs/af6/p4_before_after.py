# AF6 probe 4: so lời đọc từng bài giữa mốc 5d7f329 (thư mục cũ truyền qua argv[1]) và HEAD.
# Chỉ đọc. In: số từ trước/sau, câu thêm mới theo loại cảnh, đỉnh dồn sát ngưỡng 1300 từ.
import glob, os, re, sys, collections, statistics, yaml

OLD = sys.argv[1]
try:
    Loader = yaml.CSafeLoader
except AttributeError:
    Loader = yaml.SafeLoader
SENT = re.compile(r'(?<=[.!?…])\s+')


def load(path):
    d = yaml.load(open(path, encoding='utf-8'), Loader=Loader)
    res = []  # (kind, sentence)
    for sc in d.get('scenes', []):
        kind = sc.get('kind')

        def walk(n):
            if isinstance(n, dict):
                for k, v in n.items():
                    if k == 'say' and isinstance(v, str):
                        for s in SENT.split(v.strip()):
                            if s.strip():
                                res.append((kind, s.strip()))
                    else:
                        walk(v)
            elif isinstance(n, list):
                for v in n:
                    walk(v)
        walk(sc)
    return res


def key(path):
    c = os.path.basename(os.path.dirname(path)).upper()
    return c + ':' + os.path.basename(path).split('_')[0]


new = {key(p): p for p in glob.glob('lessons/*/L*.yaml')}
old = {key(p): p for p in glob.glob(os.path.join(OLD, 'lessons', '*', 'L*.yaml'))}
print('new', len(new), 'old', len(old), 'only new', len(set(new) - set(old)), 'only old', sorted(set(old) - set(new))[:10])

A_COURSES = {'FND', 'PYT', 'JVA', 'JV2', 'BNK', 'BNX', 'DMS', 'CS112', 'INT', 'ACB'}
rows = []
added_frames = collections.defaultdict(set)
added_kind = collections.Counter()
wc_new = {}
for k, p in sorted(new.items()):
    sn = load(p)
    wn = sum(len(s.split()) for _, s in sn)
    wc_new[k] = wn
    if k not in old:
        rows.append((k, 0, wn, 0, 0, 0, 'NEW'))
        continue
    so = load(old[k])
    wo = sum(len(s.split()) for _, s in so)
    oset = {s for _, s in so}
    nset = {s for _, s in sn}
    add = [(kd, s) for kd, s in sn if s not in oset]
    rem = [(kd, s) for kd, s in so if s not in nset]
    aw = sum(len(s.split()) for _, s in add)
    rw = sum(len(s.split()) for _, s in rem)
    for kd, s in add:
        f = re.sub(r'\d+([.,]\d+)*', '#', s.lower())
        added_frames[f].add(k)
        added_kind[kd] += len(s.split())
    rows.append((k, wo, wn, aw, rw, len(add), 'SAME' if not add and not rem else 'CHANGED'))

out = os.path.join(os.path.dirname(__file__), 'p4_before_after.tsv')
with open(out, 'w', encoding='utf-8') as fo:
    fo.write('lesson\twords_old\twords_new\tadded_words\tremoved_words\tadded_sentences\tstatus\n')
    for r in rows:
        fo.write('\t'.join(map(str, r)) + '\n')

st = collections.Counter(r[6] for r in rows)
print('status', dict(st))
ch = [r for r in rows if r[6] == 'CHANGED']
print('changed lessons: total words old', sum(r[1] for r in ch), 'new', sum(r[2] for r in ch), 'added', sum(r[3] for r in ch), 'removed', sum(r[4] for r in ch))
print('all lessons words old', sum(r[1] for r in rows), 'new', sum(r[2] for r in rows))
print('added words by scene kind', added_kind.most_common())


def cls(k):
    c, l = k.split(':')
    n = int(l[1:])
    if c in A_COURSES or (c == 'CS115' and (n <= 21 or n >= 44)):
        return 'A'
    if c in {'CPR', 'LNX', 'MLP', 'PRJ'}:
        return 'B'
    if c in {'SPB', 'BEP', 'AIP'}:
        return 'N'
    return 'C'


bycls = collections.defaultdict(list)
for r in rows:
    bycls[cls(r[0])].append(r)
for c, rs in sorted(bycls.items()):
    chg = [r for r in rs if r[6] == 'CHANGED']
    print(f'class {c}: n={len(rs)} changed={len(chg)} same={sum(1 for r in rs if r[6]=="SAME")} new={sum(1 for r in rs if r[6]=="NEW")} '
          f'median words old={statistics.median([r[1] for r in rs]) if rs else 0} new={statistics.median([r[2] for r in rs])} '
          f'median added={statistics.median([r[3] for r in chg]) if chg else 0} removed={statistics.median([r[4] for r in chg]) if chg else 0}')

# histogram of new word counts around the 1300 threshold
v = list(wc_new.values())
print('\nword count histogram (new):')
for lo in range(900, 2600, 100):
    print(f'  {lo}-{lo+99}: {sum(1 for x in v if lo <= x < lo+100)}')
print('  <1300:', sum(1 for x in v if x < 1300), ' 1300-1349:', sum(1 for x in v if 1300 <= x < 1350), ' 1350-1399:', sum(1 for x in v if 1350 <= x < 1400))
vo = [r[1] for r in rows if r[1]]
print('old: <1300:', sum(1 for x in vo if x < 1300), ' 1300-1349:', sum(1 for x in vo if 1300 <= x < 1350))

print('\n== top 50 ADDED sentence frames shared across lessons')
for f, ls in sorted(added_frames.items(), key=lambda kv: -len(kv[1]))[:50]:
    print(f'{len(ls):4d} | {f[:170]}')
multi = sum(1 for f, ls in added_frames.items() if len(ls) >= 5)
print('added frames appearing in >=5 lessons:', multi, 'of', len(added_frames))
