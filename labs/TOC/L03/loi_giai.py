import sys, re
s = sys.stdin.read().strip() or "^(0|1)*10$;10;7"
pat_s, end_s, ls = s.split(";")
pat = re.compile(pat_s); max_l = int(ls)
ok, cnt = True, 0
for L in range(max_l + 1):
    for m in range(1 << L):
        w = format(m, f"0{L}b") if L else ""
        hit = bool(pat.fullmatch(w))
        if hit != w.endswith(end_s): ok = False
        cnt += int(hit)
print(f"matches={cnt} exact={int(ok)}")
