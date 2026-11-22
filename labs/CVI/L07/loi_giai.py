params = 256 * 12 + 12
augs = {
    'shift_2px': True, 'bright_10': True,
    'h_flip_2': False, 'rot180_6': False,
}
broken = sum(1 for ok in augs.values() if not ok)
print(f"head_params={params} broken_augs={broken}")
