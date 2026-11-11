"""Kiểm độc lập BNX L01 (OpenAPI). Đường khác so với tools/checklib_bnx/l01.py:
- nạp ĐÚNG hằng SPEC_YAML đang hiện trên màn hình bằng pyyaml, phân giải $ref, lấy lược đồ ra từ YAML (không dùng lược đồ chép tay của checklib);
- bộ kiểm viết tay: đếm từng ký tự chữ số bằng vòng lặp (không dùng biểu thức chính quy), so số nguyên bằng type();
- chạy thật chương trình VALIDATE_PY trên màn hình bằng tiến trình Python riêng và đọc đầu ra;
- phân loại thay đổi bằng mô phỏng: sinh yêu cầu/phản hồi cũ rồi thử với lược đồ mới."""
import json
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "audit" / "bnx"))
sys.path.insert(0, str(ROOT / "audit" / "bnx" / "src"))
sys.path.insert(0, str(ROOT / "tools"))
import checklib as alg  # noqa: E402
import l01 as src  # noqa: E402


def _resolve(doc, node):
    if isinstance(node, dict) and "$ref" in node:
        cur = doc
        for part in node["$ref"].lstrip("#/").split("/"):
            cur = cur[part]
        return cur
    return node


def _digits_len(s):
    """Độ dài nếu s toàn chữ số 0–9 (đếm tay), None nếu có ký tự khác."""
    n = 0
    for ch in s:
        if ch not in "0123456789":
            return None
        n += 1
    return n


def _hand_check(req, schema):
    """Bộ kiểm viết tay chỉ hiểu đúng các từ khoá lược đồ của bài: required, type string/integer, pattern ^[0-9]{a,b}$, minimum."""
    bad = []
    for f in schema["required"]:
        if f not in req:
            bad.append((f, "thiếu"))
    for f, p in schema["properties"].items():
        if f not in req:
            continue
        v = req[f]
        if p["type"] == "string":
            pat = p["pattern"]
            assert pat.startswith("^[0-9]{") and pat.endswith("}$"), pat
            lo, hi = (int(x) for x in pat[len("^[0-9]{"):-2].split(","))
            n = _digits_len(v) if type(v) is str else None
            if n is None or not (lo <= n <= hi):
                bad.append((f, "sai dạng"))
        elif p["type"] == "integer":
            if type(v) is not int or v < p["minimum"]:
                bad.append((f, "sai giá trị"))
    return bad


