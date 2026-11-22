steps = ['reserve_stock', 'charge_card', 'ship_order']
done, failed = [], None
for s in steps:
    if s == 'ship_order': failed = s; break
    done.append(s)
comp = [f'undo_{s}' for s in reversed(done)]
print(f'failed_at={failed}')
print(f'compensations={comp}')
