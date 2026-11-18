import math

p = 420 / 500
se = math.sqrt(p * (1 - p)) / math.sqrt(500)
print(f"khoang tin cay 95% cho ti le dung 420/500: [{round(p - 1.96 * se, 4)}, {round(p + 1.96 * se, 4)}]")
n = 200
b_hon, a_hon = 20, 10
print(f"cot ghep cap: B hon A tren {b_hon} mau, A hon B tren {a_hon} mau")
tb = (b_hon - a_hon) / n
bp = (b_hon + a_hon) / n
sd = math.sqrt(bp - tb**2)
se_h = sd / math.sqrt(n)
lo, hi = tb - 1.96 * se_h, tb + 1.96 * se_h
print("trung binh hieu:", round(tb, 4))
print("sai so chuan cua hieu:", round(se_h, 4))
print(f"khoang tin cay 95% cua hieu: [{round(lo, 4)}, {round(hi, 4)}]")
print("chua du bang chung:", lo <= 0 <= hi)
pp = 0.9
print("mau can cho nua do rong 0.01 (p=0.9):", math.ceil(1.96**2 * pp * (1 - pp) / 0.01**2))
