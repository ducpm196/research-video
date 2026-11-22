ridge = 20e12 / 2e12
ai = 2.0
attained_tflops = min(20.0, ai * 2.0)
print(f"ridge_intensity={ridge:.1f} ai={ai:.3f} max_tflops={attained_tflops:.3f}")
