import sys


def main() -> None:
    kv = dict(line.strip().split("=", 1) for line in sys.stdin.read().splitlines() if "=" in line)
    bal = int(kv["balance"])
    ops = [int(x) for x in kv["ops"].split(",") if x]
    rejected = 0
    red_caught = 0
    for amt in ops:
        if amt > 0 and bal >= amt:
            bal -= amt
        else:
            rejected += 1
            red_caught += 1
    print(f"final_balance={bal}")
    print(f"rejected_count={rejected}")
    print(f"red_caught={red_caught}")


if __name__ == "__main__":
    main()
