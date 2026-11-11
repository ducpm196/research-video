"""Kiểm độc lập BNX L02 (Protocol Buffers, hạn chót). Đường khác so với tools/checklib_bnx/l02.py:
- phân tích ĐÚNG văn bản .proto đang hiện (PROTO_V1, PROTO_BAD, PROTO_RESERVED), dựng descriptor và mã/giải mã bằng thư viện
  protobuf thật (google.protobuf trong .venv), so với hàm checklib;
- chạy thật các chương trình trên màn hình (ENCODE_PY, DECODE_PY + RENUM_PY, DEADLINE_PY) bằng tiến trình Python riêng;
- hạn chót: mô phỏng đồng hồ từng mi li giây (không dùng phép trừ dồn như checklib)."""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "audit" / "bnx"))
sys.path.insert(0, str(ROOT / "audit" / "bnx" / "src"))
sys.path.insert(0, str(ROOT / "tools"))
import checklib as alg  # noqa: E402
import l02 as src  # noqa: E402


def _parse_proto(text):
    """Phân tích tối giản đúng cú pháp các tệp của bài: một message, trường `kiểu tên = số;`, `reserved số;`, `reserved "tên";`."""
    body = re.search(r"message\s+(\w+)\s*\{(.*?)\}", text, re.S)
    fields, rnums, rnames = [], [], []
    for line in body.group(2).split("\n"):
        line = line.split("//")[0].strip()
        if not line:
            continue
        m = re.fullmatch(r"(int64|string)\s+(\w+)\s*=\s*(\d+);", line)
        if m:
            fields.append((m.group(2), int(m.group(3)), m.group(1)))
            continue
        m = re.fullmatch(r'reserved\s+(\d+);', line)
        if m:
            rnums.append(int(m.group(1)))
            continue
        m = re.fullmatch(r'reserved\s+"(\w+)";', line)
        if m:
            rnames.append(m.group(1))
            continue
        raise ValueError(f"dòng .proto lạ: {line!r}")
    assert text.startswith('syntax = "proto3";')
    return body.group(1), fields, rnums, rnames


def _msg_class(tag, text):
    from google.protobuf import descriptor_pb2, descriptor_pool, message_factory
    name, fields, rnums, rnames = _parse_proto(text)
    T = descriptor_pb2.FieldDescriptorProto
    fd = descriptor_pb2.FileDescriptorProto(name=f"{tag}.proto", package=f"bnx_{tag}", syntax="proto3")
    m = fd.message_type.add(name=name)
    for fname, num, typ in fields:
        m.field.add(name=fname, number=num, label=T.LABEL_OPTIONAL, type=T.TYPE_INT64 if typ == "int64" else T.TYPE_STRING)
    for r in rnums:
        m.reserved_range.add(start=r, end=r + 1)
    m.reserved_name.extend(rnames)
    pool = descriptor_pool.DescriptorPool()
    pool.Add(fd)
    return message_factory.GetMessageClass(pool.FindMessageTypeByName(f"bnx_{tag}.{name}")), fields, rnums, rnames


def _run_py(code):
    p = subprocess.run([sys.executable, "-I", "-X", "utf8", "-B", "-c", code], capture_output=True, text=True, encoding="utf-8", timeout=60)
    return p.returncode, p.stdout.strip()


def _clock_sim(budget, costs, propagate=True):
    """Mô phỏng từng mi li giây: mỗi dịch vụ bắt đầu khi dịch vụ trước xong; bị huỷ khi đồng hồ chạm hạn của nó."""
    t, res = 0, []
    for c in costs:
        deadline = budget if propagate else t + budget   # hạn tuyệt đối mà dịch vụ này nhận
        left_at_start = deadline - t
        done = 0
        while done < c and t < deadline:
            t += 1
            done += 1
        if done < c:
            res.append(("hết giờ", left_at_start, t))
            return res
        res.append(("xong", left_at_start, t))
    return res


