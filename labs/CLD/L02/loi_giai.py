import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
layers = kv['layers'].split(',')
print(f'hits_src_change={layers.index(kv["ch1"])}\nhits_req_change={layers.index(kv["ch2"])}')
