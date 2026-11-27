# AF6 probe 2: câu lời đọc (say) lặp lại giữa nhiều bài -> dấu hiệu sinh hàng loạt / câu đệm.
# Chỉ đọc. In: thống kê lặp theo câu nguyên văn và theo "khung câu" (đã thay số/từ trong ngoặc/backtick bằng #).
import glob, os, re, sys, collections, yaml, json

try:
    Loader = yaml.CSafeLoader
except AttributeError:
    Loader = yaml.SafeLoader

SENT = re.compile(r'(?<=[.!?…])\s+')


def says(node, kind=None, sid=None, out=None):
    if out is None:
        out = []
    if isinstance(node, dict):
        k = node.get('kind', kind) if 'kind' in node and 'id' in node else kind
        s = node.get('id', sid) if 'kind' in node and 'id' in node else sid
        for key, v in node.items():
            if key == 'say' and isinstance(v, str):
                out.append((k, s, v))
            else:
                says(v, k, s, out)
    elif isinstance(node, list):
        for v in node:
            says(v, kind, sid, out)
    return out


def frame(s):
    s = s.lower()
    s = re.sub(r'`[^`]*`', '#', s)
    s = re.sub(r'\$[^$]*\$', '#', s)
    s = re.sub(r'[“"][^”"]*[”"]', '#', s)
    s = re.sub(r'\d+([.,]\d+)*', '#', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s


exact = collections.defaultdict(set)   # sentence -> lessons
fr = collections.defaultdict(set)
per_lesson = {}
kind_of = collections.defaultdict(collections.Counter)
files = sorted(glob.glob('lessons/*/L*.yaml'))
for f in files:
    course = os.path.basename(os.path.dirname(f)).upper()
    lid = course + ':' + os.path.basename(f).split('_')[0]
    d = yaml.load(open(f, encoding='utf-8'), Loader=Loader)
    sents = []
    for kind, sid, text in says(d.get('scenes', d)):
        for s in SENT.split(text.strip()):
            s = s.strip()
            if len(s.split()) >= 6:
                sents.append((kind, s))
                exact[s].add(lid)
                fr[frame(s)].add(lid)
                kind_of[frame(s)][kind] += 1
    per_lesson[lid] = sents

print('lessons', len(files), 'sentences(>=6 words)', sum(len(v) for v in per_lesson.values()))
for thr in (5, 10, 20, 50, 100):
    n = sum(1 for s, ls in exact.items() if len(ls) >= thr)
    m = sum(1 for s, ls in fr.items() if len(ls) >= thr)
    print(f'exact sentences in >={thr} lessons: {n}; frames in >={thr} lessons: {m}')

print('\n== top 60 frames by number of lessons')
top = sorted(fr.items(), key=lambda kv: -len(kv[1]))[:60]
for s, ls in top:
    courses = len({x.split(':')[0] for x in ls})
    print(f'{len(ls):4d} bài / {courses:2d} khoá | {dict(kind_of[s].most_common(2))} | {s[:150]}')

# per-lesson share of words that sit in frames shared by >=20 lessons
rows = []
for lid, sents in per_lesson.items():
    tot = sum(len(s.split()) for _, s in sents) or 1
    shared = sum(len(s.split()) for _, s in sents if len(fr[frame(s)]) >= 20)
    prac_tot = sum(len(s.split()) for k, s in sents if k == 'practice') or 0
    prac_sh = sum(len(s.split()) for k, s in sents if k == 'practice' and len(fr[frame(s)]) >= 20)
    rows.append((lid, tot, shared, round(100 * shared / tot, 1), prac_tot, prac_sh))
rows.sort(key=lambda r: -r[3])
out = os.path.join(os.path.dirname(__file__), 'p2_repeat_per_lesson.tsv')
with open(out, 'w', encoding='utf-8') as fo:
    fo.write('lesson\twords\tshared_words\tshared_pct\tpractice_words\tpractice_shared\n')
    for r in rows:
        fo.write('\t'.join(map(str, r)) + '\n')
import statistics
p = [r[3] for r in rows]
print('\nshare of spoken words in frames shared by >=20 lessons: median', statistics.median(p), 'p90', statistics.quantiles(p, n=10)[-1], 'max', max(p))
for thr in (10, 20, 30, 50):
    print(f'  lessons with shared share >= {thr}%:', sum(1 for x in p if x >= thr))
pr = [(r[0], r[4], r[5]) for r in rows if r[4]]
print('lessons with practice scene words:', len(pr))
for thr in (30, 50, 80):
    print(f'  practice >= {thr}% shared frames:', sum(1 for _, a, b in pr if 100 * b / a >= thr))
bycourse = collections.defaultdict(list)
for r in rows:
    bycourse[r[0].split(':')[0]].append(r[3])
print('\ncourse median shared% (desc)')
print(' '.join(f'{c}:{statistics.median(v):.0f}' for c, v in sorted(bycourse.items(), key=lambda kv: -statistics.median(kv[1]))))
