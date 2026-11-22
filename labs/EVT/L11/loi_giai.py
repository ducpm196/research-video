mps = round(864_000_000 / 86400)
batch_sz = 40
batches = 400_000 // batch_sz
print(f'msgs_per_sec={mps}')
print(f'batches={batches}')
print(f'rpc_cut={400_000 // batches}x')
