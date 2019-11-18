import time
from random import randrange
from threading import Thread, Lock


memory_size = 0
memory = []

empty_memory = False
empty_file = False


def priority_schedule(lock):
    '''
    O algoritmo usado foi o de prioridade
    '''
    global memory
    global empty_memory
    global empty_file

    # enquanto houver processos na memoria ou arquivo  
    while (not empty_file or not empty_memory):
        lock.acquire()

        # seta a variavel caso a memoria esteja vazia
        if len(memory) == 0:
            empty_memory = True
            lock.release()
            continue
        else:
            empty_memory = False

        # primeiro processo da memoria
        process = memory[0]
        # index do atual processo
        process_index = 0
        i = 0
        
        for proc in memory:
            # se a prioridade for maior, troca e atualiza os indices
            if proc[3] < process[3]:
                process = proc
                process_index = i
            i += 1

        # manda o processo para a CPU
        cpu(process[2])
        # remove o processo da memoria
        memory.pop(process_index)

        lock.release()

        # espera ate tentar enviar um novo processo para a cpu (um por vez)
        time.sleep(process[2])


def cpu(_time):
    '''
    Apenas espera a quantidade de segundos passada por parametro
    '''
    global empty_memory
    global empty_file
    time.sleep(_time)
    # caso nao exista mais nenhum processo no HD ou memoria
    if (empty_file and empty_memory):
        print("Não existem processos a serem executados. Fim do programa.")
        exit(0)


def get_safe_list(list, index):
    '''
    Funcao auxiliar
    '''
    try:
        return list[index]
    except IndexError:
        return None


def add_process_to_memory(process):
    '''
    Adiciona um processo vindo do HD para a memoria
    '''
    global memory_size
    # verifica se ira passar do limite da memoria
    if not (memory_size + process[4]) > 50:
        memory.append(process)
        memory_size += int(get_safe_list(process, 4))


def rewrite_hd(processes):
    '''
    Reescreve todo o HD
    '''
    with open('hdd.txt', 'w') as hd:
        hd.writelines(processes)


def read_hd():
    '''
    Le a primeira linha do HD
    '''
    with open('hdd.txt', 'r') as hd:
        process = hd.readline()
        rewrite_hd(list(hd))
        return process


def watch_memory(lock):
    '''
    Verifica a todo momento o HD em busca de novos processos.
    A execucao ira terminar quando nao houver mais nenhum processo no HD
    e nem na memoria.
    '''
    global memory_size
    global empty_memory
    global empty_file

    while (not empty_file or not empty_memory):
        lock.acquire()

        # se a memoria estiver cheia, nao adiciona
        if memory_size >= 50:
            lock.release()
            time.sleep(1)
            continue

        line = read_hd()

        # se a linha vazia, entao HD vazio
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


def get_processes(lock):
    '''
    Imprime na tela os processos em execucao
    '''
    lock.acquire()
    print('PID\tNAME\tQUANTUM\tPRIORITY\tSIZE')
    
    for proc in memory:
        print(proc[0], '\t', proc[1], '\t', proc[2], '\t', proc[3], '\t', proc[4])

    lock.release()


def add_processes(lock):
    '''
    Adiciona n processos ao HD
    '''
    print("Quantos processos deseja adicionar?")
    num_processes = input()

    lock.acquire()

    print(type(int(num_processes)))

    for i in range(int(num_processes)):
        process = "%d 1 %d %d %d" % (randrange(100), randrange(10), randrange(3), randrange(10))
        with open('hdd.txt', 'a') as hd:
            hd.write(process+"\n")

    lock.release()


def main(lock):
    '''
    Funcao principal com menu de opcoes
    '''
    global empty_memory
    global empty_file

    # executara enquanto houver processos
    while (not empty_file or not empty_memory):
        print("\nSelecione a opção desejada:")
        print("1 - Mostrar processos em execução\n2 - Adicionar mais processos\n\nSua opção: ")
        opc = input()

        if opc == '1':
            get_processes(lock)
        elif opc == '2':
            add_processes(lock)
        else:
            print("Opção inválida!")


if __name__ == "__main__":
    lock_memory = Lock()
    # thread para observar o hd e memoria
    memory_thread = Thread(target=memory_manager, args=(lock_memory, ))
    memory_thread.start()

    # thread para realizar o escalonamento de processos
    thread_process = Thread(target=priority_schedule, args=(lock_memory, ))
    thread_process.start()

    main(lock_memory)
