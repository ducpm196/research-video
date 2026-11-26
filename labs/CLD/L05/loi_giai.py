import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
des = kv['desired'].split(','); cur = kv['running'].split(',') if kv.get('running') else []
miss = [p for p in des if p not in cur]; after = sorted(cur + miss)
print(f'created={miss}\nconverged={int(after == sorted(des))}')