def run(rec):
    # 1. thư viện protobuf thật, descriptor dựng từ văn bản .proto trên màn hình
    try:
        import google.protobuf as gp
        ver = gp.__version__
    except ImportError:
        rec("L02", None, "thiếu thư viện google.protobuf — không kiểm được bằng thư viện thật")
        return
    V1, f1, _, _ = _msg_class("v1", src.PROTO_V1)
    BAD, fb, _, _ = _msg_class("bad", src.PROTO_BAD)
    RES, fr, rn, rnm = _msg_class("res", src.PROTO_RESERVED)
    rec("L02", [(n, k) for n, k, _ in f1] == [("id", 1), ("to_account", 2), ("amount", 3), ("fee", 4)]
        and "service TransferService" in src.PROTO_V1 and "rpc Create(Transfer) returns (Transfer);" in src.PROTO_V1,
        f"PROTO_V1 phân tích được: 4 trường số hiệu 1–4, dịch vụ một rpc (google.protobuf {ver})")
    b150 = V1(id=150).SerializeToString()
    rec("L02", b150.hex() == "089601" == alg.bnx_pb_field(1, 0, 150).hex(), f"protobuf thật: Transfer(id=150) → {b150.hex(' ')} = checklib")
    bs = V1(to_account="0123456789").SerializeToString()
    rec("L02", bs == alg.bnx_pb_field(2, 2, "0123456789") and len(bs) == 12 and bs[:2].hex() == "120a",
        f"protobuf thật: to_account='0123456789' → {bs.hex(' ')} (12 byte) = checklib")
    rec("L02", len(V1(id=150, to_account="0123456789").SerializeToString()) == 15, "bản tin hai trường: 3 + 12 = 15 byte (protobuf thật)")
    b300 = V1(amount=300).SerializeToString()
    rec("L02", b300.hex() == "18ac02" == alg.bnx_pb_field(3, 0, 300).hex(), f"quiz câu 1: trường 3 = 300 → {b300.hex(' ')}")
    # 2. JSON 10 byte
    js = json.dumps({"id": 150}, separators=(",", ":"))
    rec("L02", js == '{"id":150}' and len(js.encode()) == 10 == alg.bnx_json_len({"id": 150}) and 10 - len(b150) == 7,
        "JSON {\"id\":150} dài 10 byte, ít hơn 7 byte so với 3 byte nhị phân")
    # 3. đổi số hiệu: bản tin cũ (mã bằng V1) đọc bằng PROTO_BAD
    old = V1(id=150, amount=500000, fee=5500).SerializeToString()
    x = BAD.FromString(old)
    rec("L02", old.hex(" ") == "08 96 01 18 a0 c2 1e 20 fc 2a" and (x.id, x.amount, x.fee) == (150, 5500, 500000)
        and alg.bnx_pb_named(old, {1: "id", 3: "fee", 4: "amount"}) == {"id": 150, "fee": 500000, "amount": 5500},
        f"bản tin cũ {old.hex(' ')} đọc bằng PROTO_BAD (protobuf thật): amount={x.amount}, fee={x.fee}; không có lỗi nào")
    y = RES.FromString(old)
    rec("L02", rn == [2] and rnm == ["to_account"] and (y.id, y.amount, y.fee) == (150, 500000, 5500)
        and [(n, k) for n, k, _ in fr] == [("id", 1), ("amount", 3), ("fee", 4)],
        "PROTO_RESERVED: reserved 2 và \"to_account\"; bản tin cũ vẫn đọc đúng amount 500000, fee 5500")
    # 4. chạy thật chương trình trên màn hình
    rc, o = _run_py(src.ENCODE_PY)
    rec("L02", rc == 0 and o == src.ENCODE_OUT and o.splitlines()[0].startswith(b150.hex(" ")), f"chạy thật ENCODE_PY: {o.splitlines()}")
    rc, o = _run_py(src.DECODE_PY)
    rec("L02", rc == 0 and o == src.DECODE_OUT, f"chạy thật DECODE_PY: {o.splitlines()}")
    rc, o = _run_py(src.DECODE_PY + "\n" + src.RENUM_PY)
    lines = o.splitlines()
    rec("L02", rc == 0 and "\n".join(lines[2:]) == src.RENUM_OUT and f"'amount': {x.amount}" in lines[-1] and f"'fee': {x.fee}" in lines[-1],
        f"chạy thật RENUM_PY khớp protobuf thật: {lines[2:]}")
    rc, o = _run_py(src.DEADLINE_PY)
    rec("L02", rc == 0 and o == src.DEADLINE_OUT, f"chạy thật DEADLINE_PY: {o.splitlines()}")
    # 5. hạn chót: mô phỏng đồng hồ ↔ checklib
    sim = _clock_sim(2000, [800] * 3)
    lib = alg.bnx_deadline_chain(2000, [800] * 3)
    rec("L02", [(s, l) for s, l, _ in sim] == lib == [("xong", 2000), ("xong", 1200), ("hết giờ", 400)] and sim[-1][2] == 2000,
        f"hạn 2000 ms, 3 × 800 ms: mô phỏng đồng hồ {sim}; dịch vụ 3 bị huỷ đúng lúc 2000 ms")
    sim4 = _clock_sim(3000, [800] * 4)
    rec("L02", [(s, l) for s, l, _ in sim4] == alg.bnx_deadline_chain(3000, [800] * 4) and sim4[-1][:2] == ("hết giờ", 600),
        f"quiz câu 2: hạn 3000 ms, 4 × 800 ms → dịch vụ 4 hết giờ khi còn 600 ms {sim4}")
    reset = _clock_sim(2000, [800] * 3, propagate=False)
    rec("L02", [s for s, _, _ in reset] == ["xong"] * 3 and reset[-1][2] == 2400 and reset[-1][2] - 2000 == alg.bnx_deadline_wasted(2000, [800] * 3) == 400,
        f"lỗi 3: mỗi dịch vụ đặt lại 2 giây → chuỗi xong ở {reset[-1][2]} ms, quá hạn người dùng 400 ms")
    # 6. phép tính nền
    rec("L02", int("10010110", 2) == 0x96 == 150 and (1 << 3, 150 >> 7, 150 & 127, 22 | 128) == (8, 1, 22, 150)
        and alg.bnx_pb_key(2, 2) == 18 and len(alg.bnx_pb_varint(5)) == 1 and len(alg.bnx_pb_varint(150)) == 2,
        "ôn nền: 1001 0110 = 0x96 = 150; 1<<3 = 8; 150>>7 = 1; 150&127 = 22; khoá trường 2 kiểu 2 = 18")
