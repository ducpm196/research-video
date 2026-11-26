import sys
import torch
import torch.nn as nn


def main() -> None:
    kv = dict(tok.split("=", 1) for tok in sys.stdin.read().split() if "=" in tok)
    seed = int(kv["seed"])
    hid = int(kv["hidden"])
    torch.manual_seed(seed)
    X = torch.tensor([[0.0, 0.0], [0.0, 1.0], [1.0, 0.0], [1.0, 1.0]] * 25)
    y = torch.tensor([0, 1, 1, 0] * 25)
    net = nn.Sequential(nn.Linear(2, hid), nn.ReLU(), nn.Linear(hid, 2))
    opt = torch.optim.Adam(net.parameters(), lr=float(kv["lr_mlp"]))
    crit = nn.CrossEntropyLoss()
    for _ in range(int(kv["steps_mlp"])):
        opt.zero_grad()
        loss = crit(net(X), y)
        loss.backward()
        opt.step()
    net.eval()
    with torch.no_grad():
        acc_mlp = (net(X[:4]).argmax(1) == y[:4]).float().mean().item()

    torch.manual_seed(seed)
    lin = nn.Sequential(nn.Linear(2, hid), nn.Linear(hid, 2))
    opt2 = torch.optim.SGD(lin.parameters(), lr=float(kv["lr_lin"]))
    for _ in range(int(kv["steps_lin"])):
        opt2.zero_grad()
        l2 = crit(lin(X[:4]), y[:4])
        l2.backward()
        opt2.step()
    with torch.no_grad():
        acc_lin = (lin(X[:4]).argmax(1) == y[:4]).float().mean().item()
    print(f"n_params={sum(p.numel() for p in net.parameters())}")
    print(f"mlp_xor_acc={acc_mlp:.2f}")
    print(f"no_relu_xor_acc={acc_lin:.2f}")


if __name__ == "__main__":
    main()
