nums = [15, 6, 2]
left_assoc = (nums[0] - nums[1]) - nums[2]
right_assoc = nums[0] - (nums[1] - nums[2])
print(f"left_assoc={left_assoc} right_assoc={right_assoc}")
