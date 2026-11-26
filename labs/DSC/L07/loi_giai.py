import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
p = lambda s: tuple(int(x) for x in s.split(','))
a1, a2, b1, b2 = p(kv['asm']), p(kv['alg']), p(kv['bsm']), p(kv['blg'])
won = int((a1[0] / a1[1] > b1[0] / b1[1]) and (a2[0] / a2[1] > b2[0] / b2[1]))
pa = (a1[0] + a2[0]) / (a1[1] + a2[1]); pb = (b1[0] + b2[0]) / (b1[1] + b2[1])
print(f'sub_A_wins={won} pooled_A={pa:.3f} pooled_B={pb:.3f}')
