#!/usr/bin/env bash
# Chạy sau khi máy chủ đã chạy ở cửa sổ khác (java MayChu.java).
curl -s -w "\n" -X POST localhost:8099/chuyen
curl -s -w "\n" -X POST localhost:8099/chuyen
curl -s -w "\n" -X POST localhost:8099/chuyen
curl -s -w "\n" -X POST localhost:8099/chuyen-co-khoa -H "Idempotency-Key: abc"
curl -s -w "\n" -X POST localhost:8099/chuyen-co-khoa -H "Idempotency-Key: abc"
curl -s -w "\n" -X POST localhost:8099/chuyen-co-khoa -H "Idempotency-Key: abc"
