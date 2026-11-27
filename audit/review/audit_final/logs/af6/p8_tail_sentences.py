# AF6 probe 8: "câu đuôi" = câu lời đọc được THÊM sau mốc 5d7f329 ở cảnh không phải Tự làm.
# Với từng step: so say cũ/mới theo (scene id, chỉ số step). Đếm câu thêm, câu thêm nằm cuối step,
# và câu thêm không có từ nội dung nào chung với show của step (dấu hiệu lệch màn hình). Chỉ đọc.
import glob, os, re, sys, collections, statistics, yaml

OLD = sys.argv[1]
Loader = getattr(yaml, 'CSafeLoader', yaml.SafeLoader)
SENT = re.compile(r'(?<=[.!?…])\s+')
ABS = re.compile(r'hoàn toàn|tuyệt đối|triệt để|dứt điểm|trọn vẹn|luôn luôn|không bao giờ|mọi trường hợp|tránh hẳn|xoá bỏ hoàn toàn|miễn nhiễm', re.I)


def steps(path):
    d = yaml.load(open(path, encoding='utf-8'), Loader=Loader)
    out = {}
    for sc in d.get('scenes', []):
        for i, st in enumerate(sc.get('steps') or []):
            if isinstance(st, dict) and isinstance(st.get('say'), str):
                out[(sc.get('id'), i)] = (sc.get('kind'), st.get('say').strip(), str(st.get('show') or ''))
    return out


def key(path):
    return os.path.basename(os.path.dirname(path)).upper() + ':' + os.path.basename(path).split('_')[0]


def words(s):
    return set(w for w in re.findall(r'[0-9a-zà-ỹđ]+', s.lower()) if len(w) >= 4 or w.isdigit())


new = {key(p): p for p in glob.glob('lessons/*/L*.yaml')}
old = {key(p): p for p in glob.glob(os.path.join(OLD, 'lessons', '*', 'L*.yaml'))}
rows = []
tot = collections.Counter()
kinds = collections.Counter()
detail = []
for k in sorted(new):
    if k not in old:
        continue
    sn, so = steps(new[k]), steps(old[k])
    old_all = set()
    for _, say, _ in so.values():
        old_all.update(s.strip() for s in SENT.split(say))
    n_add = n_tail = n_off = n_abs = w_add = 0
    for sk, (kind, say, show) in sn.items():
        if kind == 'practice':
            continue
        ss = [s.strip() for s in SENT.split(say) if s.strip()]
        showw = words(re.sub(r'<[^>]+>', ' ', show))
        for j, s in enumerate(ss):
            if s in old_all or len(s.split()) < 5:
                continue
            n_add += 1
            w_add += len(s.split())
            kinds[kind] += 1
            tail = j >= len(ss) - 2 and len(ss) > 1
            off = len(words(s) & showw) == 0
            ab = bool(ABS.search(s))
            n_tail += tail
            n_off += off
            n_abs += ab
            if tail and off:
                detail.append((k, sk[0], sk[1], int(ab), s))
    rows.append((k, n_add, w_add, n_tail, n_off, n_abs))
    tot['lessons'] += 1
    tot['added'] += n_add
    tot['added_words'] += w_add
    tot['tail'] += n_tail
    tot['off_screen'] += n_off
    tot['absolute_words'] += n_abs

here = os.path.dirname(__file__)
with open(os.path.join(here, 'p8_tail_per_lesson.tsv'), 'w', encoding='utf-8') as fo:
    fo.write('lesson\tadded_sent\tadded_words\ttail\toff_screen\tabsolute\n')
    for r in rows:
        fo.write('\t'.join(map(str, r)) + '\n')
with open(os.path.join(here, 'p8_tail_candidates.tsv'), 'w', encoding='utf-8') as fo:
    fo.write('lesson\tscene\tstep\tabsolute\tsentence\n')
    for r in detail:
        fo.write('\t'.join(map(str, r)) + '\n')
print(dict(tot))
print('by scene kind', kinds.most_common())
v = [r[1] for r in rows]
print('added sentences per lesson: median', statistics.median(v), 'p90', statistics.quantiles(v, n=10)[-1], 'max', max(v))
for thr in (1, 5, 10, 20):
    print(f'  lessons with >= {thr} added non-practice sentences:', sum(1 for x in v if x >= thr))
print('tail+off-screen candidates:', len(detail), 'in', len({d[0] for d in detail}), 'lessons; with absolute wording:', sum(d[3] for d in detail))
