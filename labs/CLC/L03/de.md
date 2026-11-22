# Lab CLC L03 — Bộ đánh giá chính sách phân quyền định danh (IAM)

Viết hàm `eval_iam(policies, action)` nhận danh sách cặp `(hiệu lực, tập thao tác)`. Nếu có bất kỳ câu `'Deny'` (từ chối tường minh) khớp `action` hoặc `'*'` thì trả `'DENY'`; ngược lại nếu có `'Allow'` khớp thì trả `'ALLOW'`; mặc định `'DENY'`. Kiểm thử 3 trường hợp trên hai bộ quyền `p_ro = [('Allow', {'s3:GetObject'})]` và `p_mix = [('Allow', {'*'}), ('Deny', {'ec2:TerminateInstances'})]`: kiểm tra `'s3:GetObject'` với `p_ro` (`read_allow`), `'ec2:TerminateInstances'` với `p_mix` (`terminate_deny`) và `'iam:PassRole'` với `p_ro` (`unmatched_default`).

Định dạng đầu ra (3 dòng):
`read_allow=<ALLOW|DENY>`
`terminate_deny=<ALLOW|DENY>`
`unmatched_default=<ALLOW|DENY>`

Chấm tự động:
```bash
bash labs/cham.sh CLC L03 duong_dan/bai_cua_ban.py
```
