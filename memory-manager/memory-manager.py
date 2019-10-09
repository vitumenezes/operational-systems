import time
from threading import Thread, Lock

memory_size = 0
memory = []


def get_safe_list(list, index):
    try:
        return list[index]
    except IndexError:
        return None


def memory_time(lock):
    while len(memory) > 0:
        lock.acquire()
        for process in memory:
            if int(process[2]) > 0:
                process[2] -= 1
                if int(process[2]) == 0:
                    memory.remove(process)
        lock.release()
        print('yeah bab')
        # print(memory)
        time.sleep(1)


def rewrite_hd(processes):
    with open('hdd.txt', 'w') as hd:
        hd.writelines(processes)


def read_hd():
    with open('hdd.txt', 'r') as hd:
        process = hd.readline()
        rewrite_hd(list(hd))
        return process


def fill_memory():
    global memory_size
    while memory_size < 50:
        line = read_hd()
        if not line:
            print("tem mair n")
            break

        process = line.replace('\n', '').split(' ')
        process = list(map(int, process))
        memory.append(process)
        memory_size += int(get_safe_list(process, 1))


def memory_checker():
    with open('hdd.txt', 'r') as hd:
        process = hd.readline()
        rewrite_hd(list(hd))
        return process


def memory_manager():
    fill_memory()


if __name__ == "__main__":
    memory_manager()
    lock = Lock()
    memory_time_checker = Thread(target=memory_time, args=(lock,))
    memory_time_checker.start()
