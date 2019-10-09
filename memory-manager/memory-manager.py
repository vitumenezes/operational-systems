import time
from threading import Thread, Lock

memory_size = 0
memory = []


def get_safe_list(list, index):
    try:
        return list[index]
    except IndexError:
        return None


def swap_process(new_process):
    global memory_size
    old_processs = memory.pop(0)
    memory.append(new_process)
    memory_size -= old_processs[1]


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
    print('reescrito')
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


def memory_checker(lock):
    print("PASSAGEM")
    lock.acquire()
    time.sleep(1)
    aux_list = []
    with open('hdd.txt', 'r') as hd:
        for line in hd:
            if line == '':
                print("Arquivo encerrado")
                break;
            
            process = list(line)

            if int(process[6]) == 0:
                swap_process(list(map(int, process)))
            else:
                result = str(int(line[6]) - 1)
                process[6] = result
                aux_list.append(''.join(process))
            
    rewrite_hd(aux_list)
    lock.release()
    
    memory_checker(lock)


def memory_manager(lock):
    fill_memory()
    memory_checker(lock)

if __name__ == "__main__":
    lock = Lock()
    memory_manager(lock)
    memory_time_checker = Thread(target=memory_time, args=(lock,))
    memory_time_checker.start()