def run(rec):
    doc = yaml.safe_load(src.SPEC_YAML)
    lines = src.SPEC_YAML.strip("\n").split("\n")
    # 1. năm đoạn trên màn hình là các dòng liên tiếp của đặc tả, phủ đủ 42 dòng, mỗi đoạn ≤ 12 dòng và tự là YAML hợp lệ
    parts = sorted(src.SPEC_PARTS.values())
    cover = [i for a, b in parts for i in range(a, b + 1)]
    ok_parts = cover == list(range(1, len(lines) + 1)) and all(b - a + 1 <= 12 for a, b in parts) and all(
        isinstance(yaml.safe_load("\n".join(lines[a - 1:b])), dict) for a, b in parts)
    rec("L01", ok_parts, f"5 đoạn YAML trên màn hình phủ đúng {len(lines)} dòng của SPEC_YAML, mỗi đoạn ≤ 12 dòng, tự phân tích được")
    # 2. cấu trúc OpenAPI 3.0.3
    op = doc["paths"]["/transfers"]["post"]
    hdr = op["parameters"][0]
    body = op["requestBody"]
    schema = _resolve(doc, body["content"]["application/json"]["schema"])
    ok_struct = (doc["openapi"] == "3.0.3" and {"title", "version"} <= set(doc["info"])
                 and hdr == {"in": "header", "name": "Idempotency-Key", "required": True, "schema": {"type": "string"}}
                 and body["required"] is True and set(op["responses"]) == {"201", "400", "409", "422"}
                 and all(r.get("description") for r in op["responses"].values())
                 and schema["required"] == ["fromAccount", "toAccount", "amount"])
    rec("L01", ok_struct, "đặc tả: openapi 3.0.3, POST /transfers, phần đầu Idempotency-Key bắt buộc, thân bắt buộc, $ref phân giải được, phản hồi 201/400/409/422 có description")
    # 3. lược đồ lấy từ YAML trùng lược đồ checklib dùng
    probe = [{"fromAccount": "0123456789", "toAccount": "9876543210", "amount": 1}, {"fromAccount": "123", "amount": 0},
             {"toAccount": "1" * 19, "amount": "5"}, {"fromAccount": "1" * 20, "toAccount": 123456789012, "amount": True}]
    rec("L01", schema["properties"]["amount"] == {"type": "integer", "minimum": 1}
        and schema["properties"]["fromAccount"] == schema["properties"]["toAccount"] == {"type": "string", "pattern": "^[0-9]{10,19}$"}
        and all(alg.bnx_oas_errors(r, schema) == alg.bnx_oas_errors(r) for r in probe),
        "lược đồ lấy từ YAML: hai tài khoản chuỗi ^[0-9]{10,19}$, amount integer minimum 1; checklib cho cùng lỗi khi dùng lược đồ YAML hay lược đồ chép sẵn")
    # 4. ba yêu cầu thử: bộ kiểm viết tay trên lược đồ YAML ↔ checklib
    reqs = [{"fromAccount": "0123456789", "toAccount": "9876543210", "amount": 500000},
            {"fromAccount": "0123456789", "toAccount": "9876543210", "amount": 0},
            {"fromAccount": "0123456789", "amount": 500000}]
    hand = [_hand_check(r, schema) for r in reqs]
    lib = alg.bnx_oas_batch()
    ok3 = ([len(h) for h in hand] == [0, 1, 1] and hand[1][0][0] == "amount" and hand[2][0] == ("toAccount", "thiếu")
           and [s for s, _ in lib] == [201 if not h else 400 for h in hand]
           and [[e.split(":")[0] for e in errs] for _, errs in lib] == [[f for f, _ in h] for h in hand])
    rec("L01", ok3, f"ba yêu cầu thử theo lược đồ YAML (bộ kiểm tay): {hand}; checklib: {lib}")
    # 5. các con số khác của bài
    q1 = {"fromAccount": "0123456789", "toAccount": "12345678901234567890", "amount": 100000}
    hook = {"fromAccount": "0123456789", "to": "9876543210", "amount": "500000"}
    others = [
        (_hand_check(q1, schema) == [("toAccount", "sai dạng")] and alg.bnx_oas_errors(q1) == ["toAccount: sai dạng"], "quiz câu 1: 20 chữ số → toAccount sai, 400"),
        (sorted(f for f, _ in _hand_check(hook, schema)) == ["amount", "toAccount"] and alg.bnx_oas_status(hook) == 400, "hook: tên to và số tiền chuỗi → 400"),
        (_digits_len("0123456789") == 10 and _digits_len("12345") == 5 and _digits_len("0123-456789") is None
         and alg.bnx_oas_match("0123456789") and not alg.bnx_oas_match("12345") and not alg.bnx_oas_match("0123-456789"), "mẫu: 10 chữ số khớp, 5 chữ số và có gạch không khớp"),
        (_hand_check({"fromAccount": "0123456789", "toAccount": "9876543210", "amount": "500000"}, schema) == [("amount", "sai giá trị")], "bước 4: số tiền dạng chuỗi bị từ chối"),
    ]
    for ok, what in others:
        rec("L01", ok, what)
    # 6. JSON và YAML ở cảnh ôn nền là cùng dữ liệu, 3 cặp, hợp lệ theo lược đồ
    j, y = json.loads(src.BODY_JSON), yaml.safe_load(src.BODY_YAML)
    rec("L01", j == y and len(j) == 3 and _hand_check(j, schema) == [], f"thân JSON = thân YAML, 3 cặp, hợp lệ: {j}")
    # 7. chạy thật chương trình trên màn hình, đầu ra khớp hằng VALIDATE_OUT và khớp bộ kiểm tay
    p = subprocess.run([sys.executable, "-I", "-X", "utf8", "-B", "-c", src.VALIDATE_PY], capture_output=True, text=True, encoding="utf-8", timeout=60)
    outl = p.stdout.strip().splitlines()
    rec("L01", p.returncode == 0 and p.stdout.strip() == src.VALIDATE_OUT.strip()
        and [int(l.split()[1]) for l in outl] == [201 if not h else 400 for h in hand],
        f"chạy thật VALIDATE_PY: {outl}")
    # 7b. hai lỗi người đọc độc lập báo (2026-11-11): số tài khoản có xuống dòng cuối lọt qua `$` của Python; trường có tên mà null lọt qua.
    #     Chạy chính các hàm trên màn hình với hai ca này; so với bộ kiểm tay (vòng lặp) và checklib (mẫu kiểu ECMA).
    nl = {"fromAccount": "0123456789" + chr(10), "toAccount": "9876543210", "amount": 500000}
    nul = {"fromAccount": "0123456789", "toAccount": None, "amount": None}
    probe = src.VALIDATE_PY.split(chr(10) + "A, B = ")[0] + chr(10) + "print(kiem(%r))" % (nl,) + chr(10) + "print(kiem(%r))" % (nul,) + chr(10)
    p2 = subprocess.run([sys.executable, "-I", "-X", "utf8", "-B", "-c", probe], capture_output=True, text=True, encoding="utf-8", timeout=60)
    o2 = p2.stdout.strip().splitlines()
    rec("L01", p2.returncode == 0 and o2 == ["['fromAccount: sai dạng']", "['toAccount: thiếu', 'amount: thiếu']"]
        and _hand_check(nl, schema) == [("fromAccount", "sai dạng")] and len(_hand_check(nul, schema)) == 2
        and alg.bnx_oas_status(nl) == 400 and alg.bnx_oas_status(nul) == 400 and not alg.bnx_oas_match("0123456789" + chr(10)),
        f"bộ kiểm trên màn hình từ chối số tài khoản có xuống dòng cuối và trường null: {o2}")
    # 8. phân loại thay đổi bằng mô phỏng (yêu cầu cũ thử với lược đồ mới; trường máy khách cũ đọc có còn được bảo đảm)
    def sim_request(new_schema):
        old_ok = [r for r in reqs if not _hand_check(r, schema)]
        return "phá vỡ" if any(_hand_check(r, new_schema) for r in old_ok) else "tương thích"

    def sim_response(old, new):
        need = {f: old["properties"][f]["type"] for f in old.get("required", old["properties"])}
        good = all(f in new["properties"] and new["properties"][f]["type"] == t and f in new.get("required", new["properties"])
                   for f, t in need.items())
        return "tương thích" if good else "phá vỡ"

    s_purpose = dict(schema, required=schema["required"] + ["purpose"],
                     properties=dict(schema["properties"], purpose={"type": "string", "pattern": "^[0-9]{1,140}$"}))
    s_amount_str = dict(schema, properties=dict(schema["properties"], amount={"type": "string", "pattern": "^[0-9]{1,19}$"}))
    r_old = {"required": ["id", "toAccount"], "properties": {"id": {"type": "string"}, "toAccount": {"type": "string"}}}
    r_fee = {"required": ["id", "toAccount"], "properties": dict(r_old["properties"], fee={"type": "integer"})}
    r_drop = {"required": ["id"], "properties": {"id": {"type": "string"}}}
    cases = [
        (sim_request(s_purpose), alg.bnx_oas_change(schema, s_purpose, "request"), "phá vỡ", "thêm purpose bắt buộc vào yêu cầu"),
        (sim_request(s_amount_str), alg.bnx_oas_change(schema, s_amount_str, "request"), "phá vỡ", "đổi amount số nguyên → chuỗi"),
        (sim_response(r_old, r_fee), alg.bnx_oas_change(r_old, r_fee, "response"), "tương thích", "thêm fee tuỳ chọn ở phản hồi"),
        (sim_response(r_old, r_drop), alg.bnx_oas_change(r_old, r_drop, "response"), "phá vỡ", "xoá toAccount khỏi phản hồi"),
    ]
    for a, b, want, what in cases:
        rec("L01", a == b == want, f"{what}: mô phỏng {a}, checklib {b}, bài nói {want}")
    rec("L01", alg.bnx_oas_old_valid_after(["purpose"]) == sum(1 for r in reqs if not _hand_check(r, schema) and not _hand_check(r, s_purpose)) == 0,
        "bước 6: thêm purpose bắt buộc → 0 yêu cầu cũ hợp lệ còn hợp lệ")
