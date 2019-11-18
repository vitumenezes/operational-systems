import time
import random
from threading import Thread, Lock


memory_size = 0
memory = []

empty_memory = False
empty_file = False


def priority_schedule(lock):
    global memory
    global empty_memory
    global empty_file

    while (not empty_file or not empty_memory):
        lock.acquire()

        if len(memory) == 0:
            empty_memory = True
            lock.release()
            continue
        else:
            empty_memory = False

        process_time = memory[0][3]
        process_index = 0

        for i in range(len(memory)):
            if memory[i][3] < process_time:
                process_time = memory[i][3]
                process_index = i

        cpu(process_time)
        memory.pop(process_index)
        # print(memory)

        lock.release()

        time.sleep(process_time)


def cpu(_time):
    '''
    Apenas espera a quantidade de segundos passada por parametro
    '''
    # print("Esperando %d segundos" % _time)
    time.sleep(_time)


def get_safe_list(list, index):
    try:
        return list[index]
    except IndexError:
        return None


def add_process_to_memory(process):
    global memory_size
    if not (memory_size + process[4]) > 50:
        memory.append(process)
        memory_size += int(get_safe_list(process, 4))


def rewrite_hd(processes):
    with open('hdd.txt', 'w') as hd:
        hd.writelines(processes)


def read_hd():
    with open('hdd.txt', 'r') as hd:
        process = hd.readline()
        rewrite_hd(list(hd))
        return process


def watch_memory(lock):
    global memory_size
    global empty_memory
    global empty_file

    while (not empty_file or not empty_memory):
        lock.acquire()

        if memory_size >= 50:
            lock.release()
            time.sleep(1)
            continue

        line = read_hd()

        if not line:
            empty_file = True
            lock.release()
            time.sleep(1)
            continue
        else:
            empty_file = False

        process = line.replace('\n', '').split(' ')
        process = list(map(int, process))
        add_process_to_memory(process)
        lock.release()
        time.sleep(1)


def memory_manager(lock):
    watch_memory(lock)


def get_processes():
    '''
    Imprime na tela os processos em execucao
    '''
    print('PID\tNAME\tQUANTUM\tPRIORITY\tSIZE')
    for proc in memory:
        print(proc[0], '\t', proc[1], '\t', proc[2]], '\t', proc[3], '\t', proc[4])


def add_processes():
    print("Quantos processos deseja adicionar?")
    num_processes = input()




def main(lock):
    global empty_memory
    global empty_file

    while (not empty_file or not empty_memory):
        print("\nSelecione a opção desejada:")
        print("1 - Mostrar processos em execução\nAdicionar mais processos\n\nSua opcção: ")
        opc = input()

        if opc == '1':
            get_processes()
        elif opc == '2':
            add_processes(lock)
        else:
            print("Opção inválida!")


if __name__ == "__main__":
    lock_memory = Lock()
    memory_thread = Thread(target=memory_manager, args=(lock_memory, ))
    memory_thread.start()

    thread_process = Thread(target=priority_schedule, args=(lock_memory, ))
    thread_process.start()

    main(lock_memory)
