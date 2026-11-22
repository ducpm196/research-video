k, n = 5, 100
no_p = k * n
id_p = k + n - 1
print(f'cycles_no_pipe={no_p}')
print(f'cycles_pipe_ideal={id_p} speedup={no_p / id_p:.2f}')
print(f'cycles_with_12_stalls={id_p + 12}')
