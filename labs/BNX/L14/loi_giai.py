from fractions import Fraction as F


def nhan(rate, cap, times):
    tok, last, ok = F(cap), F(0), 0
    for t in times:
        tok = min(F(cap), tok + (t - last) * rate)
        last = t
        if tok >= 1:
            tok, ok = tok - 1, ok + 1
    return ok


dong = [F(0)] * 20
rai = [F(i, 10) for i in range(20)]
a = nhan(4, 6, dong)
print("dong 20 yeu cau: nhan", a, "tu choi", 20 - a)
b = nhan(4, 6, rai)
print("rai deu: nhan", b, "can tren", int(6 + 4 * F(19, 10)))
n = 50
print(n, "ben dong:", n * a, "qua cong,", n * (20 - a), "tu choi")
print("hang cho", n * a / 120, "giay neu hau phuong chiu 120 yeu cau/giay")
