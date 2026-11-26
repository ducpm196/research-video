import sys
s = sys.stdin.read().strip() or "09:12 09:49|env_split,preview_nonempty,two_person,cancel_tpl"
ts, gs = s.split("|")
t1s, t2s = ts.split()
to_m = lambda t: int(t.split(":")[0]) * 60 + int(t.split(":")[1])
guards = [x for x in gs.split(",") if x]
print(f"mins_delay={to_m(t2s) - to_m(t1s)} guards_passed={len(guards)}")
