majority = False
cp_ok = 1 if majority else 0
ap_a, ap_b = 'v_new', 'v_old'
print(f'cp_rejected_minority={int(cp_ok == 0)}')
print(f'ap_available_minority={int(ap_a == "v_new")}')
print(f'ap_diverged={int(ap_a != ap_b)}')
