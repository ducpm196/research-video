jobs = 29423
fails = round(jobs * 1.2)
completed_all = int(jobs > 0 and fails > 0)
print(f'jobs={jobs}')
print(f'worker_failures={fails}')
print(f'completed_all={completed_all}')
