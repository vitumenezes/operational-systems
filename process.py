import psutil
import pprint
import time
import os
import signal


def getListOfProcessSortedByMemory():
    '''
    Recupera a lista de processos do sistema
    '''
    process_list = []
    # iteracao sobre todos os processos
    for proc in psutil.process_iter():
       try:
           pinfo = proc.as_dict(attrs=['pid', 'name', 'username'])
           pinfo['vms'] = proc.memory_info().vms / (1024 * 1024)
           process_list.append(pinfo);
       except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
           pass

    process_list = sorted(process_list, key=lambda procObj: procObj['vms'], reverse=True)
    return process_list


def getProcess():
    '''
    Imprime na tela os processos em execucao
    '''
    # lista de processos
    listOfRunningProcess = getListOfProcessSortedByMemory()
    # filtrei apenas pelos com python3, assim ficaria mais visivel a duplicacao
    listProc = (elem for elem in listOfRunningProcess if elem['name'] == 'python3')

    os.system('clear')
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)
    print('MEMORYUSAGE\tPID\tUSERNAME\tNAME')
    for elem in listProc:
        print(elem['vms'], '\t', elem['pid'], '\t', elem['username'], '\t', elem['name'])

    # killProcess()


def killProcess():
    '''
    Mata um processo
    '''
    process = input('\nDigite o PID do processo:')
    os.kill(int(process), signal.SIGKILL)
    getProcess()


def processFunc():
    '''
    Fork a cada 10 segundos. O filho chama a funcao novamente
    '''
    for i in range(3):
        time.sleep(10)
        pid = os.fork()
        if pid > 0:
            continue
        else:
            processFunc()
    # Ao final, morre
    exit()


def main():
    getProcess()
    pid = os.fork()
    if pid < 0:
        print("Erro")
    elif pid > 0:
        getProcess()
    else:
        processFunc()


if __name__ == '__main__':
    main()
    # Ainda faltam alguns tratamentos de excecoes
    while True:
        print('\n1 - Atualizar\n2 - Matar processo')
        opc = input('\nDigite a opção: ')
        print(opc)
        if opc == '1':
            getProcess()
        elif opc == '2':
            killProcess()
        else:
            continue
