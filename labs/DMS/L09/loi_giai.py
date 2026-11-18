from itertools import product, permutations

def in_ra(mo_ta, cong_thuc, vet_can):
    print(mo_ta + ':', cong_thuc, vet_can)

in_ra('ma PIN 4 chu so (duoc lap)', 10 ** 4, len(list(product(range(10), repeat=4))))
in_ra('ma PIN 4 chu so khac nhau', 10 * 9 * 8 * 7, len(list(permutations(range(10), 4))))
in_ra('xep 5 nguoi thanh hang', 5 * 4 * 3 * 2 * 1, len(list(permutations('ABCDE'))))
in_ra('chuoi 3 ky tu tu abcd, duoc lap', 4 ** 3, len(list(product('abcd', repeat=3))))
in_ra('chuoi 3 ky tu tu abcd, khong lap', 4 * 3 * 2, len(list(permutations('abcd', 3))))
chan = 0
for p in permutations('12345', 3):
    if int(p[2]) % 2 == 0:
        chan = chan + 1
in_ra('so chan 3 chu so khac nhau tu 1..5', 2 * 4 * 3, chan)
