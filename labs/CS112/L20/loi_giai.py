import itertools

a = [9, 4, 7, 2, 8, 11, 3, 10, 5, 12]
n = len(a)
L = [1] * n
so_sanh = 0
for i in range(n):
    for j in range(i):
        so_sanh += 1
        if a[j] < a[i]:
            L[i] = max(L[i], L[j] + 1)
print("L:", " ".join(map(str, L)))

i = L.index(max(L))
day = [a[i]]
while L[i] > 1:
    i = min(j for j in range(i) if a[j] < a[i] and L[j] == L[i] - 1)
    day.append(a[i])
day.reverse()
print(f"LIS: {max(L)} qua {' '.join(map(str, day))}; so sanh bang: {so_sanh}")

tot, thu = 0, 0
for r in range(1, n + 1):
    for S in itertools.combinations(range(n), r):
        thu += 1
        if all(a[S[t]] < a[S[t + 1]] for t in range(r - 1)):
            tot = max(tot, r)
print(f"Vet can LIS: {tot} ({thu} tap con)")

X, Y = "THUATTOAN", "TOANTHUAT"
c = [[0] * (len(Y) + 1) for _ in range(len(X) + 1)]
for i in range(1, len(X) + 1):
    for j in range(1, len(Y) + 1):
        if X[i - 1] == Y[j - 1]:
            c[i][j] = c[i - 1][j - 1] + 1
        else:
            c[i][j] = max(c[i - 1][j], c[i][j - 1])
i, j, xau = len(X), len(Y), []
while i > 0 and j > 0:
    if X[i - 1] == Y[j - 1]:
        xau.append(X[i - 1])
        i, j = i - 1, j - 1
    elif c[i - 1][j] >= c[i][j - 1]:
        i -= 1
    else:
        j -= 1
print(f"LCS: {c[len(X)][len(Y)]} qua {''.join(reversed(xau))}")
print("Bang = vet can:", "CO" if max(L) == tot else "KHONG")
