"""Simple system monitor"""

import psutil


def get_cpu_usage(option = "all", interval = 1.0, per_cpu = False):
    return psutil.cpu_percent(interval=interval, percpu=per_cpu)


def get_mem_usage(option = "all"):
    mem = psutil.virtual_memory()
    if option == "all":
        return mem
    elif option == "total":
        return mem.total
    elif option == "available":
        return mem.available
    elif option == "percent":
        return mem.percent
    elif option == "used":
        return mem.used
    elif option == "free":
        return mem.free

def get_disk_usage(option = "all"):
    disk = psutil.disk_usage('/')
    if option == "all":
        return disk
    elif option == "total":
        return disk.total
    elif option == "free":
        return disk.free
    elif option == "used":
        return disk.used
    elif option == "percent":
        return disk.percent

if __name__ == '__main__':
    print(get_cpu_usage())
    print(get_mem_usage().percent)
    print(get_disk_usage())
