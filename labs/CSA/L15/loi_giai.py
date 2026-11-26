import sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
irq = (kv['kbps'] // kv['block_kb']) * kv['irq_cyc']
dma = kv['dma_setup'] + kv['irq_cyc']
print(f'irq_cycles_per_s={irq}')
print(f'dma_cycles_per_s={dma}')
print(f'dma_saved_pct={100 * (irq - dma) / irq:.1f}%')
