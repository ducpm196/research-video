import sys
import torch


def main() -> None:
    kv = dict(tok.split("=", 1) for tok in sys.stdin.read().split() if "=" in tok)
    x0 = torch.tensor(float(kv["x0"]), requires_grad=True)
    (x0 ** 2).backward()
    (x0 ** 2).backward()
    acc = x0.grad.item()
    x0.grad.zero_()
    (x0 ** 2).backward()
    rst = x0.grad.item()

    torch.manual_seed(int(kv["seed"]))
    x = torch.linspace(-1, 1, 20).unsqueeze(1)
    y = float(kv["w_true"]) * x + float(kv["b_true"])
    m = torch.nn.Linear(1, 1)
    opt = torch.optim.SGD(m.parameters(), lr=float(kv["lr"]))
    for _ in range(int(kv["steps"])):
        opt.zero_grad()
        loss = ((m(x) - y) ** 2).mean()
        loss.backward()
        opt.step()
    print(f"grad_accum={acc:.1f}")
    print(f"grad_reset={rst:.1f}")
    print(f"fitted_wb={m.weight.item():.2f}_{m.bias.item():.2f}")


if __name__ == "__main__":
    main()
