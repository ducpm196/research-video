vp = lambda x, W=1280: round((x + 1.0) / 2.0 * W)
print(f"ndc_to_px={[vp(-1.0), vp(0.25), vp(1.0)]}")
