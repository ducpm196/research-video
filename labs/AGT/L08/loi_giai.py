toks = [1500 + 400 * k for k in range(8)]
print(
    f"final_ctx={toks[-1]} total_input={sum(toks)} "
    f"mult={sum(toks) / toks[-1]:.2f}x"
)
