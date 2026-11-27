# AF6 probe 3: hồ sơ lab (chỉ đọc): độ dài đề, độ dài lời giải, ngôn ngữ, thư viện, ca ẩn, chế độ.
import os, re, glob, collections, statistics

rows = []
imports = collections.Counter()
for d in sorted(glob.glob('labs/*/L*')):
    if not os.path.isdir(d):
        continue
    c, l = d.replace('\\', '/').split('/')[1:3]
    de = os.path.join(d, 'de.md')
    de_words = len(open(de, encoding='utf-8', errors='replace').read().split()) if os.path.exists(de) else -1
    sols = [f for f in glob.glob(os.path.join(d, 'loi_giai*')) if os.path.isfile(f)]
    proj = os.path.isdir(os.path.join(d, 'loi_giai'))
    ext = ''
    loc = 0
    if sols:
        ext = os.path.splitext(sols[0])[1]
        src = open(sols[0], encoding='utf-8', errors='replace').read()
        loc = sum(1 for x in src.splitlines() if x.strip() and not x.strip().startswith(('#', '//')))
        if ext == '.py':
            for m in re.finditer(r'^\s*(?:import|from)\s+([A-Za-z_][\w]*)', src, re.M):
                imports[m.group(1)] += 1
    elif proj:
        ext = 'du_an'
        for root, _, fs in os.walk(os.path.join(d, 'loi_giai')):
            for f in fs:
                if f.endswith(('.java', '.py', '.js', '.sql', '.sh', '.c', '.go', '.yaml', '.yml', '.xml')):
                    try:
                        loc += sum(1 for x in open(os.path.join(root, f), encoding='utf-8', errors='replace') if x.strip())
                    except OSError:
                        pass
    ca = os.path.isdir(os.path.join(d, 'ca_an'))
    n_ca = len(glob.glob(os.path.join(d, 'ca_an', '*.in'))) + len(glob.glob(os.path.join(d, 'ca_an', 'in_*'))) + len(glob.glob(os.path.join(d, 'ca_an', 'args_*'))) + len(glob.glob(os.path.join(d, 'ca_an', 'seed_*'))) if ca else 0
    ham = os.path.exists(os.path.join(d, 'ca_an', 'ham.json'))
    kiem = os.path.isdir(os.path.join(d, 'kiem'))
    bang = os.path.exists(os.path.join(d, 'bang_kiem.md'))
    md = os.path.join(d, 'mong_doi.txt')
    md_lines = sum(1 for x in open(md, encoding='utf-8', errors='replace') if x.strip()) if os.path.exists(md) else -1
    rows.append((c, l, ext, de_words, loc, md_lines, int(ca), n_ca, int(ham), int(kiem), int(bang)))

out = os.path.join(os.path.dirname(__file__), 'p3_labs.tsv')
with open(out, 'w', encoding='utf-8') as fo:
    fo.write('course\tlesson\text\tde_words\tsol_loc\tmong_doi_lines\tca_an\tn_ca\tham_json\tkiem\tbang_kiem\n')
    for r in rows:
        fo.write('\t'.join(map(str, r)) + '\n')
print('labs', len(rows))
print('ext', collections.Counter(r[2] for r in rows).most_common())
print('ca_an dirs', sum(r[6] for r in rows), 'ham.json', sum(r[8] for r in rows), 'kiem', sum(r[9] for r in rows), 'bang_kiem', sum(r[10] for r in rows))
print('no ca_an/kiem/bang', sum(1 for r in rows if not (r[6] or r[9] or r[10])))
for name, idx in (('de_words', 3), ('sol_loc', 4), ('mong_doi_lines', 5)):
    v = [r[idx] for r in rows if r[idx] >= 0]
    q = statistics.quantiles(v, n=10)
    print(name, 'min', min(v), 'p10', q[0], 'median', statistics.median(v), 'p90', q[-1], 'max', max(v))
print('labs with sol_loc <= 6:', sum(1 for r in rows if 0 < r[4] <= 6), '; <= 10:', sum(1 for r in rows if 0 < r[4] <= 10), '; >= 40:', sum(1 for r in rows if r[4] >= 40))
print('labs with mong_doi 1 line:', sum(1 for r in rows if r[5] == 1), '; <=2:', sum(1 for r in rows if 0 < r[5] <= 2))
print('labs with de_words <= 60:', sum(1 for r in rows if 0 <= r[3] <= 60), '; <= 100:', sum(1 for r in rows if 0 <= r[3] <= 100))
print('python imports', imports.most_common(40))
by = collections.defaultdict(list)
for r in rows:
    by[r[0]].append(r)
print('\ncourse  n  ext  med_de_words  med_sol_loc  med_out_lines  ca_an')
for c, rs in sorted(by.items()):
    exts = ','.join(f'{k}{v}' for k, v in collections.Counter(r[2] for r in rs).most_common())
    print(f'{c:6s} {len(rs):3d} {exts:28s} {statistics.median(r[3] for r in rs):6.0f} {statistics.median(r[4] for r in rs):6.0f} {statistics.median(r[5] for r in rs):5.0f} {sum(r[6] or r[9] for r in rs):3d}')
