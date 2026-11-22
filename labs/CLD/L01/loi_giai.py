apps, app_mb, os_mb = 12, 40, 450
cont = apps * app_mb
vm = apps * (app_mb + os_mb)
print(f'container_mb={cont}')
print(f'vm_mb={vm}')
print(f'vm_extra_gb={(vm - cont) / 1000:.2f}')
