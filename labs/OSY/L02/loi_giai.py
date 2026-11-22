def waits(order):
    t = 0; w = []
    for b in order: w.append(t); t += b
    return w, sum(w) / len(w)
b = [24, 3, 3]
fw, fa = waits(b)
sw = [0] * 3; t = 0
for i in sorted(range(3), key=lambda k: b[k]): sw[i] = t; t += b[i]
sa = sum(sw) / 3
print(f'fcfs_waits={fw[0]},{fw[1]},{fw[2]} avg={fa:.2f}')
print(f'sjf_waits={sw[0]},{sw[1]},{sw[2]} avg={sa:.2f}')
print(f'wait_saved={fa - sa:.2f}')
