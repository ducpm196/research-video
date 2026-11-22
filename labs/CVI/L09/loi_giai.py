tp, fp, fn = 45, 15, 10
iou = tp / (tp + fp + fn)
dice = 2 * tp / (2 * tp + fp + fn)
total_px, obj_px = 100 * 100, 200
acc_bg = (total_px - obj_px) / total_px
iou_bg = 0 / obj_px
print(f"iou={iou:.3f} dice={dice:.3f} dice_ge_iou={int(dice >= iou)}",
      f"acc_all_bg={acc_bg:.2f} iou_all_bg={iou_bg:.1f}")
