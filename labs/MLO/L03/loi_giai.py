pred = lambda s: 1 if 'tot' in s else 0
inv_ok = all(pred(f"{n} is tot") == 1 for n in ('Binh', 'Chi', 'Dung'))
slice_acc = {'maj': 0.94, 'min': 0.71}
ok_min = int(min(slice_acc.values()) >= 0.80)
print(f"inv_pass={int(inv_ok)} min_slice_pass={ok_min}")
