def eval_iam(policies, action):
    hits = [eff for eff, acts in policies if action in acts or '*' in acts]
    if 'Deny' in hits: return 'DENY'
    return 'ALLOW' if 'Allow' in hits else 'DENY'
p_ro = [('Allow', {'s3:GetObject'})]
p_mix = [('Allow', {'*'}), ('Deny', {'ec2:TerminateInstances'})]
print(f"read_allow={eval_iam(p_ro, 's3:GetObject')}")
print(f"terminate_deny={eval_iam(p_mix, 'ec2:TerminateInstances')}")
print(f"unmatched_default={eval_iam(p_ro, 'iam:PassRole')}")
