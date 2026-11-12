#!/usr/bin/env bash
# In số bài còn lại trong hàng dựng (dòng duy nhất trong rebuild.queue chưa có trong rebuild.done).
cd /d/research-video/audit/review/learn_final || exit 1
awk '{print $1" "$2}' rebuild.queue | sort -u > /tmp/q_ids.txt
awk '{print $1" "$2}' rebuild.done | sort -u > /tmp/d_ids.txt
comm -23 /tmp/q_ids.txt /tmp/d_ids.txt | wc -l
