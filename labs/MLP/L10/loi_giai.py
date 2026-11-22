import torch
x0 = torch.tensor(3.0, requires_grad=True)
(x0 ** 2).backward(); (x0 ** 2).backward()
acc = x0.grad.item()
x0.grad.zero_(); (x0 ** 2).backward()
rst = x0.grad.item()
torch.manual_seed(42)
x = torch.linspace(-1, 1, 20).unsqueeze(1); y = 3.0 * x + 2.0
m = torch.nn.Linear(1, 1); opt = torch.optim.SGD(m.parameters(), lr=0.2)
for _ in range(120):
    opt.zero_grad(); loss = ((m(x) - y) ** 2).mean(); loss.backward(); opt.step()
print(f'grad_accum={acc:.1f}')
print(f'grad_reset={rst:.1f}')
print(f'fitted_wb={m.weight.item():.2f}_{m.bias.item():.2f}')
