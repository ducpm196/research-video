fan = (128 * 1024 * 1024) // 1024; tot_tab = fan * fan
print(f'entries_per_table={fan}')
print(f'max_tablets_pow2={tot_tab.bit_length() - 1}')
print(f'entries_sq_exact={tot_tab}')
