import numpy as np

so_lieu = np.array([[120, 4000], [150, 5200], [90, 3100], [200, 6100], [140, 4600]], dtype=float)
tb = so_lieu.mean(axis=0)
do_lech = so_lieu.std(axis=0)
chuan = (so_lieu - tb) / do_lech
print("Trung binh:", np.round(tb, 2))
print("Do lech chuan:", np.round(do_lech, 2))
print(np.round(chuan, 3))
print("Trung binh cot sau chuan hoa ~ 0:", np.allclose(chuan.mean(axis=0), 0))
print("Do lech chuan cot sau chuan hoa:", np.round(chuan.std(axis=0), 6))
