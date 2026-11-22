irq = (1000 // 4) * 1000
dma = 500 + 1000
print(f'irq_cycles_per_s={irq}')
print(f'dma_cycles_per_s={dma}')
print(f'dma_saved_pct={100 * (irq - dma) / irq:.1f}%')
