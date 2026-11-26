import sys
s = sys.stdin.read().strip() or "45 15 10 100 200"
tp, fp, fn, side, obj_px = map(int, s.split())
iou = tp / (tp + fp + fn)
dice = 2 * tp / (2 * tp + fp + fn)
tot = side * side
acc_bg = (tot - obj_px) / tot
print(f"iou={iou:.3f} dice={dice:.3f} dice_ge_iou={int(dice >= iou)} acc_all_bg={acc_bg:.2f} iou_all_bg=0.0")
