import itertools

N = 7
CANH = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 0), (1, 5), (2, 6)]


def doc_lap(S):
    return all(not (a in S and b in S) for a, b in CANH)


def phu(S):
    return all(a in S or b in S for a, b in CANH)


tot = {}
for k in range(N, -1, -1):
    for S in itertools.combinations(range(N), k):
        if doc_lap(set(S)) and "mis" not in tot:
            tot["mis"] = (k, set(S))
        if phu(set(S)):
            tot["mvc"] = k
a, S = tot["mis"]
b = tot["mvc"]
print(f"Tap doc lap lon nhat: {a}, phu dinh nho nhat: {b}, tong = {a + b}")
duyet = 0
hop_le = True
for u, v in CANH:
    duyet += 1
    if u in S and v in S:
        hop_le = False
print(f"Kiem chung chi: duyet {duyet} canh, hop le: {'CO' if hop_le else 'KHONG'}")

MON = [(3, 8), (5, 10), (4, 7), (6, 13), (2, 3), (7, 12)]


def tui(W):
    dp = [0] * (W + 1)
    for w, g in MON:
        for c in range(W, w - 1, -1):
            dp[c] = max(dp[c], dp[c - w] + g)
    return dp[W]


for W in (14, 14000):
    print(f"Cai tui 0/1 W = {W}: toi uu {tui(W)}, so o bang {len(MON) * (W + 1)}, so bit cua W: {W.bit_length()}")
