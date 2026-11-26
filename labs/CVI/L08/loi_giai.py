import sys
s = sys.stdin.read().strip() or "0,0,12,12 6,6,18,18 2,0,14,12"
b0, b1, b2 = [tuple(map(float, x.split(","))) for x in s.split()]
def iou(a, b):
    iw = max(0.0, min(a[2], b[2]) - max(a[0], b[0]))
    ih = max(0.0, min(a[3], b[3]) - max(a[1], b[1]))
    inter = iw * ih
    ua = (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - inter
    return inter / ua
print(f"iou_diff={iou(b0, b1):.3f} iou_nms={iou(b0, b2):.3f}")
