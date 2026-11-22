import math
proof_hashes = int(math.log2(4096))
proof_bytes = proof_hashes * 32
print(f"merkle_hashes={proof_hashes} proof_bytes={proof_bytes}")
