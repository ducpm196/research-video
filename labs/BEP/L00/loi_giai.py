import math
import sys


def main() -> None:
    kv = dict(line.strip().split("=", 1) for line in sys.stdin.read().splitlines() if "=" in line)
    items = [p.split(":") for p in kv["items"].split(",") if ":" in p]
    limit = int(kv["batch_limit"])
    unique_users = {u for _, u in items}
    n_batches = math.ceil(len(unique_users) / limit) if unique_users else 0
    print(f"naive_queries={1 + len(items)}")
    print(f"unique_keys={len(unique_users)}")
    print(f"dataloader_queries={1 + n_batches}")


if __name__ == "__main__":
    main()
