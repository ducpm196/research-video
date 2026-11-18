import math

N = 10000
benh = N * 2 // 100
bao_dung = benh * 95 // 100
khoe = N - benh
bao_nham = khoe * 5 // 100
print(f"dem 10000 nguoi: benh {benh}, bao dung {bao_dung}, bao nham {bao_nham}")
print("xac suat that khi duong tinh (dem):", round(bao_dung / (bao_dung + bao_nham), 4))


def bayes(tien_nghiem, nhay=0.95, nham=0.05):
    tu = nhay * tien_nghiem
    return tu / (tu + nham * (1 - tien_nghiem))


print("xac suat that khi duong tinh (Bayes):", round(bayes(0.02), 4))
print("tien nghiem 0.2%:", round(bayes(0.002), 4))
xs = {0: 0.2, 1: 0.5, 2: 0.3}
ek = sum(x * p for x, p in xs.items())
ek2 = sum(x * x * p for x, p in xs.items())
print("ky vong:", round(ek, 4))
print("phuong sai:", round(ek2 - ek**2, 4))
print("do lech chuan:", round(math.sqrt(ek2 - ek**2), 4))
