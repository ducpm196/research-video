def iou(a, b):
    iw = max(0, min(a[2], b[2]) - max(a[0], b[0]))
    ih = max(0, min(a[3], b[3]) - max(a[1], b[1]))
    inter = iw * ih
    ua = (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - inter
    return inter / ua
print(f"iou_diff={iou((0, 0, 12, 12), (6, 6, 18, 18)):.3f}",
      f"iou_nms={iou((0, 0, 12, 12), (2, 0, 14, 12)):.3f}")
