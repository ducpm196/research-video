import hashlib
import sys


def tail_hash(events: list[str]) -> str:
    h = "0" * 64
    for ev in events:
        h = hashlib.sha256(f"{h}|{ev}".encode("utf-8")).hexdigest()
    return h


def main() -> None:
    kv = dict(line.strip().split("=", 1) for line in sys.stdin.read().splitlines() if "=" in line)
    keys = [x for x in kv["miss_keys"].split(",") if x]
    events = [x for x in kv["events"].split(",") if x]
    tidx = int(kv["tamper_idx"])

    sf_reads = len(set(keys))
    orig_h = tail_hash(events)
    mod = list(events)
    mod[tidx] = mod[tidx] + "*"
    mod_h = tail_hash(mod)

    print(f"db_reads_sf={sf_reads}")
    print(f"tail_hash12={orig_h[:12]}")
    print(f"tamper_detected={int(orig_h != mod_h)}")


if __name__ == "__main__":
    main()
