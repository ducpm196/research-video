from itertools import permutations

S = [1, 2, 3, 4, 6, 8, 12, 24]

def duoi(x):
    return [a for a in S if a != x and x % a == 0]

canh = []
for a in S:
    for b in S:
        if a != b and b % a == 0 and not any(c != a and c != b and c % a == 0 and b % c == 0 for c in S):
            canh.append((a, b))

print('so canh Hasse:', len(canh))
print('canh:', ' '.join(str(a) + '-' + str(b) for a, b in canh))
print('phan tu toi tieu:', ' '.join(str(x) for x in S if not duoi(x)))
print('phan tu toi dai:', ' '.join(str(x) for x in S if not any(y != x and y % x == 0 for y in S)))
khong_sanh = 0
for a in S:
    for b in S:
        if a < b and b % a != 0:
            khong_sanh = khong_sanh + 1
print('cap khong so sanh duoc:', khong_sanh)

hang = []
while len(hang) < len(S):
    san_sang = [x for x in S if x not in hang and all(a in hang for a in duoi(x))]
    hang.append(max(san_sang))
print('sap xep to po (chon so lon nhat):', ' '.join(str(x) for x in hang))

dem = 0
for h in permutations(S):
    if all(h.index(a) < h.index(b) for a in S for b in S if a != b and b % a == 0):
        dem = dem + 1
print('so cach sap xep to po:', dem)
