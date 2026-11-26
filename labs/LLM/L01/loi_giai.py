import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
p = eval(kv['p']) if '/' in kv['p'] else float(kv['p'])
ppl = p ** (-1.0 / int(kv['steps'])); add1 = 1.0 / (int(kv['ctx']) + int(kv['vocab']))
print(f'perplexity={ppl:.3f} add1_unseen={add1:.3f}')
