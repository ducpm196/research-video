import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
theo = int(kv['chips']) * int(kv['per_chip']); eff = int(kv['real_pos']) / theo * 100.0
sim_s = round(int(kv['sims']) / float(kv['secs'])); dr = int(kv['games']) - int(kv['wins']) - int(kv['losses'])
print(f'deepblue_eff={eff:.1f}% sim_rate={sim_s}/s az_draws={dr}')
