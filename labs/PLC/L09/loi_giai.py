import sys
s = sys.stdin.read().strip() or "10 20"
v1, v2 = map(int, s.split())
def bad(x, lst=[]): lst.append(x); return lst
def good(x, lst=None): lst = [] if lst is None else lst; lst.append(x); return lst
bad(v1); r_bad = bad(v2)
good(v1); r_good = good(v2)
print(f"bad={r_bad} good={r_good}")
