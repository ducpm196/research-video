from itertools import combinations

HAM = [
    ('f1', {1: 'a', 2: 'b', 3: 'a', 4: 'c'}, {'a', 'b', 'c'}),
    ('f2', {1: 'a', 2: 'c', 3: 'd'}, {'a', 'b', 'c', 'd'}),
    ('f3', {1: 'x', 2: 'z', 3: 'y'}, {'x', 'y', 'z'}),
    ('f4', {1: 'p', 2: 'q', 3: 'p', 4: 'p', 5: 'q'}, {'p', 'q'}),
    ('f5', {1: 'a', 2: 'a', 3: 'b'}, {'a', 'b', 'c'}),
]

for ten, f, B in HAM:
    don = len(set(f.values())) == len(f)
    toan = set(f.values()) == B
    if don and toan:
        print(ten + ': song anh')
    else:
        print(ten + ': ' + ('don anh' if don else 'khong don anh') + ', ' + ('toan anh' if toan else 'khong toan anh'))

for k in (7, 6):
    tong = 0
    co_cap = 0
    for chon in combinations(range(1, 13), k):
        tong = tong + 1
        if any(a + b == 13 for a in chon for b in chon):
            co_cap = co_cap + 1
    print('chon', k, 'so tu 1 den 12:', tong, 'cach,', co_cap, 'cach co cap tong 13')
