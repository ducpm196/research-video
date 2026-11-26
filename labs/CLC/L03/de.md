# Lab CLC L03 — Bộ đánh giá chính sách phân quyền định danh (IAM)

Đọc `stdin` `q1=<str> q2=<str> q3=<str>`. Đánh giá 3 thao tác theo quy tắc ưu tiên Deny tường minh > Allow > Deny mặc định trên hai bộ chính sách cố định:
- `p_ro = [('Allow', {'s3:GetObject'})]` (áp dụng cho `q1` → `read_allow`, và `q3` → `unmatched_default`)
- `p_mix = [('Allow', {'*'}), ('Deny', {'ec2:TerminateInstances'})]` (áp dụng cho `q2` → `terminate_deny`)

In 3 dòng: `read_allow=<ALLOW|DENY>`, `terminate_deny=<ALLOW|DENY>`, `unmatched_default=<ALLOW|DENY>`.
Chấm tự động: `bash labs/cham.sh CLC L03 duong_dan/bai_cua_ban.py`
