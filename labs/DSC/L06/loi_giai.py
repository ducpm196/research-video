import math
def corr(pts):
    mx = sum(x for x, _ in pts)/len(pts); my = sum(y for _, y in pts)/len(pts)
    num = sum((x-mx)*(y-my) for x, y in pts)
    dx = sum((x-mx)**2 for x, _ in pts)
    dy = sum((y-my)**2 for _, y in pts)
    return num / math.sqrt(dx * dy)
base = [(1,2),(2,3),(3,5),(4,7)]
print(f"r_clean={corr(base):.3f} r_outlier={corr(base+[(25,-12)]):.3f}")
