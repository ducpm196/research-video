v1 = {'order_id': 10, 'amount': 200}
v2 = {'order_id': 11, 'amount': 350, 'tier': 'vip'}
old_read = v2['order_id']
new_tier = v1.get('tier', 'std')
print(f'old_reads_v2={old_read}')
print(f'new_reads_v1={new_tier}')
