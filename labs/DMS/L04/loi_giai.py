def tong(n):
    t = 0
    for k in range(1, n + 1):
        t = t + k * k
    return t

def ct(n):
    return n * (n + 1) * (2 * n + 1) // 6

def sai(n):
    return n * (n + 1) * (n + 2) // 6

print('co so:', tong(1), ct(1))
for n in range(1, 5):
    print('quy nap ' + str(n) + '->' + str(n + 1) + ': ' + str(tong(n)) + ' + ' + str((n + 1) ** 2)
          + ' = ' + str(tong(n) + (n + 1) ** 2) + ', cong thuc ' + str(ct(n + 1)))
dung = True
for n in range(1, 1001):
    if tong(n) != ct(n):
        dung = False
print('kiem 1..1000:', 'dung' if dung else 'sai')
n = 1
while tong(n) == sai(n):
    n = n + 1
print('cong thuc sai: co so dung, sai dau tien o n=' + str(n))
