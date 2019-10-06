
from time import sleep
from threading import Thread


def threadFunction(waiting_time):
    print('\tEsperando %s segundos' % waiting_time)
    sleep(waiting_time)


n = -1
def prioritySchedule(processes):
    for i in range(4):
        print(f'Processos de prioridade %d sendo executados:' % i)
        for j in range(3):
            global n
            n += 1
            thread = processes[i][n % len(processes[i])]
            cpu(thread)
            # Espera a thread finalizar
            thread.join()


def cpu(thread):
    '''
    Apenas inicia a thread
    '''
    thread.start()


def main():
    '''
    Agora cada posicao do vetor de vetor indica uma prioridade, sendo 0 a mais
    alta. Todos os processos/threads daquele indice serao executados, dai entao
    a proxima prioridade entrara na fila. Utilizei 4 prioridades e 3 threads
    para cada uma.
    '''
    processes = []
    # Tempos definidos estaticamente
    waiting_times = [2,3,4]

    for i in range(4):
        priority = []
        for j in range(3):
            thread = Thread(target=threadFunction, args=[waiting_times[j]])
            priority.append(thread)
        processes.append(priority)

    prioritySchedule(processes)


if __name__ == '__main__':
    main()
