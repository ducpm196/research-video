from fractions import Fraction

that = [1] * 5 + [0] * 15
doan = [1, 1, 1, 1, 0] + [1, 1, 1] + [0] * 12


def dem(t, d):
    tp = sum(1 for a, b in zip(t, d) if a == 1 and b == 1)
    fp = sum(1 for a, b in zip(t, d) if a == 0 and b == 1)
    fn = sum(1 for a, b in zip(t, d) if a == 1 and b == 0)
    tn = sum(1 for a, b in zip(t, d) if a == 0 and b == 0)
    return tp, fp, fn, tn


tp, fp, fn, tn = dem(that, doan)
print(f"TP={tp} FP={fp} FN={fn} TN={tn}")
n = tp + fp + fn + tn
p, r = Fraction(tp, tp + fp), Fraction(tp, tp + fn)
print("ti le dung:", Fraction(tp + tn, n))
print("do chuan xac:", p)
print("do phu:", r)
print("F1:", 2 * p * r / (p + r))
tp2, fp2, fn2, tn2 = dem(that, [0] * 20)
print(f"mo hinh luoi (luon bao 0): ti le dung {Fraction(tp2 + tn2, n)}, do phu {Fraction(tp2, tp2 + fn2)}")
print("trung binh cong cua hai chi so:", (p + r) / 2)
