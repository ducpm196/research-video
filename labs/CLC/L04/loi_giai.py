import sys
n = int(sys.stdin.read().split('=')[1])
l11, l4 = n * 1e-11, n * 1e-4
print(f'loss_11nines={l11:.5f}\nloss_4nines={l4:.1f}\nyears_per_loss={round(1.0 / l11)}')
