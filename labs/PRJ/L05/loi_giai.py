import struct
import sys
from collections import deque


def parse_kv(text: str) -> dict[str, str]:
    kv: dict[str, str] = {}
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("bursts="):
            kv["bursts"] = line.split("=", 1)[1].strip()
        else:
            for tok in line.split():
                k, v = tok.split("=", 1)
                kv[k] = v
    return kv


def main() -> None:
    kv = parse_kv(sys.stdin.read())
    pid = int(kv["pid"])
    plen = int(kv["plen"])
    fill = kv["fill"].encode("ascii")[:1]
    q = int(kv["q"])
    bursts = [int(x) for x in kv["bursts"].split()]

    buf = struct.pack("<HH", pid, plen) + fill * plen
    dec_id, dec_len = struct.unpack("<HH", buf[:4])

    rem = list(bursts)
    t = 0
    fin = [0] * len(bursts)
    dq = deque(range(len(bursts)))
    while dq:
        i = dq.popleft()
        d = min(q, rem[i])
        t += d
        rem[i] -= d
        if rem[i] > 0:
            dq.append(i)
        else:
            fin[i] = t
    waits = [fin[i] - bursts[i] for i in range(len(bursts))]

    print(f"frame_total_bytes={4 + dec_len}")
    print(f"rr_avg_wait={sum(waits) / len(waits):.2f}")
    print(f"header_valid={int(dec_id == pid and len(buf) == 4 + dec_len)}")


if __name__ == "__main__":
    main()
