from time import sleep
from threading import Thread


def threadFunction(waiting_time):
    print('Esperando %s segundos' % waiting_time)
    sleep(waiting_time)


n = -1
def roundRobin(processes):
    '''
    Deixei apenas uma execucao. Nao encontrei um modo de fazer com que a thread
    execute a funcao novamente. A funcao run deveria fazer isso, mas precisa do
    start() (que ja executa a thread uma vez). Se houver um jeito de iniciar a
    thread sem que ela execute a funcao de inicio, o codigo pode ser consertado.
    '''
    for i in range(3):
        # Necessita ser global para sempre ser incrementada (caso o laco seja infinito)
        global n
        n += 1

        # Posicao corrente, de forma circular (inicio ao fim)
        thread = processes[n % len(processes)]
        cpu(thread)

        # Espera a thread finalizar
        thread.join()


def cpu(thread):
    '''
    Apenas inicia a thread
    '''
    thread.start()


def main():
    processes = []
    # Tempos definidos estaticamente

    waiting_times = [2,3,4]
    for i in range(3):
        thread = Thread(target=threadFunction, args=[waiting_times[i]])
        processes.append(thread)

    roundRobin(processes)


if __name__ == '__main__':
    main()
