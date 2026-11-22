#!/usr/bin/env bash
set -euo pipefail
base=120; n=10; rw=5
shared=$((base + n * rw))
full=$((n * base))
saved=$((full - shared))
echo "shared_10_mb=$shared"
echo "saved_mb=$saved"
echo "oom_exit=$((128 + 9))"
