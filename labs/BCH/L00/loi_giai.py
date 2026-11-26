import sys
s = sys.stdin.read().strip() or "5|1,1,1,0|1,1,0,0"
ns, a_s, b_s = s.split("|")
n = int(ns)
need = lambda v: int(v[0] and v[1] and (not v[2]) and (not v[3]))
a = [int(x) for x in a_s.split(",")]
b = [int(x) for x in b_s.split(",")]
print(f"central_ops=1 maj_quorum_5={(n // 2) + 1} school_need={need(a)} rivals_need={need(b)}")
