from math import comb
from itertools import product, combinations_with_replacement

def in_ra(mo_ta, cong_thuc, vet_can):
    print(mo_ta + ':', cong_thuc, vet_can)

in_ra('x1+x2+x3+x4 = 7', comb(7 + 3, 3), sum(1 for x in product(range(8), repeat=4) if sum(x) == 7))
in_ra('x1+x2+x3 = 12, moi xi >= 2', comb(6 + 2, 2), sum(1 for x in product(range(13), repeat=3) if sum(x) == 12 and min(x) >= 2))
in_ra('chon 4 vien kem tu 6 vi', comb(4 + 5, 5), len(list(combinations_with_replacement(range(6), 4))))
in_ra('x1+x2+x3 = 10, moi xi <= 5', comb(12, 2) - 3 * comb(4 + 2, 2), sum(1 for x in product(range(11), repeat=3) if sum(x) == 10 and max(x) <= 5))
