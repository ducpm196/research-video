# AF6 probe 6: lab "tính công thức" theo chặng (chỉ đọc). Cần p3_labs.tsv và p2_repeat_per_lesson.tsv. Chạy từ gốc kho.
import csv, collections, re
ST = {'S01': ['FND', 'JVA', 'JV2', 'PYT'], 'S02': ['BNK'], 'S03': ['BNX', 'SPB', 'BEP'], 'S04': ['INT', 'ACB'], 'S05': ['DMS', 'CS112', 'CS115a'],
      'S06': ['CPR', 'LNX', 'CSA', 'OSY', 'NET'], 'S07': ['SWF', 'SDP', 'DBS', 'WEB', 'SEC'], 'S08': ['DSY', 'EVT', 'DEN', 'CLD', 'CLC', 'DVO', 'SAR'],
      'S09': ['CS115b', 'AIF', 'DAN', 'DSC', 'MLP', 'MLO', 'IRS', 'LLM', 'AGT', 'RLN', 'CVI', 'AIP'], 'S10': ['TOC', 'PLC', 'PAR', 'HCI', 'SEP', 'CAS'], 'S11': ['RBM', 'ESY', 'ROB', 'GFX', 'BCH']}
def stage(c, l):
    n = int(l[1:])
    if c == 'PRJ': return 'S%02d' % (n + 1)
    if c == 'CS115': c = 'CS115a' if (n <= 21 or n >= 44) else 'CS115b'
    for s, cs in ST.items():
        if c in cs: return s
D = 'audit/review/audit_final/logs/af6/'
rows = list(csv.DictReader(open(D + 'p3_labs.tsv', encoding='utf-8'), delimiter='\t'))
rep = {r['lesson']: r for r in csv.DictReader(open(D + 'p2_repeat_per_lesson.tsv', encoding='utf-8'), delimiter='\t')}
agg = collections.defaultdict(collections.Counter)
REAL = {'sklearn', 'numpy', 'pandas', 'torch', 'sqlite3', 'pytest', 'matplotlib', 'socket', 'threading', 'subprocess'}
for r in rows:
    c, l = r['course'], r['lesson']; a = agg[stage(c, l)]; a['n'] += 1
    loc = int(r['sol_loc']); ext = r['ext']
    if ext == '.py':
        src = open(f'labs/{c}/{l}/loi_giai.py', encoding='utf-8', errors='replace').read()
        real = bool(set(re.findall(r'^\s*(?:import|from)\s+([A-Za-z_]\w*)', src, re.M)) & REAL)
    else:
        real = ext in ('.java', '.sql', '.sh', '.c', '.js', 'du_an')
    a['toy'] += (ext == '.py' and not real and loc <= 12)
    a['real'] += real
    a['loc30'] += loc >= 30
    p = rep.get(f'{c}:{l}')
    if p and int(p['practice_words']) and 100 * int(p['practice_shared']) / int(p['practice_words']) >= 50: a['tpl'] += 1
print('stage n toy real loc>=30 practice_tpl')
T = collections.Counter()
for s in sorted(agg):
    a = agg[s]; print(s, a['n'], a['toy'], a['real'], a['loc30'], a['tpl'])
    T.update(a)
print('ALL', dict(T))
