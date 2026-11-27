# AF6 probe 9: kiểm lại các phát hiện PR-01, PR-02, PR-09, PR-19 của bản phản biện kế hoạch. Chỉ đọc.
import glob, os, re, sys, json, difflib, collections, yaml
OLD = sys.argv[1]
Loader = getattr(yaml, 'CSafeLoader', yaml.SafeLoader)
SENT = re.compile(r'(?<=[.!?…])\s+')
def key(p): return os.path.basename(os.path.dirname(p)).upper() + ':' + os.path.basename(p).split('_')[0]
def steps(path):
    d = yaml.load(open(path, encoding='utf-8'), Loader=Loader); out = {}
    for sc in d.get('scenes', []):
        for i, st in enumerate(sc.get('steps') or []):
            if isinstance(st, dict):
                out[(sc.get('id'), i)] = (sc.get('kind'), str(st.get('say') or '').strip(), str(st.get('show') or ''), 'focus' in st, st.get('pause') or 0)
    return out
new = {key(p): p for p in glob.glob('lessons/*/L*.yaml')}
old = {key(p): p for p in glob.glob(os.path.join(OLD, 'lessons', '*', 'L*.yaml'))}
mute = edits = infocus = show_changed = steps_c = 0
pause_share = []
for k in sorted(new):
    sn = steps(new[k])
    # pause share from build report timeline if available
    c, l = k.split(':')
    tot_pause = sum(float(v[4]) for v in sn.values())
    br = f'out/{c}/{l}/build_report.json'
    try:
        dur = json.load(open(br, encoding='utf-8')).get('duration') or 0
    except Exception:
        dur = 0
    if dur: pause_share.append((tot_pause / dur, k))
    if k not in old: continue
    so = steps(old[k])
    old_all = set()
    for v in so.values(): old_all.update(s.strip() for s in SENT.split(v[1]))
    for sk, (kind, say, show, hasfocus, _) in sn.items():
        if sk in so and so[sk][2] != show: show_changed += 1
        if kind == 'practice': continue
        ss = [s.strip() for s in SENT.split(say) if s.strip()]
        added = [s for s in ss if s not in old_all and len(s.split()) >= 5]
        if not added: continue
        if len(added) == len([s for s in ss if len(s.split()) >= 5]): mute += 1
        if hasfocus: infocus += len(added)
        olds = [s.strip() for s in SENT.split(so[sk][1])] if sk in so else []
        gone = [s for s in olds if s not in ss]
        for a in added:
            if any(difflib.SequenceMatcher(None, a, g).ratio() >= 0.6 for g in gone): edits += 1
print('steps where every (>=5-word) sentence is added -> would go mute:', mute)
print('added sentences that are edits of a removed old sentence (ratio>=0.6):', edits)
print('added sentences inside steps having focus:', infocus)
print('steps (same scene id + index) whose show changed:', show_changed)
ps = sorted(pause_share, reverse=True)
print('lessons with duration:', len(ps), '; pause share >10%:', sum(1 for x, _ in ps if x > 0.10), '>20%:', sum(1 for x, _ in ps if x > 0.20), 'max', ps[:3])
