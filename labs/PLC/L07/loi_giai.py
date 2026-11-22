def make_adder(start, step):
    val = [start]
    def inc():
        val[0] += step
        return val[0]
    return inc
a1, a2 = make_adder(20, 4), make_adder(20, 7)
print(f"a1={[a1(), a1()]} a2={a2()}")
