errs = {
    'wrong_tool': 31, 'bad_args': 18, 'early_stop': 7, 'tool_fail': 4,
}
tot = sum(errs.values())
print(f"top_cause_pct={errs['wrong_tool'] / tot * 100:.1f}% total={tot}")
