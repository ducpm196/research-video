# Lab AIP L04 — Trình quản lý Intent/Slot nhiều lượt & Agentic Tool Guardrail

Đọc từ `stdin` 3 dòng:
- Dòng 1: `turns=<intent:k=v,k=v;...>` (các lượt ngăn cách bằng `;`, nếu không có đổi intent thì phần đầu ghi `KEEP`)
- Dòng 2: `required_slots=<k1,k2,...>`
- Dòng 3: `allow=<t1,t2,...> max_steps=<int> calls=<tool:arg_int,...>` (`arg` hợp lệ phải phân tích được thành số nguyên > 0)

Yêu cầu:
1. Duyệt qua từng lượt: nếu `intent != 'KEEP'` và `intent != cur_intent`, cập nhật `cur_intent = intent` và xoá sạch `slots = {}`; sau đó cập nhật `slots` từ các cặp `k=v` của lượt đó. Cuối cùng kiểm tra `slots_ready = int(set(required_slots) <= set(slots))`.
2. Duyệt từng lệnh gọi trong `calls`: chỉ cho phép thực thi (`executed += 1`) nếu `executed < max_steps`, `tool in allow` và đối số chuyển được sang số nguyên `> 0`; ngược lại tăng `blocked += 1`.
3. In đúng 3 dòng: `final_intent=<str> slots_ready=<0|1>`, `executed_tools=<int>`, `blocked_tools=<int>`.

Chấm tự động: `bash labs/cham.sh AIP L04 duong_dan/bai_cua_ban.py`
