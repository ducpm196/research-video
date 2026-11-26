import re
import sys

PII_RX = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+|\b0\d{9}\b")


def main() -> None:
    lines = sys.stdin.read().splitlines()
    kv: dict[str, str] = {}
    for ln in lines:
        ln = ln.strip()
        if not ln:
            continue
        if "log_line=" in ln:
            before, log_val = ln.split("log_line=", 1)
            kv["log_line"] = log_val
            for tok in before.split():
                k, v = tok.split("=", 1)
                kv[k] = v
        else:
            for tok in ln.split():
                if "=" in tok:
                    k, v = tok.split("=", 1)
                    kv[k] = v

    status = int(kv["status"])
    lat = int(kv["lat_ms"])
    max_lat = int(kv["max_lat"])
    sel = kv["selector"]
    qa_pass = int(status == 200 and lat <= max_lat and "data-testid" in sel)

    matches = PII_RX.findall(kv["log_line"])
    cleaned = PII_RX.sub("[REDACTED]", kv["log_line"])
    assert not PII_RX.search(cleaned)

    di = float(kv["rate_unpriv"]) / float(kv["rate_priv"])
    gov_ok = int(di >= 0.80)
    ship = int(qa_pass == 1 and gov_ok == 1)

    print(f"qa_pass={qa_pass} pii_redacted={len(matches)}")
    print(f"disparate_impact={di:.3f} gov_ok={gov_ok}")
    print(f"ship_ready={ship}")


if __name__ == "__main__":
    main()
