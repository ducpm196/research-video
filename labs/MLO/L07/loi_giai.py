import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
o = [float(x) for x in kv['old'].split(',')]; nw = [float(x) for x in kv['new'].split(',')]; th = float(kv['thr'])
dis = sum(int((a >= th) != (b >= th)) for a, b in zip(o, nw))
print(f'served=old disagree={dis}/{len(o)}')
