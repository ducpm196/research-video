"""Nhánh cận TSP bằng ma trận rút gọn (kiểu “chi phí nhỏ nhất trước”) cho ma trận 5×5 của bài L15 — in mọi cận dưới.
Dùng để kiểm các số trên màn hình (L15 có checks gọi lại cùng logic). Chạy: .venv/Scripts/python audit/cs112/tsp_bb.py"""
import heapq
import itertools
import math
import sys

INF = math.inf
C = [[INF, 20, 30, 10, 11], [15, INF, 16, 4, 2], [3, 5, INF, 2, 4], [19, 6, 18, INF, 3], [16, 4, 7, 16, INF]]


def reduce(M):
    M = [r[:] for r in M]
    n, total = len(M), 0
    for i in range(n):
        m = min(M[i])
        if 0 < m < INF:
            M[i] = [v - m for v in M[i]]; total += m
    for j in range(n):
        m = min(M[i][j] for i in range(n))
        if 0 < m < INF:
            for i in range(n):
                M[i][j] -= m
            total += m
    return M, total


def child(M, lb, i, j, start=0):
    N = [r[:] for r in M]
    cost = N[i][j]
    for k in range(len(N)):
        N[i][k] = INF; N[k][j] = INF
    N[j][start] = INF
    R, r = reduce(N)
    return R, lb + cost + r


def solve(trace=None):
    R0, lb0 = reduce(C)
    heap = [(lb0, [0], R0)]
    best, best_tour = INF, None
    while heap:
        lb, path, M = heapq.heappop(heap)
        if lb >= best:
            continue
        if len(path) == len(C):
            if lb < best:
                best, best_tour = lb, path
            continue
        for j in range(len(C)):
            if j not in path:
                M2, lb2 = child(M, lb, path[-1], j)
                if trace is not None:
                    trace.append((tuple(p + 1 for p in path + [j]), lb2))
                if lb2 < best:
                    heapq.heappush(heap, (lb2, path + [j], M2))
    return best, best_tour


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    R0, lb0 = reduce(C)
    print("LB gốc", lb0)
    for row in R0:
        print(row)
    tr = []
    best, tour = solve(tr)
    for t, v in tr:
        print("->".join(map(str, t)), v)
    print("tốt nhất", best, [v + 1 for v in tour])
    bf = min(sum(C[a][b] for a, b in zip((0,) + p, p + (0,))) for p in itertools.permutations(range(1, 5)))
    print("vét cạn", bf, "số chu trình", math.factorial(4))
