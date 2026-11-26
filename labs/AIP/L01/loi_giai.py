import math
import sys


def main() -> None:
    kv = {}
    for line in sys.stdin.read().splitlines():
        for tok in line.strip().split():
            if "=" in tok:
                k, v = tok.split("=", 1)
                kv[k] = v

    min_f1 = float(kv["min_f1"])
    max_lat = float(kv["max_lat"])
    cands = []
    for part in kv["runs"].split(","):
        if part.count(":") == 2:
            rid, f1_s, lat_s = part.split(":")
            f1, lat = float(f1_s), float(lat_s)
            if f1 >= min_f1 and lat <= max_lat:
                cands.append((rid, f1, lat))
    best_id = min(cands, key=lambda x: (-x[1], x[2], x[0]))[0] if cands else "NONE"

    na, ca = int(kv["na"]), int(kv["ca"])
    nb, cb = int(kv["nb"]), int(kv["cb"])
    pa, pb = ca / na, cb / nb
    pp = (ca + cb) / (na + nb)
    den = math.sqrt(pp * (1.0 - pp) * (1.0 / na + 1.0 / nb)) if 0.0 < pp < 1.0 else 0.0
    z = (pb - pa) / den if den > 0 else 0.0
    deploy = int(best_id != "NONE" and z >= float(kv["z_thresh"]))

    print(f"promoted_run={best_id}")
    print(f"ab_z={z:.3f}")
    print(f"deploy_prod={deploy}")


if __name__ == "__main__":
    main()
