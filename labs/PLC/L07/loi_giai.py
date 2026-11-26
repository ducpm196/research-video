import sys
s = sys.stdin.read().strip() or "20 4 7"
st, k1, k2 = map(int, s.split())
def make_adder(start, step):
    val = start
    def inc():
        nonlocal val
        val += step
        return val
    return inc
a1, a2 = make_adder(st, k1), make_adder(st, k2)
print(f"a1={[a1(), a1()]} a2={a2()}")
