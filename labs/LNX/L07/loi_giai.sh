#!/usr/bin/env bash
set -euo pipefail
exec < <(tr -d '\r')
read -r BASE N RW SIG
shared=$((BASE + N * RW))
full=$((N * BASE))
saved=$((full - shared))
echo "shared_mb=$shared"
echo "saved_mb=$saved"
echo "oom_exit=$((128 + SIG))"
